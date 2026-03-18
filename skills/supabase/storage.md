---
name: supabase-storage
description: Generates Supabase Storage bucket configuration, RLS policies, and file upload/download components for React and Angular.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase Storage Generator

## Usage

Run `/supabase-storage <bucket-name>` or `/supabase-storage <pattern>` where pattern is one of: `avatar`, `documents`, `public-assets`.

## Pre-Generation (MANDATORY)

Before generating any code, you MUST complete these steps in order:

1. **Check latest version**: Use `WebSearch` to find the current Supabase Storage documentation and changelog for any recent API changes.
2. **Fetch official docs**: Use `WebFetch` on `https://supabase.com/docs/guides/storage` to pull the latest storage guide.
3. **Verify patterns**: Confirm that the Storage API methods (`upload`, `download`, `list`, `remove`, `createSignedUrl`, `getPublicUrl`), bucket policies, and image transform features are current.
4. **Use latest patterns**: If newer Storage API patterns exist (e.g., resumable uploads, S3-compatible API), prefer them over legacy approaches.

Do NOT skip these steps. Storage APIs evolve frequently and outdated patterns cause silent failures.

## Generated Structure

The skill generates the following files depending on the pattern:

```
supabase/migrations/YYYYMMDDHHMMSS_create_storage_<bucket>.sql   # Bucket + RLS policies migration
src/hooks/useFileUpload.ts                                        # Upload hook (React)
src/components/FileUpload.tsx                                     # Upload component (React)
src/services/storage.service.ts                                   # Storage service (Angular)
```

## Standards

- **Bucket policies via SQL**: Always create buckets and policies inside migration files, never client-side. This ensures reproducibility and version control.
- **File validation**: Validate file type and size on the client AND enforce limits via bucket configuration and RLS policies. Never trust the client alone.
- **Signed URLs**: Use signed URLs for private files. Use public URLs only for buckets explicitly marked public.
- **Path structure**: Organize user files as `{user_id}/{folder}/{filename}`. This maps naturally to RLS policies that scope access by `auth.uid()`.
- **Transforms**: Use Supabase image transforms for generating thumbnails and resized variants. Do not generate separate files for each size.
- **Upsert**: Use the `upsert: true` option for avatar and profile image updates to replace existing files without needing a delete step.
- **Cleanup**: When a parent record is deleted, delete the associated storage objects. Use database triggers or application-level cleanup.

---

## Examples

### 1. Bucket Creation Migration

This migration creates a bucket with size limits, allowed MIME types, and RLS policies scoped per user.

```sql
-- supabase/migrations/20240101000000_create_storage_avatars.sql

-- Create the bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'avatars',
  'avatars',
  true,
  5242880, -- 5MB
  ARRAY['image/jpeg', 'image/png', 'image/webp', 'image/gif']
);

-- Policy: authenticated users can upload to their own folder
CREATE POLICY "Users can upload their own avatar"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy: anyone can view avatars (public bucket)
CREATE POLICY "Anyone can view avatars"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'avatars');

-- Policy: users can update their own avatar
CREATE POLICY "Users can update their own avatar"
ON storage.objects FOR UPDATE
TO authenticated
USING (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
)
WITH CHECK (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy: users can delete their own avatar
CREATE POLICY "Users can delete their own avatar"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'avatars'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

For a **private** bucket (e.g., documents), set `public` to `false` and restrict the SELECT policy:

```sql
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'documents',
  'documents',
  false,
  10485760, -- 10MB
  ARRAY['application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain']
);

CREATE POLICY "Users can read their own documents"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'documents'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

---

### 2. Avatar Upload (React)

A complete avatar upload component with drag-and-drop, preview, validation, progress, and upsert.

```tsx
// src/hooks/useFileUpload.ts
import { useState, useCallback } from 'react';
import { supabase } from '@/lib/supabase';

interface UploadOptions {
  bucket: string;
  path: string;
  upsert?: boolean;
  onProgress?: (percent: number) => void;
}

interface UploadResult {
  path: string;
  publicUrl?: string;
}

export function useFileUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(async (
    file: File,
    { bucket, path, upsert = false, onProgress }: UploadOptions
  ): Promise<UploadResult | null> => {
    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      const { data, error: uploadError } = await supabase.storage
        .from(bucket)
        .upload(path, file, {
          upsert,
          contentType: file.type,
        });

      if (uploadError) throw uploadError;

      // For public buckets, get the public URL
      const { data: urlData } = supabase.storage
        .from(bucket)
        .getPublicUrl(data.path);

      setProgress(100);
      onProgress?.(100);

      return { path: data.path, publicUrl: urlData.publicUrl };
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Upload failed';
      setError(message);
      return null;
    } finally {
      setUploading(false);
    }
  }, []);

  const remove = useCallback(async (bucket: string, paths: string[]) => {
    const { error: removeError } = await supabase.storage
      .from(bucket)
      .remove(paths);
    if (removeError) throw removeError;
  }, []);

  return { upload, remove, uploading, progress, error };
}
```

