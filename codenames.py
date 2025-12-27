import csv
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

CSV_FILE = "./words.csv"  # Path to your CSV file
GRID_SIZE = 5
BUTTON_WIDTH = 16
BUTTON_HEIGHT = 6

# Fun, vibrant color scheme with gradients
MARKER_COLORS = {
    "None": "#ffffff",
    "Blue": "#6366f1",
    "Red": "#f43f5e",
    "Beige": "#e8dcc8",
    "Bomb": "#1f2937",
}

class CodenamesUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Codenames 1–2 Samuel")
        self.root.configure(bg="#f3f4f6")
        
        # Configure root window to expand with resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.words = self.load_words()
        if len(self.words) < 25:
            messagebox.showerror("Error", "CSV must contain at least 25 words.")
            self.root.destroy()
            return
        
        self.cards = []
        self.marker_choice = tk.StringVar(value="None")
        self.card_images = {}  # Cache for rounded button images
        self.used_words = set()  # Track words currently in use
        
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
    
    def create_rounded_button_image(self, color, width=200, height=120):
        """Create a rounded rectangle image for button styling"""
        key = (color, width, height)
        if key in self.card_images:
            return self.card_images[key]
        
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        radius = 20
        
        # Draw rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (width - 1, height - 1)],
            radius=radius,
            fill=color,
            outline=color
        )
        
        photo = ImageTk.PhotoImage(img)
        self.card_images[key] = photo
        return photo
    
    def build_controls(self):
        control_frame = tk.Frame(self.root, bg="#f3f4f6")
        control_frame.pack(pady=15, fill=tk.X)
        
        # Title
        title = tk.Label(
            control_frame,
            text="Select Marker:",
            font=("Comic Sans MS", 16, "bold"),
            bg="#f3f4f6",
            fg="#1f2937"
        )
        title.pack(side=tk.LEFT, padx=10)

        for label in MARKER_COLORS:
            btn = tk.Radiobutton(
                control_frame,
                text=label,
                variable=self.marker_choice,
                value=label,
                indicatoron=False,
                width=8,
                bg=MARKER_COLORS[label],
                fg="white" if label in ("Blue", "Red", "Bomb") else "#1f2937",
                font=("Comic Sans MS", 12, "bold"),
                relief="raised",
                bd=2,
                activebackground=MARKER_COLORS[label],
                selectcolor=MARKER_COLORS[label]
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh Grid",
            command=self.generate_grid,
            width=14,
            bg="#10b981",
            fg="white",
            font=("Comic Sans MS", 12, "bold"),
            relief="raised",
            bd=2,
            activebackground="#059669"
        )
        refresh_btn.pack(side=tk.LEFT, padx=15)
    
    def build_grid(self):
        self.grid_frame = tk.Frame(self.root, bg="#f3f4f6")
        self.grid_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure grid to expand with window
        for r in range(GRID_SIZE):
            self.grid_frame.grid_rowconfigure(r, weight=1)
            for c in range(GRID_SIZE):
                self.grid_frame.grid_columnconfigure(c, weight=1)
        
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                # Create a frame to hold the button with shadow effect
                card_frame = tk.Frame(self.grid_frame, bg="#f3f4f6")
                card_frame.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
                
                btn = tk.Button(
                    card_frame,
                    text="",
                    wraplength=120,
                    justify="center",
                    bg=MARKER_COLORS["None"],
                    fg="#1f2937",
                    font=("Comic Sans MS", 14, "bold"),
                    relief="raised",
                    bd=5,
                    activebackground=MARKER_COLORS["None"],
                    activeforeground="#1f2937"
                )
                btn.pack(fill=tk.BOTH, expand=True)
                btn.config(command=lambda b=btn: self.apply_marker(b))
                
                # Add right-click context menu
                btn.bind("<Button-3>", lambda event, b=btn: self.show_context_menu(event, b))
                
                row.append(btn)
            self.cards.append(row)
    
    def generate_grid(self):
        selected = random.sample(self.words, 25)
        self.used_words = set()
        index = 0
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                eng, kor = selected[index]
                btn = self.cards[r][c]
                btn.config(
                    text=f"{eng}\n{kor}",
                    bg=MARKER_COLORS["None"],
                    fg="#1f2937",
                    activebackground=MARKER_COLORS["None"],
                    activeforeground="#1f2937"
                )
                self.used_words.add((eng, kor))
                index += 1
    
    def get_new_word(self):
        """Get a random word that hasn't been used"""
        available_words = [w for w in self.words if w not in self.used_words]
        if not available_words:
            messagebox.showwarning("No Words Available", "All words have been used!")
            return None
        return random.choice(available_words)
    
    def show_context_menu(self, event, button):
        """Show context menu for replacing a word"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(
            label="Replace Word",
            command=lambda: self.replace_word(button)
        )
        context_menu.post(event.x_root, event.y_root)
    
    def replace_word(self, button):
        """Replace a single word with a new random word"""
        new_word = self.get_new_word()
        if new_word is None:
            return
        
        # Remove old word from used set
        old_text = button.cget("text")
        old_eng = old_text.split("\n")[0]
        for word in self.used_words.copy():
            if word[0] == old_eng:
                self.used_words.remove(word)
                break
        
        # Add new word
        eng, kor = new_word
        button.config(text=f"{eng}\n{kor}")
        self.used_words.add(new_word)
    
    def apply_marker(self, button):
        choice = self.marker_choice.get()
        color = MARKER_COLORS[choice]
        text_color = "white" if choice in ("Blue", "Red", "Bomb") else "#1f2937"
        button.config(
            bg=color,
            activebackground=color,
            fg=text_color,
            activeforeground=text_color
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = CodenamesUI(root)
    root.mainloop()
