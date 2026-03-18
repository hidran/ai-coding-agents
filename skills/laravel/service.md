---
name: laravel-service
description: Generates a Laravel Service class with interface, ServiceProvider binding, dependency injection, and unit tests. Clean architecture pattern.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel Service Generator

## Usage

Run `/laravel-service <ServiceName>`

Replace `<ServiceName>` with the domain concept (e.g., `Order`, `Payment`, `Inventory`). The generator will append `Service`, `ServiceInterface`, and `ServiceProvider` suffixes automatically.

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure

The skill generates the following files:

| File | Purpose |
|------|---------|
| `app/Services/<Service>Service.php` | Service implementation with business logic |
| `app/Contracts/<Service>ServiceInterface.php` | Interface contract defining the public API |
| `app/Providers/<Service>ServiceProvider.php` | ServiceProvider with interface-to-implementation binding |
| `tests/Unit/Services/<Service>ServiceTest.php` | Unit tests with mocked dependencies |

## Standards

- **Interface-driven**: Always create an interface and bind it in a dedicated ServiceProvider. Never instantiate services directly.
- **Constructor injection**: Inject all dependencies via constructor with type hints. No service locator or facade usage inside services.
- **Single responsibility**: Each service handles one domain concern. If a service grows beyond 5-7 public methods, consider splitting it.
- **Return types**: All methods must have explicit return types, including `void`.
- **DTOs**: Accept and return typed DTOs for complex operations. Use readonly classes with named constructors (PHP 8.2+).
- **Exceptions**: Throw domain-specific exceptions, not generic ones. Create exception classes under `app/Exceptions/`.
- **Strict types**: Every PHP file must declare `strict_types=1`.

## Examples

### 1. Interface -- `OrderServiceInterface`

```php
<?php

declare(strict_types=1);

namespace App\Contracts;

use App\DTOs\CreateOrderDTO;
use App\Models\Order;
use App\ValueObjects\Money;

interface OrderServiceInterface
{
    /**
     * Create a new order from the given DTO.
     *
     * @throws \App\Exceptions\OrderCreationException
     */
    public function create(CreateOrderDTO $dto): Order;

    /**
     * Find an order by its ID.
     *
     * @throws \App\Exceptions\OrderNotFoundException
     */
    public function findById(int $id): Order;

    /**
     * Cancel an existing order.
     *
     * @throws \App\Exceptions\OrderNotFoundException
     * @throws \App\Exceptions\OrderCancellationException
     */
    public function cancel(int $id): void;

    /**
     * Calculate the total for an order including tax and discounts.
     */
    public function calculateTotal(Order $order): Money;
}
```

### 2. Service Implementation -- `OrderService`

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\Contracts\OrderRepositoryInterface;
use App\Contracts\OrderServiceInterface;
use App\Contracts\PaymentGatewayInterface;
use App\DTOs\CreateOrderDTO;
use App\Enums\OrderStatus;
use App\Events\OrderCancelled;
use App\Events\OrderCreated;
use App\Exceptions\OrderCancellationException;
use App\Exceptions\OrderNotFoundException;
use App\Models\Order;
use App\ValueObjects\Money;
use Illuminate\Support\Facades\DB;

final readonly class OrderService implements OrderServiceInterface
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private PaymentGatewayInterface $paymentGateway,
    ) {}

    public function create(CreateOrderDTO $dto): Order
    {
        return DB::transaction(function () use ($dto): Order {
            $order = $this->orderRepository->create([
                'customer_id' => $dto->customerId,
                'items' => $dto->items,
                'shipping_address' => $dto->shippingAddress,
                'status' => OrderStatus::Pending,
            ]);

            $total = $this->calculateTotal($order);

            $this->paymentGateway->authorize(
                amount: $total,
                customerId: $dto->customerId,
            );

            $order->update(['total_cents' => $total->cents]);

            event(new OrderCreated($order));

            return $order->refresh();
        });
    }

    public function findById(int $id): Order
    {
        $order = $this->orderRepository->find($id);

        if ($order === null) {
            throw OrderNotFoundException::withId($id);
        }

        return $order;
    }

    public function cancel(int $id): void
    {
        $order = $this->findById($id);

        if ($order->status === OrderStatus::Shipped) {
            throw OrderCancellationException::alreadyShipped($id);
        }

        if ($order->status === OrderStatus::Cancelled) {
            throw OrderCancellationException::alreadyCancelled($id);
        }

        DB::transaction(function () use ($order): void {
            $this->paymentGateway->refund(
                orderId: $order->id,
                amount: new Money($order->total_cents),
            );

            $this->orderRepository->update($order->id, [
                'status' => OrderStatus::Cancelled,
                'cancelled_at' => now(),
            ]);

            event(new OrderCancelled($order));
        });
    }

    public function calculateTotal(Order $order): Money
    {
        $subtotal = $order->items->sum(
            fn ($item) => $item->price_cents * $item->quantity
        );

        $taxRate = 0.08;
        $taxAmount = (int) round($subtotal * $taxRate);

        $discountCents = $order->discount_cents ?? 0;

        return new Money(
            cents: max(0, $subtotal + $taxAmount - $discountCents),
        );
    }
}
```

### 3. ServiceProvider -- `OrderServiceProvider`

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Contracts\OrderServiceInterface;
use App\Services\OrderService;
use Illuminate\Support\ServiceProvider;

final class OrderServiceProvider extends ServiceProvider
{
    /**
     * Register services into the container.
     */
    public function register(): void
    {
        $this->app->singleton(
            OrderServiceInterface::class,
            OrderService::class,
        );
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
```

