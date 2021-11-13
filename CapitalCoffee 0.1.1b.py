import tkinter as tk
import tkinter.ttk as ttk


def main():
    """The main function that sets and runs everything"""

    root = tk.Tk()
    root.geometry("350x400")
    root.title("Capital Coffee")

    coffees = [["Cappuccino", 4.50],
               ["Flat White", 4.50],
               ["Cafe Latte", 4.50],
               ["Long Espresso", 4.50],
               ["Short Espresso", 4.50],
               ["Long Macchiato", 4.50],
               ["Choffee", 7.00],
               ["White Choffee", 7.00],
               ["Chocolate Latte", 7.00],
               ["White Chocolate Latte", 7.00],
               ["Affogato", 7.00],
               ["Cafe Vienna", 7.00]]

    root.mainloop()


if __name__ == '__main__':
    main()
