#!/usr/bin/env python3
import array
import asyncio
from caproto.threading.client import Context
from caproto.server import (pvproperty, PVGroup, pvfunction, ioc_arg_parser,
                            run)

SLEEP_TIME = 1

async def main():
    ctx = Context()
    x = pvproperty(value=0.0)
    #pv_name = "13SIM1:Proc1:TIFF:Capture"
    #pv_name = '13SIM1:Proc1:cam1:YSine2Phase_RBV'
    pv_name = "13SIM1:cam1:AcquireTime"

    # Infinite loop for continuous monitoring
    while True:
        # Get the PV context and value
        pv = ctx.get_pvs(pv_name)[0]
        val = pv.read().data[0]
        pv.write(0)
        print(val)
        if(val):
            pv.write(0)
        else:
            pv.write(1)

        await asyncio.sleep(SLEEP_TIME)

if __name__ == '__main__':
    while True:
        asyncio.run(main())
