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
    pv_name = "counter:x"
   

    # Infinite loop for continuous monitoring
    while True:
        # Get the PV context and value
        pv = ctx.get_pvs(pv_name)[0]
        val = pv.read().data[0]
        print(val)

        await asyncio.sleep(SLEEP_TIME)
        await example(val, ctx, pv_name)

async def example(val, ctx, pv_name):
    # Additional functionality examples
    # Explained:
    # Once the counter reaches 20 it is paused for 5 seconds
    # It is reset to 0
    # Every time it is reset the step is increased by one
    if(val > 20):
        await pauseFixedTime(ctx.get_pvs('counter:pause')[0], 5) # pause example
        reset(ctx.get_pvs(pv_name)[0])
        print(getRate(pv_name, ctx))
        setStep(ctx.get_pvs('counter:step')[0], getStep(ctx.get_pvs('counter:step')[0])+1)

# - Pause
def pause(pv):
    pv.write([1])
    return True

def unPause(pv):
    pv.write([0])
    return True

async def pauseFixedTime(pv, timeLimit):
    isPaused = pause(pv)
    await asyncio.sleep(timeLimit)
    isPaused = unPause(pv) 
    return isPaused

# Rate is not a pv in its own right, so requires the pv name
# in order to retrive the pv's SCAN value

def getRate(pv_name, ctx):
    return ctx.get_pvs(pv_name+'.SCAN')[0].read().data[0]

def getRateDef(rate):
    definition = ""
    if(rate == 0):
        definition = "Passive"
    elif(rate == 1):
        definition = "Event"
    elif(rate == 2):
        definition = "I/O Interrupt"
    elif(rate == 3):
        definition = "10 second"
    elif(rate == 4):
        definition = "5 second"
    elif(rate == 5):
        definition = "2 second"
    elif(rate == 6):
        definition = "1 second"
    elif(rate == 7):
        definition = "0.2 second"
    elif(rate == 8):
        definition = "0.1 second"
    else:
        definition = "Rate out of range"
    return definition

def setRate(pv_name, ctx, newRate):
    isSet = False
    ctx.get_pvs(pv_name+'.SCAN')[0].write([int(newRate)])
    isSet = True
    return isSet

def getStep(pv):
    return pv.read().data[0]
        
# - Change step
def setStep(pv, newStep):
    isSet = False
    pv.write([float(newStep)])
    isSet = True
    return isSet

def reset(pv):
    pv.write([0])
    return True

def resetWhen(pv, resetWhen):
    # The counter is reset to zero if it is reaches a certian value
    isReset = False # Used to return true if the value has been reset
    if(pv.read().data[0] >= resetWhen):
       pv.write([float(0)])
       isReset = True
    return isReset

def resetToChoiceWhen(pv, resetWhen, resetTo):
    # The counter is reset to a chosen value if it is reaches a certian value
    isReset = False # Used to return true if the value has been reset
    if(pv.read().data[0] >= resetWhen):
       pv.write([float(resetTo)])
       isReset = True
    return True

if __name__ == '__main__':
    asyncio.run(main())
