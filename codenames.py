import csv
import random
import tkinter as tk
from tkinter import messagebox

CSV_FILE = "words.csv"  # Path to your CSV file
GRID_SIZE = 5
BUTTON_WIDTH = 16
BUTTON_HEIGHT = 6

MARKER_COLORS = {
    "None": "#f0f0f0",
    "Blue": "#4a90e2",
    "Red": "#d0021b",
    "Beige": "#f5e6c8",
    "Bomb": "#4a4a4a",
}

class CodenamesUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Codenames 1–2 Samuel")
        
        self.words = self.load_words()
        if len(self.words) < 25:
            messagebox.showerror("Error", "CSV must contain at least 25 words.")
            self.root.destroy()
            return
        
        self.cards = []
        self.marker_choice = tk.StringVar(value="None")
        
        self.build_controls()
        self.build_grid()
        self.generate_grid()
    
    def load_words(self):
        words = []
        try:
            with open(CSV_FILE, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        english = row[0].strip()
                        korean = row[1].strip()
                        words.append((english, korean))
        except FileNotFoundError:
            messagebox.showerror("Error", f"CSV file not found: {CSV_FILE}")
            self.root.destroy()
        return words
    
    def build_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        for label in MARKER_COLORS:
            btn = tk.Radiobutton(
                control_frame,
                text=label,
                variable=self.marker_choice,
                value=label,
                indicatoron=False,
                width=8,
                bg=MARKER_COLORS[label],
                fg="white" if label in ("Blue", "Red", "Bomb") else "black"
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        refresh_btn = tk.Button(
            control_frame,
            text="Refresh Grid",
            command=self.generate_grid,
            width=12,
            bg="#4caf50",
            fg="white",
            font=("Arial", 12, "bold")
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
    
    def build_grid(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
        
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    width=BUTTON_WIDTH,
                    height=BUTTON_HEIGHT,
                    wraplength=120,
                    justify="center",
                    bg=MARKER_COLORS["None"],
                    fg="black",
                    font=("Arial", 12, "bold")
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                btn.config(command=lambda b=btn: self.apply_marker(b))
                row.append(btn)
            self.cards.append(row)
    
    def generate_grid(self):
        selected = random.sample(self.words, 25)
        index = 0
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                eng, kor = selected[index]
                btn = self.cards[r][c]
                btn.config(
                    text=f"{eng}\n{kor}",
                    bg=MARKER_COLORS["None"],
                    fg="black",
                    activebackground=MARKER_COLORS["None"],
                    font=("Arial", 12, "bold")
                )
                index += 1
    
    def apply_marker(self, button):
        choice = self.marker_choice.get()
        color = MARKER_COLORS[choice]
        button.config(
            bg=color,
            activebackground=color,
            fg="black"  # always black text
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CodenamesUI(root)
    root.mainloop()
