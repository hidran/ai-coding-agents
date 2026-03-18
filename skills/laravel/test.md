---
name: laravel-test
description: Generates Laravel Feature and Unit tests with factories, HTTP testing, database assertions, and mocking. Supports both PHPUnit and Pest.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Laravel Test Generator

## Usage
Run `/laravel-test <ModelName>` or `/laravel-test <ClassName>`

## Structure
Generates:
- `tests/Feature/<Model>ControllerTest.php`: HTTP/Feature tests
- `tests/Unit/<Model>ServiceTest.php`: Unit tests (if service exists)
- `database/factories/<Model>Factory.php`: Model factory (if not exists)

## Process
1. Detect testing framework (PHPUnit or Pest) from `phpunit.xml` or `tests/Pest.php`
2. Read the source class to understand methods and dependencies
3. Generate factory if model is involved
4. Generate Feature tests for controller endpoints
5. Generate Unit tests for service/business logic

## Standards
- **RefreshDatabase**: Feature tests use `RefreshDatabase` trait
- **Factories**: Always use model factories, never manual `DB::insert` or `Model::create` with raw data
- **HTTP testing**: Use `$this->getJson()`, `$this->postJson()` etc. for API tests
- **Authentication**: Use `$this->actingAs()` with factory-created users
- **Assertions**: Use Laravel-specific assertions (`assertDatabaseHas`, `assertJsonStructure`, `assertRedirect`)
- **One concern per test**: Each test method tests one behavior
- **Descriptive names**: `test_user_can_create_post_with_valid_data`

## Examples

### 1. Model Factory

```php
<?php

namespace Database\Factories;

use App\Models\Post;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends Factory<Post>
 */
class PostFactory extends Factory
{
    protected $model = Post::class;

    public function definition(): array
    {
        $title = fake()->sentence();

        return [
            'user_id' => User::factory(),
            'title' => $title,
            'slug' => Str::slug($title),
            'content' => fake()->paragraphs(3, asText: true),
            'published_at' => null,
        ];
    }

    public function published(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => now(),
        ]);
    }

    public function draft(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => null,
        ]);
    }

    public function featured(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_featured' => true,
            'published_at' => now(),
        ]);
    }

    public function configure(): static
    {
        return $this->afterCreating(function (Post $post) {
            $post->tags()->attach(
                \App\Models\Tag::factory()->count(3)->create()
            );
        });
    }
}

// Sequence usage:
// Post::factory()
//     ->count(4)
//     ->sequence(
//         ['status' => 'draft'],
//         ['status' => 'published'],
//         ['status' => 'archived'],
//         ['status' => 'draft'],
//     )
//     ->create();
```

### 2. Feature Test (PHPUnit)

