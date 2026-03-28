# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-03-28

### Added
- **8 Workflow Skills** inspired by Superpowers methodology
  - `brainstorming` - Socratic design refinement
  - `writing-plans` - 2-5 minute task breakdown
  - `subagent-driven-development` - Parallel agent execution
  - `executing-plans` - Batch implementation with checkpoints
  - `test-driven-development` - RED-GREEN-REFACTOR enforcement
  - `systematic-debugging` - 4-phase root cause analysis
  - `using-git-worktrees` - Isolated dev environments
  - `requesting-code-review` - Pre-merge quality gates
- **Multi-platform plugin support**
  - Claude Code plugin manifest (`.claude-plugin/`)
  - Gemini CLI extension (`.gemini/`)
  - Kimi CLI skill (`.agents/skills/ai-coding-agents/`)
  - OpenCode support (`.opencode/`)
- Enhanced build system supporting multiple source directories
- 80 total agents (up from 65)

### Changed
- Improved README with badges, comparison tables, and visual elements
- Updated package.json with SEO-friendly keywords
- Restructured project for better organization

## [1.0.0] - 2026-02-15

### Added
- Initial release with 65 specialized AI agents
- Build system with Node.js and Python support
- Interactive skill selector
- Multi-platform installation scripts
- Support for Claude Code, Gemini CLI, and Codex

[2.0.0]: https://github.com/hidran/ai-coding-agents/releases/tag/v2.0.0
[1.0.0]: https://github.com/hidran/ai-coding-agents/releases/tag/v1.0.0
