import pyglet
import arcade
import pymunk
import timeit
import math
import os

from botsley.run.task import runner

import wyggles.app
from wyggles.assets import asset
from wyggles.engine import *
from wyggles.wyggle import Wyggle
from wyggles.ball import Ball
from wyggles.fruit import FruitFactory


COLUMNS = 20
ROWS = 20

TILE_WIDTH = 128
TILE_HEIGHT = 128

TILE_SCALING = 1

#SCREEN_WIDTH = int(COLUMNS * TILE_WIDTH * TILE_SCALING)
#SCREEN_HEIGHT = int(ROWS * TILE_HEIGHT * TILE_SCALING)
SCREEN_WIDTH = world_right
SCREEN_HEIGHT = world_top
SCREEN_TITLE = "Wyggles"

#WYGGLE_COUNT = 3
WYGGLE_COUNT = 1

MAX_FOOD = 3
#MAX_FOOD = 10

def spawnWyggle(layer):
    wyggle = Wyggle(layer)
    materializeRandomFromCenter(wyggle)

def spawnWyggles(layer):
    for count in range(WYGGLE_COUNT):
        spawnWyggle(layer)

#Balls
def spawnBall(layer):
    ball = Ball(layer)
    ball.materialize_at(random.random() * (world_right - 100), random.random() * (world_top - 100))

def spawnBalls(layer):
    i = 0
    while(i < 10):
        i = i + 1
        spawnBall(layer)

def spawnFood(layer):
    fruitFactory = FruitFactory(layer)
    #apple = Apple(layer)
    for i in range(MAX_FOOD):
        fruit = fruitFactory.create_random()
        materializeRandomFromCenter(fruit)

def spawnFruit(layer):
    fruitFactory = FruitFactory(layer)
    fruit = fruitFactory.create_random()
    materializeRandomFromCenter(fruit)

def spawnObstacle(sprite):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = sprite.position
    shape = pymunk.Poly(body, sprite.hit_box)
    shape.elasticity = .5
    shape.friction = .9
    sprite_engine.space.add(shape)
    #layer.append(shape)

#Walls
def spawnWall(layer, x, y, w, z):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x + (w-x)/2, y + (z-y)/2
    shape = pymunk.Poly.create_box(body, (w-x, z-y))
    shape.elasticity = .5
    shape.friction = .9
    sprite_engine.space.add(shape)
    #layer.append(shape)

def spawnWalls(layer):
    left = world_left 
    left = world_bottom 
    right = world_right 
    top = world_top
    thickness = 200
    #North Wall
    spawnWall(layer, left-thickness, left-thickness, right+thickness, left)
    #East Wall
    spawnWall(layer, right, left-thickness, right+thickness, top+thickness)
    #South Wall
    spawnWall(layer, left-thickness, top, right+thickness, top+thickness)
    #West Wall
    spawnWall(layer, left-thickness, left-thickness, left, top+thickness)

class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class BoxSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename, width, height):
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.layers = []
        self.respawning_food = False
        BG_WIDTH = 128
        BG_HEIGHT = 128

        '''
        #self.background = arcade.load_texture(asset('grass.png'))
        bg_path = ":resources:images/tiles/grassCenter.png"
        #bg_path = asset('grass.png')
        self.background = arcade.Sprite(bg_path, TILE_SCALING,
                                         repeat_count_x=width/BG_WIDTH, repeat_count_y=height/BG_HEIGHT)
        self.background.position = (width/2, height/2)
        self.background.width = width
        self.background.height = height
        '''
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # -- Pymunk
        self.space = sprite_engine.space

        my_map = arcade.tilemap.read_tmx(asset('level1.tmx'))

        self.layers.append(arcade.tilemap.process_layer(my_map, 'ground', TILE_SCALING))

        self.layers.append(arcade.tilemap.process_layer(my_map, 'enemy', TILE_SCALING))


        self.wyggle_layer = Layer('wyggles')
        self.layers.append(self.wyggle_layer)
        spawnWyggles(self.wyggle_layer)

        self.ball_layer = Layer('balls')
        self.layers.append(self.ball_layer)
        spawnBalls(self.ball_layer)

        self.food_layer = Layer('food')
        self.layers.append(self.food_layer)
        spawnFood(self.food_layer)

        wyggles.app.landscape_layer = self.landscape_layer = landscape_layer = arcade.tilemap.process_layer(my_map, 'landscape', TILE_SCALING)
        self.layers.append(landscape_layer)
        for sprite in landscape_layer:
            spawnObstacle(sprite)

        # Lists of sprites or lines
        self.sprite_list = Layer('walls')
        self.layers.append(self.sprite_list)
        self.static_lines = []

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        self.draw_time = 0
        self.processing_time = 0

        spawnWalls(self.static_lines)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw the background
        #(left, right, bottom, top) = viewport = arcade.get_viewport()
        #arcade.draw_lrwh_rectangle_textured(left, bottom, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        #self.background.draw()

        # Draw all the sprites
        for layer in self.layers:
            layer.draw()

        for wyggle in self.wyggle_layer:
            brain = wyggle.brain
            if not brain:
                continue
            txt = brain.state
            arcade.draw_text(txt, wyggle.x + 16, wyggle.y + 16, arcade.color.BLACK, 12)
            focus = brain.focus
            if not focus:
                continue
            arcade.draw_line(wyggle.x, wyggle.y, focus.x, focus.y, arcade.color.BLACK, 1)


        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 20, arcade.color.BLACK, 12)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.BLACK, 12)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.last_mouse_position = x, y
            # See if we clicked on anything
            shape_list = self.space.point_query((x, y), 1, pymunk.ShapeFilter())

            # If we did, remember what we clicked on
            if len(shape_list) > 0:
                self.shape_being_dragged = shape_list[0]

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # With right mouse button, shoot a heavy coin fast.
            mass = 60
            radius = 10
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = x, y
            body.velocity = 2000, 0
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)

            sprite = CircleSprite(shape, ":resources:images/items/coinGold.png")
            self.sprite_list.append(sprite)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Release the item we are holding (if any)
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            # If we are holding an object, move it with the mouse
            self.last_mouse_position = x, y
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def on_update(self, delta_time):
        start_time = timeit.default_timer()
        self.wyggle_layer.on_update(delta_time)
        self.ball_layer.on_update(delta_time)
        self.food_layer.on_update(delta_time)
        if len(self.food_layer) < MAX_FOOD and not self.respawning_food:
            self.respawning_food = True
            def re_spawn(dt, *args, **kwargs):
                spawnFruit(self.food_layer)
                self.respawning_food = False

            pyglet.clock.schedule_once(re_spawn, 3.0)

        # Check for balls that fall off the screen
        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.position.y < 0:
                # Remove balls from physics space
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                # Remove balls from physics list
                sprite.remove_from_sprite_lists()

        self.space.step(1 / 60.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        # Move sprites to where physics objects are
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time


#def main():
MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

#arcade.run()
#pyglet.app.run()
#pyglet.app.EventLoop().run()
#pyglet.app.event_loop.run()

class MyEventLoop(pyglet.app.EventLoop):
    pass
    '''
    def idle(self):
        runner.step()
        return super().idle()
    '''

def step_runner(delta_time):
    runner.step()

pyglet.clock.schedule_interval(step_runner, .25)

pyglet.app.event_loop = event_loop = MyEventLoop()

@event_loop.event
def on_window_close(window):
    print('close')
    event_loop.exit()
    return pyglet.event.EVENT_HANDLED

event_loop.run()

#if __name__ == "__main__":
#    main()
