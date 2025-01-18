import asyncio
import websockets
import os
import json

# WebSocketの接続ハンドラ
async def handler(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            try:
                # メッセージをJSON形式として解析
                received_data = json.loads(message)
                response = {
                    "cmd": "message",
                    "val": received_data.get("val", "No Value Received")
                }
                # クライアントに応答を送信
                await websocket.send(json.dumps(response))
                print(f"Sent: {response}")
            except json.JSONDecodeError:
                # 非JSONメッセージの場合、そのままエコー
                await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

# サーバーのメイン関数
async def main():
    # Render から提供される環境変数 PORT を取得
    port = int(os.getenv("PORT", 10000))  # デフォルト値は 10000
    print(f"Starting WebSocket server on port {port}")
    
    # WebSocket サーバーの起動
    server = await websockets.serve(handler, "0.0.0.0", port)
    await server.wait_closed()

# サーバーを実行
if __name__ == "__main__":
    asyncio.run(main())