```php
<?php

namespace Tests\Feature;

use App\Models\Post;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostControllerTest extends TestCase
{
    use RefreshDatabase;

    private User $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
    }

    public function test_guest_cannot_access_posts_create(): void
    {
        $response = $this->getJson('/api/posts/create');

        $response->assertUnauthorized();
    }

    public function test_user_can_list_posts(): void
    {
        Post::factory()->count(3)->for($this->user)->create();

        $response = $this->actingAs($this->user)
            ->getJson('/api/posts');

        $response->assertOk()
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'title', 'slug', 'content', 'published_at', 'created_at'],
                ],
                'meta' => ['current_page', 'last_page', 'per_page', 'total'],
            ]);
    }

    public function test_user_can_create_post_with_valid_data(): void
    {
        $payload = [
            'title' => 'My New Post',
            'content' => 'This is the post content.',
        ];

        $response = $this->actingAs($this->user)
            ->postJson('/api/posts', $payload);

        $response->assertCreated()
            ->assertJsonPath('data.title', 'My New Post');

        $this->assertDatabaseHas('posts', [
            'user_id' => $this->user->id,
            'title' => 'My New Post',
        ]);
    }

    public function test_create_post_fails_with_invalid_data(): void
    {
        $response = $this->actingAs($this->user)
            ->postJson('/api/posts', []);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['title', 'content']);
    }

    public function test_user_can_update_own_post(): void
    {
        $post = Post::factory()->for($this->user)->create();

        $response = $this->actingAs($this->user)
            ->putJson("/api/posts/{$post->id}", [
                'title' => 'Updated Title',
                'content' => $post->content,
            ]);

        $response->assertOk()
            ->assertJsonPath('data.title', 'Updated Title');

        $this->assertDatabaseHas('posts', [
            'id' => $post->id,
            'title' => 'Updated Title',
        ]);
    }

    public function test_user_cannot_update_others_post(): void
    {
        $otherUser = User::factory()->create();
        $post = Post::factory()->for($otherUser)->create();

        $response = $this->actingAs($this->user)
            ->putJson("/api/posts/{$post->id}", [
                'title' => 'Hijacked Title',
                'content' => 'Hijacked content.',
            ]);

        $response->assertForbidden();
    }

    public function test_user_can_delete_post(): void
    {
        $post = Post::factory()->for($this->user)->create();

        $response = $this->actingAs($this->user)
            ->deleteJson("/api/posts/{$post->id}");

        $response->assertNoContent();

        $this->assertDatabaseMissing('posts', [
            'id' => $post->id,
        ]);
    }

    public function test_posts_are_paginated(): void
    {
        Post::factory()->count(25)->for($this->user)->create();

        $response = $this->actingAs($this->user)
            ->getJson('/api/posts');

        $response->assertOk()
            ->assertJsonPath('meta.total', 25)
            ->assertJsonPath('meta.per_page', 15)
            ->assertJsonCount(15, 'data');
    }
}
```

### 3. Feature Test (Pest)

```php
<?php

use App\Models\Post;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->user = User::factory()->create();
});

it('prevents guests from accessing post creation', function () {
    $this->getJson('/api/posts/create')
        ->assertUnauthorized();
});

it('lists posts with pagination', function () {
    Post::factory()->count(25)->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->getJson('/api/posts');

    $response->assertOk();

    expect($response->json('meta.total'))->toBe(25)
        ->and($response->json('meta.per_page'))->toBe(15)
        ->and($response->json('data'))->toHaveCount(15);
});

it('creates a post with valid data', function () {
    $payload = [
        'title' => 'My New Post',
        'content' => 'This is the post content.',
    ];

    $response = $this->actingAs($this->user)
        ->postJson('/api/posts', $payload);

    $response->assertCreated();

    expect($response->json('data.title'))->toBe('My New Post');

    $this->assertDatabaseHas('posts', [
        'user_id' => $this->user->id,
        'title' => 'My New Post',
    ]);
});

it('fails validation with missing title', function () {
    $response = $this->actingAs($this->user)
        ->postJson('/api/posts', ['content' => 'Some content.']);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors(['title']);
});

it('fails validation for various invalid inputs', function (array $payload, string $errorField) {
    $response = $this->actingAs($this->user)
        ->postJson('/api/posts', $payload);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors([$errorField]);
})->with([
    'missing title' => [['content' => 'Some content'], 'title'],
    'missing content' => [['title' => 'A Title'], 'content'],
    'title too long' => [['title' => str_repeat('a', 256), 'content' => 'Content'], 'title'],
    'title not a string' => [['title' => 123, 'content' => 'Content'], 'title'],
]);

it('allows a user to update their own post', function () {
    $post = Post::factory()->for($this->user)->create();

    $response = $this->actingAs($this->user)
        ->putJson("/api/posts/{$post->id}", [
            'title' => 'Updated Title',
            'content' => $post->content,
        ]);

    $response->assertOk();
    expect($response->json('data.title'))->toBe('Updated Title');
});

it('forbids a user from updating another users post', function () {
    $otherUser = User::factory()->create();
    $post = Post::factory()->for($otherUser)->create();

    $this->actingAs($this->user)
        ->putJson("/api/posts/{$post->id}", [
            'title' => 'Hijacked',
            'content' => 'Hijacked content.',
        ])
        ->assertForbidden();
});

it('deletes a post and removes it from the database', function () {
    $post = Post::factory()->for($this->user)->create();

    $this->actingAs($this->user)
        ->deleteJson("/api/posts/{$post->id}")
        ->assertNoContent();

    $this->assertDatabaseMissing('posts', ['id' => $post->id]);
});
```

