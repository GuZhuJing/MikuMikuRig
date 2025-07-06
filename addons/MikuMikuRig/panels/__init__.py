import os
import bpy
from bpy.props import *

from MikuMikuRig.addons.MikuMikuRig.config import __addon_name__

def print_json_files(directory):
    json_file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_file_name = os.path.join(root, file)
                json_file_names.append(json_file_name)

    return json_file_names


def print_json():
    # 获取当前运行的Py文件的路径
    current_file_path = __file__

    # 获取文件夹路径
    new_path = os.path.dirname(os.path.dirname(current_file_path))

    # 当前文件夹路径
    new_file_path = os.path.join(new_path, 'operators', 'presets')

    # 调用函数获取JSON文件名称列表
    json_file_names = print_json_files(new_file_path)

    presets_name = []

    for name in json_file_names:
        name = os.path.basename(name)
        names = os.path.splitext(name)
        json_name = names[0]
        presets_name.append((json_name, json_name, json_name))

    return presets_name


class MMR_property(bpy.types.PropertyGroup):

    presets: EnumProperty(
        name="presets",
        items=print_json(),
        default='MMD_JP',
        description="控制器预设"
    )

    filepath: StringProperty(
        name="",
        subtype='FILE_PATH',
        description="取VMD的第1帧为初始姿势"
    )

    number: IntProperty(
        name="Int Config",
        default=2,
    )

    boolean: BoolProperty(
        name="Boolean Config",
        default=False,
    )

    # 创建布尔属性作为极向目标开关
    Polar_target: BoolProperty(
        name="Polar target",
        default=False
    )

    extras_enabled: BoolProperty(
        name="Extras Enabled",
        default=False
    )

    Shoulder_linkage: BoolProperty(
        name="Shoulder linkage",
        default=False
    )

    Initial_pose: BoolProperty(
        name="Initial pose",
        default=False,
        description="取VMD的第1帧为初始姿势"
    )

    json_filepath: StringProperty(
        name="",
        subtype='FILE_PATH',
        description="导入json字典预设"
    )

    Import_presets: BoolProperty(
        name="Import presets",
        default=False,
        description="导入json字典预设"
    )
    Bend_the_bones: BoolProperty(
        name="Bend the bones",
        default=True,
        description="非MMD骨骼不要启用,请手动弯曲骨骼"
    )

    make_presets: BoolProperty(
        default=True,
    )

    number: IntProperty(
        default=0,
    )
    json_txt: StringProperty(
        name="",
        subtype='FILE_NAME',
    )
    designated: BoolProperty(
        default=True,
    )

    designated: BoolProperty(
        default=True,
    )
    Copy_the_file: BoolProperty(
        default=True,
    )