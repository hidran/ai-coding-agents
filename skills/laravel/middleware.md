---
name: laravel-middleware
description: Generates Laravel HTTP middleware with before/after/terminable patterns, route registration, and tests.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Laravel Middleware Generator

## Usage

Run `/laravel-middleware <MiddlewareName>`

The skill generates a complete middleware class and its corresponding feature test, following Laravel 11+ conventions and PHP 8.2+ standards.

## Structure

Generates the following files:

- `app/Http/Middleware/<MiddlewareName>.php` -- Middleware class
- `tests/Feature/Middleware/<MiddlewareName>Test.php` -- Middleware tests

## Standards

- **Single responsibility**: One middleware, one concern. Do not bundle unrelated checks into a single middleware.
- **Before vs After**: Use before middleware for validation, authentication, and request gating. Use after middleware for response modification (headers, formatting).
- **Terminable**: Use `terminate()` for work that should happen after the response has been sent to the browser, such as logging or cleanup.
- **Parameters**: Support middleware parameters passed via route definitions (e.g., `middleware('name:param1,param2')`).
- **Type hints**: Always provide full type hints on `handle()`, `terminate()`, and any other public methods.
- **Response handling**: Return proper HTTP responses (403, 429, 406, etc.) with structured JSON bodies instead of using `abort()`.

## Examples

### 1. Before Middleware -- EnsureApiVersion

Checks the `Accept` header for a versioned media type and rejects requests that do not match.

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class EnsureApiVersion
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): Response  $next
     */
    public function handle(Request $request, Closure $next, string $version = 'v1'): Response
    {
        $accept = $request->header('Accept', '');
        $expected = "application/vnd.api+json; version={$version}";

        if (! str_contains($accept, "version={$version}")) {
            return response()->json([
                'error' => 'Not Acceptable',
                'message' => "This endpoint requires Accept header: {$expected}",
            ], Response::HTTP_NOT_ACCEPTABLE);
        }

        $request->attributes->set('api_version', $version);

        return $next($request);
    }
}
```

### 2. After Middleware -- AddSecurityHeaders

Adds security headers to every response. Header values are pulled from `config/security.php`.

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class AddSecurityHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): Response  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        $headers = [
            'X-Content-Type-Options' => config('security.headers.x_content_type_options', 'nosniff'),
            'X-Frame-Options' => config('security.headers.x_frame_options', 'SAMEORIGIN'),
            'Strict-Transport-Security' => config('security.headers.strict_transport_security', 'max-age=31536000; includeSubDomains'),
            'X-XSS-Protection' => config('security.headers.x_xss_protection', '1; mode=block'),
            'Content-Security-Policy' => config('security.headers.content_security_policy', "default-src 'self'"),
            'Referrer-Policy' => config('security.headers.referrer_policy', 'strict-origin-when-cross-origin'),
        ];

        foreach ($headers as $key => $value) {
            $response->headers->set($key, $value);
        }

        return $response;
    }
}
```

The accompanying config file (`config/security.php`):

```php
<?php

return [
    'headers' => [
        'x_content_type_options' => 'nosniff',
        'x_frame_options' => 'SAMEORIGIN',
        'strict_transport_security' => 'max-age=31536000; includeSubDomains',
        'x_xss_protection' => '1; mode=block',
        'content_security_policy' => "default-src 'self'",
        'referrer_policy' => 'strict-origin-when-cross-origin',
    ],
];
```

### 3. Rate Limiting Middleware -- ThrottleByTeam

Custom rate limiting scoped to the authenticated user's team rather than the individual user.

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

final class ThrottleByTeam
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): Response  $next
     */
    public function handle(Request $request, Closure $next, int $maxAttempts = 60, int $decaySeconds = 60): Response
    {
        $team = $request->user()?->currentTeam;

        if (! $team) {
            return $next($request);
        }

        $key = "team:{$team->id}";

        if (RateLimiter::tooManyAttempts($key, $maxAttempts)) {
            $retryAfter = RateLimiter::availableIn($key);

            return response()->json([
                'error' => 'Too Many Requests',
                'message' => 'Your team has exceeded the rate limit.',
                'retry_after' => $retryAfter,
            ], Response::HTTP_TOO_MANY_REQUESTS)
                ->withHeaders([
                    'Retry-After' => $retryAfter,
                    'X-RateLimit-Limit' => $maxAttempts,
                    'X-RateLimit-Remaining' => RateLimiter::remaining($key, $maxAttempts),
                ]);
        }

        RateLimiter::hit($key, $decaySeconds);

        $response = $next($request);

        return $response->withHeaders([
            'X-RateLimit-Limit' => $maxAttempts,
            'X-RateLimit-Remaining' => RateLimiter::remaining($key, $maxAttempts),
        ]);
    }
}
```

### 4. Terminable Middleware -- LogApiRequest

Implements both `handle()` and `terminate()`. The heavy logging work runs after the response has already been sent to the client.

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;

final class LogApiRequest
{
    /**
     * Handle an incoming request.
     *
     * @param  Closure(Request): Response  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $request->attributes->set('request_start_time', microtime(true));

        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        $startTime = $request->attributes->get('request_start_time');
        $duration = $startTime ? round((microtime(true) - $startTime) * 1000, 2) : null;

        Log::channel('api')->info('API Request', [
            'method' => $request->method(),
            'url' => $request->fullUrl(),
            'status' => $response->getStatusCode(),
            'duration_ms' => $duration,
            'ip' => $request->ip(),
            'user_id' => $request->user()?->id,
        ]);
    }
}
```

### 5. Registration (Laravel 11+)

Laravel 11 registers middleware in `bootstrap/app.php` rather than a kernel class.

