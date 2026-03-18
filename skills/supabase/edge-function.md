---
name: supabase-edge-function
description: Generates Supabase Edge Functions (Deno/TypeScript) with proper error handling, CORS, authentication, and database access.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase Edge Function Generator

## Usage

Run `/supabase-edge-function <function-name>`

Replace `<function-name>` with a kebab-case name (e.g., `send-email`, `process-payment`, `sync-users`).

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:

1. **Check latest version**: Use `WebSearch` to find current Supabase Edge Functions documentation and Deno runtime version.
2. **Fetch official docs**: Use `WebFetch` on https://supabase.com/docs/guides/functions to retrieve the latest patterns.
3. **Verify patterns**: Confirm that `Deno.serve`, import maps, and Supabase client usage are current.
4. **Use latest patterns**: Prefer any newer Edge Functions patterns discovered over the examples below. The examples serve as a baseline -- always favor up-to-date official guidance.

## Structure

The skill generates the following files:

```
supabase/
  functions/
    <function-name>/
      index.ts          # Edge function entry point
    _shared/
      cors.ts           # Shared CORS headers (created if not exists)
      supabase-client.ts # Shared Supabase admin client (created if not exists)
```

## Standards

- **Deno runtime**: Use Deno-native APIs and imports. No Node.js built-ins.
- **Error handling**: Wrap all logic in try/catch. Return proper HTTP status codes and JSON error bodies.
- **CORS**: Always handle OPTIONS preflight requests and attach CORS headers to every response.
- **Authentication**: Verify the JWT from the `Authorization` header using the Supabase client. Return 401 for missing or invalid tokens.
- **Environment variables**: Use `Deno.env.get()` for all secrets and configuration. Never hardcode keys.
- **Types**: Full TypeScript with database types imported from a generated `database.types.ts`.
- **Response format**: Always return JSON with a consistent structure: `{ data, error }`.
- **Logging**: Use `console.log` and `console.error` for observability in the Supabase dashboard.
- **Imports**: Use `https://esm.sh/` for third-party packages or Deno import maps. Never use bare npm specifiers.

---

## Examples

### 1. Basic CRUD Function

A function that handles GET, POST, PUT, and DELETE for a resource.

**`supabase/functions/<function-name>/index.ts`**

```typescript
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders, handleCors } from "../_shared/cors.ts";
import { createAdminClient, createUserClient } from "../_shared/supabase-client.ts";
import type { Database } from "../_shared/database.types.ts";

type Item = Database["public"]["Tables"]["items"]["Row"];
type InsertItem = Database["public"]["Tables"]["items"]["Insert"];
type UpdateItem = Database["public"]["Tables"]["items"]["Update"];

Deno.serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return handleCors();
  }

  try {
    // Verify authentication
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(
        JSON.stringify({ data: null, error: "Missing Authorization header" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } },
      );
    }

    const supabase = createUserClient(authHeader.replace("Bearer ", ""));
    const url = new URL(req.url);
    const id = url.searchParams.get("id");

    switch (req.method) {
      case "GET": {
        if (id) {
          const { data, error } = await supabase
            .from("items")
            .select("*")
            .eq("id", id)
            .single();
          if (error) throw error;
          return new Response(
            JSON.stringify({ data, error: null }),
            { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
          );
        }
        const { data, error } = await supabase.from("items").select("*");
        if (error) throw error;
        return new Response(
          JSON.stringify({ data, error: null }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
        );
      }

      case "POST": {
        const body: InsertItem = await req.json();
        const { data, error } = await supabase
          .from("items")
          .insert(body)
          .select()
          .single();
        if (error) throw error;
        return new Response(
          JSON.stringify({ data, error: null }),
          { status: 201, headers: { ...corsHeaders, "Content-Type": "application/json" } },
        );
      }

      case "PUT": {
        if (!id) {
          return new Response(
            JSON.stringify({ data: null, error: "Missing id parameter" }),
            { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } },
          );
        }
        const body: UpdateItem = await req.json();
        const { data, error } = await supabase
          .from("items")
          .update(body)
          .eq("id", id)
          .select()
          .single();
        if (error) throw error;
        return new Response(
          JSON.stringify({ data, error: null }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
        );
      }

      case "DELETE": {
        if (!id) {
          return new Response(
            JSON.stringify({ data: null, error: "Missing id parameter" }),
            { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } },
          );
        }
        const { error } = await supabase.from("items").delete().eq("id", id);
        if (error) throw error;
        return new Response(
          JSON.stringify({ data: { id }, error: null }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
        );
      }

      default:
        return new Response(
          JSON.stringify({ data: null, error: "Method not allowed" }),
          { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } },
        );
    }
  } catch (err) {
    console.error("Edge function error:", err);
    const message = err instanceof Error ? err.message : "Internal server error";
    const status = (err as { code?: string })?.code === "PGRST116" ? 404 : 500;
    return new Response(
      JSON.stringify({ data: null, error: message }),
      { status, headers: { ...corsHeaders, "Content-Type": "application/json" } },
    );
  }
});
```

