# AI Agents 🤖

<div align="center">
  <h2>🤖 AI Agents</h2>
  <p>Developed and maintained by <a href="https://github.com/hidran">hidran</a></p>
</div>

---

**Your new AI-powered development squad is here!** 🚀

Meet 80 specialized AI skills that supercharge your development workflow. From system architecture to marketing copy, these Claude Code agents are like having a whole team of experts at your fingertips - and they never need coffee breaks!

## 🚀 Quick Install

### Claude Code Plugin (Recommended)

```bash
# Install via Claude Code marketplace
/plugin marketplace add hidran/ai-coding-agents
/plugin install ai-coding-agents@hidran/ai-coding-agents

# Or directly
/plugin install https://github.com/hidran/ai-coding-agents
```

### Gemini CLI Extension

```bash
# Install as Gemini extension
gemini extensions install https://github.com/hidran/ai-coding-agents

# Update
gemini extensions update ai-coding-agents
```

### One-Liner Install (Any Platform)

```bash
# For Claude (default)
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"'

# For Gemini
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"' -- gemini

# For Codex
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"' -- codex

# For Kimi CLI
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"' -- kimi
```

## 🚀 Quick Start (Manual)


The installation process is now simpler and more reliable. You no longer need to manually copy individual files.

### 1. Clone the Repository
If you haven't already, clone the project to your local machine:
```bash
git clone https://github.com/hidran/ai-coding-agents.git
cd ai-coding-agents
```

### 2. Install Dependencies

Choose your preferred build system:

**Option A: Node.js (Recommended)**
```bash
npm install
```

**Option B: Python**
```bash
python3 -m pip install -r requirements.txt
```

### 3. Build & Install

The installer supports multiple AI platforms and skill selection options:

```bash
# Build and install all skills
./scripts/install.sh --all

# Build and install specific skills only
./scripts/install.sh --skills=api-designer,code-reviewer,ui-designer

# Interactive skill selection (with checkbox UI)
./scripts/install.sh

# For Gemini or Codex platforms
./scripts/install.sh --all --platform=gemini
```

Or use the build script directly:

```bash
# Using Node.js
npm run build:all           # Build all skills
npm run build:list          # List available skills
node scripts/build.js --skills=api-designer,code-reviewer

# Using Python
python3 scripts/build.py --all
python3 scripts/build.py --list
python3 scripts/build.py --skills=api-designer,code-reviewer
```

This will build and validate the skills, and copy them into the `./.claude/skills` directory (or equivalent for your platform).

### 3. Restart and Use
Restart your IDE or code editor where you use Claude Code. The new agents will now be available for use.

### Usage
Once installed, it's like having your own AI specialists on speed dial! 📞

- **🎯 Automatic Delegation**: Claude Code automatically calls in the right skill for your task.
- **🗣️ Explicit Invocation**: "Hey `code-reviewer`, check this function!" - just ask for any skill by name.
- **🧠 Context-Aware**: Your AI team collaborates seamlessly on complex multi-step projects.

📚 **New to Claude Code agents?** Check out the [official documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) to learn how agents work.

## 🤖 Your AI Dream Team

*Meet your new coding sidekicks - each one a specialist in their field:*

### 🏗️ Workflow (8 skills)
*Development process automation and methodology enforcement*
- **brainstorming** - Use this skill when starting a new feature, project, or when the user has a vague idea that needs refinement.
- **executing-plans** - Use this skill to execute implementation plans in batches with human checkpoints.
- **requesting-code-review** - Use this skill before marking work complete to review against the plan, check code quality, and identify issues.
- **subagent-driven-development** - Use this skill to execute implementation plans using subagents.
- **systematic-debugging** - Use this skill when debugging issues, errors, or unexpected behavior.
- **test-driven-development** - Use this skill during implementation to enforce RED-GREEN-REFACTOR cycle.
- **using-git-worktrees** - Use this skill to create isolated development environments for features.
- **writing-plans** - Use this skill after design approval to break work into bite-sized, actionable tasks.

