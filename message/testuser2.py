# import asyncio
# import websockets
# import json

# async def send_message():
#     async with websockets.connect('ws://localhost:8000/ws/users/1/chat/') as websocket:
#         message = {
#             'action': 'message',
#             'roomId': 'Vu4uXgtQtVEcPRY8G9MAow',  # Replace with the actual room ID
#             'message': 'Hello, world!',
#             'user': 1,  # Replace with the actual user ID
#         }
#         await websocket.send(json.dumps(message))
#         response = await websocket.recv()
#         print("Received response:", response)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_message())
#     loop.close()

import asyncio
import json
import websockets
async def send_message():
    async with websockets.connect('ws://localhost:8000/ws/users/1/chat/') as websocket:
        start = True
        while True:
            message = {
                'action': 'message',
                'roomId': 'Vu4uXgtQtVEcPRY8G9MAow',  # Replace with the actual room ID
                'message': 'Hello, world!',
                'user': 1,  # Replace with the actual user ID
            }
            if start:
                await websocket.send(json.dumps(message))
                start = False
            response = await websocket.recv()
            # print("Received response:", response)
            
                
             # Handle received messages
            try:
                message_data = json.loads(response)
                sender_user_id = message_data.get('user')
                
                if sender_user_id is not None and sender_user_id != 1:
                    print(f"Received message from user {sender_user_id}: {response}")
                    
                    # Allow the user to write back
                    user_response = input("Write your response (or type 'exit' to end): ")
                    if user_response.lower() == 'exit':
                        break
                    
                    # Send the user's response back to the WebSocket
                    reply_message = {
                        'action': 'message',
                        'roomId': 'Vu4uXgtQtVEcPRY8G9MAow',
                        'message': user_response,
                        'user': 1,
                    }
                    await websocket.send(json.dumps(reply_message))
                        
            except json.JSONDecodeError:
                print("Received non-JSON message:", response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

