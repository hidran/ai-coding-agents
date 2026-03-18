---
name: laravel-command
description: Generates Laravel Artisan console commands with arguments, options, scheduling, progress bars, interactive prompts, and tests.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Laravel Artisan Command Generator

## Usage

Run `/laravel-command <CommandName>` to generate a complete Artisan console command with its associated test file.

## Structure

This skill generates the following files:

- `app/Console/Commands/<CommandName>.php` -- The Artisan command class
- `tests/Feature/Commands/<CommandName>Test.php` -- Feature tests for the command

## Standards

- **Typed signature**: Use typed arguments and options in the `$signature` property with clear descriptions.
- **Exit codes**: Always return `self::SUCCESS` or `self::FAILURE` from the `handle()` method. Never return void or arbitrary integers.
- **Progress bars**: Use progress bars for any operation that iterates over a collection or performs batch processing.
- **Prompts**: Use Laravel Prompts (`text()`, `select()`, `confirm()`, `table()`, `password()`, `multiselect()`, `spin()`) for interactive commands.
- **Logging**: Log important operations using `Log::info()` or `Log::error()`. Console output alone is not sufficient for production commands.
- **Dependency injection**: Inject services via `handle()` method parameters rather than resolving from the container manually.
- **Scheduling**: Include an example of how to register the command on the scheduler with appropriate frequency and guards.

## Examples

### 1. Batch Processing Command -- PruneExpiredOrders

```php
<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Services\OrderService;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;

class PruneExpiredOrders extends Command
{
    protected $signature = 'orders:prune
        {--days=30 : Number of days to keep}
        {--dry-run : Show what would be deleted without deleting}';

    protected $description = 'Prune expired orders older than the specified number of days';

    public function handle(OrderService $orderService): int
    {
        $days = (int) $this->option('days');
        $dryRun = (bool) $this->option('dry-run');

        if ($dryRun) {
            $this->components->warn('Running in dry-run mode. No records will be deleted.');
        }

        $this->components->info("Searching for orders older than {$days} days...");

        $expiredOrders = $orderService->getExpiredOrders($days);

        if ($expiredOrders->isEmpty()) {
            $this->components->info('No expired orders found. Nothing to prune.');
            return self::SUCCESS;
        }

        $this->components->info("Found {$expiredOrders->count()} expired orders.");

        $this->table(
            ['ID', 'Customer', 'Created At', 'Status'],
            $expiredOrders->map(fn ($order) => [
                $order->id,
                $order->customer_name,
                $order->created_at->toDateTimeString(),
                $order->status,
            ])->toArray(),
        );

        if ($dryRun) {
            $this->components->warn("Dry run complete. {$expiredOrders->count()} orders would be deleted.");
            return self::SUCCESS;
        }

        $failed = 0;
        $bar = $this->output->createProgressBar($expiredOrders->count());
        $bar->start();

        foreach ($expiredOrders->chunk(100) as $chunk) {
            try {
                $orderService->deleteOrders($chunk->pluck('id')->toArray());
            } catch (\Throwable $e) {
                $failed += $chunk->count();
                Log::error('Failed to prune order chunk', [
                    'ids' => $chunk->pluck('id')->toArray(),
                    'error' => $e->getMessage(),
                ]);
            }

            $bar->advance($chunk->count());
        }

        $bar->finish();
        $this->newLine(2);

        $deleted = $expiredOrders->count() - $failed;

        $this->components->task('Pruning expired orders', fn () => $failed === 0);

        if ($failed > 0) {
            $this->components->error("Completed with errors: {$deleted} deleted, {$failed} failed.");
            Log::warning('Order pruning completed with failures', [
                'deleted' => $deleted,
                'failed' => $failed,
                'days' => $days,
            ]);
            return self::FAILURE;
        }

        $this->components->info("Successfully pruned {$deleted} expired orders.");
        Log::info('Order pruning completed', ['deleted' => $deleted, 'days' => $days]);

        return self::SUCCESS;
    }
}
```

