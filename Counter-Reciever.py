#!/usr/bin/env python3
import array
import asyncio
from caproto.threading.client import Context
from caproto.server import (pvproperty, PVGroup, pvfunction, ioc_arg_parser,
                            run)
async def main():
    ctx = Context()
    x = pvproperty(value=0.0)
    pv_name = "counter:x"
    
    while True:
        x = ctx.get_pvs(pv_name)[0].read().data
        print(x[0])
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
