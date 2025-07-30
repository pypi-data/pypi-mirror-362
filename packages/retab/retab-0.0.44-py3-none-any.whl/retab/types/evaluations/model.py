import datetime
from typing import Any, Optional

import nanoid  # type: ignore
from pydantic import BaseModel, Field, computed_field

from ...utils.json_schema import generate_schema_data_id, generate_schema_id
from ..inference_settings import InferenceSettings
from .documents import EvaluationDocument
from .iterations import Iteration


class BaseEvaluation(BaseModel):
    id: str = Field(default_factory=lambda: "proj_" + nanoid.generate())
    name: str = Field(default="", description="The name of the evaluation")
    json_schema: dict[str, Any] = Field(default_factory=dict, description="The json schema of the evaluation")
    default_inference_settings: InferenceSettings = Field(default=InferenceSettings(), description="The default inference properties for the evaluation.")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))


# Actual Object stored in DB
class Evaluation(BaseEvaluation):
    documents: list[EvaluationDocument] = Field(default_factory=list)
    iterations: list[Iteration] = Field(default_factory=list)

    @computed_field  # type: ignore
    @property
    def schema_data_id(self) -> str:
        """Returns the SHA1 hash of the schema data, ignoring all prompt/description/default fields.

        Returns:
            str: A SHA1 hash string representing the schema data version.
        """
        return generate_schema_data_id(self.json_schema)

    # This is a computed field, it is exposed when serializing the object
    @computed_field  # type: ignore
    @property
    def schema_id(self) -> str:
        """Returns the SHA1 hash of the complete schema.

        Returns:
            str: A SHA1 hash string representing the complete schema version.
        """
        return generate_schema_id(self.json_schema)


class ListEvaluationParams(BaseModel):
    schema_id: Optional[str] = Field(default=None, description="The ID of the schema")
    schema_data_id: Optional[str] = Field(default=None, description="The ID of the schema data")


class CreateEvaluationRequest(BaseModel):
    name: str
    json_schema: dict[str, Any]
    default_inference_settings: InferenceSettings


# This is basically the same as BaseEvaluation, but everything is optional.
# Could be achieved by convert_basemodel_to_partial_basemodel(BaseEvaluation) but we prefer explicitness
class PatchEvaluationRequest(BaseModel):
    name: Optional[str] = Field(default=None, description="The name of the document")
    json_schema: Optional[dict[str, Any]] = Field(default=None, description="The json schema of the evaluation")
    default_inference_settings: Optional[InferenceSettings] = Field(default=None, description="The default inference properties for the evaluation (mostly used in the frontend)")


class AddIterationFromJsonlRequest(BaseModel):
    jsonl_gcs_path: str
