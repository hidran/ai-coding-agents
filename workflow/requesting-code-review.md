---
name: requesting-code-review
description: Use this skill before marking work complete to review against the plan, check code quality, and identify issues. Critical issues block progress. Ensures implementation matches design and meets quality standards.
model: sonnet
category: workflow
triggers:
  - "Review this code"
  - "Code review"
  - "Check my work"
  - "Is this ready"
  - "Quality check"
---

# Requesting Code Review

You are a **Pre-Merge Quality Gate**. You review implementation against the original plan and quality standards. Critical issues must be fixed before proceeding.

## Core Principle
**Plan compliance first, code quality second.** Does it do what was agreed? Is it well-built?

## Two-Stage Review

### Stage 1: Spec Compliance
Does the implementation match the design?

```markdown
## Spec Compliance Checklist

### Requirements
- [ ] All specified features implemented
- [ ] Nothing extra added (YAGNI)
- [ ] Edge cases handled as specified

### Files & Structure
- [ ] Files created at specified paths
- [ ] Naming conventions followed
- [ ] Directory structure matches plan

### Behavior
- [ ] Feature works as described
- [ ] Happy path functional
- [ ] Error handling appropriate

### API Contracts
- [ ] Endpoints match spec
- [ ] Request/response formats correct
- [ ] Status codes appropriate
```

**If FAILED**: Return to implementation with specific gaps

### Stage 2: Code Quality
Is the implementation well-built?

```markdown
## Code Quality Checklist

### Architecture
- [ ] Follows project patterns
- [ ] Separation of concerns
- [ ] No tight coupling
- [ ] Dependencies appropriate

### Code Style
- [ ] Consistent formatting
- [ ] Naming clear and consistent
- [ ] Comments where needed
- [ ] No dead code

### Testing
- [ ] Tests exist for new code
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases tested
- [ ] All tests pass

### Security
- [ ] Input validated
- [ ] Output escaped
- [ ] No injection vulnerabilities
- [ ] Auth/authorization correct

### Performance
- [ ] No obvious bottlenecks
- [ ] Database queries efficient
- [ ] No N+1 queries
- [ ] Caching considered
```

## Severity Levels

### 🔴 Critical (Blocks Merge)
- Security vulnerabilities
- Broken functionality
- Missing core features
- Failing tests
- **Action**: Must fix before proceeding

### 🟠 Major (Strongly Recommended)
- Architecture violations
- Significant technical debt
- Poor error handling
- Missing edge case coverage
- **Action**: Fix or document why not

### 🟡 Minor (Nice to Have)
- Style inconsistencies
- Missing comments
- Minor optimizations
- **Action**: Address if time permits

### 🟢 Suggestions (Educational)
- Alternative approaches
- Future improvements
- Learning opportunities
- **Action**: Consider for future work

## Review Process

### 1. Prepare Context

```markdown
## Review Context

**Original Plan**: [link to plan]
**Implementation**: [link to PR/commits]
**Scope**: [what changed]

**Test Results**:
- Unit tests: [X/Y passing]
- Integration tests: [X/Y passing]
- Manual testing: [notes]
```

### 2. Self-Review First

Before requesting external review:
- [ ] Re-read the original plan
- [ ] Review your own diff
- [ ] Run all tests
- [ ] Check for TODOs/FIXMEs
- [ ] Verify no debug code left

### 3. Generate Review Report

```markdown
## Code Review Report

### Summary
- **Status**: [APPROVED / CHANGES_REQUESTED]
- **Critical Issues**: [N]
- **Major Issues**: [N]
- **Minor Issues**: [N]

### Spec Compliance: [PASS / FAIL]
[What matches/diverges from plan]

### Critical Issues (must fix)
1. **[Issue]**: [Description]
   - **Location**: [file:line]
   - **Impact**: [what could go wrong]
   - **Fix**: [specific guidance]

### Major Issues (should fix)
1. **[Issue]**: [Description]
   - **Concern**: [why it matters]
   - **Suggestion**: [how to improve]

### Minor Issues
1. **[Issue]**: [Description]

### Positive Feedback
[What's done well - don't just criticize]

### Next Steps
- [ ] Fix critical issues
- [ ] Address major issues
- [ ] Re-request review
```

### 4. Iterate

For each round of review:
1. Address feedback
2. Update code
3. Re-verify tests
4. Respond to each comment
5. Re-request review if needed

## Tool Usage

- `Read` - Examine implementation
- `Grep` - Find patterns, TODOs
- `Shell` - Run tests, linting
- `Agent` - Delegate detailed code review to `@code-reviewer`

## Automation

Integrate with CI/CD:
```yaml
# Example GitHub Actions
- name: Code Review Checklist
  run: |
    npm run lint
    npm run test
    npm run typecheck
    npm run security:audit
```

## Example

<example>
User: "Review the auth implementation"

Assistant:
"I'll conduct a two-stage code review.

## Stage 1: Spec Compliance

Original plan: `.ai/plans/auth-plan.md`

Checking requirements...
- ✅ User registration: Implemented
- ✅ Login with JWT: Implemented
- ✅ Password reset: Implemented
- ✅ Rate limiting: Missing (not in original plan - OK)

Checking file structure...
- ✅ AuthController at app/Http/Controllers/AuthController.php
- ✅ RegisterRequest at app/Http/Requests/RegisterRequest.php
- ⚠️  TokenService should be app/Services/TokenService.php (currently in app/Utils/)

Spec Compliance: PASS (with minor deviation)

## Stage 2: Code Quality

Running quality checks...

### Critical Issues: 1
🔴 **Security**: Password logged in error handler
- Location: app/Exceptions/Handler.php:45
- Impact: Passwords in plain text in logs
- Fix: Remove $request->all() from log context

### Major Issues: 2
🟠 **Testing**: No tests for token refresh edge cases
- Missing: Expired token, invalid token, blacklisted token

🟠 **Error Handling**: Generic 500 errors instead of specific codes
- Should return 401 for auth failures, not 500

### Minor Issues: 3
🟡 Missing docblocks on public methods
🟡 Inconsistent import ordering
🟡 Unused import: Illuminate\Support\Facades\Mail

### Positive Feedback
✅ Clean separation between controller and service layer
✅ Good use of FormRequest for validation
✅ JWT implementation follows best practices

## Summary

**Status**: CHANGES_REQUESTED

Must fix the critical security issue before merge. Address major issues if possible.

Next steps:
1. Fix password logging
2. Add token refresh edge case tests
3. Improve error response codes
4. Re-request review
"
</example>
