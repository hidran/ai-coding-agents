---
name: angular-feature
description: Generates a complete Angular feature with standalone components, service, routes, guards, resolver, and tests.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Angular Feature Generator

This skill scaffolds a complete feature module in an Angular application using standalone components and modern Angular patterns.

## Usage

Run `/angular-feature <FeatureName>`

## Structure

Creates `src/app/features/<feature-name>/`:

- `<feature-name>.routes.ts`: Lazy-loaded route configuration
- `<feature-name>-list/<feature-name>-list.component.ts`: List page (standalone)
- `<feature-name>-detail/<feature-name>-detail.component.ts`: Detail page (standalone)
- `<feature-name>.service.ts`: HTTP service with typed API calls
- `<feature-name>.guard.ts`: Functional route guard
- `<feature-name>.resolver.ts`: Functional route resolver
- `models/<feature-name>.model.ts`: TypeScript interfaces/types
- `<feature-name>.service.spec.ts`: Service tests
- `<feature-name>-list/<feature-name>-list.component.spec.ts`: Component tests

## Standards

- **Standalone**: All components are standalone, no NgModules
- **Signals**: Use signals for state, computed for derived state
- **Lazy Loading**: Feature routes are lazy-loaded via loadChildren
- **Functional Guards/Resolvers**: Use functional style (Angular 15+), not class-based
- **HttpClient**: Use inject() function, typed responses
- **Reactive**: Use toSignal() to bridge RxJS observables to signals where appropriate

## Step-by-Step Generation

When the user runs `/angular-feature <FeatureName>`:

1. Convert `<FeatureName>` to kebab-case for file/folder names and PascalCase for class names.
2. Detect the project root by locating `angular.json`.
3. Create all files listed in the Structure section.
4. Register the feature routes in the app's route configuration if `app.routes.ts` exists.

## Examples

All examples use a "Product" feature to illustrate the patterns.

### 1. Model Interfaces

**File**: `src/app/features/product/models/product.model.ts`

```typescript
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  imageUrl: string;
  createdAt: string;
  updatedAt: string;
}

export interface ProductListResponse {
  data: Product[];
  total: number;
  page: number;
  pageSize: number;
}

export interface ProductDetailResponse {
  data: Product;
}
```

### 2. Service

**File**: `src/app/features/product/product.service.ts`

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product, ProductListResponse, ProductDetailResponse } from './models/product.model';

@Injectable({ providedIn: 'root' })
export class ProductService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api/products';

  getAll(page = 1, pageSize = 10): Observable<ProductListResponse> {
    const params = new HttpParams()
      .set('page', page)
      .set('pageSize', pageSize);
    return this.http.get<ProductListResponse>(this.baseUrl, { params });
  }

  getById(id: number): Observable<ProductDetailResponse> {
    return this.http.get<ProductDetailResponse>(`${this.baseUrl}/${id}`);
  }

  create(product: Omit<Product, 'id' | 'createdAt' | 'updatedAt'>): Observable<Product> {
    return this.http.post<Product>(this.baseUrl, product);
  }

  update(id: number, product: Partial<Product>): Observable<Product> {
    return this.http.put<Product>(`${this.baseUrl}/${id}`, product);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
```

### 3. Functional Guard

**File**: `src/app/features/product/product.guard.ts`

```typescript
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../../core/auth.service';

export const productGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(['/login']);
};
```

### 4. Functional Resolver

**File**: `src/app/features/product/product.resolver.ts`

```typescript
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { ProductService } from './product.service';
import { Product } from './models/product.model';
import { map } from 'rxjs/operators';

export const productResolver: ResolveFn<Product> = (route) => {
  const productService = inject(ProductService);
  const id = Number(route.paramMap.get('id'));
  return productService.getById(id).pipe(map((res) => res.data));
};
```

### 5. Routes File

**File**: `src/app/features/product/product.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { productGuard } from './product.guard';
import { productResolver } from './product.resolver';

