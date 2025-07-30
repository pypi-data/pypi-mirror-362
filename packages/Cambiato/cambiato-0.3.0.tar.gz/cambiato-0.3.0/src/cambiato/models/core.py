r"""The core data models of Cambiato."""

# Standard library
from typing import Any

# Third party
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, ValidationError

# Local
from cambiato import exceptions


class BaseModel(PydanticBaseModel):
    r"""The BaseModel that all models inherit from."""

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            raise exceptions.CambiatoError(str(e)) from None