### 🏗️ Architecture (6 skills)
*The masterminds who design your digital empire*
- **api-designer** - Use this agent when you need to design REST APIs, GraphQL schemas, or other API interfaces.
- **database-planner** - Use this agent when you need to design database schemas, plan data models, optimize queries, or solve database-related architectural challenges.
- **feature-spec-writer** - Use this agent when you need to write detailed technical specifications for new features or system components.
- **supabase-architect** - Use this agent when you need to design Supabase database schemas, plan project architecture, optimize queries, or design real-time features.
- **system-designer** - Use this agent when you need to design system architecture, plan technical infrastructure, or create end-to-end solutions for complex challenges.
- **tech-stack-advisor** - Use this agent when you need to choose technologies, evaluate frameworks, or make architectural technology decisions.

### 🏗️ Code quality (6 skills)
*The guardians of clean, secure, and blazing-fast code*
- **code-reviewer** - Use this agent when you need expert code review and quality analysis.
- **documentation-writer** - Use this agent when you need to create or improve code documentation, API docs, README files, or technical documentation.
- **performance-optimizer** - Use this agent when you need to analyze and optimize code performance, identify bottlenecks, or improve application speed and efficiency.
- **refactoring-expert** - Use this agent when you need to refactor existing code, improve code structure, or modernize legacy code.
- **security-auditor** - Use this agent when you need to audit code for security vulnerabilities, implement security best practices, or review security-sensitive features.
- **test-strategist** - Use this agent when you need to plan testing strategies, write test cases, or improve test coverage.

### 🏗️ Design (9 skills)
*The creative geniuses who make everything beautiful*
- **brand-designer** - Use this agent when you need to create brand identity elements, design logos, or establish visual brand guidelines.
- **brand-guidelines** - Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel.
- **color-specialist** - Use this agent when you need to choose color schemes, create color palettes, or ensure color accessibility.
- **design-system-builder** - Use this agent to create and manage comprehensive design systems.
- **icon-designer** - Use this agent when you need to design custom icons, create iconography systems, or plan visual symbols for your application.
- **layout-designer** - Use this agent when you need to create page layouts, design responsive grid systems, or plan content organization.
- **typography-expert** - Use this agent when you need to choose fonts, create typography systems, or optimize text readability and hierarchy.
- **ui-designer** - Use this agent when you need to design user interfaces, create UI components, or improve visual design.
- **wireframe-creator** - Use this agent when you need to create wireframes, plan user flows, or design low-fidelity prototypes.

### 🏗️ Marketing (8 skills)
*The word wizards who turn features into must-haves*
- **ad-copy-creator** - Use this agent when you need to create paid advertising copy for Google Ads, Facebook Ads, LinkedIn Ads, or other platforms.
- **blog-writer** - Use this agent when you need to create technical blog posts, tutorials, or content marketing articles.
- **copywriter** - Use this agent when you need compelling marketing copy, product descriptions, headlines, or persuasive content.
- **email-writer** - Use this agent when you need to create email campaigns, newsletters, or automated email sequences.
- **landing-page-writer** - Use this agent when you need to create high-converting landing page copy, optimize conversion rates, or write persuasive sales pages.
- **seo-optimizer** - Use this agent when you need to optimize content for search engines, improve SEO rankings, or research keywords.
- **social-media-creator** - Use this agent when you need to create social media content, plan posting strategies, or engage with online communities.
- **youtube-downloader** - Download YouTube videos with customizable quality and format options.

### 🏗️ Product (6 skills)
*The user champions who build products people actually want*
- **accessibility-checker** - Use this agent when you need to audit accessibility compliance, ensure WCAG standards, or make interfaces inclusive for users with disabilities.
- **competitor-researcher** - Use this agent when you need to analyze competitors, research market positioning, or understand competitive landscape.
- **feature-prioritizer** - Use this agent when you need to prioritize feature requests, evaluate competing development options, or make strategic product decisions.
- **feedback-analyzer** - Use this agent when you need to analyze user feedback, customer reviews, or support tickets to extract actionable insights.
- **user-story-writer** - Use this agent when you need to write user stories, acceptance criteria, or translate business requirements into development tasks.
- **ux-reviewer** - Use this agent when you need to review user experience designs, analyze user interfaces, or improve usability.

