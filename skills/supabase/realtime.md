---
name: supabase-realtime
description: Generates Supabase Realtime subscriptions, broadcast channels, and presence tracking for React and Angular applications.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Supabase Realtime Generator

This skill generates Supabase Realtime subscriptions, broadcast channels, and presence tracking implementations for React and Angular applications using `@supabase/supabase-js` v2+ channel API.

## Usage

Run `/supabase-realtime <pattern>` where pattern is one of:

- `db-changes` - Database change subscriptions (INSERT, UPDATE, DELETE)
- `broadcast` - Broadcast channels for ephemeral messaging
- `presence` - Presence tracking for online users
- `full` - Complete implementation with all three patterns

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:

1. **Check latest version**: Use `WebSearch` to find the current Supabase Realtime documentation and any recent API changes.
2. **Fetch official docs**: Use `WebFetch` on https://supabase.com/docs/guides/realtime to get the latest patterns.
3. **Verify patterns**: Confirm that channel API, broadcast, and presence patterns are still current.
4. **Use latest patterns**: If Supabase has introduced newer Realtime API patterns, prefer those over the examples below.

## Structure

This skill generates the following files depending on the pattern:

### React (`db-changes`, `broadcast`, `presence`, `full`)
- `src/hooks/useRealtimeSubscription.ts` - Generic database changes hook
- `src/hooks/usePresence.ts` - Presence tracking hook
- `src/hooks/useBroadcast.ts` - Broadcast channel hook

### Angular (`db-changes`, `broadcast`, `presence`, `full`)
- `src/services/realtime.service.ts` - Complete Realtime service with Observables and signals

## Standards

Follow these standards in all generated code:

- **Cleanup**: Always unsubscribe and remove channels on component unmount (`useEffect` cleanup in React, `DestroyRef` in Angular).
- **Error handling**: Handle subscription errors, connection drops, and automatic reconnection.
- **Type safety**: Type all payloads using database types from `@supabase/supabase-js`. Define explicit interfaces for broadcast and presence payloads.
- **Filtering**: Use server-side filters (e.g., `filter: 'room_id=eq.123'`) to reduce incoming payload volume.
- **RLS**: Supabase Realtime respects Row Level Security policies. Always document this in generated code comments so developers understand that users only receive changes they are authorized to see.
- **Performance**: Throttle or debounce UI updates for high-frequency changes. Batch state updates where possible.

## Examples

### 1. Database Changes (React Hook) - `useRealtimeSubscription`