```tsx
// src/components/FileUpload.tsx
import { useState, useRef, useCallback, type DragEvent, type ChangeEvent } from 'react';
import { useFileUpload } from '@/hooks/useFileUpload';
import { supabase } from '@/lib/supabase';

interface AvatarUploadProps {
  userId: string;
  currentAvatarUrl?: string;
  onUploadComplete?: (url: string) => void;
  maxSizeMB?: number;
  acceptedTypes?: string[];
}

const DEFAULT_ACCEPTED = ['image/jpeg', 'image/png', 'image/webp'];
const BUCKET = 'avatars';

export function AvatarUpload({
  userId,
  currentAvatarUrl,
  onUploadComplete,
  maxSizeMB = 5,
  acceptedTypes = DEFAULT_ACCEPTED,
}: AvatarUploadProps) {
  const { upload, uploading, progress, error } = useFileUpload();
  const [preview, setPreview] = useState<string | null>(currentAvatarUrl ?? null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    if (!acceptedTypes.includes(file.type)) {
      return `Invalid file type. Accepted: ${acceptedTypes.join(', ')}`;
    }
    if (file.size > maxSizeMB * 1024 * 1024) {
      return `File too large. Maximum size: ${maxSizeMB}MB`;
    }
    return null;
  };

  const handleFile = useCallback(async (file: File) => {
    const validationError = validateFile(file);
    if (validationError) {
      alert(validationError);
      return;
    }

    // Show preview
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    const ext = file.name.split('.').pop() ?? 'png';
    const path = `${userId}/avatar.${ext}`;

    const result = await upload(file, {
      bucket: BUCKET,
      path,
      upsert: true,
    });

    if (result?.publicUrl) {
      // Append cache-buster to force refresh
      const url = `${result.publicUrl}?t=${Date.now()}`;
      setPreview(url);
      onUploadComplete?.(url);
    }

    URL.revokeObjectURL(objectUrl);
  }, [userId, upload, onUploadComplete]);

  const onDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <div>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        style={{
          width: 150,
          height: 150,
          borderRadius: '50%',
          border: `2px dashed ${dragOver ? '#3b82f6' : '#d1d5db'}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          overflow: 'hidden',
          position: 'relative',
          background: '#f9fafb',
        }}
      >
        {preview ? (
          <img src={preview} alt="Avatar" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        ) : (
          <span style={{ color: '#9ca3af', textAlign: 'center', fontSize: 14 }}>
            Drop image or click
          </span>
        )}
        {uploading && (
          <div style={{
            position: 'absolute', inset: 0,
            background: 'rgba(0,0,0,0.5)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: '#fff', fontSize: 18, fontWeight: 'bold',
          }}>
            {progress}%
          </div>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={acceptedTypes.join(',')}
        onChange={onChange}
        style={{ display: 'none' }}
      />
      {error && <p style={{ color: '#ef4444', marginTop: 8 }}>{error}</p>}
    </div>
  );
}
```

---

### 3. Document Upload with Metadata

Upload files to a private bucket and track metadata in a `documents` table. Generates signed URLs for secure downloads.

```sql
-- Migration: create documents table
CREATE TABLE public.documents (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name text NOT NULL,
  size integer NOT NULL,
  mime_type text NOT NULL,
  storage_path text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL
);

ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own documents"
ON public.documents FOR ALL
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());
```

```tsx
// src/hooks/useDocuments.ts
import { useState, useEffect, useCallback } from 'react';
import { supabase } from '@/lib/supabase';

interface Document {
  id: string;
  name: string;
  size: number;
  mime_type: string;
  storage_path: string;
  created_at: string;
}

const BUCKET = 'documents';
const SIGNED_URL_EXPIRY = 3600; // 1 hour

