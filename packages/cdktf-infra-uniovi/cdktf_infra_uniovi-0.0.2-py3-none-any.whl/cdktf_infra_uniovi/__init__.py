r'''
# cdktf-infra-uniovi

Repository for my End of Master's Project library
'''
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

from ._jsii import *

import cdktf as _cdktf_9a9027ec
import cdktf_cdktf_provider_aws.security_group as _cdktf_cdktf_provider_aws_security_group_0cbe8a87
import cdktf_cdktf_provider_docker.container as _cdktf_cdktf_provider_docker_container_ee71896e
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.AWSLampStackProps",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId", "vpc_id": "vpcId"},
)
class AWSLampStackProps:
    def __init__(
        self,
        *,
        subnet_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnet_id: Subnet ID where the machine will be deployed. This is an optional property, and if not specified, the default subnet will be used. If you specify a VPC, you must also specify a subnet within that VPC.
        :param vpc_id: Virtual Private Cloud (VPC) ID where the machine will be deployed. This is an optional property, and if not specified, the default VPC will be used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1c88e55650acb8cd26beb46e93279b6ab68082efb8a603c2d209d08ae25f77)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID where the machine will be deployed.

        This is an optional property, and if not specified, the default subnet will be used.
        If you specify a VPC, you must also specify a subnet within that VPC.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Virtual Private Cloud (VPC) ID where the machine will be deployed.

        This is an optional property, and if not specified, the default VPC will be used.
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AWSLampStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.AWSLempStackProps",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId", "vpc_id": "vpcId"},
)
class AWSLempStackProps:
    def __init__(
        self,
        *,
        subnet_id: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnet_id: Subnet ID where the machine will be deployed. This is an optional property, and if not specified, the default subnet will be used. If you specify a VPC, you must also specify a subnet within that VPC.
        :param vpc_id: Virtual Private Cloud (VPC) ID where the machine will be deployed. This is an optional property, and if not specified, the default VPC will be used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d0e2f1f5bfc6aaa08bf8524aded636bce2c90bb338d07a11b1dafbf67e7027)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID where the machine will be deployed.

        This is an optional property, and if not specified, the default subnet will be used.
        If you specify a VPC, you must also specify a subnet within that VPC.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Virtual Private Cloud (VPC) ID where the machine will be deployed.

        This is an optional property, and if not specified, the default VPC will be used.
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AWSLempStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlpineBasic(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.AlpineBasic",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "AlpineVersion",
        machine_props: typing.Union["BasicMachineComponentPropsInterface", typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab4b89ab300a09efded257e20057e657c525929c5dc6065dcd25c706a85e1f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: "ProviderType",
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05b14f4090e7b53cf7153776330e879424e0ef2d7bf74e4996449cf14a4315f)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="createdAlpineMachine")
    def _created_alpine_machine(
        self,
    ) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdAlpineMachine"))

    @_created_alpine_machine.setter
    def _created_alpine_machine(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fc86fbbfa58c958051ee8edaeb6588d07011d4493441d653ab7ea9f334e2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAlpineMachine", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="cdktf-infra-uniovi.AlpineVersion")
class AlpineVersion(enum.Enum):
    LATEST = "LATEST"


@jsii.enum(jsii_type="cdktf-infra-uniovi.ApachePhpVersion")
class ApachePhpVersion(enum.Enum):
    PHP_APACHE_8_2 = "PHP_APACHE_8_2"
    PHP_APACHE_8_3 = "PHP_APACHE_8_3"


class ApacheServerBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf-infra-uniovi.ApacheServerBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "ApacheVersion",
        server_props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfce72c124795bc07abd86c038f1657e7667a04a8940ca2617d97645a8a6183)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    @abc.abstractmethod
    def _deploy(
        self,
        strategy: "IDeployStrategy",
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: "ProviderType",
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242e20e5ecea7213fd0a62d403d97656f346fb7e68d8bbf0f7f4c28b10688d8e)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    @abc.abstractmethod
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getDockerProps")
    @abc.abstractmethod
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="supportedApacheImagesMap")
    @abc.abstractmethod
    def _supported_apache_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="createdApacheServer")
    def _created_apache_server(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdApacheServer"))

    @_created_apache_server.setter
    def _created_apache_server(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45edbfafca7edf65e7477cead254c2ca9c54a3540dce3edad8b996e60958250f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdApacheServer", value) # pyright: ignore[reportArgumentType]


class _ApacheServerBaseProxy(ApacheServerBase):
    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: "IDeployStrategy",
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab703c2304d30f51cda5145ddcecfdb9c622cdf8a4975523a7137e21d8bc2911)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b494b9acd5949030a62f4cb11b3e530363ee3cad9951871aa1ae04889f43d3)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16381f5fae20c854994c8a3ebe8c1c87f8720d0ab680f42ada041d25141480cd)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedApacheImagesMap")
    def _supported_apache_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedApacheImagesMap"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApacheServerBase).__jsii_proxy_class__ = lambda : _ApacheServerBaseProxy


