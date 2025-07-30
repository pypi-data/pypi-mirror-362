import asyncio
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from async_property import AwaitLoader, async_cached_property
from loguru import logger as log
import time
from asyncinit import asyncinit
from singleton_decorator import singleton

@dataclass
class GraphToken:
    accessToken: str
    expiresOn: str
    expires_on: str
    subscription: str
    tenant: str
    tokenType: str

@singleton
@asyncinit
class AzureCLI(AwaitLoader):
    instance = None

    async def __init__(self, dir: Path):
        self.dir = dir
        _ = await self.user
        _ = await self.service_principal
        _ = await self.app_registration
        log.success(f"{self}: Successfully initialized!")

    def __repr__(self):
        return f"[{self.dir.name.title()}.AzureCLI]"

    @async_cached_property
    async def user(self):
        from pyzurecli.user import AzureCLIUser
        return await AzureCLIUser.__async_init__(self)

    @async_cached_property
    async def service_principal(self):
        return await self.user.sp_from_user(self)

    @async_cached_property
    async def app_registration(self):
        from pyzurecli.app_registration import AzureCLIAppRegistration
        return await AzureCLIAppRegistration.__async_init__(self)

    @async_cached_property
    async def metadata(self) -> SimpleNamespace:
        from pyzurecli.user import UserSession #abandoned rel imports lol
        ses: UserSession = await self.user.azure_profile
        if ses is None:
            try:
                ses: UserSession = await self.user.azure_profile
                log.debug(ses)
            except ses is None: raise RuntimeError(f"{self}: UserSession returned '{ses}', "
                                           f"which is unreadable! "
                                           f"Either your login failed or there was "
                                           f"an async race condition... Try restarting."
                                           )
        subscription = ses.subscriptions[0]
        subscription_id = subscription.id
        tenant_id = subscription.tenantId
        return SimpleNamespace(
            user=ses,
            subscription_id=subscription_id,
            tenant_id=tenant_id
        )

async def debug():
    await AzureCLI(Path.cwd())

if __name__ == "__main__":
    asyncio.run(debug())
    time.sleep(500)
