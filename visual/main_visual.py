import bpy
import argparse

class MainVisual:
    def __init__(self, scene_name):
        self.scene_name = scene_name
    
    def create_cube(self, size, location, color):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        bpy.ops.primitive_cube_add(location=location)
        bpy.context.object.location[2] = 2

    def create_scene(self, size, location, color, cube):
        if cube:
            self.create_cube(size, location, color)
        bpy.context.scene.render.filepath = f"{self.scene_name}"
        bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scene_name', help='Name of scene', required=True)
    parser.add_argument('-c', '--cube', help='Creates cube')
    parser.add_argument('-si', '--object_size', help='Size of object to add')
    args = parser.parse_args()
    main_vis = MainVisual(args.scene_name)