@jsii.enum(jsii_type="cdktf-infra-uniovi.ApacheVersion")
class ApacheVersion(enum.Enum):
    LATEST = "LATEST"
    APACHE_DEBIAN = "APACHE_DEBIAN"
    APACHE_ALPINE = "APACHE_ALPINE"


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.BaseInfrastructureComponentProps",
    jsii_struct_bases=[],
    name_mapping={"provider_type": "providerType"},
)
class BaseInfrastructureComponentProps:
    def __init__(self, *, provider_type: "ProviderType") -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1301670514c8c4548413681cfd9ccb34f2f4031ab2ed7e49bcdb5e76ca7e405)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
        }

    @builtins.property
    def provider_type(self) -> "ProviderType":
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("ProviderType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseInfrastructureComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.BaseWebStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "my_sql_database": "mySqlDatabase",
        "my_sql_password": "mySqlPassword",
        "my_sql_root_password": "mySqlRootPassword",
        "my_sql_user": "mySqlUser",
        "my_sql_version": "mySqlVersion",
    },
)
class BaseWebStackProps:
    def __init__(
        self,
        *,
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ef02751303e2e918a9fa28cd7ddfbde85004b0b5cd4d2df0d7aaab56d85963)
            check_type(argname="argument my_sql_database", value=my_sql_database, expected_type=type_hints["my_sql_database"])
            check_type(argname="argument my_sql_password", value=my_sql_password, expected_type=type_hints["my_sql_password"])
            check_type(argname="argument my_sql_root_password", value=my_sql_root_password, expected_type=type_hints["my_sql_root_password"])
            check_type(argname="argument my_sql_user", value=my_sql_user, expected_type=type_hints["my_sql_user"])
            check_type(argname="argument my_sql_version", value=my_sql_version, expected_type=type_hints["my_sql_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if my_sql_database is not None:
            self._values["my_sql_database"] = my_sql_database
        if my_sql_password is not None:
            self._values["my_sql_password"] = my_sql_password
        if my_sql_root_password is not None:
            self._values["my_sql_root_password"] = my_sql_root_password
        if my_sql_user is not None:
            self._values["my_sql_user"] = my_sql_user
        if my_sql_version is not None:
            self._values["my_sql_version"] = my_sql_version

    @builtins.property
    def my_sql_database(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_root_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_user(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_version(self) -> typing.Optional["MySQLVersion"]:
        '''The type of stack being deployed.

        This property is used to determine the specific stack configuration and behavior.
        It is a mandatory property and must be one of the supported stack types.

        Example::

            StackType.LAMP
        '''
        result = self._values.get("my_sql_version")
        return typing.cast(typing.Optional["MySQLVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseWebStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.BasicAWSMachineComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "use_persistence": "usePersistence",
        "vpc_id": "vpcId",
    },
)
class BasicAWSMachineComponentProps:
    def __init__(
        self,
        *,
        security_group_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        use_persistence: typing.Optional[builtins.bool] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param security_group_id: Security Group ID to associate with the machine. This is an optional property, and if not specified, a newly created security group will be used.
        :param subnet_id: Subnet ID where the machine will be deployed. This is an optional property, and if not specified, the default subnet will be used. If you specify a VPC, you must also specify a subnet within that VPC.
        :param use_persistence: Whether to use persistence for the machine. This is an optional property, and if not specified, it defaults to false. If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        :param vpc_id: Virtual Private Cloud (VPC) ID where the machine will be deployed. This is an optional property, and if not specified, the default VPC will be used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0dfbf5fff865407a05f6cc613e9837be3a91fc970d20711fce3334718ccc7f)
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument use_persistence", value=use_persistence, expected_type=type_hints["use_persistence"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if use_persistence is not None:
            self._values["use_persistence"] = use_persistence
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Security Group ID to associate with the machine.

        This is an optional property, and if not specified, a newly created security group will be used.
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID where the machine will be deployed.

        This is an optional property, and if not specified, the default subnet will be used.
        If you specify a VPC, you must also specify a subnet within that VPC.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_persistence(self) -> typing.Optional[builtins.bool]:
        '''Whether to use persistence for the machine.

        This is an optional property, and if not specified, it defaults to false.
        If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        '''
        result = self._values.get("use_persistence")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Virtual Private Cloud (VPC) ID where the machine will be deployed.

        This is an optional property, and if not specified, the default VPC will be used.
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAWSMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.BasicDockerMachineComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "networks": "networks",
        "use_volume": "useVolume",
        "volumes": "volumes",
    },
)
class BasicDockerMachineComponentProps:
    def __init__(
        self,
        *,
        networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_volume: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param networks: Networks for the Docker container. This is an advanced property that allows you to specify multiple networks for the container. Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        :param use_volume: Whether you want to use a volume for the container or not; if not specified, it defaults to false. If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        :param volumes: List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema. Each volume must have a mandatory ``containerPath`` If ``useVolume`` is true, this property's value will be used to define the volumes for the container. If not specified, internally a default volume will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8278e4fc9967ab072168da7fd2d542df00a8b166f95e6e4c74cd945d3a90ab)
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument use_volume", value=use_volume, expected_type=type_hints["use_volume"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if networks is not None:
            self._values["networks"] = networks
        if use_volume is not None:
            self._values["use_volume"] = use_volume
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]]:
        '''Networks for the Docker container.

        This is an advanced property that allows you to specify multiple networks for the container.
        Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]], result)

    @builtins.property
    def use_volume(self) -> typing.Optional[builtins.bool]:
        '''Whether you want to use a volume for the container or not;

        if not specified, it defaults to false.
        If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        '''
        result = self._values.get("use_volume")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]]:
        '''List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema.

        Each volume must have a mandatory ``containerPath``
        If ``useVolume`` is true, this property's value will be used to define the volumes for the container.
        If not specified, internally a default volume will be created.
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicDockerMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.BasicMachineComponentPropsInterface",
    jsii_struct_bases=[BaseInfrastructureComponentProps],
    name_mapping={
        "provider_type": "providerType",
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
    },
)
class BasicMachineComponentPropsInterface(BaseInfrastructureComponentProps):
    def __init__(
        self,
        *,
        provider_type: "ProviderType",
        aws_props: typing.Optional[typing.Union[BasicAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[BasicDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param aws_props: 
        :param docker_props: 
        '''
        if isinstance(aws_props, dict):
            aws_props = BasicAWSMachineComponentProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = BasicDockerMachineComponentProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d96babee21da0697cf5cadc06b2fd6341ac04551e3e85e9119e157c9432906)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
        }
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props

    @builtins.property
    def provider_type(self) -> "ProviderType":
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("ProviderType", result)

    @builtins.property
    def aws_props(self) -> typing.Optional[BasicAWSMachineComponentProps]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional[BasicAWSMachineComponentProps], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[BasicDockerMachineComponentProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[BasicDockerMachineComponentProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicMachineComponentPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.CustomAWSMachineComponentProps",
    jsii_struct_bases=[BasicAWSMachineComponentProps],
    name_mapping={
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "use_persistence": "usePersistence",
        "vpc_id": "vpcId",
        "custom_user_data": "customUserData",
        "security_group_ingress_rules": "securityGroupIngressRules",
    },
)
class CustomAWSMachineComponentProps(BasicAWSMachineComponentProps):
    def __init__(
        self,
        *,
        security_group_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        use_persistence: typing.Optional[builtins.bool] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        custom_user_data: typing.Optional[builtins.str] = None,
        security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param security_group_id: Security Group ID to associate with the machine. This is an optional property, and if not specified, a newly created security group will be used.
        :param subnet_id: Subnet ID where the machine will be deployed. This is an optional property, and if not specified, the default subnet will be used. If you specify a VPC, you must also specify a subnet within that VPC.
        :param use_persistence: Whether to use persistence for the machine. This is an optional property, and if not specified, it defaults to false. If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        :param vpc_id: Virtual Private Cloud (VPC) ID where the machine will be deployed. This is an optional property, and if not specified, the default VPC will be used.
        :param custom_user_data: Allows the user to pass custom user data for the machine. This is an optional property; if specified, it will override any default user data that would be generated. You are usually okay with not passing this property, unless you have really specific requirements for the machine's initialization and want fine-grained control over the user data script.
        :param security_group_ingress_rules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d69ac0dad572bcb03bb2c83dbaf0274bc1e8a1bf86473767d9222c2291b770)
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument use_persistence", value=use_persistence, expected_type=type_hints["use_persistence"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument custom_user_data", value=custom_user_data, expected_type=type_hints["custom_user_data"])
            check_type(argname="argument security_group_ingress_rules", value=security_group_ingress_rules, expected_type=type_hints["security_group_ingress_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if use_persistence is not None:
            self._values["use_persistence"] = use_persistence
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if custom_user_data is not None:
            self._values["custom_user_data"] = custom_user_data
        if security_group_ingress_rules is not None:
            self._values["security_group_ingress_rules"] = security_group_ingress_rules

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Security Group ID to associate with the machine.

        This is an optional property, and if not specified, a newly created security group will be used.
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID where the machine will be deployed.

        This is an optional property, and if not specified, the default subnet will be used.
        If you specify a VPC, you must also specify a subnet within that VPC.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_persistence(self) -> typing.Optional[builtins.bool]:
        '''Whether to use persistence for the machine.

        This is an optional property, and if not specified, it defaults to false.
        If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        '''
        result = self._values.get("use_persistence")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Virtual Private Cloud (VPC) ID where the machine will be deployed.

        This is an optional property, and if not specified, the default VPC will be used.
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_user_data(self) -> typing.Optional[builtins.str]:
        '''Allows the user to pass custom user data for the machine.

        This is an optional property; if specified, it will override any default user data that would be generated.
        You are usually okay with not passing this property, unless you have really specific requirements for the machine's initialization and want fine-grained
        control over the user data script.
        '''
        result = self._values.get("custom_user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ingress_rules(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]]:
        result = self._values.get("security_group_ingress_rules")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomAWSMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.CustomDockerMachineComponentProps",
    jsii_struct_bases=[BasicDockerMachineComponentProps],
    name_mapping={
        "networks": "networks",
        "use_volume": "useVolume",
        "volumes": "volumes",
        "expose_rdp": "exposeRDP",
        "expose_ssh": "exposeSSH",
        "expose_vnc": "exposeVNC",
        "external_rdp_port": "externalRDPPort",
        "external_ssh_port": "externalSSHPort",
        "external_vnc_port": "externalVNCPort",
        "ports": "ports",
    },
)
class CustomDockerMachineComponentProps(BasicDockerMachineComponentProps):
    def __init__(
        self,
        *,
        networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_volume: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        expose_rdp: typing.Optional[builtins.bool] = None,
        expose_ssh: typing.Optional[builtins.bool] = None,
        expose_vnc: typing.Optional[builtins.bool] = None,
        external_rdp_port: typing.Optional[jsii.Number] = None,
        external_ssh_port: typing.Optional[jsii.Number] = None,
        external_vnc_port: typing.Optional[jsii.Number] = None,
        ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param networks: Networks for the Docker container. This is an advanced property that allows you to specify multiple networks for the container. Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        :param use_volume: Whether you want to use a volume for the container or not; if not specified, it defaults to false. If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        :param volumes: List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema. Each volume must have a mandatory ``containerPath`` If ``useVolume`` is true, this property's value will be used to define the volumes for the container. If not specified, internally a default volume will be created.
        :param expose_rdp: Enables remote desktop access via RDP (default internal & external port is 3389).
        :param expose_ssh: Whether to expose SSH access to the container (defaults to false if not included). If true, you can optionally specify ``externalSSHPort`` (default internal port is 22, external port is 2222).
        :param expose_vnc: Enables remote desktop access via VNC (default internal & external port is 5900).
        :param external_rdp_port: External port to use for RDP, if ``exposeRDP`` is true.
        :param external_ssh_port: External port to map to container's SSH port (22). If not set, port 2222 will try to be assigned
        :param external_vnc_port: External port to use for VNC, if ``exposeVNC`` is true, unless overriden in ``ports``.
        :param ports: List of ports to expose from the container, following Docker's ContainerPorts schema. Each port must have an internal value, external is optional (if not present, Docker will choose a random port). These ports will take precedence over any other port configured, so in case a port is defined in externalSSHPort, externalVNCPort or externalRDPPort and explicitly set again in this ports property, this second value is the one that will get added to the container
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee038677aa7af54bb41889f21c36c3a8c903aecaed9b3b1c4a1ffce4b2881094)
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument use_volume", value=use_volume, expected_type=type_hints["use_volume"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument expose_rdp", value=expose_rdp, expected_type=type_hints["expose_rdp"])
            check_type(argname="argument expose_ssh", value=expose_ssh, expected_type=type_hints["expose_ssh"])
            check_type(argname="argument expose_vnc", value=expose_vnc, expected_type=type_hints["expose_vnc"])
            check_type(argname="argument external_rdp_port", value=external_rdp_port, expected_type=type_hints["external_rdp_port"])
            check_type(argname="argument external_ssh_port", value=external_ssh_port, expected_type=type_hints["external_ssh_port"])
            check_type(argname="argument external_vnc_port", value=external_vnc_port, expected_type=type_hints["external_vnc_port"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if networks is not None:
            self._values["networks"] = networks
        if use_volume is not None:
            self._values["use_volume"] = use_volume
        if volumes is not None:
            self._values["volumes"] = volumes
        if expose_rdp is not None:
            self._values["expose_rdp"] = expose_rdp
        if expose_ssh is not None:
            self._values["expose_ssh"] = expose_ssh
        if expose_vnc is not None:
            self._values["expose_vnc"] = expose_vnc
        if external_rdp_port is not None:
            self._values["external_rdp_port"] = external_rdp_port
        if external_ssh_port is not None:
            self._values["external_ssh_port"] = external_ssh_port
        if external_vnc_port is not None:
            self._values["external_vnc_port"] = external_vnc_port
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]]:
        '''Networks for the Docker container.

        This is an advanced property that allows you to specify multiple networks for the container.
        Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]], result)

    @builtins.property
    def use_volume(self) -> typing.Optional[builtins.bool]:
        '''Whether you want to use a volume for the container or not;

        if not specified, it defaults to false.
        If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        '''
        result = self._values.get("use_volume")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]]:
        '''List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema.

        Each volume must have a mandatory ``containerPath``
        If ``useVolume`` is true, this property's value will be used to define the volumes for the container.
        If not specified, internally a default volume will be created.
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]], result)

    @builtins.property
    def expose_rdp(self) -> typing.Optional[builtins.bool]:
        '''Enables remote desktop access via RDP (default internal & external port is 3389).'''
        result = self._values.get("expose_rdp")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expose_ssh(self) -> typing.Optional[builtins.bool]:
        '''Whether to expose SSH access to the container (defaults to false if not included).

        If true, you can optionally specify ``externalSSHPort`` (default internal port is 22, external port is 2222).
        '''
        result = self._values.get("expose_ssh")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expose_vnc(self) -> typing.Optional[builtins.bool]:
        '''Enables remote desktop access via VNC (default internal & external port is 5900).'''
        result = self._values.get("expose_vnc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def external_rdp_port(self) -> typing.Optional[jsii.Number]:
        '''External port to use for RDP, if ``exposeRDP`` is true.'''
        result = self._values.get("external_rdp_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_ssh_port(self) -> typing.Optional[jsii.Number]:
        '''External port to map to container's SSH port (22).

        If not set, port 2222 will try to be assigned
        '''
        result = self._values.get("external_ssh_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_vnc_port(self) -> typing.Optional[jsii.Number]:
        '''External port to use for VNC, if ``exposeVNC`` is true, unless overriden in ``ports``.'''
        result = self._values.get("external_vnc_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]]:
        '''List of ports to expose from the container, following Docker's ContainerPorts schema.

        Each port must have an internal value, external is optional (if not present, Docker will choose a random port).
        These ports will take precedence over any other port configured, so in case a port is defined in externalSSHPort,
        externalVNCPort or externalRDPPort and explicitly set again in this ports property, this second value is the one
        that will get added to the container
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDockerMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.CustomMachineComponentPropsInterface",
    jsii_struct_bases=[BaseInfrastructureComponentProps],
    name_mapping={
        "provider_type": "providerType",
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
    },
)
class CustomMachineComponentPropsInterface(BaseInfrastructureComponentProps):
    def __init__(
        self,
        *,
        provider_type: "ProviderType",
        aws_props: typing.Optional[typing.Union[CustomAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[CustomDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param aws_props: 
        :param docker_props: 
        '''
        if isinstance(aws_props, dict):
            aws_props = CustomAWSMachineComponentProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = CustomDockerMachineComponentProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4808c88d1e8ec8a3012318a609934006dcb0e556333dcc48e16dcb99d3a062eb)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
        }
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props

    @builtins.property
    def provider_type(self) -> "ProviderType":
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("ProviderType", result)

    @builtins.property
    def aws_props(self) -> typing.Optional[CustomAWSMachineComponentProps]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional[CustomAWSMachineComponentProps], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[CustomDockerMachineComponentProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[CustomDockerMachineComponentProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomMachineComponentPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DebianBasic(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.DebianBasic",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "DebianVersion",
        machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8fff4725a9531cbe5ba90a833a827a492919dc2b94a5f1f50a3de82d53b33e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: "ProviderType",
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69745c6888fde783f2a0e5eb2a675c0d625f8b4803e917e1740247f96f52f0b)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="createdDebianMachine")
    def _created_debian_machine(
        self,
    ) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdDebianMachine"))

    @_created_debian_machine.setter
    def _created_debian_machine(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae3e48f35b030c95ce243920649f0c48b15a5d51c555dd98557e85d9af31529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdDebianMachine", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="cdktf-infra-uniovi.DebianVersion")
class DebianVersion(enum.Enum):
    LATEST = "LATEST"
    DEBIAN_12 = "DEBIAN_12"
    DEBIAN_11 = "DEBIAN_11"


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.DockerLampStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "apache_port": "apachePort",
        "my_sql_port": "mySqlPort",
        "php_my_admin_port": "phpMyAdminPort",
    },
)
class DockerLampStackProps:
    def __init__(
        self,
        *,
        apache_port: typing.Optional[jsii.Number] = None,
        my_sql_port: typing.Optional[jsii.Number] = None,
        php_my_admin_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param apache_port: 
        :param my_sql_port: 
        :param php_my_admin_port: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bab3cd38ab08ed1da9dd85b29f394a497a1f64d77bf4987b4bfbff09094c3ac)
            check_type(argname="argument apache_port", value=apache_port, expected_type=type_hints["apache_port"])
            check_type(argname="argument my_sql_port", value=my_sql_port, expected_type=type_hints["my_sql_port"])
            check_type(argname="argument php_my_admin_port", value=php_my_admin_port, expected_type=type_hints["php_my_admin_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apache_port is not None:
            self._values["apache_port"] = apache_port
        if my_sql_port is not None:
            self._values["my_sql_port"] = my_sql_port
        if php_my_admin_port is not None:
            self._values["php_my_admin_port"] = php_my_admin_port

    @builtins.property
    def apache_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("apache_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def my_sql_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("my_sql_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def php_my_admin_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("php_my_admin_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerLampStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.DockerLempStackProps",
    jsii_struct_bases=[],
    name_mapping={"my_sql_port": "mySqlPort", "nginx_port": "nginxPort"},
)
class DockerLempStackProps:
    def __init__(
        self,
        *,
        my_sql_port: typing.Optional[jsii.Number] = None,
        nginx_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param my_sql_port: 
        :param nginx_port: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f747830eb36daee7cd0e8c3142251d4aa4a36192eb684f4a9fd36cd43d7696)
            check_type(argname="argument my_sql_port", value=my_sql_port, expected_type=type_hints["my_sql_port"])
            check_type(argname="argument nginx_port", value=nginx_port, expected_type=type_hints["nginx_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if my_sql_port is not None:
            self._values["my_sql_port"] = my_sql_port
        if nginx_port is not None:
            self._values["nginx_port"] = nginx_port

    @builtins.property
    def my_sql_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("my_sql_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nginx_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("nginx_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerLempStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.DockerServerProps",
    jsii_struct_bases=[BasicDockerMachineComponentProps],
    name_mapping={
        "networks": "networks",
        "use_volume": "useVolume",
        "volumes": "volumes",
        "ports": "ports",
    },
)
class DockerServerProps(BasicDockerMachineComponentProps):
    def __init__(
        self,
        *,
        networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_volume: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param networks: Networks for the Docker container. This is an advanced property that allows you to specify multiple networks for the container. Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        :param use_volume: Whether you want to use a volume for the container or not; if not specified, it defaults to false. If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        :param volumes: List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema. Each volume must have a mandatory ``containerPath`` If ``useVolume`` is true, this property's value will be used to define the volumes for the container. If not specified, internally a default volume will be created.
        :param ports: An optional list of ports to expose from the container, following Docker's ``ContainerPorts`` schema. Each port must have an internal value, external is optional (if not present, Docker will choose a random port).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e38d0dbe099a9768f7239c0773c380ee979046b507fa00b696d9c821b421ef)
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument use_volume", value=use_volume, expected_type=type_hints["use_volume"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if networks is not None:
            self._values["networks"] = networks
        if use_volume is not None:
            self._values["use_volume"] = use_volume
        if volumes is not None:
            self._values["volumes"] = volumes
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]]:
        '''Networks for the Docker container.

        This is an advanced property that allows you to specify multiple networks for the container.
        Each network must follow Docker's ``ContainerNetworksAdvanced`` schema.
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced]], result)

    @builtins.property
    def use_volume(self) -> typing.Optional[builtins.bool]:
        '''Whether you want to use a volume for the container or not;

        if not specified, it defaults to false.
        If set to true, you can optionally specify ``volumes`` to define the volumes to use.
        '''
        result = self._values.get("use_volume")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]]:
        '''List of volumes to use for the container, following Docker's ``ContainerVolumes`` schema.

        Each volume must have a mandatory ``containerPath``
        If ``useVolume`` is true, this property's value will be used to define the volumes for the container.
        If not specified, internally a default volume will be created.
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes]], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]]:
        '''An optional list of ports to expose from the container, following Docker's ``ContainerPorts`` schema.

        Each port must have an internal value, external is optional (if not present, Docker will choose a random port).
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HardenedApacheServer(
    ApacheServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.HardenedApacheServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: ApacheVersion,
        server_props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d728d3b23b650af7747c1596f058c9ad6298312523c2ae8c8670f0d087151836)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: "IDeployStrategy",
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b597728661842fa87b5f42a12c1afbbe2ef8198aec2c987dab9c0152502c917f)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395a3fb982c69ec9593f03aa97b81a73a6d6df8f360e0368de10de404faadad3)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327206b80fd862bb959d3d21a5aa0f767a9aa8e6c5c18bf89e75e0aeba658138)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedApacheImagesMap")
    def _supported_apache_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedApacheImagesMap"))