### 2. Interactive Command -- SetupProject

```php
<?php

declare(strict_types=1);

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;

use function Laravel\Prompts\confirm;
use function Laravel\Prompts\multiselect;
use function Laravel\Prompts\password;
use function Laravel\Prompts\select;
use function Laravel\Prompts\spin;
use function Laravel\Prompts\text;

class SetupProject extends Command
{
    protected $signature = 'project:setup';

    protected $description = 'Interactively configure the project environment';

    public function handle(): int
    {
        $this->components->info('Welcome to the project setup wizard.');

        $appName = text(
            label: 'Application name',
            placeholder: 'My Application',
            default: config('app.name', 'Laravel'),
            required: true,
        );

        $environment = select(
            label: 'Select environment',
            options: ['local', 'staging', 'production'],
            default: 'local',
        );

        $dbConnection = select(
            label: 'Database driver',
            options: ['mysql', 'pgsql', 'sqlite'],
            default: 'mysql',
        );

        $dbHost = text(
            label: 'Database host',
            default: '127.0.0.1',
            required: $dbConnection !== 'sqlite',
        );

        $dbName = text(
            label: 'Database name',
            default: 'laravel',
            required: true,
        );

        $dbUser = text(
            label: 'Database username',
            default: 'root',
        );

        $dbPassword = password(
            label: 'Database password',
        );

        $features = multiselect(
            label: 'Enable features',
            options: [
                'telescope' => 'Laravel Telescope',
                'horizon' => 'Laravel Horizon',
                'pulse' => 'Laravel Pulse',
                'sanctum' => 'Laravel Sanctum',
            ],
            default: ['sanctum'],
        );

        $envValues = [
            'APP_NAME' => "\"{$appName}\"",
            'APP_ENV' => $environment,
            'DB_CONNECTION' => $dbConnection,
            'DB_HOST' => $dbHost,
            'DB_DATABASE' => $dbName,
            'DB_USERNAME' => $dbUser,
            'DB_PASSWORD' => $dbPassword,
        ];

        spin(
            callback: function () use ($envValues) {
                $this->writeEnvValues($envValues);
            },
            message: 'Writing environment configuration...',
        );

        $this->components->info('Environment file updated.');

        if (confirm(label: 'Run database migrations?', default: true)) {
            spin(
                callback: fn () => $this->call('migrate', ['--force' => $environment !== 'local']),
                message: 'Running migrations...',
            );
            $this->components->info('Migrations completed.');
        }

        if (confirm(label: 'Seed the database?', default: $environment === 'local')) {
            spin(
                callback: fn () => $this->call('db:seed'),
                message: 'Seeding database...',
            );
            $this->components->info('Database seeded.');
        }

        Log::info('Project setup completed', [
            'environment' => $environment,
            'features' => $features,
        ]);

        $this->components->info('Project setup complete!');

        return self::SUCCESS;
    }

    private function writeEnvValues(array $values): void
    {
        $envPath = base_path('.env');
        $contents = file_exists($envPath) ? file_get_contents($envPath) : '';

        foreach ($values as $key => $value) {
            $pattern = "/^{$key}=.*/m";

            if (preg_match($pattern, $contents)) {
                $contents = preg_replace($pattern, "{$key}={$value}", $contents);
            } else {
                $contents .= PHP_EOL . "{$key}={$value}";
            }
        }

        file_put_contents($envPath, $contents);
    }
}
```

### 3. Schedule Registration

#### Laravel 11+ (routes/console.php)

```php
<?php

use Illuminate\Support\Facades\Schedule;

Schedule::command('orders:prune --days=30')
    ->dailyAt('02:00')
    ->withoutOverlapping()
    ->onOneServer()
    ->emailOutputOnFailure('ops@example.com');

Schedule::command('orders:prune --days=90')
    ->weeklyOn(Schedule::SUNDAY, '03:00')
    ->withoutOverlapping()
    ->onOneServer()
    ->appendOutputTo(storage_path('logs/prune.log'));
```

