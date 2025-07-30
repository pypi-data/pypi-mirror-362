from typing import Optional

from pydantic import BaseModel, model_validator

from akride import Constants
from akride.core.enums import DataType
from akride.core.exceptions import UserError


class SourceContainerData(BaseModel):
    id: str


class CreateDatasetIn(BaseModel):
    dataset_name: str
    dataset_namespace: str = "default"
    data_type: DataType = DataType.IMAGE
    glob_pattern: str = Constants.DEFAULT_IMAGE_BLOB_EXPR
    overwrite: bool = False
    sample_frame_rate: float = -1

    source_container_data: Optional[SourceContainerData] = None

    @model_validator(mode="after")
    def validate_model(self):
        if self.data_type == DataType.IMAGE and self.sample_frame_rate != -1:
            raise UserError(
                message="Sample frame rate is not applicable for image datasets!",
            )

        if (
            self.data_type == DataType.VIDEO and
            self.glob_pattern == Constants.DEFAULT_IMAGE_BLOB_EXPR
        ):
            self.glob_pattern = Constants.DEFAULT_VIDEO_BLOB_EXPR

        return self

