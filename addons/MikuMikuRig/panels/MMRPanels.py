import bpy

from MikuMikuRig.addons.MikuMikuRig.config import __addon_name__
from MikuMikuRig.addons.MikuMikuRig.operators.RIG import mmdarmoptOperator, mmrexportvmdactionsOperator
from MikuMikuRig.addons.MikuMikuRig.operators.RIG import polartargetOperator
from MikuMikuRig.addons.MikuMikuRig.operators.RIG import mmrrigOperator
from MikuMikuRig.addons.MikuMikuRig.operators.MMRpresets import mmrmakepresetsOperator, mmrdesignatedOperator
from MikuMikuRig.common.i18n.i18n import i18n

class MMD_Arm_Opt(bpy.types.Panel):
    bl_label = "MMD tool"
    bl_idname = "SCENE_PT_MMD_Arm_Opt"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMR"

    def draw(self, context: bpy.types.Context):

        mmr = context.object.mmr

        # 从上往下排列
        layout = self.layout

        if mmr.boolean:
            # 增加按钮大小并添加图标
            row = layout.row()
            row.scale_y = 1.2  # 这将使按钮的垂直尺寸加倍
            row.operator(polartargetOperator.bl_idname, text="Optimization MMD Armature", icon='BONE_DATA')
            col = layout.column_flow(columns=2)

        else:
            # 增加按钮大小并添加图标
            row = layout.row()
            row.scale_y = 1.2  # 这将使按钮的垂直尺寸加倍
            row.operator(mmdarmoptOperator.bl_idname, text="Optimization MMD Armature", icon='BONE_DATA')

        row1 = layout.row()
        row1.prop(mmr, "boolean", text="是否启用极向目标")

        col = layout.column_flow(columns=2)
        col.scale_y = 1.2

        obj = context.active_object
        if obj:
            # 第五个骨骼和约束组合
            bone_name_1 = "ひじ.L"
            constraint_name_1 = "【IK】L"
            obj = bpy.context.object
            if obj and obj.type == 'ARMATURE':
                bone_1 = obj.pose.bones.get(bone_name_1)
                if bone_1:
                    constraint_1 = bone_1.constraints.get(constraint_name_1)
                    if constraint_1:
                        if mmr.boolean:
                            col.prop(constraint_1, "pole_angle", text="手IK.L(极向角度)")

            # 第二个骨骼和约束组合
            bone_name_2 = "手首.L"
            constraint_name_2 = "【复制旋转】.L"
            if obj and obj.type == 'ARMATURE':
                bone_2 = obj.pose.bones.get(bone_name_2)
                if bone_2:
                    constraint_2 = bone_2.constraints.get(constraint_name_2)
                    if constraint_2:
                        col.prop(constraint_2, "influence",text="手IK.L(旋转)")

            # 第一个骨骼和约束组合
            bone_name_1 = "ひじ.L"
            constraint_name_1 = "【IK】L"
            obj = bpy.context.object
            if obj and obj.type == 'ARMATURE':
                bone_1 = obj.pose.bones.get(bone_name_1)
                if bone_1:
                    constraint_1 = bone_1.constraints.get(constraint_name_1)
                    if constraint_1:
                        col.prop(constraint_1, "influence",text="手IK.L(位置)")

            # 第六个骨骼和约束组合
            bone_name_1 = "ひじ.R"
            constraint_name_1 = "【IK】R"
            obj = bpy.context.object
            if obj and obj.type == 'ARMATURE':
                bone_1 = obj.pose.bones.get(bone_name_1)
                if bone_1:
                    constraint_1 = bone_1.constraints.get(constraint_name_1)
                    if constraint_1:
                        if mmr.boolean:
                            col.prop(constraint_1, "pole_angle", text="手IK.R(极向角度)")

            # 第三个骨骼和约束组合
            bone_name_1 = "ひじ.R"
            constraint_name_1 = "【IK】R"
            obj = bpy.context.object
            if obj and obj.type == 'ARMATURE':
                bone_1 = obj.pose.bones.get(bone_name_1)
                if bone_1:
                    constraint_1 = bone_1.constraints.get(constraint_name_1)
                    if constraint_1:
                        col.prop(constraint_1, "influence", text="手IK.R(位置)")

            # 第四个骨骼和约束组合
            bone_name_2 = "手首.R"
            constraint_name_2 = "【复制旋转】.R"
            if obj and obj.type == 'ARMATURE':
                bone_2 = obj.pose.bones.get(bone_name_2)
                if bone_2:
                    constraint_2 = bone_2.constraints.get(constraint_name_2)
                    if constraint_2:
                        col.prop(constraint_2, "influence", text="手IK.R(旋转)")

        layout.operator(mmrexportvmdactionsOperator.bl_idname, text="Export VMD actions", icon='ANIM')

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

class MMD_Rig_Opt(bpy.types.Panel):
    bl_label = "Controller options"
    bl_idname = "SCENE_PT_MMR_Rig_Opt"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MMR"

    def draw(self, context: bpy.types.Context):

        # 从上往下排列
        layout = self.layout

        mmr = context.object.mmr

        if mmr.make_presets:
            if mmr.Import_presets:
                layout.prop(mmr,"json_filepath",text=i18n('presets'))
            else:
                layout.prop(mmr,"presets",text=i18n('presets'))

            row = layout.row()
            row.operator(mmrmakepresetsOperator.bl_idname, text="make presets")
            row.prop(mmr, "Import_presets", text=i18n("Import presets"), toggle=True)

            # 增加按钮大小并添加图标
            layout.scale_y = 1.2  # 这将使按钮的垂直尺寸加倍
            layout.operator(mmrrigOperator.bl_idname, text="Build a controller",icon="OUTLINER_DATA_ARMATURE")

            layout.prop(mmr, "extras_enabled", text=i18n("Extras"), toggle=True,icon="PREFERENCES")

            if mmr.extras_enabled:

                layout.prop(mmr, "Bend_the_bones", text=i18n("Bend the bones"))

                layout.prop(mmr, "Polar_target", text=i18n("Polar target"))

                layout.prop(mmr, "Shoulder_linkage", text=i18n("Shoulder linkage"))
                if mmr.Shoulder_linkage:
                    layout.label(text=i18n("This option has a serious bug and should not be enabled"),icon='ERROR')

                if mmr.Bend_the_bones:
                    layout.prop(mmr, "Initial_pose", text=i18n("Customize the initial pose"))
                    if mmr.Initial_pose:
                        layout.prop(mmr,"filepath")
        else:
            layout.scale_y = 1.2  # 这将使按钮的垂直尺寸加倍
            layout.prop(mmr, "json_txt")
            row = layout.row()
            if mmr.number < 57:
                row.operator(mmrdesignatedOperator.bl_idname, text="designated")
            row.operator(mmrmakepresetsOperator.bl_idname, text="Exit the designation")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None
