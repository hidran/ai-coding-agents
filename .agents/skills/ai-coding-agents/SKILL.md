# AI Coding Agents

This skill provides access to 65+ specialized AI agents for development workflows, from architecture to marketing.

## Installation

```bash
# Clone the repository
git clone https://github.com/hidran/ai-coding-agents.git ~/.agents/skills/ai-coding-agents

# Or use the install script
curl -fsSL https://raw.githubusercontent.com/hidran/ai-coding-agents/main/scripts/install.sh | bash
```

## Included Agents

### Architecture
- `system-designer` - Distributed systems architecture
- `api-designer` - REST/GraphQL API design
- `database-planner` - Schema design and optimization
- `tech-stack-advisor` - Technology selection

### Code Quality
- `code-reviewer` - Code quality analysis
- `test-strategist` - Testing architecture
- `security-auditor` - Security review
- `performance-optimizer` - Performance tuning

### Workflow (New)
- `brainstorming` - Design refinement through questioning
- `writing-plans` - Task breakdown and planning
- `subagent-driven-development` - Parallel agent execution
- `test-driven-development` - TDD enforcement
- `systematic-debugging` - 4-phase debugging
- `using-git-worktrees` - Isolated development
- `requesting-code-review` - Quality gates
- `executing-plans` - Batch implementation

### Framework Generators
- `laravel-feature` - Laravel scaffolding
- `react-component` - React components
- `nextjs-page` - Next.js pages
- `nestjs-resource` - NestJS resources

### And 40+ more...

## Usage

Agents auto-trigger based on context or invoke explicitly:

```
@system-designer Design a scalable notification system
@code-reviewer Check this authentication logic
/brainstorming I want to build a marketplace
```

## For Kimi CLI

These agents work with Kimi CLI's subagent system. Invoke via:
- Direct mention: `@agent-name`
- Slash command: `/agent-name`
- Natural language triggers

## Repository

https://github.com/hidran/ai-coding-agents
