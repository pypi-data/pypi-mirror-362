r'''
# cdk-eks-cluster-module

cdk-eks-cluster-module  is a [CDK]((github.com/aws-cdk/cdk)) that helps you configure complete EKS clusters that are fully bootstrapped with the operational software that is needed to deploy and operate workloads. You can describe the configuration for the desired state of your EKS cluster, such as the control plane, worker nodes, and Kubernetes add-ons, as code.

## :sparkles: Features

* :white_check_mark: AWS EKS Cluster Addons
* :white_check_mark: Support for Multiple NodeGroups with labels and taints
* :white_check_mark: Support for Multiple fargate profiles with labels and namespace
* :white_check_mark: AWS EKS Identity Provider Configuration
* :white_check_mark: Support for custom AMI, custom launch template, and custom user data including custom user data template
* :white_check_mark: commonComponents interface allow to install custom repo/local helm chart
* :white_check_mark: Install aws-ebs-csi-driver,aws-efs-csi-driver,node-problem-detector helm charts to help manage storage, and nodes.

## :clapper: Quick Start

The quick start shows you how to create an **AWS-EKS** using this module.

### Prerequisites

* A working [`aws`](https://aws.amazon.com/cli/) CLI installation with access to an account and administrator privileges
* You'll need a recent [NodeJS](https://nodejs.org) installation
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to interact with your fresh cluster

To get going you'll need a CDK project. For details please refer to the [detailed guide for CDK](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html).

Create an empty directory on your system.

```bash
mkdir aws-quick-start-eks && cd aws-quick-start-eks
```

Bootstrap your CDK project, we will use TypeScript, but you can switch to any other supported language.

```bash
npx cdk init sample-eks  --language typescript
npx cdk bootstrap
```

Install using NPM:

```
npm install @smallcase/cdk-eks-cluster-module
```

Using yarn

```
yarn add @smallcase/cdk-eks-cluster-module
```

Using eks cluster can be deployed using the following sample code snippet:

```python
import {
  EKSCluster,
  VpcCniAddonVersion,
} from '@smallcase/cdk-eks-cluster-module';

const key = new kms.Key(this, 'EKS-KMS', {
      enabled: true,
      alias: 'EKS-KMS',
    });
key.addToResourcePolicy(new iam.PolicyStatement({
      sid: 'encrypt root volumes of nodeGroup using kms',
      actions: [
        'kms:Encrypt',
        'kms:Decrypt',
        'kms:ReEncrypt*',
        'kms:GenerateDataKey*',
        'kms:CreateGrant',
        'kms:DescribeKey',
      ],
      resources: ['*'],
      principals: [new iam.AnyPrincipal()],
      conditions: {
        StringEquals: {
          'kms:CallerAccount': '<YOUR-AWS-ID>',
          'kms:ViaService': 'ec2.<REGION>.amazonaws.com',
        },
      },
    }));

  const securityGroup = new ec2.SecurityGroup(
      this,
      'EKS-WORKER-SG',
      {
        vpc: vpc,
        description: 'Kubernetes Worker SecurityGroup',
      },
    );

  const testNodeTemplete = new ec2.LaunchTemplate(this, 'testNodeTemplete', {
      instanceType: new ec2.InstanceType('m5a.large'),
      blockDevices: [
        {
          deviceName: '/dev/xvda',
          volume: ec2.BlockDeviceVolume.ebs(40,
            {
              deleteOnTermination: true,
              encrypted: true,
              volumeType: ec2.EbsDeviceVolumeType.GP3,
              kmsKey: key,
            },
          ),
          mappingEnabled: true,
        },
      ],
    });
let ekscluster = new EKSCluster(this, 'EKS-CLUSTER', {
      availabilityZones: Stack.of(this).availabilityZones,
      clusterVPC: vpc,
      kmsKey: key,
      region: Stack.of(this).region,
      workerSecurityGroup: securityGroup,
      addonProps: {
        vpnCniAddonVersion: VpcCniAddonVersion.V1_11_0,
      },
      clusterConfig: {
        clusterName: 'EKS-CLUSTER',
        clusterVersion: eks.KubernetesVersion.V1_22,
        // this will create cluster autoscaler service account with iam role
        addAutoscalerIam: true,
        albControllerVersion: eks.AlbControllerVersion.V2_2_4,
        defaultCapacity: 3,
        subnets: {
          privateSubnetGroupName: 'Private',
        },
        nodeGroups: [
          {
            name: 'test-node',
            instanceTypes: [],
            minSize: 3,
            maxSize: 6,
            launchTemplateSpec: {
              version: testNodeTemplete.versionNumber,
              id: testNodeTemplete.launchTemplateId!,
            },
            subnetGroupName: 'Private',
            labels: {
              role: 'test-eks-cluster',
            },
            taints: {
              role: 'test-eks-cluster',
            },
            tags: {
              'k8s.io/cluster-autoscaler/enabled': 'TRUE',
              'k8s.io/cluster-autoscaler/EKS-CLUSTER':
                'owned',
            },
          },
        ]
        commonComponents: {
          'aws-efs-csi-driver': {
            iamPolicyPath: ['../../assets/policy/aws-efs-csi-driver-policy.json'],
            // above mention iam policy will be used for this service account
            serviceAccounts: ['efs-csi-controller-sa', 'efs-csi-node-sa'],
            helm: {
              chartName: 'aws-efs-csi-driver',
              chartVersion: '2.2.0',
              helmRepository: 'https://kubernetes-sigs.github.io/aws-efs-csi-driver/',
              namespace: 'kube-system',
            },
          },
        },
        teamMembers: [
          "your-aws-user",
        ],
        teamExistingRolePermission: { //optional
          '<YOUR_ROLE_ARN>': 'system:masters',
        },
      }
  })
```

## [API.md](./API.md)
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_eks as _aws_cdk_aws_eks_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.AddonProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_values": "configurationValues",
        "vpn_cni_addon_version": "vpnCniAddonVersion",
    },
)
class AddonProps:
    def __init__(
        self,
        *,
        configuration_values: typing.Optional[builtins.str] = None,
        vpn_cni_addon_version: typing.Optional["VpcCniAddonVersion"] = None,
    ) -> None:
        '''
        :param configuration_values: 
        :param vpn_cni_addon_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9975c31b067437c657a3f94425cf31b29dcc29137d03fecb2e866ad248fbb6b8)
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
            check_type(argname="argument vpn_cni_addon_version", value=vpn_cni_addon_version, expected_type=type_hints["vpn_cni_addon_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values
        if vpn_cni_addon_version is not None:
            self._values["vpn_cni_addon_version"] = vpn_cni_addon_version

    @builtins.property
    def configuration_values(self) -> typing.Optional[builtins.str]:
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_cni_addon_version(self) -> typing.Optional["VpcCniAddonVersion"]:
        result = self._values.get("vpn_cni_addon_version")
        return typing.cast(typing.Optional["VpcCniAddonVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.ArgoCD",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "cluster_role_name": "clusterRoleName",
    },
)
class ArgoCD:
    def __init__(
        self,
        *,
        assume_role_arn: builtins.str,
        cluster_role_name: builtins.str,
    ) -> None:
        '''
        :param assume_role_arn: 
        :param cluster_role_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a96e07b960fdc73800c6c39016a3ff7b72083a7af299c0ccef5e493ff9060d0)
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument cluster_role_name", value=cluster_role_name, expected_type=type_hints["cluster_role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assume_role_arn": assume_role_arn,
            "cluster_role_name": cluster_role_name,
        }

    @builtins.property
    def assume_role_arn(self) -> builtins.str:
        result = self._values.get("assume_role_arn")
        assert result is not None, "Required property 'assume_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_role_name(self) -> builtins.str:
        result = self._values.get("cluster_role_name")
        assert result is not None, "Required property 'cluster_role_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArgoCD(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.ClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "cluster_version": "clusterVersion",
        "default_capacity": "defaultCapacity",
        "node_groups": "nodeGroups",
        "subnets": "subnets",
        "tags": "tags",
        "team_members": "teamMembers",
        "add_autoscaler_iam": "addAutoscalerIam",
        "alb_controller_version": "albControllerVersion",
        "argo_cd": "argoCD",
        "common_components": "commonComponents",
        "debug_logs": "debugLogs",
        "default_common_components": "defaultCommonComponents",
        "deprecate_cluster_auto_scaler": "deprecateClusterAutoScaler",
        "fargate_profiles": "fargateProfiles",
        "kubectl_layer": "kubectlLayer",
        "namespaces": "namespaces",
        "public_allow_access": "publicAllowAccess",
        "skip_external_dns": "skipExternalDNS",
        "team_existing_role_permission": "teamExistingRolePermission",
    },
)
class ClusterConfig:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        cluster_version: _aws_cdk_aws_eks_ceddda9d.KubernetesVersion,
        default_capacity: jsii.Number,
        node_groups: typing.Sequence[typing.Union["NodeGroupConfig", typing.Dict[builtins.str, typing.Any]]],
        subnets: typing.Union["InternalMap", typing.Dict[builtins.str, typing.Any]],
        tags: typing.Union["InternalMap", typing.Dict[builtins.str, typing.Any]],
        team_members: typing.Sequence[builtins.str],
        add_autoscaler_iam: typing.Optional[builtins.bool] = None,
        alb_controller_version: typing.Optional[_aws_cdk_aws_eks_ceddda9d.AlbControllerVersion] = None,
        argo_cd: typing.Optional[typing.Union[ArgoCD, typing.Dict[builtins.str, typing.Any]]] = None,
        common_components: typing.Optional[typing.Mapping[builtins.str, "ICommonComponentsProps"]] = None,
        debug_logs: typing.Optional[builtins.bool] = None,
        default_common_components: typing.Optional[typing.Union["DefaultCommonComponents", typing.Dict[builtins.str, typing.Any]]] = None,
        deprecate_cluster_auto_scaler: typing.Optional[builtins.bool] = None,
        fargate_profiles: typing.Optional[typing.Sequence[typing.Union["FargateProfile", typing.Dict[builtins.str, typing.Any]]]] = None,
        kubectl_layer: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion] = None,
        namespaces: typing.Optional[typing.Mapping[builtins.str, typing.Union["NamespaceSpec", typing.Dict[builtins.str, typing.Any]]]] = None,
        public_allow_access: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_external_dns: typing.Optional[builtins.bool] = None,
        team_existing_role_permission: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_name: 
        :param cluster_version: 
        :param default_capacity: 
        :param node_groups: 
        :param subnets: 
        :param tags: 
        :param team_members: 
        :param add_autoscaler_iam: 
        :param alb_controller_version: 
        :param argo_cd: 
        :param common_components: 
        :param debug_logs: 
        :param default_common_components: 
        :param deprecate_cluster_auto_scaler: 
        :param fargate_profiles: 
        :param kubectl_layer: 
        :param namespaces: 
        :param public_allow_access: 
        :param skip_external_dns: 
        :param team_existing_role_permission: 
        '''
        if isinstance(subnets, dict):
            subnets = InternalMap(**subnets)
        if isinstance(tags, dict):
            tags = InternalMap(**tags)
        if isinstance(argo_cd, dict):
            argo_cd = ArgoCD(**argo_cd)
        if isinstance(default_common_components, dict):
            default_common_components = DefaultCommonComponents(**default_common_components)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790140b15ea89389baac9354004284c53266f60c5ab92c244d71af13dd772e5e)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument default_capacity", value=default_capacity, expected_type=type_hints["default_capacity"])
            check_type(argname="argument node_groups", value=node_groups, expected_type=type_hints["node_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument team_members", value=team_members, expected_type=type_hints["team_members"])
            check_type(argname="argument add_autoscaler_iam", value=add_autoscaler_iam, expected_type=type_hints["add_autoscaler_iam"])
            check_type(argname="argument alb_controller_version", value=alb_controller_version, expected_type=type_hints["alb_controller_version"])
            check_type(argname="argument argo_cd", value=argo_cd, expected_type=type_hints["argo_cd"])
            check_type(argname="argument common_components", value=common_components, expected_type=type_hints["common_components"])
            check_type(argname="argument debug_logs", value=debug_logs, expected_type=type_hints["debug_logs"])
            check_type(argname="argument default_common_components", value=default_common_components, expected_type=type_hints["default_common_components"])
            check_type(argname="argument deprecate_cluster_auto_scaler", value=deprecate_cluster_auto_scaler, expected_type=type_hints["deprecate_cluster_auto_scaler"])
            check_type(argname="argument fargate_profiles", value=fargate_profiles, expected_type=type_hints["fargate_profiles"])
            check_type(argname="argument kubectl_layer", value=kubectl_layer, expected_type=type_hints["kubectl_layer"])
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
            check_type(argname="argument public_allow_access", value=public_allow_access, expected_type=type_hints["public_allow_access"])
            check_type(argname="argument skip_external_dns", value=skip_external_dns, expected_type=type_hints["skip_external_dns"])
            check_type(argname="argument team_existing_role_permission", value=team_existing_role_permission, expected_type=type_hints["team_existing_role_permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "cluster_version": cluster_version,
            "default_capacity": default_capacity,
            "node_groups": node_groups,
            "subnets": subnets,
            "tags": tags,
            "team_members": team_members,
        }
        if add_autoscaler_iam is not None:
            self._values["add_autoscaler_iam"] = add_autoscaler_iam
        if alb_controller_version is not None:
            self._values["alb_controller_version"] = alb_controller_version
        if argo_cd is not None:
            self._values["argo_cd"] = argo_cd
        if common_components is not None:
            self._values["common_components"] = common_components
        if debug_logs is not None:
            self._values["debug_logs"] = debug_logs
        if default_common_components is not None:
            self._values["default_common_components"] = default_common_components
        if deprecate_cluster_auto_scaler is not None:
            self._values["deprecate_cluster_auto_scaler"] = deprecate_cluster_auto_scaler
        if fargate_profiles is not None:
            self._values["fargate_profiles"] = fargate_profiles
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if namespaces is not None:
            self._values["namespaces"] = namespaces
        if public_allow_access is not None:
            self._values["public_allow_access"] = public_allow_access
        if skip_external_dns is not None:
            self._values["skip_external_dns"] = skip_external_dns
        if team_existing_role_permission is not None:
            self._values["team_existing_role_permission"] = team_existing_role_permission

    @builtins.property
    def cluster_name(self) -> builtins.str:
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_version(self) -> _aws_cdk_aws_eks_ceddda9d.KubernetesVersion:
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.KubernetesVersion, result)

    @builtins.property
    def default_capacity(self) -> jsii.Number:
        result = self._values.get("default_capacity")
        assert result is not None, "Required property 'default_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def node_groups(self) -> typing.List["NodeGroupConfig"]:
        result = self._values.get("node_groups")
        assert result is not None, "Required property 'node_groups' is missing"
        return typing.cast(typing.List["NodeGroupConfig"], result)

    @builtins.property
    def subnets(self) -> "InternalMap":
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast("InternalMap", result)

    @builtins.property
    def tags(self) -> "InternalMap":
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast("InternalMap", result)

    @builtins.property
    def team_members(self) -> typing.List[builtins.str]:
        result = self._values.get("team_members")
        assert result is not None, "Required property 'team_members' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def add_autoscaler_iam(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("add_autoscaler_iam")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def alb_controller_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_eks_ceddda9d.AlbControllerVersion]:
        result = self._values.get("alb_controller_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_eks_ceddda9d.AlbControllerVersion], result)

    @builtins.property
    def argo_cd(self) -> typing.Optional[ArgoCD]:
        result = self._values.get("argo_cd")
        return typing.cast(typing.Optional[ArgoCD], result)

    @builtins.property
    def common_components(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "ICommonComponentsProps"]]:
        result = self._values.get("common_components")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "ICommonComponentsProps"]], result)

    @builtins.property
    def debug_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("debug_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_common_components(self) -> typing.Optional["DefaultCommonComponents"]:
        result = self._values.get("default_common_components")
        return typing.cast(typing.Optional["DefaultCommonComponents"], result)

    @builtins.property
    def deprecate_cluster_auto_scaler(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("deprecate_cluster_auto_scaler")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fargate_profiles(self) -> typing.Optional[typing.List["FargateProfile"]]:
        result = self._values.get("fargate_profiles")
        return typing.cast(typing.Optional[typing.List["FargateProfile"]], result)

    @builtins.property
    def kubectl_layer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]:
        result = self._values.get("kubectl_layer")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion], result)

    @builtins.property
    def namespaces(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "NamespaceSpec"]]:
        result = self._values.get("namespaces")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "NamespaceSpec"]], result)

    @builtins.property
    def public_allow_access(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("public_allow_access")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_external_dns(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("skip_external_dns")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def team_existing_role_permission(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("team_existing_role_permission")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CommonHelmCharts(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.CommonHelmCharts",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
        helm_props: typing.Union["StandardHelmProps", typing.Dict[builtins.str, typing.Any]],
        dependent_namespaces: typing.Optional[typing.Sequence[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]] = None,
        iam_policy_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_charts: typing.Optional[builtins.bool] = None,
        service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param helm_props: 
        :param dependent_namespaces: 
        :param iam_policy_path: 
        :param log_charts: 
        :param service_accounts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5404c69b77f40af5bbafd8659f90a5fea8699752ead3071d1922a0bf7c5466)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CommonHelmChartsProps(
            cluster=cluster,
            helm_props=helm_props,
            dependent_namespaces=dependent_namespaces,
            iam_policy_path=iam_policy_path,
            log_charts=log_charts,
            service_accounts=service_accounts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.CommonHelmChartsProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "helm_props": "helmProps",
        "dependent_namespaces": "dependentNamespaces",
        "iam_policy_path": "iamPolicyPath",
        "log_charts": "logCharts",
        "service_accounts": "serviceAccounts",
    },
)
class CommonHelmChartsProps:
    def __init__(
        self,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
        helm_props: typing.Union["StandardHelmProps", typing.Dict[builtins.str, typing.Any]],
        dependent_namespaces: typing.Optional[typing.Sequence[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]] = None,
        iam_policy_path: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_charts: typing.Optional[builtins.bool] = None,
        service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster: 
        :param helm_props: 
        :param dependent_namespaces: 
        :param iam_policy_path: 
        :param log_charts: 
        :param service_accounts: 
        '''
        if isinstance(helm_props, dict):
            helm_props = StandardHelmProps(**helm_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab74f17dea60f0a28aedf5f616fe27bb0b4691796b641bfd375294bc66c1416a)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument helm_props", value=helm_props, expected_type=type_hints["helm_props"])
            check_type(argname="argument dependent_namespaces", value=dependent_namespaces, expected_type=type_hints["dependent_namespaces"])
            check_type(argname="argument iam_policy_path", value=iam_policy_path, expected_type=type_hints["iam_policy_path"])
            check_type(argname="argument log_charts", value=log_charts, expected_type=type_hints["log_charts"])
            check_type(argname="argument service_accounts", value=service_accounts, expected_type=type_hints["service_accounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "helm_props": helm_props,
        }
        if dependent_namespaces is not None:
            self._values["dependent_namespaces"] = dependent_namespaces
        if iam_policy_path is not None:
            self._values["iam_policy_path"] = iam_policy_path
        if log_charts is not None:
            self._values["log_charts"] = log_charts
        if service_accounts is not None:
            self._values["service_accounts"] = service_accounts

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.ICluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.ICluster, result)

    @builtins.property
    def helm_props(self) -> "StandardHelmProps":
        result = self._values.get("helm_props")
        assert result is not None, "Required property 'helm_props' is missing"
        return typing.cast("StandardHelmProps", result)

    @builtins.property
    def dependent_namespaces(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]]:
        result = self._values.get("dependent_namespaces")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]], result)

    @builtins.property
    def iam_policy_path(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("iam_policy_path")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_charts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("log_charts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("service_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonHelmChartsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.CoreAddonProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "addon_version": "addonVersion",
        "configuration_values": "configurationValues",
        "namespace": "namespace",
        "resolve_conflicts": "resolveConflicts",
    },
)
class CoreAddonProps:
    def __init__(
        self,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        addon_version: typing.Optional[builtins.str] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resolve_conflicts: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param cluster: 
        :param addon_version: 
        :param configuration_values: 
        :param namespace: 
        :param resolve_conflicts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f74064bc618ba94d9f9df56e3c897a47a160945504e0c88228c2c8f12ed3ae4)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument resolve_conflicts", value=resolve_conflicts, expected_type=type_hints["resolve_conflicts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
        }
        if addon_version is not None:
            self._values["addon_version"] = addon_version
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values
        if namespace is not None:
            self._values["namespace"] = namespace
        if resolve_conflicts is not None:
            self._values["resolve_conflicts"] = resolve_conflicts

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, result)

    @builtins.property
    def addon_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("addon_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_values(self) -> typing.Optional[builtins.str]:
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolve_conflicts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("resolve_conflicts")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.CoreAddonValuesProps",
    jsii_struct_bases=[],
    name_mapping={
        "addon_version": "addonVersion",
        "configuration_values": "configurationValues",
    },
)
class CoreAddonValuesProps:
    def __init__(
        self,
        *,
        addon_version: typing.Optional[builtins.str] = None,
        configuration_values: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addon_version: 
        :param configuration_values: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e12355f4b84b8449c52f3fc2b5c257b35c96dd52f870f39e67c6efc6b89beea)
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addon_version is not None:
            self._values["addon_version"] = addon_version
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values

    @builtins.property
    def addon_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("addon_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_values(self) -> typing.Optional[builtins.str]:
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoreAddonValuesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CoreDnsAddon(
    _aws_cdk_aws_eks_ceddda9d.CfnAddon,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.CoreDnsAddon",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        addon_version: typing.Optional[builtins.str] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resolve_conflicts: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param addon_version: 
        :param configuration_values: 
        :param namespace: 
        :param resolve_conflicts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e171c7882ef3806f1271b18a97a551178f47e6bac56547d01c9ab3c32b6a95b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CoreAddonProps(
            cluster=cluster,
            addon_version=addon_version,
            configuration_values=configuration_values,
            namespace=namespace,
            resolve_conflicts=resolve_conflicts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.DefaultCommonComponents",
    jsii_struct_bases=[],
    name_mapping={
        "aws_ebs_csi_driver": "awsEbsCsiDriver",
        "aws_efs_csi_driver": "awsEfsCsiDriver",
        "cluster_autoscaler": "clusterAutoscaler",
        "external_dns": "externalDns",
    },
)
class DefaultCommonComponents:
    def __init__(
        self,
        *,
        aws_ebs_csi_driver: typing.Optional[typing.Union["DefaultCommonComponentsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_efs_csi_driver: typing.Optional[typing.Union["DefaultCommonComponentsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_autoscaler: typing.Optional[typing.Union["DefaultCommonComponentsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        external_dns: typing.Optional[typing.Union["DefaultCommonComponentsProps", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_ebs_csi_driver: 
        :param aws_efs_csi_driver: 
        :param cluster_autoscaler: 
        :param external_dns: 
        '''
        if isinstance(aws_ebs_csi_driver, dict):
            aws_ebs_csi_driver = DefaultCommonComponentsProps(**aws_ebs_csi_driver)
        if isinstance(aws_efs_csi_driver, dict):
            aws_efs_csi_driver = DefaultCommonComponentsProps(**aws_efs_csi_driver)
        if isinstance(cluster_autoscaler, dict):
            cluster_autoscaler = DefaultCommonComponentsProps(**cluster_autoscaler)
        if isinstance(external_dns, dict):
            external_dns = DefaultCommonComponentsProps(**external_dns)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae95b57888d660638f3368bfcab2375ac90f478fbc634f487a72b89685fb3473)
            check_type(argname="argument aws_ebs_csi_driver", value=aws_ebs_csi_driver, expected_type=type_hints["aws_ebs_csi_driver"])
            check_type(argname="argument aws_efs_csi_driver", value=aws_efs_csi_driver, expected_type=type_hints["aws_efs_csi_driver"])
            check_type(argname="argument cluster_autoscaler", value=cluster_autoscaler, expected_type=type_hints["cluster_autoscaler"])
            check_type(argname="argument external_dns", value=external_dns, expected_type=type_hints["external_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_ebs_csi_driver is not None:
            self._values["aws_ebs_csi_driver"] = aws_ebs_csi_driver
        if aws_efs_csi_driver is not None:
            self._values["aws_efs_csi_driver"] = aws_efs_csi_driver
        if cluster_autoscaler is not None:
            self._values["cluster_autoscaler"] = cluster_autoscaler
        if external_dns is not None:
            self._values["external_dns"] = external_dns

    @builtins.property
    def aws_ebs_csi_driver(self) -> typing.Optional["DefaultCommonComponentsProps"]:
        result = self._values.get("aws_ebs_csi_driver")
        return typing.cast(typing.Optional["DefaultCommonComponentsProps"], result)

    @builtins.property
    def aws_efs_csi_driver(self) -> typing.Optional["DefaultCommonComponentsProps"]:
        result = self._values.get("aws_efs_csi_driver")
        return typing.cast(typing.Optional["DefaultCommonComponentsProps"], result)

    @builtins.property
    def cluster_autoscaler(self) -> typing.Optional["DefaultCommonComponentsProps"]:
        result = self._values.get("cluster_autoscaler")
        return typing.cast(typing.Optional["DefaultCommonComponentsProps"], result)

    @builtins.property
    def external_dns(self) -> typing.Optional["DefaultCommonComponentsProps"]:
        result = self._values.get("external_dns")
        return typing.cast(typing.Optional["DefaultCommonComponentsProps"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultCommonComponents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.DefaultCommonComponentsProps",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace"},
)
class DefaultCommonComponentsProps:
    def __init__(self, *, namespace: typing.Optional[builtins.str] = None) -> None:
        '''
        :param namespace: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448c1b677efed850237975e31bff7ba8d6ef3220069be99b6eeb832336d8bc08)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultCommonComponentsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EKSCluster(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.EKSCluster",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        cluster_config: typing.Union[ClusterConfig, typing.Dict[builtins.str, typing.Any]],
        kms_key: _aws_cdk_aws_kms_ceddda9d.Key,
        region: builtins.str,
        worker_security_group: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
        addon_props: typing.Optional[typing.Union[AddonProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        core_dns_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
        kube_proxy_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cluster_config: 
        :param kms_key: 
        :param region: 
        :param worker_security_group: 
        :param addon_props: 
        :param cluster_vpc: 
        :param core_dns_addon_props: 
        :param kube_proxy_addon_props: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74f2319be73bf0895e6abd907dc8fd0eb276de45e5d8cfc05f17b8c659a3427)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EKSClusterProps(
            availability_zones=availability_zones,
            cluster_config=cluster_config,
            kms_key=kms_key,
            region=region,
            worker_security_group=worker_security_group,
            addon_props=addon_props,
            cluster_vpc=cluster_vpc,
            core_dns_addon_props=core_dns_addon_props,
            kube_proxy_addon_props=kube_proxy_addon_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAccountWithIamRole")
    def add_service_account_with_iam_role(
        self,
        service_account_name: builtins.str,
        service_account_namespace: builtins.str,
        policy: typing.Any,
    ) -> None:
        '''
        :param service_account_name: -
        :param service_account_namespace: -
        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244fcfec11a7cbffd9e4c9bcf2d78de68391815a5785a0723cf09218c4cde98e)
            check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
            check_type(argname="argument service_account_namespace", value=service_account_namespace, expected_type=type_hints["service_account_namespace"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addServiceAccountWithIamRole", [service_account_name, service_account_namespace, policy]))

    @builtins.property
    @jsii.member(jsii_name="additionalFargateProfile")
    def additional_fargate_profile(
        self,
    ) -> typing.List[_aws_cdk_aws_eks_ceddda9d.FargateProfile]:
        return typing.cast(typing.List[_aws_cdk_aws_eks_ceddda9d.FargateProfile], jsii.get(self, "additionalFargateProfile"))

    @builtins.property
    @jsii.member(jsii_name="additionalNodegroups")
    def additional_nodegroups(self) -> typing.List[_aws_cdk_aws_eks_ceddda9d.Nodegroup]:
        return typing.cast(typing.List[_aws_cdk_aws_eks_ceddda9d.Nodegroup], jsii.get(self, "additionalNodegroups"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="fargateProfiles")
    def fargate_profiles(self) -> typing.List["FargateProfile"]:
        return typing.cast(typing.List["FargateProfile"], jsii.get(self, "fargateProfiles"))


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.EKSClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cluster_config": "clusterConfig",
        "kms_key": "kmsKey",
        "region": "region",
        "worker_security_group": "workerSecurityGroup",
        "addon_props": "addonProps",
        "cluster_vpc": "clusterVPC",
        "core_dns_addon_props": "coreDnsAddonProps",
        "kube_proxy_addon_props": "kubeProxyAddonProps",
    },
)
class EKSClusterProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        cluster_config: typing.Union[ClusterConfig, typing.Dict[builtins.str, typing.Any]],
        kms_key: _aws_cdk_aws_kms_ceddda9d.Key,
        region: builtins.str,
        worker_security_group: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
        addon_props: typing.Optional[typing.Union[AddonProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        core_dns_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
        kube_proxy_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param cluster_config: 
        :param kms_key: 
        :param region: 
        :param worker_security_group: 
        :param addon_props: 
        :param cluster_vpc: 
        :param core_dns_addon_props: 
        :param kube_proxy_addon_props: 
        '''
        if isinstance(cluster_config, dict):
            cluster_config = ClusterConfig(**cluster_config)
        if isinstance(addon_props, dict):
            addon_props = AddonProps(**addon_props)
        if isinstance(core_dns_addon_props, dict):
            core_dns_addon_props = CoreAddonValuesProps(**core_dns_addon_props)
        if isinstance(kube_proxy_addon_props, dict):
            kube_proxy_addon_props = CoreAddonValuesProps(**kube_proxy_addon_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bb6b8826502f0eaab304de996086c71bb5400212fb582a3fd42b7ab7425498)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument worker_security_group", value=worker_security_group, expected_type=type_hints["worker_security_group"])
            check_type(argname="argument addon_props", value=addon_props, expected_type=type_hints["addon_props"])
            check_type(argname="argument cluster_vpc", value=cluster_vpc, expected_type=type_hints["cluster_vpc"])
            check_type(argname="argument core_dns_addon_props", value=core_dns_addon_props, expected_type=type_hints["core_dns_addon_props"])
            check_type(argname="argument kube_proxy_addon_props", value=kube_proxy_addon_props, expected_type=type_hints["kube_proxy_addon_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
            "cluster_config": cluster_config,
            "kms_key": kms_key,
            "region": region,
            "worker_security_group": worker_security_group,
        }
        if addon_props is not None:
            self._values["addon_props"] = addon_props
        if cluster_vpc is not None:
            self._values["cluster_vpc"] = cluster_vpc
        if core_dns_addon_props is not None:
            self._values["core_dns_addon_props"] = core_dns_addon_props
        if kube_proxy_addon_props is not None:
            self._values["kube_proxy_addon_props"] = kube_proxy_addon_props

    @builtins.property
    def availability_zones(self) -> typing.List[builtins.str]:
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cluster_config(self) -> ClusterConfig:
        result = self._values.get("cluster_config")
        assert result is not None, "Required property 'cluster_config' is missing"
        return typing.cast(ClusterConfig, result)

    @builtins.property
    def kms_key(self) -> _aws_cdk_aws_kms_ceddda9d.Key:
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.Key, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def worker_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.SecurityGroup:
        result = self._values.get("worker_security_group")
        assert result is not None, "Required property 'worker_security_group' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SecurityGroup, result)

    @builtins.property
    def addon_props(self) -> typing.Optional[AddonProps]:
        result = self._values.get("addon_props")
        return typing.cast(typing.Optional[AddonProps], result)

    @builtins.property
    def cluster_vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        result = self._values.get("cluster_vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def core_dns_addon_props(self) -> typing.Optional[CoreAddonValuesProps]:
        result = self._values.get("core_dns_addon_props")
        return typing.cast(typing.Optional[CoreAddonValuesProps], result)

    @builtins.property
    def kube_proxy_addon_props(self) -> typing.Optional[CoreAddonValuesProps]:
        result = self._values.get("kube_proxy_addon_props")
        return typing.cast(typing.Optional[CoreAddonValuesProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EKSClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.FargateProfile",
    jsii_struct_bases=[],
    name_mapping={
        "namespaces": "namespaces",
        "profile_name": "profileName",
        "labels": "labels",
        "pod_execution_role": "podExecutionRole",
        "subnet_selection": "subnetSelection",
    },
)
class FargateProfile:
    def __init__(
        self,
        *,
        namespaces: typing.Sequence[builtins.str],
        profile_name: builtins.str,
        labels: typing.Optional[typing.Union["InternalMap", typing.Dict[builtins.str, typing.Any]]] = None,
        pod_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param namespaces: 
        :param profile_name: 
        :param labels: 
        :param pod_execution_role: 
        :param subnet_selection: 
        '''
        if isinstance(labels, dict):
            labels = InternalMap(**labels)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2aa023d6c22a5b4811103a56b0122737def3e78a6261b5adfeb71277b65caa)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument pod_execution_role", value=pod_execution_role, expected_type=type_hints["pod_execution_role"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
            "profile_name": profile_name,
        }
        if labels is not None:
            self._values["labels"] = labels
        if pod_execution_role is not None:
            self._values["pod_execution_role"] = pod_execution_role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def labels(self) -> typing.Optional["InternalMap"]:
        result = self._values.get("labels")
        return typing.cast(typing.Optional["InternalMap"], result)

    @builtins.property
    def pod_execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        result = self._values.get("pod_execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@smallcase/cdk-eks-cluster-module.ICommonComponentsProps")
class ICommonComponentsProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="helm")
    def helm(self) -> "StandardHelmProps":
        ...

    @helm.setter
    def helm(self, value: "StandardHelmProps") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="iamPolicyPath")
    def iam_policy_path(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @iam_policy_path.setter
    def iam_policy_path(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceAccounts")
    def service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @service_accounts.setter
    def service_accounts(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...


class _ICommonComponentsPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-eks-cluster-module.ICommonComponentsProps"

    @builtins.property
    @jsii.member(jsii_name="helm")
    def helm(self) -> "StandardHelmProps":
        return typing.cast("StandardHelmProps", jsii.get(self, "helm"))

    @helm.setter
    def helm(self, value: "StandardHelmProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f30dd012cd799cde218018d5ac5706eac5adce13495e65c6dc46c8a4fcb5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamPolicyPath")
    def iam_policy_path(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "iamPolicyPath"))

    @iam_policy_path.setter
    def iam_policy_path(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a348f9308028e9e1436c35c37d05c057373d0b3b77ce199c1b5ebcdf009c3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPolicyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccounts")
    def service_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccounts"))

    @service_accounts.setter
    def service_accounts(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e601a2297c8ff073256ab6c92c0224f63ca2328055f26df8d78e7465b0fdbb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccounts", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICommonComponentsProps).__jsii_proxy_class__ = lambda : _ICommonComponentsPropsProxy


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.InternalMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class InternalMap:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubeProxyAddon(
    _aws_cdk_aws_eks_ceddda9d.CfnAddon,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.KubeProxyAddon",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        addon_version: typing.Optional[builtins.str] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resolve_conflicts: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param addon_version: 
        :param configuration_values: 
        :param namespace: 
        :param resolve_conflicts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a281cc1dc224b6872395a5c6de175b4662a1dae93699fa1c33a981dff90d916)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CoreAddonProps(
            cluster=cluster,
            addon_version=addon_version,
            configuration_values=configuration_values,
            namespace=namespace,
            resolve_conflicts=resolve_conflicts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.NamespaceSpec",
    jsii_struct_bases=[],
    name_mapping={"annotations": "annotations", "labels": "labels"},
)
class NamespaceSpec:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: 
        :param labels: 
        '''
        if isinstance(annotations, dict):
            annotations = InternalMap(**annotations)
        if isinstance(labels, dict):
            labels = InternalMap(**labels)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5530f023665184696cad3b8f145b7aa7ff1f4e533ca42351cde627a4d7af2be4)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def annotations(self) -> typing.Optional[InternalMap]:
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[InternalMap], result)

    @builtins.property
    def labels(self) -> typing.Optional[InternalMap]:
        result = self._values.get("labels")
        return typing.cast(typing.Optional[InternalMap], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamespaceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.NodeGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_types": "instanceTypes",
        "labels": "labels",
        "max_size": "maxSize",
        "min_size": "minSize",
        "name": "name",
        "subnet_group_name": "subnetGroupName",
        "taints": "taints",
        "capacity_type": "capacityType",
        "desired_size": "desiredSize",
        "disk_size": "diskSize",
        "launch_template_spec": "launchTemplateSpec",
        "node_ami_version": "nodeAMIVersion",
        "ssh_key_name": "sshKeyName",
        "subnet_az": "subnetAz",
        "tags": "tags",
    },
)
class NodeGroupConfig:
    def __init__(
        self,
        *,
        instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
        labels: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
        max_size: jsii.Number,
        min_size: jsii.Number,
        name: builtins.str,
        subnet_group_name: builtins.str,
        taints: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
        capacity_type: typing.Optional[_aws_cdk_aws_eks_ceddda9d.CapacityType] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        launch_template_spec: typing.Optional[typing.Union[_aws_cdk_aws_eks_ceddda9d.LaunchTemplateSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        node_ami_version: typing.Optional[builtins.str] = None,
        ssh_key_name: typing.Optional[builtins.str] = None,
        subnet_az: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param instance_types: 
        :param labels: 
        :param max_size: 
        :param min_size: 
        :param name: 
        :param subnet_group_name: 
        :param taints: 
        :param capacity_type: 
        :param desired_size: 
        :param disk_size: 
        :param launch_template_spec: 
        :param node_ami_version: 
        :param ssh_key_name: 
        :param subnet_az: 
        :param tags: 
        '''
        if isinstance(labels, dict):
            labels = InternalMap(**labels)
        if isinstance(taints, dict):
            taints = InternalMap(**taints)
        if isinstance(launch_template_spec, dict):
            launch_template_spec = _aws_cdk_aws_eks_ceddda9d.LaunchTemplateSpec(**launch_template_spec)
        if isinstance(tags, dict):
            tags = InternalMap(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22726f264b432d7e021c4a10f26a39372a162c8521587a3237724adacc23634)
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument capacity_type", value=capacity_type, expected_type=type_hints["capacity_type"])
            check_type(argname="argument desired_size", value=desired_size, expected_type=type_hints["desired_size"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument launch_template_spec", value=launch_template_spec, expected_type=type_hints["launch_template_spec"])
            check_type(argname="argument node_ami_version", value=node_ami_version, expected_type=type_hints["node_ami_version"])
            check_type(argname="argument ssh_key_name", value=ssh_key_name, expected_type=type_hints["ssh_key_name"])
            check_type(argname="argument subnet_az", value=subnet_az, expected_type=type_hints["subnet_az"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_types": instance_types,
            "labels": labels,
            "max_size": max_size,
            "min_size": min_size,
            "name": name,
            "subnet_group_name": subnet_group_name,
            "taints": taints,
        }
        if capacity_type is not None:
            self._values["capacity_type"] = capacity_type
        if desired_size is not None:
            self._values["desired_size"] = desired_size
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if launch_template_spec is not None:
            self._values["launch_template_spec"] = launch_template_spec
        if node_ami_version is not None:
            self._values["node_ami_version"] = node_ami_version
        if ssh_key_name is not None:
            self._values["ssh_key_name"] = ssh_key_name
        if subnet_az is not None:
            self._values["subnet_az"] = subnet_az
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        result = self._values.get("instance_types")
        assert result is not None, "Required property 'instance_types' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def labels(self) -> InternalMap:
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(InternalMap, result)

    @builtins.property
    def max_size(self) -> jsii.Number:
        result = self._values.get("max_size")
        assert result is not None, "Required property 'max_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_size(self) -> jsii.Number:
        result = self._values.get("min_size")
        assert result is not None, "Required property 'min_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_group_name(self) -> builtins.str:
        result = self._values.get("subnet_group_name")
        assert result is not None, "Required property 'subnet_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def taints(self) -> InternalMap:
        result = self._values.get("taints")
        assert result is not None, "Required property 'taints' is missing"
        return typing.cast(InternalMap, result)

    @builtins.property
    def capacity_type(self) -> typing.Optional[_aws_cdk_aws_eks_ceddda9d.CapacityType]:
        result = self._values.get("capacity_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_eks_ceddda9d.CapacityType], result)

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("desired_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def launch_template_spec(
        self,
    ) -> typing.Optional[_aws_cdk_aws_eks_ceddda9d.LaunchTemplateSpec]:
        result = self._values.get("launch_template_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_eks_ceddda9d.LaunchTemplateSpec], result)

    @builtins.property
    def node_ami_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("node_ami_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_key_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("ssh_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_az(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("subnet_az")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[InternalMap]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[InternalMap], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.StandardHelmProps",
    jsii_struct_bases=[],
    name_mapping={
        "chart_name": "chartName",
        "chart_release_name": "chartReleaseName",
        "chart_version": "chartVersion",
        "create_namespace": "createNamespace",
        "helm_repository": "helmRepository",
        "helm_values": "helmValues",
        "local_helm_chart": "localHelmChart",
        "namespace": "namespace",
    },
)
class StandardHelmProps:
    def __init__(
        self,
        *,
        chart_name: builtins.str,
        chart_release_name: typing.Optional[builtins.str] = None,
        chart_version: typing.Optional[builtins.str] = None,
        create_namespace: typing.Optional[builtins.bool] = None,
        helm_repository: typing.Optional[builtins.str] = None,
        helm_values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        local_helm_chart: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param chart_name: 
        :param chart_release_name: 
        :param chart_version: 
        :param create_namespace: 
        :param helm_repository: 
        :param helm_values: 
        :param local_helm_chart: 
        :param namespace: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a7a877fff3503e1d8fc6b4a60abbf452f538d3baa288a634fd82fd5748159d)
            check_type(argname="argument chart_name", value=chart_name, expected_type=type_hints["chart_name"])
            check_type(argname="argument chart_release_name", value=chart_release_name, expected_type=type_hints["chart_release_name"])
            check_type(argname="argument chart_version", value=chart_version, expected_type=type_hints["chart_version"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument helm_repository", value=helm_repository, expected_type=type_hints["helm_repository"])
            check_type(argname="argument helm_values", value=helm_values, expected_type=type_hints["helm_values"])
            check_type(argname="argument local_helm_chart", value=local_helm_chart, expected_type=type_hints["local_helm_chart"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chart_name": chart_name,
        }
        if chart_release_name is not None:
            self._values["chart_release_name"] = chart_release_name
        if chart_version is not None:
            self._values["chart_version"] = chart_version
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if helm_repository is not None:
            self._values["helm_repository"] = helm_repository
        if helm_values is not None:
            self._values["helm_values"] = helm_values
        if local_helm_chart is not None:
            self._values["local_helm_chart"] = local_helm_chart
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def chart_name(self) -> builtins.str:
        result = self._values.get("chart_name")
        assert result is not None, "Required property 'chart_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def chart_release_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("chart_release_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def chart_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("chart_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def helm_repository(self) -> typing.Optional[builtins.str]:
        result = self._values.get("helm_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def helm_values(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("helm_values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def local_helm_chart(self) -> typing.Optional[builtins.str]:
        result = self._values.get("local_helm_chart")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardHelmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-eks-cluster-module.VpcCniAddonProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "addon_version": "addonVersion",
        "configuration_values": "configurationValues",
        "namespace": "namespace",
        "resolve_conflicts": "resolveConflicts",
    },
)
class VpcCniAddonProps:
    def __init__(
        self,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        addon_version: typing.Optional["VpcCniAddonVersion"] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resolve_conflicts: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param cluster: 
        :param addon_version: 
        :param configuration_values: 
        :param namespace: 
        :param resolve_conflicts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25310b0aed0637db1536c6cffbed91e061449be1c988ea226df47859148e2916)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument resolve_conflicts", value=resolve_conflicts, expected_type=type_hints["resolve_conflicts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
        }
        if addon_version is not None:
            self._values["addon_version"] = addon_version
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values
        if namespace is not None:
            self._values["namespace"] = namespace
        if resolve_conflicts is not None:
            self._values["resolve_conflicts"] = resolve_conflicts

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, result)

    @builtins.property
    def addon_version(self) -> typing.Optional["VpcCniAddonVersion"]:
        result = self._values.get("addon_version")
        return typing.cast(typing.Optional["VpcCniAddonVersion"], result)

    @builtins.property
    def configuration_values(self) -> typing.Optional[builtins.str]:
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolve_conflicts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("resolve_conflicts")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcCniAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcCniAddonVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.VpcCniAddonVersion",
):
    def __init__(self, version: builtins.str) -> None:
        '''
        :param version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e0c0a934e32178e6598cce1932bf626d0e0021d4719647ac88d3dde4d74180)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        jsii.create(self.__class__, self, [version])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "VpcCniAddonVersion":
        '''Custom add-on version.

        :param version: custom add-on version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc831d7596d953cbda7bbeb70cc00d578a184570fe5d6fff2dd7f744cff47fb)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("VpcCniAddonVersion", jsii.sinvoke(cls, "of", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_10_1")
    def V1_10_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.10.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_10_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_10_2")
    def V1_10_2(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.10.2.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_10_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_10_3")
    def V1_10_3(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.10.3.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_10_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_11_0")
    def V1_11_0(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.11.0.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_11_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_11_2")
    def V1_11_2(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.11.2.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_11_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_11_3")
    def V1_11_3(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.11.3.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_11_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_11_4")
    def V1_11_4(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.11.4.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_11_4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_12_0")
    def V1_12_0(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.12.0.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_12_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_12_1")
    def V1_12_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.12.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_12_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_12_2")
    def V1_12_2(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.12.2.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_12_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_12_5")
    def V1_12_5(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.12.5.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_12_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_12_5_2")
    def V1_12_5_2(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.12.5.2.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_12_5_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_17_1_1")
    def V1_17_1_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.17.1.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_17_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_18_6_1")
    def V1_18_6_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.18.6.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_18_6_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_19_0_1")
    def V1_19_0_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.19.0.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_19_0_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_19_2_1")
    def V1_19_2_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.19.2.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_19_2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_19_2_5")
    def V1_19_2_5(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.19.2.5.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_19_2_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_19_3_1")
    def V1_19_3_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.19.3.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_19_3_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_19_5_3")
    def V1_19_5_3(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.19.5.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_19_5_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_6_3")
    def V1_6_3(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.6.3.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_6_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_10")
    def V1_7_10(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.7.10.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_7_10"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_5")
    def V1_7_5(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.7.5.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_7_5"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_6")
    def V1_7_6(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.7.6.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_7_6"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_9")
    def V1_7_9(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.7.9.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_7_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_8_0")
    def V1_8_0(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.8.0.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_8_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_9_0")
    def V1_9_0(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.9.0.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_9_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_9_1")
    def V1_9_1(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.9.1.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_9_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_9_3")
    def V1_9_3(cls) -> "VpcCniAddonVersion":
        '''vpc-cni version 1.9.3.'''
        return typing.cast("VpcCniAddonVersion", jsii.sget(cls, "V1_9_3"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))


class VpcEniAddon(
    _aws_cdk_aws_eks_ceddda9d.CfnAddon,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-eks-cluster-module.VpcEniAddon",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        addon_version: typing.Optional[VpcCniAddonVersion] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        resolve_conflicts: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param addon_version: 
        :param configuration_values: 
        :param namespace: 
        :param resolve_conflicts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42778f18b9fbda23a24fb044e3a423d682c90887996f32ed2ca664961bd653f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcCniAddonProps(
            cluster=cluster,
            addon_version=addon_version,
            configuration_values=configuration_values,
            namespace=namespace,
            resolve_conflicts=resolve_conflicts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "AddonProps",
    "ArgoCD",
    "ClusterConfig",
    "CommonHelmCharts",
    "CommonHelmChartsProps",
    "CoreAddonProps",
    "CoreAddonValuesProps",
    "CoreDnsAddon",
    "DefaultCommonComponents",
    "DefaultCommonComponentsProps",
    "EKSCluster",
    "EKSClusterProps",
    "FargateProfile",
    "ICommonComponentsProps",
    "InternalMap",
    "KubeProxyAddon",
    "NamespaceSpec",
    "NodeGroupConfig",
    "StandardHelmProps",
    "VpcCniAddonProps",
    "VpcCniAddonVersion",
    "VpcEniAddon",
]

publication.publish()

def _typecheckingstub__9975c31b067437c657a3f94425cf31b29dcc29137d03fecb2e866ad248fbb6b8(
    *,
    configuration_values: typing.Optional[builtins.str] = None,
    vpn_cni_addon_version: typing.Optional[VpcCniAddonVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a96e07b960fdc73800c6c39016a3ff7b72083a7af299c0ccef5e493ff9060d0(
    *,
    assume_role_arn: builtins.str,
    cluster_role_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790140b15ea89389baac9354004284c53266f60c5ab92c244d71af13dd772e5e(
    *,
    cluster_name: builtins.str,
    cluster_version: _aws_cdk_aws_eks_ceddda9d.KubernetesVersion,
    default_capacity: jsii.Number,
    node_groups: typing.Sequence[typing.Union[NodeGroupConfig, typing.Dict[builtins.str, typing.Any]]],
    subnets: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
    tags: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
    team_members: typing.Sequence[builtins.str],
    add_autoscaler_iam: typing.Optional[builtins.bool] = None,
    alb_controller_version: typing.Optional[_aws_cdk_aws_eks_ceddda9d.AlbControllerVersion] = None,
    argo_cd: typing.Optional[typing.Union[ArgoCD, typing.Dict[builtins.str, typing.Any]]] = None,
    common_components: typing.Optional[typing.Mapping[builtins.str, ICommonComponentsProps]] = None,
    debug_logs: typing.Optional[builtins.bool] = None,
    default_common_components: typing.Optional[typing.Union[DefaultCommonComponents, typing.Dict[builtins.str, typing.Any]]] = None,
    deprecate_cluster_auto_scaler: typing.Optional[builtins.bool] = None,
    fargate_profiles: typing.Optional[typing.Sequence[typing.Union[FargateProfile, typing.Dict[builtins.str, typing.Any]]]] = None,
    kubectl_layer: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion] = None,
    namespaces: typing.Optional[typing.Mapping[builtins.str, typing.Union[NamespaceSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_allow_access: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_external_dns: typing.Optional[builtins.bool] = None,
    team_existing_role_permission: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5404c69b77f40af5bbafd8659f90a5fea8699752ead3071d1922a0bf7c5466(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
    helm_props: typing.Union[StandardHelmProps, typing.Dict[builtins.str, typing.Any]],
    dependent_namespaces: typing.Optional[typing.Sequence[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]] = None,
    iam_policy_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_charts: typing.Optional[builtins.bool] = None,
    service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab74f17dea60f0a28aedf5f616fe27bb0b4691796b641bfd375294bc66c1416a(
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
    helm_props: typing.Union[StandardHelmProps, typing.Dict[builtins.str, typing.Any]],
    dependent_namespaces: typing.Optional[typing.Sequence[_aws_cdk_aws_eks_ceddda9d.KubernetesManifest]] = None,
    iam_policy_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_charts: typing.Optional[builtins.bool] = None,
    service_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f74064bc618ba94d9f9df56e3c897a47a160945504e0c88228c2c8f12ed3ae4(
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    addon_version: typing.Optional[builtins.str] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resolve_conflicts: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e12355f4b84b8449c52f3fc2b5c257b35c96dd52f870f39e67c6efc6b89beea(
    *,
    addon_version: typing.Optional[builtins.str] = None,
    configuration_values: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e171c7882ef3806f1271b18a97a551178f47e6bac56547d01c9ab3c32b6a95b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    addon_version: typing.Optional[builtins.str] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resolve_conflicts: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae95b57888d660638f3368bfcab2375ac90f478fbc634f487a72b89685fb3473(
    *,
    aws_ebs_csi_driver: typing.Optional[typing.Union[DefaultCommonComponentsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_efs_csi_driver: typing.Optional[typing.Union[DefaultCommonComponentsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_autoscaler: typing.Optional[typing.Union[DefaultCommonComponentsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    external_dns: typing.Optional[typing.Union[DefaultCommonComponentsProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448c1b677efed850237975e31bff7ba8d6ef3220069be99b6eeb832336d8bc08(
    *,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74f2319be73bf0895e6abd907dc8fd0eb276de45e5d8cfc05f17b8c659a3427(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zones: typing.Sequence[builtins.str],
    cluster_config: typing.Union[ClusterConfig, typing.Dict[builtins.str, typing.Any]],
    kms_key: _aws_cdk_aws_kms_ceddda9d.Key,
    region: builtins.str,
    worker_security_group: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    addon_props: typing.Optional[typing.Union[AddonProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    core_dns_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    kube_proxy_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244fcfec11a7cbffd9e4c9bcf2d78de68391815a5785a0723cf09218c4cde98e(
    service_account_name: builtins.str,
    service_account_namespace: builtins.str,
    policy: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bb6b8826502f0eaab304de996086c71bb5400212fb582a3fd42b7ab7425498(
    *,
    availability_zones: typing.Sequence[builtins.str],
    cluster_config: typing.Union[ClusterConfig, typing.Dict[builtins.str, typing.Any]],
    kms_key: _aws_cdk_aws_kms_ceddda9d.Key,
    region: builtins.str,
    worker_security_group: _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    addon_props: typing.Optional[typing.Union[AddonProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    core_dns_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    kube_proxy_addon_props: typing.Optional[typing.Union[CoreAddonValuesProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2aa023d6c22a5b4811103a56b0122737def3e78a6261b5adfeb71277b65caa(
    *,
    namespaces: typing.Sequence[builtins.str],
    profile_name: builtins.str,
    labels: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
    pod_execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f30dd012cd799cde218018d5ac5706eac5adce13495e65c6dc46c8a4fcb5ad(
    value: StandardHelmProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a348f9308028e9e1436c35c37d05c057373d0b3b77ce199c1b5ebcdf009c3ad(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e601a2297c8ff073256ab6c92c0224f63ca2328055f26df8d78e7465b0fdbb0c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a281cc1dc224b6872395a5c6de175b4662a1dae93699fa1c33a981dff90d916(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    addon_version: typing.Optional[builtins.str] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resolve_conflicts: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5530f023665184696cad3b8f145b7aa7ff1f4e533ca42351cde627a4d7af2be4(
    *,
    annotations: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22726f264b432d7e021c4a10f26a39372a162c8521587a3237724adacc23634(
    *,
    instance_types: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType],
    labels: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
    max_size: jsii.Number,
    min_size: jsii.Number,
    name: builtins.str,
    subnet_group_name: builtins.str,
    taints: typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]],
    capacity_type: typing.Optional[_aws_cdk_aws_eks_ceddda9d.CapacityType] = None,
    desired_size: typing.Optional[jsii.Number] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    launch_template_spec: typing.Optional[typing.Union[_aws_cdk_aws_eks_ceddda9d.LaunchTemplateSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    node_ami_version: typing.Optional[builtins.str] = None,
    ssh_key_name: typing.Optional[builtins.str] = None,
    subnet_az: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Union[InternalMap, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a7a877fff3503e1d8fc6b4a60abbf452f538d3baa288a634fd82fd5748159d(
    *,
    chart_name: builtins.str,
    chart_release_name: typing.Optional[builtins.str] = None,
    chart_version: typing.Optional[builtins.str] = None,
    create_namespace: typing.Optional[builtins.bool] = None,
    helm_repository: typing.Optional[builtins.str] = None,
    helm_values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    local_helm_chart: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25310b0aed0637db1536c6cffbed91e061449be1c988ea226df47859148e2916(
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    addon_version: typing.Optional[VpcCniAddonVersion] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resolve_conflicts: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e0c0a934e32178e6598cce1932bf626d0e0021d4719647ac88d3dde4d74180(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc831d7596d953cbda7bbeb70cc00d578a184570fe5d6fff2dd7f744cff47fb(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42778f18b9fbda23a24fb044e3a423d682c90887996f32ed2ca664961bd653f6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    addon_version: typing.Optional[VpcCniAddonVersion] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    resolve_conflicts: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
