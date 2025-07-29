from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from cleo.io.outputs.output import Verbosity

from poetry.plugins.plugin import Plugin
from versioning import pep440, semver2
from versioning.project import NoVersion

if TYPE_CHECKING:
    from cleo.io.io import IO

    from poetry.poetry import Poetry


class SimpleGitVersioning(Plugin):  # pragma: no cover
    def activate(self, poetry: Poetry, io: IO):
        try:
            config = poetry.pyproject.data["tool"]["simple-git-versioning"]["poetry"]
        except KeyError:
            io.write_line("simple-git-versioning is not enabled", verbosity=Verbosity.DEBUG)
            return

        if isinstance(config, str):
            scheme = config
        elif isinstance(config, Mapping):
            scheme = config.get("scheme", "pep440")
        else:
            raise TypeError(f"unexpected type for `tool.simple-git-versioning.poetry`: '{type(config)}'")

        scheme = scheme.casefold()
        if scheme == "pep440":
            Project = pep440.Project
            options = dict(dev=0)
        elif scheme == "semver2":
            Project = semver2.Project
            options = dict()
        else:
            raise ValueError(
                f"unexpected value for `tool.simple-git-versioning.poetry.scheme`: '{scheme}', expected 'pep440' or 'semver2'"
            )

        with Project(path=poetry.pyproject.path.parent) as proj:
            try:
                poetry.package._set_version(str(proj.version()))
            except NoVersion:
                poetry.package._set_version(str(proj.release(**options)))