export function useDocuments(userId: string) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from('documents')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (!error && data) setDocuments(data);
    setLoading(false);
  }, [userId]);

  useEffect(() => { fetchDocuments(); }, [fetchDocuments]);

  const uploadDocument = async (file: File) => {
    const path = `${userId}/files/${Date.now()}_${file.name}`;

    const { error: uploadError } = await supabase.storage
      .from(BUCKET)
      .upload(path, file, { contentType: file.type });
    if (uploadError) throw uploadError;

    const { error: dbError } = await supabase.from('documents').insert({
      user_id: userId,
      name: file.name,
      size: file.size,
      mime_type: file.type,
      storage_path: path,
    });
    if (dbError) {
      // Rollback: remove uploaded file
      await supabase.storage.from(BUCKET).remove([path]);
      throw dbError;
    }

    await fetchDocuments();
  };

  const getDownloadUrl = async (storagePath: string): Promise<string> => {
    const { data, error } = await supabase.storage
      .from(BUCKET)
      .createSignedUrl(storagePath, SIGNED_URL_EXPIRY);
    if (error) throw error;
    return data.signedUrl;
  };

  const deleteDocument = async (doc: Document) => {
    const { error: storageError } = await supabase.storage
      .from(BUCKET)
      .remove([doc.storage_path]);
    if (storageError) throw storageError;

    const { error: dbError } = await supabase
      .from('documents')
      .delete()
      .eq('id', doc.id);
    if (dbError) throw dbError;

    await fetchDocuments();
  };

  return { documents, loading, uploadDocument, getDownloadUrl, deleteDocument };
}
```

---

### 4. Image Gallery with Transforms

Display images from a bucket folder using Supabase image transforms for thumbnails.

```tsx
// src/components/ImageGallery.tsx
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

interface GalleryProps {
  bucket: string;
  folder: string;
  thumbnailWidth?: number;
  thumbnailHeight?: number;
}

interface GalleryItem {
  name: string;
  fullUrl: string;
  thumbnailUrl: string;
}

export function ImageGallery({
  bucket,
  folder,
  thumbnailWidth = 200,
  thumbnailHeight = 200,
}: GalleryProps) {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  useEffect(() => {
    async function loadImages() {
      setLoading(true);
      const { data, error } = await supabase.storage
        .from(bucket)
        .list(folder, { sortBy: { column: 'created_at', order: 'desc' } });

      if (error || !data) {
        setLoading(false);
        return;
      }

      const images = data
        .filter((f) => f.name && !f.name.startsWith('.'))
        .map((file) => {
          const path = `${folder}/${file.name}`;
          const { data: fullData } = supabase.storage.from(bucket).getPublicUrl(path);
          const { data: thumbData } = supabase.storage.from(bucket).getPublicUrl(path, {
            transform: { width: thumbnailWidth, height: thumbnailHeight, resize: 'cover' },
          });
          return {
            name: file.name,
            fullUrl: fullData.publicUrl,
            thumbnailUrl: thumbData.publicUrl,
          };
        });

      setItems(images);
      setLoading(false);
    }
    loadImages();
  }, [bucket, folder, thumbnailWidth, thumbnailHeight]);

  const handleDelete = async (item: GalleryItem) => {
    if (!confirm(`Delete ${item.name}?`)) return;
    const { error } = await supabase.storage
      .from(bucket)
      .remove([`${folder}/${item.name}`]);
    if (!error) setItems((prev) => prev.filter((i) => i.name !== item.name));
  };

  if (loading) return <p>Loading images...</p>;
  if (!items.length) return <p>No images found.</p>;

  return (
    <>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
        {items.map((item) => (
          <div key={item.name} style={{ position: 'relative' }}>
            <img
              src={item.thumbnailUrl}
              alt={item.name}
              loading="lazy"
              onClick={() => setSelectedImage(item.fullUrl)}
              style={{ width: '100%', borderRadius: 8, cursor: 'pointer' }}
            />
            <button
              onClick={() => handleDelete(item)}
              style={{
                position: 'absolute', top: 4, right: 4,
                background: 'rgba(0,0,0,0.6)', color: '#fff',
                border: 'none', borderRadius: 4, padding: '2px 8px', cursor: 'pointer',
              }}
            >
              X
            </button>
          </div>
        ))}
      </div>
      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer', zIndex: 1000,
          }}
        >
          <img src={selectedImage} alt="Full size" style={{ maxWidth: '90vw', maxHeight: '90vh' }} />
        </div>
      )}
    </>
  );
}
```

---

### 5. Angular Storage Service

A complete Angular service with upload, download, remove, list, progress tracking via Observables, and URL helpers.

```typescript
// src/services/storage.service.ts
import { Injectable } from '@angular/core';
import { SupabaseClient, createClient } from '@supabase/supabase-js';
import { Observable, Subject, from, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../environments/environment';

export interface UploadProgress {
  percent: number;
  done: boolean;
}

export interface StorageFile {
  name: string;
  id: string | null;
  created_at: string | null;
  metadata: Record<string, unknown> | null;
}

@Injectable({ providedIn: 'root' })
export class StorageService {
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(environment.supabaseUrl, environment.supabaseAnonKey);
  }

  upload(bucket: string, path: string, file: File, options?: { upsert?: boolean }): Observable<string> {
    return from(
      this.supabase.storage.from(bucket).upload(path, file, {
        upsert: options?.upsert ?? false,
        contentType: file.type,
      })
    ).pipe(
      map(({ data, error }) => {
        if (error) throw error;
        return data.path;
      }),
      catchError((err) => throwError(() => err))
    );
  }

  download(bucket: string, path: string): Observable<Blob> {
    return from(this.supabase.storage.from(bucket).download(path)).pipe(
      map(({ data, error }) => {
        if (error) throw error;
        return data;
      }),
      catchError((err) => throwError(() => err))
    );
  }

  remove(bucket: string, paths: string[]): Observable<void> {
    return from(this.supabase.storage.from(bucket).remove(paths)).pipe(
      map(({ error }) => {
        if (error) throw error;
      }),
      catchError((err) => throwError(() => err))
    );
  }

  list(bucket: string, folder: string): Observable<StorageFile[]> {
    return from(
      this.supabase.storage.from(bucket).list(folder, {
        sortBy: { column: 'created_at', order: 'desc' },
      })
    ).pipe(
      map(({ data, error }) => {
        if (error) throw error;
        return (data ?? []) as StorageFile[];
      }),
      catchError((err) => throwError(() => err))
    );
  }

  getSignedUrl(bucket: string, path: string, expiresIn = 3600): Observable<string> {
    return from(this.supabase.storage.from(bucket).createSignedUrl(path, expiresIn)).pipe(
      map(({ data, error }) => {
        if (error) throw error;
        return data.signedUrl;
      }),
      catchError((err) => throwError(() => err))
    );
  }

  getPublicUrl(bucket: string, path: string): string {
    const { data } = this.supabase.storage.from(bucket).getPublicUrl(path);
    return data.publicUrl;
  }

  getTransformUrl(
    bucket: string,
    path: string,
    transform: { width?: number; height?: number; resize?: 'cover' | 'contain' | 'fill'; quality?: number }
  ): string {
    const { data } = this.supabase.storage.from(bucket).getPublicUrl(path, { transform });
    return data.publicUrl;
  }
}
```

---

### 6. Storage Policies SQL -- Common Patterns

#### Users manage their own folder

```sql
-- INSERT: users upload to their own folder
CREATE POLICY "Users upload to own folder"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'my-bucket'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- SELECT: users read from their own folder
CREATE POLICY "Users read own folder"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'my-bucket'
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- DELETE: users delete from their own folder
CREATE POLICY "Users delete from own folder"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'my-bucket'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

