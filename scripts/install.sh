#!/bin/bash

# This script is a conceptual example of a more robust installation process.
# It assumes that a `dist/` directory has been created by the build script
# and that its contents have been packaged into a release artifact.

# For local testing, we'll package the `dist` directory ourselves.

# Determine the directory where the install.sh script is located
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
CLAUDES_CODE_AGENTS_ROOT="$(dirname "$SCRIPT_DIR")"

VERSION="v1.0.0-dev"
DIST_DIR="$CLAUDES_CODE_AGENTS_ROOT/dist"
BUILD_SCRIPT="$CLAUDES_CODE_AGENTS_ROOT/scripts/build.py"
RELEASE_ARCHIVE="agents.tar.gz"

# Default platform
PLATFORM="claude"
FRAMEWORKS=""
VENV_DIR="$CLAUDES_CODE_AGENTS_ROOT/venv"
REQUIREMENTS_FILE="$CLAUDES_CODE_AGENTS_ROOT/requirements.txt"

# Parse arguments
for arg in "$@"; do
  case $arg in
    --platform=*)
      PLATFORM="${arg#*=}"
      ;;
    --frameworks=*)
      FRAMEWORKS="${arg#*=}"
      ;;
    *)
      # Assume first non-flag argument is platform if not set
      if [[ "$arg" != --* ]] && [ -z "$PLATFORM_SET" ]; then
          PLATFORM="$arg"
          PLATFORM_SET=true
      fi
      ;;
  esac
done

# Install to .{platform} directory (e.g., .claude, .gemini)
AGENT_DIR="$(pwd)/.${PLATFORM}"

DIST_AGENTS_DIR="${DIST_DIR}/.${PLATFORM}"


echo "--- AI Agents Installer ---"
echo "Target Platform: $PLATFORM"
if [ -n "$FRAMEWORKS" ]; then
    echo "Selected Frameworks: $FRAMEWORKS"
else
    echo "Selected Frameworks: All"
fi
echo "Installation Directory: $AGENT_DIR"


# --- 1. Setup Python Environment ---
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

if [ -f "$REQUIREMENTS_FILE" ]; then
    # Quietly install requirements to avoid cluttering output unless there's an error
    "$VENV_DIR/bin/pip" install -q -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to install requirements via pip. Build might fail."
    fi
fi

# --- 2. Run build script to ensure dist is up-to-date ---
if [ -f "$BUILD_SCRIPT" ]; then
    echo "Running build script to generate artifacts for $PLATFORM..."
    # Use the venv python to run the script
    "$VENV_DIR/bin/python3" "$BUILD_SCRIPT" --platform="$PLATFORM"
    if [ $? -ne 0 ]; then
        echo "Build failed. Aborting installation."
        exit 1
    fi
else
    echo "Build script not found. Assuming dist directory is ready."
fi


# --- 2. Check if dist directory exists ---
if [ ! -d "$DIST_AGENTS_DIR" ]; then
    echo "Error: The '${DIST_AGENTS_DIR}' directory was not found after build."
    echo "Please check the build process for platform: $PLATFORM"
    exit 1
fi

# --- 3. Create a local release artifact from the dist directory ---
echo "Creating local release artifact: $RELEASE_ARCHIVE from $DIST_AGENTS_DIR..."

# If frameworks are specified, we need to filter what we package
if [ -n "$FRAMEWORKS" ]; then
    # Create a temporary directory for filtering
    TEMP_DIST_DIR=$(mktemp -d)

    # Copy base directories (agents, rules)
    cp -r "$DIST_AGENTS_DIR/agents" "$TEMP_DIST_DIR/" 2>/dev/null || true
    cp -r "$DIST_AGENTS_DIR/rules" "$TEMP_DIST_DIR/" 2>/dev/null || true

    # Handle skills specially
    mkdir -p "$TEMP_DIST_DIR/skills"

    # Convert comma-separated string to array
    IFS=',' read -ra ADDR <<< "$FRAMEWORKS"
    for framework in "${ADDR[@]}"; do
        # Trim whitespace
        framework=$(echo "$framework" | xargs)

        # Copy matching skills
        # We look for skills that match the framework name in their path or filename
        # This assumes skills are organized like skills/react/component.md or skills/react-component.md

        # Find skills in the source dist that match the framework
        # Note: This is a simple match. Adjust logic if structure is complex.
        find "$DIST_AGENTS_DIR/skills" -name "*${framework}*" -exec cp -r {} "$TEMP_DIST_DIR/skills/" \;
    done

    # Also copy CLAUDE.md (or equivalent)
    cp "$DIST_AGENTS_DIR"/*.md "$TEMP_DIST_DIR/" 2>/dev/null || true

    # Create archive from temp dir
    tar -czf "$RELEASE_ARCHIVE" -C "$TEMP_DIST_DIR" .
    rm -rf "$TEMP_DIST_DIR"
else
    # Package everything
    tar -czf "$RELEASE_ARCHIVE" -C "$DIST_AGENTS_DIR" .
fi


# --- 4. Install the agents ---
echo "Installing agents to $AGENT_DIR..."

# Ensure the target directory exists
mkdir -p "$AGENT_DIR"

# Unpack the release artifact into the target directory
# The -C flag changes the directory, and we unpack the contents of dist/
tar -xzf "$RELEASE_ARCHIVE" -C "$AGENT_DIR"

# --- 5. Cleanup ---
rm "$RELEASE_ARCHIVE"

echo ""
echo "✅ Installation complete!"
echo "   ${AGENT_DIR} now contains the latest agent definitions for ${PLATFORM}."
echo "   Please restart your IDE for The AI Coding Agent (or relevant AI system) to recognize the new agents."
