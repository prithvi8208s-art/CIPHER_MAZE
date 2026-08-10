"""
CIPHER MAZE — Python Tkinter Version
=====================================
Project by: [Your Name]
Course: Computer Science — The Apollo University

CONCEPTS USED:
  - Recursive Backtracking (maze generation)
  - BFS Breadth-First Search (pathfinding)
  - Classical Ciphers: Caesar, Atbash, ROT-13
  - Tkinter GUI with Canvas drawing
"""

import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

# ─────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────
COLS       = 17       # must be odd
ROWS       = 17       # must be odd
CELL_SIZE  = 28       # pixels per cell
WALL_COLOR = "#6a0dad"
PATH_COLOR = "#1a0030"
GLOW_COLOR = "#cc00ff"
SOLVE_COLOR= "#00ffcc"
PLAYER_COL = "#ffffff"
EXIT_COLOR = "#ffdd00"
BG_COLOR   = "#07000f"


# ─────────────────────────────────────────
#  CIPHER FUNCTIONS
# ─────────────────────────────────────────

def caesar_decode(text):
    """Shift each letter BACK by 3. D→A, E→B, etc."""
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') - 3) % 26 + ord('A'))
        else:
            result += ch
    return result


def atbash_decode(text):
    """Mirror the alphabet. A↔Z, B↔Y, C↔X."""
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr(ord('Z') - (ord(ch) - ord('A')))
        else:
            result += ch
    return result


def rot13_decode(text):
    """Rotate each letter by 13 positions."""
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') + 13) % 26 + ord('A'))
        else:
            result += ch
    return result


# ─────────────────────────────────────────
#  MAZE GENERATION — Recursive Backtracking
# ─────────────────────────────────────────

def generate_maze(rows, cols):
    """
    Returns a 2D grid where each cell is a dict:
      { 'top': bool, 'right': bool, 'bottom': bool, 'left': bool }
    True = wall exists, False = wall removed (passage open)
    """
    # Initialise every cell with all 4 walls
    grid = [[{'top': True, 'right': True, 'bottom': True, 'left': True}
             for _ in range(cols)] for _ in range(rows)]

    visited = [[False] * cols for _ in range(rows)]

    def carve(r, c):
        visited[r][c] = True
        # Shuffle directions for random maze
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check bounds and unvisited
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                # Remove wall between current and neighbour
                wall_r = r + dr // 2   # middle cell row
                wall_c = c + dc // 2   # middle cell col

                # Determine which wall to remove based on direction
                if dr == -2:   # moving UP
                    grid[r][c]['top']         = False
                    grid[wall_r][wall_c]['top']    = False
                    grid[wall_r][wall_c]['bottom'] = False
                    grid[nr][nc]['bottom']    = False
                elif dr == 2:  # moving DOWN
                    grid[r][c]['bottom']      = False
                    grid[wall_r][wall_c]['top']    = False
                    grid[wall_r][wall_c]['bottom'] = False
                    grid[nr][nc]['top']        = False
                elif dc == -2: # moving LEFT
                    grid[r][c]['left']        = False
                    grid[wall_r][wall_c]['left']   = False
                    grid[wall_r][wall_c]['right']  = False
                    grid[nr][nc]['right']      = False
                elif dc == 2:  # moving RIGHT
                    grid[r][c]['right']       = False
                    grid[wall_r][wall_c]['left']   = False
                    grid[wall_r][wall_c]['right']  = False
                    grid[nr][nc]['left']       = False

                carve(nr, nc)  # recurse into neighbour

    carve(0, 0)
    return grid


# ─────────────────────────────────────────
#  PATHFINDING — Breadth First Search (BFS)
# ─────────────────────────────────────────

