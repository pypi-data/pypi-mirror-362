'''
# NightyNight and WakeyWakey!

Do you have a EC2 instance or an RDS instance that you only need during certain hours of the day? Do you want to reduce it's cost? How about just stopping it every night?

That's the NightyNight construct. It's very simple. Give it an `instanceId` and it will create a Lambda and a CloudWatch Event Rule to fire the lambda at a specific time of day. If the instance is running, it's stopped.

There are currently two variations of the construct:

* [NightyNightForEc2](./API.md#matthewbonig-nightynight-nightynightforec2) - stops an EC2 instance at a given time.
* [NightyNightForRds](./API.md#matthewbonig-nightynight-nightynightforrds) - stops an RDS instance at a given time.
* [NightyNightForAsg](./API.md#matthewbonig-nightynight-nightynightforasg) - sets the desired capacity for an ASG at a given time.
* [NightyNightForEcs](./API.md#matthewbonig-nightynight-nightynightforecs) - sets the desired capacity for an ECS service at a given time.

# WakeyWakey

The WakeyWakey construct (from [this](https://github.com/mbonig/wakeywakey) repository) has been integrated into this library. You don't need to install
a separate dependency anymore.

* [WakeyWakeyForEc2](./API.md#matthewbonig-nightynight-wakeywakeyforec2) - start an EC2 instance at a given time.
* [WakeyWakeyForRds](./API.md#matthewbonig-nightynight-wakeywakeyforrds) - start an RDS instance at a given time.

There isn't a specific construct for starting ASGs or ECS services, since you can just set the count to whatever you want.

# This is a pre-release!

This is a quick first-draft. All the options that will likely need to be added to accommodate a large
number of use-cases are still needed. If you'd like to make requests or help update this construct, please
open an [Issue](https://github.com/mbonig/nightynight/issues) or a [PR](https://github.com/mbonig/cicd-spa-website/pulls).

There are multiple versions of this library published. You should be using the v0.X.X versions for now.
There are versions published that match the CDK version they depend on, but don't use those.

# What it creates

![arch.png](./arch.png)

* A Rule that will, on a given schedule, fire a lambda.
* A Lambda with permissions to describe ec2 instances. It will read the instance by the given `instanceId` and then stop the instance if it's in a running state.

# Example:

```python
import {NightyNightForEc2, WakeyWakeyForEc2} from "./ec2";

export class NightyNightStack extends Stack {

  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new NightyNightForEc2(this, 'nighty-night', {instanceId: 'i-123123123123'});
    new WakeyWakeyForEc2(this, 'wakey-wakey', {instanceId: 'i-123123123123'})
  }
}
```

This will stop the instance with id `i-123123123123` at (the default) 4am UTC. It will then start the instance at 12am UTC.

# API Doc

See the [API Docs](./API.md) for more info.

## Contributing

Please open Pull Requests and Issues on the [Github Repo](https://github.com/mbonig/nightynight).

## License

MIT
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

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import constructs as _constructs_77d1e7e8


class NightyNightForAsg(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForAsg",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will set the given ASG's desired capacity.

    Typically used when you've got and ASG that you can scale during set hours.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        auto_scaling_group: _aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup,
        desired_capacity: jsii.Number,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param auto_scaling_group: the AutoScalingGroup you'd like to change the instance count on.
        :param desired_capacity: Desired capacity.
        :param schedule: An option CronOptions to specify the time of day to scale. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc4279edc9d2659436b5924b051f8d9a546fafb1d1a95b1d4350e892f6c1e3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NightyNightForAsgProps(
            auto_scaling_group=auto_scaling_group,
            desired_capacity=desired_capacity,
            schedule=schedule,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForAsgProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group": "autoScalingGroup",
        "desired_capacity": "desiredCapacity",
        "schedule": "schedule",
    },
)
class NightyNightForAsgProps:
    def __init__(
        self,
        *,
        auto_scaling_group: _aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup,
        desired_capacity: jsii.Number,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param auto_scaling_group: the AutoScalingGroup you'd like to change the instance count on.
        :param desired_capacity: Desired capacity.
        :param schedule: An option CronOptions to specify the time of day to scale. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901110fb62ac30566c23400732c2629c4272ea5d6a18cfcbffb3965b67854f81)
            check_type(argname="argument auto_scaling_group", value=auto_scaling_group, expected_type=type_hints["auto_scaling_group"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling_group": auto_scaling_group,
            "desired_capacity": desired_capacity,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def auto_scaling_group(self) -> _aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup:
        '''the AutoScalingGroup you'd like to change the instance count on.'''
        result = self._values.get("auto_scaling_group")
        assert result is not None, "Required property 'auto_scaling_group' is missing"
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup, result)

    @builtins.property
    def desired_capacity(self) -> jsii.Number:
        '''Desired capacity.'''
        result = self._values.get("desired_capacity")
        assert result is not None, "Required property 'desired_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to scale.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForAsgProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNightForEc2(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForEc2",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will stop the given ec2 instance at the specified time.

    Typically used when you've got ec2 instances that you only need during business hours
    and want to reduce the costs of.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like stopped. Must provide this if tags is not provided.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00ff22036ebef4c454a5291935a87db57320688efd7e2c3f7724c1878640f4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NightyNightForEc2Props(
            filters=filters, instance_id=instance_id, schedule=schedule
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForEc2Props",
    jsii_struct_bases=[],
    name_mapping={
        "filters": "filters",
        "instance_id": "instanceId",
        "schedule": "schedule",
    },
)
class NightyNightForEc2Props:
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like stopped. Must provide this if tags is not provided.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05feb9e09cc42251beb394574960ae1b5d9dced14392ea964411e775f79cb211)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Filters to match to find an EC2 instance.

        Must provide this if instanceId is not provided. If instanceId is provided this
        is ignored.
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''the instanceId of the EC2 instance you'd like stopped.

        Must provide this if tags is not provided.
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForEc2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNightForEcs(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForEcs",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will set the given ECS Service's desired capacity.

    Typically, used when you've got an ECS Service that you can scale during set hours.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        desired_capacity: jsii.Number,
        service_name: builtins.str,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param desired_capacity: Desired capacity.
        :param service_name: The service name to update.
        :param cluster: The ECS Cluster where the service resides. Default: 'default'
        :param schedule: An option CronOptions to specify the time of day to scale. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecfdcec6088dc8af879950e65d90e5b10999ced682bbe4550dca8d08cb49cc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NightyNightForEcsProps(
            desired_capacity=desired_capacity,
            service_name=service_name,
            cluster=cluster,
            schedule=schedule,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForEcsProps",
    jsii_struct_bases=[],
    name_mapping={
        "desired_capacity": "desiredCapacity",
        "service_name": "serviceName",
        "cluster": "cluster",
        "schedule": "schedule",
    },
)
class NightyNightForEcsProps:
    def __init__(
        self,
        *,
        desired_capacity: jsii.Number,
        service_name: builtins.str,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param desired_capacity: Desired capacity.
        :param service_name: The service name to update.
        :param cluster: The ECS Cluster where the service resides. Default: 'default'
        :param schedule: An option CronOptions to specify the time of day to scale. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb47b36ac6806c92ed8be2ab923cc6699a9b56cfebb7dbb2d6adcc329e5a569a)
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "desired_capacity": desired_capacity,
            "service_name": service_name,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def desired_capacity(self) -> jsii.Number:
        '''Desired capacity.'''
        result = self._values.get("desired_capacity")
        assert result is not None, "Required property 'desired_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''The service name to update.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster]:
        '''The ECS Cluster where the service resides.

        :default: 'default'
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to scale.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForEcsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNightForRds(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNightForRds",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will stop the given rds instance at the specified time.

    Typically used when you've got rds instances that you only need during business hours
    and want to reduce the costs of.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c264f0d27b48ffcc4726b5729219df130c4d63337b84ac9cdf1fe08a3f3b424b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NightyNightForRdsProps(
            db_instance_identifier=db_instance_identifier, schedule=schedule
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightForRdsProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_instance_identifier": "dbInstanceIdentifier",
        "schedule": "schedule",
    },
)
class NightyNightForRdsProps:
    def __init__(
        self,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for the NightNight construct.

        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a77345a54438d8d49011f5378163b45a45f690036e755ba5d147ccda68bd02)
            check_type(argname="argument db_instance_identifier", value=db_instance_identifier, expected_type=type_hints["db_instance_identifier"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_instance_identifier": db_instance_identifier,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def db_instance_identifier(self) -> builtins.str:
        '''the DBInstanceIdentifier of the RDS instance you'd like stopped.'''
        result = self._values.get("db_instance_identifier")
        assert result is not None, "Required property 'db_instance_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightForRdsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightProps",
    jsii_struct_bases=[NightyNightForEc2Props],
    name_mapping={
        "filters": "filters",
        "instance_id": "instanceId",
        "schedule": "schedule",
    },
)
class NightyNightProps(NightyNightForEc2Props):
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like stopped. Must provide this if tags is not provided.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0ab75614c71e0657ec494be96c733ceec5ca212e5435e16b96bf6d2e919d1b)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Filters to match to find an EC2 instance.

        Must provide this if instanceId is not provided. If instanceId is provided this
        is ignored.
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''the instanceId of the EC2 instance you'd like stopped.

        Must provide this if tags is not provided.
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to stop the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WakeyWakeyForEc2(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.WakeyWakeyForEc2",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will start the given ec2 instance at the specified time.

    Typically used when you've got ec2 instances that you only need during business hours
    and want to reduce the costs of. Use in conjunction with the Nightynight construct at

    :matthewbonig: /nightynight
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like started. If instanceId is provided the filters is ignored.
        :param schedule: An option CronOptions to specify the time of day to start the instance. Default: { day: '*', hour: '12', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbe6cddf9747481bf61b93835f76ec4b1be68dd0ec5be56e5fee2f3e8665718)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WakeyWakeyForEc2Props(
            filters=filters, instance_id=instance_id, schedule=schedule
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.WakeyWakeyForEc2Props",
    jsii_struct_bases=[],
    name_mapping={
        "filters": "filters",
        "instance_id": "instanceId",
        "schedule": "schedule",
    },
)
class WakeyWakeyForEc2Props:
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like started. If instanceId is provided the filters is ignored.
        :param schedule: An option CronOptions to specify the time of day to start the instance. Default: { day: '*', hour: '12', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd1566dcc272ed6921941ea68de4a3a32b4c3a2ca1cf440a0c305dc8d7b108d)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''Filters to match to find an EC2 instance.

        Must provide this if instanceId is not provided. If instanceId is provided this
        is ignored.

        Example::

            [{
            Name: 'STRING_VALUE',
            Values: [
            'STRING_VALUE',
            ]
            }]
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''the instanceId of the EC2 instance you'd like started.

        If instanceId is provided the filters is ignored.
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to start the instance.

        :default:

        {
        day: '*',
        hour: '12',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WakeyWakeyForEc2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WakeyWakeyForRds(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.WakeyWakeyForRds",
):
    '''A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will start the given rds instance at the specified time.

    Typically used when you've got rds instances that you only need during business hours
    and want to reduce the costs of.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like started.
        :param schedule: An option CronOptions to specify the time of day to start the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f09fc765637c289146bdbad55049113eed33f420a9f6abdc8ec723447d1db1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WakeyWakeyForRdsProps(
            db_instance_identifier=db_instance_identifier, schedule=schedule
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.WakeyWakeyForRdsProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_instance_identifier": "dbInstanceIdentifier",
        "schedule": "schedule",
    },
)
class WakeyWakeyForRdsProps:
    def __init__(
        self,
        *,
        db_instance_identifier: builtins.str,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Props for the WakeyWakeyForRds construct.

        :param db_instance_identifier: the DBInstanceIdentifier of the RDS instance you'd like started.
        :param schedule: An option CronOptions to specify the time of day to start the instance. Default: { day: '*', hour: '4', minute: '0' }
        '''
        if isinstance(schedule, dict):
            schedule = _aws_cdk_aws_events_ceddda9d.CronOptions(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a48d59f030f873f7289aa06f6fe7c972e7e429651175ba08262dbb6b84d3e02)
            check_type(argname="argument db_instance_identifier", value=db_instance_identifier, expected_type=type_hints["db_instance_identifier"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_instance_identifier": db_instance_identifier,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def db_instance_identifier(self) -> builtins.str:
        '''the DBInstanceIdentifier of the RDS instance you'd like started.'''
        result = self._values.get("db_instance_identifier")
        assert result is not None, "Required property 'db_instance_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions]:
        '''An option CronOptions to specify the time of day to start the instance.

        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.CronOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WakeyWakeyForRdsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NightyNight(
    NightyNightForEc2,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNight",
):
    '''(deprecated) This class is deprecated, please use NightyNightForEc2.

    :deprecated: in favor of NightyNightForEc2

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param filters: Filters to match to find an EC2 instance. Must provide this if instanceId is not provided. If instanceId is provided this is ignored.
        :param instance_id: the instanceId of the EC2 instance you'd like stopped. Must provide this if tags is not provided.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c1b7d57b09108f98995d37a24b28c0ebb5d29582d9c57ffb289708a9f1aeb6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NightyNightProps(
            filters=filters, instance_id=instance_id, schedule=schedule
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "NightyNight",
    "NightyNightForAsg",
    "NightyNightForAsgProps",
    "NightyNightForEc2",
    "NightyNightForEc2Props",
    "NightyNightForEcs",
    "NightyNightForEcsProps",
    "NightyNightForRds",
    "NightyNightForRdsProps",
    "NightyNightProps",
    "WakeyWakeyForEc2",
    "WakeyWakeyForEc2Props",
    "WakeyWakeyForRds",
    "WakeyWakeyForRdsProps",
]

publication.publish()

def _typecheckingstub__5dc4279edc9d2659436b5924b051f8d9a546fafb1d1a95b1d4350e892f6c1e3c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    auto_scaling_group: _aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup,
    desired_capacity: jsii.Number,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901110fb62ac30566c23400732c2629c4272ea5d6a18cfcbffb3965b67854f81(
    *,
    auto_scaling_group: _aws_cdk_aws_autoscaling_ceddda9d.IAutoScalingGroup,
    desired_capacity: jsii.Number,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00ff22036ebef4c454a5291935a87db57320688efd7e2c3f7724c1878640f4e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05feb9e09cc42251beb394574960ae1b5d9dced14392ea964411e775f79cb211(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecfdcec6088dc8af879950e65d90e5b10999ced682bbe4550dca8d08cb49cc5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    desired_capacity: jsii.Number,
    service_name: builtins.str,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb47b36ac6806c92ed8be2ab923cc6699a9b56cfebb7dbb2d6adcc329e5a569a(
    *,
    desired_capacity: jsii.Number,
    service_name: builtins.str,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c264f0d27b48ffcc4726b5729219df130c4d63337b84ac9cdf1fe08a3f3b424b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db_instance_identifier: builtins.str,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a77345a54438d8d49011f5378163b45a45f690036e755ba5d147ccda68bd02(
    *,
    db_instance_identifier: builtins.str,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0ab75614c71e0657ec494be96c733ceec5ca212e5435e16b96bf6d2e919d1b(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbe6cddf9747481bf61b93835f76ec4b1be68dd0ec5be56e5fee2f3e8665718(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd1566dcc272ed6921941ea68de4a3a32b4c3a2ca1cf440a0c305dc8d7b108d(
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f09fc765637c289146bdbad55049113eed33f420a9f6abdc8ec723447d1db1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    db_instance_identifier: builtins.str,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a48d59f030f873f7289aa06f6fe7c972e7e429651175ba08262dbb6b84d3e02(
    *,
    db_instance_identifier: builtins.str,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c1b7d57b09108f98995d37a24b28c0ebb5d29582d9c57ffb289708a9f1aeb6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.CronOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
