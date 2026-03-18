---
name: supabase-migration
description: Generates Supabase database migrations with PostgreSQL, TypeScript types generation, and seed data. Includes indexes, constraints, and triggers.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase Migration Generator

This skill generates PostgreSQL migrations for Supabase projects with proper naming, types generation, and seed data.

## Usage

Run `/supabase-migration <table_name>` or `/supabase-migration <description>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:

1. **Check latest version**: Use `WebSearch` to find the current stable version of Supabase CLI and database features.
2. **Fetch official docs**: Use `WebFetch` on the Supabase documentation (https://supabase.com/docs/guides/database/migrations) for migration best practices.
3. **Verify patterns**: Confirm that migration naming, type generation, and CLI commands are still current.
4. **Use latest patterns**: If Supabase has introduced newer approaches, prefer those over the examples below.
5. **Note version**: Add a comment in generated SQL indicating which Supabase/PostgreSQL features are used.

## Structure

This skill generates the following files:

- `supabase/migrations/YYYYMMDDHHMMSS_create_<table>.sql` -- Migration file with table creation, indexes, triggers
- `supabase/migrations/YYYYMMDDHHMMSS_add_rls_<table>.sql` -- Row Level Security policies (separate migration)
- `supabase/seed.sql` -- Seed data (appended, not overwritten)
- Triggers type regeneration via `supabase gen types typescript`

## Standards

- **Naming convention**: Timestamp prefix `YYYYMMDDHHMMSS_<description>.sql` (e.g., `20240115120000_create_products.sql`)
- **UUID primary keys**: Use `gen_random_uuid()` as the default value for `id` columns
- **Timestamps**: Always include `created_at` and `updated_at` with `timestamptz` type
- **Updated_at trigger**: Create a `moddatetime` trigger for automatic `updated_at` maintenance
- **Indexes**: Add indexes on foreign keys, status columns, and commonly queried columns
- **Constraints**: Use CHECK constraints for data validation at the database level
- **RLS**: Enable Row Level Security on every table; create policies in a separate migration file
- **Types**: Use proper PostgreSQL types (`text`, `timestamptz`, `jsonb`, `uuid`, `numeric`, etc.)
- **Enums**: Use PostgreSQL `CREATE TYPE ... AS ENUM` or CHECK constraints for status fields
- **Idempotency**: Use `IF NOT EXISTS` where possible to make migrations safe to re-run

## Process

1. Read existing migrations in `supabase/migrations/` to understand the current schema and avoid conflicts.
2. Read `supabase/config.toml` for project configuration and local settings.
3. Generate the migration SQL file with a proper timestamp-based name.
4. Generate RLS policies in a separate migration file (timestamp incremented by 1 minute or more).
5. Append to `supabase/seed.sql` if sample data is appropriate for the new table.
6. Remind the developer to run `supabase db push` (for remote) or `supabase migration up` (for local).

## Examples

### 1. Table Creation Migration

**File**: `supabase/migrations/20240115120000_create_products.sql`

```sql
-- Supabase Migration: Create products table
-- Requires: PostgreSQL 15+, moddatetime extension
-- Supabase CLI: v1.x+

-- Enable the moddatetime extension (idempotent)
create extension if not exists moddatetime with schema extensions;

-- Create product_status enum type
do $$
begin
  if not exists (select 1 from pg_type where typname = 'product_status') then
    create type public.product_status as enum ('draft', 'published', 'archived');
  end if;
end
$$;

-- Create products table
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  description text,
  price numeric not null constraint products_price_positive check (price > 0),
  status public.product_status not null default 'draft',
  metadata jsonb default '{}'::jsonb,
  image_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Indexes
create index if not exists idx_products_user_id on public.products(user_id);
create index if not exists idx_products_status on public.products(status);
create index if not exists idx_products_created_at on public.products(created_at desc);

-- Automatic updated_at trigger
drop trigger if exists handle_updated_at on public.products;
create trigger handle_updated_at
  before update on public.products
  for each row
  execute procedure extensions.moddatetime(updated_at);

-- Enable Row Level Security
alter table public.products enable row level security;

-- Add table and column comments
comment on table public.products is 'User-created products with pricing and status tracking.';
comment on column public.products.metadata is 'Arbitrary JSON metadata for extensibility.';
```

### 2. Junction/Pivot Table Migration

**File**: `supabase/migrations/20240115120100_create_product_tags.sql`

```sql
-- Supabase Migration: Create product_tags junction table
-- Links products to tags (many-to-many)

-- Create tags table if it does not exist
create table if not exists public.tags (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  created_at timestamptz not null default now()
);

