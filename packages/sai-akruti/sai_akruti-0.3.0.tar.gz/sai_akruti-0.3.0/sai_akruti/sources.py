import json
import time
from abc import ABC
from pathlib import Path
from typing import Any, Dict, List, Type

import boto3
import botocore.exceptions
from dotenv import dotenv_values
from pydantic import fields
from pydantic_settings import PydanticBaseSettingsSource, BaseSettings


def _process_parameter_value(key: str, value: Any, param_type: str) -> Dict[str, Any]:
    """Process already-decrypted parameter value based on its type."""
    result = {}

    if param_type == "StringList":
        # Value should already be a comma-separated string; split into list
        result[key] = value.split(",")
    else:
        # String or SecureString — try to load JSON dict
        try:
            value_dict = json.loads(value)
            if isinstance(value_dict, dict):
                result.update(value_dict)  # Unpack dict keys
            else:
                result[key] = value  # Non-dict JSON (e.g., str, list, etc.)
        except (json.JSONDecodeError, TypeError):
            result[key] = value  # Non-JSON string fallback

    return result


class MultiDotEnvSettingsSource(PydanticBaseSettingsSource, ABC):
    """Load from multiple .env files in order."""
    env_files: List[Path]

    def __init__(self, settings_cls: Type[BaseSettings], env_files: List[Path]):
        super().__init__(settings_cls)
        self.env_files = env_files

    def __call__(self) -> Dict[str, Any]:
        data = {}
        for env_file in self.env_files:
            if env_file.exists():
                data.update(dotenv_values(env_file))
        return data

    def get_field_value(self, field: fields.FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        data = self()
        if field_name in data:
            return data[field_name], "dotenv", True
        return None, "dotenv", False


class SSMSettingsSource(PydanticBaseSettingsSource, ABC):
    """Load from AWS SSM Parameter Store, supporting multiple prefixes."""

    def __init__(
            self,
            settings_cls: Type[BaseSettings],
            prefixes: List[str],
            region: str = "us-west-2",
            ttl: int = 300
    ):
        super().__init__(settings_cls)
        self.prefixes = prefixes
        self.client = boto3.client("ssm", region_name=region)
        self.ttl_seconds = ttl
        self._last_loaded: float = 0
        self._cached_data: Dict[str, Any] = {}

    def _fetch_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        for prefix in self.prefixes:
            if prefix.endswith("/"):
                paginator = self.client.get_paginator("get_parameters_by_path")
                for page in paginator.paginate(Path=prefix, Recursive=True, WithDecryption=True):
                    for param in page.get("Parameters", []):
                        full_path = param["Name"]
                        result = _process_parameter_value(
                            full_path.rsplit("/", 1)[-1].upper(),
                            param.get("Value", ""),
                            param.get("Type", "String")
                        )
                        data.update(result)
            else:
                try:
                    response = self.client.get_parameter(Name=prefix, WithDecryption=True)
                    param = response.get("Parameter", {})
                    result = _process_parameter_value(
                        prefix.rsplit("/", 1)[-1].upper(),
                        param.get("Value", ""),
                        param.get("Type", "String")
                    )
                    data.update(result)
                except self.client.exceptions.ParameterNotFound:
                    continue  # Optional: log missing parameter

        return data

    @property
    def _should_reload(self) -> bool:
        return time.time() - self._last_loaded > self.ttl_seconds

    @property
    def ssm_data(self) -> Dict[str, Any]:
        if not self._cached_data or self._should_reload:
            self._cached_data = self._fetch_data()
            self._last_loaded = time.time()
        return self._cached_data

    def __call__(self) -> Dict[str, Any]:
        return self.ssm_data

    def get_field_value(self, field: fields.FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        data = self()
        if field_name in data:
            return data[field_name], "ssm", True
        return None, "ssm", False


class SecretsManagerSettingsSource(PydanticBaseSettingsSource, ABC):
    """Load from AWS Secrets Manager, supporting multiple secrets."""

    def __init__(self, settings_cls: Type[BaseSettings], secret_ids: List[str], region: str = "us-west-2"):
        super().__init__(settings_cls)
        self.secret_ids = secret_ids
        self.client = boto3.client("secretsmanager", region_name=region)

    def __call__(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for secret_id in self.secret_ids:
            try:
                response = self.client.get_secret_value(SecretId=secret_id)
                secret_string = response.get("SecretString")
                if secret_string:
                    secret_data = json.loads(secret_string)
                    if isinstance(secret_data, dict):
                        data.update(secret_data)
            except botocore.exceptions.BotoCoreError as e:
                raise e
        return data

    def get_field_value(self, field: fields.FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        data = self()
        if field_name in data:
            return data[field_name], "secrets", True
        return None, "secrets", False
