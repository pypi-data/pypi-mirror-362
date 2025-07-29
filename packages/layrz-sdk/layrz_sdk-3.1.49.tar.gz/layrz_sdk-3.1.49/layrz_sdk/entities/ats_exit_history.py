"""Exit Execution History"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import (
  BaseModel,
  ConfigDict,
  Field,
  PositiveInt,  # useful if you later want a non-nullable positive int
  conint,
)


class AtsExitExecutionHistory(BaseModel):
  pk: int = Field(description='Primary key of the Exit Execution History')

  from_asset: int = Field(
    description='ID of the asset from which the exit is initiated',
  )
  to_asset: int = Field(
    description='ID of the asset to which the exit is directed',
  )

  status: Literal['PENDING', 'FAILED', 'SUCCESS'] = Field(
    default='PENDING',
  )
  from_app: Optional[Literal['ATSWEB', 'ATSMOBILE', 'NFC']] = Field(
    default=None,
    description='Application from which the exit was initiated',
  )

  error_response: Optional[str] = Field(
    default=None,
    description='Error response received during the exit process',
  )

  generated_by: int = Field(
    description='ID of the user or system that initiated the exit',
  )

  queue_id: Optional[int] = Field(
    default=None,
    description='ID of the queue associated with the exit',
  )
  to_asset_mileage: Optional[float] = Field(
    default=None,
    description='Mileage of the asset to which the exit is directed',
  )

  created_at: datetime = Field(
    description='Timestamp when the exit was created',
  )
  updated_at: datetime = Field(
    description='Timestamp when the exit was last updated',
  )

  model_config = ConfigDict(from_attributes=True)
