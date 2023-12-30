
class Vertex_buffer_object_no_texturing:

    def __init__(self, context,vertices_provider):
        self.context = context
        self.vertex_buffer_object = self.get_vertex_buffer_data(vertices_provider)
        self.format = '3f 3f'
        self.attribs = ['in_normal', 'in_position']

       
    
    def get_vertex_buffer_data(self,vertices_provider):

        vertex_data = vertices_provider
        vbo = self.context.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.vertex_buffer_object.release()
    
    



class Vertex_buffer_object_with_texturing:
    def __init__(self, context,vertices_provider_with_texture_coordinates):
        self.context = context
        self.vertex_buffer_object = self.get_vertex_buffer_data(vertices_provider_with_texture_coordinates)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
    
    def get_vertex_buffer_data(self,vertices_provider_with_texture_coordinates):

        vertex_data = vertices_provider_with_texture_coordinates()
        vbo = self.context.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.vertex_buffer_object.release()