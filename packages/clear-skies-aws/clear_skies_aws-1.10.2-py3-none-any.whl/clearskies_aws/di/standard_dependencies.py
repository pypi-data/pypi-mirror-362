from types import ModuleType

import boto3 as boto3_module
from boto3.session import Session as Boto3Session
from clearskies import Environment
from clearskies.di import StandardDependencies as DefaultStandardDependencies

from ..backends import (
    DynamoDBBackend,
    DynamoDBPartiQLBackend,
    DynamoDBPartiQLCursor,
    SqsBackend,
)
from ..secrets import ParameterStore


class StandardDependencies(DefaultStandardDependencies):

    def provide_dynamo_db_parti_ql_cursor(
        self, boto3_session: Boto3Session
    ) -> DynamoDBPartiQLCursor:
        return DynamoDBPartiQLCursor(boto3_session)

    def provide_dynamo_db_backend(
        self, boto3: ModuleType, environment: Environment
    ) -> DynamoDBBackend:
        return DynamoDBBackend(boto3, environment)

    def provide_dynamo_db_parti_ql_backend(
        self, dynamo_db_parti_ql_cursor: DynamoDBPartiQLCursor, environment: Environment
    ) -> DynamoDBPartiQLBackend:
        return DynamoDBPartiQLBackend(dynamo_db_parti_ql_cursor)

    def provide_sqs_backend(
        self, boto3: ModuleType, environment: Environment
    ) -> SqsBackend:
        return SqsBackend(boto3, environment)

    def provide_boto3(self) -> ModuleType:
        import boto3
        return boto3

    def provide_secrets(
        self, boto3: ModuleType, environment: Environment
    ) -> ParameterStore:
        # This is just here so that we can auto-inject the secrets into the environment without having
        # to force the developer to define a secrets manager
        return ParameterStore(boto3, environment)

    def provide_boto3_session(
        self, boto3: ModuleType, environment: Environment
    ) -> boto3_module.session.Session:

        if not environment.get("AWS_REGION", True):
            raise ValueError(
                "To use AWS Session you must use set AWS_REGION in the .env file or an environment variable"
            )

        session = boto3.session.Session(region_name=environment.get("AWS_REGION", True))
        return session
