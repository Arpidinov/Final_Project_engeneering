from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from kivy.properties import NumericProperty
from pipe import Pipe

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

        self.floor_texture = Image(source="img_5.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def on_size(self, *args):
        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width , self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + time_passed/4.5)%Window.width, self.floor_texture.uvpos[1])

        # Redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)

class Bird(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self,touch):
        self.source = 'open.png'
        self.velocity = 100
        super().on_touch_down(touch)
    def on_press(self, touch):
        self.source = 'close.png'
        super().on_touch_up(touch)






class MainApp(App):
    pipes = []
    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)
    def start_game(self):
        num_pipes = 5
        distance_between_pipes = Window.width /(num_pipes-1)

        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(96 + 100, self.root.height - 80 )
            pipe.size_hint = (None,None)
            pipe.pos= ( i * distance_between_pipes,71 )
            pipe.size = (64,self.root.height- 71)
            self.pipes.append(pipe)
            self.root.add_widget(pipe)
        Clock.schedule_interval(self.move_pipes,1/60.)

    def move_pipes(self,time_passed):
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # check if we need to reposition the pipe at the right side
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width



MainApp().run()
