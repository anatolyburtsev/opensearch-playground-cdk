from aws_cdk import (
    Stack,
    CfnOutput,
)
from aws_cdk.aws_opensearchservice import (
    Domain,
    EngineVersion,
    EbsOptions,
    EncryptionAtRestOptions,
    LoggingOptions,
)

from constructs import Construct


class CdkOpensearchLambdaPlaygroundStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain = Domain(
            self,
            "Domain",
            domain_name="open-search-hello-world",
            version=EngineVersion.OPENSEARCH_2_5,
            ebs=EbsOptions(volume_size=20),
            node_to_node_encryption=True,
            encryption_at_rest=EncryptionAtRestOptions(enabled=True),
            logging=LoggingOptions(
                slow_search_log_enabled=True,
                app_log_enabled=True,
                slow_index_log_enabled=True,
            ),
        )

        CfnOutput(
            self,
            "OpenSearch Endpoint",
            description="OpenSearch Endpoint",
            value=domain.domain_endpoint,
        )
