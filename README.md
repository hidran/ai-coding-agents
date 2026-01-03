# AI Agents 🤖

<div align="center">
  <img src="https://vizra.ai/img/vizra-logo.svg" alt="Vizra" width="120" style="margin-bottom: 20px;">
  
  Forked and maintained by [hidran](https://github.com/hidran)
  
  <small>Based on the original project by [Vizra-AI](https://github.com/vizra-ai/claude-code-agents)</small>
</div>

---

**Your new AI-powered development squad is here!** 🚀

Meet 61 specialized AI agents that supercharge your development workflow. From system architecture to marketing copy, these Claude Code agents are like having a whole team of experts at your fingertips - and they never need coffee breaks!

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

### 2. Run the Installer
Execute the `scripts/install.sh` script. This script now automates the entire process and supports multiple AI platforms.

```bash
# For Claude Code agents (default)
./scripts/install.sh --platform=claude

# For Gemini agents
./scripts/install.sh --platform=gemini

# You can also omit --platform, and it will default to 'claude'
./scripts/install.sh
```
This will build and validate all the agents, and copy the complete, verified set into the `./.claude/agents` directory (or equivalent in your current working directory).

### 3. Restart and Use
Restart your IDE or code editor where you use Claude Code. The new agents will now be available for use.

### Usage
Once installed, it's like having 61 AI specialists on speed dial! 📞

- **🎯 Automatic Delegation**: Claude Code automatically calls in the right expert for your task.
- **🗣️ Explicit Invocation**: "Hey `code-reviewer`, check this function!" - just ask for any agent by name.
- **🧠 Context-Aware**: Your AI team collaborates seamlessly on complex multi-step projects.

📚 **New to Claude Code agents?** Check out the [official documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) to learn how agents work.

## 🤖 Your AI Dream Team

*Meet your new coding sidekicks - each one a specialist in their field:*

### 🏗️ Architecture (5 agents)
*The masterminds who design your digital empire*
- **api-designer** - A specialist in api designer.
- **database-planner** - A specialist in database planner.
- **feature-spec-writer** - A specialist in feature spec writer.
- **system-designer** - A specialist in system designer.
- **tech-stack-advisor** - A specialist in tech stack advisor.

### 🏗️ Code-quality (6 agents)
*The guardians of clean, secure, and blazing-fast code*
- **code-reviewer** - A specialist in code reviewer.
- **documentation-writer** - A specialist in documentation writer.
- **performance-optimizer** - A specialist in performance optimizer.
- **refactoring-expert** - A specialist in refactoring expert.
- **security-auditor** - A specialist in security auditor.
- **test-strategist** - A specialist in test strategist.

### 🏗️ Design (8 agents)
*The creative geniuses who make everything beautiful*
- **brand-designer** - A specialist in brand designer.
- **color-specialist** - A specialist in color specialist.
- **design-system-builder** - A specialist in design system builder.
- **icon-designer** - A specialist in icon designer.
- **layout-designer** - A specialist in layout designer.
- **typography-expert** - A specialist in typography expert.
- **ui-designer** - A specialist in ui designer.
- **wireframe-creator** - A specialist in wireframe creator.

### 🏗️ Marketing (7 agents)
*The word wizards who turn features into must-haves*
- **ad-copy-creator** - A specialist in ad copy creator.
- **blog-writer** - A specialist in blog writer.
- **copywriter** - A specialist in copywriter.
- **email-writer** - A specialist in email writer.
- **landing-page-writer** - A specialist in landing page writer.
- **seo-optimizer** - A specialist in seo optimizer.
- **social-media-creator** - A specialist in social media creator.

### 🏗️ Product (6 agents)
*The user champions who build products people actually want*
- **accessibility-checker** - A specialist in accessibility checker.
- **competitor-researcher** - A specialist in competitor researcher.
- **feature-prioritizer** - A specialist in feature prioritizer.
- **feedback-analyzer** - A specialist in feedback analyzer.
- **user-story-writer** - A specialist in user story writer.
- **ux-reviewer** - A specialist in ux reviewer.

### 🏗️ Business (6 agents)
*The suit-wearing strategists who keep the lights on*
- **business-model-analyzer** - A specialist in business model analyzer.
- **financial-planner** - A specialist in financial planner.
- **market-researcher** - A specialist in market researcher.
- **pricing-strategist** - A specialist in pricing strategist.
- **privacy-policy-writer** - A specialist in privacy policy writer.
- **terms-writer** - A specialist in terms writer.

### 🏗️ Devops (5 agents)
*The infrastructure heroes who keep your app running while you sleep*
- **backup-planner** - A specialist in backup planner.
- **cost-optimizer** - A specialist in cost optimizer.
- **deployment-troubleshooter** - A specialist in deployment troubleshooter.
- **error-investigator** - A specialist in error investigator.
- **monitoring-setup** - A specialist in monitoring setup.

### 🏗️ Data (5 agents)
*The number crunchers who turn chaos into insights*
- **analytics-setup** - A specialist in analytics setup.
- **dashboard-planner** - A specialist in dashboard planner.
- **data-visualizer** - A specialist in data visualizer.
- **report-generator** - A specialist in report generator.
- **sql-expert** - A specialist in sql expert.

### 🏗️ Communication (6 agents)
*The translators who make tech speak human*
- **api-documenter** - A specialist in api documenter.
- **changelog-writer** - A specialist in changelog writer.
- **presentation-builder** - A specialist in presentation builder.
- **support-responder** - A specialist in support responder.
- **team-communicator** - A specialist in team communicator.
- **technical-writer** - A specialist in technical writer.

### 🏗️ Research (5 agents)
*The curious minds who keep you ahead of the curve*
- **best-practice-finder** - A specialist in best practice finder.
- **library-evaluator** - A specialist in library evaluator.
- **solution-architect** - A specialist in solution architect.
- **technology-researcher** - A specialist in technology researcher.
- **trend-analyzer** - A specialist in trend analyzer.

### 🏗️ Project-management (2 agents)
*The organizers who ensure on-time and on-budget delivery*
- **agile-coach** - A specialist in agile coach.
- **project-planner** - A specialist in project planner.

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