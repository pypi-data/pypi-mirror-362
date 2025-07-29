"""Utilities for running the curator."""

import importlib
import logging
import os
import shlex
import subprocess
import sys
import typing as t
from datetime import datetime

import flywheel
from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils import curator as c
from flywheel_gear_toolkit.utils import datatypes, walker

log = logging.getLogger(__name__)


def container_to_pickleable_dict(container: datatypes.Container) -> t.Dict[str, str]:
    """Returns a pickable dictionary version of a Flywheel.

    Drops the flywheel SDK so that the object can be pickled when passed around
    for multiprocessing.
    """
    val = {
        "id": container.id,
        "container_type": container.container_type,
    }
    if container.container_type == "file":
        if hasattr(container, "file_id"):
            val["id"] = container.file_id
        val["parent_type"] = container.parent_ref.get("type")
        val["parent_id"] = container.parent_ref.get("id")
    return val


def container_from_pickleable_dict(
    val: t.Dict, local_curator: c.HierarchyCurator
) -> datatypes.Container:
    """Take the simple pickleable dict entry and return the flywheel container."""
    get_container_fn = getattr(
        local_curator.context.client, f"get_{val['container_type']}"
    )
    container = get_container_fn(val["id"])
    return container


def handle_work(
    children: t.List[t.Dict[str, str]],
    local_curator: c.HierarchyCurator,
    handle: t.Callable[[c.HierarchyCurator, t.List[datatypes.Container]], None],
):
    """Convert list of dicts into list of containers and run callback on it."""
    containers = []
    for child in children:
        try:
            container = container_from_pickleable_dict(child, local_curator)
        except flywheel.rest.ApiException:
            log.error("Could not get container, skipping curation", exc_info=True)
        else:
            containers.append(container)
    handle(local_curator, containers)


def make_walker(container: datatypes.Container, curator: c.HierarchyCurator):
    """Generate a walker from a container and curator."""
    w = walker.Walker(
        container,
        depth_first=curator.config.depth_first,
        reload=curator.config.reload,
        stop_level=curator.config.stop_level,
    )
    return w


def reload_file_parent(
    container: datatypes.Container,
    local_curator: c.HierarchyCurator,
):
    """Reload the parent of a file container."""
    if getattr(container, "container_type", "") == "file":
        if getattr(container, "parent", None):
            return container
        get_parent_fn = getattr(
            local_curator.context.client, f"get_{container.parent_ref.type}"
        )
        container._parent = get_parent_fn(container.parent_ref.id)
    return container


def update_analysis_label(destination, curator_path):
    """Update the analysis label to include the curator script name."""
    script_name = os.path.basename(curator_path)
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    analysis_label = f"hierarchy-curator - {script_name} - {now}"
    destination.update(label=analysis_label)


def install_latest_flywheel_sdk():
    """Reloading latest flywheel-sdk modules."""
    log.info("Installing latest flywheel-sdk")

    # Install flywheel using pip

    command = (
        f"{sys.executable} -m pip --disable-pip-version-check install flywheel-sdk"
    )
    args = shlex.split(command)
    subprocess.check_call(args, shell=False)

    # subprocess.check_call(
    #     [
    #         sys.executable,
    #         "-m",
    #         "pip",
    #         "--disable-pip-version-check",
    #         "install",
    #         "flywheel-sdk",
    #     ],
    #     shell=False,
    # )

    # Reload flywheel modules
    packages = [x for x in sys.modules.keys() if x.startswith("flywheel")]
    for m in packages:
        try:
            module = importlib.import_module(m)
            importlib.reload(module)
        except ModuleNotFoundError:
            pass


def init_fw_client(gear_context: GearToolkitContext) -> flywheel.Client:
    """Initialize flywheel client.

    Arguments:
        gear_context (GearToolkitContext): The gear context

    Returns:
        flywheel.Client: The flywheel client
    """
    # Access the flywheel API
    fw = gear_context.get_client()

    log.info("Initializing the Flywheel client")
    # Check user Info
    user_info = fw.get_current_user()

    log.info(
        "You are logged in as:\nFirstname: %s\nLastname: %s\nEmail: %s",
        user_info.firstname,
        user_info.lastname,
        user_info.email,
    )

    return fw
