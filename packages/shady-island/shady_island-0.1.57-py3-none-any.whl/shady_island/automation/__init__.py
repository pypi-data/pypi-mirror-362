from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class ContainerImagePipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.automation.ContainerImagePipeline",
):
    '''Allows images pushed to an ECR repo to trigger updates to an ECS service.

    This construct produces a CodePipeline pipeline using the "ECR Source"
    action, an "ECS Deploy" action, and a custom Lambda handler in between that
    transforms the JSON from the "Source" action into the JSON needed for the
    "Deploy" action.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container: builtins.str,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
        service: _aws_cdk_aws_ecs_ceddda9d.IBaseService,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        pipeline_type: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new ContainerImagePipeline.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param container: The name of the container in the task definition to update.
        :param repository: The ECR repository where images will be pushed.
        :param service: The ECS service to update when an image is pushed to the ECR repository.
        :param artifact_bucket: A custom bucket for artifacts. Default: - A new bucket will be created
        :param pipeline_type: The pipeline type (V1 or V2). Default: - V1
        :param tag: The container image tag to observe for changes in the ECR repository. Default: - "latest"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cedb29f5ea4e41db2040cf196e8fb5c9c4a295ca5a54967d23de3d82284bb5a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerImagePipelineProps(
            container=container,
            repository=repository,
            service=service,
            artifact_bucket=artifact_bucket,
            pipeline_type=pipeline_type,
            tag=tag,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> _aws_cdk_aws_codepipeline_ceddda9d.Pipeline:
        '''The CodePipeline pipeline.'''
        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.Pipeline, jsii.get(self, "pipeline"))


@jsii.data_type(
    jsii_type="shady-island.automation.ContainerImagePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "repository": "repository",
        "service": "service",
        "artifact_bucket": "artifactBucket",
        "pipeline_type": "pipelineType",
        "tag": "tag",
    },
)
class ContainerImagePipelineProps:
    def __init__(
        self,
        *,
        container: builtins.str,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
        service: _aws_cdk_aws_ecs_ceddda9d.IBaseService,
        artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        pipeline_type: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the ContainerImagePipeline constructor.

        :param container: The name of the container in the task definition to update.
        :param repository: The ECR repository where images will be pushed.
        :param service: The ECS service to update when an image is pushed to the ECR repository.
        :param artifact_bucket: A custom bucket for artifacts. Default: - A new bucket will be created
        :param pipeline_type: The pipeline type (V1 or V2). Default: - V1
        :param tag: The container image tag to observe for changes in the ECR repository. Default: - "latest"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82c69c46656ae83e2077c89d799ffb8536b4ddcc17b205a38a2221073be2e48)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument artifact_bucket", value=artifact_bucket, expected_type=type_hints["artifact_bucket"])
            check_type(argname="argument pipeline_type", value=pipeline_type, expected_type=type_hints["pipeline_type"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
            "repository": repository,
            "service": service,
        }
        if artifact_bucket is not None:
            self._values["artifact_bucket"] = artifact_bucket
        if pipeline_type is not None:
            self._values["pipeline_type"] = pipeline_type
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def container(self) -> builtins.str:
        '''The name of the container in the task definition to update.'''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        '''The ECR repository where images will be pushed.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, result)

    @builtins.property
    def service(self) -> _aws_cdk_aws_ecs_ceddda9d.IBaseService:
        '''The ECS service to update when an image is pushed to the ECR repository.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.IBaseService, result)

    @builtins.property
    def artifact_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''A custom bucket for artifacts.

        :default: - A new bucket will be created
        '''
        result = self._values.get("artifact_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def pipeline_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType]:
        '''The pipeline type (V1 or V2).

        :default: - V1
        '''
        result = self._values.get("pipeline_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The container image tag to observe for changes in the ECR repository.

        :default: - "latest"
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImagePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ContainerImagePipeline",
    "ContainerImagePipelineProps",
]

publication.publish()

def _typecheckingstub__cedb29f5ea4e41db2040cf196e8fb5c9c4a295ca5a54967d23de3d82284bb5a4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container: builtins.str,
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    service: _aws_cdk_aws_ecs_ceddda9d.IBaseService,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    pipeline_type: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82c69c46656ae83e2077c89d799ffb8536b4ddcc17b205a38a2221073be2e48(
    *,
    container: builtins.str,
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    service: _aws_cdk_aws_ecs_ceddda9d.IBaseService,
    artifact_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    pipeline_type: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.PipelineType] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
