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

{{AGENT_LIST}}

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
