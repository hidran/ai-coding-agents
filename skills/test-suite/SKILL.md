---
name: test-suite
description: Scaffolds test files for existing code. Supports PHPUnit, Pest, Jest, and Vitest with arrange/act/assert pattern.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Test Suite Generator

This skill reads existing source files and generates comprehensive test suites matching the project's testing framework.

## Usage

Run `/test-suite <path/to/source-file>` or `/test-suite <ClassName>`

## Process

1. **Detect framework**: Read project config (`composer.json`, `package.json`, `phpunit.xml`, `vitest.config`, `jest.config`) to determine testing framework.
2. **Read source**: Analyze the source file to extract classes, methods, dependencies.
3. **Generate tests**: Create test file with arrange/act/assert pattern for each public method.
4. **Mock dependencies**: Set up mocks for injected dependencies.

## Supported Frameworks

### PHP

- **PHPUnit**: `tests/Unit/` or `tests/Feature/` following PSR-4
- **Pest**: Same directories, using Pest's `test()` / `it()` syntax

### JavaScript/TypeScript

- **Jest**: `__tests__/` or `*.test.ts` co-located
- **Vitest**: `*.spec.ts` or `*.test.ts` co-located

## Standards

- **Arrange/Act/Assert**: Every test follows this pattern explicitly.
- **One assertion per test**: Prefer focused tests over multi-assert tests.
- **Descriptive names**: Test names describe the behavior, not the method.
- **Mock boundaries**: Mock external dependencies (HTTP, DB, filesystem), not internal classes.
- **Edge cases**: Include tests for null/empty inputs, error conditions, boundary values.
- **Data providers**: Use parameterized tests for similar test cases with different data.

## Examples

### 1. PHPUnit -- Testing a Laravel Service with Repository Dependency

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Services;

use App\Exceptions\InsufficientBalanceException;
use App\Models\Transaction;
use App\Repositories\WalletRepository;
use App\Services\WalletService;
use Mockery;
use Mockery\MockInterface;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

final class WalletServiceTest extends TestCase
{
    private MockInterface $walletRepository;
    private WalletService $walletService;

    protected function setUp(): void
    {
        parent::setUp();

        $this->walletRepository = Mockery::mock(WalletRepository::class);
        $this->walletService = new WalletService($this->walletRepository);
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }

    #[Test]
    public function it_transfers_funds_between_two_wallets(): void
    {
        // Arrange
        $senderId = 1;
        $receiverId = 2;
        $amount = 250.00;

        $this->walletRepository
            ->shouldReceive('getBalance')
            ->with($senderId)
            ->andReturn(1000.00);

        $this->walletRepository
            ->shouldReceive('debit')
            ->with($senderId, $amount)
            ->once();

        $this->walletRepository
            ->shouldReceive('credit')
            ->with($receiverId, $amount)
            ->once();

        $this->walletRepository
            ->shouldReceive('recordTransaction')
            ->once()
            ->andReturn(new Transaction([
                'sender_id' => $senderId,
                'receiver_id' => $receiverId,
                'amount' => $amount,
            ]));

        // Act
        $transaction = $this->walletService->transfer($senderId, $receiverId, $amount);

        // Assert
        $this->assertInstanceOf(Transaction::class, $transaction);
        $this->assertEquals($amount, $transaction->amount);
    }

    #[Test]
    public function it_throws_when_sender_has_insufficient_balance(): void
    {
        // Arrange
        $senderId = 1;
        $receiverId = 2;
        $amount = 5000.00;

        $this->walletRepository
            ->shouldReceive('getBalance')
            ->with($senderId)
            ->andReturn(100.00);

        // Assert
        $this->expectException(InsufficientBalanceException::class);
        $this->expectExceptionMessage('Sender does not have enough funds');

        // Act
        $this->walletService->transfer($senderId, $receiverId, $amount);
    }

    #[Test]
    #[DataProvider('invalidTransferAmountProvider')]
    public function it_rejects_invalid_transfer_amounts(float $amount, string $expectedMessage): void
    {
        // Arrange
        $senderId = 1;
        $receiverId = 2;

        // Assert
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage($expectedMessage);

        // Act
        $this->walletService->transfer($senderId, $receiverId, $amount);
    }

    public static function invalidTransferAmountProvider(): array
    {
        return [
            'zero amount' => [0.00, 'Transfer amount must be positive'],
            'negative amount' => [-50.00, 'Transfer amount must be positive'],
            'exceeds single transaction limit' => [100_001.00, 'Amount exceeds single transaction limit'],
        ];
    }

    #[Test]
    public function it_returns_transaction_history_for_a_wallet(): void
    {
        // Arrange
        $walletId = 1;
        $transactions = collect([
            new Transaction(['amount' => 100.00]),
            new Transaction(['amount' => 200.00]),
        ]);

        $this->walletRepository
            ->shouldReceive('getTransactions')
            ->with($walletId, 30)
            ->andReturn($transactions);

        // Act
        $result = $this->walletService->getHistory($walletId, days: 30);

        // Assert
        $this->assertCount(2, $result);
    }
}
```

### 2. Pest -- Same Service with Pest Syntax

```php
<?php

