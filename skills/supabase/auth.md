---
name: supabase-auth
description: Generates Supabase authentication flows including email/password, OAuth providers, magic link, and protected routes for React and Angular.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase Auth Flow Generator

## Usage

Run `/supabase-auth <flow>` where flow is: `email`, `oauth`, `magic-link`, `phone`, or `full`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:

1. **Check latest version**: Use `WebSearch` to find current Supabase Auth documentation and @supabase/supabase-js version
2. **Fetch official docs**: Use `WebFetch` on https://supabase.com/docs/guides/auth
3. **Verify patterns**: Confirm that auth methods, session handling, and SSR patterns are still current
4. **Use latest patterns**: If Supabase has introduced newer auth approaches (PKCE, SSR helpers), prefer those

## Framework Detection

Before generating files, detect the project framework:

1. **Glob** for `next.config.*`, `angular.json`, `package.json`
2. Read `package.json` to identify:
   - `next` dependency -> Next.js (React + SSR)
   - `@angular/core` dependency -> Angular
   - `react` without `next` -> React SPA
3. Check for existing Supabase setup by grepping for `@supabase/supabase-js` or `@supabase/ssr`
4. Detect TypeScript by checking for `tsconfig.json`

## Structure

Generates (varies by framework detected):

### React/Next.js

- `src/lib/supabase/client.ts`: Browser Supabase client
- `src/lib/supabase/server.ts`: Server Supabase client (if Next.js)
- `src/hooks/useAuth.ts`: Auth hook with session management
- `src/components/auth/LoginForm.tsx`: Login component
- `src/components/auth/SignUpForm.tsx`: Sign up component
- `src/components/auth/AuthGuard.tsx`: Protected route wrapper
- `src/components/auth/OAuthButtons.tsx`: OAuth provider buttons

### Angular

- `src/app/services/supabase-auth.service.ts`: Auth service
- `src/app/guards/auth.guard.ts`: Route guard
- `src/app/components/login/login.component.ts`: Login component
- `src/app/components/signup/signup.component.ts`: Signup component
- `src/app/interceptors/auth.interceptor.ts`: HTTP interceptor for tokens

## Standards

- **PKCE flow**: Use PKCE for all OAuth flows (default in Supabase v2+)
- **Session management**: Handle session refresh, expiry, and token rotation
- **Error handling**: User-friendly error messages for auth errors
- **Loading states**: Show loading during auth operations
- **Redirect handling**: Proper callback URL handling for OAuth and magic links
- **Type safety**: Use Supabase generated types for User and Session
- **SSR support**: When Next.js is detected, use `@supabase/ssr` for cookie-based session handling
- **Environment variables**: Always read from `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` (Next.js) or `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` (Vite) or `environment.ts` (Angular)

## Examples

### 1. Supabase Client Setup

#### Browser client (`src/lib/supabase/client.ts`)

