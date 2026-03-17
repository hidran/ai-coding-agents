#!/bin/bash

# AI Coding Agents Installer
# Installs skills for Claude Code, Gemini, Codex, and other AI platforms

# Determine the directory where the install.sh script is located
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
CLAUDES_CODE_AGENTS_ROOT="$(dirname "$SCRIPT_DIR")"

VERSION="v2.0.0"
DIST_DIR="$CLAUDES_CODE_AGENTS_ROOT/dist"

# Detect available build script (Node.js preferred, fallback to Python)
NODE_BUILD_SCRIPT="$CLAUDES_CODE_AGENTS_ROOT/scripts/build.js"
PYTHON_BUILD_SCRIPT="$CLAUDES_CODE_AGENTS_ROOT/scripts/build.py"

# Auto-detect build tool
if command -v node &> /dev/null && [ -f "$NODE_BUILD_SCRIPT" ] && [ -d "$CLAUDES_CODE_AGENTS_ROOT/node_modules" ]; then
    USE_NODE=true
    BUILD_SCRIPT="$NODE_BUILD_SCRIPT"
    BUILD_CMD="node"
elif command -v python3 &> /dev/null && [ -f "$PYTHON_BUILD_SCRIPT" ]; then
    USE_NODE=false
    BUILD_SCRIPT="$PYTHON_BUILD_SCRIPT"
    BUILD_CMD="python3"
else
    echo "❌ Error: Neither Node.js (with dependencies) nor Python 3 is available."
    echo "   Install one of them:"
    echo "   • Node.js: npm install"
    echo "   • Python:  python3 -m pip install -r requirements.txt"
    exit 1
fi

RELEASE_ARCHIVE="skills.tar.gz"

# Default settings
PLATFORM="claude"
SKILLS=""
BUILD_ALL=false
INTERACTIVE=false
VENV_DIR="$CLAUDES_CODE_AGENTS_ROOT/venv"
REQUIREMENTS_FILE="$CLAUDES_CODE_AGENTS_ROOT/requirements.txt"

show_help() {
  echo "AI Coding Agents Installer $VERSION"
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  --platform=<platform>   Target platform (claude|gemini|codex). Default: claude"
  echo "  --all                   Install all available skills"
  echo "  --skills=<list>         Comma-separated list of skills to install"
  echo "  --interactive           Interactive skill selection"
  echo "  --list                  List all available skills and exit"
  echo "  --help, -h              Show this help message and exit"
  echo ""
  echo "Prerequisites:"
  echo "  Node.js version (recommended): npm install"
  echo "  Python version (fallback):     pip install -r requirements.txt"
  echo ""
  echo "Examples:"
  echo "  $0 --all                           # Install all skills"
  echo "  $0 --skills=api-designer,code-reviewer  # Install specific skills"
  echo "  $0 --interactive                   # Interactive selection"
  echo "  $0 --platform=gemini --all         # Install all for Gemini"
  echo ""
}

# Parse arguments
for arg in "$@"; do
  case $arg in
    --help|-h)
      show_help
      exit 0
      ;;
    --platform=*)
      PLATFORM="${arg#*=}"
      ;;
    --all)
      BUILD_ALL=true
      ;;
    --skills=*)
      SKILLS="${arg#*=}"
      ;;
    --interactive)
      INTERACTIVE=true
      ;;
    --list)
      LIST_SKILLS=true
      ;;
    *)
      # Skip unknown arguments
      ;;
  esac
done

# Install to .{platform} directory (e.g., .claude, .gemini)
AGENT_DIR="$(pwd)/.${PLATFORM}"
DIST_PLATFORM_DIR="${DIST_DIR}/.${PLATFORM}"

# Handle --list option
if [ "$LIST_SKILLS" = true ]; then
    echo ""
    if [ -f "$BUILD_SCRIPT" ]; then
        if [ "$USE_NODE" = true ]; then
            node "$BUILD_SCRIPT" --list
        else
            "$VENV_DIR/bin/python3" "$BUILD_SCRIPT" --list
        fi
    else
        echo "Error: Build script not found. Cannot list skills."
        exit 1
    fi
    exit 0
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🤖 AI Coding Agents Installer $VERSION                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Target Platform: $PLATFORM"
echo "Install Directory: $AGENT_DIR"
if [ "$USE_NODE" = true ]; then
    echo "Build Tool: Node.js ($(node --version))"
