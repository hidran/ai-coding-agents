---
name: adr
description: Generates Architecture Decision Records (ADRs) with context, decision, consequences, and maintains an index. Essential for documenting technical decisions.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Architecture Decision Record Generator

This skill creates and manages Architecture Decision Records (ADRs) following the Michael Nygard format.

## Usage
Run `/adr <title>` to create a new ADR
Run `/adr list` to show all ADRs
Run `/adr supersede <number> <new-title>` to supersede an existing ADR

## Structure
Creates/maintains:
- `docs/adr/NNNN-<title-slug>.md`: Individual ADR files (0001, 0002, ...)
- `docs/adr/README.md`: Index of all ADRs with status and links

## Process
1. **Check existing ADRs**: Read `docs/adr/` to determine next number
2. **Gather context**: Ask about the problem, constraints, alternatives considered
3. **Generate ADR**: Create the record with all sections
4. **Update index**: Add entry to `docs/adr/README.md`

## ADR Template

Each ADR follows this structure:

```markdown
# NNNN. Title of Decision

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded by [NNNN](NNNN-title.md)
**Deciders**: [list of people involved]
**Tags**: [architecture, security, performance, etc.]

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive
- What becomes easier or possible as a result of this change?

### Negative
- What becomes harder or impossible as a result of this change?

### Neutral
- What other changes might need to happen as a result?

## Alternatives Considered

### Alternative 1: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

### Alternative 2: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## References
- Links to relevant resources, RFCs, documentation
```

## Standards
- **Immutable records**: Once accepted, ADRs are never modified (only superseded)
- **Sequential numbering**: Always use the next available number
- **Clear context**: The "why" is more important than the "what"
- **Alternatives**: Always document what was considered and why it was rejected
- **Consequences**: Be honest about trade-offs, both positive and negative

## Examples

### Example ADR

```markdown
# 0004. Use PostgreSQL Instead of MySQL for the Reporting Service

**Date**: 2026-02-15
**Status**: Accepted
**Deciders**: Backend team, Data engineering lead, CTO
**Tags**: database, architecture, reporting

## Context

The team is building a new reporting service that must support complex analytical queries over semi-structured data. Our existing infrastructure runs MySQL 5.7 across all services, and the operations team is experienced with MySQL administration, backups, and monitoring.

However, the reporting service has specific requirements that push beyond what MySQL handles well:

- Reports involve filtering and aggregating data stored as JSON blobs (event metadata, user preferences, audit trails). The current approach of extracting JSON fields in application code is slow and error-prone.
- Full-text search across report descriptions, comments, and audit logs is needed. The team currently uses a separate Elasticsearch instance for search, adding operational complexity.
- Several reports require window functions, CTEs, and recursive queries that are either unavailable or poorly optimized in MySQL 5.7.
- The data model is expected to evolve frequently as new report types are added, making schema flexibility important.

## Decision

Use PostgreSQL 15 for the new reporting service. All other existing services will continue to use MySQL. The reporting service will consume data via event streams and maintain its own read-optimized data store.

## Consequences

### Positive
- Native JSONB support enables efficient indexing and querying of semi-structured data without application-level parsing
- Built-in full-text search with `tsvector`/`tsquery` eliminates the need for a separate Elasticsearch instance for this service
- Mature support for window functions, CTEs, lateral joins, and recursive queries simplifies complex report generation
- Rich extension ecosystem (pg_trig, PostGIS, pg_stat_statements) provides room for future growth

### Negative
- Operations team must learn PostgreSQL administration, monitoring, and backup procedures
- Two database technologies in production increases infrastructure complexity
- Existing MySQL connection pooling, migration tooling, and monitoring dashboards will not apply to this service
- Developer onboarding takes longer due to differences in SQL dialect and tooling

### Neutral
- CI/CD pipeline needs a PostgreSQL test instance alongside the existing MySQL one
- Database migration tooling (currently Flyway configured for MySQL) must be configured separately for PostgreSQL
- Connection pooling may require PgBouncer, which is a new component to manage

## Alternatives Considered

### Alternative 1: MySQL 8 with JSON Functions
- **Pros**: No new technology to learn; consistent with existing infrastructure; MySQL 8 adds improved JSON support and CTEs
- **Cons**: JSON indexing is less mature than PostgreSQL JSONB; no native full-text search comparable to PostgreSQL; would still require Elasticsearch for search; upgrade from 5.7 to 8 carries its own migration risk
- **Why rejected**: Does not fully address the JSON querying and full-text search requirements without additional infrastructure

### Alternative 2: MongoDB
- **Pros**: Excellent for semi-structured data; flexible schema; built-in aggregation pipeline
- **Cons**: Weak support for complex joins and relational queries needed for multi-entity reports; another new technology with a steeper operational learning curve; eventual consistency model complicates reporting accuracy
- **Why rejected**: Reporting queries frequently join across multiple entities, which is not a strength of document databases

### Alternative 3: Elasticsearch as Primary Store
- **Pros**: Excellent full-text search; good JSON handling; scales horizontally
- **Cons**: Not designed as a primary data store; no transactional guarantees; complex cluster management; query language is limited for relational operations
- **Why rejected**: Elasticsearch excels at search but is not suitable as the system of record for a reporting service that requires transactional consistency

## References
- [PostgreSQL JSONB Documentation](https://www.postgresql.org/docs/15/datatype-json.html)
- [PostgreSQL Full Text Search](https://www.postgresql.org/docs/15/textsearch.html)
- [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Internal RFC: Reporting Service Requirements (Confluence, 2026-01-20)
```

### Example Index (docs/adr/README.md)

```markdown
# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) for this project.

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [0001](0001-use-typescript-for-backend.md) | Use TypeScript for Backend Services | Accepted | 2025-09-10 |
| [0002](0002-adopt-event-driven-architecture.md) | Adopt Event-Driven Architecture | Accepted | 2025-10-22 |
| [0003](0003-use-redis-for-session-storage.md) | Use Redis for Session Storage | Superseded by [0005](0005-migrate-sessions-to-database.md) | 2025-11-05 |
| [0004](0004-use-postgresql-for-reporting-service.md) | Use PostgreSQL for the Reporting Service | Accepted | 2026-02-15 |

## About ADRs

An Architecture Decision Record captures an important architectural decision made along with its context and consequences. ADRs are immutable once accepted -- if a decision changes, a new ADR supersedes the old one.

For more information, see [Michael Nygard's article on ADRs](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
```
