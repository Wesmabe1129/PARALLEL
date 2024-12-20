import tkinter as tk
import threading
import random
import time
import json

# Lock object for synchronization
lock = threading.Lock()

# Load data from JSON
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"trade_log": [], "offers": {}, "traders": {"Trader_A": ["item1", "item2"], "Trader_B": ["item3", "item4"], "Trader_C": ["item5", "item6"], "Trader_D": ["item7", "item8"]}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

class WidgetGenerator:
    @staticmethod
    def create_label(master, text=None, textvariable=None, font=None, grid=None, pack=None, place=None):
        label = tk.Label(master, text=text, textvariable=textvariable, font=font)
        WidgetGenerator.set_geometry_manager(label, pack=pack, grid=grid, place=place)
        return label
    
    @staticmethod
    def create_button(master, text=None, font=None, command=None, grid=None, pack=None, place=None, state=None):
        button = tk.Button(master, text=text, font=font, state=state, command=command)
        WidgetGenerator.set_geometry_manager(button, pack=pack, grid=grid, place=place)
        return button
    
    @staticmethod
    def create_listbox(master, grid=None, pack=None, place=None):
        listbox = tk.Listbox(master)
        WidgetGenerator.set_geometry_manager(listbox, pack=pack, grid=grid, place=place)
        return listbox

    @staticmethod
    def create_entry(master, font=None, show=None, width=None, grid=None, pack=None, place=None):
        entry = tk.Entry(master, font=font, show=show, width=width)
        WidgetGenerator.set_geometry_manager(entry, pack=pack, grid=grid, place=place)
        return entry

    @staticmethod
    def create_frame(master, grid=None, pack=None, place=None):
        frame = tk.Frame(master)
        WidgetGenerator.set_geometry_manager(frame, pack=pack, grid=grid, place=place)
        return frame

    @staticmethod
    def set_geometry_manager(widget, pack=None, grid=None, place=None):
        if pack:
            widget.pack(**pack)
        elif grid:
            widget.grid(**grid)
        elif place:
            widget.place(**place)
        else:
            widget.pack()


active_windows = 0

