from pathlib import Path

from hatchling.plugin import hookimpl
from hatchling.version.source.plugin.interface import VersionSourceInterface
from versioning import pep440, semver2
from versioning.project import NoVersion


class SimpleGitVersioningVersionSource(VersionSourceInterface):  # pragma: no cover
    PLUGIN_NAME = "simple-git-versioning"

    def get_version_data(self) -> dict:
        try:
            scheme = self.config["scheme"]
        except KeyError:
            Project = pep440.Project
            options = dict(dev=0)
        else:
            if not isinstance(scheme, str):
                raise TypeError(
                    f"unexpected versioning scheme (tool.hatch.version.scheme): '{scheme}', expected 'pep440' or 'semver2'"
                )

            scheme = scheme.casefold()
            if scheme == "pep440":
                Project = pep440.Project
                options = dict(dev=0)
            elif scheme == "semver2":
                Project = semver2.Project
                options = dict()
            else:
                raise ValueError(
                    f"unexpected versioning scheme (tool.hatch.version.scheme): '{scheme}', expected 'pep440' or 'semver2'"
                )

        with Project(path=Path(self.root)) as proj:
            try:
                return {"version": str(proj.version())}
            except NoVersion:
                return {"version": str(proj.release(**options))}


@hookimpl
def hatch_register_version_source():  # pragma: no cover
    return SimpleGitVersioningVersionSource
