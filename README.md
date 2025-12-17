# 🎮 Ultimate Tic-Tac-Toe AI Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Algorithm](https://img.shields.io/badge/Algorithm-Minimax%20%2B%20Alpha--Beta-green)

A high-performance, strategic game agent for **Ultimate Tic-Tac-Toe**, engineered to handle high branching factors using adversarial search algorithms. This project features a modular game engine, multiple difficulty tiers, and an interactive web dashboard.

---

## 📖 Table of Contents
- [About the Game](#-about-the-game)
- [Key Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Installation & Usage](#-installation--usage)
- [Project Structure](#-project-structure)
- [Algorithm Details](#-algorithm-details)

---

## 🧠 About the Game
**Ultimate Tic-Tac-Toe** is a recursive variation of the classic game. It is played on a 9x9 grid, divided into nine 3x3 local boards.
* **The Constraint:** The cell you play in determines which local board your opponent must play in next.
* **The Goal:** Win 3 local boards in a row (horizontally, vertically, or diagonally) to win the global board.
* **Complexity:** The branching factor is significantly higher than standard Tic-Tac-Toe (~81 moves initially), requiring efficient state-space search optimization.

---

## ✨ Key Features
* **🤖 Advanced AI Agent:** Implements **Minimax with Alpha-Beta Pruning** to explore decision trees efficiently (Depth 6+).
* **⚡ Optimized Heuristics:** Custom evaluation functions quantify positional advantages, sub-grid control, and center-board dominance.
* **📊 Interactive Dashboard:** A modern web UI built with **Streamlit** featuring valid-move highlighting and real-time game status.
* **⚔️ Multi-Tier Difficulty:**
    * **Easy:** Stochastic/Random agent.
    * **Medium:** Greedy heuristic agent (Baseline).
    * **Hard:** Depth-limited Minimax agent with pruning.
* **🧪 Modular Engine:** Decoupled game logic (`src/ultimate_ttt_engine.py`) from AI strategies, facilitating A/B testing and benchmarking.

---

## 🛠 Technical Architecture
The project follows a modular software engineering pattern:

* **Game Engine:** Handles state validation, macro-board constraints, and win condition checking.
* **AI Core:** Stateless bot functions (`play(board, prev_move, player)`) that return optimal moves.
* **Frontend:** A reactive Streamlit app that maintains session state and handles user interaction.

---

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x
* Pip

### 1. Clone the Repository
```bash
git clone https://github.com/Parth7234/UltimateTTT.git
cd UltimateTTT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Web Interface (Recommended)
Launch the interactive game dashboard:

```bash
streamlit run app.py
```

### 4. Run CLI Version
To play in the terminal without a GUI:

```bash
python scripts/Player_vs_bot.py
```

## 📂 Project Structure

```bash

UltimateTTT/
├── app.py                     # Main Streamlit Web Application
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git configuration
│
├── src/                       # Source Code Package
│   ├── __init__.py
│   ├── ultimate_ttt_engine.py # Core Game Logic & Rules
│   ├── game.py                # Bot vs Bot Simulation Runner
│   ├── minimax_bot.py         # HARD Bot (Alpha-Beta Pruning)
│   ├── ai.py                  # MEDIUM Bot (Baseline Heuristic)
│   └── random_bot.py          # EASY Bot (Stochastic)
│
├── scripts/                   # Executable Scripts
│   └── Player_vs_bot.py       # Terminal-based gameplay
│
├── legacy/                    # Reference implementations
│   └── reference_tictactoe.c  # Original logic in C
│
└── docs/                      # Documentation
    └── dev_notes.txt          # Development log and ideas

```

## 🔬 **Algorithm Details**

### **The Minimax Agent (`minimax_bot.py`)**
The **Hard** difficulty agent uses a **recursive Minimax algorithm** enhanced with **Alpha-Beta Pruning** to efficiently reduce the search space by eliminating irrelevant branches in the game tree.

---

### **Heuristic Evaluation Function**
Because exploring the complete game tree of **Ultimate Tic-Tac-Toe** is computationally infeasible in real time, the AI evaluates **non-terminal states** using a weighted heuristic based on:

- **Global Board Control**  
  Higher rewards for securing **center** and **corner macro-boards**

- **Local Board Advantage**  
  Positional scoring based on **piece dominance** within active sub-grids

- **Terminal State Detection**  
  Immediate high-magnitude scores for **win / loss conditions**

---

### **Performance Notes**
- **Average Decision Time:** `< 2 seconds` (Depth **4–6**)  
- **Baseline Comparison:**  
  Consistently outperforms the **Greedy Baseline (`ai.py`)** by prioritizing **long-term macro-board strategy** over short-term local wins

---

## 🤝 **Contributing**
Contributions are **welcome and encouraged**!  
Please feel free to **open an issue** or **submit a pull request** for improvements or enhancements.

---

## 📜 **License**
This project is **open-source** and distributed under the **MIT License**.
