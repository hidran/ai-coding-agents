---
name: laravel-livewire
description: Generates Livewire 3 components with form objects, validation, real-time features, Alpine.js integration, and tests.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Laravel Livewire Component Generator

This skill scaffolds a complete Livewire 3 component with form objects, Blade templates, and feature tests.

## Usage
Run `/laravel-livewire <ComponentName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Laravel
2. **Fetch official docs**: Use `WebFetch` on the relevant Laravel documentation page (https://laravel.com/docs/) for the feature being generated
3. **Verify patterns**: Confirm that the APIs, methods, and patterns shown in the examples below are still current
4. **Use latest patterns**: If the framework has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Laravel version the code targets

## Structure
Generates:
- `app/Livewire/<ComponentName>.php`: Livewire 3 component class.
- `resources/views/livewire/<component-name>.blade.php`: Blade template.
- `app/Livewire/Forms/<ComponentName>Form.php`: Form object (if form-based).
- `tests/Feature/Livewire/<ComponentName>Test.php`: Livewire tests.

## Standards
- **Livewire 3 syntax**: Use `#[Layout]`, `#[Title]`, `#[On]`, `#[Computed]` attributes.
- **Form Objects**: Use Livewire Form objects for form handling, not inline properties.
- **Lazy Loading**: Use `#[Lazy]` for expensive components.
- **Alpine.js**: Use `x-data`, `wire:model.live`, `@entangle` for client-side interactivity.
- **Computed properties**: Use `#[Computed]` instead of public methods for template data.
- **Pagination**: Use `WithPagination` trait.
- **File uploads**: Use `WithFileUploads` trait when needed.
- **URL query strings**: Use `#[Url]` for filterable/searchable components.

## Examples

### Full-Page Component
```php
<?php

namespace App\Livewire;

use App\Models\Product;
use Livewire\Attributes\Computed;
use Livewire\Attributes\Layout;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

#[Layout('layouts.app')]
#[Title('Products')]
class ProductIndex extends Component
{
    use WithPagination;

    #[Url(as: 'q')]
    public string $search = '';

    #[Url]
    public string $sortBy = 'created_at';

    #[Url]
    public string $sortDirection = 'desc';

    #[Url]
    public int $perPage = 10;

    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    public function sortBy(string $column): void
    {
        if ($this->sortBy === $column) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortBy = $column;
            $this->sortDirection = 'asc';
        }

        $this->resetPage();
    }

    public function delete(int $productId): void
    {
        Product::findOrFail($productId)->delete();

        $this->dispatch('product-deleted');
    }

    #[Computed]
    public function products()
    {
        return Product::query()
            ->when($this->search, fn ($query, $search) => $query
                ->where('name', 'like', "%{$search}%")
                ->orWhere('sku', 'like', "%{$search}%")
            )
            ->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage);
    }

    public function render()
    {
        return view('livewire.product-index');
    }
}
```

### Form Component
```php
<?php

namespace App\Livewire;

use App\Livewire\Forms\ProductForm;
use Livewire\Attributes\Layout;
use Livewire\Attributes\Title;
use Livewire\Component;
use Livewire\WithFileUploads;

#[Layout('layouts.app')]
#[Title('Create Product')]
class CreateProduct extends Component
{
    use WithFileUploads;

    public ProductForm $form;

    public function save(): void
    {
        $this->form->validate();
        $this->form->store();

        session()->flash('success', 'Product created successfully.');

        $this->redirectRoute('products.index', navigate: true);
    }

    public function render()
    {
        return view('livewire.create-product');
    }
}
```

