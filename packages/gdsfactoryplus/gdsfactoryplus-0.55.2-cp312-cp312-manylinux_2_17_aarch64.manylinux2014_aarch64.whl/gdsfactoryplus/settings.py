"""Parse the GDSFactory+ settings."""

import os
from functools import cache
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray
from pydantic import Field, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

from gdsfactoryplus.project import maybe_find_docode_project_dir


class PdkSettings(BaseSettings):
    """PDK Settings."""

    name: str = "generic"

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class DrcSettings(BaseSettings):
    """DRC Settings."""

    timeout: int = 60
    host: str = "https://dodeck.gdsfactory.com"
    process: str = ""
    pdk: str = ""

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class ApiSettings(BaseSettings):
    """API Settings."""

    host: str = Field(
        default="https://prod.gdsfactory.com/",
        validation_alias="GFP_LANDING_PAGE_BASE_URL",
    )
    key: str = ""

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class ExternalSettings(BaseSettings):
    """External Settings."""

    model_config = SettingsConfigDict(
        extra="ignore",
    )

    axiomatic_api_key: str = ""

    @model_validator(mode="after")
    def validate_axiomatic_api_key(self) -> Self:
        """Get the axiomatic API key from the environment variable."""
        if "GFP_EXTERNAL_AXIOMATIC_API_KEY" in os.environ:
            self.axiomatic_api_key = os.environ["GFP_EXTERNAL_AXIOMATIC_API_KEY"]
        return self


class KwebSettings(BaseSettings):
    """Kweb Settings."""

    host: str = "localhost"
    https: bool = False

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class Linspace(BaseSettings):
    """A linear spacing definition."""

    min: float = 0.0
    max: float = 1.0
    num: int = 50

    model_config = SettingsConfigDict(
        extra="ignore",
    )

    @property
    def arr(self) -> NDArray[np.float64]:
        """Create array from linspace definition."""
        return np.linspace(self.min, self.max, self.num, dtype=np.float64)

    @property
    def step(self) -> float:
        """Get step between elements."""
        return float(self.arr[1] - self.arr[0])


class Arange(BaseSettings):
    """An array range definition."""

    min: float = 0.0
    max: float = 1.0
    step: float = 0.1

    model_config = SettingsConfigDict(
        extra="ignore",
    )

    @property
    def arr(self) -> NDArray[np.float64]:
        """Create array from arange definition."""
        return np.arange(self.min, self.max, self.step, dtype=np.float64)

    @property
    def num(self) -> int:
        """Get number of elements."""
        return int(self.arr.shape[0])


class SimSettings(BaseSettings):
    """Simulation Settings."""

    wls: Linspace | Arange = Field(
        default_factory=lambda: Linspace(min=1.5, max=1.6, num=300)
    )

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class GptSettings(BaseSettings):
    """GPT Settings."""

    host: str = "https://doitforme.gdsfactory.com"
    pdk: str = ""

    model_config = SettingsConfigDict(
        extra="ignore",
    )


class Settings(BaseSettings):
    """Settings."""

    name: str = ""
    ignore: list[str] = Field(default_factory=list)
    pdk: PdkSettings = Field(default_factory=PdkSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    drc: DrcSettings = Field(default_factory=DrcSettings)
    sim: SimSettings = Field(default_factory=SimSettings)
    gpt: GptSettings = Field(default_factory=GptSettings)
    kweb: KwebSettings = Field(default_factory=KwebSettings)
    external: ExternalSettings = Field(default_factory=ExternalSettings)

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "gdsfactoryplus"),
        env_prefix="GFP_",
        env_nested_delimiter="_",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Add global gdsfactoryplus.toml and local pyproject.toml to the sources."""
        sources = [init_settings, env_settings, dotenv_settings, file_secret_settings]
        sources.append(
            PyprojectTomlConfigSettingsSource(
                settings_cls=settings_cls,
                toml_file=Path("~").expanduser().resolve()
                / ".gdsfactory"
                / "gdsfactoryplus.toml",
            )
        )
        project_dir = maybe_find_docode_project_dir()
        if project_dir is not None:
            sources.append(
                PyprojectTomlConfigSettingsSource(
                    settings_cls=settings_cls,
                    toml_file=Path(project_dir).resolve() / "pyproject.toml",
                )
            )
        return tuple(sources)

    def _validate_ignore(self) -> Self:
        # expand glob patterns in ignore list
        """Expand glob patterns in ignore list."""
        repodir = Path(maybe_find_docode_project_dir() or ".").resolve()
        picsdir = repodir / self.name
        new = []
        for pattern in self.ignore:
            for path in picsdir.glob(pattern):
                fn = str(path.resolve().relative_to(picsdir))
                new.append(fn)
        self.ignore = new
        return self

    def _validate_name(self) -> Self:
        """Get the name from the pyproject.toml [project] section."""
        if self.name:
            return self
        project_settings = ProjectSettings()
        self.name = project_settings.name
        return self

    @model_validator(mode="after")
    def _validate(self) -> Self:
        """Run validations after all fields are set."""
        # order is important here.
        self._validate_name()
        self._validate_ignore()
        return self


class ProjectSettings(BaseSettings):
    """Settings."""

    name: str = "pics"
    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("project",),
        env_prefix="GFP_PROJECT_",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Read the [project] section of the pyproject.toml."""
        sources = [init_settings, env_settings, dotenv_settings, file_secret_settings]
        project_dir = maybe_find_docode_project_dir()
        if project_dir is not None:
            sources.append(
                PyprojectTomlConfigSettingsSource(
                    settings_cls=settings_cls,
                    toml_file=Path(project_dir).resolve() / "pyproject.toml",
                )
            )
        return tuple(sources)


@cache
def get_settings() -> Settings:
    """Get the gdsfactoryplus settings."""
    return Settings()
