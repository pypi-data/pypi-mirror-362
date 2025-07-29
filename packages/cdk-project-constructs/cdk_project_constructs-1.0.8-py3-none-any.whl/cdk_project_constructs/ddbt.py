from typing import Union, Any, Optional

import aws_cdk as cdk
import aws_cdk.aws_kms as kms
import aws_cdk.aws_dynamodb as ddb
from constructs import Construct


class DDBTable(Construct):
    """Create AWS DynamoDB table."""

    # pylint: disable=W0235
    # pylint: disable=W0622
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_ddb_table(
        self,
        table_name: str,
        time_to_live_attribute: str,
        partition_key: Union[ddb.Attribute, dict[str, Any]],
        sort_key: Union[ddb.Attribute, dict[str, Any], None] = None,
        kms_key: Optional[kms.IKey] = None,
        read_capacity: Optional[Union[int, float, None]] = None,
        write_capacity: Optional[Union[int, float, None]] = None,
        table_class: ddb.TableClass = ddb.TableClass.STANDARD,
        billing_mode: ddb.BillingMode = ddb.BillingMode.PAY_PER_REQUEST,
        removal_policy: cdk.RemovalPolicy = cdk.RemovalPolicy.DESTROY,
        encryption: ddb.TableEncryption = ddb.TableEncryption.DEFAULT,
        point_in_time_recovery: bool = False,
    ) -> ddb.Table:
        """Create an AWS DynamoDB table with the specified configuration.

        Args:
            table_name (str): The name of the DynamoDB table.
            time_to_live_attribute (str): The name of the attribute that will be used for time-to-live (TTL) functionality.
            partition_key (Union[ddb.Attribute, dict[str, Any]]): The partition key for the table.
            sort_key (Union[ddb.Attribute, dict[str, Any], None], optional): The sort key for the table, if any.
            kms_key (Optional[kms.IKey], optional): The KMS key to use for encryption.
            read_capacity (Optional[Union[int, float, None]], optional): The read capacity for the table.
            write_capacity (Optional[Union[int, float, None]], optional): The write capacity for the table.
            table_class (ddb.TableClass, optional): The table class to use.
            billing_mode (ddb.BillingMode, optional): The billing mode for the table.
            removal_policy (cdk.RemovalPolicy, optional): The removal policy for the table.
            encryption (ddb.TableEncryption, optional): The encryption method for the table.
            point_in_time_recovery (bool, optional): Whether to enable point-in-time recovery for the table.

        Returns:
            ddb.Table: The created DynamoDB table.
        """
        return ddb.Table(
            self,
            id=table_name,
            table_name=table_name,
            billing_mode=billing_mode,
            encryption=encryption,
            encryption_key=kms_key,
            point_in_time_recovery=point_in_time_recovery,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=removal_policy,
            table_class=table_class,
            time_to_live_attribute=time_to_live_attribute,
            partition_key=partition_key,
            sort_key=sort_key,
        )
