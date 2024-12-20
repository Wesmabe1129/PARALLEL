import asyncio
import websockets
import json

# Server-side data
data = {
    "trade_log": [],
    "offers": {
        "Trader_A": "Gold",
        "Trader_B": "Diamond",
        "Trader_C": "Emerald",
        "Trader_D": "Obsidian"
    },
    "type": "update_offers",
    "traders": {
        "Trader_A": [
            "Gold",
            "Silver",
            "Bronze"
        ],
        "Trader_B": [
            "Diamond",
            "Platinum",
            "Copper"
        ],
        "Trader_C": [
            "Emerald",
            "Ruby",
            "Sapphire"
        ],
        "Trader_D": [
            "Obsidian",
            "Amethyst",
            "Topaz"
        ]
    }

}

connected_clients = set()

async def broadcast(message):
    """Broadcast a message to all connected clients."""
    if connected_clients:
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handle_client(websocket):
    """Handle individual client connections."""
    connected_clients.add(websocket)
    try:
        # Send initial data to the client
        await websocket.send(json.dumps(data))

        async for message in websocket:
            request = json.loads(message)
            action = request.get("action")

            if action == "offer_item":
                trader, item = request["trader"], request["item"]
                data["offers"][trader] = item
                await broadcast(json.dumps({"type": "update_offers", "offers": data["offers"]}))

            elif action == "accept_offer":
                trader1, trader2, item2 = request["trader1"], request["trader2"], request["item2"]
                if trader2 in data["offers"] and data["offers"][trader2] == item2:
                    item1 = data["offers"].pop(trader2)
                    data["trade_log"].append(f"{trader1} traded {item1} with {trader2} for {item2}")
                    await broadcast(json.dumps({
                        "type": "update_all",
                        "offers": data["offers"],
                        "trade_log": data["trade_log"]
                    }))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
