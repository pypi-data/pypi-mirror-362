import importlib.metadata
import os

import setuptools

try:
    __version__ = importlib.metadata.version("iker-python-setup")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "version_string_local",
    "version_string_scm",
    "version_string",
    "setup",
]


def read_version_tuple(cwd: str | None, *, version_file: str, patch_env_var: str) -> tuple[int, int, int]:
    if cwd is None:
        cwd = os.getcwd()

    with open(os.path.join(cwd, version_file)) as fh:
        major_str, minor_str, *patch_strs = fh.read().strip().split(".")

    major = max(0, int(major_str))
    minor = max(0, int(minor_str))

    patch_str = patch_strs[0] if len(patch_strs) > 0 else os.getenv(patch_env_var)
    patch = 0 if patch_str is None else min(999999, max(0, int(patch_str)))

    return major, minor, patch


def version_string_local(cwd: str | None,
                         *,
                         version_file: str,
                         patch_env_var: str) -> str:
    major, minor, patch = read_version_tuple(cwd, version_file=version_file, patch_env_var=patch_env_var)
    return f"{major}.{minor}.{patch}"


def version_string_scm(cwd: str | None,
                       *,
                       version_file: str,
                       patch_env_var: str,
                       scm_branch_name: str,
                       scm_branch_env_var: str) -> str:
    import setuptools_scm
    if cwd is None:
        cwd = os.getcwd()

    def find_scm_root(cd: str) -> str:
        cd = os.path.abspath(cd)
        for item in os.listdir(cd):
            if os.path.isdir(os.path.join(cd, item)) and item == ".git":
                return cd
        pd = os.path.dirname(cd)
        if pd == cd:
            raise ValueError("Cannot find SCM root properly")
        return find_scm_root(pd)

    def version_scheme_callback(scm_version: setuptools_scm.ScmVersion) -> str:
        major, minor, patch = read_version_tuple(cwd, version_file=version_file, patch_env_var=patch_env_var)
        if scm_version.branch == scm_branch_name or os.getenv(scm_branch_env_var) == scm_branch_name:
            return f"{major}.{minor}.{patch}"
        return f"{major}.{minor}.{0}"

    def local_scheme_callback(scm_version: setuptools_scm.ScmVersion) -> str:
        if scm_version.branch == scm_branch_name or os.getenv(scm_branch_env_var) == scm_branch_name:
            return ""
        if scm_version.dirty:
            return scm_version.format_with("+{node}.dirty")
        return scm_version.format_with("+{node}")

    return setuptools_scm.get_version(root=find_scm_root(cwd),
                                      version_scheme=version_scheme_callback,
                                      local_scheme=local_scheme_callback,
                                      normalize=True)


def version_string(cwd: str | None = None,
                   default: str = "0.0.0",
                   *,
                   version_file: str = "VERSION",
                   patch_env_var: str = "BUILD_NUMBER",
                   scm_branch_name: str = "master",
                   scm_branch_env_var: str = "GIT_BRANCH",
                   strict: bool = False) -> str:
    try:
        return version_string_scm(cwd,
                                  version_file=version_file,
                                  patch_env_var=patch_env_var,
                                  scm_branch_name=scm_branch_name,
                                  scm_branch_env_var=scm_branch_env_var)
    except Exception as e:
        if strict:
            raise e
    try:
        return version_string_local(cwd,
                                    version_file=version_file,
                                    patch_env_var=patch_env_var)
    except Exception as e:
        if strict:
            raise e
    return default


def setup(cwd: str | None = None, **kwargs):
    setuptools.setup(version=version_string(cwd, **kwargs), **kwargs)
