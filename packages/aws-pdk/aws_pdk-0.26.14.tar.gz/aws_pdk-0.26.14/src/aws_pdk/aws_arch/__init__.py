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

from .aws_arch import (
    DrawioAws4ParentShapes as _DrawioAws4ParentShapes_3c51fc93,
    DrawioAwsResourceIconStyleBase as _DrawioAwsResourceIconStyleBase_7d96f13d,
    ParsedAssetKey as _ParsedAssetKey_c2e22d32,
)
from .aws_arch.drawio_spec.aws4 import ShapeNames as _ShapeNames_c7319e7b
from .aws_arch.pricing_manifest import Service as _Service_de1b914e


class AwsArchitecture(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.aws_arch.AwsArchitecture",
):
    '''AwsArchitecture provides an interface for retrieving the inferred normalization between `@aws-cdk/cfnspec <https://github.com/aws/aws-cdk/blob/main/packages/%40aws-cdk/cfnspec>`_ and `AWS Architecture Icons <https://aws.amazon.com/architecture/icons/>`_ systems for all CloudFormation "services" and "resources".'''

    @jsii.member(jsii_name="formatAssetPath")
    @builtins.classmethod
    def format_asset_path(
        cls,
        qualified_asset_key: builtins.str,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Gets formatted asset path including extension and theme.

        :param qualified_asset_key: The qualified asset key (eg: compute/ec2/service_icon, storage/s3/bucket).
        :param format: The format to return (eg: png, svg).
        :param theme: - (Optional) The theme to use, if not specific or now matching asset for the them, the default theme is used.

        :return: Relative asset file path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e12aed85f4b5ad80e1ca8cce0ef4f1cef77aac7f54dc5696e074e095c24bb0)
            check_type(argname="argument qualified_asset_key", value=qualified_asset_key, expected_type=type_hints["qualified_asset_key"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "formatAssetPath", [qualified_asset_key, format, theme]))

    @jsii.member(jsii_name="getCategory")
    @builtins.classmethod
    def get_category(cls, category: builtins.str) -> "AwsCategory":
        '''Get specific category based on id.

        :param category: -

        :see: {@link AwsCategory.getCategory }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be0e69437dbf20f1148d01e1723d0904b527d2a7610a457c044389517fc912d)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
        return typing.cast("AwsCategory", jsii.sinvoke(cls, "getCategory", [category]))

    @jsii.member(jsii_name="getInstanceTypeIcon")
    @builtins.classmethod
    def get_instance_type_icon(
        cls,
        instance_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Get icon for EC2 instance type.

        :param instance_type: - The {@link AwsAsset.InstanceType} to get icon for.
        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a4bd5f7681f00a5db4f9360958b417ae22a2454bcdcad45e8bb804ba8c92cc)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getInstanceTypeIcon", [instance_type, format, theme]))

    @jsii.member(jsii_name="getRdsInstanceTypeIcon")
    @builtins.classmethod
    def get_rds_instance_type_icon(
        cls,
        instance_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
        theme: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Get icon for RDS instance type.

        :param instance_type: - The {@link AwsAsset.RdsInstanceType} to get icon for.
        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736b9d908e5cb23042bbd1614f8decbd48310242a1ab7fde5ccaa26aaea4bc68)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getRdsInstanceTypeIcon", [instance_type, format, theme]))

    @jsii.member(jsii_name="getResource")
    @builtins.classmethod
    def get_resource(cls, cfn_type: builtins.str) -> "AwsResource":
        '''Get resource based on Cfn Resource Type (eg: AWS::S3::Bucket).

        :param cfn_type: -

        :see: {@link AwsResource.getResource }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d523e4408e467c23430be0831cd1bce6021fbd55e0c980bb3a5d0e97ddb697)
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
        return typing.cast("AwsResource", jsii.sinvoke(cls, "getResource", [cfn_type]))

    @jsii.member(jsii_name="getService")
    @builtins.classmethod
    def get_service(cls, identifier: builtins.str) -> "AwsService":
        '''Get specific service based on identifier (eg: S3, AWS::S3, AWS::S3::Bucket).

        :param identifier: -

        :see: {@link AwsSerfice.getService }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16a49f10a18290e7979371bff79c04718d2e30b1f15b42375d343e38c93fe6c)
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
        return typing.cast("AwsService", jsii.sinvoke(cls, "getService", [identifier]))

    @jsii.member(jsii_name="parseAssetPath")
    @builtins.classmethod
    def parse_asset_path(cls, asset_path: builtins.str) -> _ParsedAssetKey_c2e22d32:
        '''Parse assets path into part descriptor.

        :param asset_path: - Absolute or relative asset file path to parse.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62214db900e10c5c6f0aba2c457bdba2afef4a87d41a3e32632b1464d0c495a0)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast(_ParsedAssetKey_c2e22d32, jsii.sinvoke(cls, "parseAssetPath", [asset_path]))

    @jsii.member(jsii_name="resolveAssetPath")
    @builtins.classmethod
    def resolve_asset_path(cls, asset_path: builtins.str) -> builtins.str:
        '''Resolve relative asset path to absolute asset path.

        :param asset_path: - The relative asset path to resolve.

        :return: Absolute asset path

        :throws: Error if asset path is not relative
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e770dfdd6bfb95fb9452c476e677cba8a10512c2964efdde2c91b34173987802)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "resolveAssetPath", [asset_path]))

    @jsii.member(jsii_name="resolveAssetSvgDataUrl")
    @builtins.classmethod
    def resolve_asset_svg_data_url(cls, svg_asset_path: builtins.str) -> builtins.str:
        '''Resolve relative asset path as SVG `Data URL <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs>`_.

        ``data:image/svg+xml;base64,...``

        :param svg_asset_path: - The relative path of svg asset to resolve.

        :return: SVG `Data URL <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs>`_

        :throws: Error if path is not svg
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c95629117e0e7830b6dc50dfbd4ddd91d5a77354952676bea5aa3c6c458c09)
            check_type(argname="argument svg_asset_path", value=svg_asset_path, expected_type=type_hints["svg_asset_path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "resolveAssetSvgDataUrl", [svg_asset_path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="assetDirectory")
    def asset_directory(cls) -> builtins.str:
        '''The absolute directory where `AWS Architecture Icons <https://aws.amazon.com/architecture/icons/>`_ are stored and retrieved.'''
        return typing.cast(builtins.str, jsii.sget(cls, "assetDirectory"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="categories")
    def categories(cls) -> typing.Mapping[builtins.str, "AwsCategory"]:
        '''Get all categories.

        :see: {@link AwsCategory.categories }
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsCategory"], jsii.sget(cls, "categories"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="resources")
    def resources(cls) -> typing.Mapping[builtins.str, "AwsResource"]:
        '''Get all resources.

        :see: {@link AwsResource.resources }
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsResource"], jsii.sget(cls, "resources"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="services")
    def services(cls) -> typing.Mapping[builtins.str, "AwsService"]:
        '''Get all services.

        :see: {@link AwsService.services }
        '''
        return typing.cast(typing.Mapping[builtins.str, "AwsService"], jsii.sget(cls, "services"))


class AwsCategory(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.aws_arch.AwsCategory"):
    '''AwsCategory class provides an interface for normalizing category metadata between mapped systems.'''

    @jsii.member(jsii_name="getCategory")
    @builtins.classmethod
    def get_category(cls, id: builtins.str) -> "AwsCategory":
        '''Get {@link AwsCategory} based on {@link AwsCategoryId}.

        :param id: The id of the category to retrieve.

        :return: Returns the category with the id
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04bc93052b5d28a7387907f2d892d80b7e5d57f79117e9d274bf2c7c9655d4f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("AwsCategory", jsii.sinvoke(cls, "getCategory", [id]))

    @jsii.member(jsii_name="categoryServices")
    def category_services(self) -> typing.List["AwsService"]:
        '''Gets a list of all services within this category.'''
        return typing.cast(typing.List["AwsService"], jsii.invoke(self, "categoryServices", []))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Retrieves a well-formatted relative path to the icon for this given category in the specified format.

        :param format: -
        :param theme: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a48767dfcd25849c1f9862dbf2ba826834e87f83e367090863c25c8d1f92f39)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="categories")
    def categories(cls) -> typing.Mapping[builtins.str, "AwsCategory"]:
        '''Get record of all categories keyed by category id.'''
        return typing.cast(typing.Mapping[builtins.str, "AwsCategory"], jsii.sget(cls, "categories"))

    @builtins.property
    @jsii.member(jsii_name="fillColor")
    def fill_color(self) -> builtins.str:
        '''Fill color for the category.'''
        return typing.cast(builtins.str, jsii.get(self, "fillColor"))

    @builtins.property
    @jsii.member(jsii_name="fontColor")
    def font_color(self) -> builtins.str:
        '''Font color for the category.'''
        return typing.cast(builtins.str, jsii.get(self, "fontColor"))

    @builtins.property
    @jsii.member(jsii_name="gradientColor")
    def gradient_color(self) -> builtins.str:
        '''Gradien color for the category.'''
        return typing.cast(builtins.str, jsii.get(self, "gradientColor"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The unique id of the category.

        Example::

            "security_identity_compliance"
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The proper name of the category.

        Example::

            "Security, Identity, & Compliance"
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="variants")
    def variants(self) -> typing.List[builtins.str]:
        '''Alternative names used to identity this category.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "variants"))

    @builtins.property
    @jsii.member(jsii_name="drawioStyles")
    def drawio_styles(self) -> typing.Optional["AwsCategoryDrawioStyles"]:
        '''Drawio style definition for this category.'''
        return typing.cast(typing.Optional["AwsCategoryDrawioStyles"], jsii.get(self, "drawioStyles"))


class AwsCategoryDrawioStyles(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws/pdk.aws_arch.AwsCategoryDrawioStyles",
):
    '''AwsCategoryDrawioStyles is a utility class for constructing drawio shape styles for services and resources.'''

    def __init__(
        self,
        category_shape: _ShapeNames_c7319e7b,
        *,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param category_shape: -
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a63de69e72543617d1929419c191f944e8d928b64ec2267f5490bdcbbaa8467)
            check_type(argname="argument category_shape", value=category_shape, expected_type=type_hints["category_shape"])
        base = _DrawioAwsResourceIconStyleBase_7d96f13d(
            fill_color=fill_color,
            font_color=font_color,
            gradient_color=gradient_color,
            align=align,
            aspect=aspect,
            dashed=dashed,
            font_size=font_size,
            font_style=font_style,
            gradient_direction=gradient_direction,
            html=html,
            outline_connect=outline_connect,
            stroke_color=stroke_color,
            vertical_align=vertical_align,
            vertical_label_position=vertical_label_position,
            pointer_event=pointer_event,
        )

        jsii.create(self.__class__, self, [category_shape, base])

    @jsii.member(jsii_name="getResourceStyle")
    def get_resource_style(
        self,
        resource_shape: _ShapeNames_c7319e7b,
    ) -> "AwsDrawioShapeStyle":
        '''Gets the drawio style for a resource based on the category style.

        :param resource_shape: The resource shape to style based on category.

        :return: The style drawio style definition for the resource based on category style.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b127e5580dd58f2e4644468dece96828994dfe68279ee0345f69c57eebdb60a)
            check_type(argname="argument resource_shape", value=resource_shape, expected_type=type_hints["resource_shape"])
        return typing.cast("AwsDrawioShapeStyle", jsii.invoke(self, "getResourceStyle", [resource_shape]))

    @jsii.member(jsii_name="getServiceStyle")
    def get_service_style(
        self,
        service_shape: _ShapeNames_c7319e7b,
    ) -> "AwsDrawioResourceIconStyle":
        '''Gets the drawio style for a service based on the category style.

        :param service_shape: The service shape to style based on category.

        :return: The style drawio style definition for the resource based on category style.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08f67ba5223f7362a096974316d19908fec9ec26e8142d305ffb314ffdb43a1)
            check_type(argname="argument service_shape", value=service_shape, expected_type=type_hints["service_shape"])
        return typing.cast("AwsDrawioResourceIconStyle", jsii.invoke(self, "getServiceStyle", [service_shape]))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> _DrawioAwsResourceIconStyleBase_7d96f13d:
        return typing.cast(_DrawioAwsResourceIconStyleBase_7d96f13d, jsii.get(self, "base"))

    @builtins.property
    @jsii.member(jsii_name="categoryShape")
    def category_shape(self) -> _ShapeNames_c7319e7b:
        return typing.cast(_ShapeNames_c7319e7b, jsii.get(self, "categoryShape"))

    @builtins.property
    @jsii.member(jsii_name="categoryStyle")
    def category_style(self) -> "AwsDrawioResourceIconStyle":
        '''Get the drawio style for this category.'''
        return typing.cast("AwsDrawioResourceIconStyle", jsii.get(self, "categoryStyle"))


@jsii.data_type(
    jsii_type="@aws/pdk.aws_arch.AwsDrawioResourceIconStyle",
    jsii_struct_bases=[_DrawioAwsResourceIconStyleBase_7d96f13d],
    name_mapping={
        "align": "align",
        "aspect": "aspect",
        "dashed": "dashed",
        "font_size": "fontSize",
        "font_style": "fontStyle",
        "gradient_direction": "gradientDirection",
        "html": "html",
        "outline_connect": "outlineConnect",
        "stroke_color": "strokeColor",
        "vertical_align": "verticalAlign",
        "vertical_label_position": "verticalLabelPosition",
        "pointer_event": "pointerEvent",
        "fill_color": "fillColor",
        "font_color": "fontColor",
        "gradient_color": "gradientColor",
        "res_icon": "resIcon",
        "shape": "shape",
    },
)
class AwsDrawioResourceIconStyle(_DrawioAwsResourceIconStyleBase_7d96f13d):
    def __init__(
        self,
        *,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        res_icon: _ShapeNames_c7319e7b,
        shape: _DrawioAws4ParentShapes_3c51fc93,
    ) -> None:
        '''Drawio resource icon style definition for AWS Resources.

        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param res_icon: 
        :param shape: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98d9cfa5ff463d371e3bee4e6e58a9be6f3e488e8ba26e1bc37ffc9d0063412)
            check_type(argname="argument align", value=align, expected_type=type_hints["align"])
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument dashed", value=dashed, expected_type=type_hints["dashed"])
            check_type(argname="argument font_size", value=font_size, expected_type=type_hints["font_size"])
            check_type(argname="argument font_style", value=font_style, expected_type=type_hints["font_style"])
            check_type(argname="argument gradient_direction", value=gradient_direction, expected_type=type_hints["gradient_direction"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument outline_connect", value=outline_connect, expected_type=type_hints["outline_connect"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
            check_type(argname="argument vertical_label_position", value=vertical_label_position, expected_type=type_hints["vertical_label_position"])
            check_type(argname="argument pointer_event", value=pointer_event, expected_type=type_hints["pointer_event"])
            check_type(argname="argument fill_color", value=fill_color, expected_type=type_hints["fill_color"])
            check_type(argname="argument font_color", value=font_color, expected_type=type_hints["font_color"])
            check_type(argname="argument gradient_color", value=gradient_color, expected_type=type_hints["gradient_color"])
            check_type(argname="argument res_icon", value=res_icon, expected_type=type_hints["res_icon"])
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "align": align,
            "aspect": aspect,
            "dashed": dashed,
            "font_size": font_size,
            "font_style": font_style,
            "gradient_direction": gradient_direction,
            "html": html,
            "outline_connect": outline_connect,
            "stroke_color": stroke_color,
            "vertical_align": vertical_align,
            "vertical_label_position": vertical_label_position,
            "fill_color": fill_color,
            "font_color": font_color,
            "gradient_color": gradient_color,
            "res_icon": res_icon,
            "shape": shape,
        }
        if pointer_event is not None:
            self._values["pointer_event"] = pointer_event

    @builtins.property
    def align(self) -> builtins.str:
        result = self._values.get("align")
        assert result is not None, "Required property 'align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspect(self) -> builtins.str:
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashed(self) -> jsii.Number:
        result = self._values.get("dashed")
        assert result is not None, "Required property 'dashed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_size(self) -> jsii.Number:
        result = self._values.get("font_size")
        assert result is not None, "Required property 'font_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_style(self) -> typing.Union[builtins.str, jsii.Number]:
        result = self._values.get("font_style")
        assert result is not None, "Required property 'font_style' is missing"
        return typing.cast(typing.Union[builtins.str, jsii.Number], result)

    @builtins.property
    def gradient_direction(self) -> builtins.str:
        result = self._values.get("gradient_direction")
        assert result is not None, "Required property 'gradient_direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def html(self) -> jsii.Number:
        result = self._values.get("html")
        assert result is not None, "Required property 'html' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def outline_connect(self) -> jsii.Number:
        result = self._values.get("outline_connect")
        assert result is not None, "Required property 'outline_connect' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stroke_color(self) -> builtins.str:
        result = self._values.get("stroke_color")
        assert result is not None, "Required property 'stroke_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_align(self) -> builtins.str:
        result = self._values.get("vertical_align")
        assert result is not None, "Required property 'vertical_align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_label_position(self) -> builtins.str:
        result = self._values.get("vertical_label_position")
        assert result is not None, "Required property 'vertical_label_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pointer_event(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("pointer_event")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_color(self) -> builtins.str:
        result = self._values.get("fill_color")
        assert result is not None, "Required property 'fill_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def font_color(self) -> builtins.str:
        result = self._values.get("font_color")
        assert result is not None, "Required property 'font_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gradient_color(self) -> builtins.str:
        result = self._values.get("gradient_color")
        assert result is not None, "Required property 'gradient_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def res_icon(self) -> _ShapeNames_c7319e7b:
        result = self._values.get("res_icon")
        assert result is not None, "Required property 'res_icon' is missing"
        return typing.cast(_ShapeNames_c7319e7b, result)

    @builtins.property
    def shape(self) -> _DrawioAws4ParentShapes_3c51fc93:
        result = self._values.get("shape")
        assert result is not None, "Required property 'shape' is missing"
        return typing.cast(_DrawioAws4ParentShapes_3c51fc93, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDrawioResourceIconStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws/pdk.aws_arch.AwsDrawioShapeStyle",
    jsii_struct_bases=[_DrawioAwsResourceIconStyleBase_7d96f13d],
    name_mapping={
        "align": "align",
        "aspect": "aspect",
        "dashed": "dashed",
        "font_size": "fontSize",
        "font_style": "fontStyle",
        "gradient_direction": "gradientDirection",
        "html": "html",
        "outline_connect": "outlineConnect",
        "stroke_color": "strokeColor",
        "vertical_align": "verticalAlign",
        "vertical_label_position": "verticalLabelPosition",
        "pointer_event": "pointerEvent",
        "fill_color": "fillColor",
        "font_color": "fontColor",
        "gradient_color": "gradientColor",
        "shape": "shape",
    },
)
class AwsDrawioShapeStyle(_DrawioAwsResourceIconStyleBase_7d96f13d):
    def __init__(
        self,
        *,
        align: builtins.str,
        aspect: builtins.str,
        dashed: jsii.Number,
        font_size: jsii.Number,
        font_style: typing.Union[builtins.str, jsii.Number],
        gradient_direction: builtins.str,
        html: jsii.Number,
        outline_connect: jsii.Number,
        stroke_color: builtins.str,
        vertical_align: builtins.str,
        vertical_label_position: builtins.str,
        pointer_event: typing.Optional[jsii.Number] = None,
        fill_color: builtins.str,
        font_color: builtins.str,
        gradient_color: builtins.str,
        shape: _ShapeNames_c7319e7b,
    ) -> None:
        '''Drawio shape based style definition.

        :param align: 
        :param aspect: 
        :param dashed: 
        :param font_size: 
        :param font_style: 
        :param gradient_direction: 
        :param html: 
        :param outline_connect: 
        :param stroke_color: 
        :param vertical_align: 
        :param vertical_label_position: 
        :param pointer_event: 
        :param fill_color: 
        :param font_color: 
        :param gradient_color: 
        :param shape: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbccd22315ecaf60f95a27f682ddefea131947464dd6d30ad1f9fcac99a7fc58)
            check_type(argname="argument align", value=align, expected_type=type_hints["align"])
            check_type(argname="argument aspect", value=aspect, expected_type=type_hints["aspect"])
            check_type(argname="argument dashed", value=dashed, expected_type=type_hints["dashed"])
            check_type(argname="argument font_size", value=font_size, expected_type=type_hints["font_size"])
            check_type(argname="argument font_style", value=font_style, expected_type=type_hints["font_style"])
            check_type(argname="argument gradient_direction", value=gradient_direction, expected_type=type_hints["gradient_direction"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument outline_connect", value=outline_connect, expected_type=type_hints["outline_connect"])
            check_type(argname="argument stroke_color", value=stroke_color, expected_type=type_hints["stroke_color"])
            check_type(argname="argument vertical_align", value=vertical_align, expected_type=type_hints["vertical_align"])
            check_type(argname="argument vertical_label_position", value=vertical_label_position, expected_type=type_hints["vertical_label_position"])
            check_type(argname="argument pointer_event", value=pointer_event, expected_type=type_hints["pointer_event"])
            check_type(argname="argument fill_color", value=fill_color, expected_type=type_hints["fill_color"])
            check_type(argname="argument font_color", value=font_color, expected_type=type_hints["font_color"])
            check_type(argname="argument gradient_color", value=gradient_color, expected_type=type_hints["gradient_color"])
            check_type(argname="argument shape", value=shape, expected_type=type_hints["shape"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "align": align,
            "aspect": aspect,
            "dashed": dashed,
            "font_size": font_size,
            "font_style": font_style,
            "gradient_direction": gradient_direction,
            "html": html,
            "outline_connect": outline_connect,
            "stroke_color": stroke_color,
            "vertical_align": vertical_align,
            "vertical_label_position": vertical_label_position,
            "fill_color": fill_color,
            "font_color": font_color,
            "gradient_color": gradient_color,
            "shape": shape,
        }
        if pointer_event is not None:
            self._values["pointer_event"] = pointer_event

    @builtins.property
    def align(self) -> builtins.str:
        result = self._values.get("align")
        assert result is not None, "Required property 'align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aspect(self) -> builtins.str:
        result = self._values.get("aspect")
        assert result is not None, "Required property 'aspect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashed(self) -> jsii.Number:
        result = self._values.get("dashed")
        assert result is not None, "Required property 'dashed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_size(self) -> jsii.Number:
        result = self._values.get("font_size")
        assert result is not None, "Required property 'font_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def font_style(self) -> typing.Union[builtins.str, jsii.Number]:
        result = self._values.get("font_style")
        assert result is not None, "Required property 'font_style' is missing"
        return typing.cast(typing.Union[builtins.str, jsii.Number], result)

    @builtins.property
    def gradient_direction(self) -> builtins.str:
        result = self._values.get("gradient_direction")
        assert result is not None, "Required property 'gradient_direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def html(self) -> jsii.Number:
        result = self._values.get("html")
        assert result is not None, "Required property 'html' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def outline_connect(self) -> jsii.Number:
        result = self._values.get("outline_connect")
        assert result is not None, "Required property 'outline_connect' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stroke_color(self) -> builtins.str:
        result = self._values.get("stroke_color")
        assert result is not None, "Required property 'stroke_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_align(self) -> builtins.str:
        result = self._values.get("vertical_align")
        assert result is not None, "Required property 'vertical_align' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vertical_label_position(self) -> builtins.str:
        result = self._values.get("vertical_label_position")
        assert result is not None, "Required property 'vertical_label_position' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pointer_event(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("pointer_event")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_color(self) -> builtins.str:
        result = self._values.get("fill_color")
        assert result is not None, "Required property 'fill_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def font_color(self) -> builtins.str:
        result = self._values.get("font_color")
        assert result is not None, "Required property 'font_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gradient_color(self) -> builtins.str:
        result = self._values.get("gradient_color")
        assert result is not None, "Required property 'gradient_color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shape(self) -> _ShapeNames_c7319e7b:
        result = self._values.get("shape")
        assert result is not None, "Required property 'shape' is missing"
        return typing.cast(_ShapeNames_c7319e7b, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDrawioShapeStyle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsResource(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.aws_arch.AwsResource"):
    '''AwsResource class provides an interface for normalizing resource metadata between mapped systems.'''

    @jsii.member(jsii_name="findResource")
    @builtins.classmethod
    def find_resource(cls, value: builtins.str) -> typing.Optional["AwsResource"]:
        '''Find {@link AwsResource} associated with given value.

        :param value: - The value to match {@link AwsResource}; can be id, asset key, full name, etc.

        :throws: Error is no resource found
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5c7ddfcdf43f257feeb38a381e94867f78bf7575ae977c20f62415c9a2e20a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["AwsResource"], jsii.sinvoke(cls, "findResource", [value]))

    @jsii.member(jsii_name="getResource")
    @builtins.classmethod
    def get_resource(cls, cfn_resource_type: builtins.str) -> "AwsResource":
        '''Get {@link AwsResource} by CloudFormation resource type.

        :param cfn_resource_type: - Fully qualifief CloudFormation resource type (eg: AWS:S3:Bucket).

        :throws: Error is no resource found
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750b029e959fdaf2222b734882c8c040f1facf9f9b439d11ff882c76fb63f0c9)
            check_type(argname="argument cfn_resource_type", value=cfn_resource_type, expected_type=type_hints["cfn_resource_type"])
        return typing.cast("AwsResource", jsii.sinvoke(cls, "getResource", [cfn_resource_type]))

    @jsii.member(jsii_name="drawioStyle")
    def drawio_style(self) -> typing.Optional[AwsDrawioShapeStyle]:
        '''Gets the draiwio style for the resource.'''
        return typing.cast(typing.Optional[AwsDrawioShapeStyle], jsii.invoke(self, "drawioStyle", []))

    @jsii.member(jsii_name="getCategoryIcon")
    def get_category_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Gets the category icon for the resource.

        This maybe different than {@link AwsResource.service.category.icon } based on mappings overrides, which
        if do not exist will fallback to {@link AwsResource.service.category.icon }.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :see: {@link AwsService.icon }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4facfacf196ff51861ba52ac299734d023441967e8819ad528a24a807c851573)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getCategoryIcon", [format, theme]))

    @jsii.member(jsii_name="getGeneralIcon")
    def get_general_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Gets the general icon for the resource if available.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path or undefined if does not have general icon
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6547ece59dba8e343e9a9058c1c96abe51aa6fed2eefdbfb024a1d4f23ce1ec)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getGeneralIcon", [format, theme]))

    @jsii.member(jsii_name="getResourceIcon")
    def get_resource_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Gets the resource specific icon for the resource.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path or undefined if does not have resource icon
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__789ff86219f1c0b5894c0503395ccee37f10896da0fd73e759de0d2522440b19)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getResourceIcon", [format, theme]))

    @jsii.member(jsii_name="getServiceIcon")
    def get_service_icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Gets the service icon for the resource.

        This maybe different than {@link AwsResource.service.icon } based on mappings overrides, which
        if do not exist will fallback to {@link AwsResource.service.icon }.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path

        :see: {@link AwsService.icon }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a6ebb6e910a264c9263944f401366c91e5fc18a29112609e1f153ee4785b73)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getServiceIcon", [format, theme]))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Gets the best icon match for the resource following the order of: 1.

        explicit resource icon
        2. general icon
        3. service icon

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba25aadd5625afbef1b8aa97804aba2baf5023fa1ab457e45929c07802ff4e7)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="resources")
    def resources(cls) -> typing.Mapping[builtins.str, "AwsResource"]:
        '''Get record of all resources keyed by resource id.'''
        return typing.cast(typing.Mapping[builtins.str, "AwsResource"], jsii.sget(cls, "resources"))

    @builtins.property
    @jsii.member(jsii_name="cfnResourceType")
    def cfn_resource_type(self) -> builtins.str:
        '''Fully-qualified CloudFormation resource type (eg: "AWS:S3:Bucket").'''
        return typing.cast(builtins.str, jsii.get(self, "cfnResourceType"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "AwsService":
        '''The {@link AwsService} the resource belongs to.'''
        return typing.cast("AwsService", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="drawioShape")
    def drawio_shape(self) -> typing.Optional[_ShapeNames_c7319e7b]:
        '''The drawio shape mapped to this resource, or undefined if no mapping.'''
        return typing.cast(typing.Optional[_ShapeNames_c7319e7b], jsii.get(self, "drawioShape"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> typing.Optional[builtins.str]:
        '''The proper full name of the resource.

        Example::

            "Bucket", "Amazon S3 on Outposts"
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullName"))


class AwsService(metaclass=jsii.JSIIMeta, jsii_type="@aws/pdk.aws_arch.AwsService"):
    '''AwsService class provides an interface for normalizing service metadata between mapped systems.'''

    @jsii.member(jsii_name="findService")
    @builtins.classmethod
    def find_service(cls, value: builtins.str) -> typing.Optional["AwsService"]:
        '''Finds the {@link AwsService} associated with a given value.

        :param value: Value to match {@link AwsService}, which can be ``id``, ``assetKey``, ``fullName``, etc.

        :return: Returns matching {@link AwsService } or ``undefined`` if not found

        :throws: Error if service not found
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1530ec81e768fb94c2a11e4466c6996a473e9ba5e4192a162f94645fea7e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["AwsService"], jsii.sinvoke(cls, "findService", [value]))

    @jsii.member(jsii_name="getService")
    @builtins.classmethod
    def get_service(cls, cfn_service: builtins.str) -> "AwsService":
        '''Get {@link AwsService} by CloudFormation "service" name, where service name is expressed as ``<provider>::<service>::<resource>``.

        :param cfn_service: The service name to retrieve {@link AwsService} for.

        :return: Returns the {@link AwsService } associated with the ``cfnService`` provided

        :throws: Error is service not found
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d552acf18455224dad5a8c78524a7e4a9869e2497bf6c932076fd847975224e)
            check_type(argname="argument cfn_service", value=cfn_service, expected_type=type_hints["cfn_service"])
        return typing.cast("AwsService", jsii.sinvoke(cls, "getService", [cfn_service]))

    @jsii.member(jsii_name="drawioStyle")
    def drawio_style(self) -> typing.Optional[AwsDrawioResourceIconStyle]:
        '''Get drawio style for this service.'''
        return typing.cast(typing.Optional[AwsDrawioResourceIconStyle], jsii.invoke(self, "drawioStyle", []))

    @jsii.member(jsii_name="icon")
    def icon(
        self,
        format: builtins.str,
        theme: typing.Optional[builtins.str] = None,
    ) -> typing.Optional[builtins.str]:
        '''Get relative asset icon for the service for a given format and optional theme.

        :param format: - The format of icon.
        :param theme: - Optional theme.

        :return: Returns relative asset icon path
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155a87e9b7d4ef31ca815f09a23c8c6c6eb844c5fb9546e0f2c055d501e8ef68)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument theme", value=theme, expected_type=type_hints["theme"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "icon", [format, theme]))

    @jsii.member(jsii_name="serviceResources")
    def service_resources(self) -> typing.List[AwsResource]:
        '''List all resources of this service.'''
        return typing.cast(typing.List[AwsResource], jsii.invoke(self, "serviceResources", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="services")
    def services(cls) -> typing.Mapping[builtins.str, "AwsService"]:
        '''Get record of all {@link AwsService}s keyed by ``id``.'''
        return typing.cast(typing.Mapping[builtins.str, "AwsService"], jsii.sget(cls, "services"))

    @builtins.property
    @jsii.member(jsii_name="cfnProvider")
    def cfn_provider(self) -> builtins.str:
        '''The CloudFormation "provider" for the service, as expressed by ``<provicer>::<service>::<resource>``.'''
        return typing.cast(builtins.str, jsii.get(self, "cfnProvider"))

    @builtins.property
    @jsii.member(jsii_name="cfnService")
    def cfn_service(self) -> builtins.str:
        '''The CloudFormation "service" for the service, as expressed by ``<provicer>::<service>::<resource>``.'''
        return typing.cast(builtins.str, jsii.get(self, "cfnService"))

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        '''The proper full name of the service.

        Example::

            "AWS Glue", "Amazon S3"
        '''
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> typing.Optional[AwsCategory]:
        '''The category the service belongs to, or undefined if does not belong to a category.'''
        return typing.cast(typing.Optional[AwsCategory], jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="drawioShape")
    def drawio_shape(self) -> typing.Optional[_ShapeNames_c7319e7b]:
        '''Drawio shape associated with this service, or undefined if service not mapped to draiwio shape.'''
        return typing.cast(typing.Optional[_ShapeNames_c7319e7b], jsii.get(self, "drawioShape"))

    @builtins.property
    @jsii.member(jsii_name="pricingMetadata")
    def pricing_metadata(self) -> typing.Optional[_Service_de1b914e]:
        '''Get service pricing metadata.'''
        return typing.cast(typing.Optional[_Service_de1b914e], jsii.get(self, "pricingMetadata"))

    @builtins.property
    @jsii.member(jsii_name="pricingServiceCode")
    def pricing_service_code(self) -> typing.Optional[builtins.str]:
        '''The pricing ``serviceCode`` associated with this service, or undefined if service not mapped to pricing.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingServiceCode"))


@jsii.data_type(
    jsii_type="@aws/pdk.aws_arch.ParsedAssetKey",
    jsii_struct_bases=[],
    name_mapping={
        "asset_key": "assetKey",
        "basename": "basename",
        "category": "category",
        "instance_type": "instanceType",
        "iot_thing": "iotThing",
        "resource": "resource",
        "service": "service",
    },
)
class ParsedAssetKey:
    def __init__(
        self,
        *,
        asset_key: builtins.str,
        basename: builtins.str,
        category: builtins.str,
        instance_type: typing.Optional[builtins.str] = None,
        iot_thing: typing.Optional[builtins.str] = None,
        resource: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Parsed asset key.

        :param asset_key: Reference to the full key that was parsed.
        :param basename: The last segment of the key (which is the nested icon). For instances and things this includes the dir prefix.
        :param category: Category id.
        :param instance_type: The instance type if key is for an ec2 instance.
        :param iot_thing: The iot thing if key is for an iot thing.
        :param resource: Resource id if key is for a resource.
        :param service: Service id if key is partitioned by resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b771e0c8526482b283301f8f573bd5f7d6ddb051fd6b5febf43a472722b760)
            check_type(argname="argument asset_key", value=asset_key, expected_type=type_hints["asset_key"])
            check_type(argname="argument basename", value=basename, expected_type=type_hints["basename"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument iot_thing", value=iot_thing, expected_type=type_hints["iot_thing"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_key": asset_key,
            "basename": basename,
            "category": category,
        }
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if iot_thing is not None:
            self._values["iot_thing"] = iot_thing
        if resource is not None:
            self._values["resource"] = resource
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def asset_key(self) -> builtins.str:
        '''Reference to the full key that was parsed.'''
        result = self._values.get("asset_key")
        assert result is not None, "Required property 'asset_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basename(self) -> builtins.str:
        '''The last segment of the key (which is the nested icon).

        For instances and things this includes the dir prefix.
        '''
        result = self._values.get("basename")
        assert result is not None, "Required property 'basename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def category(self) -> builtins.str:
        '''Category id.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type if key is for an ec2 instance.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot_thing(self) -> typing.Optional[builtins.str]:
        '''The iot thing if key is for an iot thing.'''
        result = self._values.get("iot_thing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[builtins.str]:
        '''Resource id if key is for a resource.'''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service id if key is partitioned by resource.'''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParsedAssetKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsArchitecture",
    "AwsCategory",
    "AwsCategoryDrawioStyles",
    "AwsDrawioResourceIconStyle",
    "AwsDrawioShapeStyle",
    "AwsResource",
    "AwsService",
    "ParsedAssetKey",
    "aws_arch",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aws_arch

def _typecheckingstub__37e12aed85f4b5ad80e1ca8cce0ef4f1cef77aac7f54dc5696e074e095c24bb0(
    qualified_asset_key: builtins.str,
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be0e69437dbf20f1148d01e1723d0904b527d2a7610a457c044389517fc912d(
    category: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a4bd5f7681f00a5db4f9360958b417ae22a2454bcdcad45e8bb804ba8c92cc(
    instance_type: builtins.str,
    format: typing.Optional[builtins.str] = None,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736b9d908e5cb23042bbd1614f8decbd48310242a1ab7fde5ccaa26aaea4bc68(
    instance_type: builtins.str,
    format: typing.Optional[builtins.str] = None,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d523e4408e467c23430be0831cd1bce6021fbd55e0c980bb3a5d0e97ddb697(
    cfn_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16a49f10a18290e7979371bff79c04718d2e30b1f15b42375d343e38c93fe6c(
    identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62214db900e10c5c6f0aba2c457bdba2afef4a87d41a3e32632b1464d0c495a0(
    asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e770dfdd6bfb95fb9452c476e677cba8a10512c2964efdde2c91b34173987802(
    asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c95629117e0e7830b6dc50dfbd4ddd91d5a77354952676bea5aa3c6c458c09(
    svg_asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04bc93052b5d28a7387907f2d892d80b7e5d57f79117e9d274bf2c7c9655d4f(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a48767dfcd25849c1f9862dbf2ba826834e87f83e367090863c25c8d1f92f39(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a63de69e72543617d1929419c191f944e8d928b64ec2267f5490bdcbbaa8467(
    category_shape: _ShapeNames_c7319e7b,
    *,
    fill_color: builtins.str,
    font_color: builtins.str,
    gradient_color: builtins.str,
    align: builtins.str,
    aspect: builtins.str,
    dashed: jsii.Number,
    font_size: jsii.Number,
    font_style: typing.Union[builtins.str, jsii.Number],
    gradient_direction: builtins.str,
    html: jsii.Number,
    outline_connect: jsii.Number,
    stroke_color: builtins.str,
    vertical_align: builtins.str,
    vertical_label_position: builtins.str,
    pointer_event: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b127e5580dd58f2e4644468dece96828994dfe68279ee0345f69c57eebdb60a(
    resource_shape: _ShapeNames_c7319e7b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08f67ba5223f7362a096974316d19908fec9ec26e8142d305ffb314ffdb43a1(
    service_shape: _ShapeNames_c7319e7b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98d9cfa5ff463d371e3bee4e6e58a9be6f3e488e8ba26e1bc37ffc9d0063412(
    *,
    align: builtins.str,
    aspect: builtins.str,
    dashed: jsii.Number,
    font_size: jsii.Number,
    font_style: typing.Union[builtins.str, jsii.Number],
    gradient_direction: builtins.str,
    html: jsii.Number,
    outline_connect: jsii.Number,
    stroke_color: builtins.str,
    vertical_align: builtins.str,
    vertical_label_position: builtins.str,
    pointer_event: typing.Optional[jsii.Number] = None,
    fill_color: builtins.str,
    font_color: builtins.str,
    gradient_color: builtins.str,
    res_icon: _ShapeNames_c7319e7b,
    shape: _DrawioAws4ParentShapes_3c51fc93,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbccd22315ecaf60f95a27f682ddefea131947464dd6d30ad1f9fcac99a7fc58(
    *,
    align: builtins.str,
    aspect: builtins.str,
    dashed: jsii.Number,
    font_size: jsii.Number,
    font_style: typing.Union[builtins.str, jsii.Number],
    gradient_direction: builtins.str,
    html: jsii.Number,
    outline_connect: jsii.Number,
    stroke_color: builtins.str,
    vertical_align: builtins.str,
    vertical_label_position: builtins.str,
    pointer_event: typing.Optional[jsii.Number] = None,
    fill_color: builtins.str,
    font_color: builtins.str,
    gradient_color: builtins.str,
    shape: _ShapeNames_c7319e7b,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5c7ddfcdf43f257feeb38a381e94867f78bf7575ae977c20f62415c9a2e20a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750b029e959fdaf2222b734882c8c040f1facf9f9b439d11ff882c76fb63f0c9(
    cfn_resource_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4facfacf196ff51861ba52ac299734d023441967e8819ad528a24a807c851573(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6547ece59dba8e343e9a9058c1c96abe51aa6fed2eefdbfb024a1d4f23ce1ec(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789ff86219f1c0b5894c0503395ccee37f10896da0fd73e759de0d2522440b19(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a6ebb6e910a264c9263944f401366c91e5fc18a29112609e1f153ee4785b73(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba25aadd5625afbef1b8aa97804aba2baf5023fa1ab457e45929c07802ff4e7(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1530ec81e768fb94c2a11e4466c6996a473e9ba5e4192a162f94645fea7e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d552acf18455224dad5a8c78524a7e4a9869e2497bf6c932076fd847975224e(
    cfn_service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155a87e9b7d4ef31ca815f09a23c8c6c6eb844c5fb9546e0f2c055d501e8ef68(
    format: builtins.str,
    theme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b771e0c8526482b283301f8f573bd5f7d6ddb051fd6b5febf43a472722b760(
    *,
    asset_key: builtins.str,
    basename: builtins.str,
    category: builtins.str,
    instance_type: typing.Optional[builtins.str] = None,
    iot_thing: typing.Optional[builtins.str] = None,
    resource: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
