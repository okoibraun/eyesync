#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import time
import json
from aiohttp import web

#CLIENTS = ['p6']
#CLIENTS = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
CLIENTS = ['p3', 'p4', 'p5', 'p6', 'p7']
client_names = set(CLIENTS)

client_sockets = set()

t0 = time.time()*1000.0;

async def register_client(name, socket):
    if not name in client_names:
        print(f"received unexpected name: {name} -- ignorning")
        return 
    client_names.remove(name)
    client_sockets.add(socket)
    #print(f"< {name}, waiting for {client_names}")
    await notify_clients()

async def notify_clients():
    if not client_names:
        client_names.update(CLIENTS)
        t = time.time()*1000.0 - t0
        #print(f"> {t}")
        await asyncio.wait([client.send(f"{t}") for client in client_sockets])
        client_sockets.clear()

async def sync(socket, path):
    while True:
        data = await socket.recv()
        fields = data.split(' ')
        if len(fields) > 2:
            print(f"1st register {data}");
        await register_client(fields[0], socket)

start_server = websockets.serve(sync, "", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