```typescript
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "@/types/supabase";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

#### Server client for Next.js App Router (`src/lib/supabase/server.ts`)

```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import type { Database } from "@/types/supabase";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Called from Server Component; setAll can be ignored.
          }
        },
      },
    }
  );
}
```

#### Plain React / Vite client (`src/lib/supabase/client.ts`)

```typescript
import { createClient as createSupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/types/supabase";

export const supabase = createSupabaseClient<Database>(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);
```

### 2. Email/Password Flow (React)

#### Login component (`src/components/auth/LoginForm.tsx`)

```tsx
"use client";

import { useState, type FormEvent } from "react";
import { useAuth } from "@/hooks/useAuth";

export function LoginForm() {
  const { signIn, loading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    const { error: authError } = await signIn(email, password);
    if (authError) {
      setError(authError.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div role="alert">{error}</div>}

      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        autoComplete="email"
      />

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        autoComplete="current-password"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
```

#### Sign up component (`src/components/auth/SignUpForm.tsx`)

```tsx
"use client";

import { useState, type FormEvent } from "react";
import { useAuth } from "@/hooks/useAuth";

export function SignUpForm() {
  const { signUp, loading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    const { error: authError } = await signUp(email, password);
    if (authError) {
      setError(authError.message);
    } else {
      setSuccess(true);
    }
  }

  if (success) {
    return <p>Check your email to confirm your account.</p>;
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div role="alert">{error}</div>}

      <label htmlFor="signup-email">Email</label>
      <input
        id="signup-email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        autoComplete="email"
      />

      <label htmlFor="signup-password">Password</label>
      <input
        id="signup-password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        minLength={8}
        autoComplete="new-password"
      />

      <label htmlFor="signup-confirm">Confirm password</label>
      <input
        id="signup-confirm"
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        required
        autoComplete="new-password"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Creating account..." : "Sign up"}
      </button>
    </form>
  );
}
```

### 3. OAuth Flow (React)

#### OAuth buttons (`src/components/auth/OAuthButtons.tsx`)

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import type { Provider } from "@supabase/supabase-js";

const providers: { name: string; id: Provider }[] = [
  { name: "Google", id: "google" },
  { name: "GitHub", id: "github" },
  { name: "Discord", id: "discord" },
];

export function OAuthButtons() {
  const [loading, setLoading] = useState<Provider | null>(null);

  async function handleOAuth(provider: Provider) {
    setLoading(provider);
    const supabase = createClient();

    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) {
      console.error("OAuth error:", error.message);
      setLoading(null);
    }
  }

  return (
    <div>
      {providers.map(({ name, id }) => (
        <button
          key={id}
          onClick={() => handleOAuth(id)}
          disabled={loading !== null}
        >
          {loading === id ? `Connecting to ${name}...` : `Continue with ${name}`}
        </button>
      ))}
    </div>
  );
}
```

#### OAuth callback handler (Next.js App Router: `src/app/auth/callback/route.ts`)

```typescript
import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/dashboard";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (!error) {
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`);
}
```

### 4. Magic Link Flow

#### Magic link component (`src/components/auth/MagicLinkForm.tsx`)

```tsx
"use client";

import { useState, type FormEvent } from "react";
import { createClient } from "@/lib/supabase/client";

export function MagicLinkForm() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const supabase = createClient();
    const { error: otpError } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    setLoading(false);

    if (otpError) {
      setError(otpError.message);
    } else {
      setSent(true);
    }
  }

  if (sent) {
    return (
      <div>
        <h2>Check your email</h2>
        <p>We sent a magic link to <strong>{email}</strong>.</p>
        <p>Click the link in the email to sign in.</p>
        <button onClick={() => setSent(false)}>Use a different email</button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div role="alert">{error}</div>}

      <label htmlFor="magic-email">Email</label>
      <input
        id="magic-email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        autoComplete="email"
        placeholder="you@example.com"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Sending link..." : "Send magic link"}
      </button>
    </form>
  );
}
```

### 5. Auth Hook (React)

#### `src/hooks/useAuth.ts`

```typescript
"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import type { AuthError, Provider, Session, User } from "@supabase/supabase-js";

type AuthResult = { error: AuthError | null };

export function useAuth() {
  const supabase = useMemo(() => createClient(), []);
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session: s } }) => {
      setSession(s);
      setUser(s?.user ?? null);
      setLoading(false);
    });

    // Listen for auth state changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, s) => {
      setSession(s);
      setUser(s?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, [supabase]);

  const signIn = useCallback(
    async (email: string, password: string): Promise<AuthResult> => {
      setLoading(true);
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      setLoading(false);
      return { error };
    },
    [supabase]
  );

  const signUp = useCallback(
    async (email: string, password: string): Promise<AuthResult> => {
      setLoading(true);
      const { error } = await supabase.auth.signUp({ email, password });
      setLoading(false);
      return { error };
    },
    [supabase]
  );

  const signInWithOAuth = useCallback(
    async (provider: Provider): Promise<AuthResult> => {
      const { error } = await supabase.auth.signInWithOAuth({
        provider,
        options: { redirectTo: `${window.location.origin}/auth/callback` },
      });
      return { error };
    },
    [supabase]
  );

  const signOut = useCallback(async (): Promise<AuthResult> => {
    const { error } = await supabase.auth.signOut();
    return { error };
  }, [supabase]);

  return { user, session, loading, signIn, signUp, signInWithOAuth, signOut };
}
```

### 6. Auth Guard (React)

#### `src/components/auth/AuthGuard.tsx`

```tsx
"use client";