-- Create product_tags junction table
create table if not exists public.product_tags (
  product_id uuid not null references public.products(id) on delete cascade,
  tag_id uuid not null references public.tags(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (product_id, tag_id)
);

-- Indexes for reverse lookups
create index if not exists idx_product_tags_tag_id on public.product_tags(tag_id);
create index if not exists idx_product_tags_created_at on public.product_tags(created_at desc);

-- Enable RLS
alter table public.tags enable row level security;
alter table public.product_tags enable row level security;
```

### 3. RLS Policies Migration

**File**: `supabase/migrations/20240115120200_add_rls_products.sql`

```sql
-- Supabase Migration: Add RLS policies for products table
-- Policies use auth.uid() to identify the current user

-- SELECT: Authenticated users can read published products
create policy "Published products are viewable by authenticated users"
  on public.products
  for select
  to authenticated
  using (status = 'published');

-- SELECT: Owners can read all their own products regardless of status
create policy "Users can view their own products"
  on public.products
  for select
  to authenticated
  using (user_id = auth.uid());

-- INSERT: Authenticated users can create products under their own user_id
create policy "Users can create their own products"
  on public.products
  for insert
  to authenticated
  with check (user_id = auth.uid());

-- UPDATE: Owners can update their own products
create policy "Users can update their own products"
  on public.products
  for update
  to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

-- DELETE: Owners can delete their own products
create policy "Users can delete their own products"
  on public.products
  for delete
  to authenticated
  using (user_id = auth.uid());
```

### 4. TypeScript Types Generation

After applying migrations, regenerate TypeScript types:

```bash
supabase gen types typescript --local > src/types/database.types.ts
```

This produces typed definitions for every table. Example usage with the Supabase client:

```typescript
import { createClient } from '@supabase/supabase-js';
import type { Database } from './types/database.types';

const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Fully typed query -- IDE autocompletes columns and infers return types
const { data: products, error } = await supabase
  .from('products')
  .select('id, name, price, status, created_at')
  .eq('status', 'published')
  .order('created_at', { ascending: false });

// Type for insert operations
type NewProduct = Database['public']['Tables']['products']['Insert'];

const newProduct: NewProduct = {
  user_id: 'some-uuid',
  name: 'Widget',
  price: 29.99,
  status: 'draft',
};

const { data, error: insertError } = await supabase
  .from('products')
  .insert(newProduct)
  .select()
  .single();

// Type for row reads
type Product = Database['public']['Tables']['products']['Row'];

// Type for update operations
type ProductUpdate = Database['public']['Tables']['products']['Update'];
```

### 5. Seed Data

**File**: `supabase/seed.sql` (append to existing content)

```sql
-- Seed data for products and tags
-- Note: Requires a user in auth.users. In local dev, use the Supabase dashboard
-- to create a test user, then replace the UUID below.

-- Insert tags
insert into public.tags (id, name) values
  ('a1b2c3d4-0000-0000-0000-000000000001', 'electronics'),
  ('a1b2c3d4-0000-0000-0000-000000000002', 'clothing'),
  ('a1b2c3d4-0000-0000-0000-000000000003', 'home-garden')
on conflict (name) do nothing;

-- Insert sample products (replace user_id with a real auth.users id)
insert into public.products (id, user_id, name, description, price, status, metadata) values
  (
    'b1b2c3d4-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000000', -- replace with real user UUID
    'Wireless Headphones',
    'Noise-cancelling over-ear headphones with 30-hour battery life.',
    89.99,
    'published',
    '{"brand": "AudioPro", "color": "black", "wireless": true}'::jsonb
  ),
  (
    'b1b2c3d4-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000000', -- replace with real user UUID
    'Cotton T-Shirt',
    'Premium organic cotton t-shirt available in multiple sizes.',
    24.50,
    'published',
    '{"material": "organic cotton", "sizes": ["S", "M", "L", "XL"]}'::jsonb
  ),
  (
    'b1b2c3d4-0000-0000-0000-000000000003',
    '00000000-0000-0000-0000-000000000000', -- replace with real user UUID
    'Draft Product',
    'This product is still being prepared.',
    10.00,
    'draft',
    '{}'::jsonb
  )
on conflict (id) do nothing;

-- Link products to tags
insert into public.product_tags (product_id, tag_id) values
  ('b1b2c3d4-0000-0000-0000-000000000001', 'a1b2c3d4-0000-0000-0000-000000000001'),
  ('b1b2c3d4-0000-0000-0000-000000000002', 'a1b2c3d4-0000-0000-0000-000000000002'),
  ('b1b2c3d4-0000-0000-0000-000000000003', 'a1b2c3d4-0000-0000-0000-000000000001')
on conflict do nothing;
```

## Post-Generation Checklist

After generating the migration files, remind the developer to:

1. **Review the SQL** for correctness before applying.
2. **Run locally**: `supabase migration up` or `supabase db reset` (resets and re-applies all migrations + seed).
3. **Regenerate types**: `supabase gen types typescript --local > src/types/database.types.ts`
4. **Push to remote** (when ready): `supabase db push`
5. **Test RLS policies** using the Supabase dashboard SQL editor with different user roles.
6. **Verify seed data** loaded correctly via the Table Editor in the dashboard.
