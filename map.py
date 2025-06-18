import tkinter as tk
from tkinter import messagebox

class MapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Map")
        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        # simple canvas acting as a placeholder for the map
        self.canvas = tk.Canvas(self, width=400, height=300, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # draw grid lines to represent the map
        for i in range(0, 401, 40):
            self.canvas.create_line(i, 0, i, 300, fill="#ddd")
        for j in range(0, 301, 30):
            self.canvas.create_line(0, j, 400, j, fill="#ddd")

    def _create_menu(self):
        menubar = tk.Menu(self)
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Simple Map Demo\n\nThis example demonstrates adding a menu to a map using Tkinter."
        )

    def show_instructions(self):
        messagebox.showinfo(
            "Instructions",
            "- Click and drag to explore the map (disabled in this demo).\n- Use the Help menu for information."
        )

if __name__ == "__main__":
    app = MapApp()
    app.mainloop()
