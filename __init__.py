
bl_info = {
    "name": "Browser_Scroll_Resizer (BSR)", "author": "Barrunterio",
    "version": (1, 0, 0), "blender": (4, 2, 0), "location": "Add Shortcut Operation",
    "description": "Custom operation to resize content in the file browser using Alt + Scroll Mouse",
    "wiki_url": "", "category": "Interface"}

import bpy, rna_keymap_ui
from bpy.types import AddonPreferences

class TBY_FBSR_prop(bpy.types.PropertyGroup):
    tby_bsr_multiplier_resize_factor: bpy.props.IntProperty(default=10)

#OPERATIONS
class tby_WheelUp(bpy.types.Operator):
    """Increase the size of file Viewer"""
    bl_idname = "tbycontext.filesizeincrease"
    bl_label = "Increase file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        tbytool = context.scene.tby_bsr_tool
        mrf = tbytool.tby_bsr_multiplier_resize_factor
        
        type = context.space_data.params.display_type
        if type == 'LIST_VERTICAL':
            bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'               
        elif type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'THUMBNAIL'
            bpy.context.space_data.params.display_size = 24      
        elif type == 'THUMBNAIL':
            if bpy.context.space_data.params.display_size < 256:
                if (bpy.context.space_data.params.display_size + mrf) >= 256:
                    bpy.context.space_data.params.display_size = 256
                if bpy.context.space_data.params.display_size < 256:
                    bpy.context.space_data.params.display_size = bpy.context.space_data.params.display_size + mrf
        return {'FINISHED'}
class tby_WheelDown(bpy.types.Operator):
    """Decrease the size of file Viewer"""
    bl_idname = "tbycontext.filesizedecrease"
    bl_label = "Decrease file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = bpy.context.window_manager
        tbytool = context.scene.tby_bsr_tool
        mrf = tbytool.tby_bsr_multiplier_resize_factor
        type = context.space_data.params.display_type

        if type == 'THUMBNAIL':
            if bpy.context.space_data.params.display_size > 16:
                if (bpy.context.space_data.params.display_size - mrf) <= 16:
                    bpy.context.space_data.params.display_size = 16
                else:                    
                    bpy.context.space_data.params.display_size = bpy.context.space_data.params.display_size - mrf
            if bpy.context.space_data.params.display_size <= 16:
                bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'
        if type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'LIST_VERTICAL'                                
        return {'FINISHED'}

class TBY_BSR_Preferences_Panel(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        tbytool = context.scene.tby_bsr_tool
         
        box=layout.box()
        box.label(text="Hotkey:")
        col = box.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        row = layout.row()
        col = row.column()
        col.prop(self, "TBOVER", text="")
        box.label(text="Properties:")
        box.prop(tbytool,"tby_bsr_multiplier_resize_factor",text="Multiplier_Factor")


classes = (
    TBY_FBSR_prop,
    tby_WheelDown, tby_WheelUp,
    TBY_BSR_Preferences_Panel)
addon_keymaps = []    

#append_individual_keys
def key(dfbool,km,kmi):
    kmi.active = dfbool
    addon_keymaps.append((km, kmi)) 

def register():
 #CLASS
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.tby_bsr_tool = bpy.props.PointerProperty(type=TBY_FBSR_prop)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:    
    #3Dview
        km = kc.keymaps.new(name='File Browser', space_type='FILE_BROWSER')
        key(True,km,km.keymap_items.new("tbycontext.filesizedecrease", 'WHEELOUTMOUSE', 'PRESS', alt=True))
        key(True,km,km.keymap_items.new("tbycontext.filesizeincrease", 'WHEELINMOUSE', 'PRESS', alt=True))
    #bpy.utils.register_class(TBY_FBSR_prop)
    #bpy.types.WindowManager.TBY_FBSR_prop_wm = bpy.props.PointerProperty(type=TBY_FBSR_prop)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.tby_bsr_tool
    
    #KEYMAP
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()   

    bpy.utils.unregister_class(TBY_FBSR_prop)
    
if __name__ == "__main__":
    register()
