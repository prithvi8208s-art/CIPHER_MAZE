# 🔐 Cipher Maze

> A cryptography-themed maze game built with Python and Tkinter, combining classical ciphers, recursive maze generation, and BFS pathfinding.

## 🎮 About the Project

**Cipher Maze** is an interactive desktop puzzle game where the player must decrypt an encrypted message and then escape through a randomly generated maze.

The project combines multiple Computer Science concepts into one game:

- 🔑 Classical Cryptography
- 🧩 Recursive Backtracking
- 🧭 Breadth-First Search (BFS)
- 🖥️ Tkinter GUI
- 🎯 Pathfinding and maze navigation

---

## ✨ Features

- 🔐 Caesar Cipher
- 🔄 Atbash Cipher
- 🔁 ROT-13 Cipher
- 🧩 Randomly generated mazes
- 🧠 Recursive Backtracking maze generation
- 🧭 BFS-based pathfinding
- ⚡ Auto-Solve feature
- ⌨️ Arrow Keys and WASD controls
- ⏱️ 90-second countdown timer
- 🏆 Score system
- 📈 Level and move tracking
- 🎨 Neon / holographic themed interface

---

## 🕹️ How to Play

### Phase 1 — Decrypt the Cipher

Each level gives you an encrypted message.

Identify the cipher and enter the correct decrypted message.

The game currently includes:

1. **Caesar Cipher**
2. **Atbash Cipher**
3. **ROT-13**

### Phase 2 — Unlock the Maze

After successfully decrypting the message, the maze path is unlocked.

The game uses **Breadth-First Search (BFS)** to calculate the shortest path from the starting point to the exit.


### Phase 3 — Escape

Navigate through the maze using:

- **Arrow Keys**
- **W A S D**

Reach the ⭐ exit before the timer runs out.

You can also use **Auto-Solve** to watch the BFS path being followed automatically.
THEN YOU WILL BE MOVED TO LEVEL 2
---

## 📸 Screenshots

### 🎮 Main Game

![Cipher Maze Main Game](<MAIN GAME SCREEN.png>)

### 🔐 Maze After Decrypting

![Maze After Decrypting](<MAZE AFTER DECRYPTING.png>)

### 🏆 Maze Solved

![Maze Solved](<MAZE SOLVED.png>)

## 🧠 Algorithms Used

### Recursive Backtracking

Recursive Backtracking is used to generate the maze.

The algorithm:

1. Starts from the first cell.
2. Selects a random unvisited neighboring cell.
3. Removes the wall between the cells.
4. Recursively continues through the maze.
5. Backtracks when there are no unvisited neighbors.

This creates a different randomized maze whenever a new maze is generated.

### Breadth-First Search (BFS)

BFS is used to find a path from the starting position to the exit.

```text
Start → Maze → Exit
```

Because every movement has equal cost, BFS finds the shortest path from the starting position to the exit.

---

## 🔐 Cryptography

The project demonstrates three classical cipher techniques.

### Caesar Cipher

Letters are shifted by 3 positions.

```text
D → A
E → B
F → C
```

### Atbash Cipher

The alphabet is mirrored.

```text
A ↔ Z
B ↔ Y
C ↔ X
```

### ROT-13

Each letter is rotated by 13 positions.

```text
A → N
B → O
C → P