@jsii.interface(jsii_type="cdktf-infra-uniovi.IDeployStrategy")
class IDeployStrategy(typing_extensions.Protocol):
    @jsii.member(jsii_name="deployBasicMachine")
    def deploy_basic_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        ...

    @jsii.member(jsii_name="deployBasicServer")
    def deploy_basic_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        ...

    @jsii.member(jsii_name="deployCustomMachine")
    def deploy_custom_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        ...

    @jsii.member(jsii_name="deployHardenedServer")
    def deploy_hardened_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        ...

    @jsii.member(jsii_name="deployInsecureServer")
    def deploy_insecure_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        ...

    @jsii.member(jsii_name="deployWebStack")
    def deploy_web_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stack_type: "StackType",
        *,
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stack_type: -
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        ...


class _IDeployStrategyProxy:
    __jsii_type__: typing.ClassVar[str] = "cdktf-infra-uniovi.IDeployStrategy"

    @jsii.member(jsii_name="deployBasicMachine")
    def deploy_basic_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889b2c0b9e2cfb286cdb5c78a4692ba25a70c9d8f374856ff29d74ddbc557f9f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicMachine", [scope, id, props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployBasicServer")
    def deploy_basic_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9459499ef26471a73827589507bc1f457b23a14664edc8cb331b2a8b029976bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicServer", [scope, id, props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployCustomMachine")
    def deploy_custom_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32adc70207f1d2f865c7ee5e3be5fbe26098aef1f83cb5e910a5e47e92e444b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployCustomMachine", [scope, id, props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployHardenedServer")
    def deploy_hardened_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a02e7392467234db22ee01df8595c5be808d50c5d011c9df600a686ab3a947)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployHardenedServer", [scope, id, props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployInsecureServer")
    def deploy_insecure_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union["InternalAWSMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union["InternalDockerMachineComponentProps", typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d166d5d086a1f423ede45830d6dcf2f23708cb5bb1ecbd4427dbfcf2b928353f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployInsecureServer", [scope, id, props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployWebStack")
    def deploy_web_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stack_type: "StackType",
        *,
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stack_type: -
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16835735b7ab044be3c3b6c7057fb70d0a2269ca8dbafc31d1ae5f93b0c74cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        props = BaseWebStackProps(
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deployWebStack", [scope, id, stack_type, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeployStrategy).__jsii_proxy_class__ = lambda : _IDeployStrategyProxy


class InsecureApacheServer(
    ApacheServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.InsecureApacheServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: ApacheVersion,
        server_props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319da680f78f1987973a782ebcd43888580287cbd5e2856aca5fce355490e00e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275509706f5a851f5847fe77008769f10760f3cc034511e2de8a55901536f9b6)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5919c25cd1aee440ce574deb64f9bc1554d20e17c1d3c94e5204dcb3ee5f3fd)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> "InternalMachineComponentPropsInterface":
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbe6c041cbbd254bf301b115fe57db3aad13bc90b182f55b0f4e87ba2c63126)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast("InternalMachineComponentPropsInterface", jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedApacheImagesMap")
    def _supported_apache_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedApacheImagesMap"))


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.InternalAWSMachineComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami": "ami",
        "additional_security_group_ingress_rules": "additionalSecurityGroupIngressRules",
        "custom_init_script_path": "customInitScriptPath",
    },
)
class InternalAWSMachineComponentProps:
    def __init__(
        self,
        *,
        ami: builtins.str,
        additional_security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_init_script_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ami: The Amazon Machine Image (AMI) ID to use for the machine. This is a mandatory property and must be one of the supported AMIs; however, its value should come from picking the corresponding AMI from the supported images list, by choosing the appropriate combination of provider type and image version.
        :param additional_security_group_ingress_rules: 
        :param custom_init_script_path: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714ef897a68d6f74d414742128a8107dbb21ca1ab4bd337b137b581c51ac3d28)
            check_type(argname="argument ami", value=ami, expected_type=type_hints["ami"])
            check_type(argname="argument additional_security_group_ingress_rules", value=additional_security_group_ingress_rules, expected_type=type_hints["additional_security_group_ingress_rules"])
            check_type(argname="argument custom_init_script_path", value=custom_init_script_path, expected_type=type_hints["custom_init_script_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ami": ami,
        }
        if additional_security_group_ingress_rules is not None:
            self._values["additional_security_group_ingress_rules"] = additional_security_group_ingress_rules
        if custom_init_script_path is not None:
            self._values["custom_init_script_path"] = custom_init_script_path

    @builtins.property
    def ami(self) -> builtins.str:
        '''The Amazon Machine Image (AMI) ID to use for the machine.

        This is a mandatory property and must be one of the supported AMIs; however, its value should come from picking the corresponding
        AMI from the supported images list, by choosing the appropriate combination of provider type and image version.
        '''
        result = self._values.get("ami")
        assert result is not None, "Required property 'ami' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_security_group_ingress_rules(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]]:
        result = self._values.get("additional_security_group_ingress_rules")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]], result)

    @builtins.property
    def custom_init_script_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("custom_init_script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalAWSMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.InternalDockerMachineComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "additional_ports": "additionalPorts",
        "build_args": "buildArgs",
        "custom_command": "customCommand",
        "custom_image_name": "customImageName",
        "dockerfile_path": "dockerfilePath",
        "volume_container_path": "volumeContainerPath",
    },
)
class InternalDockerMachineComponentProps:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        additional_ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        custom_command: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_image_name: typing.Optional[builtins.str] = None,
        dockerfile_path: typing.Optional[builtins.str] = None,
        volume_container_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: The name of the Docker image to use for the machine. This is a mandatory property and must be one of the supported Docker images; however, it's value should come from picking the corresponding image from the supported images list, by choosing the appropriate combination of provider type and image version. It is used to ensure that the machine is created with a specific image, instead of allowing the user to pass any arbitrary image name that may not exist or be supported.
        :param additional_ports: We may need to pass specific ports for certain use cases in case the user doesn't pass them. We cannot rely on the user to pass them, and we shouldn't overflow the user-facing interfaces with too many fields when some are "mandatory" but only for specific machines
        :param build_args: 
        :param custom_command: 
        :param custom_image_name: 
        :param dockerfile_path: A custom Dockerfile path to build the image from, in case we need to build a custom image. This is an optional property, and if not specified, no specific Dockerfile will be used. However, you should be careful not to pass a ``customImageName`` in those cases.
        :param volume_container_path: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015cf9cbcbee88765f5fe6bcfb61efd2907315ffc98f41eb63d6bb2149eaeb06)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument additional_ports", value=additional_ports, expected_type=type_hints["additional_ports"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument custom_command", value=custom_command, expected_type=type_hints["custom_command"])
            check_type(argname="argument custom_image_name", value=custom_image_name, expected_type=type_hints["custom_image_name"])
            check_type(argname="argument dockerfile_path", value=dockerfile_path, expected_type=type_hints["dockerfile_path"])
            check_type(argname="argument volume_container_path", value=volume_container_path, expected_type=type_hints["volume_container_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
        }
        if additional_ports is not None:
            self._values["additional_ports"] = additional_ports
        if build_args is not None:
            self._values["build_args"] = build_args
        if custom_command is not None:
            self._values["custom_command"] = custom_command
        if custom_image_name is not None:
            self._values["custom_image_name"] = custom_image_name
        if dockerfile_path is not None:
            self._values["dockerfile_path"] = dockerfile_path
        if volume_container_path is not None:
            self._values["volume_container_path"] = volume_container_path

    @builtins.property
    def image_name(self) -> builtins.str:
        '''The name of the Docker image to use for the machine.

        This is a mandatory property and must be one of the supported Docker images; however, it's value should come from picking the corresponding
        image from the supported images list, by choosing the appropriate combination of provider type and image version.
        It is used to ensure that the machine is created with a specific image, instead of allowing the user to pass any arbitrary image name that may not
        exist or be supported.

        Example::

            "ubuntu:latest"
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_ports(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]]:
        '''We may need to pass specific ports for certain use cases in case the user doesn't pass them.

        We cannot rely on the user to pass them, and we shouldn't overflow the user-facing interfaces with too
        many fields when some are "mandatory" but only for specific machines
        '''
        result = self._values.get("additional_ports")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts]], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def custom_command(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("custom_command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_image_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("custom_image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dockerfile_path(self) -> typing.Optional[builtins.str]:
        '''A custom Dockerfile path to build the image from, in case we need to build a custom image.

        This is an optional property, and if not specified, no specific Dockerfile will be used. However, you should be careful not to pass a ``customImageName`` in those cases.
        '''
        result = self._values.get("dockerfile_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_container_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("volume_container_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalDockerMachineComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.InternalMachineComponentPropsInterface",
    jsii_struct_bases=[],
    name_mapping={
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
        "ubuntu_pro_token": "ubuntuProToken",
    },
)
class InternalMachineComponentPropsInterface:
    def __init__(
        self,
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if isinstance(aws_props, dict):
            aws_props = InternalAWSMachineComponentProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = InternalDockerMachineComponentProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835395862fa576af5bb917b2fc6118b4bf24a3d2bcec9fa48acaf6b8f7815b07)
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
            check_type(argname="argument ubuntu_pro_token", value=ubuntu_pro_token, expected_type=type_hints["ubuntu_pro_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props
        if ubuntu_pro_token is not None:
            self._values["ubuntu_pro_token"] = ubuntu_pro_token

    @builtins.property
    def aws_props(self) -> typing.Optional[InternalAWSMachineComponentProps]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional[InternalAWSMachineComponentProps], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[InternalDockerMachineComponentProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[InternalDockerMachineComponentProps], result)

    @builtins.property
    def ubuntu_pro_token(self) -> typing.Optional[builtins.str]:
        '''Ubuntu Pro subscription token used to attach the instance.'''
        result = self._values.get("ubuntu_pro_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalMachineComponentPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LampBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf-infra-uniovi.LampBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de5c0c54c2315787d46bc1aea61e48f257987ea22ae91838c511a4b298be031)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        stack_props = LampStackPropsInterface(
            include_php_my_admin=include_php_my_admin,
            aws_props=aws_props,
            docker_props=docker_props,
            php_my_admin_version=php_my_admin_version,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        jsii.create(self.__class__, self, [scope, id, stack_props])

    @jsii.member(jsii_name="deploy")
    @abc.abstractmethod
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        ...


class _LampBaseProxy(LampBase):
    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507633b94040c0417258d57320505bc2a21b2ac2b9b926d45c1213829d391189)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        stack_props = LampStackPropsInterface(
            include_php_my_admin=include_php_my_admin,
            aws_props=aws_props,
            docker_props=docker_props,
            php_my_admin_version=php_my_admin_version,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deploy", [strategy, id, stack_type, stack_props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LampBase).__jsii_proxy_class__ = lambda : _LampBaseProxy


class LampStack(
    LampBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.LampStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b7f54e01aba634ed622dbbfc09529f898468c8fbfc389e69500de22dc27a77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        stack_props = LampStackPropsInterface(
            include_php_my_admin=include_php_my_admin,
            aws_props=aws_props,
            docker_props=docker_props,
            php_my_admin_version=php_my_admin_version,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        jsii.create(self.__class__, self, [scope, id, stack_props])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d7b2445ea5a2780fed8d0235eba300bb73f08ea63ac32678b2110f1351244c)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        stack_props = LampStackPropsInterface(
            include_php_my_admin=include_php_my_admin,
            aws_props=aws_props,
            docker_props=docker_props,
            php_my_admin_version=php_my_admin_version,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deploy", [strategy, id, stack_type, stack_props]))


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.LampStackPropsInterface",
    jsii_struct_bases=[BaseInfrastructureComponentProps, BaseWebStackProps],
    name_mapping={
        "provider_type": "providerType",
        "my_sql_database": "mySqlDatabase",
        "my_sql_password": "mySqlPassword",
        "my_sql_root_password": "mySqlRootPassword",
        "my_sql_user": "mySqlUser",
        "my_sql_version": "mySqlVersion",
        "include_php_my_admin": "includePhpMyAdmin",
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
        "php_my_admin_version": "phpMyAdminVersion",
        "php_version": "phpVersion",
    },
)
class LampStackPropsInterface(BaseInfrastructureComponentProps, BaseWebStackProps):
    def __init__(
        self,
        *,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
        include_php_my_admin: builtins.bool,
        aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_my_admin_version: typing.Optional["PhpMyAdminVersion"] = None,
        php_version: typing.Optional[ApachePhpVersion] = None,
    ) -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        :param include_php_my_admin: 
        :param aws_props: 
        :param docker_props: 
        :param php_my_admin_version: 
        :param php_version: The version of PHP to use in the LAMP stack. This property is optional and can be omitted if the default version is acceptable. If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        '''
        if isinstance(aws_props, dict):
            aws_props = AWSLampStackProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = DockerLampStackProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c00a24e3e3f48fdc1b1828556a3a5e104b2bcf54744cf6fe676c6ca500482d)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument my_sql_database", value=my_sql_database, expected_type=type_hints["my_sql_database"])
            check_type(argname="argument my_sql_password", value=my_sql_password, expected_type=type_hints["my_sql_password"])
            check_type(argname="argument my_sql_root_password", value=my_sql_root_password, expected_type=type_hints["my_sql_root_password"])
            check_type(argname="argument my_sql_user", value=my_sql_user, expected_type=type_hints["my_sql_user"])
            check_type(argname="argument my_sql_version", value=my_sql_version, expected_type=type_hints["my_sql_version"])
            check_type(argname="argument include_php_my_admin", value=include_php_my_admin, expected_type=type_hints["include_php_my_admin"])
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
            check_type(argname="argument php_my_admin_version", value=php_my_admin_version, expected_type=type_hints["php_my_admin_version"])
            check_type(argname="argument php_version", value=php_version, expected_type=type_hints["php_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
            "include_php_my_admin": include_php_my_admin,
        }
        if my_sql_database is not None:
            self._values["my_sql_database"] = my_sql_database
        if my_sql_password is not None:
            self._values["my_sql_password"] = my_sql_password
        if my_sql_root_password is not None:
            self._values["my_sql_root_password"] = my_sql_root_password
        if my_sql_user is not None:
            self._values["my_sql_user"] = my_sql_user
        if my_sql_version is not None:
            self._values["my_sql_version"] = my_sql_version
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props
        if php_my_admin_version is not None:
            self._values["php_my_admin_version"] = php_my_admin_version
        if php_version is not None:
            self._values["php_version"] = php_version

    @builtins.property
    def provider_type(self) -> "ProviderType":
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("ProviderType", result)

    @builtins.property
    def my_sql_database(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_root_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_user(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_version(self) -> typing.Optional["MySQLVersion"]:
        '''The type of stack being deployed.

        This property is used to determine the specific stack configuration and behavior.
        It is a mandatory property and must be one of the supported stack types.

        Example::

            StackType.LAMP
        '''
        result = self._values.get("my_sql_version")
        return typing.cast(typing.Optional["MySQLVersion"], result)

    @builtins.property
    def include_php_my_admin(self) -> builtins.bool:
        result = self._values.get("include_php_my_admin")
        assert result is not None, "Required property 'include_php_my_admin' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def aws_props(self) -> typing.Optional[AWSLampStackProps]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional[AWSLampStackProps], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[DockerLampStackProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[DockerLampStackProps], result)

    @builtins.property
    def php_my_admin_version(self) -> typing.Optional["PhpMyAdminVersion"]:
        result = self._values.get("php_my_admin_version")
        return typing.cast(typing.Optional["PhpMyAdminVersion"], result)

    @builtins.property
    def php_version(self) -> typing.Optional[ApachePhpVersion]:
        '''The version of PHP to use in the LAMP stack.

        This property is optional and can be omitted if the default version is acceptable.
        If specified, it is mandatory to use a supported version from the ``ApachePhpVersion`` enum.
        '''
        result = self._values.get("php_version")
        return typing.cast(typing.Optional[ApachePhpVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LampStackPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LempBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf-infra-uniovi.LempBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef47cdd9b9729164452374528b41aef7b178b2a176466dc2a67b1fefa493dae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        stack_props = LempStackPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        jsii.create(self.__class__, self, [scope, id, stack_props])

    @jsii.member(jsii_name="deploy")
    @abc.abstractmethod
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        ...


class _LempBaseProxy(LempBase):
    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5721c9f1ab3eabd5ee92c0f3eb63542cc4e53ea319b3eafda31e96d6ac20ea94)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        stack_props = LempStackPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deploy", [strategy, id, stack_type, stack_props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LempBase).__jsii_proxy_class__ = lambda : _LempBaseProxy


class LempStack(
    LempBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.LempStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6e65cbf150499c5de69757d7dae7833c70fe77878a36965f42e68a21e940ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        stack_props = LempStackPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        jsii.create(self.__class__, self, [scope, id, stack_props])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        stack_type: "StackType",
        *,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
    ) -> None:
        '''
        :param strategy: -
        :param id: -
        :param stack_type: -
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea52fd1abd6c632502d418e37c7e5e24dd2b1358d2074d02f43e950417dc436)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        stack_props = LempStackPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            php_version=php_version,
            provider_type=provider_type,
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deploy", [strategy, id, stack_type, stack_props]))


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.LempStackPropsInterface",
    jsii_struct_bases=[BaseInfrastructureComponentProps, BaseWebStackProps],
    name_mapping={
        "provider_type": "providerType",
        "my_sql_database": "mySqlDatabase",
        "my_sql_password": "mySqlPassword",
        "my_sql_root_password": "mySqlRootPassword",
        "my_sql_user": "mySqlUser",
        "my_sql_version": "mySqlVersion",
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
        "php_version": "phpVersion",
    },
)
class LempStackPropsInterface(BaseInfrastructureComponentProps, BaseWebStackProps):
    def __init__(
        self,
        *,
        provider_type: "ProviderType",
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional["MySQLVersion"] = None,
        aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
        php_version: typing.Optional["NginxPhpVersion"] = None,
    ) -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.
        :param aws_props: 
        :param docker_props: 
        :param php_version: 
        '''
        if isinstance(aws_props, dict):
            aws_props = AWSLempStackProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = DockerLempStackProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947b4c93dad362e677d5374d8b920798e538d954b19907e686d5a693b13c3ec6)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument my_sql_database", value=my_sql_database, expected_type=type_hints["my_sql_database"])
            check_type(argname="argument my_sql_password", value=my_sql_password, expected_type=type_hints["my_sql_password"])
            check_type(argname="argument my_sql_root_password", value=my_sql_root_password, expected_type=type_hints["my_sql_root_password"])
            check_type(argname="argument my_sql_user", value=my_sql_user, expected_type=type_hints["my_sql_user"])
            check_type(argname="argument my_sql_version", value=my_sql_version, expected_type=type_hints["my_sql_version"])
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
            check_type(argname="argument php_version", value=php_version, expected_type=type_hints["php_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
        }
        if my_sql_database is not None:
            self._values["my_sql_database"] = my_sql_database
        if my_sql_password is not None:
            self._values["my_sql_password"] = my_sql_password
        if my_sql_root_password is not None:
            self._values["my_sql_root_password"] = my_sql_root_password
        if my_sql_user is not None:
            self._values["my_sql_user"] = my_sql_user
        if my_sql_version is not None:
            self._values["my_sql_version"] = my_sql_version
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props
        if php_version is not None:
            self._values["php_version"] = php_version

    @builtins.property
    def provider_type(self) -> "ProviderType":
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast("ProviderType", result)

    @builtins.property
    def my_sql_database(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_root_password(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_user(self) -> typing.Optional[builtins.str]:
        result = self._values.get("my_sql_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def my_sql_version(self) -> typing.Optional["MySQLVersion"]:
        '''The type of stack being deployed.

        This property is used to determine the specific stack configuration and behavior.
        It is a mandatory property and must be one of the supported stack types.

        Example::

            StackType.LAMP
        '''
        result = self._values.get("my_sql_version")
        return typing.cast(typing.Optional["MySQLVersion"], result)

    @builtins.property
    def aws_props(self) -> typing.Optional[AWSLempStackProps]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional[AWSLempStackProps], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[DockerLempStackProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[DockerLempStackProps], result)

    @builtins.property
    def php_version(self) -> typing.Optional["NginxPhpVersion"]:
        result = self._values.get("php_version")
        return typing.cast(typing.Optional["NginxPhpVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LempStackPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdktf-infra-uniovi.MySQLVersion")
class MySQLVersion(enum.Enum):
    LATEST = "LATEST"
    LTS = "LTS"
    MYSQL_9_3 = "MYSQL_9_3"
    MYSQL_8_4 = "MYSQL_8_4"


@jsii.enum(jsii_type="cdktf-infra-uniovi.NginxPhpVersion")
class NginxPhpVersion(enum.Enum):
    PHP_NGINX_8_2 = "PHP_NGINX_8_2"


class NginxServerBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf-infra-uniovi.NginxServerBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "NginxVersion",
        server_props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59d9a908833100222d2377a2e27a8ae09d09399908be22914ec0b7037df7e5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    @abc.abstractmethod
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: "ProviderType",
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b8b7f49d14a0e66e1f5337dd3177563267ee4cfe7f9d5bb9458ff297e38800)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    @abc.abstractmethod
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getDockerProps")
    @abc.abstractmethod
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="supportedNginxImagesMap")
    @abc.abstractmethod
    def _supported_nginx_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="createdNginxServer")
    def _created_nginx_server(self) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdNginxServer"))

    @_created_nginx_server.setter
    def _created_nginx_server(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f4c22a95b5ad65da4577021b8a62753fd36ef0bb9592771499d8c0b0905fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdNginxServer", value) # pyright: ignore[reportArgumentType]


class _NginxServerBaseProxy(NginxServerBase):
    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union["ServerPropsInterface", typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c510fa95b5603372bdc810e257045d70bed453c10724571704b3c53b6e333667)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fa848ce215cc43df526e0d8e3bc4ce84241e900fa6ca98ef14e2bd430925b4)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0548c9484d04d3aaae47827a5e7633be9aba36cd5ab36051903872fb5a6208)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedNginxImagesMap")
    def _supported_nginx_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedNginxImagesMap"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NginxServerBase).__jsii_proxy_class__ = lambda : _NginxServerBaseProxy


@jsii.enum(jsii_type="cdktf-infra-uniovi.NginxVersion")
class NginxVersion(enum.Enum):
    LATEST = "LATEST"


@jsii.enum(jsii_type="cdktf-infra-uniovi.PhpMyAdminVersion")
class PhpMyAdminVersion(enum.Enum):
    LATEST = "LATEST"


class ProviderDeployStrategyFactory(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.ProviderDeployStrategyFactory",
):
    @jsii.member(jsii_name="getProviderDeployStrategy")
    @builtins.classmethod
    def get_provider_deploy_strategy(
        cls,
        provider_type: "ProviderType",
    ) -> IDeployStrategy:
        '''
        :param provider_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2080356753be8befde69a2f8e8ec78e1a71e3ce7fddf270dc9d3aef3481326a)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
        return typing.cast(IDeployStrategy, jsii.sinvoke(cls, "getProviderDeployStrategy", [provider_type]))


@jsii.enum(jsii_type="cdktf-infra-uniovi.ProviderType")
class ProviderType(enum.Enum):
    DOCKER = "DOCKER"
    AWS = "AWS"


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.ServerPropsInterface",
    jsii_struct_bases=[BaseInfrastructureComponentProps],
    name_mapping={
        "provider_type": "providerType",
        "aws_props": "awsProps",
        "docker_props": "dockerProps",
    },
)
class ServerPropsInterface(BaseInfrastructureComponentProps):
    def __init__(
        self,
        *,
        provider_type: ProviderType,
        aws_props: typing.Optional[typing.Union["AwsServerProps", typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[DockerServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param provider_type: The provider type for the infrastructure component. This property is used to determine which cloud provider the component will be deployed on. It is a mandatory property and must be one of the supported provider types.
        :param aws_props: 
        :param docker_props: 
        '''
        if isinstance(aws_props, dict):
            aws_props = AwsServerProps(**aws_props)
        if isinstance(docker_props, dict):
            docker_props = DockerServerProps(**docker_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e18d8a93c32e6107de35c15d2595a8db35635394f96bc23d9ccbcd6da0930f)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument aws_props", value=aws_props, expected_type=type_hints["aws_props"])
            check_type(argname="argument docker_props", value=docker_props, expected_type=type_hints["docker_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_type": provider_type,
        }
        if aws_props is not None:
            self._values["aws_props"] = aws_props
        if docker_props is not None:
            self._values["docker_props"] = docker_props

    @builtins.property
    def provider_type(self) -> ProviderType:
        '''The provider type for the infrastructure component.

        This property is used to determine which cloud provider the component will be deployed on.
        It is a mandatory property and must be one of the supported provider types.

        Example::

            ProviderType.Docker
        '''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast(ProviderType, result)

    @builtins.property
    def aws_props(self) -> typing.Optional["AwsServerProps"]:
        result = self._values.get("aws_props")
        return typing.cast(typing.Optional["AwsServerProps"], result)

    @builtins.property
    def docker_props(self) -> typing.Optional[DockerServerProps]:
        result = self._values.get("docker_props")
        return typing.cast(typing.Optional[DockerServerProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerPropsInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SingletonProviderFactory(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.SingletonProviderFactory",
):
    @jsii.member(jsii_name="getProvider")
    @builtins.classmethod
    def get_provider(
        cls,
        provider_type: ProviderType,
        scope: _constructs_77d1e7e8.Construct,
        existing_provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.TerraformProvider:
        '''
        :param provider_type: -
        :param scope: -
        :param existing_provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11070dc128f531d20c08489c265205b236198116d9e9bbef274657ac5688775)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument existing_provider", value=existing_provider, expected_type=type_hints["existing_provider"])
        return typing.cast(_cdktf_9a9027ec.TerraformProvider, jsii.sinvoke(cls, "getProvider", [provider_type, scope, existing_provider]))


@jsii.enum(jsii_type="cdktf-infra-uniovi.StackType")
class StackType(enum.Enum):
    LAMP = "LAMP"
    LEMP = "LEMP"


class UbuntuBasic(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.UbuntuBasic",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0a16f71c1676817471c049e101bb6bfac39feb071711d4c48e937665834773)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd828c869b09b3569e16794d148ed6fa809b76c8b16128f66ea88a5e6ba8ec70)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: ProviderType,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1457d466794c7ed795f210c51f844db27be2097fce99221996937da4f7b5564d)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="createdUbuntuMachine")
    def _created_ubuntu_machine(
        self,
    ) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdUbuntuMachine"))

    @_created_ubuntu_machine.setter
    def _created_ubuntu_machine(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b4588982ea58d44c172e712846d318fd163e224386cfe30f189f14fc4dbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdUbuntuMachine", value) # pyright: ignore[reportArgumentType]


class UbuntuCustomBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf-infra-uniovi.UbuntuCustomBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d8aa3e2a7e296ae1cccbcb9e19714f85704e5a5563e5f73007fcd6db309ff1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    @abc.abstractmethod
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getAdditionalProps")
    def _get_additional_props(
        self,
        provider_type: ProviderType,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param provider_type: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d503eab41f04657723f0052bd99a733946ca0f70e47e7eceb5452c9d81da9c3c)
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAdditionalProps", [provider_type, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    @abc.abstractmethod
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        ...

    @jsii.member(jsii_name="getDockerProps")
    @abc.abstractmethod
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="createdUbuntuMachine")
    def _created_ubuntu_machine(
        self,
    ) -> typing.Optional[_constructs_77d1e7e8.Construct]:
        return typing.cast(typing.Optional[_constructs_77d1e7e8.Construct], jsii.get(self, "createdUbuntuMachine"))

    @_created_ubuntu_machine.setter
    def _created_ubuntu_machine(
        self,
        value: typing.Optional[_constructs_77d1e7e8.Construct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afce00d1252a3a98b78bc5db46da5af9a1c69c659b086f5782ce33a41325f23f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdUbuntuMachine", value) # pyright: ignore[reportArgumentType]


class _UbuntuCustomBaseProxy(UbuntuCustomBase):
    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a005d0708ba8d9d28b40ffbbfea5b77797c8744ff51390fdfb37ebe418cc54)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1aaed65460e5b3502d68087194ebd3dab02b58b27d47d8c9ce8689ff53138c7)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4516d2d2f557d001451c6489dbeaf6e8e12065af729e5155459c758d0c2fa850)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, UbuntuCustomBase).__jsii_proxy_class__ = lambda : _UbuntuCustomBaseProxy


class UbuntuDNS(
    UbuntuCustomBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.UbuntuDNS",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd110e4bb21886852e7a303f0550ce50e51fdb3227aaee26bcfababa7c2dbfb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bdef2a26c328ab84d91fcc04e8b102ab5bbc2659ae242de7720b22d6a974b7d)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad24b166cc97abca23ff3f2b0f7ac94e10d10add10f6ee21be0b88265b15b97)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77cb41ac667e13eba8683afaea4e0e23005246a5ccabae8cccf43b90799c990)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))


class UbuntuDesktop(
    UbuntuCustomBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.UbuntuDesktop",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331408f97be7677ee8e88b704b6de9216b87c51b5834b3925e79e7c2287c59c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35329d70f8191129073ec63c9946b53f8a67e06bcf054948cf1f7980cb012bf4)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3f22236e85c274c7f2ee22626189b770239f44f65ad6d2168b678d8aa7cec)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ef6edb5b2fbc752a12df16a0e315e74a6567b82d287302ad1f480a2723fcd4)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))


class UbuntuDev(
    UbuntuCustomBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.UbuntuDev",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948da948ea46ad497ce95b82af7af071050f16711f618b0703476cc2f38eeed1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651dd48fe714fc4d7fe8d279daf8f5e7e4e831e3778164234ca6ef91d46bfba8)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d0beb27dc67f1a9593ce0370284f73f35f3a141a3234ff8b180506413705fc)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5676dd1b0fb24e619bca0764cefa48953e77652590d997c0bb0cd598b4e97a01)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))


class UbuntuPro(
    UbuntuCustomBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.UbuntuPro",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: "UbuntuVersion",
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param machine_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691d976ab3bb6955afa4ca620f3e3cefd56d1f397fa9be4b778c81796284fe97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, machine_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param machine_props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf369f593c5e7ac1fdd5efdf7944e2a8f396c3038fe3e4ae2de6bd19445b8055)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_props", value=machine_props, expected_type=type_hints["machine_props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, machine_props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b67ca64ee90b24ad7c1d024685537ede3a67e3678122257509a5b691f6fa5a)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a03358cd2a888a28e1c4b8ff69892a941dfdfeca12e2b59b9e605b456082ac9)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="ubuntuProToken")
    def _ubuntu_pro_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ubuntuProToken"))

    @_ubuntu_pro_token.setter
    def _ubuntu_pro_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754a0841dcd127c3b3d95e7d75af64ab64e6455ae70d34813e60c8f70baab75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ubuntuProToken", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="cdktf-infra-uniovi.UbuntuVersion")
class UbuntuVersion(enum.Enum):
    LATEST = "LATEST"
    UBUNTU_18 = "UBUNTU_18"
    UBUNTU_20 = "UBUNTU_20"
    UBUNTU_22 = "UBUNTU_22"
    UBUNTU_24 = "UBUNTU_24"


class ApacheServer(
    ApacheServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.ApacheServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: ApacheVersion,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b880d3fd3a8eba683422ba87d6b4201851b2fe27b352c6f24afb34e58ce98d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee44ed9483053198ca680f25df91a47f2b12656bd477b3fb4a03c7b97b1c3420)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f6c82c52ca37cb2040529f14fd63be2ef16bfdad3f2a6f44bb561927371b62)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467f540c2bcc3f37b1cca514cb6a50fd878e2c73b717204d00b12985c18d500a)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedApacheImagesMap")
    def _supported_apache_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedApacheImagesMap"))


@jsii.implements(IDeployStrategy)
class AwsDeployStrategy(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.AwsDeployStrategy",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="deployBasicMachine")
    def deploy_basic_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        basic_machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a basic AWS machine deployment.

        This method deploys a basic AWS EC2 instance with optional EBS volume for persistence.
        It sets up the necessary VPC, subnet, security group, and instance properties.

        :param scope: The construct scope where the resources will be defined.
        :param id: The ID for the machine component, which will be normalized to ensure it is valid for AWS resources.
        :param basic_machine_props: An object containing the properties for the basic machine.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff819fdd70c14b81b199b4c4e6625db43cbb99dc64222e75ff4eab44d945573)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument basic_machine_props", value=basic_machine_props, expected_type=type_hints["basic_machine_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicMachine", [scope, id, basic_machine_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployBasicServer")
    def deploy_basic_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a basic AWS server using the provided properties.

        This method is used to deploy an AWS EC2 instance with basic server properties and optional EBS volume for persistence.
        This method is specifically designed for server deployments, which may include additional configurations such as ports and networks.
        By default, it will expose ports 80 and 443, but this can be customized through the serverProps.

        :param scope: The scope where the resources will be defined.
        :param id: The ID for the server component, which will be normalized to ensure it is valid for AWS resources.
        :param server_props: An object containing the properties for the server. At this point it should include AWS-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing instance that is the AWS server.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f16f369c3f55f8c3397b8c96b247658c3c03138ff7970eda0cfb2202134e009)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployCustomMachine")
    def deploy_custom_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        custom_machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a custom AWS machine using the provided properties.

        A custom machine is any machine that is slightly more complex than a basic machine, and that will require a custom init script for further personalization.
        This method deploys an AWS EC2 instance with custom properties and optional EBS volume for persistence.
        It sets up the necessary VPC, subnet, security group, and instance properties, if not provided.
        It also allows for custom user data to be provided, which can include additional setup scripts or configurations that will override the original script

        :param scope: The construct scope where the resources will be defined.
        :param id: The ID for the machine component, which will be normalized to ensure it is valid for AWS resources.
        :param custom_machine_props: An object containing the properties for the custom machine. At this point it should include AWS-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :throws: Error if internal AWS properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a1bab275f8f16873057a216ee85745694d109846297586d780793f22eae540)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument custom_machine_props", value=custom_machine_props, expected_type=type_hints["custom_machine_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployCustomMachine", [scope, id, custom_machine_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployHardenedServer")
    def deploy_hardened_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a hardened AWS server using the provided properties.

        This method is used to deploy an AWS EC2 instance with hardened server properties and optional EBS volume for persistence.
        This method is specifically designed for server deployments, which may include additional configurations such as ports and networks.
        By default, it will expose ports 22 (SSH), 80 (HTTP), and 443 (HTTPS), but this can be customized through the serverProps.

        :param scope: The scope where the resources will be defined.
        :param id: The ID for the server component, which will be normalized to ensure it is valid for AWS resources.
        :param server_props: An object containing the properties for the server. At this point it should include AWS-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing instance that is the AWS server.

        :throws: Error if internal AWS properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a01de8860acc93ac60bbb0dea3e01bb7182e57f497695c9f676d0231609117)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployHardenedServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployInsecureServer")
    def deploy_insecure_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates an insecure AWS server using the provided properties.

        This method is used to deploy an AWS EC2 instance with insecure server properties and optional EBS volume for persistence.
        This method is specifically designed for server deployments, which may include additional configurations such as ports and networks.
        By default, it will expose ports 22 (SSH) and 80 (HTTP), but this can be customized through the serverProps.

        :param scope: The scope where the resources will be defined.
        :param id: The ID for the server component, which will be normalized to ensure it is valid for AWS resources.
        :param server_props: An object containing the properties for the server. At this point it should include AWS-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing instance that is the AWS server.

        :throws: Error if internal AWS properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4666c86f2820e532bafee339cfbce32e1513095cd458cab1aae58d6954ab7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployInsecureServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployWebStack")
    def deploy_web_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stack_type: StackType,
        *,
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional[MySQLVersion] = None,
    ) -> None:
        '''Generates a basic web stack using the provided properties.

        This method is used to deploy a web stack using AWS, which can be either a LAMP or LEMP stack depending on the ``stackType`` property.
        It will be used to set up a single instance with everything necessary to run a web stack (database, PHP, web server).

        :param scope: The construct scope where the resources will be defined.
        :param id: The ID for the instance, which will be normalized to ensure it is valid for AWS resources.
        :param stack_type: The type of stack to deploy, which can be either a basic web stack or a hardened web stack.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.

        :throws: Error if AWS-specific properties are not provided in props.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171cd4ce02c5363aca883adf7292f272fefa0b75564c2690cd4b12b8b800b37d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        props = BaseWebStackProps(
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deployWebStack", [scope, id, stack_type, props]))


@jsii.data_type(
    jsii_type="cdktf-infra-uniovi.AwsServerProps",
    jsii_struct_bases=[BasicAWSMachineComponentProps],
    name_mapping={
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "use_persistence": "usePersistence",
        "vpc_id": "vpcId",
        "security_group_ingress_rules": "securityGroupIngressRules",
    },
)
class AwsServerProps(BasicAWSMachineComponentProps):
    def __init__(
        self,
        *,
        security_group_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        use_persistence: typing.Optional[builtins.bool] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param security_group_id: Security Group ID to associate with the machine. This is an optional property, and if not specified, a newly created security group will be used.
        :param subnet_id: Subnet ID where the machine will be deployed. This is an optional property, and if not specified, the default subnet will be used. If you specify a VPC, you must also specify a subnet within that VPC.
        :param use_persistence: Whether to use persistence for the machine. This is an optional property, and if not specified, it defaults to false. If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        :param vpc_id: Virtual Private Cloud (VPC) ID where the machine will be deployed. This is an optional property, and if not specified, the default VPC will be used.
        :param security_group_ingress_rules: An optional list of security group ingress rules to apply to the server. This property allows you to define specific rules for inbound traffic to the server. Each rule must follow the ``SecurityGroupIngress`` schema.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd24ee47164c1514968787b5d679189bc8547ba87ec04ed03907fae9c984192)
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument use_persistence", value=use_persistence, expected_type=type_hints["use_persistence"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument security_group_ingress_rules", value=security_group_ingress_rules, expected_type=type_hints["security_group_ingress_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if use_persistence is not None:
            self._values["use_persistence"] = use_persistence
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if security_group_ingress_rules is not None:
            self._values["security_group_ingress_rules"] = security_group_ingress_rules

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''Security Group ID to associate with the machine.

        This is an optional property, and if not specified, a newly created security group will be used.
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID where the machine will be deployed.

        This is an optional property, and if not specified, the default subnet will be used.
        If you specify a VPC, you must also specify a subnet within that VPC.
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_persistence(self) -> typing.Optional[builtins.bool]:
        '''Whether to use persistence for the machine.

        This is an optional property, and if not specified, it defaults to false.
        If set to true, the machine will be configured to use persistent storage, using an EBS volume for AWS.
        '''
        result = self._values.get("use_persistence")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Virtual Private Cloud (VPC) ID where the machine will be deployed.

        This is an optional property, and if not specified, the default VPC will be used.
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ingress_rules(
        self,
    ) -> typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]]:
        '''An optional list of security group ingress rules to apply to the server.

        This property allows you to define specific rules for inbound traffic to the server.
        Each rule must follow the ``SecurityGroupIngress`` schema.
        '''
        result = self._values.get("security_group_ingress_rules")
        return typing.cast(typing.Optional[typing.List[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDeployStrategy)
class DockerDeployStrategy(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.DockerDeployStrategy",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="deployBasicMachine")
    def deploy_basic_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        basic_machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a basic, generic Docker container using the provided properties.

        This method is used to deploy a basic machine using Docker.
        It creates a Docker image and a container with the specified configurations.
        Optionally, it can include volumes, either a default volume or a set of volumes passed by the user

        :param scope: The scope in which the resources will be created.
        :param id: The ID of the machine component, which will be normalized to ensure it is valid for Docker resources.
        :param basic_machine_props: An object containing the properties for the basic machine. At this point it should include Docker-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing the Docker container.

        :throws: Error if internal Docker properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b25d0df1a471b1f275d3dc68b8053e965e170c8996dde96e8a75eee3cd0c5a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument basic_machine_props", value=basic_machine_props, expected_type=type_hints["basic_machine_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicMachine", [scope, id, basic_machine_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployBasicServer")
    def deploy_basic_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a basic Docker server using the provided properties.

        This method is used to deploy a basic server using Docker.
        It creates a Docker image and a container with the specified configurations.
        Optionally, it can include volumes, either a default volume or a set of volumes passed by the user.
        This method is specifically designed for server deployments, which may include additional configurations such as ports and networks.
        By default, it will expose ports 80 and 443, but this can be customized through the serverProps.

        :param scope: The scope in which the resources will be created.
        :param id: The ID of the server component, which will be normalized to ensure it is valid for Docker resources.
        :param server_props: An object containing the properties for the server. At this point it should include Docker-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing the Docker container.

        :throws: Error if internal Docker properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1ae1baf0995a921a7fa63c914d232da28a6e1410588f4634cb0ce4e6798a3d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployBasicServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployCustomMachine")
    def deploy_custom_machine(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        custom_machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a custom Docker machine using the provided properties.

        This method is used to deploy a custom machine using Docker.
        A custom machine is any machine that is slightly more complex than a basic machine, and that will require a custom Docker image that we build with a custom Dockerfile.
        It can include additional configurations such as ports, networks, and volumes.

        :param scope: The scope in which the resources will be created.
        :param id: The ID of the machine component, which will be normalized to ensure it is valid for Docker resources.
        :param custom_machine_props: An object containing the properties for the custom machine. At this point it should include Docker-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing the Docker container.

        :throws: Error if internal Docker properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fe186e16aea3b23f00fc045bdae8a2fac14c902cf8ef2fecc3af7a68113885)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument custom_machine_props", value=custom_machine_props, expected_type=type_hints["custom_machine_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployCustomMachine", [scope, id, custom_machine_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployHardenedServer")
    def deploy_hardened_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates a hardened Docker server using the provided properties.

        This method is used to deploy an hardened server using Docker.
        It creates a Docker image and a container with the specified configurations.
        Optionally, it can include volumes, either a default volume or a set of volumes passed by the user.
        This method is specifically designed for server deployments, which may include additional
        configurations such as ports and networks.
        By default, it will expose ports 80 and 443, but this can be customized through the serverProps.

        :param scope: The scope in which the resources will be created.
        :param id: The ID of the server component, which will be normalized to ensure it is valid for Docker resources.
        :param server_props: An object containing the properties for the server. At this point it should include Docker-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing the Docker container.

        :throws: Error if internal Docker properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f47e0fdbd4c4c7fe642e904cdadd83eea41acdeba0a071157cccba66268d095)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployHardenedServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployInsecureServer")
    def deploy_insecure_server(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        *,
        aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
        ubuntu_pro_token: typing.Optional[builtins.str] = None,
    ) -> _constructs_77d1e7e8.Construct:
        '''Generates an insecure Docker server using the provided properties.

        This method is used to deploy an insecure server using Docker.
        It creates a Docker image and a container with the specified configurations.
        Optionally, it can include volumes, either a default volume or a set of volumes passed by the user.
        This method is specifically designed for server deployments, which may include additional
        configurations such as ports and networks.
        By default, it will expose port 80 (mapped to 8080 by default), but this can be customized through the serverProps.

        :param scope: The scope in which the resources will be created.
        :param id: The ID of the server component, which will be normalized to ensure it is valid for Docker resources.
        :param server_props: An object containing the properties for the server. At this point it should include Docker-specific properties.
        :param aws_props: 
        :param docker_props: 
        :param ubuntu_pro_token: Ubuntu Pro subscription token used to attach the instance.

        :return: A Construct representing the Docker container.

        :throws: Error if internal Docker properties are not provided in internalMachineComponentProps.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3bf0988e74e74ce6fa602970fa73709e562117c0107ce0b9a703e7feb036ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
        internal_machine_component_props = InternalMachineComponentPropsInterface(
            aws_props=aws_props,
            docker_props=docker_props,
            ubuntu_pro_token=ubuntu_pro_token,
        )

        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deployInsecureServer", [scope, id, server_props, internal_machine_component_props]))

    @jsii.member(jsii_name="deployWebStack")
    def deploy_web_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        stack_type: StackType,
        *,
        my_sql_database: typing.Optional[builtins.str] = None,
        my_sql_password: typing.Optional[builtins.str] = None,
        my_sql_root_password: typing.Optional[builtins.str] = None,
        my_sql_user: typing.Optional[builtins.str] = None,
        my_sql_version: typing.Optional[MySQLVersion] = None,
    ) -> None:
        '''Generates a basic web stack using the provided properties.

        This method is used to deploy a web stack using Docker, which can be either a LAMP or LEMP stack depending on the ``stackType`` property.
        It will create several Docker containers, including a MySQL container, an Apache or Nginx container with PHP, and optionally a PhpMyAdmin container (only for LAMP stacks)

        :param scope: The construct scope in which the resources will be created.
        :param id: The ID of the web stack component, which will be normalized to ensure it is valid for Docker resources.
        :param stack_type: The type of web stack to deploy, which can be either LAMP or LEMP.
        :param my_sql_database: 
        :param my_sql_password: 
        :param my_sql_root_password: 
        :param my_sql_user: 
        :param my_sql_version: The type of stack being deployed. This property is used to determine the specific stack configuration and behavior. It is a mandatory property and must be one of the supported stack types.

        :throws: Error if Docker-specific properties are not provided in props.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ffd11e1f9b5ca832f576d6beceed9f2704228a74c6e9279a4e943ca6ebb7852)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
        props = BaseWebStackProps(
            my_sql_database=my_sql_database,
            my_sql_password=my_sql_password,
            my_sql_root_password=my_sql_root_password,
            my_sql_user=my_sql_user,
            my_sql_version=my_sql_version,
        )

        return typing.cast(None, jsii.invoke(self, "deployWebStack", [scope, id, stack_type, props]))


class HardenedNginxServer(
    NginxServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.HardenedNginxServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: NginxVersion,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd8ed441cb005facb3f907de10a46a2c1a5d447e2fb10b21677e2d8ecf77cef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0de645e77e99f7feccfe868d75f652d10a889413aff9d5d622a58f339f9407)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc522b1e614a73750e3aad7b1ffd30c22067bb1e10e4c3bb300e11d65058f932)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a398f9e799d2a6fbb1f4b9be43693dddea30c7606bdd58deeea60d8179e0e09a)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedNginxImagesMap")
    def _supported_nginx_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedNginxImagesMap"))


class InsecureNginxServer(
    NginxServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.InsecureNginxServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: NginxVersion,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e241d34cd83fb3ff4bbc0636d9b6be657b06387dabe548966001b67ead1fc23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27347f49761605baf005f08e09e2bc164f8b15fb5822b745f1d316d98f3bb487)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf266704231e27e1fff6cc11408f4efda9d1893480f0ce5fcb00e11fbc5b9690)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d90230433b939c62513e9153cbd794542a2605f10ee121dad5e01b52e4c4564)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedNginxImagesMap")
    def _supported_nginx_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedNginxImagesMap"))


class NginxServer(
    NginxServerBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-infra-uniovi.NginxServer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        version: NginxVersion,
        server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -
        :param server_props: -
        :param provider: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3389a1afa5253f74607c1ee72c948630b3fb62e1bfd2d2ee25ff86c31997a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument server_props", value=server_props, expected_type=type_hints["server_props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        jsii.create(self.__class__, self, [scope, id, version, server_props, provider])

    @jsii.member(jsii_name="deploy")
    def _deploy(
        self,
        strategy: IDeployStrategy,
        id: builtins.str,
        props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
        image_identifier: builtins.str,
    ) -> _constructs_77d1e7e8.Construct:
        '''
        :param strategy: -
        :param id: -
        :param props: -
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d281d513f626d08ba1b92f07a3c4ef7403b834dadee0a713a6a9e3f22a0417)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.invoke(self, "deploy", [strategy, id, props, image_identifier]))

    @jsii.member(jsii_name="getAWSProps")
    def _get_aws_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2229fb161b18647fbc121ac9133ecc84a89cc36d7a4fc0d924e08736c40ada42)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getAWSProps", [image_identifier]))

    @jsii.member(jsii_name="getDockerProps")
    def _get_docker_props(
        self,
        image_identifier: builtins.str,
    ) -> InternalMachineComponentPropsInterface:
        '''
        :param image_identifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556ba16a5a354b96b869bdcc32d04f9a72b7eddf4922e678bd72a23787dfe97f)
            check_type(argname="argument image_identifier", value=image_identifier, expected_type=type_hints["image_identifier"])
        return typing.cast(InternalMachineComponentPropsInterface, jsii.invoke(self, "getDockerProps", [image_identifier]))

    @builtins.property
    @jsii.member(jsii_name="supportedNginxImagesMap")
    def _supported_nginx_images_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "supportedNginxImagesMap"))


__all__ = [
    "AWSLampStackProps",
    "AWSLempStackProps",
    "AlpineBasic",
    "AlpineVersion",
    "ApachePhpVersion",
    "ApacheServer",
    "ApacheServerBase",
    "ApacheVersion",
    "AwsDeployStrategy",
    "AwsServerProps",
    "BaseInfrastructureComponentProps",
    "BaseWebStackProps",
    "BasicAWSMachineComponentProps",
    "BasicDockerMachineComponentProps",
    "BasicMachineComponentPropsInterface",
    "CustomAWSMachineComponentProps",
    "CustomDockerMachineComponentProps",
    "CustomMachineComponentPropsInterface",
    "DebianBasic",
    "DebianVersion",
    "DockerDeployStrategy",
    "DockerLampStackProps",
    "DockerLempStackProps",
    "DockerServerProps",
    "HardenedApacheServer",
    "HardenedNginxServer",
    "IDeployStrategy",
    "InsecureApacheServer",
    "InsecureNginxServer",
    "InternalAWSMachineComponentProps",
    "InternalDockerMachineComponentProps",
    "InternalMachineComponentPropsInterface",
    "LampBase",
    "LampStack",
    "LampStackPropsInterface",
    "LempBase",
    "LempStack",
    "LempStackPropsInterface",
    "MySQLVersion",
    "NginxPhpVersion",
    "NginxServer",
    "NginxServerBase",
    "NginxVersion",
    "PhpMyAdminVersion",
    "ProviderDeployStrategyFactory",
    "ProviderType",
    "ServerPropsInterface",
    "SingletonProviderFactory",
    "StackType",
    "UbuntuBasic",
    "UbuntuCustomBase",
    "UbuntuDNS",
    "UbuntuDesktop",
    "UbuntuDev",
    "UbuntuPro",
    "UbuntuVersion",
]

publication.publish()

def _typecheckingstub__dc1c88e55650acb8cd26beb46e93279b6ab68082efb8a603c2d209d08ae25f77(
    *,
    subnet_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d0e2f1f5bfc6aaa08bf8524aded636bce2c90bb338d07a11b1dafbf67e7027(
    *,
    subnet_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab4b89ab300a09efded257e20057e657c525929c5dc6065dcd25c706a85e1f3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: AlpineVersion,
    machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b14f4090e7b53cf7153776330e879424e0ef2d7bf74e4996449cf14a4315f(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fc86fbbfa58c958051ee8edaeb6588d07011d4493441d653ab7ea9f334e2ef(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfce72c124795bc07abd86c038f1657e7667a04a8940ca2617d97645a8a6183(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: ApacheVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242e20e5ecea7213fd0a62d403d97656f346fb7e68d8bbf0f7f4c28b10688d8e(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45edbfafca7edf65e7477cead254c2ca9c54a3540dce3edad8b996e60958250f(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab703c2304d30f51cda5145ddcecfdb9c622cdf8a4975523a7137e21d8bc2911(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b494b9acd5949030a62f4cb11b3e530363ee3cad9951871aa1ae04889f43d3(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16381f5fae20c854994c8a3ebe8c1c87f8720d0ab680f42ada041d25141480cd(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1301670514c8c4548413681cfd9ccb34f2f4031ab2ed7e49bcdb5e76ca7e405(
    *,
    provider_type: ProviderType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ef02751303e2e918a9fa28cd7ddfbde85004b0b5cd4d2df0d7aaab56d85963(
    *,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0dfbf5fff865407a05f6cc613e9837be3a91fc970d20711fce3334718ccc7f(
    *,
    security_group_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    use_persistence: typing.Optional[builtins.bool] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8278e4fc9967ab072168da7fd2d542df00a8b166f95e6e4c74cd945d3a90ab(
    *,
    networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_volume: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d96babee21da0697cf5cadc06b2fd6341ac04551e3e85e9119e157c9432906(
    *,
    provider_type: ProviderType,
    aws_props: typing.Optional[typing.Union[BasicAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[BasicDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d69ac0dad572bcb03bb2c83dbaf0274bc1e8a1bf86473767d9222c2291b770(
    *,
    security_group_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    use_persistence: typing.Optional[builtins.bool] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    custom_user_data: typing.Optional[builtins.str] = None,
    security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee038677aa7af54bb41889f21c36c3a8c903aecaed9b3b1c4a1ffce4b2881094(
    *,
    networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_volume: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    expose_rdp: typing.Optional[builtins.bool] = None,
    expose_ssh: typing.Optional[builtins.bool] = None,
    expose_vnc: typing.Optional[builtins.bool] = None,
    external_rdp_port: typing.Optional[jsii.Number] = None,
    external_ssh_port: typing.Optional[jsii.Number] = None,
    external_vnc_port: typing.Optional[jsii.Number] = None,
    ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4808c88d1e8ec8a3012318a609934006dcb0e556333dcc48e16dcb99d3a062eb(
    *,
    provider_type: ProviderType,
    aws_props: typing.Optional[typing.Union[CustomAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[CustomDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8fff4725a9531cbe5ba90a833a827a492919dc2b94a5f1f50a3de82d53b33e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: DebianVersion,
    machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69745c6888fde783f2a0e5eb2a675c0d625f8b4803e917e1740247f96f52f0b(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae3e48f35b030c95ce243920649f0c48b15a5d51c555dd98557e85d9af31529(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bab3cd38ab08ed1da9dd85b29f394a497a1f64d77bf4987b4bfbff09094c3ac(
    *,
    apache_port: typing.Optional[jsii.Number] = None,
    my_sql_port: typing.Optional[jsii.Number] = None,
    php_my_admin_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f747830eb36daee7cd0e8c3142251d4aa4a36192eb684f4a9fd36cd43d7696(
    *,
    my_sql_port: typing.Optional[jsii.Number] = None,
    nginx_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e38d0dbe099a9768f7239c0773c380ee979046b507fa00b696d9c821b421ef(
    *,
    networks: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_volume: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d728d3b23b650af7747c1596f058c9ad6298312523c2ae8c8670f0d087151836(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: ApacheVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b597728661842fa87b5f42a12c1afbbe2ef8198aec2c987dab9c0152502c917f(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395a3fb982c69ec9593f03aa97b81a73a6d6df8f360e0368de10de404faadad3(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327206b80fd862bb959d3d21a5aa0f767a9aa8e6c5c18bf89e75e0aeba658138(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889b2c0b9e2cfb286cdb5c78a4692ba25a70c9d8f374856ff29d74ddbc557f9f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9459499ef26471a73827589507bc1f457b23a14664edc8cb331b2a8b029976bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32adc70207f1d2f865c7ee5e3be5fbe26098aef1f83cb5e910a5e47e92e444b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a02e7392467234db22ee01df8595c5be808d50c5d011c9df600a686ab3a947(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d166d5d086a1f423ede45830d6dcf2f23708cb5bb1ecbd4427dbfcf2b928353f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16835735b7ab044be3c3b6c7057fb70d0a2269ca8dbafc31d1ae5f93b0c74cc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    stack_type: StackType,
    *,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319da680f78f1987973a782ebcd43888580287cbd5e2856aca5fce355490e00e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: ApacheVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275509706f5a851f5847fe77008769f10760f3cc034511e2de8a55901536f9b6(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5919c25cd1aee440ce574deb64f9bc1554d20e17c1d3c94e5204dcb3ee5f3fd(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbe6c041cbbd254bf301b115fe57db3aad13bc90b182f55b0f4e87ba2c63126(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714ef897a68d6f74d414742128a8107dbb21ca1ab4bd337b137b581c51ac3d28(
    *,
    ami: builtins.str,
    additional_security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_init_script_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015cf9cbcbee88765f5fe6bcfb61efd2907315ffc98f41eb63d6bb2149eaeb06(
    *,
    image_name: builtins.str,
    additional_ports: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_docker_container_ee71896e.ContainerPorts, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    custom_command: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_image_name: typing.Optional[builtins.str] = None,
    dockerfile_path: typing.Optional[builtins.str] = None,
    volume_container_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835395862fa576af5bb917b2fc6118b4bf24a3d2bcec9fa48acaf6b8f7815b07(
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de5c0c54c2315787d46bc1aea61e48f257987ea22ae91838c511a4b298be031(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    include_php_my_admin: builtins.bool,
    aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_my_admin_version: typing.Optional[PhpMyAdminVersion] = None,
    php_version: typing.Optional[ApachePhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507633b94040c0417258d57320505bc2a21b2ac2b9b926d45c1213829d391189(
    strategy: IDeployStrategy,
    id: builtins.str,
    stack_type: StackType,
    *,
    include_php_my_admin: builtins.bool,
    aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_my_admin_version: typing.Optional[PhpMyAdminVersion] = None,
    php_version: typing.Optional[ApachePhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b7f54e01aba634ed622dbbfc09529f898468c8fbfc389e69500de22dc27a77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    include_php_my_admin: builtins.bool,
    aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_my_admin_version: typing.Optional[PhpMyAdminVersion] = None,
    php_version: typing.Optional[ApachePhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d7b2445ea5a2780fed8d0235eba300bb73f08ea63ac32678b2110f1351244c(
    strategy: IDeployStrategy,
    id: builtins.str,
    stack_type: StackType,
    *,
    include_php_my_admin: builtins.bool,
    aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_my_admin_version: typing.Optional[PhpMyAdminVersion] = None,
    php_version: typing.Optional[ApachePhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c00a24e3e3f48fdc1b1828556a3a5e104b2bcf54744cf6fe676c6ca500482d(
    *,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
    include_php_my_admin: builtins.bool,
    aws_props: typing.Optional[typing.Union[AWSLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLampStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_my_admin_version: typing.Optional[PhpMyAdminVersion] = None,
    php_version: typing.Optional[ApachePhpVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef47cdd9b9729164452374528b41aef7b178b2a176466dc2a67b1fefa493dae(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_version: typing.Optional[NginxPhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5721c9f1ab3eabd5ee92c0f3eb63542cc4e53ea319b3eafda31e96d6ac20ea94(
    strategy: IDeployStrategy,
    id: builtins.str,
    stack_type: StackType,
    *,
    aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_version: typing.Optional[NginxPhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6e65cbf150499c5de69757d7dae7833c70fe77878a36965f42e68a21e940ed(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_version: typing.Optional[NginxPhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea52fd1abd6c632502d418e37c7e5e24dd2b1358d2074d02f43e950417dc436(
    strategy: IDeployStrategy,
    id: builtins.str,
    stack_type: StackType,
    *,
    aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_version: typing.Optional[NginxPhpVersion] = None,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947b4c93dad362e677d5374d8b920798e538d954b19907e686d5a693b13c3ec6(
    *,
    provider_type: ProviderType,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
    aws_props: typing.Optional[typing.Union[AWSLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerLempStackProps, typing.Dict[builtins.str, typing.Any]]] = None,
    php_version: typing.Optional[NginxPhpVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59d9a908833100222d2377a2e27a8ae09d09399908be22914ec0b7037df7e5b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: NginxVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b8b7f49d14a0e66e1f5337dd3177563267ee4cfe7f9d5bb9458ff297e38800(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f4c22a95b5ad65da4577021b8a62753fd36ef0bb9592771499d8c0b0905fed(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c510fa95b5603372bdc810e257045d70bed453c10724571704b3c53b6e333667(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fa848ce215cc43df526e0d8e3bc4ce84241e900fa6ca98ef14e2bd430925b4(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0548c9484d04d3aaae47827a5e7633be9aba36cd5ab36051903872fb5a6208(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2080356753be8befde69a2f8e8ec78e1a71e3ce7fddf270dc9d3aef3481326a(
    provider_type: ProviderType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e18d8a93c32e6107de35c15d2595a8db35635394f96bc23d9ccbcd6da0930f(
    *,
    provider_type: ProviderType,
    aws_props: typing.Optional[typing.Union[AwsServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[DockerServerProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11070dc128f531d20c08489c265205b236198116d9e9bbef274657ac5688775(
    provider_type: ProviderType,
    scope: _constructs_77d1e7e8.Construct,
    existing_provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0a16f71c1676817471c049e101bb6bfac39feb071711d4c48e937665834773(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd828c869b09b3569e16794d148ed6fa809b76c8b16128f66ea88a5e6ba8ec70(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1457d466794c7ed795f210c51f844db27be2097fce99221996937da4f7b5564d(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b4588982ea58d44c172e712846d318fd163e224386cfe30f189f14fc4dbe8(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d8aa3e2a7e296ae1cccbcb9e19714f85704e5a5563e5f73007fcd6db309ff1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d503eab41f04657723f0052bd99a733946ca0f70e47e7eceb5452c9d81da9c3c(
    provider_type: ProviderType,
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afce00d1252a3a98b78bc5db46da5af9a1c69c659b086f5782ce33a41325f23f(
    value: typing.Optional[_constructs_77d1e7e8.Construct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a005d0708ba8d9d28b40ffbbfea5b77797c8744ff51390fdfb37ebe418cc54(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1aaed65460e5b3502d68087194ebd3dab02b58b27d47d8c9ce8689ff53138c7(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4516d2d2f557d001451c6489dbeaf6e8e12065af729e5155459c758d0c2fa850(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd110e4bb21886852e7a303f0550ce50e51fdb3227aaee26bcfababa7c2dbfb4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bdef2a26c328ab84d91fcc04e8b102ab5bbc2659ae242de7720b22d6a974b7d(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad24b166cc97abca23ff3f2b0f7ac94e10d10add10f6ee21be0b88265b15b97(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77cb41ac667e13eba8683afaea4e0e23005246a5ccabae8cccf43b90799c990(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331408f97be7677ee8e88b704b6de9216b87c51b5834b3925e79e7c2287c59c8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35329d70f8191129073ec63c9946b53f8a67e06bcf054948cf1f7980cb012bf4(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df3f22236e85c274c7f2ee22626189b770239f44f65ad6d2168b678d8aa7cec(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ef6edb5b2fbc752a12df16a0e315e74a6567b82d287302ad1f480a2723fcd4(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948da948ea46ad497ce95b82af7af071050f16711f618b0703476cc2f38eeed1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651dd48fe714fc4d7fe8d279daf8f5e7e4e831e3778164234ca6ef91d46bfba8(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d0beb27dc67f1a9593ce0370284f73f35f3a141a3234ff8b180506413705fc(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5676dd1b0fb24e619bca0764cefa48953e77652590d997c0bb0cd598b4e97a01(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691d976ab3bb6955afa4ca620f3e3cefd56d1f397fa9be4b778c81796284fe97(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: UbuntuVersion,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf369f593c5e7ac1fdd5efdf7944e2a8f396c3038fe3e4ae2de6bd19445b8055(
    strategy: IDeployStrategy,
    id: builtins.str,
    machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b67ca64ee90b24ad7c1d024685537ede3a67e3678122257509a5b691f6fa5a(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a03358cd2a888a28e1c4b8ff69892a941dfdfeca12e2b59b9e605b456082ac9(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754a0841dcd127c3b3d95e7d75af64ab64e6455ae70d34813e60c8f70baab75b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b880d3fd3a8eba683422ba87d6b4201851b2fe27b352c6f24afb34e58ce98d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: ApacheVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee44ed9483053198ca680f25df91a47f2b12656bd477b3fb4a03c7b97b1c3420(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f6c82c52ca37cb2040529f14fd63be2ef16bfdad3f2a6f44bb561927371b62(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467f540c2bcc3f37b1cca514cb6a50fd878e2c73b717204d00b12985c18d500a(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff819fdd70c14b81b199b4c4e6625db43cbb99dc64222e75ff4eab44d945573(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    basic_machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f16f369c3f55f8c3397b8c96b247658c3c03138ff7970eda0cfb2202134e009(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a1bab275f8f16873057a216ee85745694d109846297586d780793f22eae540(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    custom_machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a01de8860acc93ac60bbb0dea3e01bb7182e57f497695c9f676d0231609117(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4666c86f2820e532bafee339cfbce32e1513095cd458cab1aae58d6954ab7a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171cd4ce02c5363aca883adf7292f272fefa0b75564c2690cd4b12b8b800b37d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    stack_type: StackType,
    *,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd24ee47164c1514968787b5d679189bc8547ba87ec04ed03907fae9c984192(
    *,
    security_group_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    use_persistence: typing.Optional[builtins.bool] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    security_group_ingress_rules: typing.Optional[typing.Sequence[typing.Union[_cdktf_cdktf_provider_aws_security_group_0cbe8a87.SecurityGroupIngress, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b25d0df1a471b1f275d3dc68b8053e965e170c8996dde96e8a75eee3cd0c5a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    basic_machine_props: typing.Union[BasicMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1ae1baf0995a921a7fa63c914d232da28a6e1410588f4634cb0ce4e6798a3d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fe186e16aea3b23f00fc045bdae8a2fac14c902cf8ef2fecc3af7a68113885(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    custom_machine_props: typing.Union[CustomMachineComponentPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f47e0fdbd4c4c7fe642e904cdadd83eea41acdeba0a071157cccba66268d095(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3bf0988e74e74ce6fa602970fa73709e562117c0107ce0b9a703e7feb036ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    *,
    aws_props: typing.Optional[typing.Union[InternalAWSMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_props: typing.Optional[typing.Union[InternalDockerMachineComponentProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ubuntu_pro_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffd11e1f9b5ca832f576d6beceed9f2704228a74c6e9279a4e943ca6ebb7852(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    stack_type: StackType,
    *,
    my_sql_database: typing.Optional[builtins.str] = None,
    my_sql_password: typing.Optional[builtins.str] = None,
    my_sql_root_password: typing.Optional[builtins.str] = None,
    my_sql_user: typing.Optional[builtins.str] = None,
    my_sql_version: typing.Optional[MySQLVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd8ed441cb005facb3f907de10a46a2c1a5d447e2fb10b21677e2d8ecf77cef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: NginxVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0de645e77e99f7feccfe868d75f652d10a889413aff9d5d622a58f339f9407(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc522b1e614a73750e3aad7b1ffd30c22067bb1e10e4c3bb300e11d65058f932(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a398f9e799d2a6fbb1f4b9be43693dddea30c7606bdd58deeea60d8179e0e09a(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e241d34cd83fb3ff4bbc0636d9b6be657b06387dabe548966001b67ead1fc23(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: NginxVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27347f49761605baf005f08e09e2bc164f8b15fb5822b745f1d316d98f3bb487(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf266704231e27e1fff6cc11408f4efda9d1893480f0ce5fcb00e11fbc5b9690(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d90230433b939c62513e9153cbd794542a2605f10ee121dad5e01b52e4c4564(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3389a1afa5253f74607c1ee72c948630b3fb62e1bfd2d2ee25ff86c31997a6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    version: NginxVersion,
    server_props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d281d513f626d08ba1b92f07a3c4ef7403b834dadee0a713a6a9e3f22a0417(
    strategy: IDeployStrategy,
    id: builtins.str,
    props: typing.Union[ServerPropsInterface, typing.Dict[builtins.str, typing.Any]],
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2229fb161b18647fbc121ac9133ecc84a89cc36d7a4fc0d924e08736c40ada42(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556ba16a5a354b96b869bdcc32d04f9a72b7eddf4922e678bd72a23787dfe97f(
    image_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
