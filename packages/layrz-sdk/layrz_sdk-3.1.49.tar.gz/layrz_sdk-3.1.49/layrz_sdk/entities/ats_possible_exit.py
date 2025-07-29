"""Ats Exit entity"""

from datetime import datetime
from typing import Optional

from pydantic import (
  BaseModel,
  ConfigDict,
  Field,
  PositiveInt,  # useful if you later want a non-nullable positive int
  conint,
)


class AtsPossibleExit(BaseModel):
  """AtsPossibleExit entity"""

  pk: int = Field(description='Defines the primary key of the AtsPossibleExit')

  # Nullable “positive big integer” identifier
  identifier: Optional[conint(ge=0)] = Field(  # type: ignore
    default=None,
    description='Nullable positive big integer identifier for the exit',
  )

  # Volume / gauge snapshots
  initial_tank_volume: Optional[float] = Field(
    default=None,
    description='Initial tank volume in liters',
  )
  initial_fluxometer: Optional[float] = Field(
    default=None,
    description='Initial fluxometer reading in liters',
  )
  total_liters: float = Field(
    default=0.0,
    description='Total liters of fuel involved in the exit',
  )

  # Status flags
  is_ready: bool = Field(
    default=False,
    description='Indicates if the exit is ready',
  )
  in_progress: bool = Field(
    default=False,
    description='Indicates if the exit is in progress',
  )
  is_validated: bool = Field(
    default=False,
    description='Indicates if the exit is validated',
  )

  # Lifecycle timestamps
  start_at: datetime = Field(
    default_factory=datetime.now,
    description='Timestamp when the exit started',
  )
  end_at: Optional[datetime] = Field(
    default=None,
    description='Timestamp when the exit ended',
  )

  # Derived / bookkeeping flags
  is_recalculated: bool = Field(
    default=False,
    description='Indicates if the exit has been recalculated',
  )
  is_blackbox: Optional[bool] = Field(
    default=False,
    description='Indicates if the exit is a blackbox',
  )
  false_positive_count: Optional[int] = Field(
    default=0,
    description='Count of false positives detected',
  )

  model_config = ConfigDict(from_attributes=True)  # enables .from_orm()
