#!/bin/bash
set -e

# setup.sh - Gemini Core Setup Script
# Usage: 
#   ./setup.sh        : Link GEMINI.md and .agent (Submodule mode)
#   ./setup.sh --new  : Initialize fresh project (Template mode)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$(pwd)"

echo "🤖 Gemini Core Setup..."

# Function to link global config
link_gemini() {
    echo "🔗 Linking GEMINI.md..."
    if [ -f "$ROOT_DIR/GEMINI.md" ]; then
        ln -sf "$ROOT_DIR/GEMINI.md" "$TARGET_DIR/GEMINI.md"
        echo "   ✅ Linked: $TARGET_DIR/GEMINI.md"
    else
        echo "   ❌ Error: GEMINI.md not found in $ROOT_DIR"
    fi
}

# Function to link .agent (if pure submodule mode, though often it's already there)
# If gemini-core is a submodule at .gemini/, then .agent is at .gemini/.agent
# We might want to link .agent to root if tools expect it there.
# CURRENTLY: tools look for .agent in CWD (Project Root).
# So if .gemini/ is the submodule, we need to link .gemini/.agent to ./.agent
link_agent() {
    echo "🔗 Linking .agent skills..."
    if [ -d "$ROOT_DIR/.agent" ]; then
        # Check if .agent exists and is not a symlink
        if [ -d "$TARGET_DIR/.agent" ] && [ ! -L "$TARGET_DIR/.agent" ]; then
             echo "   ⚠️  Warning: Local .agent directory exists. Skipping link."
        else
             ln -sf "$ROOT_DIR/.agent" "$TARGET_DIR/.agent"
             echo "   ✅ Linked: $TARGET_DIR/.agent -> $ROOT_DIR/.agent"
        fi
    fi
}

# Mode: New Project Initialization
if [ "$1" == "--new" ]; then
    echo "🚀 Initializing NEW project from template..."
    
    # 1. Remove Git history
    if [ -d "$TARGET_DIR/.git" ]; then
        echo "   🗑️  Removing existing .git history..."
        rm -rf "$TARGET_DIR/.git"
    fi
    
    # 2. Re-initialize Git
    echo "   ✨ Initializing fresh Git repository..."
    git init
    
    # 3. Copy assets instead of linking (Detach)
    # Actually, user might still want links if they want to update core easily?
    # No, 'clone as template' usually implies 'detach'.
    # But wait, if they detach, they lose updates.
    # RECOMMENDATION: Even new projects should use submodule if possible, 
    # BUT 'template' implies a starting point.
    # Let's keep it simple: --new creates a fresh repo but keeps the files AS IS (physical copies).
    
    echo "   ✅ Project initialized. Ready to 'git add .' and 'git commit'."
    echo "   (Note: 'GEMINI.md' and '.agent' are now independent copies)"

else
    # Mode: Submodule Setup (default)
    # Assumes run from project root, with gemini-core as submodule in $ROOT_DIR (e.g. .gemini/)
    
    link_gemini
    link_agent
    
    echo "✅ Setup complete for Submodule mode."
fi
