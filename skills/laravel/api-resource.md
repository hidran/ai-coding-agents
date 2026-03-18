---
name: laravel-api-resource
description: Generates Laravel API Resource and Collection classes for JSON transformation with conditional attributes, relationships, and pagination meta.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel API Resource Generator

## Usage

Run `/laravel-api-resource <ModelName>` to generate API Resource and Collection classes for the given Eloquent model.

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure

Generates the following files:

- `app/Http/Resources/<Model>Resource.php` -- Single resource transformation
- `app/Http/Resources/<Model>Collection.php` -- Collection with pagination meta
- Updates the corresponding controller to use the generated resources

## Standards

- **Conditional attributes**: Use `$this->when()`, `$this->whenLoaded()`, `$this->whenCounted()`
- **Nested resources**: Use other Resource classes for relationships
- **Pagination meta**: Include links and meta in collections
- **Consistent envelope**: `{ "data": [...], "meta": {...}, "links": {...} }`
- **Type hints**: Return types on `toArray()`
- **Wrapping**: Use `$wrap` property when needed

## Steps

1. Identify the model name from the user input.
2. Use `Glob` and `Grep` to locate the Eloquent model and inspect its relationships, casts, and fillable attributes.
3. Generate the Resource class at `app/Http/Resources/<Model>Resource.php`.
4. Generate the Collection class at `app/Http/Resources/<Model>Collection.php`.
5. Locate the corresponding controller and update its methods to return the new Resource and Collection classes.

## Examples

### 1. Resource Class

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'excerpt' => $this->excerpt,
            'content' => $this->content,
            'is_featured' => $this->is_featured,
            'published_at' => $this->published_at?->toIso8601String(),
            'created_at' => $this->created_at->toIso8601String(),

            // Conditional relationship: only included when eager-loaded
            'author' => new UserResource($this->whenLoaded('author')),

            // Conditional collection relationship
            'tags' => TagResource::collection($this->whenLoaded('tags')),

            // Conditional count: only included when withCount('comments') was used
            'comments_count' => $this->whenCounted('comments'),

            // Conditional field: only included when the model attribute is truthy
            'featured_position' => $this->when($this->is_featured, fn () => $this->featured_position),

            // Admin-only fields: merged into the response conditionally
            $this->mergeWhen($request->user()?->isAdmin(), fn () => [
                'internal_notes' => $this->internal_notes,
                'moderation_status' => $this->moderation_status,
                'updated_at' => $this->updated_at->toIso8601String(),
            ]),
        ];
    }
}
```

### 2. Collection Class

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class PostCollection extends ResourceCollection
{
    /**
     * The resource that this resource collects.
     *
     * @var string
     */
    public $collects = PostResource::class;

    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total_published' => $this->collection->filter(
                    fn ($post) => $post->published_at !== null
                )->count(),
            ],
        ];
    }
}
```

The resulting JSON envelope when used with pagination:

```json
{
    "data": [
        { "id": 1, "title": "..." }
    ],
    "meta": {
        "total_published": 42,
        "current_page": 1,
        "last_page": 5,
        "per_page": 15,
        "total": 73
    },
    "links": {
        "first": "https://example.com/api/posts?page=1",
        "last": "https://example.com/api/posts?page=5",
        "prev": null,
        "next": "https://example.com/api/posts?page=2"
    }
}
```

### 3. Controller Usage

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\PostCollection;
use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class PostController extends Controller
{
    /**
     * Display a listing of posts.
     */
    public function index(Request $request): PostCollection
    {
        $posts = Post::query()
            ->with(['author', 'tags'])
            ->withCount('comments')
            ->latest('published_at')
            ->paginate($request->integer('per_page', 15));

        return new PostCollection($posts);
    }

    /**
     * Display the specified post.
     */
    public function show(Post $post): PostResource
    {
        $post->load(['author', 'tags']);
        $post->loadCount('comments');

        return new PostResource($post);
    }

    /**
     * Store a newly created post.
     */
    public function store(StorePostRequest $request): JsonResponse
    {
        $post = Post::create($request->validated());

        $post->load(['author', 'tags']);

        return (new PostResource($post))
            ->response()
            ->setStatusCode(201);
    }

    /**
     * Update the specified post.
     */
    public function update(UpdatePostRequest $request, Post $post): PostResource
    {
        $post->update($request->validated());

        $post->load(['author', 'tags']);
        $post->loadCount('comments');

        return new PostResource($post);
    }

    /**
     * Remove the specified post.
     */
    public function destroy(Post $post): JsonResponse
    {
        $post->delete();

        return response()->json(null, 204);
    }
}
```

### 4. Conditional Response

Use `->additional()` to attach extra top-level data and `->response()->header()` for custom headers:

```php
/**
 * Display a listing of posts with additional metadata.
 */
public function index(Request $request): JsonResponse
{
    $posts = Post::query()
        ->with(['author', 'tags'])
        ->withCount('comments')
        ->latest('published_at')
        ->paginate($request->integer('per_page', 15));

    return (new PostCollection($posts))
        ->additional([
            'meta' => [
                'filters_applied' => $request->only(['status', 'author_id', 'tag']),
                'generated_at' => now()->toIso8601String(),
            ],
        ])
        ->response()
        ->header('X-Total-Count', (string) $posts->total())
        ->header('X-Page-Count', (string) $posts->lastPage());
}

/**
 * Display a single post with conditional additional data.
 */
public function show(Request $request, Post $post): JsonResponse
{
    $post->load(['author', 'tags']);
    $post->loadCount('comments');

    return (new PostResource($post))
        ->additional([
            'meta' => [
                'related_posts' => PostResource::collection(
                    $post->relatedPosts()->limit(3)->get()
                ),
            ],
        ])
        ->response()
        ->header('Cache-Control', 'public, max-age=60');
}
```
