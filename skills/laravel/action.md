---
name: laravel-action
description: Generates a Laravel single-action class with __invoke, validation, authorization. Usable as controller action, queued job, or console command.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel Action Generator

## Usage

Run `/laravel-action <ActionName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure

Generates:

- `app/Actions/<ActionName>.php`: Action class with `__invoke`
- `tests/Unit/Actions/<ActionName>Test.php`: Unit tests

## What is the Action Pattern?

Actions are single-purpose classes that encapsulate one business operation. They can be invoked from controllers, jobs, commands, or other actions. They promote:

- **Single Responsibility**: One class = one operation
- **Reusability**: Call from anywhere (HTTP, CLI, queue, tests)
- **Testability**: Easy to test in isolation
- **Readability**: Class name describes what it does

## Standards

- **__invoke**: Use the `__invoke` method as the single entry point
- **Naming**: Verb + Noun format: `CreateOrder`, `SendInvoice`, `ArchiveProject`
- **Typed parameters**: Accept typed DTOs or value objects, not raw arrays
- **Return types**: Explicit return type on `__invoke`
- **No side-effect constructors**: Constructor only for dependency injection
- **Composable**: Actions can call other actions

## Examples

### 1. Action Class

```php
<?php

declare(strict_types=1);

namespace App\Actions;

use App\Data\CreateOrderData;
use App\Events\OrderCreated;
use App\Exceptions\InsufficientStockException;
use App\Exceptions\PaymentFailedException;
use App\Models\Order;
use App\Repositories\OrderRepository;
use App\Services\PaymentGateway;
use App\Services\TaxCalculator;
use Illuminate\Support\Facades\DB;

final class CreateOrder
{
    public function __construct(
        private readonly OrderRepository $orderRepository,
        private readonly PaymentGateway $paymentGateway,
        private readonly TaxCalculator $taxCalculator,
    ) {}

    /**
     * @throws InsufficientStockException
     * @throws PaymentFailedException
     */
    public function __invoke(CreateOrderData $data): Order
    {
        $this->validateStock($data->items);

        $taxAmount = $this->taxCalculator->calculate($data->items, $data->shippingAddressId);

        return DB::transaction(function () use ($data, $taxAmount): Order {
            $order = $this->orderRepository->create(
                userId: $data->userId,
                items: $data->items,
                shippingAddressId: $data->shippingAddressId,
                couponCode: $data->couponCode,
                taxAmount: $taxAmount,
            );

            $this->processPayment($order);

            OrderCreated::dispatch($order);

            return $order;
        });
    }

    /**
     * @param  array<int, array{product_id: int, quantity: int}>  $items
     *
     * @throws InsufficientStockException
     */
    private function validateStock(array $items): void
    {
        foreach ($items as $item) {
            if (! $this->orderRepository->hasStock($item['product_id'], $item['quantity'])) {
                throw new InsufficientStockException(
                    "Insufficient stock for product {$item['product_id']}."
                );
            }
        }
    }

    /**
     * @throws PaymentFailedException
     */
    private function processPayment(Order $order): void
    {
        $result = $this->paymentGateway->charge(
            amount: $order->total,
            currency: $order->currency,
            customerId: $order->user_id,
        );

        if (! $result->successful) {
            throw new PaymentFailedException(
                "Payment failed for order {$order->id}: {$result->message}"
            );
        }

        $order->update(['payment_id' => $result->transactionId]);
    }
}
```

### 2. Data Class

```php
<?php

declare(strict_types=1);

namespace App\Data;

use Illuminate\Http\Request;

final readonly class CreateOrderData
{
    /**
     * @param  array<int, array{product_id: int, quantity: int}>  $items
     */
    public function __construct(
        public int $userId,
        public array $items,
        public int $shippingAddressId,
        public ?string $couponCode = null,
    ) {}

    public static function fromRequest(Request $request): self
    {
        return new self(
            userId: (int) $request->user()->id,
            items: $request->input('items'),
            shippingAddressId: (int) $request->input('shipping_address_id'),
            couponCode: $request->input('coupon_code'),
        );
    }

    /**
     * @param  array{user_id: int, items: array<int, array{product_id: int, quantity: int}>, shipping_address_id: int, coupon_code?: string|null}  $data
     */
    public static function fromArray(array $data): self
    {
        return new self(
            userId: $data['user_id'],
            items: $data['items'],
            shippingAddressId: $data['shipping_address_id'],
            couponCode: $data['coupon_code'] ?? null,
        );
    }
}
```

### 3. Usage from Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Actions\CreateOrder;
use App\Data\CreateOrderData;
use App\Http\Requests\StoreOrderRequest;
use App\Http\Resources\OrderResource;
use Illuminate\Http\JsonResponse;
use Symfony\Component\HttpFoundation\Response;

final class OrderController extends Controller
{
    public function __construct(
        private readonly CreateOrder $createOrder,
    ) {}

    public function store(StoreOrderRequest $request): JsonResponse
    {
        $data = CreateOrderData::fromRequest($request);

        $order = ($this->createOrder)($data);

        return OrderResource::make($order)
            ->response()
            ->setStatusCode(Response::HTTP_CREATED);
    }
}
```

