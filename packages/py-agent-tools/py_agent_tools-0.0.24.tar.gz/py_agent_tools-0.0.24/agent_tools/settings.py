"""
Settings for the agent_utils package.

This module contains the settings for the agent_utils package.

The settings are loaded from the environment variables.

"""

import json
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from util_common.pydantic_util import show_settings_as_env

from agent_tools._log import log


class ModelProvider(Enum):
    ARK = "ark"
    AZURE = "azure"
    BAILIAN = "bailian"
    OPENAI = "openai"
    VERTEX = "vertex"
    LAOZHANG = "laozhang"


class SupportedModel(BaseModel):
    model_name: str = Field(default="")
    deployment: str = Field(default="")
    api_version: str = Field(default="")


class AccountCredential(BaseModel):
    account_id: str = Field(default="")
    group_id: str = Field(default="")
    base_url: str = Field(default="")
    api_key: str = Field(default="")
    account_info: dict = Field(default_factory=dict)
    supported_models: list[SupportedModel] = Field(default_factory=list)


class ProviderSettingsBase(BaseSettings):
    """Base class for provider settings that automatically sets credential path."""

    credential_path: Path = Field(default=Path(""))

    def __init__(self, resource_root: Path | None = None, **kwargs):
        super().__init__(**kwargs)
        self._setup_credential_path(resource_root)

    def _setup_credential_path(self, resource_root: Path | None = None):
        """Setup the credential path based on the provider name."""
        provider_name = self.__class__.__name__.lower().replace('settings', '')
        base_path = Path(f"credentials/model_providers/{provider_name}.json")
        self.credential_path = resource_root / base_path if resource_root else base_path

    @property
    def credentials(self) -> list[AccountCredential]:
        try:
            if not self.credential_path.exists():
                raise FileNotFoundError(
                    f"{self.__class__.__name__} credentials file not found at "
                    f"{self.credential_path}"
                )
            with self.credential_path.open() as f:
                data = json.load(f)
            return [AccountCredential(**cred) for cred in data]
        except FileNotFoundError as e:
            log.warning(f"{e}")
            return []
        except json.JSONDecodeError as e:
            log.error(f"Invalid JSON in {self.credential_path}: {e}")
            return []


class AzureSettings(ProviderSettingsBase):
    """Azure OpenAI configuration settings."""

    model_config = SettingsConfigDict(env_prefix="AZURE_")


class ArkSettings(ProviderSettingsBase):
    """Ark configuration settings."""

    model_config = SettingsConfigDict(env_prefix="ARK_")


class OpenAISettings(ProviderSettingsBase):
    """OpenAI configuration settings."""

    model_config = SettingsConfigDict(env_prefix="OPENAI_")


class VertexSettings(ProviderSettingsBase):
    """Google Vertex configuration settings."""

    model_config = SettingsConfigDict(env_prefix="VERTEX_")


class BailianSettings(ProviderSettingsBase):
    """Bailian configuration settings."""

    model_config = SettingsConfigDict(env_prefix="BAILIAN_")


class LaozhangSettings(ProviderSettingsBase):
    """Laozhang configuration settings."""

    model_config = SettingsConfigDict(env_prefix="LAOZHANG_")


class AgentSettings(BaseSettings):
    """Main settings class that combines all settings."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="allow",
    )

    resource_root: Path = Field(
        default=Path("/mnt/ssd1/resource"),
        description="Root path for all resource files",
    )

    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    azure: AzureSettings = Field(default_factory=AzureSettings)
    ark: ArkSettings = Field(default_factory=ArkSettings)
    vertex: VertexSettings = Field(default_factory=VertexSettings)
    bailian: BailianSettings = Field(default_factory=BailianSettings)
    laozhang: LaozhangSettings = Field(default_factory=LaozhangSettings)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_credential_paths()

    def _update_credential_paths(self):
        """Update credential paths to use the resource root."""
        for provider in ModelProvider:
            provider_settings = getattr(self, provider.value)
            provider_settings.__init__(resource_root=self.resource_root)


agent_settings = AgentSettings()
show_settings_as_env(agent_settings)
