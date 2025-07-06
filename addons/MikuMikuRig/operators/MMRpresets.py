import shutil

import bpy
import json
import os
from MikuMikuRig.addons.MikuMikuRig.config import __addon_name__


class mmrmakepresetsOperator(bpy.types.Operator):
    '''make presets'''
    bl_idname = "object.mmr_make_presets"
    bl_label = "make presets"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 验证物体是不是骨骼
    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        if obj is not None:
            if obj.type == 'ARMATURE':
                return True
        return False

    def execute(self, context: bpy.types.Context):

        mmr = context.object.mmr

        if mmr.make_presets:
            mmr.make_presets = False
            # 初始化
            mmr.number = 0
            mmr.json_txt = '按下"指定"以指定骨骼'
            mmr.designated = True
            mmr.Copy_the_file = True
        else:
            mmr.make_presets = True

        return {'FINISHED'}


class mmrdesignatedOperator(bpy.types.Operator):
    '''designated presets'''
    bl_idname = "object.mmr_designated"
    bl_label = "designated"

    # 验证物体是不是骨骼
    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        if obj is not None:
            if obj.type == 'ARMATURE':
                return True
        return False

    def execute(self, context: bpy.types.Context):

        mmr = context.object.mmr

        # 进入姿态模式
        bpy.ops.object.mode_set(mode='POSE')

        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = 'MMR_Presets.json'
        new_file_path = os.path.join(new_path,file)
        # 读取json文件
        with open(new_file_path) as f:
            config = json.load(f)

        # 将字典config的键转换为列表
        json_keys = list(config.keys())
        # 传入数组
        fourth_key = json_keys[mmr.number]

        if mmr.designated:
            # 更新提示
            mmr.json_txt = "请选择:" + fourth_key

            print(mmr.number, fourth_key)

            mmr.designated = False
            return {'FINISHED'}
        else:

            # 获取Windows桌面的路径
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            # 源文件路径
            src_file = new_file_path
            # 目标文件路径
            dst_file = desktop_path

            # 复制文件
            if mmr.Copy_the_file:
                shutil.copy(src_file, dst_file)
                mmr.Copy_the_file = False

            file = 'MMR_Presets.json'
            json_path = os.path.join(desktop_path, file)
            # 读取json文件
            with open(json_path) as f:
                config = json.load(f)

            # 获取当前选中的骨骼
            selected_bones = bpy.context.active_bone.name
            print("当前选中的骨骼名称:", selected_bones)

            config[fourth_key] = selected_bones

            # 写入json文件
            try:
                with open(json_path, 'w', encoding='utf - 8') as f:
                    json.dump(config, f, ensure_ascii=False)
                self.report({'INFO'}, selected_bones + '写入成功!')
            except Exception as e:
                print(f"写入失败, 错误原因: {e}")

            if mmr.number != 56:
                # 更新提示
                mmr.json_txt = 'OK! 下一个'
                # 完成指定后将数组加 1
                mmr.number = mmr.number + 1
                mmr.designated = True
            else:
                # 更新提示
                self.report({'INFO'}, '文件位于:' + json_path)
                mmr.json_txt = '文件位于:' + json_path
                mmr.number = mmr.number + 1

        return {'FINISHED'}
