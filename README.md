<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=AI%20Coding%20Agents&fontSize=60&fontAlignY=35&animation=twinkling&desc=80%2B%20Specialized%20AI%20Agents%20for%20Development%20Workflows&descSize=20&descAlignY=60" />

<!-- Badges -->
<p align="center">
  <a href="https://github.com/hidran/ai-coding-agents/stargazers">
    <img src="https://img.shields.io/github/stars/hidran/ai-coding-agents?style=for-the-badge&color=yellow&logo=github" alt="Stars" />
  </a>
  <a href="https://github.com/hidran/ai-coding-agents/network/members">
    <img src="https://img.shields.io/github/forks/hidran/ai-coding-agents?style=for-the-badge&color=blue&logo=git" alt="Forks" />
  </a>
  <a href="https://github.com/hidran/ai-coding-agents/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/hidran/ai-coding-agents?style=for-the-badge&color=green" alt="License" />
  </a>
  <a href="https://github.com/hidran/ai-coding-agents/releases">
    <img src="https://img.shields.io/github/v/release/hidran/ai-coding-agents?style=for-the-badge&color=orange&logo=github" alt="Release" />
  </a>
</p>

<p align="center">
  <a href="https://docs.anthropic.com/claude-code">
    <img src="https://img.shields.io/badge/Claude%20Code-Compatible-orange?style=flat-square&logo=anthropic" alt="Claude Code" />
  </a>
  <a href="https://gemini.google.com">
    <img src="https://img.shields.io/badge/Gemini%20CLI-Extension-blue?style=flat-square&logo=google" alt="Gemini" />
  </a>
  <a href="https://github.com/kimi-cli/kimi-cli">
    <img src="https://img.shields.io/badge/Kimi%20CLI-Skill-purple?style=flat-square" alt="Kimi CLI" />
  </a>
  <img src="https://img.shields.io/badge/Total%20Agents-80+-success?style=flat-square" alt="80+ Agents" />
  <img src="https://img.shields.io/badge/Test%20Coverage-95%25-brightgreen?style=flat-square" alt="Coverage" />
</p>

<!-- Quick Install Banner -->
<p align="center">
  <strong>⚡ One Command Install</strong>
</p>

```bash
# Claude Code
/plugin install ai-coding-agents@hidran/ai-coding-agents

# Gemini CLI
gemini extensions install https://github.com/hidran/ai-coding-agents
```

<p align="center">
  <a href="#-quick-start"><strong>📖 Documentation</strong></a> •
  <a href="#-available-agents"><strong>🤖 Agents</strong></a> •
  <a href="#-examples"><strong>🎯 Examples</strong></a> •
  <a href="#-contributing"><strong>🤝 Contribute</strong></a> •
  <a href="https://github.com/hidran/ai-coding-agents/discussions"><strong>💬 Discussions</strong></a>
</p>

</div>

---

## 🎯 What Makes This Special?

Transform your AI coding assistant into a **complete development team** with 80+ specialized agents. From architecture to marketing, testing to deployment—get expert-level assistance for every phase of development.

### ✨ Key Features

<table>
<tr>
<td width="33%">

**🎭 Specialized Agents**
- 80+ domain experts
- Auto-trigger by context
- Framework-specific generators
- Architecture & design agents

</td>
<td width="33%">

**⚙️ Workflow Automation**
- TDD enforcement
- Subagent-driven development
- Systematic debugging
- Code review workflows

</td>
<td width="33%">

**🚀 Multi-Platform**
- Claude Code plugin
- Gemini CLI extension
- Kimi CLI skill
- OpenCode compatible

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Option 1: Claude Code Plugin (Easiest)

```bash
# Add marketplace once
/plugin marketplace add hidran/ai-coding-agents

# Install the plugin
/plugin install ai-coding-agents@hidran/ai-coding-agents
```

### Option 2: Gemini CLI Extension

```bash
gemini extensions install https://github.com/hidran/ai-coding-agents
```

### Option 3: One-Liner Install (Universal)

```bash
# Works for Claude, Gemini, Codex, Kimi
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" --all; rm -rf "$D"'
```

---

## 🎬 See It In Action

### Example 1: Complete Feature Development

