import tkinter as tk
import threading
import json
import asyncio
import websockets

class TradingClient:
    def __init__(self, trader_name):
        self.trader_name = trader_name
        self.inventory = []
        self.offers = {}
        self.trade_log = []
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)


        self.root = tk.Tk()
        self.root.title(f"Trading Client - {trader_name}")

        # Inventory
        tk.Label(self.root, text=f"{trader_name}'s Inventory", font=("Arial", 16)).pack(pady=10)
        self.inventory_list = tk.Listbox(self.root)
        self.inventory_list.pack(pady=5)

        # Offer section
        self.offer_entry = tk.Entry(self.root)
        self.offer_entry.pack(pady=5)
        tk.Button(self.root, text="Offer Item", command=self.offer_item).pack(pady=5)

        # Offers
        tk.Label(self.root, text="Available Trade Offers", font=("Arial", 14)).pack(pady=10)
        self.trade_offers_list = tk.Listbox(self.root)
        self.trade_offers_list.pack(pady=5)
        tk.Button(self.root, text="Accept Offer", command=self.accept_offer).pack(pady=5)

        # Trade log
        tk.Label(self.root, text="Trade Log", font=("Arial", 14)).pack(pady=10)
        self.trade_log_list = tk.Listbox(self.root)
        self.trade_log_list.pack(pady=5)

    def offer_item(self):
        item = self.offer_entry.get()
        if item and item in self.inventory:
            self.inventory.remove(item)
            self.update_inventory()
            # asyncio.run_coroutine_threadsafe(
            #     self.send_message({
            #         "action": "offer_item",
            #         "trader": self.trader_name,
            #         "item": item
            #     }),
            #     self.loop
            # )
        self.offer_entry.delete(0, tk.END)

    def accept_offer(self):
        selected = self.trade_offers_list.curselection()
        if selected:
            offer_text = self.trade_offers_list.get(selected[0])
            trader2, item2 = offer_text.split(": ")
            asyncio.run_coroutine_threadsafe(
                self.send_message({
                    "action": "accept_offer",
                    "trader1": self.trader_name,
                    "trader2": trader2,
                    "item2": item2
                }),
                self.loop
            )

    def update_inventory(self):
        self.inventory_list.delete(0, tk.END)
        for item in self.inventory:
            self.inventory_list.insert(tk.END, item)

    def update_offers(self):
        self.trade_offers_list.delete(0, tk.END)
        for trader, item in self.offers.items():
            if trader != self.trader_name:
                self.trade_offers_list.insert(tk.END, f"{trader}: {item}")

    def update_trade_log(self):
        self.trade_log_list.delete(0, tk.END)
        for log in self.trade_log:
            self.trade_log_list.insert(tk.END, log)

    async def connect(self):
        async with websockets.connect("ws://localhost:6789") as websocket:
            self.websocket = websocket
            await self.send_message({"action": "join", "trader": self.trader_name})
            async for raw_message in websocket:
                try:
                    print(f"Received: {raw_message}")
                    message = json.loads(raw_message)
                    self.handle_message(message)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode message: {raw_message}, Error: {e}")


    def handle_message(self, message):
        try:
            message_type = message.get("type")
            if message_type == "update_offers":
                self.offers = message.get("offers", {})
                self.update_offers()
            elif message_type == "update_all":
                self.offers = message.get("offers", {})
                self.trade_log = message.get("trade_log", [])
                self.update_offers()
                self.update_trade_log()
            else:
                print(f"Unknown message type: {message_type}")
        except Exception as e:
            print(f"Error handling message: {message}, Error: {e}")

    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))

    def start(self):
        # Load initial inventory
        self.inventory = ["Gold", "Silver", "Bronze"] if self.trader_name == "Trader_A" else []
        self.update_inventory()

        # Start WebSocket communication in a separate thread
        threading.Thread(target=lambda: self.loop.run_until_complete(self.connect()), daemon=True).start()

        # Start Tkinter event loop
        self.root.mainloop()


if __name__ == "__main__":
    client = TradingClient("Trader_A")
    client.start()
