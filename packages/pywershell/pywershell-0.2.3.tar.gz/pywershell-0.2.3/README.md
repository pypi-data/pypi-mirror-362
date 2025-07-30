<!-- README.md -->
# Pywershell

Async PowerShell session manager for Python.

## Install

```python
import asyncio
from pywershell.pywershell import PywershellLive

async def main():
    shell = await PywershellLive(verbose=True)
    # Run a command and await its completion
    result = await shell.run("Get-Process | Select-Object -First 5")
    print("Exit code:", result.code)
    print("Output:", result.str)
    await shell.close()

asyncio.run(main())
```