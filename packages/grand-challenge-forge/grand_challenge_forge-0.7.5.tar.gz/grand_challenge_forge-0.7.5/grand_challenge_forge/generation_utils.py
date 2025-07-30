import json
import logging
import os
import subprocess
import tempfile
import time
import uuid
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import black
from jinja2 import FileSystemLoader, StrictUndefined, TemplateNotFound
from jinja2.sandbox import ImmutableSandboxedEnvironment

from grand_challenge_forge import PARTIALS_PATH

DEBUG = os.getenv("GRAND_CHALLENGE_FORGE_DEBUG", "false").lower() == "true"

SCRIPT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
RESOURCES_PATH = SCRIPT_PATH / "resources"


logger = logging.getLogger(__name__)


def is_json(socket):
    return socket["relative_path"].endswith(".json")


def is_image(socket):
    return socket["super_kind"] == "Image"


def is_file(socket):
    return socket["super_kind"] == "File" and not socket[
        "relative_path"
    ].endswith(".json")


def has_example_value(socket):
    return "example_value" in socket and socket["example_value"] is not None


def generate_socket_value_stub_file(*, output_zip_file, target_zpath, socket):
    """Creates a stub based on a component interface"""
    if has_example_value(socket):
        zinfo = zipfile.ZipInfo(str(target_zpath))
        output_zip_file.writestr(
            zinfo,
            json.dumps(
                socket["example_value"],
                indent=4,
            ),
        )
        return

    # Copy over an example

    if is_json(socket):
        source = RESOURCES_PATH / "example.json"
    elif is_image(socket):
        source = RESOURCES_PATH / "example.mha"
        target_zpath = target_zpath / f"{str(uuid.uuid4())}.mha"
    else:
        source = RESOURCES_PATH / "example.txt"

    output_zip_file.write(
        source,
        arcname=str(target_zpath),
    )


def socket_to_socket_value(socket):
    """Creates a stub dict repr of a socket valuee"""
    sv = {
        "file": None,
        "image": None,
        "value": None,
    }
    if socket["super_kind"] == "Image":
        sv["image"] = {
            "name": "the_original_filename_of_the_file_that_was_uploaded.suffix",
        }
    if socket["super_kind"] == "File":
        sv["file"] = (
            f"https://grand-challenge.org/media/some-link/"
            f"{socket['relative_path']}"
        )
    if socket["super_kind"] == "Value":
        sv["value"] = socket.get("example_value", {"some_key": "some_value"})
    return {
        **sv,
        "interface": socket,
    }


def get_jinja2_environment(searchpath=None):
    from grand_challenge_forge.partials.filters import custom_filters

    if searchpath:
        searchpath = [searchpath, PARTIALS_PATH]
    else:
        searchpath = PARTIALS_PATH

    env = ImmutableSandboxedEnvironment(
        loader=FileSystemLoader(
            searchpath=searchpath,
            followlinks=True,
        ),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    env.filters = custom_filters
    env.filters["zip"] = zip
    env.globals["now"] = datetime.now(timezone.utc)

    return env


def copy_and_render(
    *,
    templates_dir_name,
    output_zip_file,
    target_zpath,
    context,
):
    source_path = PARTIALS_PATH / templates_dir_name

    if not source_path.exists():
        raise TemplateNotFound(source_path)

    env = get_jinja2_environment(searchpath=source_path)

    for root, _, files in os.walk(source_path, followlinks=True):
        root = Path(root)

        check_allowed_source(path=root)

        # Create relative path
        rel_path = root.relative_to(source_path)
        current_zdir = target_zpath / rel_path

        for file in sorted(files):
            source_file = root / file
            output_file = current_zdir / file

            check_allowed_source(path=source_file)

            if file.endswith(".j2"):  # Jinja2 template
                template = env.get_template(
                    name=str(source_file.relative_to(source_path))
                )
                rendered_content = template.render(
                    **context,
                    _no_gpus=DEBUG,
                )

                targetfile_zpath = output_file.with_suffix("")

                if targetfile_zpath.suffix == ".py":
                    rendered_content = apply_black(rendered_content)

                # Collect information about the file to be written to the zip file
                # (permissions, et cetera)
                zinfo = zipfile.ZipInfo.from_file(
                    source_file,
                    arcname=str(targetfile_zpath),
                )

                # Update the date time of creation, since we are technically
                # creating a new file
                # Also (partially) addresses a problem where docker build injects
                # incorrect files:
                # https://github.com/moby/buildkit/issues/4817#issuecomment-2032551066
                zinfo.date_time = time.localtime()[0:6]

                output_zip_file.writestr(zinfo, rendered_content)
            else:
                output_zip_file.write(
                    str(source_file), arcname=str(output_file)
                )


def check_allowed_source(path):
    if PARTIALS_PATH.resolve() not in path.resolve().parents:
        raise PermissionError(
            f"Only files under {PARTIALS_PATH} are allowed "
            "to be copied or rendered"
        )


def apply_black(content):
    # Format rendered Python code string using black
    result = black.format_str(
        content,
        mode=black.Mode(),
    )
    return result


@contextmanager
def zipfile_to_filesystem(output_path):
    """
    Context manager that provides an in-memory zip file handle and optionally
    extracts its contents.

    Args
    ----
        output_dir (str, Path): Directory to extract the zip contents to
        after completion.

    Yields
    ------
        ZipFile: A ZipFile object that can be written to.
    """
    zip_handle = BytesIO()

    with zipfile.ZipFile(zip_handle, "w") as zip_file:
        yield zip_file

    # Extract contents to disk if output_dir is specified
    # Use a subprocess because the ZipFile.extractall does
    # not keep permissions: https://github.com/python/cpython/issues/59999

    zip_handle.seek(0)
    os.makedirs(output_path, exist_ok=True)

    temp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    try:
        temp_zip.write(zip_handle.getvalue())
        temp_zip.close()

        subprocess.run(
            [
                "unzip",
                "-o",
                temp_zip.name,
                "-d",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.remove(temp_zip.name)
