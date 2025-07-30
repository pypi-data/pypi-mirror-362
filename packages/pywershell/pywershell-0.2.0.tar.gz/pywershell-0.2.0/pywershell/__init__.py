import asyncio

from gowershell import Response, Gowershell

CMDResult = Response
PywershellLive = Gowershell

from .pywersl import Debian, preload

Pywersl = Debian
Pywersl.distro = Debian
asyncio.run(preload())
