from typing import Union

import aws_cdk.aws_sns as sns
import aws_cdk.aws_kms as kms
from constructs import Construct


class SNSTopic(Construct):
    """Create SNS Topic with enforced SSL for data transit."""

    # pylint: disable=W0235
    # pylint: disable=W0622
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_sns_topic(
        self,
        topic_name: str,
        master_key: Union[kms.IKey, None],
        enforce_ssl: bool = True,
        is_fifo: bool = False,
        message_retention_period_in_days: int | None = None,
        content_based_deduplication: bool | None = None,
        tracing_config: Union[sns.TracingConfig, None] = sns.TracingConfig.PASS_THROUGH,
    ) -> sns.Topic:
        """Create an SNS topic with optional SSL enforcement, KMS encryption,
        FIFO configuration, and other settings.

        Args:
            topic_name (str): The name of the SNS topic.
            master_key (Union[aws_cdk.aws_kms.IKey, None]): The KMS key to encrypt messages going through the SNS topic.x
            enforce_ssl (bool, optional): Whether to enforce SSL for data transit. Defaults to True.
            is_fifo (bool, optional): Whether the SNS topic should be a FIFO topic. Defaults to False.
            message_retention_period_in_days (int, optional): The number of days to retain messages in the SNS topic.
            content_based_deduplication (bool, optional): Whether to enable content-based deduplication for the FIFO topic.
            tracing_config (Union[aws_cdk.aws_sns.TracingConfig, None], optional): The tracing configuration for the SNS topic. Defaults to TracingConfig.PASS_THROUGH.

        Returns:
            aws_cdk.aws_sns.Topic: The created SNS topic.
        """
        return sns.Topic(
            self,
            id=topic_name,
            topic_name=topic_name,
            display_name=topic_name,
            master_key=master_key,
            fifo=is_fifo,
            enforce_ssl=enforce_ssl,
            message_retention_period_in_days=message_retention_period_in_days,
            content_based_deduplication=content_based_deduplication,
            tracing_config=tracing_config,
        )
