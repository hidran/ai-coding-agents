---
name: laravel-event
description: Generates a Laravel Event with Listener, queued Job, and Notification. Full async event-driven pipeline with tests.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel Event Pipeline Generator

## Usage

Run `/laravel-event <EventName>`

The `<EventName>` should be a PascalCase noun phrase describing the domain event (e.g., `OrderPlaced`, `UserRegistered`, `PaymentFailed`).

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure

When invoked, generate the following files:

- `app/Events/<EventName>.php` -- Event class with typed readonly properties
- `app/Listeners/<EventName>Listener.php` -- Queued event listener
- `app/Jobs/Process<RelatedAction>.php` -- Background job for async processing
- `app/Notifications/<RelatedNotification>.php` -- Notification via mail and database channels
- `tests/Feature/Events/<EventName>Test.php` -- Feature tests covering the full pipeline

## Standards

- **Immutable events**: All event properties must be declared `readonly`. Events represent facts that happened and must not be mutated after creation.
- **ShouldQueue**: Listeners implement `ShouldQueue` by default. Only remove it when synchronous execution is explicitly required.
- **Typed properties**: Events carry typed data objects, not raw arrays. Use models, DTOs, or value objects.
- **Retry logic**: Jobs and listeners must define `$tries`, `$backoff`, and `$maxExceptions` to control failure behavior.
- **Failed handling**: Implement the `failed()` method on listeners and jobs to handle permanent failures (log, alert, compensate).
- **Broadcasting**: Include `ShouldBroadcast` setup when the event needs real-time delivery to frontend clients.
- **Strict types**: Every generated file must declare `strict_types=1` and target PHP 8.2+.
- **Final classes**: Events, listeners, jobs, and notifications should be declared `final` unless inheritance is explicitly needed.

## Examples

### 1. Event -- `OrderPlaced`

```php
<?php

declare(strict_types=1);

namespace App\Events;

use App\Models\Order;
use App\Models\User;
use Carbon\CarbonImmutable;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

final class OrderPlaced implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public readonly Order $order,
        public readonly User $user,
        public readonly CarbonImmutable $placedAt,
    ) {}

    /**
     * @return array<int, Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel("orders.{$this->user->id}"),
        ];
    }

    /**
     * @return array<string, mixed>
     */
    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            'total' => $this->order->total,
            'placed_at' => $this->placedAt->toIso8601String(),
        ];
    }

    public function broadcastAs(): string
    {
        return 'order.placed';
    }
}
```

### 2. Listener -- `SendOrderConfirmation`

```php
<?php

declare(strict_types=1);

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Notifications\OrderConfirmationNotification;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

final class SendOrderConfirmation implements ShouldQueue
{
    use InteractsWithQueue;

    public string $connection = 'redis';

    public string $queue = 'notifications';

    public int $tries = 3;

    /** @var array<int, int> */
    public array $backoff = [10, 60, 300];

    public int $maxExceptions = 2;

    public function handle(OrderPlaced $event): void
    {
        $event->user->notify(new OrderConfirmationNotification($event->order));
    }

    public function shouldQueue(OrderPlaced $event): bool
    {
        return $event->order->total > 0;
    }

    public function failed(OrderPlaced $event, Throwable $exception): void
    {
        report($exception);

        // Optionally alert the team or enqueue a fallback
        logger()->critical('Failed to send order confirmation', [
            'order_id' => $event->order->id,
            'user_id' => $event->user->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

### 3. Notification -- `OrderConfirmationNotification`

```php
<?php

declare(strict_types=1);

namespace App\Notifications;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

final class OrderConfirmationNotification extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        private readonly Order $order,
    ) {}

    /**
     * @return array<int, string>
     */
    public function via(object $notifiable): array
    {
        return ['mail', 'database'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage())
            ->subject("Order #{$this->order->id} Confirmed")
            ->markdown('mail.orders.confirmed', [
                'order' => $this->order,
                'user' => $notifiable,
            ]);
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(object $notifiable): array
    {
        return $this->toDatabase($notifiable);
    }

    /**
     * @return array<string, mixed>
     */
    public function toDatabase(object $notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'total' => $this->order->total,
            'status' => $this->order->status->value,
            'message' => "Your order #{$this->order->id} has been confirmed.",
        ];
    }
}
```

### 4. Job -- `ProcessOrderPayment`

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Illuminate\Queue\SerializesModels;
use Throwable;

final class ProcessOrderPayment implements ShouldQueue, ShouldBeUnique
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;

    /** @var array<int, int> */
    public array $backoff = [10, 60, 300];

    public int $maxExceptions = 2;

    public int $uniqueFor = 3600;

    public function __construct(
        private readonly Order $order,
    ) {}

    public function uniqueId(): string
    {
        return (string) $this->order->id;
    }

    /**
     * @return array<int, object>
     */
    public function middleware(): array
    {
        return [
            new WithoutOverlapping($this->order->id),
        ];
    }

    public function handle(): void
    {
        // Charge the payment gateway
        $paymentResult = app(\App\Services\PaymentGateway::class)->charge(
            amount: $this->order->total,
            paymentMethodId: $this->order->payment_method_id,
        );

        $this->order->update([
            'payment_status' => $paymentResult->status,
            'transaction_id' => $paymentResult->transactionId,
        ]);
    }

    public function failed(Throwable $exception): void
    {
        report($exception);

        $this->order->update(['payment_status' => 'failed']);

        logger()->critical('Payment processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

### 5. Feature Test -- `OrderPlacedTest`

```php
<?php