---

### 2. Webhook Handler (e.g., Stripe)

A function that receives external webhooks, verifies signatures, and processes events.

**`supabase/functions/stripe-webhook/index.ts`**

```typescript
import Stripe from "https://esm.sh/stripe@14?target=deno";
import { corsHeaders } from "../_shared/cors.ts";
import { createAdminClient } from "../_shared/supabase-client.ts";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, {
  apiVersion: "2024-06-20",
  httpClient: Stripe.createFetchHttpClient(),
});

const endpointSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const body = await req.text();
    const signature = req.headers.get("stripe-signature");

    if (!signature) {
      return new Response(
        JSON.stringify({ data: null, error: "Missing stripe-signature header" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } },
      );
    }

    // Verify webhook signature
    let event: Stripe.Event;
    try {
      event = await stripe.webhooks.constructEventAsync(body, signature, endpointSecret);
    } catch (err) {
      console.error("Webhook signature verification failed:", err);
      return new Response(
        JSON.stringify({ data: null, error: "Invalid signature" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } },
      );
    }

    const supabase = createAdminClient();

    // Idempotency: check if this event was already processed
    const { data: existing } = await supabase
      .from("webhook_events")
      .select("id")
      .eq("stripe_event_id", event.id)
      .single();

    if (existing) {
      console.log(`Event ${event.id} already processed, skipping`);
      return new Response(
        JSON.stringify({ data: { received: true, duplicate: true }, error: null }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
      );
    }

    // Process events by type
    switch (event.type) {
      case "checkout.session.completed": {
        const session = event.data.object as Stripe.Checkout.Session;
        console.log(`Checkout completed for customer: ${session.customer}`);
        await supabase
          .from("orders")
          .update({ status: "paid", stripe_session_id: session.id })
          .eq("stripe_customer_id", session.customer);
        break;
      }

      case "customer.subscription.updated": {
        const subscription = event.data.object as Stripe.Subscription;
        console.log(`Subscription updated: ${subscription.id}`);
        await supabase
          .from("subscriptions")
          .upsert({
            stripe_subscription_id: subscription.id,
            status: subscription.status,
            current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
          });
        break;
      }

      case "invoice.payment_failed": {
        const invoice = event.data.object as Stripe.Invoice;
        console.error(`Payment failed for invoice: ${invoice.id}`);
        await supabase
          .from("subscriptions")
          .update({ status: "past_due" })
          .eq("stripe_customer_id", invoice.customer);
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    // Record the event for idempotency
    await supabase.from("webhook_events").insert({
      stripe_event_id: event.id,
      event_type: event.type,
      processed_at: new Date().toISOString(),
    });

    return new Response(
      JSON.stringify({ data: { received: true }, error: null }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } },
    );
  } catch (err) {
    console.error("Webhook processing error:", err);
    return new Response(
      JSON.stringify({ data: null, error: "Webhook processing failed" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } },
    );
  }
});
```

---

### 3. Scheduled Function (Cron)

A function triggered by `pg_cron` for batch processing. No external auth required since it is invoked internally.

**`supabase/functions/cleanup-expired/index.ts`**

```typescript
import { createAdminClient } from "../_shared/supabase-client.ts";

Deno.serve(async (req: Request) => {
  try {
    // Verify the request comes from Supabase internal scheduler
    const authHeader = req.headers.get("Authorization");
    if (authHeader !== `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`) {
      return new Response(
        JSON.stringify({ data: null, error: "Unauthorized" }),
        { status: 401, headers: { "Content-Type": "application/json" } },
      );
    }

    const supabase = createAdminClient();
    const batchSize = 100;
    let totalDeleted = 0;
    let hasMore = true;

    // Process in batches to avoid timeouts
    while (hasMore) {
      const { data: expired, error: fetchError } = await supabase
        .from("sessions")
        .select("id")
        .lt("expires_at", new Date().toISOString())
        .limit(batchSize);

      if (fetchError) throw fetchError;

      if (!expired || expired.length === 0) {
        hasMore = false;
        break;
      }

      const ids = expired.map((row) => row.id);
      const { error: deleteError } = await supabase
        .from("sessions")
        .delete()
        .in("id", ids);

      if (deleteError) throw deleteError;

      totalDeleted += ids.length;
      console.log(`Deleted batch of ${ids.length} expired sessions`);

      if (expired.length < batchSize) {
        hasMore = false;
      }
    }

    console.log(`Cleanup complete. Total deleted: ${totalDeleted}`);

    return new Response(
      JSON.stringify({ data: { deleted: totalDeleted }, error: null }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    );
  } catch (err) {
    console.error("Cleanup cron error:", err);
    return new Response(
      JSON.stringify({ data: null, error: err instanceof Error ? err.message : "Cron job failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }
});
```

