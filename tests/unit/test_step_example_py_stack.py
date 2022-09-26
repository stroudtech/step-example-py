import aws_cdk as core
import aws_cdk.assertions as assertions

from step_example_py.step_example_py_stack import StepExamplePyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in step_example_py/step_example_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StepExamplePyStack(app, "step-example-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
