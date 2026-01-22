# Gemini Core

The standard foundation for AI-native development projects.
Contains the **Rules of Engagement (`GEMINI.md`)** and **Agent Skills (`.agent/`)**.

## Directory Structure
- **.agent/**: Agent skills and workflows (The "Brain").
- **templates/**: Language-specific rule sets.
    - `GEMINI.md.node`: For Node.js / TypeScript projects.
    - `GEMINI.md.python`: For Python projects.
- **scripts/**: Utility scripts (e.g., `setup.sh`).
- **src/**, **docs/**, **tests/**: Standard project structure.

---

## 🤖 For Agents: How to Initialize a New Project

### 1. Clone & Detach (Template Mode)
Use this when starting a completely new project.

1.  **Clone** this repository:
    ```bash
    git clone https://github.com/akkyey-mcp-org/gemini-core <target_project_name>
    ```

2.  **Initialize** with Language Flag:
    ```bash
    cd <target_project_name>
    # For Node.js
    ./scripts/setup.sh --new --lang=node
    # For Python
    ./scripts/setup.sh --new --lang=python
    ```
    *This removes the `.git` folder, runs `git init`, and installs the appropriate `GEMINI.md`.*

---

## 🔧 For Existing Projects (Submodule Mode)

If you are adding standard rules to an existing project:

1.  **Add Submodule**:
    ```bash
    git submodule add https://github.com/akkyey/gemini-core .gemini
    ```

2.  **Setup Links**:
    ```bash
    cd .gemini
    # For Node.js project
    ./scripts/setup.sh --lang=node
    # For Python project
    ./scripts/setup.sh --lang=python
    ```
    *This creates symlinks to the correct template and skills.*

---

## 🔄 Contribution & Feedback Loop (How to Improve)

Standard rules and skills should evolve based on project feedback.

### How to contribute changes back to Core:

1.  **Improve Locally**:
    - Modify the rule or skill within your project (e.g., inside `.gemini/templates/GEMINI.md.python` or `.gemini/.agent/skills/...`).
    - *Note: Since files are symlinked or inside the submodule, you are editing the file in the submodule.*

2.  **Commit to Core**:
    ```bash
    cd .gemini
    git checkout main  # Ensure you are on a branch
    git add .
    git commit -m "feat: improve quality_guard skill coverage logic"
    git push origin main
    ```

3.  **Update Project Reference**:
    ```bash
    cd .. # Back to project root
    git add .gemini
    git commit -m "chore: update gemini-core submodule"
    ```

4.  **Propagate**:
    - Other projects can now run `git submodule update --remote` to receive your improvements.
