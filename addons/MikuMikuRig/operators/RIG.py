import bpy
import os
import mathutils
import logging
import json
from MikuMikuRig.addons.MikuMikuRig.config import __addon_name__


class mmdarmoptOperator(bpy.types.Operator):
    '''Optimization MMD Armature'''
    bl_idname = "object.mmd_arm_opt"
    bl_label = "Optimization MMD Armature"

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
        # 当前活动物体名称
        active_object_name = bpy.context.active_object.name
        print("当前活动物体名称:", active_object_name)

        # 验证当前活动物体是不是骨骼(防刁民)
        def is_active_object_armature(context):
            active_obj = context.view_layer.objects.active
            if active_obj:
                return active_obj.type == 'ARMATURE'
            return False

        if is_active_object_armature(bpy.context):
            armature = bpy.context.active_object.data
            # 获取活动骨骼对象的所有骨骼集合名称
            collection_names = [collection.name for collection in armature.collections]
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='DESELECT')  # 取消所有选择

            # 遍历骨骼集合名称列表，并设置它们的可见性
            for name in collection_names:
                if name in bpy.context.object.data.collections_all:
                    bpy.context.object.data.collections_all[name].is_visible = False

            # 全选骨骼
            bpy.ops.pose.select_all(action='SELECT')
            # 检查是否有选中骨骼
            armature = bpy.context.active_object
            if armature and armature.type == 'ARMATURE':
                selected = any(bone.bone.select for bone in armature.pose.bones)
                if selected:
                    print('已有选中骨骼')
                    # 再次检查选中骨骼状态并打印详细信息（再次防刁民）
                    selected_bones = [bone.name for bone in armature.pose.bones if bone.bone.select]
                    print(f"选中的骨骼有: {selected_bones}")
                    # 创建新的骨骼集合
                    bpy.ops.armature.collection_add('INVOKE_DEFAULT')
                    new_collection = bpy.context.active_object.data.collections[-1]
                    new_collection.name = "[其他]"  # 名称
                    bpy.ops.armature.collection_assign('INVOKE_DEFAULT')
                    bpy.ops.pose.select_all(action='DESELECT')  # 取消所有选择
                    bpy.context.object.data.collections_all[new_collection.name].is_visible = False
                else:
                    print('没有其他骨骼')

            # 遍历Groups列表
            Groups = ['Root', 'センター', 'ＩＫ', '体(上)', '腕', '指', '体(下)', '足']
            for group in Groups:
                if group in bpy.context.object.data.collections_all:
                    bpy.context.object.data.collections_all[group].is_visible = True

            # 获取指定骨骼集合中的骨骼名称列表
            def get_bone_names_in_collection(collection_name):  # 定义一个函数
                bone_name_list = []
                # 获取当前活动对象并判断是否为骨骼对象
                armature_obj = bpy.context.active_object
                if armature_obj and armature_obj.type == 'ARMATURE':
                    # 遍历骨骼集合
                    for collection in armature_obj.data.collections:
                        if collection.name == collection_name:
                            # 遍历骨骼集合中的骨骼并添加名称到列表
                            for bone in collection.bones:
                                bone_name_list.append(bone.name)
                return bone_name_list

            result = get_bone_names_in_collection('Root')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME09'

            result = get_bone_names_in_collection('センター')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME09'

            result = get_bone_names_in_collection('ＩＫ')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME01'

            result = get_bone_names_in_collection('体(上)')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME04'

            result = get_bone_names_in_collection('腕')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME03'

            result = get_bone_names_in_collection('体(下)')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME04'

            result = get_bone_names_in_collection('足')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME03'

            result = get_bone_names_in_collection('指')
            print(result)
            # 遍历结果列表，为每个骨骼设置颜色调色板
            for bone_name in result:
                if bone_name in bpy.context.object.data.bones:
                    bpy.context.object.data.bones[bone_name].color.palette = 'THEME04'

            # 处理左侧(L)骨骼

            # 检查骨骼 "手IK.L" 是否存在
            if "手IK.L" not in bpy.context.object.data.bones.keys():
                # 编辑模式
                bpy.ops.object.mode_set(mode='EDIT')

                # 取消所有选择
                bpy.ops.armature.select_all(action='DESELECT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern="手首.L", extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get('手首.L')
                bpy.context.edit_object.data.edit_bones.active = bone
                # 复制骨骼
                bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names": False},
                                                TRANSFORM_OT_translate={"value": (0, 0, 0)})
                # 获取复制后的骨骼列表
                new_bones = bpy.context.selected_bones

                # 遍历新骨骼，并根据需要更改名称
                for i, bone in enumerate(new_bones, start=1):
                    # 构造新的骨骼名称
                    new_bone_name = "手IK.L"
                    bone.name = new_bone_name
                # 进入姿态模式
                bpy.ops.object.mode_set(mode='POSE')
                # 执行放大操作，在X、Y、Z轴方向上都放大2倍
                bpy.ops.transform.resize(value=(2, 2, 2))
                bpy.context.object.data.bones["手IK.L"].color.palette = 'THEME01'
                # 解除位置限制
                bpy.context.active_pose_bone.lock_location[0] = False
                bpy.context.active_pose_bone.lock_location[1] = False
                bpy.context.active_pose_bone.lock_location[2] = False
                bpy.context.object.data.bones["手IK.L"].color.palette = 'THEME01'

                # 取消所有选择
                bpy.ops.pose.select_all(action='DESELECT')
                # 编辑模式
                bpy.ops.object.mode_set(mode='EDIT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern="手首.L", extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get('手首.L')
                bpy.context.edit_object.data.edit_bones.active = bone
                # 姿态模式
                bpy.ops.object.mode_set(mode='POSE')

                # 检查名为'【复制旋转】.L'的约束是否存在
                def ik_constraint_exists():
                    active_bone = bpy.context.active_pose_bone
                    if active_bone:
                        for constraint in active_bone.constraints:
                            if constraint.name == '【复制旋转】.L':
                                return True
                    return False

                # 复制旋转约束
                bpy.ops.pose.constraint_add(type='COPY_ROTATION')
                active_bone = bpy.context.active_pose_bone
                # 找到刚添加的约束
                constraint = active_bone.constraints[-1]
                # 重命名约束
                constraint.name = '【复制旋转】.L'
                # 设置复制旋转约束
                bpy.context.object.pose.bones["手首.L"].constraints["【复制旋转】.L"].target = bpy.data.objects[
                    active_object_name]
                bpy.context.object.pose.bones["手首.L"].constraints["【复制旋转】.L"].subtarget = "手IK.L"
                bpy.context.object.pose.bones["手首.L"].constraints["【复制旋转】.L"].mix_mode = 'REPLACE'
                bpy.context.object.pose.bones["手首.L"].constraints["【复制旋转】.L"].influence = 1

            else:
                print('骨骼已存在')
                bpy.context.object.data.bones["手IK.L"].color.palette = 'THEME01'

            # 编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            bone_names = ["手IK.L", 'ひじ.L']
            found = False
            # 遍历列表
            for bone in bpy.context.object.data.bones:
                if bone.name in bone_names:
                    bpy.ops.object.select_pattern(pattern=bone.name)
                    # 执行清除父级操作
                    bpy.ops.armature.parent_clear(type='CLEAR')
                    print(f"找到并清除了名为 {bone.name} 的骨骼的父级关系")
                    found = True
                    # 取消所有选择
                    bpy.ops.armature.select_all(action='DESELECT')

            if not found:
                print("未找到骨骼")

            # 骨骼名称列表
            bone1_names = ['ひじ.L', '腕.L']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('腕.L')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')
            # ---------------------------------------------------------------------
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 骨骼名称列表
            bone1_names = ['手IK.L', 'センター']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('センター')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')

            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern="ひじ.L", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('ひじ.L')
            bpy.context.edit_object.data.edit_bones.active = bone

            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')

            # 检查名为'【IK】'的约束是否存在
            def ik_constraint_exists():
                active_bone = bpy.context.active_pose_bone
                if active_bone:
                    for constraint in active_bone.constraints:
                        if constraint.name == '【IK】L':
                            return True
                return False

            if not ik_constraint_exists():
                # IK约束
                bpy.ops.pose.constraint_add(type='IK')
                active_bone = bpy.context.active_pose_bone
                # 找到刚添加的IK约束
                ik_constraint = active_bone.constraints[-1]
                # 重命名约束
                ik_constraint.name = '【IK】L'
                # 设置IK约束
                bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].influence = 1
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].target = bpy.data.objects[active_object_name]
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].subtarget = "手IK.L"
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].chain_count = 2
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].iterations = 200

            # 取消所有选择
            bpy.ops.pose.select_all(action='DESELECT')

            #-----------------------------------------------------------------------------------------------------------

            # 处理右侧(R)骨骼

            # 检查骨骼 "手IK.R" 是否存在
            if "手IK.R" not in bpy.context.object.data.bones.keys():
                # 编辑模式
                bpy.ops.object.mode_set(mode='EDIT')

                # 取消所有选择
                bpy.ops.armature.select_all(action='DESELECT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern="手首.R", extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get('手首.R')
                bpy.context.edit_object.data.edit_bones.active = bone
                # 复制骨骼
                bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names": False},
                                                TRANSFORM_OT_translate={"value": (0, 0, 0)})
                # 获取复制后的骨骼列表
                new_bones = bpy.context.selected_bones

                # 遍历新骨骼，并根据需要更改名称
                for i, bone in enumerate(new_bones, start=1):
                    # 构造新的骨骼名称
                    new_bone_name = "手IK.R"
                    bone.name = new_bone_name
                # 进入姿态模式
                bpy.ops.object.mode_set(mode='POSE')
                # 执行放大操作，在X、Y、Z轴方向上都放大2倍
                bpy.ops.transform.resize(value=(2, 2, 2))
                bpy.context.object.data.bones["手IK.R"].color.palette = 'THEME01'
                # 解除位置限制
                bpy.context.active_pose_bone.lock_location[0] = False
                bpy.context.active_pose_bone.lock_location[1] = False
                bpy.context.active_pose_bone.lock_location[2] = False
                bpy.context.object.data.bones["手IK.R"].color.palette = 'THEME01'

                # 取消所有选择
                bpy.ops.pose.select_all(action='DESELECT')
                # 编辑模式
                bpy.ops.object.mode_set(mode='EDIT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern="手首.R", extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get('手首.R')
                bpy.context.edit_object.data.edit_bones.active = bone
                # 姿态模式
                bpy.ops.object.mode_set(mode='POSE')

                # 检查名为'【复制旋转】.R'的约束是否存在
                def ik_constraint_exists():
                    active_bone = bpy.context.active_pose_bone
                    if active_bone:
                        for constraint in active_bone.constraints:
                            if constraint.name == '【复制旋转】.R':
                                return True
                    return False

                # 复制旋转约束
                bpy.ops.pose.constraint_add(type='COPY_ROTATION')
                active_bone = bpy.context.active_pose_bone
                # 找到刚添加的约束
                constraint = active_bone.constraints[-1]
                # 重命名约束
                constraint.name = '【复制旋转】.R'
                # 设置复制旋转约束
                bpy.context.object.pose.bones["手首.R"].constraints["【复制旋转】.R"].target = bpy.data.objects[
                    active_object_name]
                bpy.context.object.pose.bones["手首.R"].constraints["【复制旋转】.R"].subtarget = "手IK.R"
                bpy.context.object.pose.bones["手首.R"].constraints["【复制旋转】.R"].mix_mode = 'REPLACE'
                bpy.context.object.pose.bones["手首.R"].constraints["【复制旋转】.R"].influence = 1


            else:
                print('骨骼已存在')
                bpy.context.object.data.bones["手IK.R"].color.palette = 'THEME01'

            # 编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            bone_names = ["手IK.R", 'ひじ.R']
            found = False
            # 遍历列表
            for bone in bpy.context.object.data.bones:
                if bone.name in bone_names:
                    bpy.ops.object.select_pattern(pattern=bone.name)
                    # 执行清除父级操作
                    bpy.ops.armature.parent_clear(type='CLEAR')
                    print(f"找到并清除了名为 {bone.name} 的骨骼的父级关系")
                    found = True
                    # 取消所有选择
                    bpy.ops.armature.select_all(action='DESELECT')

            if not found:
                print("未找到骨骼")

            # 骨骼名称列表
            bone1_names = ['ひじ.R', '腕.R']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('腕.R')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')
            # ---------------------------------------------------------------------
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 骨骼名称列表
            bone1_names = ['手IK.R', 'センター']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('センター')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern="ひじ.R", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('ひじ.R')
            bpy.context.edit_object.data.edit_bones.active = bone

            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')

            # 检查名为'【IK】'的约束是否存在
            def ik_constraint_exists():
                active_bone = bpy.context.active_pose_bone
                if active_bone:
                    for constraint in active_bone.constraints:
                        if constraint.name == '【IK】R':
                            return True
                return False

            if not ik_constraint_exists():
                # IK约束
                bpy.ops.pose.constraint_add(type='IK')
                active_bone = bpy.context.active_pose_bone
                # 找到刚添加的IK约束
                ik_constraint = active_bone.constraints[-1]
                # 重命名约束
                ik_constraint.name = '【IK】R'
                # 设置IK约束
                bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].influence = 1
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].target = bpy.data.objects[active_object_name]
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].subtarget = "手IK.R"
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].chain_count = 2
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].iterations = 200
            # 取消所有选择
            bpy.ops.pose.select_all(action='DESELECT')

            # 改为各自的原点
            bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
            # 开启自动IK
            bpy.context.object.pose.use_auto_ik = True

            # 切换回物体模式
            bpy.ops.object.mode_set(mode='OBJECT')

            self.report({'INFO'}, '优化成功!')
        else:
            self.report({'ERROR'}, '当前活动物体不是骨骼')

        return {'FINISHED'}