### 4. Usage from Job

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Actions\CreateOrder;
use App\Data\CreateOrderData;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

final class ProcessBulkOrders implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * @param  array<int, array{user_id: int, items: array, shipping_address_id: int, coupon_code?: string|null}>  $ordersData
     */
    public function __construct(
        private readonly array $ordersData,
    ) {}

    public function handle(CreateOrder $createOrder): void
    {
        foreach ($this->ordersData as $index => $orderData) {
            try {
                $data = CreateOrderData::fromArray($orderData);
                $order = ($createOrder)($data);

                Log::info("Bulk order created successfully.", [
                    'index' => $index,
                    'order_id' => $order->id,
                ]);
            } catch (\Throwable $e) {
                Log::error("Failed to create bulk order.", [
                    'index' => $index,
                    'user_id' => $orderData['user_id'],
                    'error' => $e->getMessage(),
                ]);
            }
        }
    }
}
```

### 5. Usage from Artisan Command

```php
<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Actions\CreateOrder;
use App\Data\CreateOrderData;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;

final class ImportOrdersFromCsv extends Command
{
    protected $signature = 'orders:import {file : Path to the CSV file}';

    protected $description = 'Import orders from a CSV file';

    public function handle(CreateOrder $createOrder): int
    {
        $path = $this->argument('file');

        if (! file_exists($path)) {
            $this->error("File not found: {$path}");

            return self::FAILURE;
        }

        $rows = array_map('str_getcsv', file($path));
        $headers = array_shift($rows);

        $this->info("Importing " . count($rows) . " orders...");
        $bar = $this->output->createProgressBar(count($rows));
        $bar->start();

        $succeeded = 0;
        $failed = 0;

        foreach ($rows as $row) {
            $mapped = array_combine($headers, $row);

            try {
                $data = CreateOrderData::fromArray([
                    'user_id' => (int) $mapped['user_id'],
                    'items' => json_decode($mapped['items'], true, 512, JSON_THROW_ON_ERROR),
                    'shipping_address_id' => (int) $mapped['shipping_address_id'],
                    'coupon_code' => $mapped['coupon_code'] ?: null,
                ]);

                ($createOrder)($data);
                $succeeded++;
            } catch (\Throwable $e) {
                $failed++;
                Log::error("CSV import failed for row.", [
                    'user_id' => $mapped['user_id'] ?? 'unknown',
                    'error' => $e->getMessage(),
                ]);
            }

            $bar->advance();
        }

        $bar->finish();
        $this->newLine(2);
        $this->info("Done. Succeeded: {$succeeded}, Failed: {$failed}");

        return $failed > 0 ? self::FAILURE : self::SUCCESS;
    }
}
```

### 6. Unit Test

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Actions;

use App\Actions\CreateOrder;
use App\Data\CreateOrderData;
use App\Events\OrderCreated;
use App\Exceptions\InsufficientStockException;
use App\Exceptions\PaymentFailedException;
use App\Models\Order;
use App\Repositories\OrderRepository;
use App\Services\PaymentGateway;
use App\Services\TaxCalculator;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Mockery;
use Mockery\MockInterface;
use Tests\TestCase;

final class CreateOrderTest extends TestCase
{
    use RefreshDatabase;

    private MockInterface&OrderRepository $orderRepository;
    private MockInterface&PaymentGateway $paymentGateway;
    private MockInterface&TaxCalculator $taxCalculator;
    private CreateOrder $action;

    protected function setUp(): void
    {
        parent::setUp();

        $this->orderRepository = Mockery::mock(OrderRepository::class);
        $this->paymentGateway = Mockery::mock(PaymentGateway::class);
        $this->taxCalculator = Mockery::mock(TaxCalculator::class);

        $this->action = new CreateOrder(
            $this->orderRepository,
            $this->paymentGateway,
            $this->taxCalculator,
        );
    }

    public function test_it_creates_an_order_successfully(): void
    {
        Event::fake([OrderCreated::class]);

        $data = new CreateOrderData(
            userId: 1,
            items: [['product_id' => 10, 'quantity' => 2]],
            shippingAddressId: 5,
            couponCode: 'SAVE10',
        );

        $order = Mockery::mock(Order::class)->makePartial();
        $order->id = 99;
        $order->total = 5000;
        $order->currency = 'USD';
        $order->user_id = 1;

        $this->orderRepository
            ->shouldReceive('hasStock')
            ->with(10, 2)
            ->once()
            ->andReturnTrue();

        $this->taxCalculator
            ->shouldReceive('calculate')
            ->with($data->items, $data->shippingAddressId)
            ->once()
            ->andReturn(500);

        $this->orderRepository
            ->shouldReceive('create')
            ->once()
            ->andReturn($order);

        $this->paymentGateway
            ->shouldReceive('charge')
            ->once()
            ->andReturn((object) ['successful' => true, 'transactionId' => 'txn_123', 'message' => '']);

        $order->shouldReceive('update')
            ->with(['payment_id' => 'txn_123'])
            ->once();

        $result = ($this->action)($data);

        $this->assertSame($order, $result);

        Event::assertDispatched(OrderCreated::class, fn ($event) => $event->order->id === 99);
    }

    public function test_it_throws_when_stock_is_insufficient(): void
    {
        $data = new CreateOrderData(
            userId: 1,
            items: [['product_id' => 10, 'quantity' => 999]],
            shippingAddressId: 5,
        );

        $this->orderRepository
            ->shouldReceive('hasStock')
            ->with(10, 999)
            ->once()
            ->andReturnFalse();

        $this->expectException(InsufficientStockException::class);

        ($this->action)($data);
    }

    public function test_it_rolls_back_transaction_on_payment_failure(): void
    {
        $data = new CreateOrderData(
            userId: 1,
            items: [['product_id' => 10, 'quantity' => 1]],
            shippingAddressId: 5,
        );

        $order = Mockery::mock(Order::class)->makePartial();
        $order->id = 50;
        $order->total = 3000;
        $order->currency = 'USD';
        $order->user_id = 1;

        $this->orderRepository
            ->shouldReceive('hasStock')
            ->andReturnTrue();

        $this->taxCalculator
            ->shouldReceive('calculate')
            ->andReturn(300);

        $this->orderRepository
            ->shouldReceive('create')
            ->andReturn($order);

        $this->paymentGateway
            ->shouldReceive('charge')
            ->once()
            ->andReturn((object) ['successful' => false, 'transactionId' => null, 'message' => 'Card declined']);

        $this->expectException(PaymentFailedException::class);
        $this->expectExceptionMessage('Card declined');

        ($this->action)($data);
    }

    public function test_it_dispatches_order_created_event(): void
    {
        Event::fake([OrderCreated::class]);

        $data = new CreateOrderData(
            userId: 1,
            items: [['product_id' => 10, 'quantity' => 1]],
            shippingAddressId: 5,
        );

        $order = Mockery::mock(Order::class)->makePartial();
        $order->id = 77;
        $order->total = 1000;
        $order->currency = 'USD';
        $order->user_id = 1;

        $this->orderRepository->shouldReceive('hasStock')->andReturnTrue();
        $this->taxCalculator->shouldReceive('calculate')->andReturn(100);
        $this->orderRepository->shouldReceive('create')->andReturn($order);
        $this->paymentGateway->shouldReceive('charge')->andReturn(
            (object) ['successful' => true, 'transactionId' => 'txn_456', 'message' => '']
        );
        $order->shouldReceive('update')->once();

        ($this->action)($data);

        Event::assertDispatched(OrderCreated::class);
    }
}
```

## Generation Instructions

When the user runs `/laravel-action <ActionName>`:

1. **Detect the project root** by finding `artisan` or `composer.json`.
2. **Create the Action class** at `app/Actions/<ActionName>.php`:
   - `declare(strict_types=1)` at the top
   - `final class` with `__invoke` as the single public method
   - Constructor injection for dependencies
   - Explicit return type on `__invoke`
   - Wrap side effects in `DB::transaction` when appropriate
3. **Create the test file** at `tests/Unit/Actions/<ActionName>Test.php`:
   - Mock all dependencies
   - Test the happy path
   - Test each exception path
   - Verify events are dispatched
4. **Print a summary** of created files and next steps.
