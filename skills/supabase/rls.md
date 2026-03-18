---
name: supabase-rls
description: Generates Supabase Row Level Security (RLS) policies for tables with common patterns like owner-based, role-based, team-based, and public read access.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase RLS Policy Generator

## Usage

Run `/supabase-rls <table_name>` or `/supabase-rls <pattern>` where pattern is one of: `owner`, `team`, `role`, `public-read`, `hierarchical`.

## Pre-Generation (MANDATORY)

Before generating any code, you MUST follow these steps in order:

1. **Check latest version**: Use `WebSearch` to find current Supabase RLS documentation and best practices for the current year.
2. **Fetch official docs**: Use `WebFetch` on https://supabase.com/docs/guides/database/postgres/row-level-security to get the canonical reference.
3. **Verify patterns**: Confirm that `auth.uid()`, `auth.jwt()`, and policy syntax are still current. Check for any deprecations or new auth helpers.
4. **Use latest patterns**: Prefer any newer Supabase auth helpers or syntax over the examples below. If the official docs show a different approach, use that instead.

Only after completing all four steps should you proceed to generate SQL.

## Structure

Generates:
- `supabase/migrations/YYYYMMDDHHMMSS_rls_<table>.sql`: RLS migration file

The timestamp format is `YYYYMMDDHHMMSS` (e.g., `20260318120000`). Use the current date and time when generating.

## Standards

- **Always enable RLS**: Every generated migration must include `ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;`
- **Force RLS for table owner**: Include `ALTER TABLE <table> FORCE ROW LEVEL SECURITY;` so that even the table owner is subject to policies.
- **Separate policies per operation**: Create one policy per operation (SELECT, INSERT, UPDATE, DELETE). Never combine operations into a single policy.
- **Descriptive names**: Policy names must describe what they allow, following the format `<table>_<operation>_<scope>` (e.g., `posts_select_own`, `posts_insert_authenticated`).
- **Use auth.uid()**: For user-owned resources, match against `auth.uid()`.
- **Use auth.jwt()**: For role-based or custom claims access, extract roles from `auth.jwt() -> 'app_metadata'` or `auth.jwt() -> 'user_metadata'`.
- **Service role bypass**: Always include a comment noting that the `service_role` key bypasses RLS entirely.
- **Performance**: Use simple, direct expressions in policies. Avoid correlated subqueries when possible; prefer helper functions or JOINs.
- **Idempotent migrations**: Use `DROP POLICY IF EXISTS` before `CREATE POLICY` so migrations can be re-run safely.

## Patterns

### 1. Owner-Based Access

Users can CRUD their own records, matched via `user_id = auth.uid()`.

```sql
-- =============================================================
-- RLS: Owner-based access for <table>
-- Users can only access rows where user_id matches their auth ID.
-- Note: service_role key bypasses RLS entirely.
-- =============================================================

ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <table> FORCE ROW LEVEL SECURITY;

-- SELECT: Users can read their own rows
DROP POLICY IF EXISTS "<table>_select_own" ON <table>;
CREATE POLICY "<table>_select_own"
  ON <table>
  FOR SELECT
  USING (user_id = auth.uid());

-- INSERT: Users can insert rows for themselves
DROP POLICY IF EXISTS "<table>_insert_own" ON <table>;
CREATE POLICY "<table>_insert_own"
  ON <table>
  FOR INSERT
  WITH CHECK (user_id = auth.uid());

-- UPDATE: Users can update their own rows
DROP POLICY IF EXISTS "<table>_update_own" ON <table>;
CREATE POLICY "<table>_update_own"
  ON <table>
  FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- DELETE: Users can delete their own rows
DROP POLICY IF EXISTS "<table>_delete_own" ON <table>;
CREATE POLICY "<table>_delete_own"
  ON <table>
  FOR DELETE
  USING (user_id = auth.uid());
```

### 2. Team-Based Access

Users can access records belonging to their team. Requires a `team_members` junction table with columns `team_id` and `user_id`.

```sql
-- =============================================================
-- RLS: Team-based access for <table>
-- Users can access rows belonging to teams they are a member of.
-- Requires: team_members(team_id, user_id) junction table.
-- Note: service_role key bypasses RLS entirely.
-- =============================================================

-- Helper function to check team membership
CREATE OR REPLACE FUNCTION public.is_team_member(_team_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members
    WHERE team_id = _team_id
      AND user_id = auth.uid()
  );
$$;

ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <table> FORCE ROW LEVEL SECURITY;

-- SELECT: Team members can read team rows
DROP POLICY IF EXISTS "<table>_select_team" ON <table>;
CREATE POLICY "<table>_select_team"
  ON <table>
  FOR SELECT
  USING (public.is_team_member(team_id));

-- INSERT: Team members can insert into their team
DROP POLICY IF EXISTS "<table>_insert_team" ON <table>;
CREATE POLICY "<table>_insert_team"
  ON <table>
  FOR INSERT
  WITH CHECK (public.is_team_member(team_id));

-- UPDATE: Team members can update their team's rows
DROP POLICY IF EXISTS "<table>_update_team" ON <table>;
CREATE POLICY "<table>_update_team"
  ON <table>
  FOR UPDATE
  USING (public.is_team_member(team_id))
  WITH CHECK (public.is_team_member(team_id));

-- DELETE: Team members can delete their team's rows
DROP POLICY IF EXISTS "<table>_delete_team" ON <table>;
CREATE POLICY "<table>_delete_team"
  ON <table>
  FOR DELETE
  USING (public.is_team_member(team_id));
```

