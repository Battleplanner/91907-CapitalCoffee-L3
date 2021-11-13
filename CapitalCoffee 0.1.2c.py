import tkinter as tk
from tkinter import ttk


class App:

    def __init__(self):
        # Sets up the root window
        self.root = tk.Tk()
        self.root.geometry("350x400")
        self.root.title("Capital Coffee")
        self.root.columnconfigure(0, weight=1)
        #self.root.rowconfigure(0, weight=1)
        self.root.grid()

        # CONSTANTS
        self.DELIVERY_CHARGE_FEE = 3.00
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

        # Cost variables
        self.cost = tk.DoubleVar()  # The total cost of the order
        self.cost.set(0.00)

        # App setup
        self.setup_order_type()

        self.root.mainloop()

    def order_type_changed(self, *args):
        if self.order_type.get() == "delivery":
            self.update_total()
        elif self.order_type.get() == "pickup":
            self.update_total()

    def setup_order_type(self):
        """Sets up a frame containing the 'pickup' and 'delivery' buttons"""
        self.order_type = tk.StringVar()

        self.order_type_frame = tk.Frame(self.root)
        self.order_type_frame.config(background="blue")
        # First column in the frame has a relative size of 1
        self.order_type_frame.grid_columnconfigure(0, weight=1)
        # Second column in the frame has a relative size of 1
        self.order_type_frame.grid_columnconfigure(1, weight=1)

        self.order_type_frame.grid(row=0, sticky=tk.EW)

        self.pickup_radio_button = tk.Radiobutton(
            self.order_type_frame,
            text="Pickup",
            indicatoron=0,
            command=lambda: self.order_type.set("pickup"))
        self.pickup_radio_button.grid(sticky=tk.EW, column=0, row=0)

        self.delivery_radio_button = tk.Radiobutton(
            self.order_type_frame,
            text="Delivery",
            indicatoron=0,
            command=lambda: self.order_type.set("delivery"))
        self.delivery_radio_button.grid(sticky=tk.EW, column=1, row=0)

        # Runs self.order_type_changed() when self.order_type is changed
        self.order_type.trace("w", self.order_type_changed)

    def update_total(self):
        """Updates the running summary/reciept"""
        self.cost.set(0.00)

        # Adds a delivery fee of $3 if delivery is selected
        if self.order_type.get() == "delivery":
            self.cost.set(self.cost.get() + self.DELIVERY_CHARGE_FEE)


if __name__ == "__main__":
    app = App()
