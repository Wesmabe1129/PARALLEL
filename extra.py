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
        return {"trade_log": [], "offers": {}}

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



        active_windows -= 1  # Decrement the counter

        # Remove this instance from the instances list
        TradingWindow.instances.remove(self)

        # If only one window is left, end the program
        if active_windows <= 1:
            for instance in TradingWindow.instances:
                instance.root.destroy()  # Close remaining windows
            self.root.destroy()  # Close this window
            print("All trading windows are closed. Trading ended.")
        else:
            self.root.destroy()  # Just close this window


    def run(self):
        self.root.mainloop()


class TradeCoordinator:
    @staticmethod
    def register_offer(trader, item):
        lock.acquire()
        try:
            data["offers"][trader] = item
            save_data(data)
            TradingWindow.refresh_all_trade_offers()  # Refresh offers in all windows
            print(f'{trader} offer an Item: {item}')
        finally:
            lock.release()


    @staticmethod
    def accept_offer(trader1, trader2, item2):
        lock.acquire()
        try:
            if trader2 in data["offers"] and data["offers"][trader2] == item2:
                item1 = data["offers"].pop(trader2)
                log_entry = f"{trader1} traded {item1} with {trader2} for {item2}"
                data["trade_log"].append(log_entry)
                save_data(data)
                TradingWindow.refresh_all_trade_logs()  # Refresh logs in all windows
                TradingWindow.refresh_all_trade_offers()  # Refresh offers in all windows
                print(f'Done Transaction {trader1} get the Item: {item2} from {trader2}')
                
                return item1
            else:
                print("Trade Already !")
            return None
        
        finally:
            lock.release()
        








class LobbyWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lobby")
        self.root.geometry("400x300")

        # Welcome label
        WidgetGenerator.create_label(
            self.root, text="Welcome to the Trading Lobby", font=("Arial", 16), pack={"pady": 20}
        )

        # Buttons for navigation
        WidgetGenerator.create_button(
            self.root,
            text="Enter Trading Room",
            command=self.open_trading_room,
            pack={"pady": 10}
        )
        WidgetGenerator.create_button(
            self.root,
            text="Start New Trading Session",
            command=self.start_trading_session,
            pack={"pady": 10}
        )

        
    def open_trading_room(self):
        # Open the trading rooms
        self.root.destroy()
        main()

    def start_trading_session(self):
        # Initialize new trading session data
        global data
        data = {
            "trade_log": [],
            "offers": {},
            "traders": {
                "Trader_A": ["Gold", "Silver", "Bronze"],
                "Trader_B": ["Diamond", "Platinum", "Copper"],
                "Trader_C": ["Emerald", "Ruby", "Sapphire"],
                "Trader_D": ["Obsidian", "Amethyst", "Topaz"]
            }
        }
        save_data(data)

        # Open the trading rooms
        self.root.destroy()
        main()

    def run(self):
        self.root.mainloop()













def main():
    # Trader A's window
    global active_windows



    trader_a_items = data["traders"]["Trader_A"]
    trader_a_window = TradingWindow("Trader A", "Trader_A", trader_a_items)

    # Trader B's window
    # trader_b_items = ["Diamond", "Platinum", "Copper"]
    trader_b_items = data["traders"]["Trader_B"]
    trader_b_window = TradingWindow("Trader B", "Trader_B", trader_b_items)

    # Trader C's window
    # trader_c_items = ["Emerald", "Ruby", "Sapphire"]
    trader_c_items = data["traders"]["Trader_C"]
    trader_c_window = TradingWindow("Trader C", "Trader_C", trader_c_items)
    
    
    trader_d_items = data["traders"]["Trader_D"]
    trader_d_window = TradingWindow("Trader D", "Trader_D", trader_d_items)

    # Run all traders
    # threading.Thread(target=trader_a_window.run, daemon=True).start()
    # threading.Thread(target=trader_b_window.run, daemon=True).start()
    # threading.Thread(target=trader_c_window.run, daemon=True).start()

    # Keep the main thread running for the windows
    trader_a_window.root.mainloop()

if __name__ == "__main__":
    lobby = LobbyWindow()
    lobby.run()