class polartargetOperator(bpy.types.Operator):
    '''Optimization MMD Armature'''
    bl_idname = "object.mmd_polars_target"
    bl_label = "Optimization MMD Armature"

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
        # 当前活动物体名称
        active_object_name = bpy.context.active_object.name
        print("当前活动物体名称:", active_object_name)
        # 调用操作
        bpy.ops.object.mmd_arm_opt()
        # 处理左侧(L)骨骼
        if "手PT.L" not in bpy.context.object.data.bones.keys():
            # 编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern="腕.L", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('腕.L')
            bpy.context.edit_object.data.edit_bones.active = bone
            # 挤出骨骼
            bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked": False},
                                          TRANSFORM_OT_translate={"value": (0, 0.15, 0), "orient_type": 'GLOBAL',
                                                                  "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
            # 获取活跃的对象
            active_obj = bpy.context.active_object
            # 获取骨架数据
            armature_data = active_obj.data
            # 获取编辑模式下的骨骼列表
            edit_bones = armature_data.edit_bones
            # 获取最后挤出的骨骼的索引
            last_extruded_bone_index = len(edit_bones) - 1
            # 获取最后挤出的骨骼的名称
            last_extruded_bone_name = edit_bones[last_extruded_bone_index].name
            print("新挤出的骨骼名称:", last_extruded_bone_name)
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=last_extruded_bone_name, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(last_extruded_bone_name)
            bpy.context.edit_object.data.edit_bones.active = bone
            # 清空父级
            bpy.ops.armature.parent_clear(type='CLEAR')
            # 改名称
            bpy.context.active_bone.name = "手PT.L"
            # 移动
            bpy.ops.transform.translate(value=(0, +0.15, 0), orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.data.bones["手PT.L"].color.palette = 'THEME11'
            # 选择活动骨骼
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.select_pattern(pattern="ひじ.L", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('ひじ.L')
            bpy.context.edit_object.data.edit_bones.active = bone
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].pole_target = bpy.data.objects[
                active_object_name]
            bpy.context.object.pose.bones["ひじ.L"].constraints["【IK】L"].pole_subtarget = "手PT.L"
        else:
            print("骨骼已存在")
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.data.bones["手PT.L"].color.palette = 'THEME11'
        # 处理右侧(R)骨骼
        if "手PT.R" not in bpy.context.object.data.bones.keys():
            # 编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern="腕.R", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('腕.R')
            bpy.context.edit_object.data.edit_bones.active = bone
            # 挤出骨骼
            bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked": False},
                                          TRANSFORM_OT_translate={"value": (0, 0.15, 0), "orient_type": 'GLOBAL',
                                                                  "orient_matrix": (
                                                                      (1, 0, 0), (0, 1, 0), (0, 0, 1))})
            # 获取活跃的对象
            active_obj = bpy.context.active_object
            # 获取骨架数据
            armature_data = active_obj.data
            # 获取编辑模式下的骨骼列表
            edit_bones = armature_data.edit_bones
            # 获取最后挤出的骨骼的索引
            last_extruded_bone_index = len(edit_bones) - 1
            # 获取最后挤出的骨骼的名称
            last_extruded_bone_name = edit_bones[last_extruded_bone_index].name
            print("新挤出的骨骼名称:", last_extruded_bone_name)
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=last_extruded_bone_name, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(last_extruded_bone_name)
            bpy.context.edit_object.data.edit_bones.active = bone
            # 清空父级
            bpy.ops.armature.parent_clear(type='CLEAR')
            # 改名称
            bpy.context.active_bone.name = "手PT.R"
            # 移动
            bpy.ops.transform.translate(value=(0, +0.25, 0), orient_type='GLOBAL',
                                        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.data.bones["手PT.R"].color.palette = 'THEME11'
            # 选择活动骨骼
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.select_pattern(pattern="ひじ.R", extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get('ひじ.R')
            bpy.context.edit_object.data.edit_bones.active = bone
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].pole_target = bpy.data.objects[
                active_object_name]
            bpy.context.object.pose.bones["ひじ.R"].constraints["【IK】R"].pole_subtarget = "手PT.R"

            # 编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 骨骼名称列表
            bone1_names = ['手PT.R', 'センター']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('センター')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 骨骼名称列表
            bone1_names = ['手PT.L', 'センター']
            # 遍历骨骼名称列表进行选择
            for bone_name in bone1_names:
                bpy.ops.object.select_pattern(pattern=bone_name)
            # 获取当前编辑的骨骼数据
            armature = bpy.context.edit_object.data
            active_bone = armature.edit_bones.get('センター')
            # 设为活动骨骼
            if active_bone:
                bpy.context.edit_object.data.edit_bones.active = active_bone
            # 认爸爸
            bpy.ops.armature.parent_set(type='OFFSET')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

        else:
            print("骨骼已存在")
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            bpy.context.object.data.bones["手PT.R"].color.palette = 'THEME11'

        self.report({'INFO'}, '优化成功!')
        # 切换回物体模式
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


class mmrrigOperator(bpy.types.Operator):
    '''Build a controller'''
    bl_idname = "object.mmr_rig"
    bl_label = "Build a controller"

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

        # 确保脊柱骨骼连续性
    def ensure_spine_continuity(self, armature_name):
        # 进入编辑模式
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=armature_name)
        bpy.context.view_layer.objects.active = bpy.data.objects[armature_name]
        bpy.ops.object.mode_set(mode='EDIT')
        
        # 获取脊柱骨骼链
        spine_bones = ['spine', 'spine.001', 'spine.002', 'spine.003', 'spine.004']
        
        # 确保每个骨骼的尾部连接到下一个骨骼的头部
        for i in range(len(spine_bones) - 1):
            current_bone = bpy.context.object.data.edit_bones.get(spine_bones[i])
            next_bone = bpy.context.object.data.edit_bones.get(spine_bones[i+1])
            
            if current_bone and next_bone:
                # 如果当前骨骼的尾部不等于下一个骨骼的头部，调整位置
                if (current_bone.tail - next_bone.head).length > 0.001:
                    print(f"修复骨骼连续性: {current_bone.name} -> {next_bone.name}")
                    next_bone.head = current_bone.tail
        # 返回物体模式
        bpy.ops.object.mode_set(mode='OBJECT')

    def execute(self, context: bpy.types.Context):

        mmr = context.object.mmr

        # 获取当前运行的Py文件的路径
        current_file_path = __file__
        # 获取当前Py文件所在的文件夹路径
        new_path = os.path.dirname(current_file_path)
        # 将当前文件夹路径和文件名组合成完整的文件路径
        file = mmr.presets + '.json'
        new_file_path = os.path.join(new_path, 'presets', file)

        if mmr.Import_presets:
            new_file_path = mmr.json_filepath

        # 读取json文件
        with open(new_file_path) as f:
            config = json.load(f)

        # 检测是否开启rigify
        if 'rigify' not in bpy.context.preferences.addons.keys():
            logging.info("检测到未开启rigify，已自动开启")
            bpy.ops.preferences.addon_enable(module="rigify")

        # 切换物体模式
        bpy.ops.object.mode_set(mode='OBJECT')
        # 当前活动物体名称
        Arm_name = bpy.context.active_object.name
        print("当前活动骨骼名称:", Arm_name)

        my_object = bpy.data.objects[Arm_name]
        if my_object in bpy.context.selected_objects:
            print('有活动骨骼')
        else:
            self.report({'ERROR'}, '未选中骨骼!')
            return {'FINISHED'}

        obj1 = bpy.data.objects[Arm_name]
        # 获取世界矩阵
        world_matrix1 = obj1.matrix_world
        # 获取世界空间坐标
        location1 = world_matrix1.translation

        # 复制物体
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, 0),
                                                              "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
        # 当前复制物体名称
        Arm2_name = bpy.context.active_object.name
        print("当前复制骨骼名称:", Arm2_name)
        # 复制物体
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, 0),
                                                              "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
        # 当前复制物体名称
        Arm3_name = bpy.context.active_object.name
        print("当前复制骨骼名称:", Arm3_name)

        # Rig骨架
        bpy.ops.object.armature_human_metarig_add()
        # 当前活动物体名称
        Rig_name = bpy.context.active_object.name
        print("当前活动骨骼名称:", Rig_name)
        # 获取对象引用
        obj2 = bpy.data.objects[Rig_name]
        # 设置Rig骨架的世界空间坐标为得到的mmd骨架坐标
        obj2.location = location1
        # 清空选择
        bpy.ops.object.select_all(action='DESELECT')

        # 选择Arm2相关操作
        # 选择物体
        bpy.ops.object.select_pattern(pattern=Arm2_name)
        obj = bpy.data.objects[Arm2_name]
        # 将该物体设置为活动对象
        bpy.context.view_layer.objects.active = obj
        # 进入姿态模式
        bpy.ops.object.mode_set(mode='POSE')
        # 清空选择
        bpy.ops.pose.select_all(action='DESELECT')
        # 将该骨骼设置为活动对象
        bpy.context.active_object.pose.bones[config['頭']].bone.select = True
        bpy.context.active_object.data.bones.active = bpy.context.active_object.pose.bones[config['頭']].bone
        obj = bpy.context.active_object
        bone = obj.pose.bones[config['頭']]
        head_world = obj.matrix_world @ bone.head
        tail_world = obj.matrix_world @ bone.tail
        print("骨骼头部世界空间坐标:", head_world)
        print("骨骼尾部世界空间坐标:", tail_world)
        new_tail_world = tail_world

        # 选择Rig相关操作
        # 选择物体
        bpy.ops.object.select_pattern(pattern=Rig_name)
        obj = bpy.data.objects[Rig_name]
        # 将该物体设置为活动对象
        bpy.context.view_layer.objects.active = obj
        # 进入姿态模式
        bpy.ops.object.mode_set(mode='POSE')
        # 清空选择
        bpy.ops.pose.select_all(action='DESELECT')
        # 将该骨骼设置为活动对象
        bpy.context.active_object.pose.bones['face'].bone.select = True
        bpy.context.active_object.data.bones.active = bpy.context.active_object.pose.bones['face'].bone

        # 获取特定骨骼的姿势对象
        pose_bone = obj.pose.bones["face"]

        # 获取骨骼头部在世界空间中的坐标
        head_world1 = obj.matrix_world @ pose_bone.head
        # 获取骨骼尾部在世界空间中的坐标
        tail_world1 = obj.matrix_world @ pose_bone.tail
        print("骨骼头部世界空间坐标:", head_world1)
        print("骨骼尾部世界空间坐标:", tail_world1)

        # 获取当前骨骼（'face'骨骼）在局部空间中的尾部坐标
        current_tail_local = pose_bone.tail
        # 根据定义好的new_tail_world计算在当前物体的局部空间下的新的尾部坐标
        # 先通过obj的逆世界矩阵乘以new_tail_world得到新的局部坐标
        new_tail_local = obj.matrix_world.inverted() @ new_tail_world
        # 计算偏移量，即新的尾部局部坐标与当前尾部局部坐标的差值
        # 这个偏移量将用于后续对骨骼矩阵的调整
        offset_local = new_tail_local - current_tail_local
        # 根据计算得到的偏移量创建一个平移矩阵
        # 这个平移矩阵将用于对骨骼矩阵进行平移操作
        translation_matrix = mathutils.Matrix.Translation(offset_local)
        # 获取当前骨骼（'face'骨骼）的原始矩阵
        bone_matrix = pose_bone.matrix
        # 将平移矩阵与原始骨骼矩阵相乘，得到新的骨骼矩阵
        # 这一步实现了对骨骼矩阵的平移变换
        new_bone_matrix = translation_matrix @ bone_matrix
        # 将新的骨骼矩阵赋值给当前骨骼（'face'骨骼）的矩阵
        # 从而实现了对骨骼姿态的更新
        pose_bone.matrix = new_bone_matrix

        # 应用姿态
        bpy.ops.pose.armature_apply(selected=False)
        # 切换物体模式
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # 融并骨骼
        # 使用方式:Merge_bones('骨架','骨骼')
        def Merge_bones(Arm, bones):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm)
            obj = bpy.data.objects[Arm]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=bones)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(bones)
            bpy.context.edit_object.data.edit_bones.active = bone
            # 融并骨骼
            bpy.ops.armature.dissolve('INVOKE_DEFAULT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')

        # 加骨骼长度
        # 使用方式:Reduce_bone_length('骨架','骨骼',长度)
        def Reduce_bone_length(Arm, bones, length):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm)
            obj = bpy.data.objects[Arm]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=bones)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(bones)
            bpy.context.edit_object.data.edit_bones.active = bone
            # 减少骨骼长度
            lengths = bpy.context.active_bone.length
            print("骨骼长度为：", lengths)
            bpy.context.active_bone.length = lengths + length
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')

        # 复制扭转值
        def bone_roll(Arn, MMD_bone, Arn1, Rig_bone):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arn)
            obj = bpy.data.objects[Arn]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=MMD_bone, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(MMD_bone)
            bpy.context.edit_object.data.edit_bones.active = bone

            Rig_roll = bpy.context.active_bone.roll
            print(f"骨骼{bone.name}的扭转（滚动）值: {Rig_roll:.6f}")

            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arn1)
            obj = bpy.data.objects[Arn1]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=Rig_bone, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(Rig_bone)
            bpy.context.edit_object.data.edit_bones.active = bone

            # 设置扭转值
            bpy.context.active_bone.roll = Rig_roll
            Arm2_ROLL = bpy.context.active_bone.roll
            print(f"骨骼{bone.name}的扭转（滚动）值: {Arm2_ROLL:.6f}")
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        # 修正约束骨骼扭转值，公式：原骨骼 - 处理完的骨骼 = 差值
        #                      差值 + 约束骨骼 = 扭转值（修正）
        def correct_roll(Arm):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm3_name)
            obj = bpy.data.objects[Arm3_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=Arm, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(Arm)
            bpy.context.edit_object.data.edit_bones.active = bone

            Arm3_roll = bpy.context.active_bone.roll
            print(f"骨骼{bone.name}的扭转（滚动）值: {Arm3_roll:.6f}")

            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm2_name)
            obj = bpy.data.objects[Arm2_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=Arm, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(Arm)
            bpy.context.edit_object.data.edit_bones.active = bone

            Arm2_ROLL = bpy.context.active_bone.roll
            print(f"骨骼{bone.name}的扭转（滚动）值: {Arm2_ROLL:.6f}")
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm_name)
            obj = bpy.data.objects[Arm_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')

            # 选择活动骨骼
            bpy.ops.object.select_pattern(pattern=Arm, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(Arm)
            bpy.context.edit_object.data.edit_bones.active = bone

            Arm_roll = bpy.context.active_bone.roll
            deviation = Arm3_roll - Arm2_ROLL
            Torsion_Value = deviation + Arm_roll
            bpy.context.active_bone.roll = Torsion_Value
            print(f"骨骼{bone.name}的扭转（滚动）值: {Torsion_Value:.6f}")
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        # 对MMD骨骼进行处理
        def Handle_MMD_bones():

            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm2_name)
            obj = bpy.data.objects[Arm2_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 获取当前正在运行的Python文件的路径并打印
            current_file_path = __file__
            print('当前py文件的路径是:', current_file_path)

            # 获取当前Python文件所在的文件夹路径并打印
            new_path = os.path.dirname(current_file_path)
            print('当前文件夹是:', new_path)

            # 将当前文件夹路径和文件名'Initial_pose.vmd'组合成完整的文件路径，并打印
            file_name = 'Initial_pose.vmd'
            new_file_path = os.path.join(new_path, file_name)
            print('包含VMD文件的路径是:', new_file_path)

            # 获取结束帧数值
            gfdt = bpy.context.scene.frame_end

            # 自定初始姿势
            if mmr.Initial_pose:
                new_file_path = mmr.filepath
                file_name = os.path.basename(new_file_path)
                new_path = os.path.dirname(new_file_path)
            if mmr.Bend_the_bones:
                # 导入初始姿势VMD文件
                bpy.ops.mmd_tools.import_vmd(filepath=new_file_path,
                                            files=[{"name": file_name, "name": file_name}],
                                            directory=new_path)

            The_current_frame = bpy.context.scene.frame_current
            # 当前帧设置为第6帧
            bpy.context.scene.frame_current = 7
            # 恢复原来的结束帧数值
            bpy.context.scene.frame_end = gfdt

            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            # 应用姿态
            bpy.ops.pose.armature_apply(selected=False)
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            print(f'骨骼：{Arm_name}处理完成')
            bpy.context.scene.frame_current = The_current_frame

        # 删除骨骼
        def Del_bones(Arm, bones):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm)
            obj = bpy.data.objects[Arm]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 删除骨骼
            bone_names = bones
            for bone_name in bone_names:
                print('删除骨骼：', bone_name)
                bpy.ops.armature.select_all(action='DESELECT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern=bone_name)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get(bone_name)
                bpy.context.edit_object.data.edit_bones.active = bone
                bpy.ops.armature.delete()
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')

        # 与mmd骨骼对齐
        # 使用方式:Movethe_head_and_tail_of_the_bones('mmd骨骼', 'rig骨骼')
        def Movethe_head_and_tail_of_the_bones(arm, arm1):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm2_name)
            obj = bpy.data.objects[Arm2_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 判断骨骼是否存在
            bone_name = arm
            if bone_name in obj.data.bones:
                print(f"骨骼 {bone_name} 存在。")
                # 切换到编辑模式
                bpy.ops.object.mode_set(mode='EDIT')
                # 取消所有选择
                bpy.ops.armature.select_all(action='DESELECT')
                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern=arm, extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get(arm)
                bpy.context.edit_object.data.edit_bones.active = bone

                arm_head = bpy.context.active_bone.head
                arm_tail = bpy.context.active_bone.tail
                arm_roll = bpy.context.active_bone.roll
                print(f"骨骼 {bone.name}")
                print(f"骨骼{bone.name}的头部坐标: ({arm_head[0]:.6f}, {arm_head[1]:.6f}, {arm_head[2]:.6f})")
                print(f"骨骼{bone.name}的尾端坐标: ({arm_tail[0]:.6f}, {arm_tail[1]:.6f}, {arm_tail[2]:.6f})")
                print(f"骨骼{bone.name}的扭转（滚动）值: {arm_roll:.6f}")
                print('头部:', arm_head, '\n尾端:', arm_tail)
                # 全局变量
                prope_x = arm_head[0]
                prope_y = arm_head[1]
                prope_z = arm_head[2]
                etfhu_x = arm_tail[0]
                etfhu_y = arm_tail[1]
                etfhu_z = arm_tail[2]

                # 切换物体模式
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                # 选择物体
                bpy.ops.object.select_pattern(pattern=Rig_name)
                obj = bpy.data.objects[Rig_name]
                # 将该物体设置为活动对象
                bpy.context.view_layer.objects.active = obj
                # 切换到编辑模式
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')

                # 选择活动骨骼
                bpy.ops.object.select_pattern(pattern=arm1, extend=False)
                armature = bpy.context.edit_object.data
                bone = armature.edit_bones.get(arm1)
                bpy.context.edit_object.data.edit_bones.active = bone

                # 反向
                fguk = ['spine']  # 指定骨骼列表
                for element in fguk:
                    if element != bone.name:
                        bpy.context.active_bone.head[0] = prope_x  # 修改头部的x坐标
                        bpy.context.active_bone.head[1] = prope_y  # 修改头部的y坐标
                        bpy.context.active_bone.head[2] = prope_z  # 修改头部的z坐标
                        bpy.context.active_bone.tail[0] = etfhu_x  # 修改尾部的x坐标
                        bpy.context.active_bone.tail[1] = etfhu_y  # 修改尾部的y坐标
                        bpy.context.active_bone.tail[2] = etfhu_z  # 修改尾部的z坐标
                    else:
                        print('骨骼', element, '头尾相反')
                        bpy.context.active_bone.head[0] = etfhu_x  # 修改头部的x坐标
                        bpy.context.active_bone.head[1] = etfhu_y  # 修改头部的y坐标
                        bpy.context.active_bone.head[2] = etfhu_z  # 修改头部的z坐标
                        bpy.context.active_bone.tail[0] = prope_x  # 修改尾部的x坐标
                        bpy.context.active_bone.tail[1] = prope_y  # 修改尾部的y坐标
                        bpy.context.active_bone.tail[2] = prope_z  # 修改尾部的z坐标
                        bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked": False}, TRANSFORM_OT_translate={
                            "value": (0.0, 0.1, -0.0), "orient_type": 'GLOBAL',
                            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
                        bpy.context.active_bone.tail[0] = etfhu_x  # 修改尾部的x坐标
                        bpy.context.active_bone.tail[1] = etfhu_y  # 修改尾部的y坐标
                        bpy.context.active_bone.tail[2] = etfhu_z  # 修改尾部的z坐标
                        bpy.context.active_bone.name = "spine_007"
                        bpy.ops.armature.select_all(action='DESELECT')

                        # 新增的额外处理
                        # 确保 spine.004 连接到 spine.003
                        if bone.name == 'spine.004':
                            spine003 = armature.edit_bones.get('spine.003')
                            if spine003:
                                print(f"确保 {bone.name} 连接到 spine.003")
                                bpy.context.active_bone.head = spine003.tail

                        # 选择活动骨骼
                        bpy.ops.object.select_pattern(pattern="spine_007", extend=False)
                        armature = bpy.context.edit_object.data
                        bone = armature.edit_bones.get("spine_007")
                        bpy.context.edit_object.data.edit_bones.active = bone
                        bpy.ops.armature.parent_clear(type='DISCONNECT')

                print(f"骨骼 {bone.name}")
                Rig_head = bpy.context.active_bone.head
                Rig_tail = bpy.context.active_bone.tail
                Rig_roll = bpy.context.active_bone.roll
                print(f"骨骼{bone.name}的头部坐标: ({Rig_head[0]:.6f}, {Rig_head[1]:.6f}, {Rig_head[2]:.6f})")
                print(f"骨骼{bone.name}的尾端坐标: ({Rig_tail[0]:.6f}, {Rig_tail[1]:.6f}, {Rig_tail[2]:.6f})")
                print(f"骨骼{bone.name}的扭转（滚动）值: {Rig_roll:.6f}")

                bpy.ops.armature.select_all(action='DESELECT')

                # 切换物体模式
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                print(f"骨骼 {bone_name} 不存在。")

        # 删除物体
        def delete_object(object_name):
            object_to_delete = bpy.data.objects.get(object_name)
            if object_to_delete is not None:
                bpy.context.view_layer.objects.active = object_to_delete
                # 遍历当前视图层中的所有物体
                for obj in bpy.context.view_layer.objects:
                    # 取消每个物体的选择状态
                    obj.select_set(False)
                # 将需要删除的物体设置为选中状态
                object_to_delete.select_set(True)
                # 执行删除物体的操作
                bpy.ops.object.delete()

        # 加复制变换约束
        def Add_constraints(Arm2, Arm):

            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm_name)
            obj = bpy.data.objects[Arm_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 判断骨骼是否存在
            bone_name = Arm2
            if bone_name in obj.data.bones:
                print(f"骨骼 {bone_name} 存在。")
                # 切换物体模式
                bpy.ops.object.mode_set(mode='OBJECT')

                bpy.ops.object.select_all(action='DESELECT')
                # 选择物体
                bpy.ops.object.select_pattern(pattern=Arm_name)
                obj = bpy.data.objects[Arm_name]
                # 将该物体设置为活动对象
                bpy.context.view_layer.objects.active = obj
                # 进入姿态模式
                bpy.ops.object.mode_set(mode='POSE')
                # 清空选择
                bpy.ops.pose.select_all(action='DESELECT')

                # 将该骨骼设置为活动对象
                bpy.context.active_object.pose.bones[Arm2].bone.select = True;
                bpy.context.active_object.data.bones.active = bpy.context.active_object.pose.bones[Arm2].bone
                # 添加约束
                bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
                # 获取新的约束名称
                constraint_name = bpy.context.active_object.pose.bones[Arm2].constraints[-1].name
                # 改名称
                constraints_name1 = 'MMR_复制变换'
                bpy.context.object.pose.bones[Arm2].constraints[constraint_name].name = constraints_name1
                # 设置参数
                bpy.context.object.pose.bones[Arm2].constraints[constraints_name1].target = bpy.data.objects[
                    Rigify_name]
                bpy.context.object.pose.bones[Arm2].constraints[constraints_name1].subtarget = Arm

                print(f"骨骼 {bone_name}已添加约束。")

                bone_roll(Rigify_name, Arm, Arm_name, Arm2)

                correct_roll(Arm2)

                # 切换物体模式
                bpy.ops.object.mode_set(mode='OBJECT')
                # 清空选择
                bpy.ops.object.select_all(action='DESELECT')

            else:
                print(f"骨骼 {bone_name} 不存在。")

        # 选择活动骨骼
        def Select_the_bones(arm):

            bpy.ops.object.select_pattern(pattern=arm, extend=False)
            armature = bpy.context.edit_object.data
            bone = armature.edit_bones.get(arm)
            bpy.context.edit_object.data.edit_bones.active = bone

        # 加骨骼父级
        def Add_the_bone_parent(a, b):

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')

            # 获取骨架对象
            armature = bpy.context.object

            # 获取父骨骼和子骨骼
            parent_bone = armature.data.edit_bones.get(b)
            child_bone = armature.data.edit_bones.get(a)

            # 设置父子关系
            child_bone.parent = parent_bone

        # 复制父级骨骼
        def Bone_Parent(bones):

            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Rigify_name)
            obj = bpy.data.objects[Rigify_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            # 切换到编辑模式
            bpy.ops.object.mode_set(mode='EDIT')
            # 取消所有选择
            bpy.ops.armature.select_all(action='DESELECT')
            # 选择活动骨骼
            Select_the_bones(bones)
            # 复制
            bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names": False},
                                            TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL',
                                                                    "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
            # 改名称
            bpy.context.active_bone.name = bones + '_parent'
            sergv_bone = bpy.context.active_bone.name
            # 清空父级
            bpy.ops.armature.parent_clear(type='CLEAR')

            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            # 删除当前选中骨骼所有约束
            pose_bones = bpy.context.selected_pose_bones

            for bone in pose_bones:
                for constraint in bone.constraints:
                    bone.constraints.remove(constraint)

        # 复制旋转
        def Copy_the_rotation(Arm, bone, bones):
            # 切换物体模式
            bpy.ops.object.mode_set(mode='OBJECT')
            # 清空选择
            bpy.ops.object.select_all(action='DESELECT')
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm)
            obj = bpy.data.objects[Arm]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj
            # 判断骨骼是否存在
            bone_name = bone
            if bone_name in obj.data.bones:
                print(f"骨骼 {bone_name} 存在。")
                # 切换物体模式
                bpy.ops.object.mode_set(mode='OBJECT')

                bpy.ops.object.select_all(action='DESELECT')
                # 选择物体
                bpy.ops.object.select_pattern(pattern=Arm)
                obj = bpy.data.objects[Arm]
                # 将该物体设置为活动对象
                bpy.context.view_layer.objects.active = obj
                # 进入姿态模式
                bpy.ops.object.mode_set(mode='POSE')
                # 清空选择
                bpy.ops.pose.select_all(action='DESELECT')

                # 将该骨骼设置为活动对象
                bpy.context.active_object.pose.bones[bone].bone.select = True;
                bpy.context.active_object.data.bones.active = bpy.context.active_object.pose.bones[bone].bone
                # 添加约束
                bpy.ops.pose.constraint_add(type='COPY_ROTATION')
                # 获取新的约束名称
                constraint_name = bpy.context.active_object.pose.bones[bone].constraints[-1].name
                # 改名称
                constraints_name = 'MMR_复制旋转'
                bpy.context.object.pose.bones[bone].constraints[constraint_name].name = constraints_name
                # 设置参数
                bpy.context.object.pose.bones[bone].constraints[constraints_name].target = bpy.data.objects[Arm]
                bpy.context.object.pose.bones[bone].constraints[constraints_name].subtarget = bones
                bpy.context.object.pose.bones[bone].constraints[constraints_name].influence = 0.5
                print(f"骨骼 {bone_name}已添加约束。")

        # 处理
        Handle_MMD_bones()

        # 左侧肢体部分
        Movethe_head_and_tail_of_the_bones(config['腕.L'], config['Arm.L'])
        Movethe_head_and_tail_of_the_bones(config['ひじ.L'], config['forearm.L'])
        Movethe_head_and_tail_of_the_bones(config['手首.L'], config['hand.L'])
        Movethe_head_and_tail_of_the_bones(config['肩.L'], config['shoulder.L'])
        Movethe_head_and_tail_of_the_bones(config['足.L'], config['thigh.L'])
        Movethe_head_and_tail_of_the_bones(config['ひざ.L'], config['shin.L'])
        Movethe_head_and_tail_of_the_bones(config['足首.L'], config['foot.L'])
        Movethe_head_and_tail_of_the_bones(config['足先EX.L'], config['toe.L'])
        Movethe_head_and_tail_of_the_bones(config['足首D.L'], config['heel.L'])

        # 右侧肢体部分
        Movethe_head_and_tail_of_the_bones(config['腕.R'], config['Arm.R'])
        Movethe_head_and_tail_of_the_bones(config['ひじ.R'], config['forearm.R'])
        Movethe_head_and_tail_of_the_bones(config['手首.R'], config['hand.R'])
        Movethe_head_and_tail_of_the_bones(config['肩.R'], config['shoulder.R'])
        Movethe_head_and_tail_of_the_bones(config['足.R'], config['thigh.R'])
        Movethe_head_and_tail_of_the_bones(config['ひざ.R'], config['shin.R'])
        Movethe_head_and_tail_of_the_bones(config['足首.R'], config['foot.R'])
        Movethe_head_and_tail_of_the_bones(config['足先EX.R'], config['toe.R'])
        Movethe_head_and_tail_of_the_bones(config['足首D.R'], config['heel.R'])

        # 身体部分
        Movethe_head_and_tail_of_the_bones(config['下半身'], config['spine'])
        Movethe_head_and_tail_of_the_bones(config['上半身'], config['spine.001'])
        Movethe_head_and_tail_of_the_bones(config['上半身1'], config['spine.002'])
        Movethe_head_and_tail_of_the_bones(config['上半身3'], config['spine.002'])
        Movethe_head_and_tail_of_the_bones(config['上半身2'], config['spine.003'])
        Merge_bones(Rig_name, config['spine.004'])
        Movethe_head_and_tail_of_the_bones(config['首'], config['spine.004'])
        Movethe_head_and_tail_of_the_bones(config['頭'], config['spine.006'])
        Movethe_head_and_tail_of_the_bones(config['頭'], config['face'])
        Movethe_head_and_tail_of_the_bones(config['目.L'], config['eye.L'])
        Movethe_head_and_tail_of_the_bones(config['目.R'], config['eye.R'])

        # 大拇指
        Movethe_head_and_tail_of_the_bones(config['親指０.R'], config['thumb.01.R'])
        Movethe_head_and_tail_of_the_bones(config['親指１.R'], config['thumb.02.R'])
        Movethe_head_and_tail_of_the_bones(config['親指２.R'], config['thumb.03.R'])
        # 食指
        Movethe_head_and_tail_of_the_bones(config['人指１.R'], config['palm.01.R'])
        Movethe_head_and_tail_of_the_bones(config['人指１.R'], config['f_index.01.R'])
        Movethe_head_and_tail_of_the_bones(config['人指２.R'], config['f_index.02.R'])
        Movethe_head_and_tail_of_the_bones(config['人指３.R'], config['f_index.03.R'])
        # 中指
        Movethe_head_and_tail_of_the_bones(config['中指１.R'], config['palm.02.R'])
        Movethe_head_and_tail_of_the_bones(config['中指１.R'], config['f_middle.01.R'])
        Movethe_head_and_tail_of_the_bones(config['中指２.R'], config['f_middle.02.R'])
        Movethe_head_and_tail_of_the_bones(config['中指３.R'], config['f_middle.03.R'])
        # 无名指
        Movethe_head_and_tail_of_the_bones(config['薬指１.R'], config['palm.03.R'])
        Movethe_head_and_tail_of_the_bones(config['薬指１.R'], config['f_ring.01.R'])
        Movethe_head_and_tail_of_the_bones(config['薬指２.R'], config['f_ring.02.R'])
        Movethe_head_and_tail_of_the_bones(config['薬指３.R'], config['f_ring.03.R'])
        # 小指
        Movethe_head_and_tail_of_the_bones(config['小指１.R'], config['palm.04.R'])
        Movethe_head_and_tail_of_the_bones(config['小指１.R'], config['f_pinky.01.R'])
        Movethe_head_and_tail_of_the_bones(config['小指２.R'], config['f_pinky.02.R'])
        Movethe_head_and_tail_of_the_bones(config['小指３.R'], config['f_pinky.03.R'])

        # 大拇指
        Movethe_head_and_tail_of_the_bones(config['親指０.L'], config['thumb.01.L'])
        Movethe_head_and_tail_of_the_bones(config['親指１.L'], config['thumb.02.L'])
        Movethe_head_and_tail_of_the_bones(config['親指２.L'], config['thumb.03.L'])

        # 食指
        Movethe_head_and_tail_of_the_bones(config['人指１.L'], config['palm.01.L'])
        Movethe_head_and_tail_of_the_bones(config['人指１.L'], config['f_index.01.L'])
        Movethe_head_and_tail_of_the_bones(config['人指２.L'], config['f_index.02.L'])
        Movethe_head_and_tail_of_the_bones(config['人指３.L'], config['f_index.03.L'])

        # 中指
        Movethe_head_and_tail_of_the_bones(config['中指１.L'], config['palm.02.L'])
        Movethe_head_and_tail_of_the_bones(config['中指１.L'], config['f_middle.01.L'])
        Movethe_head_and_tail_of_the_bones(config['中指２.L'], config['f_middle.02.L'])
        Movethe_head_and_tail_of_the_bones(config['中指３.L'], config['f_middle.03.L'])

        # 无名指
        Movethe_head_and_tail_of_the_bones(config['薬指１.L'], config['palm.03.L'])
        Movethe_head_and_tail_of_the_bones(config['薬指１.L'], config['f_ring.01.L'])
        Movethe_head_and_tail_of_the_bones(config['薬指２.L'], config['f_ring.02.L'])
        Movethe_head_and_tail_of_the_bones(config['薬指３.L'], config['f_ring.03.L'])

        # 小指
        Movethe_head_and_tail_of_the_bones(config['小指１.L'], config['palm.04.L'])
        Movethe_head_and_tail_of_the_bones(config['小指１.L'], config['f_pinky.01.L'])
        Movethe_head_and_tail_of_the_bones(config['小指２.L'], config['f_pinky.02.L'])
        Movethe_head_and_tail_of_the_bones(config['小指３.L'], config['f_pinky.03.L'])

        # 删除多余骨骼
        Del_bones(Rig_name, ['breast.R', 'breast.L', 'pelvis.R', 'pelvis.L'])

        # 清空选择
        bpy.ops.object.select_all(action='DESELECT')
        # 选择物体
        bpy.ops.object.select_pattern(pattern=Rig_name)
        obj = bpy.data.objects[Rig_name]
        # 将该物体设置为活动对象
        bpy.context.view_layer.objects.active = obj

        # 确保脊柱骨骼连续性
        self.ensure_spine_continuity(Rig_name)

        # Rigify
        bpy.ops.pose.rigify_generate('INVOKE_DEFAULT')

        # 当前活动物体名称
        Rigify_name = bpy.context.active_object.name
        print("当前活动骨骼名称:", Rigify_name)
        bpy.context.object.data.collections_all["ORG"].is_visible = True

        # 较正骨骼
        # 眼睛
        Bone_Parent(config['ORG-eye.L'])
        Bone_Parent(config['ORG-eye.R'])

        if mmr.Shoulder_linkage:
            # 肩膀
            Bone_Parent(config['ORG-shoulder.R'])
            Bone_Parent(config['ORG-shoulder.L'])

        # 进入姿态模式
        bpy.ops.object.mode_set(mode='POSE')
        # 应用姿态
        bpy.ops.pose.armature_apply(selected=False)
        # 认义父
        # 眼睛
        Add_the_bone_parent(config['ORG-eye.L_parent'], config['ORG-eye.L'])
        Add_the_bone_parent(config['ORG-eye.R_parent'], config['ORG-eye.R'])

        if mmr.Shoulder_linkage:
            # 肩膀
            Add_the_bone_parent('ORG-shoulder.R_parent', config['ORG-Arm.R'])
            Add_the_bone_parent('ORG-shoulder.L_parent', config['ORG-Arm.L'])

        # 左侧肢体部分
        Add_constraints(config['腕.L'], config['ORG-Arm.L']),
        Add_constraints(config['ひじ.L'], config['ORG-forearm.L']),
        Add_constraints(config['手首.L'], config['ORG-hand.L']),
        Add_constraints(config['肩.L'], config['ORG-shoulder.L']),
        Add_constraints(config['足.L'], config['ORG-thigh.L']),
        Add_constraints(config['ひざ.L'], config['ORG-shin.L']),
        Add_constraints(config['足首.L'], config['ORG-foot.L']),
        Add_constraints(config['足先EX.L'], config['ORG-toe.L']),

        # 右侧肢体部分
        Add_constraints(config['腕.R'], config['ORG-Arm.R']),
        Add_constraints(config['ひじ.R'], config['ORG-forearm.R']),
        Add_constraints(config['手首.R'], config['ORG-hand.R']),
        Add_constraints(config['肩.R'], config['ORG-shoulder.R']),
        Add_constraints(config['足.R'], config['ORG-thigh.R']),
        Add_constraints(config['ひざ.R'], config['ORG-shin.R']),
        Add_constraints(config['足首.R'], config['ORG-foot.R']),
        Add_constraints(config['足先EX.R'], config['ORG-toe.R']),

        # 身体部分
        Add_constraints(config['下半身'], config['ORG-spine_007']),
        Add_constraints(config['上半身'], config['ORG-spine.001']),
        Add_constraints(config['上半身1'], config['ORG-spine.002']),
        Add_constraints(config['上半身3'], config['ORG-spine.002']),
        Add_constraints(config['上半身2'], config['ORG-spine.003']),
        Add_constraints(config['首'], config['ORG-spine.004']),
        Add_constraints(config['頭'], config['ORG-spine.006']),
        Add_constraints(config['目.L'], config['ORG-eye.L_parent']),
        Add_constraints(config['目.R'], config['ORG-eye.R_parent']),
        # 手指部分
        Add_constraints(config['親指０.R'], config['ORG-thumb.01.R']),
        Add_constraints(config['親指１.R'], config['ORG-thumb.02.R']),
        Add_constraints(config['親指２.R'], config['ORG-thumb.03.R']),
        Add_constraints(config['人指１.R'], config['ORG-f_index.01.R']),
        Add_constraints(config['人指２.R'], config['ORG-f_index.02.R']),
        Add_constraints(config['人指３.R'], config['ORG-f_index.03.R']),
        Add_constraints(config['中指１.R'], config['ORG-f_middle.01.R']),
        Add_constraints(config['中指２.R'], config['ORG-f_middle.02.R']),
        Add_constraints(config['中指３.R'], config['ORG-f_middle.03.R']),
        Add_constraints(config['薬指１.R'], config['ORG-f_ring.01.R']),
        Add_constraints(config['薬指２.R'], config['ORG-f_ring.02.R']),
        Add_constraints(config['薬指３.R'], config['ORG-f_ring.03.R']),
        Add_constraints(config['小指１.R'], config['ORG-f_pinky.01.R']),
        Add_constraints(config['小指２.R'], config['ORG-f_pinky.02.R']),
        Add_constraints(config['小指３.R'], config['ORG-f_pinky.03.R']),
        Add_constraints(config['親指０.L'], config['ORG-thumb.01.L']),
        Add_constraints(config['親指１.L'], config['ORG-thumb.02.L']),
        Add_constraints(config['親指２.L'], config['ORG-thumb.03.L']),
        Add_constraints(config['人指１.L'], config['ORG-f_index.01.L']),
        Add_constraints(config['人指２.L'], config['ORG-f_index.02.L']),
        Add_constraints(config['人指３.L'], config['ORG-f_index.03.L']),
        Add_constraints(config['中指１.L'], config['ORG-f_middle.01.L']),
        Add_constraints(config['中指２.L'], config['ORG-f_middle.02.L']),
        Add_constraints(config['中指３.L'], config['ORG-f_middle.03.L']),
        Add_constraints(config['薬指１.L'], config['ORG-f_ring.01.L']),
        Add_constraints(config['薬指２.L'], config['ORG-f_ring.02.L']),
        Add_constraints(config['薬指３.L'], config['ORG-f_ring.03.L']),
        Add_constraints(config['小指１.L'], config['ORG-f_pinky.01.L']),
        Add_constraints(config['小指２.L'], config['ORG-f_pinky.02.L']),
        Add_constraints(config['小指３.L'], config['ORG-f_pinky.03.L']),

        # 切换物体模式
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # 选择物体
        bpy.ops.object.select_pattern(pattern=Rigify_name)
        obj = bpy.data.objects[Rigify_name]
        # 将该物体设置为活动对象
        bpy.context.view_layer.objects.active = obj

        bpy.context.object.data.collections_all["ORG"].is_visible = False
        # 设置可见性
        bpy.context.object.data.collections_all["Face (Primary)"].is_visible = False
        bpy.context.object.data.collections_all["Face (Secondary)"].is_visible = False
        bpy.context.object.data.collections_all["Torso (Tweak)"].is_visible = False
        bpy.context.object.data.collections_all["Fingers (Detail)"].is_visible = False
        bpy.context.object.data.collections_all["Arm.L (FK)"].is_visible = False
        bpy.context.object.data.collections_all["Arm.R (FK)"].is_visible = False
        bpy.context.object.data.collections_all["Arm.L (Tweak)"].is_visible = False
        bpy.context.object.data.collections_all["Arm.R (Tweak)"].is_visible = False
        bpy.context.object.data.collections_all["Leg.L (FK)"].is_visible = False
        bpy.context.object.data.collections_all["Leg.R (FK)"].is_visible = False
        bpy.context.object.data.collections_all["Leg.L (Tweak)"].is_visible = False
        bpy.context.object.data.collections_all["Leg.R (Tweak)"].is_visible = False
        # 最前面
        bpy.context.object.show_in_front = True

        # 切换到编辑模式
        bpy.ops.object.mode_set(mode='EDIT')
        # 取消所有选择
        bpy.ops.armature.select_all(action='DESELECT')

        # 选择活动骨骼
        Select_the_bones('thigh_ik.L')

        thigh_z = bpy.context.active_bone.tail[2]
        # 取消所有选择
        bpy.ops.armature.select_all(action='DESELECT')
        # 选择活动骨骼
        Select_the_bones('torso')
        # 复制
        bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names": False},
                                        TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL',
                                                                "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1))})
        # 改名称
        bpy.context.active_bone.name = "torso_root"
        # 移动骨骼
        bpy.context.active_bone.tail[2] = thigh_z
        bpy.context.active_bone.head[2] = thigh_z

        bpy.ops.armature.parent_clear(type='CLEAR')

        # 认义父
        Add_the_bone_parent('torso', 'torso_root')
        Add_the_bone_parent('hand_ik.R', 'torso_root')
        Add_the_bone_parent('hand_ik.L', 'torso_root')
        Add_the_bone_parent('torso_root', 'root')

        # 进入姿态模式
        bpy.ops.object.mode_set(mode='POSE')
        # 变形大法
        bpy.context.active_pose_bone.custom_shape = bpy.data.objects["WGT-rig_root"]
        # 各自的原点
        bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        # 自动ik
        bpy.context.object.pose.use_auto_ik = True
        # 隐藏骨骼
        bone_names = ["jaw_master", "teeth.T", "teeth.B", "nose_master", "tongue_master"]
        for bone_name in bone_names:
            if bone_name in bpy.data.objects[Rigify_name].data.bones:
                bone = bpy.data.objects[Rigify_name].data.bones[bone_name]
                bone.hide = True
        # 关闭ik拉伸
        bpy.context.object.pose.bones["thigh_parent.R"]["IK_Stretch"] = 0
        bpy.context.object.pose.bones["thigh_parent.L"]["IK_Stretch"] = 0
        bpy.context.object.pose.bones["upper_arm_parent.L"]["IK_Stretch"] = 0
        bpy.context.object.pose.bones["upper_arm_parent.R"]["IK_Stretch"] = 0

        # 取消所有选择
        bpy.ops.pose.select_all(action='DESELECT')

        # 是否启用级向
        if mmr.Polar_target:
            bones = [('upper_arm_ik.L', 'upper_arm_parent.L'), ('upper_arm_ik.R', 'upper_arm_parent.R')]
            for side in bones:
                ik_bone_name, parent_bone_name = side
                # 选择活动骨骼
                bone = bpy.context.active_object.pose.bones[ik_bone_name].bone
                bone.select = True
                bpy.context.active_object.data.bones.active = bone
                # 启用级向
                bpy.context.object.pose.bones[parent_bone_name]["pole_vector"] = True

                # 取消所有选择
                bpy.ops.pose.select_all(action='DESELECT')

        # 肩膀联动
        if mmr.Shoulder_linkage:
            Copy_the_rotation(Rigify_name, 'shoulder.R', 'ORG-shoulder.R_parent')
            Copy_the_rotation(Rigify_name, 'shoulder.L', 'ORG-shoulder.L_parent')

        bpy.context.active_object.pose.bones['root'].bone.select = True;
        bpy.context.active_object.data.bones.active = bpy.context.active_object.pose.bones['root'].bone

        bpy.ops.pose.select_all(action='DESELECT')
        # 切换物体模式
        bpy.ops.object.mode_set(mode='OBJECT')
        # 改名称
        bpy.context.object.name = Arm_name + '_' + Rigify_name

        bpy.ops.object.select_all(action='DESELECT')

        # 定义一个列表
        object_names = [Rig_name, Arm2_name, Arm3_name]
        # 遍历物体名称列表，调用delete_object函数删除物体
        for object_name in object_names:
            delete_object(object_name)

        if mmr.Bend_the_bones:
            # 设置MMD骨骼
            # 选择物体
            bpy.ops.object.select_pattern(pattern=Arm_name)
            obj = bpy.data.objects[Arm_name]
            # 将该物体设置为活动对象
            bpy.context.view_layer.objects.active = obj

            bpy.context.object.pose.bones["足ＩＫ.L"].mmd_ik_toggle = False
            bpy.context.object.pose.bones["足ＩＫ.R"].mmd_ik_toggle = False
            bpy.context.object.pose.bones["つま先ＩＫ.R"].mmd_ik_toggle = False
            bpy.context.object.pose.bones["つま先ＩＫ.L"].mmd_ik_toggle = False

        # 隐藏物体
        bpy.data.objects[Arm_name].hide_set(True)

        bpy.ops.object.select_all(action='DESELECT')
        self.report({'INFO'}, '优化成功!')
        return {'FINISHED'}


class mmrexportvmdactionsOperator(bpy.types.Operator):
    '''Export VMD actions'''
    bl_idname = "object.mmr_export_vmd"
    bl_label = "Export VMD actions"

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

        # 获取名称
        obj = context.object.name
        obj = obj.removesuffix('_rig')
        print(obj)
        bpy.ops.object.mode_set(mode="OBJECT")
        # 选择物体
        bpy.data.objects[obj].select_set(True)
        # 设为活动物体
        bpy.context.view_layer.objects.active = bpy.data.objects[obj]
        # 取消隐藏物体
        bpy.data.objects[obj].hide_set(False)
        # 姿态模式
        bpy.ops.object.mode_set(mode="POSE")

        # 检查所有的骨骼，如果有名称为"MMR_复制变换"的骨骼约束，则选中
        armature = context.object
        for bone in armature.pose.bones:
            for constraint in bone.constraints:
                if constraint.name == "MMR_复制变换":
                    bone.bone.select = True
                    break

        start = bpy.context.scene.frame_start
        end = bpy.context.scene.frame_end

        bpy.ops.nla.bake(frame_start=start, frame_end=end, visual_keying=True, bake_types={'POSE'})

        bpy.ops.mmd_tools.export_vmd("INVOKE_DEFAULT")

        return {'FINISHED'}