class TradingWindow:
    instances = []  # Keep track of all instances


    def __init__(self, title, trader_name, items):
        global active_windows
        self.root = tk.Tk()
        self.root.title(title)
        self.trader_name = trader_name
        self.inventory = items
        self.locked_offers = set()
        TradingWindow.instances.append(self)  # Register instance
        active_windows += 1

        # Handle the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inventory display
        WidgetGenerator.create_label(
            self.root, text=f"{self.trader_name}'s Inventory", font=("Arial", 16), pack={"pady": 10}
        )
        self.inventory_list = WidgetGenerator.create_listbox(self.root, pack={"pady": 10})
        self.update_inventory()

        # Trade offer section
        self.offer_entry = WidgetGenerator.create_entry(self.root, width=20, pack={"pady": 5})
        WidgetGenerator.create_button(
            self.root, text="Offer Item", command=self.offer_item, pack={"pady": 5}
        )

        # Trade offers display
        WidgetGenerator.create_label(
            self.root, text="Available Trade Offers", font=("Arial", 14), pack={"pady": 10}
        )
        self.trade_offers_list = WidgetGenerator.create_listbox(self.root, pack={"pady": 10})
        self.update_trade_offers()

        # Accept Trade button
        WidgetGenerator.create_button(
            self.root, text="Accept Offer", command=self.accept_selected_offer, pack={"pady": 5}
        )

        # Trade log section
        WidgetGenerator.create_label(
            self.root, text="Trade Log", font=("Arial", 14), pack={"pady": 10}
        )
        self.trade_log_list = WidgetGenerator.create_listbox(self.root, pack={"pady": 10})
        self.update_trade_log()

        # Start updating trade offers in real-time
        self.schedule_trade_offer_updates()

        # Start simulated trading every 2 seconds
        self.simulate_trading()

    def update_inventory(self):
        lock.acquire()
        try:
            self.inventory_list.delete(0, tk.END)
            for item in self.inventory:
                self.inventory_list.insert(tk.END, item)
            print("Done Updating Inventory")
        finally:
            lock.release()

    def update_trade_log(self):
        self.trade_log_list.delete(0, tk.END)
        for entry in data["trade_log"]:
            self.trade_log_list.insert(tk.END, entry)

    def update_trade_offers(self):
        # Cache the currently displayed offers in the listbox
        current_offers = self.trade_offers_list.get(0, tk.END)

        # Iterate through available offers in data["offers"]
        for trader, item in data["offers"].items():
            offer = f"{trader}: {item}"

            # Only add the offer if it's not already listed, doesn't belong to the current trader, and is not locked
            if trader != self.trader_name and offer not in current_offers and offer not in self.locked_offers:
                self.trade_offers_list.insert(tk.END, offer)

    def offer_item(self):
        item = self.offer_entry.get()
        if item and item in self.inventory:
            self.inventory.remove(item)
            self.update_inventory()
            TradeCoordinator.register_offer(self.trader_name, item)
        self.offer_entry.delete(0, tk.END)

    def accept_selected_offer(self):
        # Get the selected offer from the listbox
        selected_offer = self.trade_offers_list.curselection()

        if selected_offer:
            offer_text = self.trade_offers_list.get(selected_offer[0])
            trader2, item2 = offer_text.split(": ")
            item2 = item2.strip()

            # Lock the offer while interacting with it
            self.locked_offers.add(offer_text)

            # Accept the trade
            item1 = TradeCoordinator.accept_offer(self.trader_name, trader2, item2)

            if item1:
                self.inventory.append(item1)
                self.update_inventory()
                self.update_trade_log()  # Update trade log with the accepted trade
                save_data(data)

            # Unlock the offer once the trade is completed
            self.locked_offers.remove(offer_text)

    def simulate_trading(self):
        """Simulate trades every 2 seconds."""
        self.trade_simulation_id = self.root.after(2000, self.execute_trade)

    def execute_trade(self):
        """Perform trade between two traders with a 2-second interval."""
        trader_names = list(data["traders"].keys())
        trader1 = random.choice(trader_names)
        trader2 = random.choice([t for t in trader_names if t != trader1])

        # Simulate the trade action
        item1 = random.choice(data["traders"][trader1])
        item2 = random.choice(data["traders"][trader2])

        print(f"Simulating trade: {trader1} offers {item1} to {trader2} for {item2}")

        # Register the offer and accept the trade
        TradeCoordinator.register_offer(trader1, item1)
        TradeCoordinator.accept_offer(trader2, trader1, item2)

        # Continue trading every 2 seconds
        self.simulate_trading()

    @staticmethod
    def refresh_all_trade_offers():
        for instance in TradingWindow.instances:
            instance.update_trade_offers()

    @staticmethod
    def refresh_all_trade_logs():
        for instance in TradingWindow.instances:
            instance.update_trade_log()

    def schedule_trade_offer_updates(self):
        """Schedule the real-time update task."""
        self.after_id = self.root.after(1000, self.update_trade_offers_realtime)

    def update_trade_offers_realtime(self):
        self.update_trade_offers()
        self.schedule_trade_offer_updates()

    def on_close(self):
        """Handle the close event of the window."""
        global active_windows

        # Cancel the `after` task to prevent invalid command errors
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        if self.trade_simulation_id is not None:
            self.root.after_cancel(self.trade_simulation_id)

        active_windows -= 1  # Decrement the counter

        # Save the state of the program when closing the window
        save_data(data)

        self.root.destroy()

class TradeCoordinator:
    @staticmethod
    def register_offer(trader, item):
        if trader not in data["offers"]:
            data["offers"][trader] = item
        TradingWindow.refresh_all_trade_offers()

    @staticmethod
    def accept_offer(trader1, trader2, item2):
        # Ensure the item to trade is available for trader1
        if item2 in data["traders"][trader2]:
            data["traders"][trader1].append(item2)
            data["traders"][trader2].remove(item2)

            # Update the trade log
            trade_entry = f"{trader1} traded {item2} for {item2}"
            data["trade_log"].append(trade_entry)

            TradingWindow.refresh_all_trade_logs()
            TradingWindow.refresh_all_trade_offers()

            return item2

        return None

# Create multiple trading windows
window1 = TradingWindow("Trader A's Window", "Trader_A", ["item1", "item2"])
window2 = TradingWindow("Trader B's Window", "Trader_B", ["item3", "item4"])

# Start the GUI loop
window1.root.mainloop()
window2.root.mainloop()