else
    echo "Build Tool: Python ($($VENV_DIR/bin/python3 --version 2>/dev/null || python3 --version))"
fi
echo ""

# Determine build mode
BUILD_OPTS=""
if [ "$BUILD_ALL" = true ]; then
    echo "Mode: Installing ALL skills"
    BUILD_OPTS="--all"
elif [ -n "$SKILLS" ]; then
    echo "Mode: Installing selected skills"
    echo "Skills: $SKILLS"
    BUILD_OPTS="--skills=$SKILLS"
elif [ "$INTERACTIVE" = true ]; then
    echo "Mode: Interactive skill selection"
else
    echo "Mode: Interactive skill selection (default)"
    echo ""
    echo "Tip: Use --all to install all skills, or --skills=list to select specific ones."
fi
echo ""

# --- 1. Setup Environment ---
if [ "$USE_NODE" = true ]; then
    echo "📦 Using Node.js build system..."
    echo "   Build tool: Node.js ($(node --version))"
    
    # Check if node_modules exists
    if [ ! -d "$CLAUDES_CODE_AGENTS_ROOT/node_modules" ]; then
        echo "📦 Installing Node.js dependencies..."
        cd "$CLAUDES_CODE_AGENTS_ROOT"
        npm install
        if [ $? -ne 0 ]; then
            echo "❌ Error: Failed to install Node.js dependencies."
            exit 1
        fi
    fi
else
    echo "📦 Using Python build system..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Error: python3 could not be found."
        exit 1
    fi

    if [ ! -d "$VENV_DIR" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi

    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "📦 Installing Python dependencies..."
        "$VENV_DIR/bin/pip" install -q -r "$REQUIREMENTS_FILE"
        if [ $? -ne 0 ]; then
            echo "⚠️  Warning: Failed to install some requirements."
        fi
    fi
fi

# --- 2. Run build script ---
if [ -f "$BUILD_SCRIPT" ]; then
    echo ""
    echo "🔨 Building skills for $PLATFORM..."
    echo "────────────────────────────────────────"
    
    if [ "$USE_NODE" = true ]; then
        node "$BUILD_SCRIPT" --platform="$PLATFORM" $BUILD_OPTS
    else
        "$VENV_DIR/bin/python3" "$BUILD_SCRIPT" --platform="$PLATFORM" $BUILD_OPTS
    fi
    
    BUILD_STATUS=$?
    echo "────────────────────────────────────────"
    
    if [ $BUILD_STATUS -ne 0 ]; then
        echo ""
        echo "❌ Build failed. Aborting installation."
        exit 1
    fi
else
    echo "❌ Error: Build script not found at $BUILD_SCRIPT"
    exit 1
fi

# --- 3. Verify dist directory ---
if [ ! -d "$DIST_PLATFORM_DIR" ]; then
    echo "❌ Error: Distribution directory not found: $DIST_PLATFORM_DIR"
    exit 1
fi

# Count skills being installed
SKILL_COUNT=$(find "$DIST_PLATFORM_DIR/skills" -name "SKILL.md" | wc -l)
echo ""
echo "📦 Packaging $SKILL_COUNT skills..."


# --- 4. Install the skills ---
echo ""
echo "📥 Installing skills to $AGENT_DIR..."

# Ensure the target directory exists
mkdir -p "$AGENT_DIR"

# Copy skills from dist to target
if [ -d "$DIST_PLATFORM_DIR/skills" ]; then
    # Create skills directory if it doesn't exist
    mkdir -p "$AGENT_DIR/skills"
    
    # Copy each skill
    for skill_dir in "$DIST_PLATFORM_DIR/skills"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            cp -r "$skill_dir" "$AGENT_DIR/skills/"
        fi
    done
fi

# Copy platform configuration file (CLAUDE.md, GEMINI.md, etc.)
cp "$DIST_PLATFORM_DIR"/*.md "$AGENT_DIR/" 2>/dev/null || true

# --- 5. Summary ---
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ INSTALLATION COMPLETE!                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Installed to: $AGENT_DIR"
echo "🎯 Platform: $PLATFORM"
echo "🔧 Skills installed: $SKILL_COUNT"
echo ""
echo "Next steps:"
echo "   1. Restart your IDE/editor"
echo "   2. Claude Code will automatically detect the new skills"
echo "   3. Use a skill by typing /skill-name or mentioning it"
echo ""
echo "💡 Tip: Run with --list to see all available skills"
echo ""
