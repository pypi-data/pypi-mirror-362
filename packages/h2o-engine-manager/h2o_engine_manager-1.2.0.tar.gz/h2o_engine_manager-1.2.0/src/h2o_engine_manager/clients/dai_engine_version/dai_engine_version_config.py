from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.dai_engine_version.version import DAIEngineVersion


class DAIEngineVersionConfig:
    """
    DAIEngineVersion configuration used as input for apply method.
    """

    def __init__(
        self,
        dai_engine_version_id: str,
        image: str,
        deprecated: bool = False,
        aliases: Optional[List[str]] = None,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: Optional[List[str]] = None,
    ):
        self.dai_engine_version_id = dai_engine_version_id
        self.image = image
        self.deprecated = deprecated
        self.aliases = aliases
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets

    def to_dai_engine_version(self):
        return DAIEngineVersion(
            image=self.image,
            deprecated=self.deprecated,
            aliases=self.aliases,
            image_pull_policy=self.image_pull_policy,
            image_pull_secrets=self.image_pull_secrets,
        )
