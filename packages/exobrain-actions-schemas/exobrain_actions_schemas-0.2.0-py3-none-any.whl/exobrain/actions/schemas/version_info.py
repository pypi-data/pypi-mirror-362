from exobrain.actions.schemas.base_model import BaseModel


class GitInfo(BaseModel):
    """
    Git information structure.

    Attributes:
        commit: The commit hash of the Git repository.
        branch: The branch name of the Git repository.
        date: The date of the commit in ISO format.
    """

    commit: str
    branch: str
    date: str


class VersionInfo(BaseModel):
    """
    Version information structure.

    Attributes:
        version: The version of the application.
        git: A dictionary containing Git information, including commit hash, branch name, and date.
    """

    version: str
    git: GitInfo


class VersionStatus(VersionInfo):
    """
    Version status structure.

    Attributes:
        status: The status of the service (e.g., "ok", "error").
        service: The name of the service (e.g., "alternate-supplier"), or None in DEV mode.
        version: The version of the service.
        git: A dictionary containing Git information, including commit hash, branch name, and date.
    """

    status: str
    service: str | None
