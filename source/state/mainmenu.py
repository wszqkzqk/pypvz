import pygame as pg
from .. import tool
from .. import constants as c
from . import level

class Menu(tool.State):
    
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        self.setupBackground()
        self.setupOption()

    def setupBackground(self):
        frame_rect = [80, 0, 800, 600]
        # 1、形参中加单星号，即f(*x)则表示x为元组，所有对x的操作都应将x视为元组类型进行。
        # 2、双星号同上，区别是x视为字典。
        # 3、在变量前加单星号表示将元组（列表、集合）拆分为单个元素。
        # 4、双星号同上，区别是目标为字典，字典前加单星号的话可以得到“键”。
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0
        
    def setupOption(self):
        self.option_frames = []
        frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 77]
        
        for name in frame_names:
            self.option_frames.append(tool.get_image_menu(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        self.option_frame_index = 0
        self.option_image = self.option_frames[self.option_frame_index]
        self.option_rect = self.option_image.get_rect()
        self.option_rect.x = 435
        self.option_rect.y = 75
        
        # 退出按钮
        frame_rect = [0, 0, 500, 500]
        self.option_exit = tool.get_image_menu(tool.GFX[c.EXIT], *frame_rect, c.BLACK, 1.1)
        self.exit_rect = self.option_exit.get_rect()
        self.exit_rect.x = 690
        self.exit_rect.y = 400

        # 小游戏
        frame_rect = [0, 0, 317, 139]
        self.option_littleGame = tool.get_image_menu(tool.GFX[c.LITTLEGAME_BUTTON], *frame_rect, c.BLACK, 0.9)
        self.option_littleGame_rect = self.option_littleGame.get_rect()
        self.option_littleGame_rect.x = 425
        self.option_littleGame_rect.y = 200

        self.option_start = 0
        self.option_timer = 0
        self.option_clicked = False
    
    def checkOptionClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.option_rect.x and x <= self.option_rect.right and
           y >= self.option_rect.y and y <= self.option_rect.bottom):
            self.option_clicked = True
            self.option_timer = self.option_start = self.current_time
        return False
    
    # 点击到按钮，修改转态的done属性
    def checkExitClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.exit_rect.x and x <= self.exit_rect.right and
           y >= self.exit_rect.y and y <= self.exit_rect.bottom):
            self.done = True
            self.next = c.EXIT

    # 检查有没有按到小游戏
    def checkLittleGameClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.option_littleGame_rect.x and x <= self.option_littleGame_rect.right and
           y >= self.option_littleGame_rect.y and y <= self.option_littleGame_rect.bottom):
            self.done = True
            # 确实小游戏还是用的level
            self.persist[c.LITTLEGAME_BUTTON] = True

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        # 没有选到选项时，检查有没有点到选项
        if not self.option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
                self.checkExitClick(mouse_pos)
                self.checkLittleGameClick(mouse_pos)
        else:
            # 点到后播放动画
            if(self.current_time - self.option_timer) > 200:
                self.option_frame_index += 1
                if self.option_frame_index >= 2:
                    self.option_frame_index = 0
                self.option_timer = self.current_time
                self.option_image = self.option_frames[self.option_frame_index]
            if(self.current_time - self.option_start) > 1300:
                self.done = True
                

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.option_image, self.option_rect)
        surface.blit(self.option_exit, self.exit_rect)
        surface.blit(self.option_littleGame, self.option_littleGame_rect)