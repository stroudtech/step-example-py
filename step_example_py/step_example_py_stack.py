from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_stepfunctions_tasks as tasks,
    aws_stepfunctions as sfn,
)
from constructs import Construct

class StepExamplePyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        start_fn = _lambda.Function(
            self,
            "StartFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="start.handler"
        )
        start = tasks.LambdaInvoke(
            self,
            "StartTask",
            lambda_function=start_fn,
            integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
            payload=sfn.TaskInput.from_object({
                "token": sfn.JsonPath.task_token,
                "input": sfn.JsonPath.string_at("$.someField"),
            })
        )
        success_fn = _lambda.Function(
            self,
            "SuccessFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="success.handler"
        )
        success = tasks.LambdaInvoke(
            self,
            "SuccessTask",
            lambda_function=success_fn,
            output_path="$.Payload"
        )

        definition = start.next(success)
        state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
        )

        start_fn.grant_invoke(state_machine.role)
        success_fn.grant_invoke(state_machine.role)
