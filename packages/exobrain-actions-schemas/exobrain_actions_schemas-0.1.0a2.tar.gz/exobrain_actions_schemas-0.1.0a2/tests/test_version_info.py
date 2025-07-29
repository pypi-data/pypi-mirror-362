import pytest

from exobrain.actions.schemas.version_info import GitInfo, VersionStatus


class TestVersionStatus:
    def test_version_status_creation(self) -> None:
        version_status = VersionStatus(
            status="ok",
            service="my-service",
            version="1.0.0",
            git=GitInfo(
                commit="abc123def",
                branch="main",
                date="2024-07-14T08:00:00Z",
            ),
        )

        assert version_status.status == "ok"
        assert version_status.service == "my-service"
        assert version_status.version == "1.0.0"
        assert version_status.git.commit == "abc123def"
        assert version_status.git.branch == "main"
        assert version_status.git.date == "2024-07-14T08:00:00Z"

    def test_version_status_service_none(self) -> None:
        status = VersionStatus(
            status="ok",
            service=None,
            version="2.1.3-beta",
            git=GitInfo(
                commit="deadbeef",
                branch="dev",
                date="2024-07-01T12:34:56Z",
            ),
        )
        assert status.service is None

    def test_version_status_missing_fields(self) -> None:
        with pytest.raises(ValueError, match="Field required") as ctx:
            # noinspection PyArgumentList
            VersionStatus(  # type: ignore
                service="missing-status",
                version="0.0.1",
                git=GitInfo(
                    commit="a1b2c3",
                    branch="fix/some-issue",
                    date="2024-01-05T00:00:00Z",
                ),
            )
        assert "status" in str(ctx.value)
