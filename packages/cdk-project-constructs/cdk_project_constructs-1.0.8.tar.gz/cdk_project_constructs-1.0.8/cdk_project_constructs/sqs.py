import aws_cdk as cdk
import aws_cdk.aws_sqs as sqs
from constructs import Construct


class SQSQueue(Construct):
    """Create AWS SQS DLQ, Standard and FIFO queue with enforced SSL for data
    transfer."""

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_dlq_queue(
        self,
        queue_name: str,
        enforce_ssl: bool = True,
    ):
        """Create SQS DLQ queue used by standard or fifo queue.

        :param enforce_ssl: By default access to the DLQ queue must be through encrypted channel - HTTPS
        :param queue_name: The name of DLQ queue
        :return: CDK SQS queue object
        """
        return sqs.Queue(self, id="sqs_dlq", enforce_ssl=enforce_ssl, queue_name=queue_name, retention_period=cdk.Duration.days(amount=7), removal_policy=cdk.RemovalPolicy.DESTROY)

    def create_standard_queue(
        self,
        dead_letter_queue: sqs.Queue,
        queue_name: str,
        visibility_timeout: int,
        delivery_delay: cdk.Duration,
        receive_message_wait_time: cdk.Duration,
        enforce_ssl: bool = True,
    ) -> sqs.Queue:
        """Create SQS Standard Queue.

        :param enforce_ssl: By default access to the DLQ queue must be through encrypted channel - HTTPS
        :param dead_letter_queue: The CDK object for SQS DQL queue
        :param queue_name: Then name of SQS queue
        :param visibility_timeout: The message visibility timeout
        :return: CDK SQS queue object
        """
        return sqs.Queue(
            self,
            id="sqs_queue",
            enforce_ssl=enforce_ssl,
            data_key_reuse=cdk.Duration.days(amount=1),
            dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3, queue=dead_letter_queue),
            queue_name=queue_name,
            retention_period=cdk.Duration.days(amount=7),
            visibility_timeout=cdk.Duration.minutes(amount=visibility_timeout),  # 3-6x than lambda timeout
            delivery_delay=delivery_delay,
            receive_message_wait_time=receive_message_wait_time,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

    def create_fifo_queue(
        self,
        dead_letter_queue: sqs.Queue,
        queue_name: str,
        visibility_timeout: int,
        delivery_delay: cdk.Duration,
        receive_message_wait_time: cdk.Duration,
        enforce_ssl: bool = True,
        content_based_deduplication: bool = True,
        deduplication_scope: sqs.DeduplicationScope = sqs.DeduplicationScope.QUEUE,
        fifo: bool = True,
    ) -> sqs.Queue:
        """Create SQS FIFO Queue.

        :param enforce_ssl: By default access to the DLQ queue must be through encrypted channel - HTTPS
        :param dead_letter_queue: The CDK object for SQS DQL queue
        :param queue_name: Then name of SQS queue
        :param visibility_timeout: The message visibility timeout
        :param delivery_delay: The delivery delay for messages in the queue
        :param receive_message_wait_time: The receive message wait time for the queue
        :param content_based_deduplication: Whether to enable content-based deduplication for the queue
        :param deduplication_scope: The deduplication scope for the queue
        :param fifo: Whether the queue should be a FIFO queue
        :return: CDK SQS queue object
        """
        return sqs.Queue(
            self,
            id="sqs_queue",
            enforce_ssl=enforce_ssl,
            data_key_reuse=cdk.Duration.days(amount=1),
            dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3, queue=dead_letter_queue),
            queue_name=f"{queue_name}.fifo",
            retention_period=cdk.Duration.days(amount=7),
            visibility_timeout=cdk.Duration.minutes(amount=visibility_timeout),  # 3-6x than lambda timeout
            content_based_deduplication=content_based_deduplication,
            deduplication_scope=deduplication_scope,
            delivery_delay=delivery_delay,
            fifo=fifo,
            receive_message_wait_time=receive_message_wait_time,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