#### Public read, authenticated write

```sql
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'public-assets');

CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'public-assets');

CREATE POLICY "Authenticated users can delete their uploads"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'public-assets'
  AND owner_id = auth.uid()
);
```

#### Admin-only bucket

```sql
-- Requires a custom claim or role check
CREATE POLICY "Admins only"
ON storage.objects FOR ALL
TO authenticated
USING (
  bucket_id = 'admin-files'
  AND (auth.jwt() ->> 'role') = 'admin'
)
WITH CHECK (
  bucket_id = 'admin-files'
  AND (auth.jwt() ->> 'role') = 'admin'
);
```

#### Team-shared bucket

```sql
-- Requires a team_members table with user_id and team_id columns
CREATE POLICY "Team members can access shared files"
ON storage.objects FOR SELECT
TO authenticated
USING (
  bucket_id = 'team-files'
  AND (storage.foldername(name))[1] IN (
    SELECT team_id::text FROM public.team_members
    WHERE user_id = auth.uid()
  )
);

CREATE POLICY "Team members can upload to their team folder"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'team-files'
  AND (storage.foldername(name))[1] IN (
    SELECT team_id::text FROM public.team_members
    WHERE user_id = auth.uid()
  )
);

CREATE POLICY "Team members can delete from their team folder"
ON storage.objects FOR DELETE
TO authenticated
USING (
  bucket_id = 'team-files'
  AND (storage.foldername(name))[1] IN (
    SELECT team_id::text FROM public.team_members
    WHERE user_id = auth.uid()
  )
);
```

---

## Pattern Quick Reference

| Pattern          | Bucket   | Public | Typical Size Limit | Use Case                        |
|------------------|----------|--------|--------------------|---------------------------------|
| `avatar`         | avatars  | Yes    | 5MB                | User profile images             |
| `documents`      | documents| No     | 10MB               | Private user files              |
| `public-assets`  | assets   | Yes    | 20MB               | Shared images, downloads        |

## Notes

- Always run `supabase db push` or `supabase migration up` after adding migration files.
- For large file uploads (>6MB), consider using resumable uploads via the `tus` protocol supported by Supabase Storage v2+.
- Image transforms are only available on paid plans and for public buckets or via signed URLs with transforms.
- When using transforms, the first request generates the transformed image and subsequent requests are served from cache.
