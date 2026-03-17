# AI Agents 🤖

<div align="center">
  <img src="https://vizra.ai/img/vizra-logo.svg" alt="Vizra" width="120" style="margin-bottom: 20px;">
  
  Forked and maintained by [hidran](https://github.com/hidran)
  
  <small>Based on the original project by [Vizra-AI](https://github.com/vizra-ai/claude-code-agents)</small>
</div>

---

**Your new AI-powered development squad is here!** 🚀

Meet 65 specialized AI skills that supercharge your development workflow. From system architecture to marketing copy, these Claude Code agents are like having a whole team of experts at your fingertips - and they never need coffee breaks!

## 🚀 Quick Install (One-Liner)

You can install the agents directly into your current project without manually cloning the repository:

```bash
# For Claude (default)
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"'

# For Gemini
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"' -- gemini

# For Codex
bash -c 'D=$(mktemp -d); git clone --depth 1 https://github.com/hidran/ai-coding-agents.git "$D" -q; "$D/scripts/install.sh" "$@"; rm -rf "$D"' -- codex
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

### 🏗️ Architecture (7 skills)
*The masterminds who design your digital empire*
- **api-designer** - API Design Specialist for REST APIs, GraphQL schemas, and API interfaces.
- **api-documenter** - API documentation specialist for developer resources.
- **database-planner** - Database Architecture Specialist for schema design and optimization.
- **design-system-builder** - Design systems specialist for comprehensive component libraries.
- **feature-spec-writer** - Technical Specification Writer for detailed feature documentation.
- **system-designer** - System & Solution Architect for high-level distributed systems.
- **tech-stack-advisor** - Technology Stack Advisor for framework and technology decisions.

### 🏗️ Code quality (6 skills)
*The guardians of clean, secure, and blazing-fast code*
- **code-reviewer** - Senior Code Reviewer for quality analysis and issue detection.
- **documentation-writer** - Technical Documentation Specialist for code docs and guides.
- **performance-optimizer** - Performance Optimization Engineer for speed and efficiency.
- **refactoring-expert** - Refactoring Specialist for code structure improvement.
- **security-auditor** - Application Security Engineer for vulnerability detection.
- **test-strategist** - QA Architect for testing strategies and coverage.

### 🏗️ Design (9 skills)
*The creative geniuses who make everything beautiful*
- **brand-designer** - Brand design specialist for identity and visual systems.
- **brand-guidelines** - Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel.
- **color-specialist** - Color design specialist for palettes and accessibility.
- **icon-designer** - Icon design specialist for iconography systems.
- **layout-designer** - Layout design specialist for responsive grids and page structure.
- **presentation-builder** - Presentation design specialist for pitch decks and slides.
- **typography-expert** - Typography specialist for font systems and readability.
- **ui-designer** - UI design specialist for interfaces and components.
- **wireframe-creator** - Wireframing specialist for user flows and prototypes.

### 🏗️ Marketing (8 skills)
*The word wizards who turn features into must-haves*
- **ad-copy-creator** - Paid advertising copywriter for Google Ads, Facebook Ads, LinkedIn Ads.
- **blog-writer** - Technical content specialist for blog posts and tutorials.
- **copywriter** - Professional copywriter for marketing copy and product descriptions.
- **email-writer** - Email marketing specialist for campaigns and sequences.
- **landing-page-writer** - Landing page copywriting specialist for high-converting sales pages.
- **seo-optimizer** - SEO specialist for search engine optimization and keyword research.
- **social-media-creator** - Social media specialist for content and posting strategies.
- **youtube-downloader** - Download YouTube videos with customizable quality and format options.

### 🏗️ Product (6 skills)
*The user champions who build products people actually want*
- **accessibility-checker** - Accessibility compliance specialist for WCAG standards and inclusive design.
- **competitor-researcher** - Competitive intelligence specialist for market analysis.
- **feature-prioritizer** - Product strategy specialist for prioritizing features and roadmaps.
- **feedback-analyzer** - User feedback analysis specialist for extracting insights.
- **user-story-writer** - Product requirements specialist for user stories and acceptance criteria.
- **ux-reviewer** - User experience specialist for interface evaluation and usability.

### 🏗️ Business (6 skills)
*The suit-wearing strategists who keep the lights on*
- **business-model-analyzer** - Business model specialist for analyzing and optimizing revenue structures.
- **financial-planner** - Financial planning specialist for projections and analysis.
- **market-researcher** - Market research specialist for analyzing markets and opportunities.
- **pricing-strategist** - Pricing strategy specialist for revenue-optimized models.
- **privacy-policy-writer** - Privacy policy specialist for GDPR-compliant documentation.
- **terms-writer** - Legal document specialist for terms of service and agreements.

### 🏗️ Devops (5 skills)
*The infrastructure heroes who keep your app running while you sleep*
- **backup-planner** - Disaster Recovery and Business Continuity Architect for backup strategies.
- **cost-optimizer** - FinOps and Cloud Cost Specialist for reducing infrastructure costs.
- **deployment-troubleshooter** - CI/CD and Infrastructure Reliability Engineer for deployment issues.
- **error-investigator** - Root Cause Analysis Investigator for production issues.
- **monitoring-setup** - Observability Engineer for monitoring and alerting systems.

### 🏗️ Data (5 skills)
*The number crunchers who turn chaos into insights*
- **analytics-setup** - Analytics implementation specialist for tracking and measurement.
- **dashboard-planner** - Dashboard design specialist for BI and monitoring interfaces.
- **data-visualizer** - Data visualization specialist for charts and visual representations.
- **report-generator** - Business reporting specialist for automated reports.
- **sql-expert** - SQL database specialist for queries and optimization.

### 🏗️ Communication (4 skills)
*The translators who make tech speak human*
- **changelog-writer** - Product communication specialist for release notes.
- **support-responder** - Customer support specialist for service communications.
- **team-communicator** - Internal communications specialist for team updates.
- **technical-writer** - Technical documentation specialist for comprehensive docs.

### 🏗️ Research (6 skills)
*The curious minds who keep you ahead of the curve*
- **best-practice-finder** - Best practices research specialist for industry standards and proven methodologies.
- **library-evaluator** - Library and framework evaluation specialist for technical tool selection.
- **solution-architect** - Solution architecture specialist for complex technical challenges.
- **technology-researcher** - Technology research specialist for emerging technologies and tools.
- **trend-analyzer** - Trend analysis specialist for industry trends and market evolution.
- **typescript-best-practices** - This skill should be used when the user asks to "review TypeScript code", "check my TS code", "review this TypeScript", "write TypeScript", or when writing, reviewing, or refactoring TypeScript code in projects with tsconfig.

### 🏗️ Project management (2 skills)
*The organizers who ensure on-time and on-budget delivery*
- **agile-coach** - Agile Coach and Scrum Master for methodologies, Sprint planning, Retrospectives.
- **project-planner** - Technical Project Manager for breaking down initiatives, creating roadmaps, managing timelines.

### 🏗️ Skills (1 skills)
*Specialized AI skills for common development tasks*
- **developer-growth-analysis** - Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant learning resources from HackerNews, and automatically sends a personalized growth report to your Slack DMs.

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