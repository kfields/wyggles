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
        
    def remove_sprite(self, sprite):
        self.remove(sprite)

    def depth_sort(self):
        sprite_list = self.sprite_list
        has_swapped = True
        while(has_swapped):
            has_swapped = False
            for i in range(len(sprite_list) - 1):
                if sprite_list[i].z > sprite_list[i+1].z:
                    self.swap(i, i+1)
                    has_swapped = True
