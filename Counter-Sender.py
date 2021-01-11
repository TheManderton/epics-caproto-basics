#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run

class CounterSender(PVGroup):
    x = pvproperty(value=0.0)

    @x.startup
    async def x(self, instance, async_lib):
        'Periodically update the value'
        while True:
            # compute next value
            x = self.x.value + 1

            # update the ChannelData instance and notify any subscribers
            await instance.write(value=x)
            
            # make the counter sleep until the next timestep
            await async_lib.library.sleep(1)

if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
            default_prefix='counter:',
            desc='Run an IOC with an increasing value.')
    ioc = CounterSender(**ioc_options)
    run(ioc.pvdb, **run_options)