To schedule this function, create a cron job in the Supabase SQL editor:

```sql
select cron.schedule(
  'cleanup-expired-sessions',
  '0 */6 * * *',  -- Every 6 hours
  $$
  select
    net.http_post(
      url := 'https://<project-ref>.supabase.co/functions/v1/cleanup-expired',
      headers := jsonb_build_object(
        'Authorization', 'Bearer ' || current_setting('app.settings.service_role_key'),
        'Content-Type', 'application/json'
      ),
      body := '{}'::jsonb
    ) as request_id;
  $$
);
```

---

### 4. Shared CORS Module

**`supabase/functions/_shared/cors.ts`**

```typescript
const allowedOrigins = Deno.env.get("ALLOWED_ORIGINS")?.split(",") ?? ["*"];

export const corsHeaders: Record<string, string> = {
  "Access-Control-Allow-Origin": allowedOrigins.join(","),
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Max-Age": "86400",
};

/**
 * Returns a 200 response with CORS headers for OPTIONS preflight requests.
 */
export function handleCors(): Response {
  return new Response("ok", { headers: corsHeaders });
}

/**
 * Wraps a Response with CORS headers.
 */
export function withCors(response: Response): Response {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(corsHeaders)) {
    headers.set(key, value);
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
```

---

### 5. Shared Supabase Client

**`supabase/functions/_shared/supabase-client.ts`**

```typescript
import { createClient, SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";
import type { Database } from "./database.types.ts";

const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
const supabaseServiceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")!;

/**
 * Creates a Supabase admin client with service_role privileges.
 * Bypasses Row Level Security. Use for server-side operations only.
 */
export function createAdminClient(): SupabaseClient<Database> {
  return createClient<Database>(supabaseUrl, supabaseServiceRoleKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
}

/**
 * Creates a Supabase client authenticated as a specific user.
 * Respects Row Level Security policies.
 * @param accessToken - The user's JWT access token
 */
export function createUserClient(accessToken: string): SupabaseClient<Database> {
  return createClient<Database>(supabaseUrl, supabaseAnonKey, {
    global: {
      headers: { Authorization: `Bearer ${accessToken}` },
    },
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
}
```

---

### 6. Testing Locally

Start the local Supabase functions server:

```bash
supabase functions serve --env-file .env.local
```

The `.env.local` file should contain:

```env
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=<your-local-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-local-service-role-key>
ALLOWED_ORIGINS=http://localhost:3000
```

**Test a CRUD function:**

```bash
# GET all items
curl -i http://127.0.0.1:54321/functions/v1/<function-name> \
  -H "Authorization: Bearer <user-jwt>"

# GET single item
curl -i "http://127.0.0.1:54321/functions/v1/<function-name>?id=123" \
  -H "Authorization: Bearer <user-jwt>"

# POST create item
curl -i -X POST http://127.0.0.1:54321/functions/v1/<function-name> \
  -H "Authorization: Bearer <user-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test"}'

# PUT update item
curl -i -X PUT "http://127.0.0.1:54321/functions/v1/<function-name>?id=123" \
  -H "Authorization: Bearer <user-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'

# DELETE item
curl -i -X DELETE "http://127.0.0.1:54321/functions/v1/<function-name>?id=123" \
  -H "Authorization: Bearer <user-jwt>"

# OPTIONS preflight
curl -i -X OPTIONS http://127.0.0.1:54321/functions/v1/<function-name>
```

**Test a webhook function:**

```bash
# Simulate a Stripe webhook (without signature verification for local testing)
curl -i -X POST http://127.0.0.1:54321/functions/v1/stripe-webhook \
  -H "Content-Type: application/json" \
  -H "stripe-signature: test_signature" \
  -d '{
    "id": "evt_test_123",
    "type": "checkout.session.completed",
    "data": { "object": { "id": "cs_test", "customer": "cus_test" } }
  }'
```

**Deploy to production:**

```bash
# Deploy a single function
supabase functions deploy <function-name>

# Deploy all functions
supabase functions deploy

# Set secrets in production
supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx STRIPE_WEBHOOK_SECRET=whsec_xxx
```

---

## Generation Checklist

When generating a new edge function, verify the following before finalizing:

- [ ] `Deno.serve()` is used as the entry point
- [ ] OPTIONS preflight is handled and returns CORS headers
- [ ] CORS headers are attached to every response
- [ ] Authorization header is validated (unless the function is internal/cron)
- [ ] All responses use `{ data, error }` JSON structure
- [ ] Errors are caught and logged with `console.error`
- [ ] Environment variables use `Deno.env.get()` with non-null assertions or fallback values
- [ ] No Node.js or bare npm imports; all third-party imports use `https://esm.sh/`
- [ ] TypeScript types are present for request/response bodies
- [ ] Shared modules (`cors.ts`, `supabase-client.ts`) are created if they do not already exist