### 3. Role-Based Access

Different permissions based on user role stored in JWT custom claims (`app_metadata`) or a `profiles` table. Supports three roles: `admin` (full access), `editor` (read + update), `viewer` (read only).

```sql
-- =============================================================
-- RLS: Role-based access for <table>
-- admin: full CRUD
-- editor: SELECT + UPDATE
-- viewer: SELECT only
-- Roles are read from auth.jwt() -> 'app_metadata' -> 'role'.
-- Note: service_role key bypasses RLS entirely.
-- =============================================================

-- Helper function to get the current user's role
CREATE OR REPLACE FUNCTION public.get_user_role()
RETURNS text
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT coalesce(
    auth.jwt() -> 'app_metadata' ->> 'role',
    'viewer'
  );
$$;

ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <table> FORCE ROW LEVEL SECURITY;

-- SELECT: All roles can read
DROP POLICY IF EXISTS "<table>_select_all_roles" ON <table>;
CREATE POLICY "<table>_select_all_roles"
  ON <table>
  FOR SELECT
  USING (public.get_user_role() IN ('admin', 'editor', 'viewer'));

-- INSERT: Only admins can insert
DROP POLICY IF EXISTS "<table>_insert_admin" ON <table>;
CREATE POLICY "<table>_insert_admin"
  ON <table>
  FOR INSERT
  WITH CHECK (public.get_user_role() = 'admin');

-- UPDATE: Admins and editors can update
DROP POLICY IF EXISTS "<table>_update_editor" ON <table>;
CREATE POLICY "<table>_update_editor"
  ON <table>
  FOR UPDATE
  USING (public.get_user_role() IN ('admin', 'editor'))
  WITH CHECK (public.get_user_role() IN ('admin', 'editor'));

-- DELETE: Only admins can delete
DROP POLICY IF EXISTS "<table>_delete_admin" ON <table>;
CREATE POLICY "<table>_delete_admin"
  ON <table>
  FOR DELETE
  USING (public.get_user_role() = 'admin');
```

### 4. Public Read, Authenticated Write

Anyone can read (no authentication required). Only authenticated users can insert. Only the row owner can update or delete.

```sql
-- =============================================================
-- RLS: Public read, authenticated write for <table>
-- SELECT: open to everyone (anon + authenticated)
-- INSERT: authenticated users only
-- UPDATE/DELETE: row owner only (user_id = auth.uid())
-- Note: service_role key bypasses RLS entirely.
-- =============================================================

ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <table> FORCE ROW LEVEL SECURITY;

-- SELECT: Public read access (no auth required)
DROP POLICY IF EXISTS "<table>_select_public" ON <table>;
CREATE POLICY "<table>_select_public"
  ON <table>
  FOR SELECT
  USING (true);

-- INSERT: Only authenticated users can create rows
DROP POLICY IF EXISTS "<table>_insert_authenticated" ON <table>;
CREATE POLICY "<table>_insert_authenticated"
  ON <table>
  FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

-- UPDATE: Only the owner can update
DROP POLICY IF EXISTS "<table>_update_own" ON <table>;
CREATE POLICY "<table>_update_own"
  ON <table>
  FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- DELETE: Only the owner can delete
DROP POLICY IF EXISTS "<table>_delete_own" ON <table>;
CREATE POLICY "<table>_delete_own"
  ON <table>
  FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());
```

### 5. Hierarchical Access

Users can access their own records plus the records of users they manage. Requires a `profiles` table with a `manager_id` column pointing to the managing user.

