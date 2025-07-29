from pydantic import BaseModel as CoreBaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class BaseModel(CoreBaseModel):
    """
    Base model for all Pydantic models in the application.

    This class sets the configuration for all derived models, including
    - `alias_generator`: Converts field names to camelCase
    - `populate_by_name`: Allows initialization with Python-style snake_case names
    - `extra`: Forbids extra fields in the model
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )
