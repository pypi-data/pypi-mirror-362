import re
import warnings
from dataclasses import dataclass
from typing import Optional

from dbnl import __version__ as sdk_version
from dbnl.warnings import DBNLAPIIncompatibilityWarning


@dataclass(order=True)
class Version:
    """A class representing semantic versioning. Build metadata and prerelease information are ignored.

    :param major: Major version number
    :param minor: Minor version number
    :param patch: Patch version number
    """

    # https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
    REGEX = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        """Convert the version to a string.

        :return: Version string
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, version: str) -> "Version":
        """Parse a version string into a Version object.

        :param version: Version string
        :return: Version object
        """
        match = re.match(cls.REGEX, version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")

        groupdict = match.groupdict()
        return cls(
            major=int(groupdict["major"]),
            minor=int(groupdict["minor"]),
            patch=int(groupdict["patch"]),
        )


MIN_SUPPORTED_API_VERSION = Version(major=0, minor=18, patch=3)


def check_version_compatibility(api_version: Optional[str]) -> None:
    """
    Check if the API version is compatible with this SDK version.

    :param api_version: API version string from server
    """
    if not api_version:
        warnings.warn(
            "Could not determine API version from OpenAPI spec. Cannot validate API version compatibility with SDK.",
            DBNLAPIIncompatibilityWarning,
        )
        return

    try:
        api_v = Version.parse(api_version)
    except ValueError:
        if api_version == "v0":
            api_v = Version(major=0, minor=0, patch=0)
        else:
            warnings.warn(
                f"Invalid API version format: {api_version}. Cannot validate API version compatibility with SDK.",
                DBNLAPIIncompatibilityWarning,
            )
            return

    if api_v < MIN_SUPPORTED_API_VERSION:
        warnings.warn(
            f"API version {api_version} is not compatible with SDK version {sdk_version}. "
            f"Minimum required API version is {MIN_SUPPORTED_API_VERSION}.",
            DBNLAPIIncompatibilityWarning,
        )
