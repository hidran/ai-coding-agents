---
name: nextjs-page
description: Generates a Next.js 14+ App Router page with metadata, loading state, error handling, and server/client component separation.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Next.js Page Generator

This skill scaffolds a new route in the Next.js App Router.

## Usage
Run `/nextjs-page <path/to/route>` (e.g., `/nextjs-page dashboard/settings`)

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Next.js
2. **Fetch official docs**: Use `WebFetch` on the relevant Next.js documentation page (https://nextjs.org/docs) for the feature being generated
3. **Verify patterns**: Confirm that App Router, Server Components, metadata API, and loading/error patterns are still current
4. **Use latest patterns**: If Next.js has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Next.js version the code targets

## Structure
It will create `src/app/<path>/`:
- `page.tsx`: The main page content (Server Component by default).
- `layout.tsx`: (Optional) Layout for this route segment.
- `loading.tsx`: Loading UI.
- `error.tsx`: Error boundary.
- `opengraph-image.tsx`: (Optional) Dynamic OG image.

## Standards
- **Server Components**: Default to Server Components. Use `"use client"` only for interactive leaves.
- **Data Fetching**: Use `fetch` with caching options or ORM calls directly in Server Components.
- **Metadata**: Export `metadata` object or `generateMetadata` function.
- **Suspense**: Use `Suspense` boundaries for granular loading states.

## Examples

### Page Implementation (Server Component)
```tsx
import { Suspense } from 'react';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { UserProfile } from '@/components/UserProfile';
import { UserProfileSkeleton } from '@/components/skeletons';
import { getUser } from '@/lib/data';

export const metadata: Metadata = {
  title: 'User Settings',
  description: 'Manage your account settings',
};

export default async function SettingsPage({ params }: { params: { id: string } }) {
  const user = await getUser(params.id);

  if (!user) {
    notFound();
  }

  return (
    <main className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Settings for {user.name}</h1>
      <Suspense fallback={<UserProfileSkeleton />}>
        <UserProfile user={user} />
      </Suspense>
    </main>
  );
}
```

### Loading State
```tsx
export default function Loading() {
  return (
    <div className="container mx-auto py-8 animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded mb-6"></div>
      <div className="h-64 bg-gray-100 rounded-lg"></div>
    </div>
  );
}
```

### Error Boundary
```tsx
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-xl font-semibold mb-4">Something went wrong!</h2>
      <button
        onClick={() => reset()}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  );
}
```
