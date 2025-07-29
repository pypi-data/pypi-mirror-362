from __future__ import annotations

from typing import List, Optional, Union

from pydantic.v1 import Field, StrictBool, StrictFloat, StrictStr

from kelvin.api.client.data_model import DataModelBase

from . import enum


class ParameterItemNoComment(DataModelBase):
    """
    ParameterItemNoComment object.

    Parameters
    ----------
    name: StrictStr
    value: Union[StrictFloat, StrictStr, StrictBool]

    """

    name: StrictStr = Field(..., description="Parameter name")
    value: Union[StrictFloat, StrictStr, StrictBool]


class ParameterItem(ParameterItemNoComment):
    """
    ParameterItem object.

    Parameters
    ----------
    comment: Optional[StrictStr]

    """

    comment: Optional[StrictStr] = Field(None, description="Additional comments regarding the parameter change action")


class StagedStatus(DataModelBase):
    """
    StagedStatus object.

    Parameters
    ----------
    message: Optional[StrictStr]
    state: Optional[enum.WorkloadStatus]
    warnings: Optional[List[StrictStr]]

    """

    message: Optional[StrictStr] = Field(
        None, description="Descriptive, human-readable string for `state`.", example="Pending for deploy"
    )
    state: Optional[enum.WorkloadStatus] = Field(
        None, description="Current status of the Staged Workload.", example="pending_deploy"
    )
    warnings: Optional[List[StrictStr]] = Field(
        None,
        description="All warnings received for any Staged Workload operations.",
        example=[
            "back-off 5m0s restarting failed container=motor-speed-control-sjfhksdfhks67",
            "back-off 5m0s restarting failed container=gateway",
        ],
    )
