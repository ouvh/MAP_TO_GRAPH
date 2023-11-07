import glm
from vertex_array_object import *
import texture

class base_model_no_texturing:

    def __init__(self,vertices_provider,shader_program,app,color=(50,50,50),position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):

        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(a) for a in rotation])
        self.scale = scale
        self.color = color
        self.model_matrix = self.get_model_matrix()


        self.vertex_array_object = Vertex_array_object_no_texturing(app.context,vertices_provider,shader_program)
        self.shader_program = shader_program
        self.camera = self.app.camera

        ###################### define the color for the shader program #############

        self.shader_program.program['m_proj'].write(self.camera.m_proj)
        self.shader_program.program['m_view'].write(self.camera.m_view)
        self.shader_program.program['m_model'].write(self.model_matrix)
        # light
        self.shader_program.program['light.position'].write(self.app.light.position)
        self.shader_program.program['light.Ia'].write(self.app.light.Ia)
        self.shader_program.program['light.Id'].write(self.app.light.Id)
        self.shader_program.program['light.Is'].write(self.app.light.Is)
        self.shader_program.program['COLOR'] = glm.vec3(color)
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def update(self):
        self.shader_program.program['COLOR'] = glm.vec3(self.color)
        self.shader_program.program['m_proj'].write(self.camera.m_proj)
        self.shader_program.program['camPos'].write(self.camera.position)
        self.shader_program.program['m_view'].write(self.camera.m_view)
        self.shader_program.program['m_model'].write(self.model_matrix)

    def render(self):
        self.update()
        self.vertex_array_object.vertex_array_object.render()

    def destroy(self):
        self.vertex_array_object.destroy()

class base_model_with_texturing:
    
    def __init__(self,texture_file_name,vertices_provider_with_texture_coordinate,shader_program,app,color=(50,50,50),position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):

        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(a) for a in rotation])
        self.scale = scale
        self.color = color
        self.model_matrix = self.get_model_matrix()

        self.texture = texture.Texture(app.context,texture_file_name)


        self.vertex_array_object = Vertex_array_object_with_texturing(app.context,vertices_provider_with_texture_coordinate,shader_program)
        self.shader_program = shader_program
        self.camera = self.app.camera

        self.shader_program.program['u_texture_0'] = 0
        self.texture.texture.use()
        # mvp
        self.shader_program.program['m_proj'].write(self.camera.m_proj)
        self.shader_program.program['m_view'].write(self.camera.m_view)
        self.shader_program.program['m_model'].write(self.model_matrix)
        # light
        self.shader_program.program['light.position'].write(self.app.light.position)
        self.shader_program.program['light.Ia'].write(self.app.light.Ia)
        self.shader_program.program['light.Id'].write(self.app.light.Id)
        self.shader_program.program['light.Is'].write(self.app.light.Is)

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def update(self):
        self.texture.texture.use()
        self.shader_program.program['camPos'].write(self.camera.position)
        self.shader_program.program['m_view'].write(self.camera.m_view)
        self.shader_program.program['m_model'].write(self.model_matrix)
   
    def render(self):
        self.update()
        self.vertex_array_object.vertex_array_object.render()
    
    def destroy(self):
        self.vertex_array_object.destroy()



    

