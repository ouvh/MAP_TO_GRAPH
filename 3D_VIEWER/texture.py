from pygame import image,transform
from moderngl import LINEAR_MIPMAP_LINEAR,LINEAR

class Texture:
    def __init__(self,context,texture_file_name) -> None:
        self.context = context
        self.texture = self.get_texture(texture_file_name)
    
    def get_texture(self, path):
        texture = image.load(path).convert()
        texture = transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.context.texture(size=texture.get_size(), components=3,
                                   data=image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (LINEAR_MIPMAP_LINEAR, LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture


    def destroy(self):
        self.texture.release()  