#!/usr/env python3

import sys
import subprocess
import time
import asyncio
from caproto.asyncio.client import Context

async def main():
    async def new_context():
        return Context()

    ctx = await new_context()
    x = await ctx.get_pvs('counter:x')
    sub = x[0].subscribe()
    res = await x[0].read()
    
    responses = []
    def f(sub, response):
        print('Recieved response from', sub.pv.name)
        responses.append(response)
    
    token = sub.add_callback(f)

    values = []
    def g(sub, response):
        values.append(response.data[0])
        print('Recieved value', values[len(values)-1])

    sub.add_callback(g)

    # The subscriber remains until the program is stopped
    while True:
        await asyncio.sleep(30)

    await sub.remove_callback(token)

    await sub.clear()

if __name__ == "__main__":
    asyncio.run(main())