**Registration:**

For **Laravel 11+**, add the provider to `bootstrap/providers.php`:

```php
return [
    App\Providers\AppServiceProvider::class,
    App\Providers\OrderServiceProvider::class,
];
```

For **Laravel 10 and earlier**, add it to `config/app.php`:

```php
'providers' => [
    // ...
    App\Providers\OrderServiceProvider::class,
],
```

### 4. Unit Test -- `OrderServiceTest`

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Services;

use App\Contracts\OrderRepositoryInterface;
use App\Contracts\PaymentGatewayInterface;
use App\DTOs\CreateOrderDTO;
use App\Enums\OrderStatus;
use App\Exceptions\OrderCancellationException;
use App\Exceptions\OrderNotFoundException;
use App\Events\OrderCancelled;
use App\Events\OrderCreated;
use App\Models\Order;
use App\Services\OrderService;
use App\ValueObjects\Money;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Mockery;
use Mockery\MockInterface;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

final class OrderServiceTest extends TestCase
{
    use RefreshDatabase;

    private OrderRepositoryInterface&MockInterface $orderRepository;
    private PaymentGatewayInterface&MockInterface $paymentGateway;
    private OrderService $service;

    protected function setUp(): void
    {
        parent::setUp();

        $this->orderRepository = Mockery::mock(OrderRepositoryInterface::class);
        $this->paymentGateway = Mockery::mock(PaymentGatewayInterface::class);

        $this->service = new OrderService(
            orderRepository: $this->orderRepository,
            paymentGateway: $this->paymentGateway,
        );
    }

    #[Test]
    public function it_creates_an_order_and_dispatches_event(): void
    {
        Event::fake([OrderCreated::class]);

        $dto = new CreateOrderDTO(
            customerId: 1,
            items: [['product_id' => 10, 'quantity' => 2, 'price_cents' => 1500]],
            shippingAddress: '123 Main St',
        );

        $order = $this->createMockOrder(id: 1, status: OrderStatus::Pending);

        $this->orderRepository
            ->shouldReceive('create')
            ->once()
            ->andReturn($order);

        $this->paymentGateway
            ->shouldReceive('authorize')
            ->once();

        $order->shouldReceive('update')->once();
        $order->shouldReceive('refresh')->once()->andReturn($order);

        $result = $this->service->create($dto);

        $this->assertSame($order, $result);
        Event::assertDispatched(OrderCreated::class);
    }

    #[Test]
    public function it_finds_an_order_by_id(): void
    {
        $order = $this->createMockOrder(id: 42, status: OrderStatus::Pending);

        $this->orderRepository
            ->shouldReceive('find')
            ->with(42)
            ->once()
            ->andReturn($order);

        $result = $this->service->findById(42);

        $this->assertSame($order, $result);
    }

    #[Test]
    public function it_throws_when_order_not_found(): void
    {
        $this->orderRepository
            ->shouldReceive('find')
            ->with(999)
            ->once()
            ->andReturn(null);

        $this->expectException(OrderNotFoundException::class);

        $this->service->findById(999);
    }

    #[Test]
    public function it_cancels_an_order_and_dispatches_event(): void
    {
        Event::fake([OrderCancelled::class]);

        $order = $this->createMockOrder(id: 1, status: OrderStatus::Pending);

        $this->orderRepository
            ->shouldReceive('find')
            ->with(1)
            ->once()
            ->andReturn($order);

        $this->paymentGateway
            ->shouldReceive('refund')
            ->once();

        $this->orderRepository
            ->shouldReceive('update')
            ->once();

        $this->service->cancel(1);

        Event::assertDispatched(OrderCancelled::class);
    }