### Form Object
```php
<?php

namespace App\Livewire\Forms;

use App\Models\Product;
use Livewire\Attributes\Validate;
use Livewire\Form;
use Livewire\WithFileUploads;
use Illuminate\Http\UploadedFile;

class ProductForm extends Form
{
    #[Validate('required|string|max:255')]
    public string $name = '';

    #[Validate('required|string')]
    public string $description = '';

    #[Validate('required|numeric|min:0')]
    public string $price = '';

    #[Validate('required|string|unique:products,sku')]
    public string $sku = '';

    #[Validate('nullable|image|max:2048')]
    public ?UploadedFile $image = null;

    public ?Product $product = null;

    public function setProduct(Product $product): void
    {
        $this->product = $product;
        $this->name = $product->name;
        $this->description = $product->description;
        $this->price = (string) $product->price;
        $this->sku = $product->sku;
    }

    public function store(): Product
    {
        $data = $this->except(['image', 'product']);

        if ($this->image) {
            $data['image_path'] = $this->image->store('products', 'public');
        }

        return Product::create($data);
    }

    public function update(): Product
    {
        $rules = $this->rules();
        $rules['sku'] = "required|string|unique:products,sku,{$this->product->id}";
        $this->validate($rules);

        $data = $this->except(['image', 'product']);

        if ($this->image) {
            $data['image_path'] = $this->image->store('products', 'public');
        }

        $this->product->update($data);

        return $this->product->fresh();
    }

    protected function rules(): array
    {
        return [
            'name' => 'required|string|max:255',
            'description' => 'required|string',
            'price' => 'required|numeric|min:0',
            'sku' => 'required|string|unique:products,sku',
            'image' => 'nullable|image|max:2048',
        ];
    }
}
```

### Blade Template (ProductIndex)
```blade
<div>
    {{-- Search & Filters --}}
    <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="relative">
            <input
                type="text"
                wire:model.live.debounce.300ms="search"
                placeholder="Search products..."
                class="rounded-lg border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
            <div wire:loading wire:target="search" class="absolute right-3 top-2.5">
                <svg class="h-5 w-5 animate-spin text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <select wire:model.live="perPage" class="rounded-lg border-gray-300 shadow-sm">
                <option value="10">10 per page</option>
                <option value="25">25 per page</option>
                <option value="50">50 per page</option>
            </select>

            <a href="{{ route('products.create') }}" wire:navigate class="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700">
                New Product
            </a>
        </div>
    </div>

    {{-- Table --}}
    <div class="overflow-hidden rounded-lg bg-white shadow">
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th wire:click="sortBy('name')" class="cursor-pointer px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                        Name
                        @if($sortBy === 'name')
                            <span>{{ $sortDirection === 'asc' ? '&#9650;' : '&#9660;' }}</span>
                        @endif
                    </th>
                    <th wire:click="sortBy('price')" class="cursor-pointer px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                        Price
                        @if($sortBy === 'price')
                            <span>{{ $sortDirection === 'asc' ? '&#9650;' : '&#9660;' }}</span>
                        @endif
                    </th>
                    <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500">
                        Actions
                    </th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white">
                @forelse($this->products as $product)
                    <tr wire:key="product-{{ $product->id }}">
                        <td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
                            {{ $product->name }}
                        </td>
                        <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                            ${{ number_format($product->price, 2) }}
                        </td>
                        <td class="whitespace-nowrap px-6 py-4 text-right text-sm" x-data="{ open: false }">
                            <div class="relative inline-block text-left">
                                <button @click="open = !open" class="text-gray-400 hover:text-gray-600">
                                    &hellip;
                                </button>
                                <div
                                    x-show="open"
                                    x-transition
                                    @click.outside="open = false"
                                    class="absolute right-0 z-10 mt-2 w-48 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5"
                                >
                                    <a href="{{ route('products.edit', $product) }}" wire:navigate class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Edit
                                    </a>
                                    <button
                                        wire:click="delete({{ $product->id }})"
                                        wire:confirm="Are you sure you want to delete this product?"
                                        class="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="3" class="px-6 py-12 text-center text-sm text-gray-500">
                            No products found.
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    {{-- Pagination --}}
    <div class="mt-4">
        {{ $this->products->links() }}
    </div>
</div>
```

