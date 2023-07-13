import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_opensearch_lambda_playground.cdk_opensearch_lambda_playground_stack import CdkOpensearchLambdaPlaygroundStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_opensearch_lambda_playground/cdk_opensearch_lambda_playground_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkOpensearchLambdaPlaygroundStack(app, "cdk-opensearch-lambda-playground")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