import { useEffect, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

interface AuthGuardProps {
  children: ReactNode;
  fallback?: ReactNode;
  redirectTo?: string;
}

export function AuthGuard({
  children,
  fallback,
  redirectTo = "/login",
}: AuthGuardProps) {
  const { session, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !session) {
      router.replace(redirectTo);
    }
  }, [loading, session, router, redirectTo]);

  if (loading) {
    return (
      fallback ?? (
        <div aria-busy="true">
          <div className="skeleton h-8 w-48 mb-4" />
          <div className="skeleton h-4 w-full mb-2" />
          <div className="skeleton h-4 w-3/4" />
        </div>
      )
    );
  }

  if (!session) {
    return null;
  }

  return <>{children}</>;
}
```

### 7. Angular Auth Service

#### `src/app/services/supabase-auth.service.ts`

```typescript
import { Injectable, signal, computed, OnDestroy } from "@angular/core";
import {
  createClient,
  SupabaseClient,
  Session,
  User,
  AuthError,
  Provider,
} from "@supabase/supabase-js";
import { environment } from "../../environments/environment";
import type { Subscription } from "@supabase/supabase-js";

@Injectable({ providedIn: "root" })
export class SupabaseAuthService implements OnDestroy {
  private supabase: SupabaseClient;
  private authSubscription: Subscription | null = null;

  private _session = signal<Session | null>(null);
  private _loading = signal(true);

  readonly session = this._session.asReadonly();
  readonly user = computed<User | null>(() => this._session()?.user ?? null);
  readonly loading = this._loading.asReadonly();
  readonly isAuthenticated = computed(() => this._session() !== null);

  constructor() {
    this.supabase = createClient(
      environment.supabaseUrl,
      environment.supabaseAnonKey
    );
    this.init();
  }

  private async init() {
    const { data } = await this.supabase.auth.getSession();
    this._session.set(data.session);
    this._loading.set(false);

    const { data: listener } = this.supabase.auth.onAuthStateChange(
      (_event, session) => {
        this._session.set(session);
        this._loading.set(false);
      }
    );
    this.authSubscription = listener.subscription;
  }

  async signIn(email: string, password: string): Promise<{ error: AuthError | null }> {
    this._loading.set(true);
    const { error } = await this.supabase.auth.signInWithPassword({ email, password });
    this._loading.set(false);
    return { error };
  }

  async signUp(email: string, password: string): Promise<{ error: AuthError | null }> {
    this._loading.set(true);
    const { error } = await this.supabase.auth.signUp({ email, password });
    this._loading.set(false);
    return { error };
  }

  async signInWithOAuth(provider: Provider): Promise<{ error: AuthError | null }> {
    const { error } = await this.supabase.auth.signInWithOAuth({
      provider,
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
    return { error };
  }

  async signInWithOtp(email: string): Promise<{ error: AuthError | null }> {
    const { error } = await this.supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
    });
    return { error };
  }

  async signOut(): Promise<{ error: AuthError | null }> {
    const { error } = await this.supabase.auth.signOut();
    return { error };
  }

  ngOnDestroy() {
    this.authSubscription?.unsubscribe();
  }
}
```

#### Functional route guard (`src/app/guards/auth.guard.ts`)

```typescript
import { inject } from "@angular/core";
import { Router, type CanActivateFn } from "@angular/router";
import { SupabaseAuthService } from "../services/supabase-auth.service";

export const authGuard: CanActivateFn = () => {
  const auth = inject(SupabaseAuthService);
  const router = inject(Router);

  if (auth.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(["/login"]);
};
```

## Post-Generation Checklist

After generating auth files, verify:

- [ ] Environment variables are documented (provide a `.env.example`)
- [ ] Supabase project URL and anon key are never hardcoded
- [ ] OAuth redirect URLs match Supabase dashboard config
- [ ] PKCE flow is used (no implicit grant)
- [ ] Session listener is cleaned up on component unmount / service destroy
- [ ] Auth callback route handles both OAuth and magic link flows
- [ ] Error messages do not leak sensitive information
- [ ] Loading states prevent duplicate submissions
