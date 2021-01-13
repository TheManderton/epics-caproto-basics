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
    x = await ctx.get_pvs('13SIM1:Proc1:TIFF:Capture')
    sub = x[0].subscribe()
    res = await x[0].read()
   
    print(res.data[0])

    responses = []
    def f(sub, response):
        print('Recieved response from', sub.pv.name)
        responses.append(response)
    
    token = sub.add_callback(f)

    values = []
    currentVal = 0
    def g(sub, response):
        values.append(response.data[0])
        currentVal = values[len(values)-1]
        print('Recieved value', currentVal)

    sub.add_callback(g)
    # --- Function calls go here --- #
    await resetWhen(x,currentVal, 10)

    # The subscriber remains until the program is stopped
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
