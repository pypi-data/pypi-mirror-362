"""Package that contains async calls to the SOIL's REST API"""

import gzip
import json
import logging
import os
from contextlib import asynccontextmanager
from itertools import takewhile
from typing import Any, Dict, Literal, TypedDict
from urllib.parse import urlencode

import httpx

from soil import errors
from soil.configuration import CONF, GLOBAL_CONFIG
from soil.types import (
    Context,
    CreateGraphLogRequest,
    Experiment,
    GetModule,
    GetModuleHash,
    GraphStateResponse,
    PipelineForRequest,
    Plan,
    SaveGraphStateRequest,
)

logger = logging.getLogger(__name__)

# Configure the logger based on the SOIL_SDK_LOGGER environment variable
log_level = os.getenv("SOIL_SDK_LOGGER", "WARNING").upper()
logger.setLevel(log_level)

API_ROOT = f"{GLOBAL_CONFIG.host!s}/v2/"
API_ROOT_V3 = f"{GLOBAL_CONFIG.host!s}/v3/"

_client: httpx.AsyncClient | None = None


async def clean_client():
    """Closes and cleans up the global httpx client if it exists."""
    global _client  # noqa: PLW0603
    if _client is not None:
        await _client.aclose()
        _client = None


@asynccontextmanager
async def _get_client():
    """Creates or reuses an async httpx client with authentication headers and HTTP/2 support."""
    global _client  # noqa: PLW0603
    if _client is None:
        max_connections = int(os.getenv("SOIL_MAX_CONNECTIONS", "10"))
        _client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {GLOBAL_CONFIG.token!s}",
                "Content-Type": "application/json",
            },
            timeout=30,
            http2=True,
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=min(20, max_connections),
            ),
        )
    try:
        # This is a workaround to avoid the issue of the token not being updated
        # when the client is reused.
        _client.headers.update(
            {
                "Authorization": f"Bearer {GLOBAL_CONFIG.token!s}",
            }
        )
        yield _client
    finally:
        if _client is not None and _client.is_closed:
            _client = None


async def upload_data(dtype: str, data: Any, metadata: Any) -> Dict[str, Any]:
    """Upload data to the cloud as a new dataset."""
    logger.debug("upload_data:%s", dtype)
    url = API_ROOT + "results/"
    body = {"type": dtype, "data": data, "metadata": metadata}

    async with _get_client() as client:
        response = await client.post(url, json=body)

    if response.status_code != 201:
        raise errors.DataNotUploaded(response.text)
    return response.json()


async def get_result(result_id: str) -> Dict[str, Any]:
    """Get the result data"""
    logger.debug("get_result:%s", result_id)
    url = API_ROOT + "results/" + result_id + "/"

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    return response.json()


async def get_alias(alias: str) -> Dict[str, Any]:
    """Gets an alias"""
    logger.debug("get_alias: %s", alias)
    url = API_ROOT + "states/?name=" + alias + "&with-roles"

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.ObjectNotFound("Error getting alias:" + response.text)

    aliases = response.json()
    if len(aliases) == 0:
        raise errors.DataNotFound("Alias not found")

    alias_id = aliases[0]["_id"]
    url = API_ROOT + "states/" + alias_id + "/"

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.ObjectNotFound("Error getting alias with id " + response.text)
    return response.json()


async def get_result_data(
    result_id: str, query: Dict[str, str] | None = None
) -> Dict[str, Any]:
    """Get the result data"""
    if query is None:
        query = {}
    logger.debug("get_result:%s %s", result_id, str(query))
    url = API_ROOT + "results/" + result_id + "/data/?" + urlencode(query)

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    return response.json()


async def create_experiment(
    plan: Plan,
    *,
    experiment_group: str | None = None,
    description: dict | str | None = None,
) -> Experiment:
    """Creates an experiment in SOIL asynchronously"""
    logger.debug("create_experiment: %s", str(plan))
    url = API_ROOT + "experiments/"
    experiment = {"name": "", "description": "", "plan": plan}
    if description is not None:
        experiment["description"] = description
    if experiment_group is not None:
        experiment["experiment_group"] = experiment_group

    async with _get_client() as client:
        response = await client.post(url, json={"experiment": experiment})

    if response.status_code != 200:
        raise ValueError("Error creating the experiment:" + response.text)
    return response.json()["experiment"]


async def get_experiment(experiment_id: str) -> Experiment:
    """Gets an experiment from SOIL asynchronously"""
    logger.debug("get_experiment: %s", experiment_id)
    url = API_ROOT + "experiments/" + experiment_id + "/"

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError(
            "Error getting the experiment " + experiment_id + "\n" + response.text
        )
    return response.json()