    #[Test]
    #[DataProvider('uncancellableStatusProvider')]
    public function it_throws_when_cancelling_order_with_invalid_status(
        OrderStatus $status,
        string $expectedException,
    ): void {
        $order = $this->createMockOrder(id: 1, status: $status);

        $this->orderRepository
            ->shouldReceive('find')
            ->with(1)
            ->once()
            ->andReturn($order);

        $this->expectException($expectedException);

        $this->service->cancel(1);
    }

    public static function uncancellableStatusProvider(): array
    {
        return [
            'already shipped' => [
                OrderStatus::Shipped,
                OrderCancellationException::class,
            ],
            'already cancelled' => [
                OrderStatus::Cancelled,
                OrderCancellationException::class,
            ],
        ];
    }

    #[Test]
    public function it_calculates_total_with_tax_and_discount(): void
    {
        $order = $this->createMockOrder(id: 1, status: OrderStatus::Pending);
        $order->discount_cents = 500;

        $items = collect([
            (object) ['price_cents' => 1000, 'quantity' => 2],
            (object) ['price_cents' => 500, 'quantity' => 1],
        ]);
        $order->shouldReceive('getAttribute')->with('items')->andReturn($items);

        $total = $this->service->calculateTotal($order);

        // Subtotal: 2500, Tax (8%): 200, Discount: 500 => Total: 2200
        $this->assertInstanceOf(Money::class, $total);
        $this->assertSame(2200, $total->cents);
    }

    private function createMockOrder(int $id, OrderStatus $status): Order&MockInterface
    {
        $order = Mockery::mock(Order::class)->makePartial();
        $order->id = $id;
        $order->status = $status;
        $order->total_cents = 0;

        return $order;
    }
}
```

### 5. DTO -- `CreateOrderDTO`

```php
<?php

declare(strict_types=1);

namespace App\DTOs;

final readonly class CreateOrderDTO
{
    /**
     * @param int         $customerId      The customer placing the order.
     * @param array<int, array{product_id: int, quantity: int, price_cents: int}> $items
     * @param string      $shippingAddress Delivery address for the order.
     * @param string|null $notes           Optional notes from the customer.
     */
    public function __construct(
        public int $customerId,
        public array $items,
        public string $shippingAddress,
        public ?string $notes = null,
    ) {}

    /**
     * Named constructor from a validated request array.
     */
    public static function fromRequest(array $validated): self
    {
        return new self(
            customerId: $validated['customer_id'],
            items: $validated['items'],
            shippingAddress: $validated['shipping_address'],
            notes: $validated['notes'] ?? null,
        );
    }
}
```

### Supporting Files Reference

These are not generated by the skill but are referenced in the examples above. Create them as needed.

**`app/ValueObjects/Money.php`**:

```php
<?php

declare(strict_types=1);

namespace App\ValueObjects;

final readonly class Money
{
    public function __construct(
        public int $cents,
    ) {}

    public function dollars(): float
    {
        return $this->cents / 100;
    }

    public function add(Money $other): self
    {
        return new self($this->cents + $other->cents);
    }
}
```

**`app/Enums/OrderStatus.php`**:

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Confirmed = 'confirmed';
    case Shipped = 'shipped';
    case Delivered = 'delivered';
    case Cancelled = 'cancelled';
}
```

**`app/Exceptions/OrderNotFoundException.php`**:

```php
<?php

declare(strict_types=1);

namespace App\Exceptions;

use RuntimeException;

final class OrderNotFoundException extends RuntimeException
{
    public static function withId(int $id): self
    {
        return new self("Order with ID {$id} was not found.");
    }
}
```

**`app/Exceptions/OrderCancellationException.php`**:

```php
<?php

declare(strict_types=1);

namespace App\Exceptions;

use RuntimeException;

final class OrderCancellationException extends RuntimeException
{
    public static function alreadyShipped(int $id): self
    {
        return new self("Order {$id} has already been shipped and cannot be cancelled.");
    }

    public static function alreadyCancelled(int $id): self
    {
        return new self("Order {$id} is already cancelled.");
    }
}
```

## Generation Checklist

When generating a service, verify:

- [ ] `declare(strict_types=1)` at the top of every file
- [ ] Interface created in `app/Contracts/`
- [ ] Service class is `final readonly` and implements the interface
- [ ] All dependencies injected via constructor with type hints
- [ ] All methods have explicit return types
- [ ] ServiceProvider uses `singleton` binding
- [ ] ServiceProvider is registered in providers config
- [ ] Unit test mocks all dependencies
- [ ] Unit test covers success, failure, and edge cases
- [ ] Domain-specific exceptions used (not generic `\Exception`)
- [ ] Events dispatched for state-changing operations
- [ ] Database transactions wrap multi-step writes
