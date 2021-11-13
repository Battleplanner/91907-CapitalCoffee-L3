import tkinter as tk
from tkinter import ttk


class App:

    def __init__(self):
        # Sets up the root window
        self.root = tk.Tk()
        self.root.geometry("350x400")
        self.root.minsize(width=350, height=400)
        self.root.maxsize(width=350, height=400)

        self.root.title("Capital Coffee")
        self.root.columnconfigure(0, weight=1)
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
        self.setup_menu()
        self.setup_order_type()
        self.setup_customer_info_frame()
        self.setup_coffee_options()
        self.setup_running_cost()

        self.root.mainloop()

    def setup_menu(self):
        """Sets up a menu containing the 'New Order', 'Print Order', and
        'Exit' options respectively"""

        self.menubar = tk.Menu(self.root)

        self.menubar.add_command(label="New Order", command=self.new_order)
        self.menubar.add_command(label="Print Order", command=self.print_order)
        self.menubar.add_command(label="Quit", command=self.root.destroy)

        self.root.config(menu=self.menubar)

    def order_type_changed(self, *args):
        """Updates the customer_address and customer_number entry widgets
        as well as the total cost"""
        if self.order_type.get() == "delivery":
            self.customer_address_entry.configure(state="normal")
            self.customer_number_entry.configure(state="normal")
            self.update_total()
        elif self.order_type.get() == "pickup":
            self.customer_address_entry.delete(0, "end")
            self.customer_number_entry.delete(0, "end")
            self.customer_address_entry.configure(state="disabled")
            self.customer_number_entry.configure(state="disabled")
            self.update_total()

    def setup_order_type(self):
        """Sets up a frame containing the 'pickup' and 'delivery' buttons"""
        self.order_type = tk.StringVar()

        self.order_type_frame = tk.Frame(self.root)
        # First column in the frame has a relative size of 1
        self.order_type_frame.grid_columnconfigure(0, weight=1)
        # Second column in the frame has a relative size of 1
        self.order_type_frame.grid_columnconfigure(1, weight=1)

        self.order_type_frame.grid(row=0, sticky=tk.EW, padx=10, pady=10)

        self.pickup_radio_button = tk.Radiobutton(
            self.order_type_frame,
            text="Pickup",
            indicatoron=False,
            command=lambda: self.order_type.set("pickup"))
        self.pickup_radio_button.grid(sticky=tk.EW, column=0, row=0)

        self.delivery_radio_button = tk.Radiobutton(
            self.order_type_frame,
            text="Delivery",
            indicatoron=False,
            command=lambda: self.order_type.set("delivery"))
        self.delivery_radio_button.grid(sticky=tk.EW, column=1, row=0)

        # Runs self.order_type_changed() when self.order_type is changed
        self.order_type.trace("w", self.order_type_changed)

    def setup_customer_info_frame(self):

        self.customer_name = tk.StringVar()
        self.customer_address = tk.StringVar()
        # Will require removing of spaces and validation for numbers only
        self.customer_number = tk.IntVar()

        self.customer_info_frame = tk.Frame(self.root)
        self.customer_info_frame.grid_columnconfigure(0, weight=1)
        self.customer_info_frame.grid_columnconfigure(1, weight=1)

        self.customer_info_frame.grid(row=1, sticky=tk.EW, padx=10, pady=10)

        self.customer_info_label = tk.Label(
            self.customer_info_frame, text="Customer Info")
        self.customer_info_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.EW)

        self.customer_name_label = tk.Label(
            self.customer_info_frame, text="Name: ", width=10, anchor="e")
        self.customer_name_label.grid(row=1, column=0, sticky=tk.EW)

        self.customer_name_entry = tk.Entry(
            self.customer_info_frame, textvariable=self.customer_name)
        self.customer_name_entry.grid(row=1, column=1, sticky=tk.EW)

        self.customer_address_label = tk.Label(
            self.customer_info_frame, text="Address: ", width=10, anchor="e")
        self.customer_address_label.grid(row=2, column=0, sticky=tk.EW)

        self.customer_address_entry = tk.Entry(
            self.customer_info_frame, textvariable=self.customer_address)
        self.customer_address_entry.grid(row=2, column=1, sticky=tk.EW)

        self.customer_number_label = tk.Label(
            self.customer_info_frame, text="Phone Number: ", width=10, anchor="e")
        self.customer_number_label.grid(row=3, column=0, sticky=tk.EW)

        self.customer_number_entry = tk.Entry(
            self.customer_info_frame, textvariable=self.customer_number)
        self.customer_number_entry.grid(row=3, column=1, sticky=tk.EW)

    def update_total(self):
        """Updates the running summary/reciept"""
        self.cost.set(0.00)
        for i in self.coffees_ordered:
            option = i.get()  # Takes the option chosen from the dropdown
            # Skips adding the cost if a coffee hasn't been selected
            if option != self.COFFEES[0]:
                # Takes last 4 characters, which should be the cost e.g 7.00
                option_cost = option[-4:]
                option_cost = float(option_cost)
                # Adds the cost of the option to the total cost
                self.cost.set(self.cost.get() + option_cost)

        # Adds a delivery fee of $3 if delivery is selected
        if self.order_type.get() == "delivery":
            self.cost.set(self.cost.get() + self.DELIVERY_CHARGE_FEE)

        # Sets the running_cost label to the new cost, rounded to 2dp
        self.running_cost_label.configure(
            text="Current Price: ${}".format('{:.2f}'.format(self.cost.get())))

    def print_order(self):
        """Validates the order and, if successful, gives the user a printed
        summary of their order"""

        self.order_type_missing_message_text = "An order type has not been \
            selected. Please select either 'Delivery' or 'Pickup"
        self.customer_name_missing_message_text = "A name for the customer \
            has not been entered. Please enter a name for the customer"
        self.customer_address_missing_message_text = "An address for the \
            customer has not been entered but you have selected 'delivery'. \
                Please enter an address for the customer or choose 'pickup' \
                    instead."
        self.customer_number_missing_message_text = "A phone number for the \
            customer has not been entered or contains invalid characters. \
                Please enter a valid phone number for the customer."
        self.coffee_one_missing_message_text = "At least one coffee must be \
            selected. Please select at least one coffee."

        # Checks to make sure a delivery type is chosen
        if (self.order_type.get() == "delivery" or
                self.order_type.get() == "pickup"):

            # Checks to make sure a customer name is entered
            if self.customer_name.get() != "":

                # Checks to make sure a delivery address is chosen, if required
                if ((self.customer_address.get() != "" and
                     self.order_type.get() == "delivery") or
                        self.order_type.get() == "pickup"):

                    # Checks to make sure the phone number is entered and valid
                    if ((self.customer_number.
                         get().
                         replace(" ", "").
                         isnumeric()) or
                            self.order_type.get() == "pickup"):

                        # Checks to make sure at least one coffee is selected
                        if self.COFFEES[0] != self.coffee_one.get():

                            self.printed_order = tk.Toplevel()
                            self.printed_order.title(
                                "Receipt: {}".format(self.customer_name.get()))

                            self.receipt_order_type = tk.Label(
                                self.printed_order,
                                text=("Order Type: {}".
                                      format(self.order_type.get())))
                            self.receipt_order_type.pack()

                            self.receipt_customer_name = tk.Label(
                                self.printed_order,
                                text=("Name: {}".
                                      format(self.customer_name.get())))
                            self.receipt_customer_name.pack()

                            if self.order_type.get() == "delivery":
                                self.receipt_customer_number = tk.Label(
                                    self.printed_order,
                                    text=("Phone Number: {}".
                                          format(self.customer_number.get())))
                                self.receipt_customer_number.pack()

                                self.receipt_customer_address = tk.Label(
                                    self.printed_order,
                                    text=("Address: {}".
                                          format(self.customer_address.get())))
                                self.receipt_customer_address.pack()

                            for i in self.coffees_ordered:
                                if i.get() != self.COFFEES[0]:
                                    self.coffee_label = tk.Label(
                                        self.printed_order,
                                        text="Coffee: {}".format(i.get()))
                                    self.coffee_label.pack()

                            if self.order_type.get() == "delivery":
                                self.delivery_charge = tk.Label(
                                    self.printed_order,
                                    text="Delivery Charge: $3.00")
                                self.delivery_charge.pack()

                            self.string_cost = (
                                '{:.2f}'.format(self.cost.get()))
                            self.total_charge = tk.Label(
                                self.printed_order,
                                text=("Total Price: ${}".
                                      format(self.string_cost)))
                            self.total_charge.pack()

                            self.final_message = tk.Label(
                                self.printed_order, text="Thank you for \
                                    shopping at Capital Coffee, please see \
                                        file at {} for your \
                                            receipt".format(receipt_name))

                        else:
                            self.coffee_one_missing_toplevel = tk.Toplevel()
                            self.coffee_one_missing_toplevel.title(
                                "No coffees selected")
                            self.coffee_one_missing_message = tk.Message(
                                self.coffee_one_missing_toplevel,
                                text=self.coffee_one_missing_message_text)
                            self.coffee_one_missing_message.pack()

                            self.coffee_one_missing_dismiss_button = tk.Button(
                                self.coffee_one_missing_toplevel,
                                text="Dismiss",
                                command=(self.
                                         coffee_one_missing_toplevel.
                                         destroy))
                            self.coffee_one_missing_dismiss_button.pack()

                    else:  # Gives a pop up about the invalid customer number
                        self.customer_number_missing_toplevel = tk.Toplevel()
                        self.customer_number_missing_toplevel.title(
                            "Customer Number not found or invalid")
                        self.customer_number_missing_message = tk.Message(
                            self.customer_number_missing_toplevel,
                            text=self.customer_number_missing_message_text)
                        self.customer_number_missing_message.pack()

                        self.customer_number_missing_dismiss_button = (
                            tk.Button(
                                self.customer_number_missing_toplevel,
                                text="Dismiss",
                                command=(self.
                                         customer_number_missing_toplevel.
                                         destroy)))
                        self.customer_number_missing_dismiss_button.pack()

                else:  # Gives a pop up about the missing customer address
                    self.customer_address_missing_toplevel = tk.Toplevel()
                    self.customer_address_missing_toplevel.title(
                        "Customer Address not found")
                    self.customer_address_missing_message = tk.Message(
                        self.customer_address_missing_toplevel,
                        text=self.customer_address_missing_message_text)
                    self.customer_address_missing_message.pack()

                    self.customer_address_missing_dismiss_button = tk.Button(
                        self.customer_address_missing_toplevel,
                        text="Dismiss",
                        command=self.customer_address_missing_toplevel.destroy)
                    self.customer_address_missing_dismiss_button.pack()

            else:  # Gives a pop up about the missing customer name
                self.customer_name_missing_toplevel = tk.Toplevel()
                self.customer_name_missing_toplevel.title(
                    "Customer Name not found")
                self.customer_name_missing_message = tk.Message(
                    self.customer_name_missing_toplevel,
                    text=self.customer_name_missing_message_text)
                self.customer_name_missing_message.pack()

                self.customer_name_missing_dismiss_button = tk.Button(
                    self.customer_name_missing_toplevel,
                    text="Dismiss",
                    command=self.customer_name_missing_toplevel.destroy)
                self.customer_name_missing_dismiss_button.pack()

        else:  # Gives a pop up about the missing order type
            self.order_type_missing_toplevel = tk.Toplevel()
            self.order_type_missing_toplevel.title("Order Type not found")
            self.order_type_missing_message = tk.Message(
                self.order_type_missing_toplevel,
                text=self.order_type_missing_message_text)
            self.order_type_missing_message.pack()

            self.order_type_missing_dismiss_button = tk.Button(
                self.order_type_missing_toplevel,
                text="Dismiss",
                command=self.order_type_missing_toplevel.destroy)
            self.order_type_missing_dismiss_button.pack()

    def setup_coffee_options(self):
        """Sets up the dropdowns and labels for selecting coffees"""
        self.coffee_options_frame = tk.Frame(self.root)
        self.coffee_options_frame.grid_columnconfigure(0, weight=1)
        self.coffee_options_frame.grid_columnconfigure(1, weight=1)
        self.coffee_options_frame.grid(row=2, sticky=tk.EW, padx=10, pady=10)

        self.coffee_one = tk.StringVar()
        self.coffee_two = tk.StringVar()
        self.coffee_three = tk.StringVar()
        self.coffee_four = tk.StringVar()
        self.coffee_five = tk.StringVar()

        self.coffees_ordered = [self.coffee_one,
                                self.coffee_two,
                                self.coffee_three,
                                self.coffee_four,
                                self.coffee_five]

        self.coffee_options_label = tk.Label(
            self.coffee_options_frame, text="Coffee Options")
        self.coffee_options_label.grid(
            row=0, column=0, columnspan=2, sticky=tk.EW)

        # Sets the default value for the coffees to be 'No Coffees Ordered'
        for i in self.coffees_ordered:
            i.set(self.COFFEES[0])

        self.coffee_one_label = tk.Label(
            self.coffee_options_frame, text="Coffee One: ", width=10, anchor="e")
        self.coffee_one_label.grid(sticky=tk.EW, row=1, column=0)

        self.coffee_one_dropdown = tk.OptionMenu(
            self.coffee_options_frame, self.coffee_one, *self.COFFEES)
        self.coffee_one_dropdown.grid(sticky=tk.EW, row=1, column=1)

        self.coffee_two_label = tk.Label(
            self.coffee_options_frame, text="Coffee Two: ", width=10, anchor="e")
        self.coffee_two_label.grid(sticky=tk.EW, row=2, column=0)

        self.coffee_two_dropdown = tk.OptionMenu(
            self.coffee_options_frame, self.coffee_two, *self.COFFEES)
        self.coffee_two_dropdown.grid(sticky=tk.EW, row=2, column=1)

        self.coffee_three_label = tk.Label(
            self.coffee_options_frame, text="Coffee Three: ", width=10, anchor="e")
        self.coffee_three_label.grid(sticky=tk.EW, row=3, column=0)

        self.coffee_three_dropdown = tk.OptionMenu(
            self.coffee_options_frame, self.coffee_three, *self.COFFEES)
        self.coffee_three_dropdown.grid(sticky=tk.EW, row=3, column=1)

        self.coffee_four_label = tk.Label(
            self.coffee_options_frame, text="Coffee Four: ", width=10, anchor="e")
        self.coffee_four_label.grid(sticky=tk.EW, row=4, column=0)

        self.coffee_four_dropdown = tk.OptionMenu(
            self.coffee_options_frame, self.coffee_four, *self.COFFEES)
        self.coffee_four_dropdown.grid(sticky=tk.EW, row=4, column=1)

        self.coffee_five_label = tk.Label(
            self.coffee_options_frame, text="Coffee Five: ", width=10, anchor="e")
        self.coffee_five_label.grid(sticky=tk.EW, row=5, column=0)

        self.coffee_five_dropdown = tk.OptionMenu(
            self.coffee_options_frame, self.coffee_five, *self.COFFEES)
        self.coffee_five_dropdown.grid(sticky=tk.EW, row=5, column=1)

        # Disable the specified dropdown
        self.coffee_two_dropdown.configure(state="disabled")
        self.coffee_three_dropdown.configure(state="disabled")
        self.coffee_four_dropdown.configure(state="disabled")
        self.coffee_five_dropdown.configure(state="disabled")

        # Runs the given function when the variable is changed
        self.coffee_one.trace("w", self.coffee_first_option_selected)
        self.coffee_two.trace("w", self.coffee_second_option_selected)
        self.coffee_three.trace("w", self.coffee_third_option_selected)
        self.coffee_four.trace("w", self.coffee_fourth_option_selected)
        self.coffee_five.trace("w", self.coffee_fifth_option_selected)

    def coffee_first_option_selected(self, *args):
        """Runs when an option is selected for the first coffee slot"""
        # If the value of the coffee_one dropdown is 'Not Selected'
        if self.coffee_one.get() == self.COFFEES[0]:
            # Disable further coffees until this one is selected
            self.coffee_two_dropdown.configure(state="disabled")
            self.coffee_three_dropdown.configure(state="disabled")
            self.coffee_four_dropdown.configure(state="disabled")
            self.coffee_five_dropdown.configure(state="disabled")

            self.coffee_two.set(self.COFFEES[0])
            self.coffee_three.set(self.COFFEES[0])
            self.coffee_four.set(self.COFFEES[0])
            self.coffee_five.set(self.COFFEES[0])

            self.update_total()
        else:
            # Make sure the next option is enabled
            self.coffee_two_dropdown.configure(state="normal")
            self.update_total()

    def coffee_second_option_selected(self, *args):
        """Runs when an option is selected for the second coffee slot"""
        # If the value of the coffee_one dropdown is 'Not Selected'
        if self.coffee_two.get() == self.COFFEES[0]:
            # Disable further coffees until this one is selected
            self.coffee_three_dropdown.configure(state="disabled")
            self.coffee_four_dropdown.configure(state="disabled")
            self.coffee_five_dropdown.configure(state="disabled")

            self.coffee_three.set(self.COFFEES[0])
            self.coffee_four.set(self.COFFEES[0])
            self.coffee_five.set(self.COFFEES[0])
        else:
            # Make sure the next option is enabled
            self.coffee_three_dropdown.configure(state="normal")
            self.update_total()

    def coffee_third_option_selected(self, *args):
        """Runs when an option is selected for the third coffee slot"""
        # If the value of the coffee_one dropdown is 'Not Selected'
        if self.coffee_three.get() == self.COFFEES[0]:
            # Disable further coffees until this one is selected
            self.coffee_four_dropdown.configure(state="disabled")
            self.coffee_five_dropdown.configure(state="disabled")

            self.coffee_four.set(self.COFFEES[0])
            self.coffee_five.set(self.COFFEES[0])
        else:
            # Make sure the next option is enabled
            self.coffee_four_dropdown.configure(state="normal")
            self.update_total()

    def coffee_fourth_option_selected(self, *args):
        """Runs when an option is selected for the fourth coffee slot"""
        # If the value of the coffee_one dropdown is 'Not Selected'
        if self.coffee_four.get() == self.COFFEES[0]:

            # Disable further coffees until this one is selected
            self.coffee_five_dropdown.configure(state="disabled")

            self.coffee_five.set(self.COFFEES[0])
        else:
            # Make sure the next option is enabled
            self.coffee_five_dropdown.configure(state="normal")
            self.update_total()

    def coffee_fifth_option_selected(self, *args):
        """Runs when an option is selected for the fifth coffee slot"""
        self.update_total()

    def new_order(self, *args):
        """Runs when the new order is made, closes and opens the app again"""
        self.root.destroy()
        app = App()

    def setup_running_cost(self):
        """Will display a current cost of the order before printing"""
        self.running_cost_frame = tk.Frame(self.root)
        self.running_cost_frame.grid(row=4, padx=10, pady=10)

        self.running_cost_label = tk.Label(
            self.running_cost_frame, text="Current Price: $0.00")
        self.running_cost_label.pack()


if __name__ == "__main__":
    app = App()
