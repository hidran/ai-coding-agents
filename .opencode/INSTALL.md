# AI Coding Agents - OpenCode Installation

## Quick Install

```bash
# Fetch and run installer
curl -fsSL https://raw.githubusercontent.com/hidran/ai-coding-agents/main/scripts/install.sh | bash -s -- --platform=opencode
```

## Manual Install

```bash
# Clone repository
git clone https://github.com/hidran/ai-coding-agents.git
cd ai-coding-agents

# Install dependencies
npm install

# Build for OpenCode
npm run build -- --platform=opencode --all

# Skills available in dist/.opencode/skills/
```

## Usage

After installation, all 65+ agents are available in OpenCode. They auto-trigger based on your requests.

## Categories

- **Workflow** - Development process automation
- **Architecture** - System design agents
- **Code Quality** - Review, testing, security
- **Framework Generators** - Laravel, React, Next.js, etc.

## Documentation

- Main README: https://github.com/hidran/ai-coding-agents
- Examples: EXAMPLES.md
- Contributing: CONTRIBUTING.md
