import glm


class Light:
    def __init__(self, position=(0, 5, 5), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # intensities
        self.Ia = 1 * self.color  # ambient  0.06
        self.Id = 0.8 * self.color  # diffuse 0.8
        self.Is = 1.0 * self.color  # specular 1.0