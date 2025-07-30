from __future__ import annotations

from datetime import datetime
from inspect import getsource
from typing import Literal

from dateutil.parser import parse
from pydantic import BaseModel, field_validator

from nortech.derivers.values.deriver import Deriver, get_deriver_from_script
from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.values.pagination import (
    PaginatedResponse,
    PaginationOptions,
)


class DeployedDeriver(BaseModel):
    id: int
    deriver: type[Deriver]

    @field_validator("deriver", mode="before")
    @classmethod
    def convert_deriver_string(cls, v):
        if isinstance(v, str):
            return get_deriver_from_script(v)
        return v


class Log(BaseModel):
    timestamp: datetime
    message: str

    def __str__(self):
        return f"{self.timestamp} {self.message}"


class LogList(BaseModel):
    logs: list[Log]

    def __str__(self) -> str:
        str_representation = "\n".join([str(log) for log in self.logs])
        return str_representation


class DeriverLogs(BaseModel):
    name: str
    flow: LogList
    processor: LogList

    def __str__(self) -> str:
        str_representation = f"Pod: {self.name}\n"
        str_representation += "\nFlow logs:\n"
        for log in self.flow.logs:
            str_representation += f"{log}\n"

        str_representation += "\nProcessor logs:\n"
        for log in self.processor.logs:
            str_representation += f"{log}\n"

        return str_representation


class LogsPerPod(BaseModel):
    pods: list[DeriverLogs]

    def __str__(self) -> str:
        str_representation = "Pods:\n"
        for pod in self.pods:
            str_representation += f"{pod}\n"

        return str_representation


def list_derivers(
    nortech_api: NortechAPI,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url="/api/v1/derivers",
        params=pagination_options.model_dump(by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200], "Failed to list Derivers.")

    return PaginatedResponse[DeployedDeriver].model_validate(response.json())


def get_deriver(nortech_api: NortechAPI, deriver_id: int):
    response = nortech_api.get(url=f"/api/v1/derivers/{deriver_id}")
    validate_response(response, [200], "Failed to get Deriver.")

    return DeployedDeriver.model_validate(response.json())


def deploy_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
):
    response = nortech_api.post(
        url="/api/v1/derivers",
        json={
            "deriver": getsource(deriver),
        },
    )
    validate_response(response, [200], "Failed to create Deriver.")

    return get_deriver_from_script(response.json()["script"])


def get_logs_from_response_logs(response_logs: str) -> LogList:
    logs = [
        Log(
            timestamp=parse(log.split(" ", 1)[0]),
            message=log.split(" ", 1)[1],
        )
        for log in response_logs.split("\n")
        if log != ""
    ]

    return LogList(logs=logs)


def get_deriver_logs(
    nortech_api: NortechAPI,
    deriver_id: int,
):
    response = nortech_api.get(
        url=f"/api/v1/derivers/{deriver_id}/logs",
    )
    validate_response(response, [200], "Failed to get Deriver logs.")

    return LogsPerPod(
        pods=[
            DeriverLogs(
                name=pod["podName"],
                flow=get_logs_from_response_logs(pod["flowLogs"]),
                processor=get_logs_from_response_logs(pod["processorLogs"]),
            )
            for pod in response.json()["logsPerPod"]
        ]
    )
