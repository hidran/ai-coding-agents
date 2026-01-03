# AI Agents 🤖

<div align="center">
  <img src="https://vizra.ai/img/vizra-logo.svg" alt="Vizra" width="120" style="margin-bottom: 20px;">
  
  Forked and maintained by [hidran](https://github.com/hidran)
  
  <small>Based on the original project by [Vizra-AI](https://github.com/vizra-ai/claude-code-agents)</small>
</div>

---

**Your new AI-powered development squad is here!** 🚀

Meet 59 specialized AI agents that supercharge your development workflow. From system architecture to marketing copy, these Claude Code agents are like having a whole team of experts at your fingertips - and they never need coffee breaks!

## 🚀 Quick Start

The installation process is now simpler and more reliable. You no longer need to manually copy individual files.

### 1. Clone the Repository
If you haven't already, clone the project to your local machine:
```bash
git clone https://github.com/hidran/claude-code-agents.git
cd claude-code-agents
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
Once installed, it's like having 59 AI specialists on speed dial! 📞

- **🎯 Automatic Delegation**: Claude Code automatically calls in the right expert for your task.
- **🗣️ Explicit Invocation**: "Hey `code-reviewer`, check this function!" - just ask for any agent by name.
- **🧠 Context-Aware**: Your AI team collaborates seamlessly on complex multi-step projects.

📚 **New to Claude Code agents?** Check out the [official documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) to learn how agents work.

{{AGENT_LIST}}

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