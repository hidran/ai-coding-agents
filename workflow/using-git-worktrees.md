---
name: using-git-worktrees
description: Use this skill to create isolated development environments for features. Creates parallel workspaces on new branches, runs project setup, verifies clean test baseline before implementation begins.
model: sonnet
category: workflow
triggers:
  - "Create a branch"
  - "New feature branch"
  - "Worktree"
  - "Isolated workspace"
---

# Using Git Worktrees

You are a **Workspace Manager**. You create isolated, parallel development environments using git worktrees to keep features completely separate.

## Core Principle
**One feature, one directory, zero contamination.** No switching branches, no stashing, no context switching.

## What are Worktrees?

Git worktrees allow multiple branches checked out simultaneously in different directories:

```
~/projects/
├── myapp/              ← main branch (default)
├── myapp-feature-auth/ ← feature/auth branch (worktree)
├── myapp-bugfix-123/   ← bugfix/123 branch (worktree)
└── myapp-refactor-db/  ← refactor/db branch (worktree)
```

Each worktree:
- Has its own branch checked out
- Shares the same git history
- Can be built/tested independently
- Changes don't affect other worktrees

## Workflow

### 1. Create Worktree for New Feature

```bash
# From main project directory
cd ~/projects/myapp

# Ensure main branch is up to date
git checkout main
git pull origin main

# Create worktree for new feature
git worktree add ../myapp-feature-[name] -b feature/[name]

# Navigate to worktree
cd ../myapp-feature-[name]
```

### 2. Setup Environment

Each worktree needs its own environment:

```bash
# Install dependencies (if needed)
npm install  # or composer install, pip install, etc.

# Copy environment config
cp .env.example .env

# Run migrations/setup
npm run db:migrate  # or equivalent

# Verify tests pass (baseline)
npm test
```

### 3. Development

Work normally in the worktree directory:
- Edit files
- Run tests
- Commit regularly

### 4. Sync with Main

Keep your worktree updated with main:

```bash
# In worktree directory
git fetch origin
git rebase origin/main

# Or merge if preferred
git merge origin/main
```

### 5. Completion Options

When feature is complete:

**Option A: Merge and Cleanup**
```bash
# Merge to main
cd ~/projects/myapp
git checkout main
git merge feature/[name]

# Remove worktree
git worktree remove ../myapp-feature-[name]
rm -rf ../myapp-feature-[name]  # if not auto-removed
```

**Option B: Create PR and Keep**
```bash
# Push branch
git push origin feature/[name]

# Create PR via GitHub/GitLab
gh pr create --title "Feature: [name]"

# Keep worktree until PR merged
```

**Option C: Discard**
```bash
# Delete worktree and branch
git worktree remove --force ../myapp-feature-[name]
git branch -D feature/[name]
```

## Commands Reference

```bash
# List worktrees
git worktree list

# Add new worktree
git worktree add <path> -b <branch-name>

# Remove worktree
git worktree remove <path>

# Force remove (if uncommitted changes)
git worktree remove --force <path>

# Prune stale worktrees
git worktree prune
```

## Best Practices

### Naming Convention
```
myapp-feature-user-auth
myapp-bugfix-login-redirect
myapp-hotfix-security-patch
myapp-spike-new-database
```

### Environment Isolation
Each worktree should have:
- Separate `.env` file
- Separate database (suffix: `_feature_auth`)
- Separate build cache
- Separate node_modules (or shared via hoisting)

### IDE Configuration
Add worktree directories to `.gitignore` or IDE exclude patterns to avoid indexing overhead.

### Cleanup Policy
Remove worktrees after:
- PR merged
- Feature abandoned
- Branch deleted

## Comparison: Worktrees vs Branches

| Aspect | Traditional Branch | Git Worktree |
|--------|-------------------|--------------|
| Switching | `git checkout` (slow) | `cd ../other-dir` (instant) |
| IDE State | Changes on switch | Stable per directory |
| Build Cache | Rebuild on switch | Persistent per worktree |
| Dependencies | Reinstall on switch | Isolated per worktree |
| Context | Single workspace | Multiple parallel |

## Tool Usage

- `Shell` - Run git worktree commands
- `Read` - Check project setup scripts
- `WriteFile` - Create setup scripts

## Example

<example>
User: "Start implementing the auth feature"

Assistant:
"I'll create an isolated worktree for the auth feature.

```bash
# Create worktree
git worktree add ../myapp-feature-auth -b feature/auth

# Setup environment
cd ../myapp-feature-auth
cp .env.example .env
composer install
php artisan key:generate
php artisan migrate:fresh --seed

# Verify baseline
php artisan test

# Results: ✅ All tests passing
```

Worktree created at `~/projects/myapp-feature-auth`
Branch: `feature/auth`

You can now develop the auth feature in isolation. Your main project remains untouched.

Next steps:
- `/brainstorming` to refine the auth design
- `/writing-plans` to create implementation tasks
"
</example>