#### Global middleware, aliases, and groups

```php
<?php

use App\Http\Middleware\AddSecurityHeaders;
use App\Http\Middleware\EnsureApiVersion;
use App\Http\Middleware\LogApiRequest;
use App\Http\Middleware\ThrottleByTeam;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        // Global middleware -- runs on every request
        $middleware->append(AddSecurityHeaders::class);
        $middleware->append(LogApiRequest::class);

        // Aliases -- usable in route definitions
        $middleware->alias([
            'ensure-api-version' => EnsureApiVersion::class,
            'throttle-team' => ThrottleByTeam::class,
        ]);

        // Group middleware -- add to existing groups
        $middleware->appendToGroup('api', [
            LogApiRequest::class,
        ]);
    })
    ->create();
```

#### Route-level usage

```php
use Illuminate\Support\Facades\Route;

// With parameter
Route::middleware('ensure-api-version:v2')->group(function () {
    Route::get('/resources', [ResourceController::class, 'index']);
});

// With multiple parameters
Route::middleware('throttle-team:100,120')->group(function () {
    Route::post('/uploads', [UploadController::class, 'store']);
});

// Combining middleware
Route::middleware(['ensure-api-version:v2', 'throttle-team:30,60'])->group(function () {
    Route::apiResource('projects', ProjectController::class);
});

// Single route
Route::get('/status', StatusController::class)
    ->middleware('ensure-api-version:v1');
```

### 6. Tests -- EnsureApiVersion

```php
<?php

declare(strict_types=1);

namespace Tests\Feature\Middleware;

use App\Http\Middleware\EnsureApiVersion;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

final class EnsureApiVersionTest extends TestCase
{
    private EnsureApiVersion $middleware;

    protected function setUp(): void
    {
        parent::setUp();
        $this->middleware = new EnsureApiVersion();
    }

    #[Test]
    public function it_passes_request_with_correct_version_header(): void
    {
        $request = Request::create('/api/test', 'GET');
        $request->headers->set('Accept', 'application/vnd.api+json; version=v1');

        $response = $this->middleware->handle($request, fn () => new Response('OK'));

        $this->assertEquals(200, $response->getStatusCode());
        $this->assertEquals('v1', $request->attributes->get('api_version'));
    }

    #[Test]
    public function it_rejects_request_with_wrong_version_header(): void
    {
        $request = Request::create('/api/test', 'GET');
        $request->headers->set('Accept', 'application/vnd.api+json; version=v1');

        $response = $this->middleware->handle($request, fn () => new Response('OK'), 'v2');

        $this->assertEquals(406, $response->getStatusCode());
        $this->assertStringContainsString('Not Acceptable', $response->getContent());
    }

    #[Test]
    public function it_rejects_request_with_missing_accept_header(): void
    {
        $request = Request::create('/api/test', 'GET');

        $response = $this->middleware->handle($request, fn () => new Response('OK'), 'v2');

        $this->assertEquals(406, $response->getStatusCode());
    }

    #[Test]
    public function it_uses_default_version_when_no_parameter_provided(): void
    {
        $request = Request::create('/api/test', 'GET');
        $request->headers->set('Accept', 'application/vnd.api+json; version=v1');

        $response = $this->middleware->handle($request, fn () => new Response('OK'));

        $this->assertEquals(200, $response->getStatusCode());
        $this->assertEquals('v1', $request->attributes->get('api_version'));
    }

    #[Test]
    public function it_sets_api_version_on_request_attributes(): void
    {
        $request = Request::create('/api/test', 'GET');
        $request->headers->set('Accept', 'application/vnd.api+json; version=v2');

        $this->middleware->handle($request, fn () => new Response('OK'), 'v2');

        $this->assertEquals('v2', $request->attributes->get('api_version'));
    }

    #[Test]
    public function it_works_with_route_integration(): void
    {
        $this->app->router->get('/api/test', fn () => response()->json(['status' => 'ok']))
            ->middleware(EnsureApiVersion::class . ':v2');

        $this->getJson('/api/test', [
            'Accept' => 'application/vnd.api+json; version=v2',
        ])->assertOk()
          ->assertJson(['status' => 'ok']);
    }

    #[Test]
    public function it_returns_json_error_on_rejection(): void
    {
        $this->app->router->get('/api/test', fn () => response()->json(['status' => 'ok']))
            ->middleware(EnsureApiVersion::class . ':v2');

        $response = $this->getJson('/api/test', [
            'Accept' => 'application/vnd.api+json; version=v1',
        ]);

        $response->assertStatus(406)
            ->assertJsonStructure(['error', 'message']);
    }

    #[Test]
    public function it_works_with_custom_headers_helper(): void
    {
        $this->app->router->get('/api/test', fn () => response()->json(['data' => true]))
            ->middleware(EnsureApiVersion::class . ':v3');

        $this->withHeaders([
            'Accept' => 'application/vnd.api+json; version=v3',
        ])->getJson('/api/test')
          ->assertOk()
          ->assertJson(['data' => true]);
    }
}
```

## Checklist

When generating middleware, verify:

- [ ] Class is declared `final` with `declare(strict_types=1)`
- [ ] `handle()` has the `Closure(Request): Response` docblock
- [ ] Parameters have sensible defaults
- [ ] Error responses return structured JSON, not `abort()`
- [ ] Response status codes match semantics (406, 429, 403, etc.)
- [ ] After middleware calls `$next($request)` before modifying the response
- [ ] Terminable middleware stores state on `$request->attributes`
- [ ] Tests cover pass, fail, parameter variations, and missing header cases
- [ ] Registration example uses Laravel 11+ `bootstrap/app.php` syntax
