import pprint
from datetime import datetime
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.base.image_pull_policy import (
    from_image_pull_policy_api_object,
)
from h2o_engine_manager.gen.model.required_dai_engine_version_resource import (
    RequiredDAIEngineVersionResource,
)
from h2o_engine_manager.gen.model.v1_dai_engine_version import V1DAIEngineVersion


class DAIEngineVersion:
    """
    DAIEngineVersion represents Driverless AI version that can be used in DAIEngine.
    """

    def __init__(
        self,
        image: str,
        name: str = "",
        deprecated: bool = False,
        aliases: Optional[List[str]] = None,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: Optional[List[str]] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
    ):
        """
        DAIEngineVersion represents a set of values that are used for DAIEngine.

        Args:
            image: Name of the Docker image used when using this DAIEngineVersion.
            name: Resource name. Format "workspaces/*/daiEngineVersions/*".
            deprecated: Indicates whether DAIEngineVersion is deprecated.
            aliases: Resource ID aliases for this DAIEngineVersion.
                Aliases are unique within the workspace.
                Any alias must be in format:
                    - contain 1-63 characters
                    - contain only lowercase alphanumeric characters or hyphen ('-')
                    - start with an alphabetic character
                    - end with an alphanumeric character
            image_pull_policy: Image pull policy applied when using this DAIEngineVersion.
                When unset, server will choose a default one.
            image_pull_secrets: List of references to k8s secrets that can be used for pulling an image
                of this DAIEngineVersion from a private container image registry or repository.
            create_time: Time when the DAIEngineVersion was created.
            update_time: Time when the DAIEngineVersion was last updated.
            creator: Name of entity that created the DAIEngineVersion.
            updater: Name of entity that last updated the DAIEngineVersion.
            creator_display_name: Human-readable name of entity that created the DAIEngineVersion.
            updater_display_name: Human-readable name of entity that last updated the DAIEngineVersion.
        """
        if aliases is None:
            aliases = []

        if image_pull_secrets is None:
            image_pull_secrets = []

        self.name = name
        self.image = image
        self.deprecated = deprecated
        self.aliases = aliases
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self) -> V1DAIEngineVersion:
        return V1DAIEngineVersion(
            image=self.image,
            deprecated=self.deprecated,
            aliases=self.aliases,
            image_pull_policy=self.image_pull_policy.to_api_object(),
            image_pull_secrets=self.image_pull_secrets,
        )

    def to_resource(self) -> RequiredDAIEngineVersionResource:
        return RequiredDAIEngineVersionResource(
            image=self.image,
            deprecated=self.deprecated,
            aliases=self.aliases,
            image_pull_policy=self.image_pull_policy.to_api_object(),
            image_pull_secrets=self.image_pull_secrets,
        )


def from_api_object(api_object: V1DAIEngineVersion) -> DAIEngineVersion:
    return DAIEngineVersion(
        image=api_object.image,
        name=api_object.name,
        deprecated=api_object.deprecated,
        aliases=api_object.aliases,
        image_pull_policy=from_image_pull_policy_api_object(api_object.image_pull_policy),
        image_pull_secrets=api_object.image_pull_secrets,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
    )


def from_api_objects(api_objects: List[V1DAIEngineVersion]) -> List[DAIEngineVersion]:
    return [from_api_object(api_object) for api_object in api_objects]