### 🏗️ Business (6 skills)
*The suit-wearing strategists who keep the lights on*
- **business-model-analyzer** - Use this agent when you need to analyze business models, evaluate monetization strategies, or optimize business operations.
- **financial-planner** - Use this agent when you need to create financial projections, analyze business finances, or plan funding strategies.
- **market-researcher** - Use this agent when you need to research target markets, analyze customer segments, or understand market opportunities.
- **pricing-strategist** - Use this agent when you need to develop pricing models, analyze pricing strategies, or optimize revenue structures.
- **privacy-policy-writer** - Use this agent when you need to create or update privacy policies, ensure GDPR compliance, or handle data protection requirements.
- **terms-writer** - Use this agent when you need to create terms of service, user agreements, or legal documents for your application.

### 🏗️ Devops (6 skills)
*The infrastructure heroes who keep your app running while you sleep*
- **backup-planner** - Use this agent when you need to design backup strategies, plan disaster recovery, or implement data protection systems.
- **cost-optimizer** - Use this agent when you need to analyze and reduce cloud infrastructure costs, optimize resource usage, or plan cost-effective scaling strategies.
- **deployment-troubleshooter** - Use this agent when you need to fix deployment issues, resolve CI/CD problems, or troubleshoot infrastructure deployments.
- **error-investigator** - Use this agent when you need to debug production issues, analyze error logs, or troubleshoot system problems.
- **monitoring-setup** - Use this agent when you need to set up monitoring, alerting, or observability systems.
- **supabase-security-reviewer** - Use this agent when you need to audit Supabase RLS policies, review auth configuration, check for security vulnerabilities, or ensure data protection compliance.

### 🏗️ Data (5 skills)
*The number crunchers who turn chaos into insights*
- **analytics-setup** - Use this agent when you need to implement analytics tracking, set up measurement systems, or create data collection strategies.
- **dashboard-planner** - Use this agent when you need to design operational dashboards, plan business intelligence interfaces, or create data monitoring systems.
- **data-visualizer** - Use this agent when you need to create charts, graphs, or visual representations of data.
- **report-generator** - Use this agent when you need to create automated reports, generate business intelligence summaries, or build recurring data reports.
- **sql-expert** - Use this agent when you need to write complex SQL queries, optimize database performance, or solve data analysis problems.

### 🏗️ Communication (6 skills)
*The translators who make tech speak human*
- **api-documenter** - Use this agent when you need to create API documentation, developer references, or integration guides.
- **changelog-writer** - Use this agent when you need to create release notes, changelogs, or product update communications.
- **presentation-builder** - Use this agent when you need to create presentations, pitch decks, or structured presentation content.
- **support-responder** - Use this agent when you need to create customer support responses, help desk communications, or customer service templates.
- **team-communicator** - Use this agent when you need to create internal team communications, status updates, or organizational announcements.
- **technical-writer** - Use this agent when you need to create any form of technical documentation, including user guides, API references, README files, or architectural documents.

### 🏗️ Research (5 skills)
*The curious minds who keep you ahead of the curve*
- **best-practice-finder** - Use this agent when you need to research industry best practices, development standards, or proven methodologies.
- **library-evaluator** - Use this agent when you need to evaluate libraries, frameworks, or development tools for specific projects.
- **solution-architect** - Use this agent when you need to research and design comprehensive solutions for complex technical challenges.
- **technology-researcher** - Use this agent when you need to research new technologies, evaluate emerging tools, or analyze technology trends.
- **trend-analyzer** - Use this agent when you need to analyze industry trends, predict technology directions, or understand market evolution patterns.

### 🏗️ Project management (2 skills)
*The organizers who ensure on-time and on-budget delivery*
- **agile-coach** - Use this agent when you need help with Agile methodologies, Sprint planning, Retrospectives, or improving team processes.
- **project-planner** - Use this agent when you need to break down large initiatives into tasks, create roadmaps, or manage project timelines.

