import bpy
import bmesh

class DREAMUV_OT_mat_assign(bpy.types.Operator):
    """Clones the material from the active face to the target faces."""
    bl_idname = "view3d.dreamuv_matassign"
    bl_label = "3D View Clone Material"
    bl_options = {"UNDO"}

    def execute(self, context):

        objs = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        facecounter = 0
        selection = {}

        # I haven't found a way to differentiate between multiple active faces in multi-object editing.
        # For now the "source" object has to be selected last.
        for obj in objs:
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            selected_faces = []
            for f in bm.faces:
                if f.select:
                    facecounter += 1
                    if f is bm.faces.active and obj is active_obj:
                        # Get source material.
                        slot_len = len(obj.material_slots)
                        if f.material_index < 0 or f.material_index >= slot_len:
                            self.report({'INFO'}, "object has no materials, aborting")
                            return {'FINISHED'}
                        
                        material = obj.material_slots[f.material_index].material
                        if material is None:
                            self.report({'INFO'}, "Active face has no material, aborting")
                            return {'FINISHED'}

                    else: selected_faces.append(f)

            if len(selected_faces) > 0:
                selection[obj] = selected_faces

        if facecounter < 2:
            self.report({'INFO'}, "only one face selected, aborting")
            return {'FINISHED'}

        # This creates a lot of duplicate materials. They can be cleaned up in post,
        # but it would be nice if we merged here if possible. 
        # Should also check if the material already exists.
        for obj in selection:
            print(obj)
            obj.data.materials.append(material)
            for f in selection[obj]:
                f.material_index = len(obj.data.materials) - 1

            bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}