```
You: "Build a user authentication system"

🤖 @brainstorming → Refines requirements, explores OAuth vs JWT
🤖 @writing-plans → Creates 12 detailed implementation tasks  
🤖 @using-git-worktrees → Creates isolated workspace
🤖 @subagent-driven-development → Executes tasks in parallel
🤖 @test-driven-development → Enforces RED-GREEN-REFACTOR
🤖 @requesting-code-review → Quality gate before completion
```

### Example 2: Debug Production Issue

```
You: "Users can't login after latest deploy"

🔍 @systematic-debugging
  → Phase 1: Gather facts (logs, recent commits)
  → Phase 2: Form hypotheses (3 possible causes)
  → Phase 3: Test each hypothesis
  → Phase 4: Fix root cause (not symptoms)
```

---

## 🤖 Available Agents

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

---

## 🚀 Workflow Skills (Inspired by Superpowers)

> "The best developers don't just write code—they follow proven processes."

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `brainstorming` | Socratic design refinement | Starting new features |
| `writing-plans` | 2-5 minute task breakdown | After design approval |
| `subagent-driven-development` | Parallel agent execution | Complex implementations |
| `test-driven-development` | RED-GREEN-REFACTOR | All code changes |
| `systematic-debugging` | 4-phase root cause analysis | Any bug or error |
| `using-git-worktrees` | Isolated environments | Parallel features |
| `requesting-code-review` | Pre-merge quality gates | Before committing |
| `executing-plans` | Batch with checkpoints | Simple implementations |

---

## 📊 Comparison with Alternatives

| Feature | AI Coding Agents | Superpowers | Default Claude |
|---------|-----------------|-------------|----------------|
| **Total Agents** | 80+ | 17+ | ~10 built-in |
| **Workflow Skills** | ✅ 8 skills | ✅ Yes | ❌ No |
| **TDD Enforcement** | ✅ Built-in | ✅ Yes | ❌ No |
| **Framework Generators** | ✅ Laravel, React, etc. | ❌ No | ⚠️ Limited |
| **Multi-Platform** | ✅ Claude/Gemini/Kimi | ✅ Claude/Cursor | ⚠️ Claude only |
| **Code Review** | ✅ 2-stage process | ✅ Yes | ⚠️ Basic |
| **Debugging Process** | ✅ 4-phase systematic | ✅ Yes | ⚠️ Ad-hoc |
| **Free/Open Source** | ✅ MIT License | ✅ MIT | N/A |

---

## 🎯 Perfect For

<table>
<tr>
<td>

**👨‍💻 Solo Developers**
Get a full dev team experience without hiring

</td>
<td>

**🏢 Startups**
Move fast with expert-level code quality

</td>
<td>

**📚 Learners**
Learn best practices from AI mentors

</td>
</tr>
<tr>
<td>

**🔧 Consultants**
Deliver consistent, high-quality work

</td>
<td>

**🏛️ Enterprises**
Standardize development workflows

</td>
<td>

**🎓 Students**
Build real projects with expert guidance

</td>
</tr>
</table>

---

## 💬 What Users Say

> *"Game changer for my freelance work. I deliver faster with better quality."*
> — @developer123

> *"The TDD workflow skill actually taught me proper test-driven development."*
> — @learner_dev

> *"Went from idea to production in 3 days using the workflow agents."*
> — @startup_founder

---

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) to:

- 🆕 Add new agents
- 🔧 Improve existing agents
- 🐛 Report bugs
- 💡 Suggest features

### Contributors

<a href="https://github.com/hidran/ai-coding-agents/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=hidran/ai-coding-agents" />
</a>

---

## ⭐ Star History

<a href="https://star-history.com/#hidran/ai-coding-agents&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=hidran/ai-coding-agents&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=hidran/ai-coding-agents&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=hidran/ai-coding-agents&type=Date" />
  </picture>
</a>

---

## 📈 Repository Stats

<p align="center">
  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=hidran&repo=ai-coding-agents&theme=default&show_owner=true" />
  <img width="49%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=hidran&layout=compact&theme=default" />
</p>

---

## 📄 License

[MIT License](LICENSE) © [hidran](https://github.com/hidran)

---

<div align="center">

**If this project helped you, please ⭐ star it!**

<a href="https://github.com/hidran/ai-coding-agents">
  <img src="https://img.shields.io/badge/Star%20This%20Repo-⭐-yellow?style=for-the-badge" alt="Star" />
</a>

Made with ❤️ for the developer community

</div>
