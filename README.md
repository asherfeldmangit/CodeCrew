# CodeMonkeys Crew

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%E2%80%93%203.13-blue?logo=python" />
  <img src="https://img.shields.io/github/license/asherfeldmangit/CodeCrew" />
  <img src="https://img.shields.io/github/actions/workflow/status/asherfeldmangit/CodeCrew/ci.yml?label=CI" />
</p>

> **Multi-agent software engineering on autopilot** — powered by [crewAI](https://crewai.com) & OpenAI.

---

## ✨ Highlights

• **Hierarchical multi-agent crew** (backend, frontend, QA, architect & engineering lead).  
• **Event-driven _Flow_ orchestration** with per-task feedback loops (design → code → review → fixes → QA).  
• **Long-, short- & entity-memory** via vector DB (Chroma) and SQLite LTM.  
• **Zero-config developer experience** — `crewai run` boots a full AI team that ships production-ready code.  
• **Utility DevOps agent** materialises monolithic artefacts into real source files on disk.

---

## 📖 Table of Contents
1. [Quick Start](#-quick-start)  
2. [Workflow Deep-Dive](#-workflow-deep-dive)  
3. [Project Structure](#-project-structure)  
4. [Architecture Diagram](#-architecture-diagram)  
5. [Configuration](#-configuration)  
6. [Contributing](#-contributing)  
7. [License](#-license)

---

## 🚀 Quick Start

```bash
# 1️⃣ Install uv (the ultra-fast Python package manager)
pip install uv

# 2️⃣ Install dependencies & lock versions
crewai install            # installs from pyproject + uv.lock

# 3️⃣ Add your OpenAI key
cp .env.example .env && echo "OPENAI_API_KEY=sk-..." >> .env

# 4️⃣ Spin up your AI engineering team 🐒
crewai run
```

The crew will ask for *requirements*, *project name* & *main class* then:
1. Generate a **design doc**.  
2. Break it down into **atomic tasks**.  
3. Implement backend → review → fix → **unit tests**.  
4. Implement frontend → review → fix → **E2E tests**.  
5. Perform **dependency audit** & materialise artefacts.

Open the generated code under `output/<PROJECT>/` — ready to run!

---

## 🔍 Workflow Deep-Dive

Below is the default pipeline executed by `EngineeringFlow`.
Steps with the same background colour run in sequence, arrows denote dependencies.

```mermaid
graph TD
    subgraph Design
        A["Design 📄\narchitect_agent"]
        B["Task Breakdown 🗂\ntask_breaker"]
    end
    subgraph Backend
        C["Backend Code 💾\nbackend_engineer"]
        D["Code Review 🔍\narchitect_agent"]
        E["Fix Comments 🛠\nbackend_engineer"]
        F["Unit Tests ✅\ntest_engineer"]
    end
    subgraph Frontend
        G["Frontend UI 💻\nfrontend_engineer"]
        H["UI Review 🔍\narchitect_agent"]
        I["Fix Comments 🛠\nfrontend_engineer"]
        J["Dependency Audit 📦\narchitect_agent"]
    end
    subgraph QA
        K["End-to-End Tests 🚦\ntest_engineer"]
    end
    A --> B --> C --> D --> E --> F
    F --> G --> H --> I --> J --> K
```

Each **code→review→fix** trio can iterate up to *three* rounds if blockers remain.

---

## 🗂 Project Structure

```text
CodeCrew/
├─ src/
│  └─ code_monkeys/
│     ├─ config/         # YAML config for agents & tasks
│     ├─ flows/          # EngineeringFlow orchestrator
│     ├─ tools/          # (Empty) custom tools namespace
│     └─ crew.py         # CrewBuilder & agents definition
├─ output/               # Generated code & reports (git-ignored)
├─ memory/               # Vector & LTM databases (git-ignored)
├─ README.md             # <- you are here
└─ pyproject.toml        # Package metadata & dependency pins
```

---

## ⚙️ Configuration

* **Agents:** customise roles & goals in `src/code_monkeys/config/agents.yaml`.  
* **Tasks:** tweak or reorder steps in `src/code_monkeys/config/tasks.yaml`.  
* **Flows:** extend `EngineeringFlow` (e.g., add Slack notifications) in `src/code_monkeys/flows/`.

---

## 🤝 Contributing

1. Fork the repo and create your feature branch (`git checkout -b feat/my-feature`).  
2. Commit your changes with conventional commits.  
3. Ensure `pytest` passes & `ruff` lints (`uv run lint`).  
4. Open a PR — we ❤️ new contributors!

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

## Understanding Your Crew

The code_monkeys Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the CodeMonkeys Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
