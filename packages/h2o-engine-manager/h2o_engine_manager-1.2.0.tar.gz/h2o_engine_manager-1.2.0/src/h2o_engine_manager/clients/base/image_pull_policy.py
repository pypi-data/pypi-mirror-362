from enum import Enum

from h2o_engine_manager.gen.model.v1_image_pull_policy import V1ImagePullPolicy
from h2o_engine_manager.gen.model.v1_image_pull_policy import (
    V1ImagePullPolicy as InternalDAIVersionImagePullPolicy,
)
from h2o_engine_manager.gen.model.v1_image_pull_policy import (
    V1ImagePullPolicy as InternalH2OVersionImagePullPolicy,
)


class ImagePullPolicy(Enum):
    IMAGE_PULL_POLICY_UNSPECIFIED = "IMAGE_PULL_POLICY_UNSPECIFIED"
    IMAGE_PULL_POLICY_ALWAYS = "IMAGE_PULL_POLICY_ALWAYS"
    IMAGE_PULL_POLICY_NEVER = "IMAGE_PULL_POLICY_NEVER"
    IMAGE_PULL_POLICY_IF_NOT_PRESENT = "IMAGE_PULL_POLICY_IF_NOT_PRESENT"

    def to_api_object(self) -> V1ImagePullPolicy:
        return V1ImagePullPolicy(self.name)

    def to_idaiv_api_image_pull_policy(self) -> InternalDAIVersionImagePullPolicy:
        return InternalDAIVersionImagePullPolicy(self.name)

    def to_ih2ov_api_image_pull_policy(self) -> InternalH2OVersionImagePullPolicy:
        return InternalH2OVersionImagePullPolicy(self.name)


def from_image_pull_policy_api_object(api_object: V1ImagePullPolicy) -> ImagePullPolicy:
    return ImagePullPolicy(str(api_object))


def from_idaiv_api_image_pull_policy_to_custom(state: InternalDAIVersionImagePullPolicy) -> ImagePullPolicy:
    return ImagePullPolicy(str(state))


def from_ih2ov_api_image_pull_policy_to_custom(state: InternalH2OVersionImagePullPolicy) -> ImagePullPolicy:
    return ImagePullPolicy(str(state))
