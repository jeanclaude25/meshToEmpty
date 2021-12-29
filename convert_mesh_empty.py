bl_info = {
    "name": "Meshes_to_emptys",
    "description": "Convert Meshes to emptys",
    "author": "Jeanclaude Stephane",
    "location": "View3D > Toolshelf > Object",
    "warning": "",
    "wiki_url": "",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "category": "Object"}

import bpy





# ------------------------------------------------------------------------
#    Instance System - Convert Meshs to Instances
# ------------------------------------------------------------------------

class Meshs_to_emptys(bpy.types.Operator):
    """Convert meshs to emptys"""
    bl_idname = "m2e.id"
    bl_label = "m2e_label"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Selectionner tous les objets
        bpy.ops.object.select_all(action='SELECT')
        #déselectionner les objets non valides (ne prendre que les meshs)
        C = bpy.context.selected_objects
        for ob in C:
            if not ob.type == 'MESH':
                ob.select = False
        C = bpy.context.selected_objects
        
        empties = []
        
        #Regrouper les objets par nom dans different empty
        #print("c0 = "+C[len(C)-1].name)
        #Deselectionner le premier de la liste
        C[len(C)-1].select = False
        C = bpy.context.selected_objects
        
        for obj in C:
            #Ajoute et déplace l'empty
            bpy.ops.object.empty_add(type='PLAIN_AXES',location=obj.matrix_world.to_translation(),rotation=obj.matrix_world.to_euler())
            
            #met la visualisation de cet empty à 1
            bpy.context.object.empty_draw_size = 1
            
            active = bpy.context.scene.objects.active
            #Sépare le nom des .XXX
            nom = obj.name.split(".")
            active.name = nom[0] +'_inst.' + nom[1]
            
            #copie le scale
            active.scale = obj.scale
            print(active.name)
            empties.append(active)
            

        for obj in C:
            bpy.data.objects.remove(obj,do_unlink=True)
            
          
        #for obj in empties:
        #    obj.name = obj.name[:-len('_duplicata')]
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Instance System - Convert Instances to Meshs
# ------------------------------------------------------------------------
class Emptys_to_meshs(bpy.types.Operator):
    """Convert emptys to meshes"""
    bl_idname = "e2m.id"
    bl_label = "e2m_label"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Selectionne tous les objets
        bpy.ops.object.select_all(action='SELECT')
        #déselectionner les objets non valides (ne prendre que les empties)
        C = bpy.context.selected_objects
        for ob in C:
            if not ob.type == 'EMPTY':
                ob.select = False
        C = bpy.context.selected_objects
        #Creer un objet
        bpy.ops.mesh.primitive_plane_add()
        instance = context.active_object
        #Pour chaque objet
        for ob in C:
            #tester au préalable si le nom contient (instance)
            if not ob.name.find('_inst') == -1:
                #Supprimer dans le nom les ".", les chiffres et les "_instances"
                nom = ob.name.split(".")
                #nom[0]
                #Deselectionner tout les objets
                bpy.ops.object.select_all(action='DESELECT')
                #Selectionner l'objet instance
                instance.select = True
                #Dupliquer l'objet instance et le déplacer au bon endroit
                bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":ob.matrix_world.to_translation()})
                #Enregistre l'objet creer
                mesh = context.active_object
                #scaler, rotationner l'objet
                #mesh.matrix_world = ob.matrix_world
                mesh.rotation_euler = ob.rotation_euler
                mesh.scale = ob.scale
                #bpy.ops.transform.rotate(value = ob.matrix_world.to_euler() )
                #changer son objet avec le nom en question
                #Enregistrer l'empty dans une liste
        #Supprimer la liste d'empty fraichement enregistré
        #Supprimer l'instance
        instance.remove()
                
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Rename Emptys
# ------------------------------------------------------------------------
class Rename_emptys(bpy.types.Operator):
    """Rename selected emptys"""
    bl_idname = "ren_em.id"
    bl_label = "ren_em_label"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Enregistre tous les  obj selectionné
        C = bpy.context.selected_objects
        for ob in C:
            if ob.type == 'MESH':
                sel_obj = ob
                ob.select = False
                
        #enregistre les obj restants
        C = bpy.context.selected_objects
        #Renomme tous les emptys
        cre = 1000
        for ob in C:
            if ob.type == 'EMPTY':
                ob.name = sel_obj.name + '.000_' + str(cre)
                cre = cre + 1
        
        return {'FINISHED'}
    
                
