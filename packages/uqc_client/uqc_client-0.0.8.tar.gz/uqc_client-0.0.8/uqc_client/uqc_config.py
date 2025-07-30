from typing import Annotated, Optional

from pydantic import (
    Field,
    computed_field,
    PositiveInt,
)
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class ClientConfig(BaseSettings):
    """
    Configuration settings for client
    """

    VERSION: str = Field(
        description="Client Version",
        default="0.0.8",
    )


class ServerConfig(BaseSettings):
    """
    Configuration settings for server
    """

    PROTOCOL_VERSION: str = Field(
        description="Client Version",
        default="1.0",
    )

    SERVER_HOST: str = Field(
        description="Server host address",
        default="cloud.unitaryqubit.com",
    )

    SERVER_PORT: int = Field(
        description="Server port number",
        default=5001,
    )

    CHIP_STATUS: str = Field(
        description="Chip Status",
        default="active",
    )

    @computed_field
    def SERVER_URL(self) -> str:
        return "http://" + self.SERVER_HOST + ":" + str(self.SERVER_PORT)


class UserConfig(BaseSettings):
    """
    Configuration settings for user
    """

    USER_TOKEN: Optional[str] = Field(
        description="User's access token get form user platform",
        default=None,
    )


class TaskConfig(BaseSettings):
    """
    Configuration settings for user tasks
    """

    DEFAULT_SHOTS: Annotated[PositiveInt, Field(ge=100, description="Minium task shots for task submit")] = 100

    DEFAULT_USED_QUBIT_NUMMBER: Annotated[PositiveInt, Field(le=5, description="Maximum used qubits for task")] = 5

    DEFAULT_TASK_TARGET: str = Field(
        description="Task target qpu for task submit",
        default="Matrix2",
    )

    DEFAULT_TASK_QPROGTYPE: str = Field(
        description="Task qprog type for task submit",
        default="openqasm",
    )

    DEFAULT_TASK_QProgVersion: str = Field(
        description="Task qprog version for task submit",
        default="3.0",
    )


class UQCConfig(
    # Client info
    ClientConfig,
    # Server info
    ServerConfig,
    # User configs
    UserConfig,
    # Task configs
    TaskConfig,
):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )

    # Before adding any config,
    # please consider to arrange it in the proper config group of existed or added
    # for better readability and maintainability.
    # Thanks for your concentration and consideration.

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
