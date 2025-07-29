from typing import List, Union

import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_kms as kms
from constructs import Construct


class S3Bucket(Construct):
    """Create S3 bucket with restricted public access, and enforced SSL for
    data transit."""

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_bucket(
        self,
        bucket_name: str,
        encryption: s3.BucketEncryption,
        kms_key: kms.IKey | None = None,
        enforce_ssl: bool = True,
        server_access_logs_bucket: s3.IBucket | None = None,
        server_access_logs_prefix: str | None = None,
        lifecycle_rules: List[s3.LifecycleRule] | None = None,
        minimum_tls_version: Union[int, float] = 1.2,
    ) -> s3.Bucket:
        """Create an S3 bucket with the specified configuration.

        Args:
            bucket_id (str): The ID of the S3 bucket.
            bucket_name (str): The name of the S3 bucket.
            encryption (s3.BucketEncryption): The type of encryption to use for the bucket.
            kms_key (kms.IKey, optional): The KMS key to use for encryption.
            enforce_ssl (bool, optional): Whether to enforce SSL for accessing the bucket.
            server_access_logs_bucket (s3.IBucket, optional): The S3 bucket to store server access logs.
            server_access_logs_prefix (str, optional): The prefix to use for storing server access logs.
            lifecycle_rules (List[s3.LifecycleRule], optional): The lifecycle rules to apply to the bucket.
            minimum_tls_version (Union[int, float], optional): The minimum TLS version to use for accessing the bucket.

        Returns:
            s3.Bucket: The created S3 bucket.
        """

        return s3.Bucket(
            self,
            id=bucket_name,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True,
            ),
            bucket_name=bucket_name,
            encryption=encryption,
            encryption_key=kms_key,
            enforce_ssl=enforce_ssl,
            minimum_tls_version=minimum_tls_version,
            lifecycle_rules=lifecycle_rules,
            public_read_access=False,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            server_access_logs_prefix=server_access_logs_prefix,
            server_access_logs_bucket=server_access_logs_bucket,
            versioned=True,
        )
