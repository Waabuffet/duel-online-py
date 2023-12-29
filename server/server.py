import asyncio
 
import websockets

playersConnected = 0

async def handler(websocket, path):
    print('player connected')
    if playersConnected == 0:
        reply = f"init-1"
        await websocket.send(reply)
    else:
        reply = f"init-2"
        await websocket.send(reply)
    
    data = await websocket.recv()
    reply = f"Data recieved as:  {data}!"
    await websocket.send(reply)

start_server = websockets.serve(handler, "localhost", 8123)
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()