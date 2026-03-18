---
name: laravel-feature
description: Generates a Laravel feature set including Model, Migration, Controller, FormRequest, and Policy.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel Feature Generator

This skill scaffolds a complete feature in a Laravel application.

## Usage
Run `/laravel-feature <ModelName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure
Generates:
- `app/Models/<Model>.php`: Eloquent model.
- `database/migrations/xxxx_xx_xx_create_<table_name>_table.php`: Database schema.
- `app/Http/Controllers/<Model>Controller.php`: Resource controller.
- `app/Http/Requests/Store<Model>Request.php`: Validation logic.
- `app/Policies/<Model>Policy.php`: Authorization logic.
- `routes/api.php` or `web.php`: Route registration.

## Standards
- **Type Hinting**: Use PHP type hints and return types.
- **Validation**: Always use FormRequests, never validate in the controller.
- **Authorization**: Use Policies for resource access control.
- **API Resources**: Use API Resources for JSON transformation.
- **Mass Assignment**: Define `$fillable` or `$guarded` in models.

## Examples

### Controller
```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Http\Requests\StorePostRequest;
use App\Http\Resources\PostResource;
use Illuminate\Http\JsonResponse;

class PostController extends Controller
{
    public function index(): JsonResponse
    {
        $posts = Post::with('author')->paginate(10);
        return PostResource::collection($posts)->response();
    }

    public function store(StorePostRequest $request): JsonResponse
    {
        $post = $request->user()->posts()->create($request->validated());
        return (new PostResource($post))
            ->response()
            ->setStatusCode(201);
    }
}
```

### Form Request
```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Authorization handled by Policy/Middleware
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'content' => ['required', 'string'],
            'published_at' => ['nullable', 'date'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
        ];
    }
}
```

### Model
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'content',
        'published_at',
        'user_id',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }
}
```
