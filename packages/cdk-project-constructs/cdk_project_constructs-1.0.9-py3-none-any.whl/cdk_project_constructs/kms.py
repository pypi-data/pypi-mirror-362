from typing import Union, List, Any

import aws_cdk as cdk
import aws_cdk.aws_kms as kms
import aws_cdk.aws_iam as iam
from constructs import Construct


class KMSKey(Construct):
    """Create KMS key with enabled key rotation."""

    # pylint: disable=W0235
    # pylint: disable=W0622
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_kms_key(
        self, alias: str, description: str, aws_accounts: Union[List[Any], None] | None = None, multi_region: bool = False, admins: List[iam.IPrincipal] | None = None
    ) -> kms.Key:
        """Create shared AWS KMS key to be used across multiple services in the
        project.

        Args:
            alias (str): Initial alias to add to the key.
            description (str): A description of the key.
            aws_accounts (Union[List[Any], None]): List of AWS accounts which can use the key.
            multi_region (bool): Whether to create a multi-region KMS key.
            admins (List[iam.IPrincipal]): List of IAM principals that should have admin access to the KMS key.

        Returns:
            cdk.aws_kms.Key: CDK KMS key object
        """
        if aws_accounts is None:
            aws_accounts = []

        kms_key = kms.Key(
            self,
            id="shared_kms_key",
            alias=alias,
            description=description,
            enabled=True,
            enable_key_rotation=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            pending_window=cdk.Duration.days(7),
            multi_region=multi_region,
            admins=admins,
        )

        if aws_accounts:
            for aws_account in aws_accounts:
                kms_key.add_to_resource_policy(
                    iam.PolicyStatement(
                        sid=f"AllowAWSAccountAccessToKMS{aws_account}",
                        resources=["*"],
                        principals=[iam.AccountPrincipal(aws_account)],
                        actions=[
                            "kms:Encrypt",
                            "kms:Decrypt",
                            "kms:ReEncrypt*",
                            "kms:GenerateDataKey*",
                            "kms:DescribeKey",
                            "kms:CreateGrant",
                            "kms:ListGrants",
                            "kms:RevokeGrant",
                        ],
                    )
                )

        return kms_key
