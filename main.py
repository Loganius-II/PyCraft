
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders.basic_lighting_shader import basic_lighting_shader
from perlin_noise import PerlinNoise
import random
from time import sleep
print("starting in 3 seconds..", flush=True)
#time.sleep(3)
noise = PerlinNoise(octaves=3, seed=random.randint(1,1000))
app = Ursina()
shader = basic_lighting_shader
player = FirstPersonController(
    mouse_sensitivity=Vec2(100,100),
    position=(0,5,0),
    height=10
)

block_textures ={
    "grass": "Textures/blocks/groundEarth.png",
    "grass2": "Textures/blocks/grass.png",
    "mud": "Textures/blocks/groundMud.png",
    "stone": "Textures/blocks/stone.png",
    "stone2": "Textures/blocks/stone2.png",
    "none": None
}
selected_b = 'grass'
Sky(texture="Textures/other/sky.png")
#grass_img = load_texture(block_textures["grass"])

class Block(Entity):
    def __init__(self,position,blocktype):
        super().__init__(
            position=position,
            model="Models/block_model.obj",
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(blocktype),
            collider="box",
            shader=shader
        )
        self.blocktype = blocktype
mini_block = Entity(
    parent=camera,
    model="Models/block_model.obj",
    scale=0.2,
    texture=block_textures.get(selected_b),
    position=(0.35, -0.25,0.5),
    rotation=(-15,-30,-5)
)
min_height = -5
for x in range(-10,10):
    for z in range(-10,10):
        height = noise([x * .02, z * 0.02])
        height = math.floor(height * 7.5)
        for y in range(height, min_height-1, -1):
            if y == min_height:
                block = Block((x,y+min_height,z), "mud")
            elif height-y >= 2:
                block = Block((x,y+min_height,z), "stone")
            else:
                block = Block((x,y+min_height,z), "grass")
index =0
def input(key):
    global selected_b, index
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            print(hit_info.entity.position + hit_info.normal)
            block = Block(hit_info.entity.position + hit_info.normal, selected_b)
    if key == "right mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.blocktype == "mud":
            destroy(mouse.hovered_entity)
    if key == 'scroll up': 
        index += 1
        if index == 4:
            index = 1
        if index == 1:
            selected_b = "grass"
            mini_block.texture = block_textures.get("grass")
        if index == 2:
            selected_b = 'stone2'
            mini_block.texture = block_textures.get("stone2")
        if index == 3:
            selected_b = 'stone'
            mini_block.texture = block_textures.get("stone")
            
app.run()