### 🏗️ Skills (7 skills)
*Specialized AI skills for common development tasks*
- **adr** - Generates Architecture Decision Records (ADRs) with context, decision, consequences, and maintains an index.
- **api-spec** - Generates OpenAPI 3.
- **developer-growth-analysis** - Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant learning resources from HackerNews, and automatically sends a personalized growth report to your Slack DMs.
- **env-setup** - Generates environment configuration including .
- **github-actions** - Generates CI/CD pipelines for GitHub Actions.
- **test-suite** - Scaffolds test files for existing code.
- **typescript-best-practices** - This skill should be used when the user asks to "review TypeScript code", "check my TS code", "review this TypeScript", "write TypeScript", or when writing, reviewing, or refactoring TypeScript code in projects with tsconfig.

## 🚀 Workflow Skills (Inspired by Superpowers)

This package includes 8 powerful **workflow skills** that bring structured development methodologies to your AI agents:

| Skill | Purpose |
|-------|---------|
| `brainstorming` | Refine ideas through Socratic questioning before coding |
| `writing-plans` | Break designs into 2-5 minute actionable tasks |
| `subagent-driven-development` | Execute plans with parallel subagents and two-stage review |
| `executing-plans` | Batch implementation with human checkpoints |
| `test-driven-development` | Enforce RED-GREEN-REFACTOR cycles |
| `systematic-debugging` | 4-phase root cause analysis |
| `using-git-worktrees` | Isolated development environments |
| `requesting-code-review` | Pre-merge quality gates |

### Development Workflow

These skills work together to create a complete development lifecycle:

```
brainstorming → writing-plans → using-git-worktrees → subagent-driven-development
       ↓                                                        ↓
[Design doc]                                          test-driven-development
       ↓                                                        ↓
writing-plans ←←←←←←←←← requesting-code-review ←←←←←← [Implementation]
```

**Key Principles:**
- 🧪 **Test-First**: Write failing tests before implementation
- 📋 **Plan-Driven**: Every task has exact specifications
- 🔍 **Evidence-Based**: Debug systematically, don't guess
- ✓ **Quality Gates**: Two-stage review before completion

## 🎯 What Makes These Agents Special

### 🌍 Universal Compatibility
- **Language Agnostic**: Python, JavaScript, Go, Rust, PHP - they speak them all
- **Platform Independent**: Web, mobile, desktop, backend - covered!
- **Framework Flexible**: React, Laravel, Django, Next.js - no favorites here

### 🚀 Production Ready
- **Detailed Prompts**: No vague "help me code" - these agents know exactly what to do
- **Context Aware**: They collaborate like a real team (minus the meeting overhead)
- **Quality Focused**: Production-grade outputs, not "here's a basic example" stuff

### ⚡ Easy Integration
- **YAML Frontmatter**: Proper Claude Code format - just works!
- **Automatic Delegation**: Claude Code picks the right agent automagically
- **Model Optimized**: Smart agents (Sonnet) for thinking, fast agents (Haiku) for writing

## 📖 Examples

### System Design
```
You: "I need to design a scalable architecture for a social media app"
Claude: [Uses system-designer agent to create comprehensive architecture]
```

### Marketing Copy  
```
You: "Write landing page copy for my project management SaaS"
Claude: [Uses landing-page-writer agent to create conversion-focused copy]
```

### Code Review
```
You: "Review this authentication function for security issues"
Claude: [Uses security-auditor and code-reviewer agents together]
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new agents
- Improving existing agents
- Reporting issues
- Submitting improvements

Check out [EXAMPLES.md](EXAMPLES.md) for detailed usage examples and workflows.

## 💖 Support This Project

**Love these agents?** Consider sponsoring to support continued development and new agent creation!

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink)](https://github.com/sponsors/aaronlumsden)

Your sponsorship helps me:
- 🤖 Create more specialized agents
- 🚀 Keep agents updated with best practices
- 📚 Maintain documentation and examples
- ⚡ Build more developer tools like this

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)


---

**Made for developers building the future** 🚀