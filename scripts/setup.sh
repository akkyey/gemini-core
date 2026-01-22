#!/bin/bash
set -e

# setup.sh - Gemini Core Setup Script
# Usage:
#   ./setup.sh --lang=node|python  : Link GEMINI.md (template) and .agent (Submodule mode)
#   ./setup.sh --new --lang=...    : Initialize fresh project (Template mode)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$(pwd)"
LANG_MODE=""
NEW_MODE=false

# Argument Parsing
for arg in "$@"; do
    case $arg in
        --new)
            NEW_MODE=true
            ;;
        --lang=*)
            LANG_MODE="${arg#*=}"
            ;;
        *)
            # unknown option
            ;;
    esac
done

echo "🤖 Gemini Core Setup..."

# Function to link global config based on language
link_gemini() {
    echo "🔗 Linking GEMINI.md..."
    
    if [ -z "$LANG_MODE" ]; then
        echo "   ⚠️  No language specified. Defaulting to 'node' rules."
        LANG_MODE="node"
    fi

    TEMPLATE_FILE="$ROOT_DIR/templates/GEMINI.md.$LANG_MODE"

    if [ -f "$TEMPLATE_FILE" ]; then
        # Force symlink creation
        ln -sf "$TEMPLATE_FILE" "$TARGET_DIR/GEMINI.md"
        echo "   ✅ Linked: $TARGET_DIR/GEMINI.md -> $TEMPLATE_FILE ($LANG_MODE)"
    else
        echo "   ❌ Error: Template not found for lang='$LANG_MODE' at $TEMPLATE_FILE"
        echo "      Available templates: $(ls $ROOT_DIR/templates/)"
        exit 1
    fi
}

# Function to link .agent (Hybrid Mode Support)
# If .agent exists as a dir (not symlink), we assume it's a project with local memories.
# In that case, we link skills INSIDE it.
link_agent() {
    # Function to link individual skills (Overlay Mode)
    # This allows the project to have its own local skills alongside shared ones.
    if [ ! -d "$TARGET_DIR/.agent/skills" ]; then
        mkdir -p "$TARGET_DIR/.agent/skills"
    fi

    # Check if target is a symlink (Legacy Mode) - if so, convert to directory
    if [ -L "$TARGET_DIR/.agent/skills" ]; then
        echo "   🔄 Converting '.agent/skills' from symlink to directory (for Overlay support)..."
        rm "$TARGET_DIR/.agent/skills"
        mkdir -p "$TARGET_DIR/.agent/skills"
    fi

    echo "   🔗 Linking Core Skills..."
    for skill_path in "$CORE_SKILLS"/*; do
        if [ -d "$skill_path" ]; then
            skill_name=$(basename "$skill_path")
            target_skill="$TARGET_DIR/.agent/skills/$skill_name"
            
            # Link only if not explicitly overridden (if a real dir exists, keep it)
            if [ ! -e "$target_skill" ]; then
                ln -sf "$skill_path" "$target_skill"
                # echo "      Linked: $skill_name"
            elif [ -L "$target_skill" ]; then
                # Update link if it exists
                ln -sf "$skill_path" "$target_skill"
            else
                echo "      ⚠️  Skipping shared skill '$skill_name' (Local override detected)"
            fi
        fi
    done
    echo "   ✅ Core skills linked. You can now add local skills to .agent/skills/"
}

# Execution
if [ "$NEW_MODE" = true ]; then
    echo "🚀 Initializing NEW project from template..."
    
    if [ -d "$TARGET_DIR/.git" ]; then
        echo "   🗑️  Removing existing .git history..."
        rm -rf "$TARGET_DIR/.git"
    fi
    
    echo "   ✨ Initializing fresh Git repository..."
    git init
    
    # In template mode, we might want to COPY the files instead of link?
    # For now, keeping links implies dependence on the template folder location which is weird if we detached.
    # Ideally: If clone --new, we probably want to COPY the content of the selected template to GEMINI.md
    
    TEMPLATE_FILE="$ROOT_DIR/templates/GEMINI.md.$LANG_MODE"
    cp "$TEMPLATE_FILE" "$TARGET_DIR/GEMINI.md"
    cp -r "$ROOT_DIR/.agent" "$TARGET_DIR/.agent"
    
    echo "   ✅ Copied assets (Detached Mode). Ready to commit."

else
    # Submodule Mode
    link_gemini
    link_agent
    echo "✅ Setup complete for Submodule mode."
fi
