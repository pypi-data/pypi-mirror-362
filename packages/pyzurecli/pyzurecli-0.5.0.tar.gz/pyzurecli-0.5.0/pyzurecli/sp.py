import uuid
from functools import cached_property
from pathlib import Path
from types import SimpleNamespace

from async_property import AwaitLoader, async_cached_property
from loguru import logger as log
from pywershell import CMDResult

from .util import json_to_dataclass
from pyzurecli import AzureCLI, az
from .user import ServicePrincipalCreds, ServicePrincipalContext
from dockwershell import Docker, DockerImage, path_to_wsl, path_to_mnt

class AzureCLIServicePrincipal(AwaitLoader):
    instances = {}
    dockerfile: str = """
    FROM mcr.microsoft.com/azure-cli
    WORKDIR /app
    """

    def __init__(self, azure_cli: az):
        self.azure_cli: AzureCLI = azure_cli
        self.dir: Path = azure_cli.dir
        self.user: DockerImage = azure_cli.user.image
        _ = self.paths
        # log.success(f"{self}: Successfully initialized!")

    def __repr__(self):
        return f"[{self.azure_cli.dir.name.title()}.AzureCLI.ServicePrincipal]"

    @cached_property
    def paths(self) -> SimpleNamespace:
        dir: Path = self.dir / "azure" / "sp" #type-ignore
        dir.mkdir(exist_ok=True, parents=True)

        dockerfile_path: Path = dir / "Dockerfile.sp"
        dockerfile_path.touch(exist_ok=True)
        with open(dockerfile_path, "w", encoding="utf-8") as f: f.write(self.dockerfile)

        azure_config: Path = dir / ".azure"
        azure_config.mkdir(exist_ok=True)
        azure_cmds: Path = azure_config / "commands"
        azure_cmds.mkdir(exist_ok=True)

        return SimpleNamespace(
            dir=dir,
            dockerfile=dockerfile_path,
            azure_config=azure_config
        )

    @async_cached_property
    async def creds(self) -> ServicePrincipalCreds | str:
        log.debug(f"{self}: Attempting to get service principal credentials...")
        meta = await self.azure_cli.metadata
        data = await self.user.run(
            f"az ad sp create-for-rbac -n mileslib --role Contributor --scope /subscriptions/{meta.subscription_id} --output json",
            headless=True)
        log.success(f"$$$$$$$$${data.json}")
        if not data.json: log.warning(f"{self}: Could not extract json for service principal credentials!")
        creds = json_to_dataclass(ServicePrincipalCreds, data.json[0])
        if creds.appId: log.success(f"{self}: Successfully initialized service principal in AzureCLI!")
        return creds

    @async_cached_property
    async def run_args(self):
        creds: ServicePrincipalCreds = await self.creds
        dir_wsl = path_to_wsl(self.paths.dir)
        cfg_wsl = path_to_wsl(self.paths.azure_config)
        cmd = f"-v {dir_wsl}:/app -v {cfg_wsl}:/root/.azure -e AZURE_CONFIG_DIR=/root/.azure -w /app"
        env = [
            f"-e AZURE_CLIENT_ID={creds.appId}",
            f"-e AZURE_CLIENT_SECRET={creds.password}",
            f"-e AZURE_TENANT_ID={creds.tenant}"
        ]
        cmd = f"{cmd} {" ".join(env)}"
        return cmd

    @async_cached_property
    async def image(self):
        inst: DockerImage = await DockerImage(self.paths.dockerfile, run_args=await self.run_args, rebuild=True)
        return inst

    @async_cached_property
    async def login(self):
        image: DockerImage = await self.image
        creds: ServicePrincipalCreds = await self.creds
        cmd = (
            f"az login --service-principal "
            f"--username {creds.appId} "
            f"--password {creds.password} "
            f"--tenant {creds.tenant}"
        )
        out = await image.run(cmd, headless=True)
        subscription_data = out.json[0] if isinstance(out.json, list) else out.json
        ses = json_to_dataclass(ServicePrincipalContext, subscription_data)
        return ses
