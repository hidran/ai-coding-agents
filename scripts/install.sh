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
VENV_DIR="$CLAUDES_CODE_AGENTS_ROOT/venv"
REQUIREMENTS_FILE="$CLAUDES_CODE_AGENTS_ROOT/requirements.txt"

# Parse arguments
if [ -n "$1" ] && [[ "$1" != --* ]]; then
    PLATFORM="$1"
    shift
fi

for arg in "$@"; do
  case $arg in
    --platform=*)
      PLATFORM="${arg#*=}"
      shift # Remove --platform= from processing
      ;;
    *)
      # Unknown option or argument
      ;;
  esac
done

AGENT_DIR="$(pwd)/.${PLATFORM}/agents"
DIST_AGENTS_DIR="${DIST_DIR}/${PLATFORM}_agents"


echo "--- AI Agents Installer ---"
echo "Target Platform: $PLATFORM"
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
tar -czf "$RELEASE_ARCHIVE" -C "$DIST_AGENTS_DIR" .

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
