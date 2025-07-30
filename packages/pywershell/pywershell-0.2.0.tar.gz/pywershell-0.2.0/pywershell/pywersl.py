from typing import List

from async_property import AwaitLoader, async_cached_property
from asyncinit import asyncinit
from loguru import logger as log
from singleton_decorator import singleton
from pywershell import Gowershell, Response


class Pywersl(AwaitLoader):
    """
    Pywershell Windows System for Linux
    """
    PREFIX = "wsl"

    @async_cached_property
    async def version(self):
        # key = "wslinit"
        # cmd = " ".join(["echo", key])
        resp: Response = await Gowershell.execute("wsl --version")
        ver = resp.output.splitlines()
        wsl_vers: str = ver[0]
        item = f"{wsl_vers}"
        if not item in wsl_vers: raise RuntimeError
        wsl_vers_num: str = wsl_vers.replace("WSL version: ", "")
        log.success(f"{self}: Running WSL Version: {wsl_vers_num}")
        return wsl_vers_num

    async def run(self, cmd: str | list, headless: bool = True) -> Response | List[Response]:
        if isinstance(cmd, str): cmd = [cmd]
        resps: [Response] = []
        for cmd in cmd:
            resp = await Gowershell.execute(f"{self.PREFIX} {cmd}", headless=headless, persist_window=False)
            resps.append(resp)
            log.debug(resp)
        if len(resps) == 1:
            return resps[0]
        else:
            return resps


@singleton
@asyncinit
class Debian(Pywersl):
    CHECK = "--list --quiet"
    INSTALL = "--install Debian"
    POST_INSTALL = [
        "-d Debian -u root -- bash -c 'apt update && apt upgrade -y'",
        "-d Debian -u root -- bash -c 'apt install -y curl wget git unzip zip ca-certificates lsb-release software-properties-common build-essential'",
        "-d Debian -u root -- bash -c 'apt install -y python3 python3-pip python3-venv'",
        "-d Debian -u root -- bash -c 'apt install -y tmux htop neofetch ripgrep fd-find fzf'",
        "-d Debian -u root -- bash -c 'apt install -y docker.io docker-compose && usermod -aG docker $USER'",
        "-d Debian -u root -- bash -c 'echo Post-install complete'",
    ]
    UNINSTALL = ["--unregister Debian"]

    async def __init__(self):
        await self.setup
        self.PREFIX = "wsl -d Debian -u root -- bash -c"

    def __repr__(self):
        return f"[Pywersl.Debian]"

    @async_cached_property
    async def setup(self):
        resp = await self.run(self.CHECK)
        out = resp.output
        if "Debian" in out:
            log.success(f"{self}: Successfully initialized Debian!")
        else:
            await self.run(self.INSTALL, headless=False)
            await self.run(self.POST_INSTALL)

    async def uninstall(self):
        out = await self.run(self.UNINSTALL)
        if "The operation completed successfully." in out.str:
            log.warning(f"{self}: Successfully uninstalled!")
            return
        raise RuntimeWarning("{self}: Could not uninstall!")


async def preload():
    log.info(f"Attempting to preload Debian...")
    _ = await Debian()