def solve_maze_bfs(grid, rows, cols):
    """
    BFS from (0,0) to (rows-1, cols-1).
    Returns list of (row, col) tuples = optimal path.
    """
    start = (0, 0)
    end   = (rows - 1, cols - 1)

    queue   = deque()
    queue.append(start)
    visited = {start: None}   # maps cell → parent cell

    direction_map = {
        'top':    (-1,  0),
        'right':  ( 0,  1),
        'bottom': ( 1,  0),
        'left':   ( 0, -1),
    }
    opposite = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}

    while queue:
        r, c = queue.popleft()

        if (r, c) == end:
            # Reconstruct path by walking back through parents
            path = []
            cur  = end
            while cur is not None:
                path.append(cur)
                cur = visited[cur]
            path.reverse()
            return path

        for direction, (dr, dc) in direction_map.items():
            # Only move if no wall in that direction
            if not grid[r][c][direction]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited:
                    visited[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return []   # no path found


# ─────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ─────────────────────────────────────────

class CipherMazeApp:

    LEVELS = [
        {
            'cipher':  'DWWDFN DW GDZQ',
            'answer':  'ATTACKATDAWN',
            'algo':    'CAESAR CIPHER',
            'hint':    'Shift each letter BACK by 3.  D→A, W→T, F→C',
            'decode':  caesar_decode,
        },
        {
            'cipher':  'GSVNVVGRMTKLRMG',
            'answer':  'THEMEETINGPOINT',
            'algo':    'ATBASH CIPHER',
            'hint':    'Mirror the alphabet.  A↔Z, B↔Y, C↔X',
            'decode':  atbash_decode,
        },
        {
            'cipher':  'URYYBJGURPBQR',
            'answer':  'FOLLOWTHECODE',
            'algo':    'ROT-13 CIPHER',
            'hint':    'Rotate each letter by 13.  U→H, R→E, Y→L',
            'decode':  rot13_decode,
        },
    ]

    def __init__(self, root):
        self.root  = root
        self.root.title("◈ Cipher Maze — Holographic Prism")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Game state
        self.level       = 0
        self.score       = 0
        self.moves       = 0
        self.time_left   = 90
        self.timer_id    = None
        self.decrypted   = False
        self.maze_solved = False
        self.grid        = []
        self.solution    = []
        self.player      = [0, 0]   # [row, col]
        self.show_path   = False

        self._build_ui()
        self._new_game()

    # ── UI CONSTRUCTION ──────────────────

    def _build_ui(self):
        # ── TOP STATS BAR
        stats_frame = tk.Frame(self.root, bg=BG_COLOR)
        stats_frame.pack(fill='x', padx=10, pady=(10, 4))

        self.lbl_level = self._stat_widget(stats_frame, "LEVEL",   "#ff44dd")
        self.lbl_score = self._stat_widget(stats_frame, "SCORE",   "#00ddff")
        self.lbl_moves = self._stat_widget(stats_frame, "MOVES",   "#bbff44")
        self.lbl_time  = self._stat_widget(stats_frame, "SECONDS", "#ffaa22")

        # ── MAIN CONTENT
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(padx=10, pady=4)

        left  = tk.Frame(main, bg=BG_COLOR)
        left.grid(row=0, column=0, sticky='n', padx=(0, 10))

        right = tk.Frame(main, bg=BG_COLOR)
        right.grid(row=0, column=1, sticky='n')

        # ── LEFT: CIPHER PANEL
        self._panel(left, "◉  PHASE 1 — DECRYPT THE CIPHER", 0)
        self.lbl_algo = tk.Label(left, text="", bg="#1a003a", fg="#cc88ff",
                                  font=("Courier", 9), pady=3, padx=10)
        self.lbl_algo.pack(fill='x', padx=8, pady=(0, 6))

        self.lbl_cipher = tk.Label(left, text="", bg="#04000c", fg="#f0e0ff",
                                    font=("Courier", 14, "bold"),
                                    wraplength=320, justify='center',
                                    pady=10, padx=10, relief='flat')
        self.lbl_cipher.pack(fill='x', padx=8)

        self.lbl_hint = tk.Label(left, text="", bg="#120020", fg="#aa88cc",
                                  font=("Courier", 9), wraplength=320,
                                  justify='left', pady=8, padx=10)
        self.lbl_hint.pack(fill='x', padx=8, pady=(4, 0))

        inp_frame = tk.Frame(left, bg=BG_COLOR)
        inp_frame.pack(fill='x', padx=8, pady=8)
        self.entry = tk.Entry(inp_frame, bg="#04000c", fg="#e0d0ff",
                               insertbackground="#cc88ff",
                               font=("Courier", 11), relief='flat',
                               bd=4, width=22)
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind("<Return>", lambda e: self._check_cipher())
        tk.Button(inp_frame, text="◈ DECRYPT", bg="#7700cc", fg="white",
                  font=("Courier", 9, "bold"), relief='flat',
                  cursor="hand2", command=self._check_cipher).pack(side='left', padx=(6, 0))

        self.lbl_feedback = tk.Label(left, text="", bg=BG_COLOR,
                                      font=("Courier", 9))
        self.lbl_feedback.pack()

        # ── LEFT: PATH PANEL
        self._panel(left, "◎  PHASE 2 — PATH COORDINATES", 1)
        self.lbl_path_info = tk.Label(left, text="Decrypt cipher first.",
                                       bg=BG_COLOR, fg="#446644",
                                       font=("Courier", 9))
        self.lbl_path_info.pack(padx=8, pady=(0, 6))

        btn_frame = tk.Frame(left, bg=BG_COLOR)
        btn_frame.pack(pady=(0, 8))
        self.btn_auto = tk.Button(btn_frame, text="⚡  Auto-Solve", bg="#005577",
                                   fg="white", font=("Courier", 9, "bold"),
                                   relief='flat', cursor="hand2",
                                   state='disabled', command=self._auto_solve)
        self.btn_auto.pack(side='left', padx=4)

        self.btn_next = tk.Button(btn_frame, text="NEXT LEVEL →", bg="#006633",
                                   fg="white", font=("Courier", 9, "bold"),
                                   relief='flat', cursor="hand2",
                                   state='disabled', command=self._next_level)
        self.btn_next.pack(side='left', padx=4)

        # ── LEFT: HOW IT WORKS
        self._panel(left, "◈  HOW IT WORKS", 2)
        steps = [
            ("1·", "#ff88ff", "Receive encrypted spy transmission"),
            ("2·", "#88ffff", "Crack cipher → maze coordinates unlock"),
            ("3·", "#ccff88", "BFS finds the optimal escape route"),
            ("4·", "#ff88cc", "Navigate or auto-solve · escape the prism"),
        ]
        for num, col, txt in steps:
            f = tk.Frame(left, bg=BG_COLOR)
            f.pack(anchor='w', padx=12, pady=1)
            tk.Label(f, text=num, fg=col, bg=BG_COLOR,
                     font=("Courier", 9, "bold")).pack(side='left')
            tk.Label(f, text=" " + txt, fg="#a080c0", bg=BG_COLOR,
                     font=("Courier", 9)).pack(side='left')

        # ── RIGHT: MAZE CANVAS
        self._panel(right, "◎  PHASE 3 — THE HOLOGRAPHIC MAZE", 3)

        self.canvas = tk.Canvas(right,
                                 width=COLS * CELL_SIZE,
                                 height=ROWS * CELL_SIZE,
                                 bg=BG_COLOR, highlightthickness=1,
                                 highlightbackground="#6a0dad")
        self.canvas.pack(padx=8, pady=(0, 8))
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self._on_key)

        tk.Button(right, text="⬡  New Maze", bg="#440088", fg="white",
                  font=("Courier", 9, "bold"), relief='flat',
                  cursor="hand2", command=self._new_game).pack(pady=(0, 10))

        tk.Label(right, text="ARROW KEYS / WASD TO MOVE",
                 bg=BG_COLOR, fg="#3a2060",
                 font=("Courier", 8)).pack(pady=(0, 8))

    def _stat_widget(self, parent, label, color):
        f = tk.Frame(parent, bg="#0d0020", relief='flat', bd=1)
        f.pack(side='left', expand=True, fill='x', padx=4, pady=2)
        v = tk.Label(f, text="0", fg=color, bg="#0d0020",
                     font=("Courier", 16, "bold"))
        v.pack()
        tk.Label(f, text=label, fg="#3a2060", bg="#0d0020",
                 font=("Courier", 7)).pack()
        return v

    def _panel(self, parent, title, idx):
        tk.Label(parent, text=title, bg=BG_COLOR, fg="#cc88ff",
                 font=("Courier", 8, "bold"),
                 pady=6).pack(anchor='w', padx=8)

    # ── GAME LOGIC ───────────────────────

    def _new_game(self):
        """Reset and start a fresh maze for current level."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.moves       = 0
        self.time_left   = 90
        self.decrypted   = False
        self.maze_solved = False
        self.show_path   = False
        self.solution    = []
        self.player      = [0, 0]

        lv = self.LEVELS[self.level]
        self.lbl_algo.config(text=lv['algo'])
        self.lbl_cipher.config(text=lv['cipher'])
        self.lbl_hint.config(text="◈  " + lv['hint'])
        self.lbl_feedback.config(text="", fg=BG_COLOR)
        self.lbl_path_info.config(text="Decrypt cipher first.", fg="#446644")
        self.entry.delete(0, 'end')

        self.btn_auto.config(state='disabled')
        self.btn_next.config(state='disabled')

        self._update_stats()

        self.grid = generate_maze(ROWS, COLS)
        self._draw_maze()
        self._tick()
        self.canvas.focus_set()

    def _update_stats(self):
        self.lbl_level.config(text=str(self.level + 1))
        self.lbl_score.config(text=str(self.score))
        self.lbl_moves.config(text=str(self.moves))
        self.lbl_time.config(text=str(self.time_left))

    def _tick(self):
        """Countdown timer — fires every 1 second."""
        if self.maze_solved:
            return
        if self.time_left > 0:
            self.time_left -= 1
            self.lbl_time.config(text=str(self.time_left))
            self.timer_id = self.root.after(1000, self._tick)
        else:
            self.lbl_feedback.config(text="⏰  Time's up! Press New Maze.",
                                      fg="#ff4466")

    def _check_cipher(self):
        """Validate the player's decryption attempt."""
        lv       = self.LEVELS[self.level]
        attempt  = self.entry.get().strip().upper().replace(" ", "")
        correct  = lv['answer'].upper().replace(" ", "")

        if attempt == correct:
            self.decrypted = True
            self.solution  = solve_maze_bfs(self.grid, ROWS, COLS)
            self.show_path = True
            self.lbl_feedback.config(
                text="◈  CIPHER CRACKED — path unlocked!", fg="#00ff88")
            self.lbl_path_info.config(
                text=f"◈  {len(self.solution)} coordinates decoded · BFS optimal",
                fg="#00cc88")
            self.btn_auto.config(state='normal')
            self.score += 500
            self._update_stats()
            self._draw_maze()   # redraw with solution path shown
        else:
            self.lbl_feedback.config(
                text="✗  Wrong — study the cipher type.", fg="#ff4466")

    def _on_key(self, event):
        """Handle keyboard movement."""
        if self.maze_solved:
            return
        key_map = {
            'Up': (-1, 0), 'w': (-1, 0),
            'Down': (1, 0), 's': (1, 0),
            'Left': (0, -1), 'a': (0, -1),
            'Right': (0, 1), 'd': (0, 1),
        }
        if event.keysym not in key_map:
            return
        dr, dc = key_map[event.keysym]
        r, c   = self.player
        nr, nc = r + dr, c + dc

        # Check bounds
        if not (0 <= nr < ROWS and 0 <= nc < COLS):
            return

        # Check wall — determine which wall to test
        if dr == -1 and not self.grid[r][c]['top']:
            self._do_move(nr, nc)
        elif dr == 1 and not self.grid[r][c]['bottom']:
            self._do_move(nr, nc)
        elif dc == -1 and not self.grid[r][c]['left']:
            self._do_move(nr, nc)
        elif dc == 1 and not self.grid[r][c]['right']:
            self._do_move(nr, nc)

    def _do_move(self, nr, nc):
        self.player = [nr, nc]
        self.moves += 1
        self._update_stats()
        self._draw_maze()
        if nr == ROWS - 1 and nc == COLS - 1:
            self._win()

    def _auto_solve(self):
        """Animate the BFS solution step by step."""
        if not self.solution:
            return
        self.btn_auto.config(state='disabled')
        self._animate_solve(0)

    def _animate_solve(self, step):
        if step >= len(self.solution):
            self._win()
            return
        r, c = self.solution[step]
        self.player = [r, c]
        self.moves += 1
        self._update_stats()
        self._draw_maze()
        self.root.after(60, self._animate_solve, step + 1)

    def _win(self):
        """Player reached the exit."""
        self.maze_solved = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        bonus = self.time_left * 5
        self.score += bonus + 200
        self._update_stats()
        self.lbl_path_info.config(
            text=f"◈  ESCAPED! +{bonus} time bonus · score {self.score}",
            fg="#ffdd44")
        self.btn_next.config(state='normal')

    def _next_level(self):
        self.level = (self.level + 1) % len(self.LEVELS)
        self._new_game()

    # ── DRAWING ──────────────────────────

    def _draw_maze(self):
        self.canvas.delete("all")
        self._draw_bg()
        if self.show_path and self.solution:
            self._draw_solution_path()
        self._draw_walls()
        self._draw_exit()
        self._draw_player()

    def _draw_bg(self):
        """Subtle grid background."""
        self.canvas.create_rectangle(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE,
                                     fill=BG_COLOR, outline="")
        for r in range(ROWS + 1):
            y = r * CELL_SIZE
            self.canvas.create_line(0, y, COLS * CELL_SIZE, y,
                                    fill="#160028", width=1)
        for c in range(COLS + 1):
            x = c * CELL_SIZE
            self.canvas.create_line(x, 0, x, ROWS * CELL_SIZE,
                                    fill="#160028", width=1)

    def _draw_solution_path(self):
        """Draw BFS solution path as glowing tiles."""
        for i, (r, c) in enumerate(self.solution):
            x1, y1 = c * CELL_SIZE + 2, r * CELL_SIZE + 2
            x2, y2 = x1 + CELL_SIZE - 4, y1 + CELL_SIZE - 4
            # Gradient from purple → cyan along the path
            t  = i / max(len(self.solution) - 1, 1)
            r_ = int(0   + t * 0)
            g_ = int(200 * t)
            b_ = int(255 - t * 55)
            fill = f"#{r_:02x}{g_:02x}{b_:02x}"
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill=fill, outline="", stipple="gray25")

    def _draw_walls(self):
        """Draw maze walls."""
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                cell = self.grid[row][col]

                if cell['top']:
                    self.canvas.create_line(x, y, x + CELL_SIZE, y,
                                            fill=WALL_COLOR, width=2)
                if cell['right']:
                    self.canvas.create_line(x + CELL_SIZE, y,
                                            x + CELL_SIZE, y + CELL_SIZE,
                                            fill=WALL_COLOR, width=2)
                if cell['bottom']:
                    self.canvas.create_line(x, y + CELL_SIZE,
                                            x + CELL_SIZE, y + CELL_SIZE,
                                            fill=WALL_COLOR, width=2)
                if cell['left']:
                    self.canvas.create_line(x, y, x, y + CELL_SIZE,
                                            fill=WALL_COLOR, width=2)

    def _draw_exit(self):
        """Draw golden exit portal."""
        c  = COLS - 1
        r  = ROWS - 1
        x1 = c * CELL_SIZE + 4
        y1 = r * CELL_SIZE + 4
        x2 = x1 + CELL_SIZE - 8
        y2 = y1 + CELL_SIZE - 8
        self.canvas.create_oval(x1, y1, x2, y2,
                                 fill=EXIT_COLOR, outline="#ffaa00", width=2)
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                  text="★", fill="#fff8aa", font=("Arial", 9))

    def _draw_player(self):
        """Draw player as glowing white orb."""
        r, c = self.player
        cx_  = c * CELL_SIZE + CELL_SIZE // 2
        cy_  = r * CELL_SIZE + CELL_SIZE // 2
        rad  = CELL_SIZE // 2 - 3

        # Outer glow ring
        self.canvas.create_oval(cx_ - rad - 3, cy_ - rad - 3,
                                 cx_ + rad + 3, cy_ + rad + 3,
                                 fill="", outline=GLOW_COLOR, width=2)
        # Filled orb
        self.canvas.create_oval(cx_ - rad, cy_ - rad,
                                 cx_ + rad, cy_ + rad,
                                 fill=PLAYER_COL, outline="#cc88ff", width=1)


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = CipherMazeApp(root)
    root.mainloop()
