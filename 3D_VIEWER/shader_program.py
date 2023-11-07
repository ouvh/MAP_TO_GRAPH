
class ShaderProgram:
    def __init__(self, context,file_name):
        self.context = context
        self.program = self.get_program(file_name)

    def get_program(self, shader_program_name):

        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        self.program.release()
