import pygame
import os
import sys
import time
import threading
from PIL import Image


def hello_world():
    """示例函数：返回欢迎信息"""
    return "Hello from mylibrary!"

def calculate_sum(a, b):
    """演示带类型提示的函数"""
    return a + b

class DataProcessor:
    """示例类：数据处理工具"""
    def __init__(self, multiplier=1):
        self.multiplier = multiplier
    def process(self, x):
        return x * self.multiplier

class GamePy:
    class Game:
        def __init__(self, width=800, height=600, title="GamePy Window", R=0, G=0, B=0):
            pygame.init()
            self.init()
            self.running = False
            self.R = R
            self.G = G
            self.B = B
            self.window = self.Window(width, height, title)
            self.event = self.Event()
            self.time = self.Time()
        
        def init(self):
            self.python__version__ = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            print("phrlibrary 1.0.1 gamepy 0.1.1 in " + str(self.python__version__) + "\nHello from the PHRLibrary GamePy World!")
    
        class Window:
            def __init__(self, width, height, title="GamePy Window"):
                self.screen = pygame.display.set_mode((width, height))
                self.caption(title)
            def caption(self, title):
                pygame.display.set_caption(title)
            def icon(self, iconfile):
                pygame.display.set_icon(Image.open(iconfile))
            def update(self):
                pass
            def render(self, fillR=0, fillG=0, fillB=0):
                self.screen.fill((fillR, fillG, fillB))
            def flip(self):
                pygame.display.flip()
    
        class Event:
            def __init__(self):
                pass
            def handle_events(self, game):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.running = False
    
        class Time:
            def __init__(self):
                self.clock = pygame.time.Clock()
            def set_fps(self, fps):
                self.clock.tick(fps)
            def delay(self, ms):
                time.sleep(ms / 1000)
    
        def run(self):
            self.running = True
            while self.running:
                self.event.handle_events(self)
                self.window.update()
                self.window.render(self.R, self.G, self.B)
                self.window.flip()
                self.time.set_fps(60)
            pygame.quit()
            sys.exit()

class game:
    def __init__(self):
        pass
    def main(self, width=800, height=600, title="GamePy Window", R=0, G=0, B=0):
        self.gamepy = GamePy()
        self.game = self.gamepy.Game(width, height, title, R, G, B)
        self.game.run()