### Livewire Test
```php
<?php

namespace Tests\Feature\Livewire;

use App\Livewire\ProductIndex;
use App\Livewire\CreateProduct;
use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Livewire\Livewire;
use Tests\TestCase;

class ProductIndexTest extends TestCase
{
    use RefreshDatabase;

    public function test_component_renders(): void
    {
        Livewire::test(ProductIndex::class)
            ->assertStatus(200)
            ->assertSee('Search products');
    }

    public function test_can_search_products(): void
    {
        Product::factory()->create(['name' => 'Widget Alpha']);
        Product::factory()->create(['name' => 'Gadget Beta']);

        Livewire::test(ProductIndex::class)
            ->set('search', 'Widget')
            ->assertSee('Widget Alpha')
            ->assertDontSee('Gadget Beta');
    }

    public function test_can_sort_products(): void
    {
        Product::factory()->create(['name' => 'Banana', 'price' => 200]);
        Product::factory()->create(['name' => 'Apple', 'price' => 100]);

        Livewire::test(ProductIndex::class)
            ->call('sortBy', 'name')
            ->assertSet('sortBy', 'name')
            ->assertSet('sortDirection', 'asc');
    }

    public function test_can_change_per_page(): void
    {
        Product::factory()->count(30)->create();

        Livewire::test(ProductIndex::class)
            ->set('perPage', 25)
            ->assertSet('perPage', 25);
    }

    public function test_can_delete_product(): void
    {
        $product = Product::factory()->create();

        Livewire::test(ProductIndex::class)
            ->call('delete', $product->id)
            ->assertDispatched('product-deleted');

        $this->assertDatabaseMissing('products', ['id' => $product->id]);
    }

    public function test_computed_products_returns_paginated_results(): void
    {
        Product::factory()->count(15)->create();

        Livewire::test(ProductIndex::class)
            ->assertSet('perPage', 10)
            ->assertViewHas('products', fn ($products) => $products->count() === 10);
    }
}

class CreateProductTest extends TestCase
{
    use RefreshDatabase;

    public function test_component_renders(): void
    {
        Livewire::test(CreateProduct::class)
            ->assertStatus(200);
    }

    public function test_form_validation(): void
    {
        Livewire::test(CreateProduct::class)
            ->call('save')
            ->assertHasErrors(['form.name' => 'required', 'form.price' => 'required']);
    }

    public function test_can_create_product(): void
    {
        Livewire::test(CreateProduct::class)
            ->set('form.name', 'New Product')
            ->set('form.description', 'A great product.')
            ->set('form.price', '29.99')
            ->set('form.sku', 'NP-001')
            ->call('save')
            ->assertHasNoErrors()
            ->assertRedirect(route('products.index'));

        $this->assertDatabaseHas('products', [
            'name' => 'New Product',
            'sku' => 'NP-001',
        ]);
    }

    public function test_can_upload_image(): void
    {
        Storage::fake('public');

        $file = UploadedFile::fake()->image('product.jpg');

        Livewire::test(CreateProduct::class)
            ->set('form.name', 'With Image')
            ->set('form.description', 'Has an image.')
            ->set('form.price', '10.00')
            ->set('form.sku', 'IMG-001')
            ->set('form.image', $file)
            ->call('save')
            ->assertHasNoErrors();

        $product = Product::where('sku', 'IMG-001')->first();
        $this->assertNotNull($product->image_path);
        Storage::disk('public')->assertExists($product->image_path);
    }
}
```

### Computed Property Access in Templates
When using `#[Computed]`, access the property via `$this->products` in Blade (not as a method call):
```blade
@foreach($this->products as $product)
    {{-- ... --}}
@endforeach
```

### Registering Routes
For full-page components, register routes directly to the component class:
```php
use App\Livewire\ProductIndex;
use App\Livewire\CreateProduct;

Route::get('/products', ProductIndex::class)->name('products.index');
Route::get('/products/create', CreateProduct::class)->name('products.create');
```
