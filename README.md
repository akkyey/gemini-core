# Gemini Core

The standard foundation for AI-native development projects.
Contains the **Rules of Engagement (`GEMINI.md`)** and **Agent Skills (`.agent/`)**.

## Directory Structure
- **.agent/**: Agent skills and workflows (The "Brain").
- **scripts/**: Utility scripts (e.g., `setup.sh`).
- **src/**, **docs/**, **tests/**: Standard project structure.
- **GEMINI.md**: Single Source of Truth for project rules.

---

## 🤖 For Agents: How to Initialize a New Project

If a user asks you to "create a new project" or "scaffold a project" using this core, follow these exact steps:

### 1. Clone & Detach (Template Mode)
Use this when starting a completely new project.

1.  **Clone** this repository to the target directory:
    ```bash
    git clone https://github.com/akkyey-mcp-org/gemini-core <target_project_name>
    ```

2.  **Detach** from core history and initialize:
    ```bash
    cd <target_project_name>
    ./scripts/setup.sh --new
    ```
    *This removes the `.git` folder and runs `git init`, making it a fresh repository.*

3.  **Verify**:
    - Check that `.git` is fresh (no commit history).
    - Check that `GEMINI.md` and `.agent/` exist.

---

## 🔧 For Existing Projects (Submodule Mode)

If you are adding standard rules to an existing project:

1.  **Add Submodule**:
    ```bash
    git submodule add https://github.com/akkyey-mcp-org/gemini-core .gemini
    ```

2.  **Setup Links**:
    ```bash
    cd .gemini
    ./scripts/setup.sh
    ```
    *This creates symlinks from the project root to `.gemini/GEMINI.md` and `.gemini/.agent`.*