# ------------------------------------------------------------------------
#   Uniform empty size
# ------------------------------------------------------------------------
class Uniform_emptys(bpy.types.Operator):
    """Uniform emptys Size"""
    bl_idname = "uni_emp.id"
    bl_label = "uni_emp_label"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):        
        C = bpy.context.selected_objects
        for ob in C:
            if not ob.type == 'EMPTY':
                ob.select = False
                
        C = bpy.context.selected_objects
        
        for ob in C:
            bpy.context.scene.objects.active = ob
            bpy.context.object.empty_draw_size = 0.1
        
        
        return {'FINISHED'}
    
    
# ------------------------------------------------------------------------
#   Snap emptys
# ------------------------------------------------------------------------
class Snap_emptys(bpy.types.Operator):
    """Snap emptys"""
    bl_idname = "snap_emp.id"
    bl_label = "snap_emp_label"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):        
        C = bpy.context.selected_objects
        for ob in C:
            if ob.type == 'MESH':
                mesh = ob
                mesh.select = False
            if ob.type == 'EMPTY':
                empt = ob
                bpy.context.scene.objects.active = ob
        
        #Dupliquer l'empty et le déplacer sur l'objet
        bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":mesh.matrix_world.to_translation()-empt.matrix_world.to_translation()})
        #Enregistre l'objet creer
        empt = context.active_object
        #prendre egalement sa rotation
        empt.rotation_euler = mesh.rotation_euler
        
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select = True
        bpy.context.scene.objects.active = mesh
        #supprimer le mesh
        bpy.ops.object.delete()
        #Reselectionne a nouveau l'empty cree
        empt.select = True
        bpy.context.scene.objects.active = empt
        
        return {'FINISHED'}
    
    
    
class InstanceSystemPanel(bpy.types.Panel):
    """Instance to emptys"""
    bl_label = "Instance Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        
        split = layout.split()
        
        row = layout.row()
        col = split.column(align=True)
        col.label(text="Instance system")
        row = layout.row()
        row.operator("m2e.id", text="Meshs to Emptys")
        row = layout.row()
        row.operator("ren_em.id", text="rename Emptys")
        row = layout.row()
        row.operator("uni_emp.id", text="Uniform Emptys")
        row = layout.row()
        row.operator("snap_emp.id", text="Snap Emptys")
        #row.operator("m2e.id", text="Particles to Emptys")
        row = layout.row()
        row = layout.row()
        row = layout.row()
        #row.operator("e2m.id", text="Emptys to Meshs")
        
    
def register():
    bpy.utils.register_class(Rename_emptys)
    bpy.utils.register_class(Snap_emptys)
    bpy.utils.register_class(Uniform_emptys)
    bpy.utils.register_class(Meshs_to_emptys)
    bpy.utils.register_class(Emptys_to_meshs)
    bpy.utils.register_class(InstanceSystemPanel)
def unregister():
    bpy.utils.unregister_class(Rename_emptys)
    bpy.utils.unregister_class(Snap_emptys)
    bpy.utils.unregister_class(Uniform_emptys)
    bpy.utils.unregister_class(Meshs_to_emptys)
    bpy.utils.unregister_class(Emptys_to_meshs)
    bpy.utils.unregister_class(InstanceSystemPanel)



if __name__ == "__main__":
    register()