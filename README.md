# Connect-4 Intelligent Agent

This repository contains the implementation of **`Policy`**, an AI agent built for the "Connect-4 Challenge" in the *Foundations of Artificial Intelligence* course (2025.2) at Universidad de La Sabana.

## 🧠 Agent Strategy

The agent uses a **hybrid architecture** that combines adversarial search with reinforcement learning to deliver robust performance from the very first game:

1. **Search engine:** **Minimax with Alpha-Beta pruning** and dynamic depth (`depth=4`) for tactical reasoning.
2. **Positional heuristic:** Mathematical evaluation based on center control and 4-token windows to guide the search at unknown leaf nodes.
3. **Persistence (Q-Learning):** A **Q-Table** that lets the agent "remember" visited states and learn from previous games (*self-play*).
4. **Reactive defense:** Emergency blocking logic to avoid immediate losses before starting the deep search.

## 📂 Project Structure

```text
.
├── groups/
│   └── GroupC/
│       ├── policy.py          # Agent source code (Policy)
│       └── train/
│           └── q_table.pkl    # Learned knowledge (persistence)
├── connect4/                  # Core game logic (environment)
├── entrega.ipynb              # Validation, training and plotting notebook
└── README.md                  # This file
```

## 🚀 Installation & Usage

1. Clone this repository:
```bash
git clone https://github.com/Gemu03/connect4
cd connect4
```

2. Install the required dependencies:
```bash
pip install numpy matplotlib tqdm notebook
```

## 🛠️ Tech Stack

Python · NumPy · Minimax + Alpha-Beta pruning · Q-Learning · Jupyter Notebook

## 📖 Documentation

The full project documentation is in `entrega.ipynb`, which details the implementation, tests, and results obtained by the agent.

## 🎤 Presentation

The project presentation is available here: [Connect-4 Presentation](https://docs.google.com/presentation/d/1v4qAmhsMKwYHcfxli3EaFQX9k_RKwrynFF7ure36CtU/edit?usp=sharing)
