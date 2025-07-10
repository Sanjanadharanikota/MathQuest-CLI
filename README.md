# MathQuest-CLI
# 🎯 MathQuest

**MathQuest** is a Python-based interactive terminal game that helps you practice arithmetic skills in a fun, fast, and intelligent way. With support for multiple operations, difficulty levels, a timed challenge mode, and visual performance tracking, MathQuest makes math practice engaging and measurable!

Whether you're a student brushing up your basics, a developer trying to keep your brain sharp, or an educator looking for a simple CLI-based tool — **MathQuest** is for you!

---

## 📌 Key Features

### 🔢 Multiple Math Operations
- Addition ➕
- Subtraction ➖
- Multiplication ✖️
- Division ➗

### 📈 Real-Time Performance Tracking
- Score counter
- Streak system (with auto difficulty suggestion)
- Detailed statistics: accuracy, average response time, etc.
- Streak encouragement messages

### 🧠 Adaptive Learning
- Automatically adjusts difficulty based on recent answers
- Encourages improvement with feedback and tips

### ⏱️ Timed Challenge Mode
- Solve as many problems as possible in 60 seconds
- Displays accuracy and speed at the end

### 📊 Visual Performance Graphs
- Accuracy trends over time
- Response time graph
- Pie chart of correct vs incorrect answers

### ⚙️ Customization Options
- Change operations anytime
- Choose from 1-digit to 3-digit problems or mixed difficulty
- Easy to use command-line interface

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.6 or higher
- `matplotlib` for graphing:

Install using pip:
```bash
pip install matplotlib

## 🕹️ How to Play 

When the game starts, you will be presented with randomly generated math problems.

You can answer directly or use commands at any time:

| Command | Description                     |
|---------|---------------------------------|
| `x`     | Exit the game                   |
| `m`     | Change operation type           |
| `n`     | Change number size (difficulty) |
| `s`     | Show current statistics         |
| `g`     | Show performance graphs         |
| `t`     | Start timed challenge mode      |

---

<h3> 📊 Performance Graphs</h3>

After solving several problems, you can type `g` to view:

- **Accuracy Over Time** – Rolling window of your correctness
- **Response Time Plot** – How fast you're solving problems
- **Correct vs Incorrect Pie Chart** – For quick review

These graphs help you visually track your learning and improvement.

