from datetime import datetime
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.base.image_pull_policy import (
    from_image_pull_policy_api_object,
)
from h2o_engine_manager.gen.model.v1_h2_o_engine_version_info import (
    V1H2OEngineVersionInfo,
)


class H2OEngineVersionInfo:
    """
    H2OEngineVersion data used during the last H2OEngine startup from the assigned h2o_engine_version.
    """

    def __init__(
        self,
        name: str = "",
        deprecated: bool = False,
        aliases: Optional[List[str]] = None,
        image: str = "",
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: Optional[List[str]] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
    ):
        if aliases is None:
            aliases = []

        if image_pull_secrets is None:
            image_pull_secrets = []

        self.name = name
        self.deprecated = deprecated
        self.aliases = aliases
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name


def from_h2o_engine_version_info_api_object(api_object: V1H2OEngineVersionInfo) -> H2OEngineVersionInfo:
    return H2OEngineVersionInfo(
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