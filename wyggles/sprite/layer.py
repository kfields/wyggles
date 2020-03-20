import operator
import arcade

class Layer(arcade.SpriteList):
    def __init__(self, name, use_spatial_hash=False, spatial_hash_cell_size=128, is_static=False):
        super().__init__(use_spatial_hash=False, spatial_hash_cell_size=128, is_static=False)
        self.name = name
        self.layers = []
    
    def draw(self, **kwargs):
        super().draw(**kwargs)
        for layer in self.layers:
            layer.draw(**kwargs)
            
    def add_layer(self, layer):
        self.layers.append(layer)
        
    def remove_layer(self, layer):
        self.layers.remove(layer)            
            
    def add_sprite(self, sprite):
        self.append(sprite)
        #self.depth_sort()
        
    def remove_sprite(self, sprite):
        self.remove(sprite)
        
    def depth_sort(self):
        self.sprite_list.sort(key=operator.attrgetter('z'))
        # Rebuild index list
        for idx, sprite in enumerate(self.sprite_list):
            self.sprite_idx[sprite] = idx