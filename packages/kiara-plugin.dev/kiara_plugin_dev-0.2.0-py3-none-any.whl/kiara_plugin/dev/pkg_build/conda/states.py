# -*- coding: utf-8 -*-
import io
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib
from pathlib import Path
from typing import Any, Dict, List, Mapping, Union

from kiara.utils.cli import terminal_print
from kiara_plugin.dev.defaults import KIARA_DEV_MICROMAMBA_TARGET_PREFIX
from kiara_plugin.dev.pkg_build.states import State


class MicroMambaAvailable(State):
    def _check(self) -> Union[None, Mapping[str, Any]]:
        root_path: str = self.get_config("root_path")
        bin_path = os.path.join(root_path, "bin", "micromamba")
        if Path(bin_path).is_file():
            return {"micromamba_bin": bin_path}
        else:
            return None

    def _purge(self) -> None:
        root_path: str = self.get_config("root_path")
        bin_path = os.path.join(root_path, "bin", "micromamba")

        os.unlink(bin_path)

    def _resolve(self) -> Mapping[str, Any]:
        current = self._check()
        if current is not None:
            return current

        this_arch = platform.machine().lower()
        this_os = platform.system().lower()

        ARCH_MAP: Dict[str, Dict[str, str]] = {
            "linux": {
                "x86_64": "linux-64",
                "amd64": "linux-64",
                "64bit": "linux-64",
                "aarch64": "linux-aarch64",
                "ppc64": "linux-ppc64le",
            },
            "darwin": {
                "arm64": "osx-arm64",
                "x86": "osx-64",
                "64bit": "osx-64",
                "amd64": "osx-64",
            },
            "windows": {},
        }

        token = ARCH_MAP.get(this_os, {}).get(this_arch, None)
        if token is None:
            raise Exception(
                f"No micromamba executable available for: {this_os} / {this_arch}."
            )

        try:
            version = self.get_config("version")
        except Exception:
            version = "latest"

        url = f"https://micro.mamba.pm/api/micromamba/{token}/{version}"

        root_path: Path = self.get_config("root_path")
        # bin_path = root_path / "bin" / "micromamba"
        # bin_path.parent.mkdir(parents=True, exist_ok=True)
        terminal_print("Downloading micromamba...")

        fh = io.BytesIO()
        with urllib.request.urlopen(url) as response:  # type: ignore  # noqa
            fh.write(response.read())

        fh.seek(0)
        tar_archive = tarfile.open(fileobj=fh, mode="r:bz2")
        tar_archive.extract("bin/micromamba", root_path)

        current = self._check()
        if current is not None:
            return current
        else:
            raise Exception("Something went wrong.")


class MambaEnvironment(State):
    def list_conda_envs(self) -> List[str]:
        micromamba_path = self.get_other_state_detail(
            "micromamba_available", "micromamba_bin"
        )
        micromamba_prefix = self.get_config("mamba_prefix")

        args = [micromamba_path, "env", "list", "--json"]
        result = subprocess.run(
            args, capture_output=True, text=True, check=True, shell=False
        )

        envs = json.loads(result.stdout)
        return [
            x[len(micromamba_prefix) + 1 :]
            for x in envs["envs"]
            if x.startswith(micromamba_prefix)
        ]

    def _check(self) -> Union[None, Mapping[str, Any]]:
        env_name: str = self.get_config("env_name")
        if not env_name:
            raise Exception("Environment 'name' can't be empty.")

        if env_name in self.list_conda_envs():
            micromamba_prefix = self.get_config("mamba_prefix")
            return {
                "env_name": env_name,
                "env_path": os.path.join(micromamba_prefix, env_name),
                "mamba_prefix": self.get_config("mamba_prefix"),
            }
        else:
            return None

    def _purge(self):
        micromamba_prefix = self.get_config("mamba_prefix")
        if not micromamba_prefix:
            raise Exception("No 'mamba_prefix' config.")
        micromamba_prefix = os.path.expanduser(micromamba_prefix)
        if KIARA_DEV_MICROMAMBA_TARGET_PREFIX not in micromamba_prefix:
            raise Exception(
                f"'mamba_prefix' not a subfolder of: {KIARA_DEV_MICROMAMBA_TARGET_PREFIX}."
            )

        shutil.rmtree(micromamba_prefix)

    def _resolve(self) -> Mapping[str, Any]:
        check = self._check()
        if check is not None:
            return check

        micromamba_prefix = self.get_config("mamba_prefix")
        micromamba_path = self.get_other_state_detail(
            "micromamba_available", "micromamba_bin"
        )

        env_name = self.get_config("env_name")
        channels = self.get_config("channels")
        dependencies = self.get_config("dependencies")

        channels_str = "\n".join((f"  - {c}" for c in channels))
        dependencies_str = "\n".join((f"  - {d}" for d in dependencies))

        spec_content = f"""name: {env_name}
channels:
{channels_str}
dependencies:
{dependencies_str}
"""
        handle, filename = tempfile.mkstemp(text=True, suffix=".yaml")
        with os.fdopen(handle, "wt") as f:
            f.write(spec_content)

        terminal_print(
            f"Creating conda environment '{env_name}'. This will take a while..."
        )

        args = [
            micromamba_path,
            "create",
            "--yes",
            "--json",
            "-p",
            os.path.join(micromamba_prefix, env_name),
            "-f",
            filename,
        ]
        result = subprocess.run(
            args, capture_output=True, text=True, shell=False, check=False
        )

        if filename is not None:
            os.unlink(filename)

        if result.returncode != 0:
            terminal_print(f"Error creating environment '{env_name}':")
            terminal_print("stdout:")
            terminal_print(result.stdout)
            terminal_print("stderr:")
            terminal_print(result.stderr)
            raise Exception(f"Error creating environment '{env_name}'.")

        # env_details = json.loads(result.stdout)

        check = self._check()
        if check is not None:
            return check
        else:
            raise Exception("Something went wrong. This is a bug.")
