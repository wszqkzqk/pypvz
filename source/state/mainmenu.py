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
        self.setupOptions()

    def setupBackground(self):
        frame_rect = (80, 0, 800, 600)
        # 1、形参中加单星号，即f(*x)则表示x为元组，所有对x的操作都应将x视为元组类型进行。
        # 2、双星号同上，区别是x视为字典。
        # 3、在变量前加单星号表示将元组（列表、集合）拆分为单个元素。
        # 4、双星号同上，区别是目标为字典，字典前加单星号的话可以得到“键”。
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0
        
    def setupOptions(self):
        # 冒险模式
        self.adventure_frames = []
        frame_names = (c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1')
        frame_rect = (0, 0, 330, 144)
        
        for name in frame_names:
            self.adventure_frames.append(tool.get_image_menu(tool.GFX[name], *frame_rect, c.BLACK, 1))
        self.adventure_frame_index = 0
        self.adventure_image = self.adventure_frames[self.adventure_frame_index]
        self.adventure_rect = self.adventure_image.get_rect()
        self.adventure_rect.x = 400
        self.adventure_rect.y = 60
        self.adventure_highlight_time = 0
        
        # 退出按钮
        self.exit_frames = []
        exit_frame_names = (c.EXIT + '_0', c.EXIT + '_1')
        exit_frame_rect = (0, 0, 47, 27)
        for name in exit_frame_names:
            self.exit_frames.append(tool.get_image_menu(tool.GFX[name], *exit_frame_rect, c.BLACK, 1.1))
        self.exit_frame_index = 0
        self.exit_image = self.exit_frames[self.exit_frame_index]
        self.exit_rect = self.exit_image.get_rect()
        self.exit_rect.x = 730
        self.exit_rect.y = 507
        self.exit_highlight_time = 0

        # 小游戏
        self.littleGame_frames = []
        littleGame_frame_names = (c.LITTLEGAME_BUTTON + '_0', c.LITTLEGAME_BUTTON + '_1')
        littleGame_frame_rect = (0, 7, 317, 135)
        for name in littleGame_frame_names:
            self.littleGame_frames.append(tool.get_image_menu(tool.GFX[name], *frame_rect, c.BLACK, 1))
        self.littleGame_frame_index = 0
        self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]
        self.littleGame_rect = self.littleGame_image.get_rect()
        self.littleGame_rect.x = 397
        self.littleGame_rect.y = 175
        self.littleGame_highlight_time = 0

        self.adventure_start = 0
        self.adventure_timer = 0
        self.adventure_clicked = False

    def inAreaAdventure(self, x, y):
        if (x >= self.adventure_rect.x and x <= self.adventure_rect.right and
            y >= self.adventure_rect.y and y <= self.adventure_rect.bottom):
            return True
        else:
            return False
    
    def inAreaExit(self, x, y):
        if (x >= self.exit_rect.x and x <= self.exit_rect.right and
            y >= self.exit_rect.y and y <= self.exit_rect.bottom):
            return True
        else:
            return False
    
    def inAreaLittleGame(self, x, y):
        if (x >= self.littleGame_rect.x and x <= self.littleGame_rect.right and
            y >= self.littleGame_rect.y and y <= self.littleGame_rect.bottom):
            return True
        else:
            return False

    def checkHilight(self, x, y):
        # 高亮冒险模式按钮
        if self.inAreaAdventure(x, y):
            self.adventure_highlight_time = self.current_time
        elif self.inAreaExit(x, y):
            self.exit_highlight_time = self.current_time
        elif self.inAreaLittleGame(x, y):
            self.littleGame_highlight_time = self.current_time


    def checkAdventureClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaAdventure(x, y):
            self.adventure_clicked = True
            self.adventure_timer = self.adventure_start = self.current_time
            self.persist[c.GAME_MODE] = c.MODE_ADVENTURE
        return False
    
    # 点击到按钮，修改转态的done属性
    def checkExitClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaExit(x, y):
            self.done = True
            self.next = c.EXIT

    # 检查有没有按到小游戏
    def checkLittleGameClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaLittleGame(x, y):
            self.done = True
            # 确实小游戏还是用的level
            # 因为目前暂时没有生存模式和解谜模式，所以暂时设置为这样
            self.persist[c.GAME_MODE] = c.MODE_LITTLEGAME

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        # 没有选到选项时，检查有没有点到选项
        if not self.adventure_clicked:
            # 先检查选项高亮预览
            x, y = pg.mouse.get_pos()
            self.checkHilight(x, y)
            if (self.current_time - self.adventure_highlight_time) < 80:
                self.adventure_frame_index = 1
            else:
                self.adventure_frame_index = 0
            self.adventure_image = self.adventure_frames[self.adventure_frame_index]
            if (self.current_time - self.exit_highlight_time) < 80:
                self.exit_frame_index = 1
            else:
                self.exit_frame_index = 0
            self.exit_image = self.exit_frames[self.exit_frame_index]
            if (self.current_time - self.littleGame_highlight_time) < 80:
                self.littleGame_frame_index= 1
            else:
                self.littleGame_frame_index = 0
            self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]

            if mouse_pos:
                self.checkAdventureClick(mouse_pos)
                self.checkExitClick(mouse_pos)
                self.checkLittleGameClick(mouse_pos)
        else:
            # 点到后播放动画
            if(self.current_time - self.adventure_timer) > 150:
                self.adventure_frame_index += 1
                if self.adventure_frame_index >= 2:
                    self.adventure_frame_index = 0
                self.adventure_timer = self.current_time
                self.adventure_image = self.adventure_frames[self.adventure_frame_index]
            if(self.current_time - self.adventure_start) > 1300:
                self.done = True
                

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.adventure_image, self.adventure_rect)
        surface.blit(self.exit_image, self.exit_rect)
        surface.blit(self.littleGame_image, self.littleGame_rect)