export const productRoutes: Routes = [
  {
    path: '',
    canActivate: [productGuard],
    children: [
      {
        path: '',
        loadComponent: () =>
          import('./product-list/product-list.component').then(
            (m) => m.ProductListComponent
          ),
      },
      {
        path: ':id',
        loadComponent: () =>
          import('./product-detail/product-detail.component').then(
            (m) => m.ProductDetailComponent
          ),
        resolve: { product: productResolver },
      },
    ],
  },
];
```

**Registering in `app.routes.ts`**:

```typescript
export const routes: Routes = [
  {
    path: 'products',
    loadChildren: () =>
      import('./features/product/product.routes').then((m) => m.productRoutes),
  },
];
```

### 6. List Component

**File**: `src/app/features/product/product-list/product-list.component.ts`

```typescript
import { Component, inject, computed } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { ProductService } from '../product.service';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [RouterLink, CurrencyPipe],
  template: `
    @if (products(); as productList) {
      <h1>Products</h1>
      <ul>
        @for (product of productList; track product.id) {
          <li>
            <a [routerLink]="[product.id]">
              {{ product.name }} - {{ product.price | currency }}
            </a>
          </li>
        } @empty {
          <li>No products found.</li>
        }
      </ul>
    } @else {
      <p>Loading products...</p>
    }
  `,
})
export class ProductListComponent {
  private readonly productService = inject(ProductService);

  private readonly response = toSignal(this.productService.getAll());
  readonly products = computed(() => this.response()?.data ?? []);
  readonly total = computed(() => this.response()?.total ?? 0);
}
```

### 7. Detail Component

**File**: `src/app/features/product/product-detail/product-detail.component.ts`

```typescript
import { Component, input } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { Product } from '../models/product.model';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CurrencyPipe],
  template: `
    @if (product(); as p) {
      <article>
        <h1>{{ p.name }}</h1>
        <p>{{ p.description }}</p>
        <p><strong>Price:</strong> {{ p.price | currency }}</p>
        <p><strong>Category:</strong> {{ p.category }}</p>
      </article>
    }
  `,
})
export class ProductDetailComponent {
  readonly product = input.required<Product>();
}
```

### 8. Service Tests

**File**: `src/app/features/product/product.service.spec.ts`

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { ProductService } from './product.service';

describe('ProductService', () => {
  let service: ProductService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ProductService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpTesting.verify());

  it('should fetch all products', () => {
    const mockResponse = { data: [], total: 0, page: 1, pageSize: 10 };

    service.getAll().subscribe((res) => {
      expect(res.data).toEqual([]);
      expect(res.total).toBe(0);
    });

    const req = httpTesting.expectOne('/api/products?page=1&pageSize=10');
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should fetch a product by id', () => {
    const mockProduct = { data: { id: 1, name: 'Test' } };

    service.getById(1).subscribe((res) => {
      expect(res.data.id).toBe(1);
    });

    const req = httpTesting.expectOne('/api/products/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockProduct);
  });

  it('should delete a product', () => {
    service.delete(1).subscribe();

    const req = httpTesting.expectOne('/api/products/1');
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
```

### 9. List Component Tests

**File**: `src/app/features/product/product-list/product-list.component.spec.ts`

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { ProductListComponent } from './product-list.component';

describe('ProductListComponent', () => {
  let component: ProductListComponent;
  let fixture: ComponentFixture<ProductListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProductListComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ProductListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

## Naming Conventions

| Input | kebab-case | PascalCase | camelCase |
|-------|-----------|------------|-----------|
| `Product` | `product` | `Product` | `product` |
| `UserProfile` | `user-profile` | `UserProfile` | `userProfile` |
| `OrderItem` | `order-item` | `OrderItem` | `orderItem` |

## Checklist

After generation, verify:

- [ ] All components use `standalone: true`
- [ ] Service uses `inject(HttpClient)`, not constructor injection
- [ ] Guard and resolver are functional, not class-based
- [ ] Routes use `loadComponent` and `loadChildren` for lazy loading
- [ ] Signals are used for component state
- [ ] `@for` and `@if` control flow syntax is used (not `*ngFor`/`*ngIf`)
- [ ] Tests use `provideHttpClient()` and `provideHttpClientTesting()`
- [ ] Feature routes are registered in `app.routes.ts`
