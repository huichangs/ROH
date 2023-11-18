import asyncio
import websockets

async def handle_websocket(websocket, path):
    try:
        while True:
            message_from_client = await websocket.recv()
            print(f"Received message from client: {message_from_client}")

            # 서버에서 메시지 처리 (예: 로그에 기록)
            # 여기에서 데이터를 원하는대로 처리하고 필요한 동작을 수행할 수 있습니다.

            # 처리된 결과를 다시 클라이언트에게 전송
            response_data = {'response': 'Message received successfully'}
            await websocket.send(response_data)
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")

start_server = websockets.serve(handle_websocket, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
