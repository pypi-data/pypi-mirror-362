import re
import signal
import sys
from types import FrameType
from typing import Any, Optional

# Can't use types-docker since it requires urllib2 which is incompatible with boto3 for Python 3.9.
import docker  # type: ignore[import-untyped]
from docker import DockerClient
from docker.errors import APIError, DockerException, NotFound  # type: ignore[import-untyped]

Container = Any
Volume = Any

from dbnl import __version__
from dbnl.errors import DBNLError

CONTAINER_NAME = "dbnl-sandbox"
VOLUME_NAME = "dbnl-sandbox"
IMAGE_NAME = "sandbox-srv"
LEGACY_REGISTRY = "us-docker.pkg.dev/dbnlai/images"
DEFAULT_REGISTRY = "ghcr.io/dbnlai/images"
DEFAULT_BASE_URL = "http://localhost:8080"
DEFAULT_REGISTRY_USERNAME = "_json_key_base64"


class SandboxError(DBNLError):
    def __init__(self, message: str) -> None:
        self.message = message


class SandboxDockerConnectionError(SandboxError):
    def __init__(self) -> None:
        super().__init__("Failed to connect to Docker. Is Docker running?")


class SandboxAlreadyRunning(SandboxError):
    def __init__(self) -> None:
        super().__init__("Sandbox is already running.")


class SandboxHaltedUnexpectedly(SandboxError):
    def __init__(self) -> None:
        super().__init__("Sandbox has halted unexpectedly.")


class SandboxNotFound(SandboxError):
    def __init__(self) -> None:
        super().__init__("Sandbox was not found.")


class SandboxVolumeNotFound(SandboxError):
    def __init__(self) -> None:
        super().__init__("Sandbox volume was not found.")


def _client() -> DockerClient:
    try:
        return docker.from_env()
    except DockerException as exc:
        raise SandboxDockerConnectionError() from exc


def default_registry(version: Optional[str]) -> str:
    """Returns the default sandbox registry."""
    if version is not None:
        match = re.match(r"^(\d+)\.(\d+)", version)
        assert match is not None, "Version string does not match expected format"
        major, minor = match.groups()
        if int(major) == 0 and int(minor) <= 24:
            return LEGACY_REGISTRY
    return DEFAULT_REGISTRY


def default_version() -> str:
    """Returns the default sandbox version."""
    match = re.match(r"^(\d+)\.(\d+)", __version__)
    assert match is not None, "Version string does not match expected format"
    major, minor = match.groups()
    return f"{major}.{minor}"


def default_base_url() -> str:
    """Returns the default base url."""
    return DEFAULT_BASE_URL


def _container(client: DockerClient) -> Optional["Container"]:
    """Gets the sandbox container if it exists."""
    try:
        return client.containers.get(CONTAINER_NAME)
    except NotFound:
        return None


def _volume(client: DockerClient) -> Optional["Volume"]:
    """Gets the sandbox volume if it exists."""
    try:
        return client.volumes.get(VOLUME_NAME)
    except NotFound:
        return None


def sandbox_start(username: Optional[str], password: Optional[str], registry: str, version: str, base_url: str) -> None:
    """Start the sandbox."""
    repository = f"{registry}/{IMAGE_NAME}"

    client = _client()

    # If credentials were provided, login.
    if username is not None and password is not None:
        client.login(username=username, password=password, registry=registry)

    # Pull image.
    image = client.images.pull(repository=repository, tag=version)

    # Check if volume exists.
    volume = _volume(client)
    if volume is None:
        volume = client.volumes.create(VOLUME_NAME)

    # Check if container exists.
    container = _container(client)
    if container is not None:
        if container.status == "running":
            # If container is running, raise an error.
            raise SandboxAlreadyRunning()
        else:
            # Otherwise, remove it.
            container.remove()

    # Start container.
    try:
        container = client.containers.run(
            image=image,
            detach=True,
            ports={8080: 8080},
            name=CONTAINER_NAME,
            privileged=True,
            environment={
                "DBNL_REGISTRY": registry,
                "DBNL_BASE_URL": base_url,
                **(
                    {
                        "DBNL_REGISTRY_USERNAME": username,
                        "DBNL_REGISTRY_PASSWORD": password,
                    }
                    if username is not None and password is not None
                    else {}
                ),
            },
            volumes={volume.name: {"bind": "/var/lib/dbnl", "mode": "rw"}},
        )
    except APIError as exc:
        if exc.status_code == 409:
            raise SandboxAlreadyRunning() from exc
        raise exc


def sandbox_status() -> str:
    """Check sandbox status."""
    client = _client()
    container = _container(client)
    if container is None:
        return "not found"
    return str(container.status)


def sandbox_logs() -> None:
    """Tail the sandbox logs."""
    client = _client()
    container = _container(client)
    if container is None:
        raise SandboxNotFound()

    # Add graceful exit handler to stop container.
    def exit_gracefully(signal: int, frame: Optional[FrameType]) -> None:
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    # Tail logs.
    logs = container.logs(stream=True)
    for l in logs:
        sys.stdout.buffer.write(l)
        sys.stdout.buffer.flush()


def sandbox_exec(command: list[str]) -> None:
    """Exec a command on the sandbox."""
    client = _client()
    container = _container(client)
    if container is None:
        raise SandboxNotFound()

    # Add graceful exit handler to stop container.
    def exit_gracefully(signal: int, frame: Optional[FrameType]) -> None:
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    # Run command.
    (_, output) = container.exec_run(command, stream=True)

    # Tail output.
    for l in output:
        sys.stdout.buffer.write(l)
        sys.stdout.buffer.flush()


def sandbox_stop() -> None:
    """Stop the sandbox."""
    client = _client()
    container = _container(client)
    if container is None:
        # Nothing to do if container is missing.
        return
    container.stop()
    container.remove()


def sandbox_delete() -> None:
    """Delete the sandbox data."""
    client = _client()
    volume = _volume(client)
    if volume is None:
        raise SandboxVolumeNotFound()
    volume.remove()
