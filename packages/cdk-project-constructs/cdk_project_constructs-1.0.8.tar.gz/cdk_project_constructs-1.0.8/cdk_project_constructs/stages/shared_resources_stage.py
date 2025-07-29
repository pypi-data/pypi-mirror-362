"""The AWS shared resources for core application stage."""

import aws_cdk as cdk

from cdk_project_constructs.stacks.governance_stack import GovernanceStack
from cdk_project_constructs.stacks.notifications_stack import NotificationsStack
from constructs import Construct


class SharedResourcesStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment, props: dict, **kwargs) -> None:
        """
        Parameters:

        - scope (Construct): The parent constructs that this stage is defined within.

        - construct_id (str): The id of this stage construct.

        - env (cdk.Environment): The CDK environment this stage is targeting.

        - props (dict): Additional properties passed to this stage.

        Functionality:

        Defines a CDK stage that contains shared resources for the application.

        The stage first calls the parent class constructor to initialize the stage.

        It then creates a NotificationsStack construct, passing the scope, a construct id,
        the environment, and any props. This will construct the notification resources for
        the app.

        """

        super().__init__(scope, construct_id, env=env, **kwargs)

        notifications_stack = NotificationsStack(
            self,
            construct_id="notifications-stack",
            env=env,
            props=props,
        )

        governance_stack = GovernanceStack(
            self,
            construct_id="governance-stack",
            env=env,
            props=props,
        )
        governance_stack.add_dependency(notifications_stack)
