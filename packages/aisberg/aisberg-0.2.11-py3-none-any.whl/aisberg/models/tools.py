from typing import Dict, List, Iterable
from pydantic import BaseModel, Field


class Property(BaseModel):
    type: str = Field(..., examples=["string"])
    description: str


class Parameters(BaseModel):
    """Schéma JSON Schema standard OpenAI pour les paramètres."""

    type: str = Field(default="object", frozen=True)
    properties: Dict[str, Property]
    required: List[str]


class Function(BaseModel):
    name: str
    description: str
    parameters: Parameters


class Tool(BaseModel):
    type: str = Field(default="function", frozen=True)
    function: Function


def make_tool(
    *,
    name: str,
    description: str,
    params: Dict[str, str],  # {"param": "description", ...}
) -> Tool:
    """Crée un objet `Tool` à partir des paramètres fournis.

    Args:
        name: Nom de la fonction.
        description: Description de la fonction.
        params: Dictionnaire des paramètres avec leur description.

    Returns:
        Un objet `Tool` prêt à être utilisé.
    """
    properties = {
        key: Property(type="string", description=desc)  # <-- adapt typage si besoin
        for key, desc in params.items()
    }
    return Tool(
        function=Function(
            name=name,
            description=description,
            parameters=Parameters(
                properties=properties,
                required=list(params.keys()),
            ),
        )
    )


def tools_to_payload(tools: Iterable[Tool]) -> List[Dict]:
    """
    Convertit des objets `Tool` (Pydantic) en payload brut..

    Args:
        tools: Un itérable d'instances `Tool`.
    Returns:
        Une liste de dicts sérialisables en JSON.
    """
    if not isinstance(tools, Iterable) or not tools:
        return []

    return [tool.model_dump(mode="json", exclude_none=True) for tool in tools]