```typescript
import { useEffect, useState, useCallback, useRef } from 'react';
import { RealtimeChannel, RealtimePostgresChangesPayload } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

// Define your database types (typically generated via supabase gen types)
interface Database {
  public: {
    Tables: {
      messages: {
        Row: {
          id: string;
          content: string;
          room_id: string;
          user_id: string;
          created_at: string;
        };
        Insert: Omit<Database['public']['Tables']['messages']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['messages']['Insert']>;
      };
    };
  };
}

type TableName = keyof Database['public']['Tables'];
type Row<T extends TableName> = Database['public']['Tables'][T]['Row'];

type PostgresEvent = 'INSERT' | 'UPDATE' | 'DELETE' | '*';

interface UseRealtimeSubscriptionOptions<T extends TableName> {
  table: T;
  event?: PostgresEvent;
  filter?: string;       // e.g., 'room_id=eq.123'
  schema?: string;       // defaults to 'public'
  enabled?: boolean;     // toggle subscription on/off
  onError?: (error: Error) => void;
}

interface UseRealtimeSubscriptionResult<T extends TableName> {
  data: Row<T>[];
  status: 'connecting' | 'connected' | 'disconnected' | 'error';
  error: Error | null;
}

/**
 * Subscribe to realtime database changes on a table.
 * Realtime respects RLS policies - users only receive changes they are authorized to see.
 */
export function useRealtimeSubscription<T extends TableName>({
  table,
  event = '*',
  filter,
  schema = 'public',
  enabled = true,
  onError,
}: UseRealtimeSubscriptionOptions<T>): UseRealtimeSubscriptionResult<T> {
  const [data, setData] = useState<Row<T>[]>([]);
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [error, setError] = useState<Error | null>(null);
  const channelRef = useRef<RealtimeChannel | null>(null);

  // Fetch initial data
  const fetchInitial = useCallback(async () => {
    let query = supabase.from(table).select('*');
    if (filter) {
      const [column, opValue] = filter.split('=');
      const [op, value] = opValue.split('.');
      query = query.filter(column, op, value);
    }
    const { data: rows, error: fetchError } = await query;
    if (fetchError) {
      const err = new Error(fetchError.message);
      setError(err);
      onError?.(err);
      return;
    }
    setData((rows as Row<T>[]) ?? []);
  }, [table, filter, onError]);

  useEffect(() => {
    if (!enabled) {
      setStatus('disconnected');
      return;
    }

    fetchInitial();
    setStatus('connecting');

    const channelName = `${table}-${filter ?? 'all'}-${Date.now()}`;

    const channelConfig: Record<string, unknown> = {
      event,
      schema,
      table,
    };
    if (filter) channelConfig.filter = filter;

    const channel = supabase
      .channel(channelName)
      .on(
        'postgres_changes' as any,
        channelConfig,
        (payload: RealtimePostgresChangesPayload<Row<T>>) => {
          switch (payload.eventType) {
            case 'INSERT':
              setData((prev) => [...prev, payload.new as Row<T>]);
              break;
            case 'UPDATE':
              setData((prev) =>
                prev.map((item) =>
                  (item as any).id === (payload.new as any).id
                    ? (payload.new as Row<T>)
                    : item
                )
              );
              break;
            case 'DELETE':
              setData((prev) =>
                prev.filter((item) => (item as any).id !== (payload.old as any).id)
              );
              break;
          }
        }
      )
      .subscribe((subscribedStatus) => {
        if (subscribedStatus === 'SUBSCRIBED') {
          setStatus('connected');
          setError(null);
        } else if (subscribedStatus === 'CHANNEL_ERROR') {
          const err = new Error(`Subscription error on ${table}`);
          setStatus('error');
          setError(err);
          onError?.(err);
        } else if (subscribedStatus === 'TIMED_OUT') {
          setStatus('error');
          const err = new Error(`Subscription timed out on ${table}`);
          setError(err);
          onError?.(err);
        }
      });

    channelRef.current = channel;

    // Cleanup: unsubscribe and remove channel on unmount
    return () => {
      if (channelRef.current) {
        supabase.removeChannel(channelRef.current);
        channelRef.current = null;
      }
      setStatus('disconnected');
    };
  }, [table, event, filter, schema, enabled, fetchInitial, onError]);

  return { data, status, error };
}
```

**Usage:**

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  const { data: messages, status } = useRealtimeSubscription({
    table: 'messages',
    event: 'INSERT',
    filter: `room_id=eq.${roomId}`,
  });

  if (status === 'connecting') return <div>Connecting...</div>;

  return (
    <ul>
      {messages.map((msg) => (
        <li key={msg.id}>{msg.content}</li>
      ))}
    </ul>
  );
}
```

---

### 2. Broadcast Channel (React) - Chat/Messaging

```typescript
import { useEffect, useState, useCallback, useRef } from 'react';
import { RealtimeChannel } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface BroadcastMessage {
  id: string;
  content: string;
  userId: string;
  userName: string;
  timestamp: number;
}

interface TypingIndicator {
  userId: string;
  userName: string;
  isTyping: boolean;
}

interface UseBroadcastOptions {
  roomId: string;
  userId: string;
  userName: string;
}

interface UseBroadcastResult {
  messages: BroadcastMessage[];
  typingUsers: string[];
  onlineCount: number;
  sendMessage: (content: string) => void;
  setTyping: (isTyping: boolean) => void;
  status: string;
}

/**
 * Broadcast channel hook for ephemeral chat messaging.
 * Messages sent via broadcast are NOT persisted - combine with database
 * changes if persistence is needed.
 */