```sql
-- =============================================================
-- RLS: Hierarchical access for <table>
-- Users can access their own rows and rows of users they manage.
-- Requires: profiles(id, manager_id) where manager_id references
--           the auth user who manages this profile.
-- Note: service_role key bypasses RLS entirely.
-- =============================================================

-- Helper: Check if the current user manages a given user (recursive)
CREATE OR REPLACE FUNCTION public.is_managed_by_current_user(_user_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    WITH RECURSIVE subordinates AS (
      -- Direct reports
      SELECT id FROM profiles
      WHERE manager_id = auth.uid()
      UNION
      -- Indirect reports (recursive)
      SELECT p.id FROM profiles p
      INNER JOIN subordinates s ON p.manager_id = s.id
    )
    SELECT 1 FROM subordinates WHERE id = _user_id
  );
$$;

ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
ALTER TABLE <table> FORCE ROW LEVEL SECURITY;

-- SELECT: Users can read own rows + rows of managed users
DROP POLICY IF EXISTS "<table>_select_hierarchy" ON <table>;
CREATE POLICY "<table>_select_hierarchy"
  ON <table>
  FOR SELECT
  USING (
    user_id = auth.uid()
    OR public.is_managed_by_current_user(user_id)
  );

-- INSERT: Users can only insert rows for themselves
DROP POLICY IF EXISTS "<table>_insert_own" ON <table>;
CREATE POLICY "<table>_insert_own"
  ON <table>
  FOR INSERT
  WITH CHECK (user_id = auth.uid());

-- UPDATE: Users can update own rows + rows of managed users
DROP POLICY IF EXISTS "<table>_update_hierarchy" ON <table>;
CREATE POLICY "<table>_update_hierarchy"
  ON <table>
  FOR UPDATE
  USING (
    user_id = auth.uid()
    OR public.is_managed_by_current_user(user_id)
  )
  WITH CHECK (
    user_id = auth.uid()
    OR public.is_managed_by_current_user(user_id)
  );

-- DELETE: Only the row owner can delete
DROP POLICY IF EXISTS "<table>_delete_own" ON <table>;
CREATE POLICY "<table>_delete_own"
  ON <table>
  FOR DELETE
  USING (user_id = auth.uid());
```

## 6. Testing RLS Policies

Use the Supabase SQL Editor or `psql` to test policies by impersonating different roles and users.

```sql
-- =============================================================
-- Testing RLS policies
-- Run these in the Supabase SQL Editor or via psql.
-- =============================================================

-- Step 1: Start a transaction so changes can be rolled back
BEGIN;

-- Step 2: Switch to the authenticated role
SET LOCAL role = 'authenticated';

-- Step 3: Set JWT claims to impersonate a specific user
SET LOCAL request.jwt.claims = '{
  "sub": "d0a1b2c3-d4e5-f6a7-b8c9-d0e1f2a3b4c5",
  "role": "authenticated",
  "app_metadata": {"role": "editor"}
}';

-- Step 4: Test SELECT (should only return rows matching the policy)
SELECT * FROM posts;

-- Step 5: Test INSERT (should succeed or fail based on policy)
INSERT INTO posts (title, content, user_id)
VALUES ('Test Post', 'Testing RLS', 'd0a1b2c3-d4e5-f6a7-b8c9-d0e1f2a3b4c5');

-- Step 6: Test UPDATE on own row (should succeed)
UPDATE posts SET title = 'Updated' WHERE id = '<some-id>';

-- Step 7: Test UPDATE on another user's row (should fail / affect 0 rows)
UPDATE posts SET title = 'Hacked' WHERE user_id != 'd0a1b2c3-d4e5-f6a7-b8c9-d0e1f2a3b4c5';

-- Step 8: Verify row counts
SELECT count(*) FROM posts;

-- Step 9: Roll back so no test data persists
ROLLBACK;
```

You can also test with the `anon` role:

```sql
BEGIN;
SET LOCAL role = 'anon';
-- This should work for public-read tables, fail for owner-based tables
SELECT * FROM posts;
ROLLBACK;
```

## 7. Common Mistakes

### Mistake 1: Forgetting to enable RLS
RLS is disabled by default. If you create policies but forget `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`, the policies have no effect and all rows are accessible.

**Fix**: Always include `ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;` at the top of every migration.

### Mistake 2: Missing WITH CHECK on INSERT/UPDATE
The `USING` clause filters which rows can be seen, but `WITH CHECK` controls which rows can be written. Omitting `WITH CHECK` on INSERT or UPDATE means users could insert rows they cannot subsequently read, or the policy silently permits all writes.

**Fix**: Always pair `USING` with `WITH CHECK` on UPDATE policies. Always include `WITH CHECK` on INSERT policies.

### Mistake 3: Using subqueries directly in policies instead of SECURITY DEFINER functions
Inline subqueries in policies execute with the calling user's permissions and can be slow. If the referenced table also has RLS, you may get unexpected empty results or circular dependency issues.

**Fix**: Wrap complex lookups in `SECURITY DEFINER` functions with `SET search_path = public`. This executes with elevated privileges and avoids RLS recursion.

### Mistake 4: Not restricting the user_id on INSERT
Without a `WITH CHECK (user_id = auth.uid())` on INSERT, an authenticated user could insert rows with another user's ID, impersonating them.

**Fix**: Always enforce `user_id = auth.uid()` in the `WITH CHECK` clause of INSERT policies for owner-based patterns.

### Mistake 5: Overly permissive SELECT policies leaking data
A common error is writing `USING (true)` on SELECT when the table should not be publicly readable, or forgetting to scope SELECT to the correct role with the `TO` clause.

**Fix**: Only use `USING (true)` when you genuinely want public (anonymous) read access. For authenticated-only access, add `TO authenticated` and scope the `USING` clause. Always audit SELECT policies to confirm they match your access intent.
