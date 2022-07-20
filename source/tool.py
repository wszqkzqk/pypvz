import os
import json
import sys
from abc import abstractmethod
import pygame as pg
from pygame.locals import *
from . import constants as c

# an abstract class, one state of automata
class State():
    def __init__(self):
        self.start_time = 0
        self.current_time = 0
        self.done = False   # false 代表未做完
        self.next = None    # 表示这个状态退出后要转到的下一个状态
        self.persist = {}   # 在状态间转换时需要传递的数据

    # 当从其他状态进入这个状态时，需要进行的初始化操作
    @abstractmethod
    def startup(self, current_time, persist):
        '''abstract method'''
    # 当从这个状态退出时，需要进行的清除操作
    def cleanup(self):
        self.done = False
        return self.persist
    # 在这个状态运行时进行的更新操作
    @abstractmethod
    def update(self, surface, keys, current_time):
        '''abstract method'''

# control this game. do event loops
class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()    # 创建一个对象来帮助跟踪时间
        self.fps = 50 * c.GAME_RATE
        self.keys = pg.key.get_pressed()
        self.mouse_pos = None
        self.mouse_click = [False, False]  # value:[left mouse click, right mouse click]
        self.current_time = 0.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.game_info = {c.CURRENT_TIME:0,
                          c.LEVEL_NUM:c.START_LEVEL_NUM,
                          c.LITTLEGAME_NUM:c.START_LITTLE_GAME_NUM}
 
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, self.game_info)

    def update(self):
        # 返回自 pygame_init() 调用以来的毫秒数 * 游戏速度倍率
        self.current_time = pg.time.get_ticks() * c.GAME_RATE

        if self.state.done:
            self.flip_state()
            
        self.state.update(self.screen, self.current_time, self.mouse_pos, self.mouse_click)
        self.mouse_pos = None
        self.mouse_click[0] = False
        self.mouse_click[1] = False

    # 状态转移
    def flip_state(self):
        if self.state.next == c.EXIT:
            pg.quit()
            os._exit(0)
        # previous, self.state_name = self.state_name, self.state.next
        self.state_name = self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                if event.key == pg.K_f:
                    SCREEN = pg.display.set_mode(c.SCREEN_SIZE, pg.HWSURFACE|pg.FULLSCREEN)
                elif event.key == pg.K_u:
                    SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()
                self.mouse_click[0], _, self.mouse_click[1] = pg.mouse.get_pressed()
                # self.mouse_click[0]表示左键，self.mouse_click[1]表示右键
                print(  f"点击位置: ({self.mouse_pos[0]:3}, {self.mouse_pos[1]:3})",
                        f"左右键点击情况: {self.mouse_click}")


    def run(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
        print('game over')

def get_image(sheet, x, y, width, height, colorkey=c.BLACK, scale=1):
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))
        if colorkey:
            image.set_colorkey(colorkey)
        image = pg.transform.scale(image,
                                   (int(rect.width*scale),
                                    int(rect.height*scale)))
        return image

def get_image_menu(sheet, x, y, width, height, colorkey=c.BLACK, scale=1):
        # 一定要保留阿尔法通道，修复主菜单bug，游戏中car显示又有bug
        image = pg.Surface([width, height], SRCALPHA)
        rect = image.get_rect()

        image.blit(sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(colorkey)
        image = pg.transform.scale(image,
                                   (int(rect.width*scale),
                                    int(rect.height*scale)))
        return image  
        
def load_image_frames(directory, image_name, colorkey, accept):
    frame_list = []
    tmp = {}
    # image_name is "Peashooter", pic name is 'Peashooter_1', get the index 1
    index_start = len(image_name) + 1 
    frame_num = 0
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            index = int(name[index_start:])
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            tmp[index]= img
            frame_num += 1

    for i in range(frame_num):  # 这里注意编号必须连续，否则会出错
        frame_list.append(tmp[i])
    return frame_list

# colorkeys 是设置图像中的某个颜色值为透明,这里用来消除白边
def load_all_gfx(directory, colorkey=c.WHITE, accept=('.png', '.jpg', '.bmp', '.gif', 'webp')):
    graphics = {}
    for name1 in os.listdir(directory):
        # subfolders under the folder resources\graphics
        dir1 = os.path.join(directory, name1)
        if os.path.isdir(dir1):
            for name2 in os.listdir(dir1):
                dir2 = os.path.join(dir1, name2)
                if os.path.isdir(dir2):
                # e.g. subfolders under the folder resources\graphics\Zombies
                    for name3 in os.listdir(dir2):
                        dir3 = os.path.join(dir2, name3)
                        # e.g. subfolders or pics under the folder resources\graphics\Zombies\ConeheadZombie
                        if os.path.isdir(dir3):
                            # e.g. it's the folder resources\graphics\Zombies\ConeheadZombie\ConeheadZombieAttack
                            image_name, _ = os.path.splitext(name3)
                            graphics[image_name] = load_image_frames(dir3, image_name, colorkey, accept)
                        else:
                            # e.g. pics under the folder resources\graphics\Plants\Peashooter
                            image_name, _ = os.path.splitext(name2)
                            graphics[image_name] = load_image_frames(dir2, image_name, colorkey, accept)
                            break
                else:
                # e.g. pics under the folder resources\graphics\Screen
                    name, ext = os.path.splitext(name2)
                    if ext.lower() in accept:
                        img = pg.image.load(dir2)
                        if img.get_alpha():
                            img = img.convert_alpha()
                        else:
                            img = img.convert()
                            img.set_colorkey(colorkey)
                        graphics[name] = img
    return graphics

# 从文件加载矩形碰撞范围
# 用于消除文件边框影响
def loadZombieImageRect():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'data', 'entity', 'zombie.json')
    with open(file_path) as f:
        data = json.load(f)
    return data[c.ZOMBIE_IMAGE_RECT]

def loadPlantImageRect():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'data', 'entity', 'plant.json')
    with open(file_path) as f:
        data = json.load(f)
    return data[c.PLANT_IMAGE_RECT]

pg.init()
pg.display.set_caption(c.ORIGINAL_CAPTION)  # 设置标题
SCREEN = pg.display.set_mode(c.SCREEN_SIZE) # 设置初始屏幕
try:    # 设置窗口图标，仅对非Nuitka时生效，Nuitka不需要包括额外的图标文件，自动跳过这一过程即可
    pg.display.set_icon(pg.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), c.ORIGINAL_LOGO)))
except:
    pass

GFX = load_all_gfx(os.path.join(os.path.dirname(os.path.dirname(__file__)) ,os.path.join("resources","graphics")))
ZOMBIE_RECT = loadZombieImageRect()
PLANT_RECT = loadPlantImageRect()

# 播放音乐
pg.mixer.init()
pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(__file__)) ,"resources", "music", "intro.opus"))
pg.mixer.music.play(-1, 0)