async def get_experiment_logs(experiment_id: str, start_date: str) -> Any:
    """Gets logs from a SOIL experiment asynchronously"""
    logger.debug("get_experiment_id: %s since %s", experiment_id, start_date)
    url = (
        API_ROOT
        + "experiments/"
        + experiment_id
        + "/logs/?"
        + urlencode({"start_date": start_date})
    )

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError(
            "Error getting the experiment " + experiment_id + "\n" + response.text
        )
    return response.json()


async def set_alias(
    alias: str,
    result_id: str,
    roles: list[str] | None = None,
    extras: dict[str, Any] | None = None,
) -> None:
    """Sets an alias for a result asynchronously. Updates a previous one with the same name."""
    logger.debug("set_alias: %s = %s", alias, result_id)
    obj = {"name": alias, "state": {"alias": alias, "result_id": result_id}}
    if extras is not None:
        obj["state"]["extras"] = extras
    if roles is not None:
        obj["roles"] = roles

    async with _get_client() as client:
        try:
            old_alias = await get_alias(alias)
            old_alias_id = old_alias["_id"]
            url = API_ROOT + "states/" + old_alias_id + "/"
            response = await client.patch(url, json=obj)
        except errors.DataNotFound:
            url = API_ROOT + "states/"
            response = await client.post(url, json=obj)

        if response.status_code != 200:
            raise errors.DataNotUploaded(
                f"Failed to create alias {alias}: {response.text}"
            )

        if roles is not None:
            await _create_app_id_roles(roles=roles)
            url = API_ROOT + "results/" + result_id + "/"
            response = await client.patch(url, json={"roles": roles})
            if response.status_code != 200:
                raise errors.DataNotUploaded(
                    f"Failed to patch result {result_id}: {response.text}"
                )


async def _create_app_id_roles(*, roles: list[str]) -> None:
    api_key = os.environ.get("APP_INFO_API_KEY")
    if api_key is None or os.getenv("PY_ENV") == "test":
        return

    auth_url = f"{CONF['auth_url']}/api/application/{CONF['auth_app_id']}"
    headers = {"Content-Type": "application/json", "Authorization": api_key}

    async with httpx.AsyncClient(http2=True) as client:
        for role in roles:
            response = await client.get(auth_url, headers=headers)
            if response.status_code != 200:
                logger.debug("Could not retrieve application info.")
                continue

            application_roles: list[dict[Literal["name"], str]] = response.json()[
                "application"
            ]["roles"]
            if len(
                list(
                    takewhile(
                        lambda app_role: app_role["name"] != role, application_roles
                    )
                )
            ) != len(application_roles):
                continue  # role already exists

            response = await client.post(
                f"{auth_url}/role",
                headers=headers,
                json={"role": {"name": role}},
            )
            if response.status_code != 200:
                logger.debug("Role could not be created because %s", response.text)


async def export_result(
    result_id: str, file_path: str, query: Dict[str, str] | None = None
) -> None:
    """Export result and saves it to a file asynchronously"""
    if query is None:
        query = {}
    logger.debug("export_result:%s %s", result_id, str(query))
    url = API_ROOT + "results/" + result_id + "/export/?" + urlencode(query)

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.DataNotFound(response.text)
    with open(file_path, "wb") as fd:
        fd.write(response.content)


class _SoilUploadModule(TypedDict):
    name: str
    code: str
    is_package: bool


async def upload_modules(modules: list[_SoilUploadModule]) -> None:
    """Uploads a chunk of modules asynchronously"""
    logger.debug("upload_modules:%s", modules)
    url = API_ROOT + "modules/"
    data = {"modules": modules}

    async with _get_client() as client:
        response = await client.post(url, json=data)

    if response.status_code != 200:
        raise errors.ModuleNotUploaded(response.text)


async def upload_module(module_name: str, code: str, is_package: bool) -> None:
    """Uploads a module asynchronously"""
    logger.debug("upload_module:%s", module_name)
    url = API_ROOT + "modules/"
    data = {"name": module_name, "code": code, "is_package": is_package}

    async with _get_client() as client:
        response = await client.post(url, json=data)

    if response.status_code != 200:
        raise errors.ModuleNotUploaded(response.text)


async def get_module(full_name: str) -> GetModule:
    """Downloads a module asynchronously"""
    logger.debug("get_module:%s", full_name)
    url = API_ROOT + "modules/" + full_name + "/"

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.ModuleNotFound(response.text)
    return response.json()


