from typing import Optional

from pydantic import BaseModel


class NetworkStatsSchema(BaseModel):
    errorMessages: int
    longMessageParts: int
    matchedMessages: int
    maxTime: Optional[str] = None
    minTime: Optional[str] = None
    name: str
    rate: float
    totalMessages: int
    unmatchedMessages: int
    uploadId: int
    vehicleId: int

    @classmethod
    def from_variables(cls, variables: dict, vehicle_id: int) -> "NetworkStatsSchema":
        return cls(
            errorMessages=variables["errorMessages"],
            longMessageParts=variables["longMessageParts"],
            matchedMessages=variables["matchedMessages"],
            maxTime=variables.get("maxTime"),
            minTime=variables.get("minTime"),
            name=variables["name"],
            rate=variables["rate"],
            totalMessages=variables["totalMessages"],
            unmatchedMessages=variables["unmatchedMessages"],
            uploadId=variables["uploadId"],
            vehicleId=vehicle_id,
        )