declare(strict_types=1);

namespace Tests\Feature\Events;

use App\Events\OrderPlaced;
use App\Jobs\ProcessOrderPayment;
use App\Listeners\SendOrderConfirmation;
use App\Models\Order;
use App\Models\User;
use App\Notifications\OrderConfirmationNotification;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

final class OrderPlacedTest extends TestCase
{
    use RefreshDatabase;

    public function test_order_placed_event_is_dispatched(): void
    {
        Event::fake([OrderPlaced::class]);

        $user = User::factory()->create();
        $order = Order::factory()->for($user)->create();

        OrderPlaced::dispatch($order, $user, CarbonImmutable::now());

        Event::assertDispatched(OrderPlaced::class, function (OrderPlaced $event) use ($order, $user) {
            return $event->order->id === $order->id
                && $event->user->id === $user->id
                && $event->placedAt instanceof CarbonImmutable;
        });
    }

    public function test_notification_is_sent_to_correct_user(): void
    {
        Notification::fake();

        $user = User::factory()->create();
        $order = Order::factory()->for($user)->create(['total' => 9999]);

        $event = new OrderPlaced($order, $user, CarbonImmutable::now());

        $listener = new SendOrderConfirmation();
        $listener->handle($event);

        Notification::assertSentTo(
            $user,
            OrderConfirmationNotification::class,
        );
    }

    public function test_payment_job_is_pushed_to_correct_queue(): void
    {
        Queue::fake();

        $order = Order::factory()->create();

        ProcessOrderPayment::dispatch($order)->onQueue('payments');

        Queue::assertPushedOn('payments', ProcessOrderPayment::class, function ($job) use ($order) {
            return true; // SerializesModels handles the order binding
        });
    }

    public function test_listener_conditionally_queues(): void
    {
        $user = User::factory()->create();
        $freeOrder = Order::factory()->for($user)->create(['total' => 0]);

        $event = new OrderPlaced($freeOrder, $user, CarbonImmutable::now());

        $listener = new SendOrderConfirmation();

        $this->assertFalse($listener->shouldQueue($event));
    }

    public function test_event_has_correct_broadcast_configuration(): void
    {
        $user = User::factory()->create();
        $order = Order::factory()->for($user)->create(['total' => 5000]);

        $event = new OrderPlaced($order, $user, CarbonImmutable::now());

        $this->assertSame('order.placed', $event->broadcastAs());

        $broadcastData = $event->broadcastWith();
        $this->assertArrayHasKey('order_id', $broadcastData);
        $this->assertArrayHasKey('total', $broadcastData);
        $this->assertArrayHasKey('placed_at', $broadcastData);
    }

    public function test_full_pipeline_integration(): void
    {
        Event::fake([OrderPlaced::class]);
        Notification::fake();
        Queue::fake();

        $user = User::factory()->create();
        $order = Order::factory()->for($user)->create(['total' => 15000]);

        OrderPlaced::dispatch($order, $user, CarbonImmutable::now());

        Event::assertDispatched(OrderPlaced::class);
    }
}
```

### 6. EventServiceProvider Registration

#### Laravel 10 and below -- Manual registration

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Events\OrderPlaced;
use App\Listeners\SendOrderConfirmation;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

final class EventServiceProvider extends ServiceProvider
{
    /** @var array<class-string, array<int, class-string>> */
    protected $listen = [
        OrderPlaced::class => [
            SendOrderConfirmation::class,
        ],
    ];

    public function shouldDiscoverEvents(): bool
    {
        return false;
    }
}
```

#### Laravel 11+ -- Attribute-based event discovery

In Laravel 11+, use PHP attributes on the listener instead of manual registration. No `EventServiceProvider` is needed.

```php
<?php

declare(strict_types=1);

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Notifications\OrderConfirmationNotification;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

#[\Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit]
final class SendOrderConfirmation implements ShouldQueue
{
    use InteractsWithQueue;

    // ... same as above
}
```

Register via `AppServiceProvider` boot method or rely on automatic event discovery (enabled by default in Laravel 11+):

```php
// bootstrap/app.php (Laravel 11+)
return Application::configure(basePath: dirname(__DIR__))
    ->withEvents([
        __DIR__ . '/../app/Listeners',
    ])
    ->create();
```

## Generation Instructions

When generating the pipeline for a given `<EventName>`:

1. **Scan the project** using `Glob` and `Grep` to determine the Laravel version, existing event patterns, queue connection, and naming conventions.
2. **Create each file** using `Write`, following the examples above as templates. Replace `OrderPlaced` with the user's `<EventName>` and adapt properties to fit the domain context.
3. **Check for conflicts** -- use `Glob` to verify no file already exists at the target paths before writing.
4. **Register the event** -- for Laravel 10 and below, update `EventServiceProvider`. For Laravel 11+, confirm event discovery is enabled or add the attribute.
5. **Report** the created files and any manual steps remaining (e.g., creating mail templates, running migrations, configuring queue workers).
