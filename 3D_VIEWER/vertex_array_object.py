from vertex_buffer_object import *


class Vertex_array_object_no_texturing:
    def __init__(self,context,vertices_provider,shader_program):

        self.context = context
        self.vertex_buffer_object = Vertex_buffer_object_no_texturing(context,vertices_provider)
        self.shader_program = shader_program
        self.vertex_array_object = self.get_vertex_array_object(shader_program,self.vertex_buffer_object)
    

    def get_vertex_array_object(self, shader_program, vertex_buffer_object):
        vao = self.context.vertex_array(shader_program.program, [(vertex_buffer_object.vertex_buffer_object, vertex_buffer_object.format, *vertex_buffer_object.attribs)])
        return vao

    def destroy(self):
        self.vertex_buffer_object.destroy()
        self.shader_program.destroy()
        self.vertex_array_object.release()
    
   



class Vertex_array_object_with_texturing:
    def __init__(self,context,vertices_provider_with_texture_coordinates,shader_program):

        self.context = context
        self.vertex_buffer_object = Vertex_buffer_object_with_texturing(context,vertices_provider_with_texture_coordinates)
        self.shader_program = shader_program
        self.vertex_array_object = self.get_vertex_array_object(shader_program,self.vertex_buffer_object)
    

    def get_vertex_array_object(self, shader_program, vertex_buffer_object):
        vao = self.context.vertex_array(shader_program.program, [(vertex_buffer_object.vertex_buffer_object, vertex_buffer_object.format, *vertex_buffer_object.attribs)])
        return vao

    def destroy(self):
        self.vertex_buffer_object.destroy()
        self.shader_program.destroy()
        self.vertex_array_object.release()