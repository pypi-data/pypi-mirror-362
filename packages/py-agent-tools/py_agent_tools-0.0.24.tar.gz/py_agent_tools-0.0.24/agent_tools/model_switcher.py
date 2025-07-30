from collections import defaultdict

from pydantic import BaseModel

from agent_tools._log import log
from agent_tools.agent_base import AgentBase, ModelNameBase
from agent_tools.ark_agent import ArkAgent, ArkCredentialPool, ArkModelName
from agent_tools.azure_agent import AzureAgent, AzureCredentialPool, AzureModelName
from agent_tools.bailian_agent import BailianAgent, BailianCredentialPool, BailianModelName
from agent_tools.credential_pool_base import CredentialPoolBase, CredentialPoolProtocol
from agent_tools.laozhang_agent import LaozhangAgent, LaozhangCredentialPool, LaozhangModelName
from agent_tools.openai_agent import OpenAIAgent, OpenAICredentialPool, OpenAIModelName
from agent_tools.vertex_agent import VertexAgent, VertexCredentialPool, VertexModelName


class ProviderMapping(BaseModel):
    provider: str
    agent_cls: type[AgentBase]
    local_credential_pool_cls: type[CredentialPoolProtocol]
    model_name_enum: type[ModelNameBase]


class ModelSwitcher:
    def __init__(self, allowed_providers: list[str], using_remote_credential_pools: bool = False):
        self._using_remote_credential_pools = using_remote_credential_pools
        self._allowed_providers = allowed_providers
        self._credential_pools: defaultdict[str, dict[str, CredentialPoolProtocol]] = defaultdict(
            dict
        )

    @property
    def _provider_mapping(self) -> dict[str, ProviderMapping]:
        return {
            'ark': ProviderMapping(
                provider='ark',
                agent_cls=ArkAgent,
                local_credential_pool_cls=ArkCredentialPool,
                model_name_enum=ArkModelName,
            ),
            'azure': ProviderMapping(
                provider='azure',
                agent_cls=AzureAgent,
                local_credential_pool_cls=AzureCredentialPool,
                model_name_enum=AzureModelName,
            ),
            'bailian': ProviderMapping(
                provider='bailian',
                agent_cls=BailianAgent,
                local_credential_pool_cls=BailianCredentialPool,
                model_name_enum=BailianModelName,
            ),
            'openai': ProviderMapping(
                provider='openai',
                agent_cls=OpenAIAgent,
                local_credential_pool_cls=OpenAICredentialPool,
                model_name_enum=OpenAIModelName,
            ),
            'vertex': ProviderMapping(
                provider='vertex',
                agent_cls=VertexAgent,
                local_credential_pool_cls=VertexCredentialPool,
                model_name_enum=VertexModelName,
            ),
            'laozhang': ProviderMapping(
                provider='laozhang',
                agent_cls=LaozhangAgent,
                local_credential_pool_cls=LaozhangCredentialPool,
                model_name_enum=LaozhangModelName,
            ),
        }

    def get_credential_pool(self, provider: str, model_name: str) -> CredentialPoolProtocol:
        """Get credential pool for a specific model."""
        if provider not in self._credential_pools:
            raise ValueError(f"Provider '{provider}' not found")
        if model_name not in self._credential_pools[provider]:
            raise ValueError(f"Model '{model_name}' not found for provider '{provider}'")
        return self._credential_pools[provider][model_name]

    def get_agent_cls(self, provider: str) -> type[AgentBase]:
        """Get agent for a specific model."""
        mapping = self._provider_mapping.get(provider, None)
        if mapping is None:
            raise ValueError(f"Provider '{provider}' not found")
        return mapping.agent_cls

    async def start_all_pools(self):
        """Start all credential pools for health checking."""
        for provider, mapping in self._provider_mapping.items():
            if provider not in self._allowed_providers:
                continue
            for model_name in mapping.model_name_enum:
                if self._using_remote_credential_pools:
                    raise NotImplementedError("Remote credential pools are not implemented yet")
                else:
                    pool = mapping.local_credential_pool_cls(target_model=model_name)
                    if isinstance(pool, CredentialPoolBase):
                        await pool.start()
                    else:
                        log.warning(f"Pool {pool} is not a CredentialPoolBase")
                self._credential_pools[provider][model_name.value] = pool

    def stop_all_pools(self):
        """Stop all credential pools."""
        for provider, pools in self._credential_pools.items():
            for pool in pools.values():
                if isinstance(pool, CredentialPoolBase):
                    pool.stop()


if __name__ == "__main__":
    import asyncio

    async def test_model_switcher():
        """Test the ModelSwitcher functionality."""

        # from agent_tools.settings import ModelProvider

        # allowed_providers = [provider.value for provider in ModelProvider]
        allowed_providers = ['ark', 'azure', 'bailian', 'laozhang']
        switcher = ModelSwitcher(allowed_providers=allowed_providers)
        await switcher.start_all_pools()
        switcher.stop_all_pools()

    try:
        asyncio.run(test_model_switcher())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("Tests completed successfully (cleanup warning ignored)")
        else:
            raise
