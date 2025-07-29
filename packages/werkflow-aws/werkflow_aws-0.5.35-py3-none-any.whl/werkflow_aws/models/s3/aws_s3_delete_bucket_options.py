from pydantic import (
    StrictStr
)

from typing import Optional
from werkflow_aws.models.base import AWSBoto3Base


class AWSs3DeleteBucketOptions(AWSBoto3Base):
    expected_bucket_owner: Optional[StrictStr]=None

