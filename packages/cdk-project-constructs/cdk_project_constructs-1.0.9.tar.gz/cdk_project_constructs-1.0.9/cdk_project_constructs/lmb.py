from typing import Union, Optional, Sequence, Mapping

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_signer as signer
import aws_cdk.aws_logs as logs
from constructs import Construct


class AWSLambdaFunction(Construct):
    """Create Lambda function and releted objects like lambda layer, signing
    config and profile, IAM role and policies."""

    # pylint: disable=W0235
    # pylint: disable=W0622
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def signing_profile(self, signing_profile_name: str, construct_id: str = "signing-profile") -> signer.ISigningProfile:
        """Creates a code signing profile using AWS Signer to be used in a code
        signing configuration for a Lambda function.

        Args:
            signing_profile_name (str): The name for the signing profile.
            construct_id (str): The ID of the construct. Defaults to "signing-profile".

        Returns:
            signer.ISigningProfile: The created AWS Signer signing profile.
        """
        return signer.SigningProfile(
            self,
            id=construct_id,
            platform=signer.Platform.AWS_LAMBDA_SHA384_ECDSA,
            signing_profile_name=signing_profile_name,
        )

    def signing_config(self, profile: signer.ISigningProfile, construct_id: str = "code-signing-config") -> lmb.ICodeSigningConfig:
        """Creates a code signing configuration for a Lambda function using an
        AWS Signer signing profile.

        Args:
            profile (signer.ISigningProfile): The AWS Signer signing profile to use for code signing.
            construct_id (str): The ID of the construct.

        Returns:
            lmb.ICodeSigningConfig: The created code signing configuration.
        """

        return lmb.CodeSigningConfig(self, id=construct_id, signing_profiles=[profile])

    def create_log_group(self, log_group_name: str, retention: logs.RetentionDays):
        """Creates a log group for the Lambda function.

        Returns:
            The LogGroup object.

        It creates a log group with the given name.
        """
        return logs.LogGroup(
            self,
            "log-group",
            log_group_name=f"/service/lambda/{log_group_name}",
            log_group_class=logs.LogGroupClass.STANDARD,
            retention=retention,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

    def create_lambda_layer(self, code_path: str, config_vars, runtimes: list[lmb.Runtime], construct_id: str = "supporting_libraries") -> lmb.LayerVersion:
        """Create a new AWS Lambda layer with the specified configuration.

        Args:
            code_path (str): The path to the directory containing the Lambda layer code.
            config_vars: Props dictionary loaded from yaml config file to be validated.
            runtimes (list[lmb.Runtime]): The list of Lambda runtimes that the layer is compatible with.
            construct_id (str): The ID of the construct.

        Returns:
            lmb.LayerVersion: The created Lambda layer.
        """
        return lmb.LayerVersion(
            self,
            id=construct_id,
            code=lmb.Code.from_asset(code_path),
            compatible_runtimes=runtimes,
            description=f"Supporting libs layer for {config_vars.project}",
        )

    # pylint: disable=R0913
    def create_lambda_function(
        self,
        code_path: str,
        function_name: str,
        env: cdk.Environment,
        layers: list[lmb.ILayerVersion] | list[lmb.LayerVersion],
        timeout: int,
        reserved_concurrent_executions: Union[None, int],
        env_variables: Mapping,
        role: Union[None, iam.Role] = None,
        signing_config: Union[lmb.ICodeSigningConfig, None] = None,
        architecture: lmb.Architecture = lmb.Architecture.ARM_64,
        runtime: lmb.Runtime = lmb.Runtime.PYTHON_3_11,
        memory_size: int = 128,
        handler: str = "lambda_handler.handler",
        profiling: bool = False,
        tracing: lmb.Tracing = lmb.Tracing.DISABLED,
        vpc: Optional[ec2.IVpc] = None,
        vpc_subnets: Optional[ec2.SubnetSelection] = None,
        security_groups: Optional[Sequence[ec2.ISecurityGroup]] = None,
        log_level: str = "INFO",
        log_group: Optional[logs.ILogGroup] = None,
        log_retention: logs.RetentionDays = logs.RetentionDays.ONE_MONTH,
        insights_version: lmb.LambdaInsightsVersion | None = lmb.LambdaInsightsVersion.VERSION_1_0_229_0,
        on_failure: lmb.IDestination | None = None,
        on_success: lmb.IDestination | None = None,
    ) -> lmb.Function:
        """Create a new AWS Lambda function with the specified configuration.

        Args:
            code_path (str): The path to the directory containing the Lambda function code.
            function_name (str): The name of the Lambda function.
            env (cdk.Environment): The AWS environment in which to create the Lambda function.
            layers (list[lmb.ILayerVersion] | list[lmb.LayerVersion]): The Lambda layers to attach to the function.
            timeout (int): The maximum execution time for the Lambda function in seconds.
            reserved_concurrent_executions (Union[None, int]): The maximum number of concurrent executions for the Lambda function.
            env_variables (Mapping): The environment variables to set for the Lambda function.
            role (Union[None, iam.Role]): The IAM role to use for the Lambda function.
            signing_config (Union[lmb.ICodeSigningConfig, None]): The code signing configuration for the Lambda function.
            architecture (lmb.Architecture): The CPU architecture for the Lambda function.
            runtime (lmb.Runtime): The runtime for the Lambda function.
            memory_size (int): The amount of memory to allocate to the Lambda function in MB.
            handler (str): The name of the function handler.
            profiling (bool): Whether to enable profiling for the Lambda function.
            tracing (lmb.Tracing): The tracing configuration for the Lambda function.
            vpc (Optional[ec2.IVpc]): The VPC to use for the Lambda function.
            vpc_subnets (Optional[ec2.SubnetSelection]): The VPC subnets to use for the Lambda function.
            security_groups (Optional[Sequence[ec2.ISecurityGroup]]): The security groups to use for the Lambda function.
            log_level (str): The log level for the Lambda function.
            log_group (Optional[logs.ILogGroup]): The log group to use for the Lambda function.
            log_retention (logs.RetentionDays): The log retention period for the Lambda function.
            insights_version (lmb.LambdaInsightsVersion | None): The version of AWS Lambda Insights to use.
            on_failure (lmb.IDestination | None): The destination for failed invocations of the Lambda function.
            on_success (lmb.IDestination | None): The destination for successful invocations of the Lambda function.

        Returns:
            lmb.Function: The created Lambda function.
        """
        lambda_environment_default_variables = {
            "LOGGER_SAMPLE_RATE": "1",
            "LOG_LEVEL": log_level,
            "METRICS_NAMESPACE": function_name,
            "METRICS_SERVICE_NAME": function_name,
            "REGION": env.region,
        }

        combined_env_variables = dict(lambda_environment_default_variables, **env_variables)

        return lmb.Function(
            self,
            architecture=architecture,
            code=lmb.Code.from_asset(code_path),
            code_signing_config=signing_config,
            environment=combined_env_variables,
            function_name=function_name,
            handler=handler,
            id=function_name,
            initial_policy=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["logs:CreateLogGroup"],
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                    resources=["arn:aws:logs:*:*:log-group:/aws/lambda-insights:*"],
                ),
            ],
            insights_version=insights_version,
            layers=layers,
            log_retention=log_retention,
            memory_size=memory_size,
            profiling=profiling,
            reserved_concurrent_executions=reserved_concurrent_executions,
            runtime=runtime,
            timeout=cdk.Duration.minutes(timeout),
            tracing=tracing,
            role=role,
            vpc_subnets=vpc_subnets,
            vpc=vpc,
            security_groups=security_groups,
            log_group=log_group,
            on_failure=on_failure,
            on_success=on_success,
        )