declare(strict_types=1);

use App\Exceptions\InsufficientBalanceException;
use App\Models\Transaction;
use App\Repositories\WalletRepository;
use App\Services\WalletService;

beforeEach(function () {
    $this->walletRepository = Mockery::mock(WalletRepository::class);
    $this->walletService = new WalletService($this->walletRepository);
});

afterEach(function () {
    Mockery::close();
});

it('transfers funds between two wallets', function () {
    // Arrange
    $senderId = 1;
    $receiverId = 2;
    $amount = 250.00;

    $this->walletRepository
        ->shouldReceive('getBalance')
        ->with($senderId)
        ->andReturn(1000.00);

    $this->walletRepository->shouldReceive('debit')->with($senderId, $amount)->once();
    $this->walletRepository->shouldReceive('credit')->with($receiverId, $amount)->once();
    $this->walletRepository
        ->shouldReceive('recordTransaction')
        ->once()
        ->andReturn(new Transaction([
            'sender_id' => $senderId,
            'receiver_id' => $receiverId,
            'amount' => $amount,
        ]));

    // Act
    $transaction = $this->walletService->transfer($senderId, $receiverId, $amount);

    // Assert
    expect($transaction)
        ->toBeInstanceOf(Transaction::class)
        ->and($transaction->amount)->toBe($amount);
});

it('throws when sender has insufficient balance', function () {
    // Arrange
    $this->walletRepository
        ->shouldReceive('getBalance')
        ->with(1)
        ->andReturn(100.00);

    // Act & Assert
    $this->walletService->transfer(1, 2, 5000.00);
})->throws(InsufficientBalanceException::class, 'Sender does not have enough funds');

it('rejects invalid transfer amounts', function (float $amount, string $expectedMessage) {
    // Act & Assert
    expect(fn () => $this->walletService->transfer(1, 2, $amount))
        ->toThrow(\InvalidArgumentException::class, $expectedMessage);
})->with([
    'zero amount' => [0.00, 'Transfer amount must be positive'],
    'negative amount' => [-50.00, 'Transfer amount must be positive'],
    'exceeds single transaction limit' => [100_001.00, 'Amount exceeds single transaction limit'],
]);

it('returns transaction history for a wallet', function () {
    // Arrange
    $transactions = collect([
        new Transaction(['amount' => 100.00]),
        new Transaction(['amount' => 200.00]),
    ]);

    $this->walletRepository
        ->shouldReceive('getTransactions')
        ->with(1, 30)
        ->andReturn($transactions);

    // Act
    $result = $this->walletService->getHistory(1, days: 30);

    // Assert
    expect($result)->toHaveCount(2);
});
```

### 3. Jest -- Testing a NestJS Service with Repository Dependency

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { OrderService } from './order.service';
import { Order, OrderStatus } from './entities/order.entity';
import { OrderItem } from './entities/order-item.entity';
import { InventoryService } from '../inventory/inventory.service';
import { InsufficientStockError } from './errors/insufficient-stock.error';
import { CreateOrderDto } from './dto/create-order.dto';

describe('OrderService', () => {
  let service: OrderService;
  let orderRepository: jest.Mocked<Repository<Order>>;
  let inventoryService: jest.Mocked<InventoryService>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        OrderService,
        {
          provide: getRepositoryToken(Order),
          useValue: {
            create: jest.fn(),
            save: jest.fn(),
            findOne: jest.fn(),
          },
        },
        {
          provide: InventoryService,
          useValue: {
            checkAvailability: jest.fn(),
            reserveStock: jest.fn(),
            releaseStock: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(OrderService);
    orderRepository = module.get(getRepositoryToken(Order));
    inventoryService = module.get(InventoryService);
  });

  describe('createOrder', () => {
    const dto: CreateOrderDto = {
      customerId: 'cust-123',
      items: [
        { productId: 'prod-1', quantity: 2, unitPrice: 29.99 },
        { productId: 'prod-2', quantity: 1, unitPrice: 49.99 },
      ],
    };

    it('should create an order when all items are in stock', async () => {
      // Arrange
      inventoryService.checkAvailability.mockResolvedValue(true);
      inventoryService.reserveStock.mockResolvedValue(undefined);

      const savedOrder = {
        id: 'order-1',
        customerId: dto.customerId,
        status: OrderStatus.CONFIRMED,
        total: 109.97,
        items: dto.items as OrderItem[],
      } as Order;

      orderRepository.create.mockReturnValue(savedOrder);
      orderRepository.save.mockResolvedValue(savedOrder);

      // Act
      const result = await service.createOrder(dto);

      // Assert
      expect(result.status).toBe(OrderStatus.CONFIRMED);
      expect(result.total).toBe(109.97);
      expect(inventoryService.reserveStock).toHaveBeenCalledTimes(2);
    });

    it('should throw InsufficientStockError when a product is unavailable', async () => {
      // Arrange
      inventoryService.checkAvailability
        .mockResolvedValueOnce(true)
        .mockResolvedValueOnce(false);

      // Act & Assert
      await expect(service.createOrder(dto)).rejects.toThrow(InsufficientStockError);
      expect(inventoryService.reserveStock).not.toHaveBeenCalled();
    });

    it('should release reserved stock if saving the order fails', async () => {
      // Arrange
      inventoryService.checkAvailability.mockResolvedValue(true);
      inventoryService.reserveStock.mockResolvedValue(undefined);
      orderRepository.create.mockReturnValue({ items: dto.items } as Order);
      orderRepository.save.mockRejectedValue(new Error('DB connection lost'));

      // Act & Assert
      await expect(service.createOrder(dto)).rejects.toThrow('DB connection lost');
      expect(inventoryService.releaseStock).toHaveBeenCalledTimes(2);
    });
  });

  describe('cancelOrder', () => {
    it('should cancel a confirmed order and release inventory', async () => {
      // Arrange
      const order = {
        id: 'order-1',
        status: OrderStatus.CONFIRMED,
        items: [{ productId: 'prod-1', quantity: 3 }],
      } as Order;

      orderRepository.findOne.mockResolvedValue(order);
      orderRepository.save.mockResolvedValue({ ...order, status: OrderStatus.CANCELLED } as Order);

      // Act
      const result = await service.cancelOrder('order-1');

      // Assert
      expect(result.status).toBe(OrderStatus.CANCELLED);
      expect(inventoryService.releaseStock).toHaveBeenCalledWith('prod-1', 3);
    });

    it('should throw when cancelling an already shipped order', async () => {
      // Arrange
      const order = { id: 'order-1', status: OrderStatus.SHIPPED } as Order;
      orderRepository.findOne.mockResolvedValue(order);

      // Act & Assert
      await expect(service.cancelOrder('order-1')).rejects.toThrow(
        'Cannot cancel an order that has already been shipped',
      );
    });
  });
});
```

