"""GDSFactory+ Pydantic models."""

from pathlib import Path
from typing import Annotated, Any, Literal, TypeAlias

from gdsfactory.read.from_yaml import from_yaml
from pydantic import BaseModel, BeforeValidator, Field

from .settings import Arange, Linspace, get_settings

MimeType = Literal[
    "html", "json", "yaml", "plain", "base64", "png", "gds", "netlist", "dict", "error"
]


class ShowMessage(BaseModel):
    """A message to vscode to show an object."""

    what: Literal["show"] = "show"  # do not override
    mime: MimeType
    content: str


class ShowGdsMessage(BaseModel):
    """A message to vscode to show a GDS."""

    what: Literal["showGds"] = "showGds"  # do not override
    gds: str
    lyrdb: str


class ReloadSchematicMessage(BaseModel):
    """A message to vscode to trigger a schematic reload."""

    what: Literal["reloadSchematic"] = "reloadSchematic"
    path: str


class ErrorMessage(BaseModel):
    """A message to vscode to trigger an error popup."""

    what: Literal["error"] = "error"  # do not override
    category: str
    message: str
    path: str


class RefreshTreesMessage(BaseModel):
    """A message to vscode to trigger a pics tree reload."""

    what: Literal["refreshPicsTree"] = "refreshPicsTree"


class RestartServerMessage(BaseModel):
    """A message to vscode to trigger a server restart."""

    what: Literal["restartServer"] = "restartServer"


class ReloadLayoutMessage(BaseModel):
    """A message to vscode to trigger a gds viewer reload."""

    what: Literal["reloadLayout"] = "reloadLayout"
    cell: str


Message: TypeAlias = (
    ShowMessage
    | ErrorMessage
    | RefreshTreesMessage
    | ReloadLayoutMessage
    | ShowGdsMessage
    | RestartServerMessage
)


def _default_pdk_name() -> str:
    return get_settings().pdk.name


def _default_wls() -> Linspace | Arange:
    return get_settings().sim.wls


class SimulationConfig(BaseModel):
    """Data model for simulation configuration."""

    pdk: str = Field(default_factory=_default_pdk_name)
    wls: Linspace | Arange = Field(default_factory=_default_wls)
    op: str = "none"
    port_in: str = ""
    settings: dict[str, Any] = Field(default_factory=dict)


def ensure_recursive_netlist(obj: Any) -> dict:
    """Ensure that a given object is a recursive netlist."""
    from gdsfactoryplus.core.shared import activate_pdk_by_name

    if isinstance(obj, Path):
        obj = str(obj)

    if isinstance(obj, str):
        pdk = activate_pdk_by_name(get_settings().pdk.name)
        if "\n" in obj or obj.endswith(".pic.yml"):
            c = from_yaml(obj)
        else:
            c = pdk.get_component(obj)
        obj = c.get_netlist(recursive=True)

    if hasattr(obj, "model_dump"):
        obj = obj.model_dump()

    if isinstance(obj, dict) and "instances" in obj:
        obj = {"top_level": obj}

    if not isinstance(obj, dict):
        msg = f"Can't validate obj {obj} into RecursiveNetlist"
        raise TypeError(msg)

    return obj


class SimulationData(BaseModel):
    """Data model for simulation."""

    netlist: Annotated[dict, BeforeValidator(ensure_recursive_netlist)]
    config: SimulationConfig = Field(default_factory=SimulationConfig)


class DoItForMe(BaseModel):
    """DoItForMe Data."""

    prompt: str = ""
    initial_circuit: str = ""
    url: str = ""


class Result(BaseModel):
    """Result class containing logs and errors to be returned."""

    log: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class User(BaseModel):
    """User class containing user information from GDSFactory+."""

    user_name: str
    email: str
    organization_name: str | None
    organization_id: str | None
    pdks: list[str] | None
    is_superuser: bool
