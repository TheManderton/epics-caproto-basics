import caproto
import asyncio
from caproto.asyncio.client import Context

class Poller:
    def __init__(self):
        self.val = 0
        self.ctx = None

    async def poll(self, pvName):
        pv = await self.ctx.get_pvs(pvName)
        read = await pv[0].read()
        val = read.data[0]
        print(pvName, " == ", val)
        self.val = val
        return val

    async def main(self):
        async with Context() as self.ctx:
            await self.poll("A")
            await self.poll("B")
            await self.poll("C")
            await self.poll("D")

if __name__ == "__main__":
    p = Poller()
    asyncio.run(p.main())