#### Laravel 10 (app/Console/Kernel.php)

```php
<?php

declare(strict_types=1);

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    protected function schedule(Schedule $schedule): void
    {
        $schedule->command('orders:prune --days=30')
            ->dailyAt('02:00')
            ->withoutOverlapping()
            ->onOneServer()
            ->emailOutputOnFailure('ops@example.com');
    }
}
```

### 4. Command Tests

```php
<?php

declare(strict_types=1);

namespace Tests\Feature\Commands;

use App\Models\Order;
use App\Services\OrderService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Mockery\MockInterface;
use Tests\TestCase;

class PruneExpiredOrdersTest extends TestCase
{
    use RefreshDatabase;

    public function test_prunes_expired_orders(): void
    {
        Order::factory()
            ->count(5)
            ->state(['created_at' => now()->subDays(60)])
            ->create();

        Order::factory()
            ->count(3)
            ->state(['created_at' => now()->subDays(10)])
            ->create();

        $this->artisan('orders:prune', ['--days' => 30])
            ->assertExitCode(0);

        $this->assertDatabaseCount('orders', 3);
    }

    public function test_dry_run_does_not_delete_records(): void
    {
        Order::factory()
            ->count(5)
            ->state(['created_at' => now()->subDays(60)])
            ->create();

        $this->artisan('orders:prune', ['--dry-run' => true])
            ->expectsOutputToContain('Dry run complete')
            ->assertExitCode(0);

        $this->assertDatabaseCount('orders', 5);
    }

    public function test_custom_days_argument(): void
    {
        Order::factory()
            ->count(3)
            ->state(['created_at' => now()->subDays(10)])
            ->create();

        Order::factory()
            ->count(2)
            ->state(['created_at' => now()->subDays(3)])
            ->create();

        $this->artisan('orders:prune', ['--days' => 7])
            ->assertExitCode(0);

        $this->assertDatabaseCount('orders', 2);
    }

    public function test_no_expired_orders_returns_success(): void
    {
        $this->artisan('orders:prune')
            ->expectsOutputToContain('No expired orders found')
            ->assertExitCode(0);
    }

    public function test_returns_failure_on_service_error(): void
    {
        Order::factory()
            ->count(3)
            ->state(['created_at' => now()->subDays(60)])
            ->create();

        $this->mock(OrderService::class, function (MockInterface $mock) {
            $mock->shouldReceive('getExpiredOrders')
                ->andReturn(Order::all());

            $mock->shouldReceive('deleteOrders')
                ->andThrow(new \RuntimeException('Database error'));
        });

        $this->artisan('orders:prune', ['--days' => 30])
            ->assertExitCode(1);
    }

    public function test_interactive_setup_command(): void
    {
        $this->artisan('project:setup')
            ->expectsQuestion('Application name', 'Test App')
            ->expectsQuestion('Select environment', 'local')
            ->expectsQuestion('Database driver', 'sqlite')
            ->expectsQuestion('Database host', '')
            ->expectsQuestion('Database name', 'test_db')
            ->expectsQuestion('Database username', 'root')
            ->expectsQuestion('Database password', '')
            ->expectsQuestion('Enable features', ['sanctum'])
            ->expectsConfirmation('Run database migrations?', 'no')
            ->expectsConfirmation('Seed the database?', 'no')
            ->assertExitCode(0);
    }
}
```

## Generation Checklist

When generating a command, verify the following:

1. The class extends `Illuminate\Console\Command`
2. The `$signature` uses descriptive argument and option names with help text
3. The `handle()` method has a return type of `int`
4. The `handle()` method returns only `self::SUCCESS` or `self::FAILURE`
5. Services are injected via `handle()` parameters, not the constructor
6. Long-running operations use a progress bar
7. Interactive commands use `Laravel\Prompts` functions, not `$this->ask()`
8. Important operations are logged with `Log::info()` or `Log::error()`
9. The test file covers success, failure, flags, and edge cases
10. All code is PHP 8.2+ with `declare(strict_types=1)` and typed properties