export function useBroadcast({
  roomId,
  userId,
  userName,
}: UseBroadcastOptions): UseBroadcastResult {
  const [messages, setMessages] = useState<BroadcastMessage[]>([]);
  const [typingUsers, setTypingUsers] = useState<string[]>([]);
  const [onlineCount, setOnlineCount] = useState(0);
  const [status, setStatus] = useState('disconnected');
  const channelRef = useRef<RealtimeChannel | null>(null);
  const typingTimeoutRef = useRef<Map<string, NodeJS.Timeout>>(new Map());

  useEffect(() => {
    const channel = supabase.channel(`room:${roomId}`, {
      config: { broadcast: { self: false } },
    });

    channel
      .on('broadcast', { event: 'message' }, ({ payload }) => {
        const msg = payload as BroadcastMessage;
        setMessages((prev) => [...prev, msg]);
      })
      .on('broadcast', { event: 'typing' }, ({ payload }) => {
        const { userId: typingUserId, userName: typingName, isTyping } = payload as TypingIndicator;
        if (typingUserId === userId) return;

        if (isTyping) {
          setTypingUsers((prev) =>
            prev.includes(typingName) ? prev : [...prev, typingName]
          );
          // Auto-clear typing after 3 seconds
          const existing = typingTimeoutRef.current.get(typingUserId);
          if (existing) clearTimeout(existing);
          typingTimeoutRef.current.set(
            typingUserId,
            setTimeout(() => {
              setTypingUsers((prev) => prev.filter((n) => n !== typingName));
              typingTimeoutRef.current.delete(typingUserId);
            }, 3000)
          );
        } else {
          setTypingUsers((prev) => prev.filter((n) => n !== typingName));
          const existing = typingTimeoutRef.current.get(typingUserId);
          if (existing) {
            clearTimeout(existing);
            typingTimeoutRef.current.delete(typingUserId);
          }
        }
      })
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState();
        setOnlineCount(Object.keys(state).length);
      })
      .subscribe(async (subscribedStatus) => {
        setStatus(subscribedStatus);
        if (subscribedStatus === 'SUBSCRIBED') {
          await channel.track({ userId, userName, online_at: new Date().toISOString() });
        }
      });

    channelRef.current = channel;

    return () => {
      typingTimeoutRef.current.forEach((timeout) => clearTimeout(timeout));
      typingTimeoutRef.current.clear();
      if (channelRef.current) {
        supabase.removeChannel(channelRef.current);
        channelRef.current = null;
      }
    };
  }, [roomId, userId, userName]);

  const sendMessage = useCallback(
    (content: string) => {
      if (!channelRef.current) return;
      const msg: BroadcastMessage = {
        id: crypto.randomUUID(),
        content,
        userId,
        userName,
        timestamp: Date.now(),
      };
      // Optimistically add own message
      setMessages((prev) => [...prev, msg]);
      channelRef.current.send({ type: 'broadcast', event: 'message', payload: msg });
    },
    [userId, userName]
  );

  const setTyping = useCallback(
    (isTyping: boolean) => {
      channelRef.current?.send({
        type: 'broadcast',
        event: 'typing',
        payload: { userId, userName, isTyping },
      });
    },
    [userId, userName]
  );

  return { messages, typingUsers, onlineCount, sendMessage, setTyping, status };
}
```

**Usage:**

```tsx
function ChatRoom({ roomId }: { roomId: string }) {
  const { messages, typingUsers, onlineCount, sendMessage, setTyping, status } = useBroadcast({
    roomId,
    userId: currentUser.id,
    userName: currentUser.name,
  });
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput('');
    setTyping(false);
  };

  return (
    <div>
      <p>{onlineCount} online | Status: {status}</p>
      <div>
        {messages.map((msg) => (
          <div key={msg.id}>
            <strong>{msg.userName}:</strong> {msg.content}
          </div>
        ))}
      </div>
      {typingUsers.length > 0 && (
        <p>{typingUsers.join(', ')} typing...</p>
      )}
      <input
        value={input}
        onChange={(e) => { setInput(e.target.value); setTyping(true); }}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

---

### 3. Presence Tracking (React Hook) - `usePresence`

```typescript
import { useEffect, useState, useCallback, useRef } from 'react';
import { RealtimeChannel } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface PresenceUser {
  userId: string;
  userName: string;
  avatarUrl?: string;
  status: 'online' | 'away' | 'busy';
  cursorPosition?: { x: number; y: number };
  lastSeen: string;
}

interface UsePresenceOptions {
  channelName: string;
  user: {
    userId: string;
    userName: string;
    avatarUrl?: string;
  };
  initialStatus?: 'online' | 'away' | 'busy';
  enabled?: boolean;
}

interface UsePresenceResult {
  onlineUsers: PresenceUser[];
  updateStatus: (status: 'online' | 'away' | 'busy') => void;
  updateCursor: (position: { x: number; y: number }) => void;
  isConnected: boolean;
}

/**
 * Presence tracking hook.
 * Tracks who is online in a channel with custom state (status, cursor, etc.).
 */
export function usePresence({
  channelName,
  user,
  initialStatus = 'online',
  enabled = true,
}: UsePresenceOptions): UsePresenceResult {
  const [onlineUsers, setOnlineUsers] = useState<PresenceUser[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const channelRef = useRef<RealtimeChannel | null>(null);
  const currentStateRef = useRef<Partial<PresenceUser>>({
    status: initialStatus,
  });

  // Throttle cursor updates to avoid flooding the channel
  const lastCursorUpdate = useRef(0);
  const CURSOR_THROTTLE_MS = 50;

  useEffect(() => {
    if (!enabled) return;

    const channel = supabase.channel(channelName);

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState<PresenceUser>();
        const users: PresenceUser[] = [];
        for (const presences of Object.values(state)) {
          // Each key can have multiple presences; take the latest
          if (presences.length > 0) {
            users.push(presences[0] as unknown as PresenceUser);
          }
        }
        setOnlineUsers(users);
      })
      .on('presence', { event: 'join' }, ({ newPresences }) => {
        // Optional: handle join animations or notifications
      })
      .on('presence', { event: 'leave' }, ({ leftPresences }) => {
        // Optional: handle leave animations or notifications
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          setIsConnected(true);
          await channel.track({
            userId: user.userId,
            userName: user.userName,
            avatarUrl: user.avatarUrl,
            status: initialStatus,
            lastSeen: new Date().toISOString(),
          });
        } else {
          setIsConnected(false);
        }
      });

    channelRef.current = channel;

    return () => {
      if (channelRef.current) {
        channelRef.current.untrack();
        supabase.removeChannel(channelRef.current);
        channelRef.current = null;
      }
      setIsConnected(false);
    };
  }, [channelName, user.userId, user.userName, user.avatarUrl, initialStatus, enabled]);

  const updateStatus = useCallback(
    (status: 'online' | 'away' | 'busy') => {
      currentStateRef.current.status = status;
      channelRef.current?.track({
        userId: user.userId,
        userName: user.userName,
        avatarUrl: user.avatarUrl,
        status,
        lastSeen: new Date().toISOString(),
        ...currentStateRef.current,
      });
    },
    [user]
  );

  const updateCursor = useCallback(
    (position: { x: number; y: number }) => {
      const now = Date.now();
      if (now - lastCursorUpdate.current < CURSOR_THROTTLE_MS) return;
      lastCursorUpdate.current = now;

      currentStateRef.current.cursorPosition = position;
      channelRef.current?.track({
        userId: user.userId,
        userName: user.userName,
        avatarUrl: user.avatarUrl,
        cursorPosition: position,
        lastSeen: new Date().toISOString(),
        ...currentStateRef.current,
      });
    },
    [user]
  );

  return { onlineUsers, updateStatus, updateCursor, isConnected };
}
```

**Usage:**

```tsx
function CollaborativeEditor({ docId }: { docId: string }) {
  const { onlineUsers, updateStatus, updateCursor, isConnected } = usePresence({
    channelName: `doc:${docId}`,
    user: { userId: currentUser.id, userName: currentUser.name, avatarUrl: currentUser.avatar },
  });

  return (
    <div
      onMouseMove={(e) => updateCursor({ x: e.clientX, y: e.clientY })}
    >
      <div>
        {onlineUsers.map((u) => (
          <span key={u.userId} title={u.status}>
            <img src={u.avatarUrl} alt={u.userName} width={24} height={24} />
          </span>
        ))}
        <span>{onlineUsers.length} online</span>
      </div>
      {/* Render remote cursors */}
      {onlineUsers
        .filter((u) => u.userId !== currentUser.id && u.cursorPosition)
        .map((u) => (
          <div
            key={u.userId}
            style={{
              position: 'fixed',
              left: u.cursorPosition!.x,
              top: u.cursorPosition!.y,
              pointerEvents: 'none',
            }}
          >
            {u.userName}
          </div>
        ))}
    </div>
  );
}
```

---

### 4. Angular Realtime Service

```typescript
import { Injectable, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Observable, Subject, BehaviorSubject, finalize } from 'rxjs';
import {
  createClient,
  SupabaseClient,
  RealtimeChannel,
  RealtimePostgresChangesPayload,
} from '@supabase/supabase-js';
import { environment } from '@/environments/environment';

interface PresenceUser {
  userId: string;
  userName: string;
  status: string;
}

/**
 * Angular Realtime service.
 * Manages Supabase channels with automatic cleanup via DestroyRef.
 * Realtime respects RLS policies - users only receive authorized changes.
 */
@Injectable({ providedIn: 'root' })
export class RealtimeService {
  private supabase: SupabaseClient;
  private channels = new Map<string, RealtimeChannel>();
  private destroyRef = inject(DestroyRef);

  // Presence as a signal for reactive templates
  readonly onlineUsers = signal<PresenceUser[]>([]);

  constructor() {
    this.supabase = createClient(environment.supabaseUrl, environment.supabaseAnonKey);

    // Cleanup all channels when service is destroyed
    this.destroyRef.onDestroy(() => this.removeAllChannels());
  }

  /**
   * Subscribe to database changes on a table, returned as an Observable.
   */
  subscribeToTable<T extends Record<string, unknown>>(
    table: string,
    options?: { event?: string; filter?: string; schema?: string }
  ): Observable<RealtimePostgresChangesPayload<T>> {
    const subject = new Subject<RealtimePostgresChangesPayload<T>>();
    const channelName = `db-${table}-${options?.filter ?? 'all'}-${Date.now()}`;

    const channelConfig: Record<string, unknown> = {
      event: options?.event ?? '*',
      schema: options?.schema ?? 'public',
      table,
    };
    if (options?.filter) channelConfig.filter = options.filter;

    const channel = this.supabase
      .channel(channelName)
      .on('postgres_changes' as any, channelConfig, (payload: RealtimePostgresChangesPayload<T>) => {
        subject.next(payload);
      })
      .subscribe((status) => {
        if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
          subject.error(new Error(`Channel ${channelName}: ${status}`));
        }
      });

    this.channels.set(channelName, channel);

    return subject.asObservable().pipe(
      takeUntilDestroyed(this.destroyRef),
      finalize(() => this.removeChannel(channelName))
    );
  }

  /**
   * Create a broadcast channel for ephemeral messaging.
   */
  createBroadcastChannel(roomId: string): {
    send: (event: string, payload: unknown) => void;
    on: (event: string) => Observable<unknown>;
    destroy: () => void;
  } {
    const channelName = `broadcast-${roomId}`;
    const channel = this.supabase.channel(channelName, {
      config: { broadcast: { self: false } },
    });

    const subjects = new Map<string, Subject<unknown>>();

    const on = (event: string): Observable<unknown> => {
      if (!subjects.has(event)) {
        const subject = new Subject<unknown>();
        subjects.set(event, subject);
        channel.on('broadcast', { event }, ({ payload }) => subject.next(payload));
      }
      return subjects.get(event)!.asObservable().pipe(takeUntilDestroyed(this.destroyRef));
    };

    channel.subscribe();
    this.channels.set(channelName, channel);

    return {
      send: (event: string, payload: unknown) => {
        channel.send({ type: 'broadcast', event, payload });
      },
      on,
      destroy: () => {
        subjects.forEach((s) => s.complete());
        subjects.clear();
        this.removeChannel(channelName);
      },
    };
  }

  /**
   * Track presence in a channel. Updates the onlineUsers signal.
   */
  trackPresence(
    channelName: string,
    user: PresenceUser
  ): {
    updateState: (state: Partial<PresenceUser>) => void;
    leave: () => void;
  } {
    const channel = this.supabase.channel(`presence-${channelName}`);

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState<PresenceUser>();
        const users: PresenceUser[] = [];
        for (const presences of Object.values(state)) {
          if (presences.length > 0) {
            users.push(presences[0] as unknown as PresenceUser);
          }
        }
        this.onlineUsers.set(users);
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track(user);
        }
      });

    this.channels.set(`presence-${channelName}`, channel);

    return {
      updateState: (state: Partial<PresenceUser>) => {
        channel.track({ ...user, ...state });
      },
      leave: () => {
        channel.untrack();
        this.removeChannel(`presence-${channelName}`);
      },
    };
  }

  private removeChannel(name: string): void {
    const channel = this.channels.get(name);
    if (channel) {
      this.supabase.removeChannel(channel);
      this.channels.delete(name);
    }
  }

  private removeAllChannels(): void {
    this.channels.forEach((channel) => this.supabase.removeChannel(channel));
    this.channels.clear();
  }
}
```

**Usage in a component:**

```typescript
@Component({ ... })
export class ChatComponent implements OnInit {
  private realtime = inject(RealtimeService);

  ngOnInit() {
    // Database changes
    this.realtime
      .subscribeToTable('messages', { event: 'INSERT', filter: 'room_id=eq.123' })
      .subscribe((payload) => {
        this.messages.push(payload.new);
      });

    // Broadcast
    const chat = this.realtime.createBroadcastChannel('room-123');
    chat.on('message').subscribe((msg) => this.messages.push(msg));
    chat.send('message', { text: 'Hello!' });

    // Presence
    this.realtime.trackPresence('room-123', {
      userId: this.user.id,
      userName: this.user.name,
      status: 'online',
    });
  }

  // Access online users in template via: realtime.onlineUsers()
}
```

---

### 5. Full Chat Example - Complete Mini Chat Component

This example combines broadcast for messages, presence for online users, and database changes for message persistence with optimistic UI updates.

```typescript
// src/hooks/useChat.ts
import { useEffect, useState, useCallback, useRef } from 'react';
import { RealtimeChannel } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface ChatMessage {
  id: string;
  content: string;
  user_id: string;
  user_name: string;
  room_id: string;
  created_at: string;
  pending?: boolean; // optimistic flag
}

interface ChatUser {
  userId: string;
  userName: string;
  avatarUrl?: string;
  isTyping: boolean;
}

interface UseChatOptions {
  roomId: string;
  userId: string;
  userName: string;
  avatarUrl?: string;
}

interface UseChatResult {
  messages: ChatMessage[];
  onlineUsers: ChatUser[];
  typingUsers: string[];
  sendMessage: (content: string) => Promise<void>;
  setTyping: (isTyping: boolean) => void;
  isConnected: boolean;
  error: Error | null;
}

/**
 * Complete chat hook combining:
 * - Broadcast for real-time message delivery
 * - Presence for online user tracking
 * - Database changes for persistence and consistency
 * - Optimistic UI updates
 *
 * RLS note: Ensure your messages table has appropriate RLS policies.
 * Users will only see messages they are authorized to access.
 */
export function useChat({
  roomId,
  userId,
  userName,
  avatarUrl,
}: UseChatOptions): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<ChatUser[]>([]);
  const [typingUsers, setTypingUsers] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const channelRef = useRef<RealtimeChannel | null>(null);
  const typingTimeouts = useRef<Map<string, NodeJS.Timeout>>(new Map());

  // Load initial messages from database
  useEffect(() => {
    const load = async () => {
      const { data, error: fetchError } = await supabase
        .from('messages')
        .select('*')
        .eq('room_id', roomId)
        .order('created_at', { ascending: true })
        .limit(100);

      if (fetchError) {
        setError(new Error(fetchError.message));
        return;
      }
      setMessages(data ?? []);
    };
    load();
  }, [roomId]);

  // Set up realtime channel with all three patterns
  useEffect(() => {
    const channel = supabase.channel(`chat:${roomId}`, {
      config: { broadcast: { self: false } },
    });

    channel
      // 1. Database changes - source of truth for persistence
      .on(
        'postgres_changes' as any,
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        (payload: any) => {
          const newMsg = payload.new as ChatMessage;
          // Replace optimistic message or add if from another user
          setMessages((prev) => {
            const optimisticIdx = prev.findIndex(
              (m) => m.pending && m.content === newMsg.content && m.user_id === newMsg.user_id
            );
            if (optimisticIdx >= 0) {
              const updated = [...prev];
              updated[optimisticIdx] = { ...newMsg, pending: false };
              return updated;
            }
            // Avoid duplicates from broadcast
            if (prev.some((m) => m.id === newMsg.id)) return prev;
            return [...prev, newMsg];
          });
        }
      )
      // 2. Broadcast - fast delivery before DB write completes
      .on('broadcast', { event: 'new-message' }, ({ payload }) => {
        const msg = payload as ChatMessage;
        if (msg.user_id === userId) return; // skip own messages
        setMessages((prev) => {
          if (prev.some((m) => m.id === msg.id)) return prev;
          return [...prev, { ...msg, pending: true }];
        });
      })
      // 3. Broadcast - typing indicators
      .on('broadcast', { event: 'typing' }, ({ payload }) => {
        const { userName: name, isTyping } = payload as { userName: string; isTyping: boolean };
        if (isTyping) {
          setTypingUsers((prev) => (prev.includes(name) ? prev : [...prev, name]));
          const existing = typingTimeouts.current.get(name);
          if (existing) clearTimeout(existing);
          typingTimeouts.current.set(
            name,
            setTimeout(() => {
              setTypingUsers((prev) => prev.filter((n) => n !== name));
              typingTimeouts.current.delete(name);
            }, 3000)
          );
        } else {
          setTypingUsers((prev) => prev.filter((n) => n !== name));
        }
      })
      // 4. Presence - track online users
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState<ChatUser>();
        const users: ChatUser[] = [];
        for (const presences of Object.values(state)) {
          if (presences.length > 0) {
            users.push(presences[0] as unknown as ChatUser);
          }
        }
        setOnlineUsers(users);
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          setIsConnected(true);
          setError(null);
          await channel.track({
            userId,
            userName,
            avatarUrl,
            isTyping: false,
          });
        } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
          setIsConnected(false);
          setError(new Error(`Connection ${status}`));
        }
      });

    channelRef.current = channel;

    return () => {
      typingTimeouts.current.forEach((t) => clearTimeout(t));
      typingTimeouts.current.clear();
      if (channelRef.current) {
        channelRef.current.untrack();
        supabase.removeChannel(channelRef.current);
        channelRef.current = null;
      }
    };
  }, [roomId, userId, userName, avatarUrl]);

  const sendMessage = useCallback(
    async (content: string) => {
      const tempId = crypto.randomUUID();
      const optimistic: ChatMessage = {
        id: tempId,
        content,
        user_id: userId,
        user_name: userName,
        room_id: roomId,
        created_at: new Date().toISOString(),
        pending: true,
      };

      // Optimistic update
      setMessages((prev) => [...prev, optimistic]);

      // Broadcast for instant delivery to others
      channelRef.current?.send({
        type: 'broadcast',
        event: 'new-message',
        payload: optimistic,
      });

      // Persist to database (this triggers postgres_changes for confirmation)
      const { error: insertError } = await supabase.from('messages').insert({
        content,
        user_id: userId,
        user_name: userName,
        room_id: roomId,
      });

      if (insertError) {
        // Remove optimistic message on failure
        setMessages((prev) => prev.filter((m) => m.id !== tempId));
        setError(new Error(insertError.message));
      }
    },
    [roomId, userId, userName]
  );

  const setTyping = useCallback(
    (isTyping: boolean) => {
      channelRef.current?.send({
        type: 'broadcast',
        event: 'typing',
        payload: { userName, isTyping },
      });
    },
    [userName]
  );

  return { messages, onlineUsers, typingUsers, sendMessage, setTyping, isConnected, error };
}
```

**Full Chat Component:**

```tsx
// src/components/Chat.tsx
import { useState, useRef, useEffect } from 'react';
import { useChat } from '@/hooks/useChat';

interface ChatProps {
  roomId: string;
  userId: string;
  userName: string;
  avatarUrl?: string;
}

export function Chat({ roomId, userId, userName, avatarUrl }: ChatProps) {
  const {
    messages,
    onlineUsers,
    typingUsers,
    sendMessage,
    setTyping,
    isConnected,
    error,
  } = useChat({ roomId, userId, userName, avatarUrl });

  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingRef = useRef(false);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    await sendMessage(input.trim());
    setInput('');
    setTyping(false);
    typingRef.current = false;
  };

  const handleInputChange = (value: string) => {
    setInput(value);
    if (value && !typingRef.current) {
      setTyping(true);
      typingRef.current = true;
    } else if (!value && typingRef.current) {
      setTyping(false);
      typingRef.current = false;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ padding: 12, borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <span style={{ color: isConnected ? 'green' : 'red' }}>●</span>
          {isConnected ? ' Connected' : ' Disconnected'}
          {error && <span style={{ color: 'red', marginLeft: 8 }}>{error.message}</span>}
        </div>
        <div>
          {onlineUsers.map((u) => (
            <span key={u.userId} title={u.userName} style={{ marginLeft: 4 }}>
              {u.avatarUrl ? (
                <img src={u.avatarUrl} alt={u.userName} width={24} height={24} style={{ borderRadius: '50%' }} />
              ) : (
                <span style={{ display: 'inline-block', width: 24, height: 24, borderRadius: '50%', backgroundColor: '#ccc', textAlign: 'center', lineHeight: '24px', fontSize: 12 }}>
                  {u.userName[0]}
                </span>
              )}
            </span>
          ))}
          <span style={{ marginLeft: 8, fontSize: 12, color: '#666' }}>
            {onlineUsers.length} online
          </span>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              marginBottom: 8,
              opacity: msg.pending ? 0.6 : 1,
              textAlign: msg.user_id === userId ? 'right' : 'left',
            }}
          >
            <div style={{ fontSize: 12, color: '#666' }}>{msg.user_name}</div>
            <div
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: 12,
                backgroundColor: msg.user_id === userId ? '#0070f3' : '#f0f0f0',
                color: msg.user_id === userId ? '#fff' : '#000',
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing indicator */}
      {typingUsers.length > 0 && (
        <div style={{ padding: '4px 12px', fontSize: 12, color: '#666', fontStyle: 'italic' }}>
          {typingUsers.join(', ')} {typingUsers.length === 1 ? 'is' : 'are'} typing...
        </div>
      )}

      {/* Input */}
      <div style={{ padding: 12, borderTop: '1px solid #eee', display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={(e) => handleInputChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
          placeholder="Type a message..."
          style={{ flex: 1, padding: 8, borderRadius: 8, border: '1px solid #ddd' }}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || !isConnected}
          style={{ padding: '8px 16px', borderRadius: 8, backgroundColor: '#0070f3', color: '#fff', border: 'none', cursor: 'pointer' }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
```

## Important Notes

- **RLS enforcement**: Supabase Realtime respects Row Level Security. Ensure your tables have appropriate RLS policies, or users will not receive change events.
- **Enable Realtime on tables**: You must enable Realtime for each table in the Supabase dashboard (Database > Replication) or via SQL: `alter publication supabase_realtime add table your_table;`
- **Channel limits**: Supabase has limits on concurrent channels per connection. Reuse channels where possible rather than creating one per subscription.
- **Broadcast vs. Database changes**: Use broadcast for ephemeral data (typing indicators, cursor positions). Use database changes for persistent data. Combine both for the best UX as shown in the full chat example.
- **Reconnection**: The Supabase client handles reconnection automatically. Monitor the subscription status callback to update UI accordingly.