### 4. Vitest -- Testing an Async Utility and React Hook

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { retryWithBackoff } from './retry';
import { renderHook, waitFor, act } from '@testing-library/react';
import { usePaginatedFetch } from './use-paginated-fetch';

describe('retryWithBackoff', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  it('should return the result on first successful attempt', async () => {
    // Arrange
    const operation = vi.fn().mockResolvedValue({ data: 'ok' });

    // Act
    const result = await retryWithBackoff(operation, { maxRetries: 3 });

    // Assert
    expect(result).toEqual({ data: 'ok' });
    expect(operation).toHaveBeenCalledTimes(1);
  });

  it('should retry on failure and succeed on a later attempt', async () => {
    // Arrange
    const operation = vi
      .fn()
      .mockRejectedValueOnce(new Error('timeout'))
      .mockRejectedValueOnce(new Error('timeout'))
      .mockResolvedValue({ data: 'recovered' });

    // Act
    const promise = retryWithBackoff(operation, { maxRetries: 3, baseDelayMs: 100 });
    await vi.runAllTimersAsync();
    const result = await promise;

    // Assert
    expect(result).toEqual({ data: 'recovered' });
    expect(operation).toHaveBeenCalledTimes(3);
  });

  it('should throw after exhausting all retries', async () => {
    // Arrange
    const operation = vi.fn().mockRejectedValue(new Error('persistent failure'));

    // Act
    const promise = retryWithBackoff(operation, { maxRetries: 2, baseDelayMs: 50 });
    await vi.runAllTimersAsync();

    // Assert
    await expect(promise).rejects.toThrow('persistent failure');
    expect(operation).toHaveBeenCalledTimes(3); // initial + 2 retries
  });
});

describe('usePaginatedFetch', () => {
  const mockFetch = vi.fn();

  beforeEach(() => {
    vi.restoreAllMocks();
    global.fetch = mockFetch;
  });

  it('should fetch the first page of results on mount', async () => {
    // Arrange
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        items: [{ id: 1, name: 'Item 1' }],
        totalPages: 5,
      }),
    });

    // Act
    const { result } = renderHook(() => usePaginatedFetch('/api/products'));

    // Assert
    await waitFor(() => {
      expect(result.current.items).toHaveLength(1);
      expect(result.current.totalPages).toBe(5);
      expect(result.current.isLoading).toBe(false);
    });
  });

  it('should append results when loading the next page', async () => {
    // Arrange
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ items: [{ id: 1 }], totalPages: 2 }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ items: [{ id: 2 }], totalPages: 2 }),
      });

    const { result } = renderHook(() => usePaginatedFetch('/api/products'));
    await waitFor(() => expect(result.current.isLoading).toBe(false));

    // Act
    act(() => result.current.loadNextPage());

    // Assert
    await waitFor(() => {
      expect(result.current.items).toHaveLength(2);
      expect(result.current.currentPage).toBe(2);
    });
  });

  it('should set error state when the fetch fails', async () => {
    // Arrange
    mockFetch.mockResolvedValue({ ok: false, status: 500 });

    // Act
    const { result } = renderHook(() => usePaginatedFetch('/api/products'));

    // Assert
    await waitFor(() => {
      expect(result.current.error).toBe('Request failed with status 500');
      expect(result.current.items).toEqual([]);
    });
  });
});
```