### 4. Unit Test (PHPUnit)

```php
<?php

namespace Tests\Unit;

use App\Models\Post;
use App\Repositories\PostRepositoryInterface;
use App\Services\PostService;
use Illuminate\Support\Str;
use Mockery;
use Mockery\MockInterface;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

class PostServiceTest extends TestCase
{
    private PostService $service;
    private MockInterface $repository;

    protected function setUp(): void
    {
        parent::setUp();

        $this->repository = Mockery::mock(PostRepositoryInterface::class);
        $this->service = new PostService($this->repository);
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }

    public function test_it_generates_unique_slug_from_title(): void
    {
        $this->repository
            ->shouldReceive('slugExists')
            ->with('my-first-post')
            ->once()
            ->andReturn(false);

        $slug = $this->service->generateSlug('My First Post');

        $this->assertSame('my-first-post', $slug);
    }

    public function test_it_appends_suffix_when_slug_already_exists(): void
    {
        $this->repository
            ->shouldReceive('slugExists')
            ->with('my-first-post')
            ->once()
            ->andReturn(true);

        $this->repository
            ->shouldReceive('slugExists')
            ->with('my-first-post-1')
            ->once()
            ->andReturn(false);

        $slug = $this->service->generateSlug('My First Post');

        $this->assertSame('my-first-post-1', $slug);
    }

    public function test_it_schedules_publish_in_the_future(): void
    {
        $publishAt = now()->addDays(7);

        $this->repository
            ->shouldReceive('update')
            ->once()
            ->withArgs(function (int $id, array $data) use ($publishAt) {
                return $id === 1
                    && $data['published_at']->equalTo($publishAt);
            })
            ->andReturn(true);

        $result = $this->service->schedulePublish(postId: 1, publishAt: $publishAt);

        $this->assertTrue($result);
    }

    public function test_it_throws_exception_for_past_publish_date(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Publish date must be in the future');

        $this->service->schedulePublish(postId: 1, publishAt: now()->subDay());
    }

    #[DataProvider('slugDataProvider')]
    public function test_slug_generation_edge_cases(string $input, string $expected): void
    {
        $this->repository
            ->shouldReceive('slugExists')
            ->andReturn(false);

        $slug = $this->service->generateSlug($input);

        $this->assertSame($expected, $slug);
    }

    public static function slugDataProvider(): array
    {
        return [
            'special characters' => ['Hello @World! #2024', 'hello-world-2024'],
            'extra spaces' => ['  Too   Many   Spaces  ', 'too-many-spaces'],
            'unicode characters' => ['Cafe avec creme', 'cafe-avec-creme'],
            'already a slug' => ['already-a-slug', 'already-a-slug'],
            'numbers only' => ['12345', '12345'],
        ];
    }
}
```

## Template Variables

When generating tests, the skill replaces the following placeholders based on the target model or class:

| Variable | Description | Example |
|---|---|---|
| `<Model>` | Pascal case model name | `Post` |
| `<model>` | Camel case variable name | `post` |
| `<models>` | Plural lowercase for routes | `posts` |
| `<table>` | Database table name | `posts` |
| `<prefix>` | API route prefix | `/api` |

## Detection Logic

The skill auto-detects the testing framework:

1. If `tests/Pest.php` exists, generate Pest syntax
2. If `phpunit.xml` exists without Pest, generate PHPUnit syntax
3. If both exist, prefer Pest
4. Check `composer.json` for `pestphp/pest` dependency as a fallback