async def get_modules() -> list[GetModuleHash]:
    """Gets a list of modules asynchronously"""
    logger.debug("get_modules")
    url = f"{API_ROOT}modules/"
    async with _get_client() as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise errors.ModuleNotFound(response.text)
    return response.json()["result"]


async def create_event(key: str, value: Any) -> Any:
    """Saves an event in soil asynchronously"""
    url = API_ROOT + "alerts/events/"

    async with _get_client() as client:
        response = await client.post(url, json={"key": key, "value": value})

    if response.status_code != 201:
        raise errors.EventNotUploaded("Error saving the event:" + response.text)
    return response.json()


async def create_alert(alert: Dict) -> Any:
    """Creates an alert asynchronously"""
    url = API_ROOT + "alerts/alerts/"

    async with _get_client() as client:
        response = await client.post(url, json=alert)

    if response.status_code != 201:
        raise errors.AlertNotUploaded("Error creating the alert:" + response.text)
    return response.json()


async def get_dictionary(name: str, language: str) -> Dict[str, Any]:
    """Get the dictionary asynchronously"""
    url = API_ROOT + "dictionaries/" + name + "/?language=" + language

    async with _get_client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise errors.DictionaryNotFound("Error getting dictionary:" + response.text)
    return response.json()


async def create_dictionary(name: str, language: str, content: Dict) -> Dict[str, Any]:
    """Create a dictionary or update it asynchronously"""
    logger.debug("create_dictionary: %s in language: %s", str(name), str(language))
    data = {
        "name": name,
        "language": language,
        "content": content,
    }
    url = f"{API_ROOT}dictionaries/"

    async with _get_client() as client:
        response = await client.post(
            url,
            content=gzip.compress(bytes(json.dumps(data), encoding="utf-8")),
            headers={"Content-Encoding": "gzip"},
        )

    if response.status_code != 200:
        raise errors.DictionaryNotUploaded(
            f"Error creating/updating the dictionary {name} in language {language}: {response.text}"
        )
    return response.json()


async def get_graph_state(
    case_mix_store_id: str, graph_state_id: str, user_roles: list[str], user_id: str
) -> GraphStateResponse:
    """Get the stored graph state"""
    url = (
        f"{API_ROOT_V3}case-mix-store/{case_mix_store_id}/graph-state/{graph_state_id}"
    )

    async with _get_client() as client:
        response = await client.get(
            url, params={"user_roles": user_roles, "user_id": user_id}
        )

    if response.status_code != 200:
        raise errors.GraphStateNotFound(response.text)
    return response.json()


async def save_graph_state(
    case_mix_store_id: str, request: SaveGraphStateRequest
) -> None:
    """Save the provided graph state"""
    url = f"{API_ROOT_V3}case-mix-store/{case_mix_store_id}/graph-state"

    async with _get_client() as client:
        response = await client.post(url, json=request)

    if response.status_code != 200:
        raise errors.GraphStateNotSaved(response.text)


async def save_pipeline_context(
    context_id: str, subset_id: str, pipeline: PipelineForRequest, user_roles: list[str]
) -> None:
    """Save the provided pipeline context"""
    url = f"{API_ROOT_V3}case-mix-store/{context_id}/pipeline-context"

    async with _get_client() as client:
        response = await client.post(
            url,
            json={
                "subset_id": subset_id,
                "pipeline": pipeline,
                "user_roles": user_roles,
            },
        )

    if response.status_code >= 300:
        raise errors.PipelineContextNotSaved(response.text)


async def get_project_context(
    case_mix_store_id: str, project_id: str, user_roles: list[str]
) -> Context:
    """Get the project context"""
    url = (
        f"{API_ROOT_V3}case-mix-store/{case_mix_store_id}/project-context/{project_id}"
    )

    async with _get_client() as client:
        response = await client.get(url, params={"user_roles": user_roles})

    if response.status_code != 200:
        raise errors.ProjectContextNotFound(response.text)
    return response.json()


async def create_graph_log(
    case_mix_store_id: str,
    graph_state_id: str,
    request: CreateGraphLogRequest,
) -> None:
    """Create a graph log"""
    url = f"{API_ROOT_V3}case-mix-store/{case_mix_store_id}/graph-state/{graph_state_id}/log"

    async with _get_client() as client:
        response = await client.post(url, json=request)

    if response.status_code != 200:
        raise errors.GraphLogNotCreated(response.text)
