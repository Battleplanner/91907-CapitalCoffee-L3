import tkinter as tk
from tkinter import ttk


class App:

    def __init__(self):
        # Sets up the root window
        self.root = tk.Tk()
        self.root.geometry("350x400")
        self.root.title("Capital Coffee")
        self.root.grid()

        # CONSTANTS
        self.COFFEES = [
            "No Coffee Selected",
            "Cappuccino - $4.50",
            "Flat White - $4.50",
            "Cafe Latte - $4.50",
            "Long Espresso - $4.50",
            "Short Espresso - $4.50",
            "Long Macchiato - $4.50",
            "Choffee - $7.00",
            "White Choffee - $7.00",
            "Chocolate Latte - $7.00",
            "White Chocolate Latte - $7.00",
            "Affogato - $7.00",
            "Cafe Vienna - $7.00"]

        self.root.mainloop()


if __name__ == "__main__":
    app = App()
