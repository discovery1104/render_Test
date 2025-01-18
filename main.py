import asyncio
import websockets
import json

async def handler(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            # JSON形式で解析
            try:
                received_data = json.loads(message)
                response = {
                    "cmd": "message",  # ws.jsが期待する形式に合わせる
                    "val": received_data.get("val", "No Value Received")
                }
                # メッセージを返送
                await websocket.send(json.dumps(response))
                print(f"Sent: {response}")
            except json.JSONDecodeError:
                # 非JSONデータの場合はそのままエコー
                await websocket.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")

async def main():
    server = await websockets.serve(handler, "localhost", 12345)
    print("Server running on ws://localhost:12345")
    await server.wait_closed()

asyncio.run(main())
