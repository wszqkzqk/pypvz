import pygame as pg
import os
from .. import tool
from .. import constants as c

class Menu(tool.State):
    
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        self.setupBackground()
        self.setupOptions()
        self.setupOptionMenu()
        self.setupSunflowerTrophy()
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
        pg.mixer.music.play(-1, 0)
        pg.display.set_caption(c.ORIGINAL_CAPTION)
        pg.mixer.music.set_volume(self.game_info[c.VOLUME])

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
        frame_names = (f'{c.OPTION_ADVENTURE}_0', f'{c.OPTION_ADVENTURE}_1')
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
        exit_frame_names = (f'{c.EXIT}_0', f'{c.EXIT}_1')
        exit_frame_rect = (0, 0, 47, 27)
        for name in exit_frame_names:
            self.exit_frames.append(tool.get_image_menu(tool.GFX[name], *exit_frame_rect, c.BLACK, 1.1))
        self.exit_frame_index = 0
        self.exit_image = self.exit_frames[self.exit_frame_index]
        self.exit_rect = self.exit_image.get_rect()
        self.exit_rect.x = 730
        self.exit_rect.y = 507
        self.exit_highlight_time = 0

        # 选项按钮
        self.option_button_frames = []
        option_button_frame_names = (f'{c.OPTION_BUTTON}_0', f'{c.OPTION_BUTTON}_1')
        option_button_frame_rect = (0, 0, 81, 31)
        for name in option_button_frame_names:
            self.option_button_frames.append(tool.get_image_menu(tool.GFX[name], *option_button_frame_rect, c.BLACK))
        self.option_button_frame_index = 0
        self.option_button_image = self.option_button_frames[self.option_button_frame_index]
        self.option_button_rect = self.option_button_image.get_rect()
        self.option_button_rect.x = 560
        self.option_button_rect.y = 490
        self.option_button_hightlight_time = 0

        # 小游戏
        self.littleGame_frames = []
        littleGame_frame_names = (c.LITTLEGAME_BUTTON + '_0', c.LITTLEGAME_BUTTON + '_1')
        littleGame_frame_rect = (0, 7, 317, 135)
        for name in littleGame_frame_names:
            self.littleGame_frames.append(tool.get_image_menu(tool.GFX[name], *littleGame_frame_rect, c.BLACK, 1))
        self.littleGame_frame_index = 0
        self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]
        self.littleGame_rect = self.littleGame_image.get_rect()
        self.littleGame_rect.x = 397
        self.littleGame_rect.y = 175
        self.littleGame_highlight_time = 0

        self.adventure_start = 0
        self.adventure_timer = 0
        self.adventure_clicked = False
        self.option_button_clicked = False

    def inArea(self, rect, x, y):
        if (x >= rect.x and x <= rect.right and
            y >= rect.y and y <= rect.bottom):
            return True
        else:
            return False

    def checkHilight(self, x, y):
        # 高亮冒险模式按钮
        if self.inArea(self.adventure_rect, x, y):
            self.adventure_highlight_time = self.current_time
        # 高亮退出按钮
        elif self.inArea(self.exit_rect, x, y):
            self.exit_highlight_time = self.current_time
        # 高亮选项按钮
        elif self.inArea(self.option_button_rect, x, y):
            self.option_button_hightlight_time = self.current_time
        # 高亮小游戏按钮
        elif self.inArea(self.littleGame_rect, x, y):
            self.littleGame_highlight_time = self.current_time

        # 检查是否应当高亮并应用结果
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
        if (self.current_time - self.option_button_hightlight_time) < 80:
            self.option_button_frame_index = 1
        else:
            self.option_button_frame_index = 0
        self.option_button_image = self.option_button_frames[self.option_button_frame_index]
        if (self.current_time - self.littleGame_highlight_time) < 80:
            self.littleGame_frame_index= 1
        else:
            self.littleGame_frame_index = 0
        self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]

    def checkAdventureClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inArea(self.adventure_rect, x, y):
            self.adventure_clicked = True
            self.adventure_timer = self.adventure_start = self.current_time
            self.persist[c.GAME_MODE] = c.MODE_ADVENTURE
            # 播放进入音效
            c.SOUND_EVILLAUGH.play()
            c.SOUND_LOSE.play()
    
    # 点击到按钮，修改转态的done属性
    def checkExitClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inArea(self.exit_rect, x, y):
            self.done = True
            self.next = c.EXIT

    # 检查有没有按到小游戏
    def checkLittleGameClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inArea(self.littleGame_rect, x, y):
            self.done = True
            self.persist[c.GAME_MODE] = c.MODE_LITTLEGAME
            # 播放点击音效
            c.SOUND_BUTTON_CLICK.play()

    def setupOptionMenu(self):
        # 选项菜单框
        frame_rect = (0, 0, 500, 500)
        self.big_menu = tool.get_image_menu(tool.GFX[c.BIG_MENU], *frame_rect, c.BLACK, 1.1)
        self.big_menu_rect = self.big_menu.get_rect()
        self.big_menu_rect.x = 150
        self.big_menu_rect.y = 0

        # 返回按钮
        frame_rect = (0, 0, 342, 87)
        self.return_button = tool.get_image_menu(tool.GFX[c.RETURN_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = 220
        self.return_button_rect.y = 440

        # 音量+、音量-
        frame_rect = (0, 0, 39, 41)
        font = pg.font.Font(c.FONT_PATH, 35)
        font.bold = True
        # 音量+
        self.volume_plus_button = tool.get_image_menu(tool.GFX[c.VOLUME_BUTTON], *frame_rect, c.BLACK)
        sign = font.render("+", True, c.YELLOWGREEN)
        sign_rect = sign.get_rect()
        sign_rect.x = 8
        sign_rect.y = -4
        self.volume_plus_button.blit(sign, sign_rect)
        self.volume_plus_button_rect = self.volume_plus_button.get_rect()
        self.volume_plus_button_rect.x = 500
        # 音量-
        self.volume_minus_button = tool.get_image_menu(tool.GFX[c.VOLUME_BUTTON], *frame_rect, c.BLACK)
        sign = font.render("-", True, c.YELLOWGREEN)
        sign_rect = sign.get_rect()
        sign_rect.x = 12
        sign_rect.y = -6
        self.volume_minus_button.blit(sign, sign_rect)
        self.volume_minus_button_rect = self.volume_minus_button.get_rect()
        self.volume_minus_button_rect.x = 450
        # 音量+、-应当处于同一高度
        self.volume_minus_button_rect.y = self.volume_plus_button_rect.y = 250

    def setupSunflowerTrophy(self):
        # 设置金银向日葵图片信息
        if self.game_info[c.LEVEL_COMPLETIONS]:
            if self.game_info[c.LITTLEGAME_COMPLETIONS]:
                frame_rect = (157, 0, 157, 269)
            else:
                frame_rect = (0, 0, 157, 269)
            self.sunflower_trophy = tool.get_image_menu(tool.GFX[c.TROPHY_SUNFLOWER], *frame_rect, c.BLACK)
            self.sunflower_trophy_rect = self.sunflower_trophy.get_rect()
            self.sunflower_trophy_rect.x = 0
            self.sunflower_trophy_rect.y = 280

    def checkOptionButtonClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inArea(self.option_button_rect, x, y):
            self.option_button_clicked = True
            # 播放点击音效
            c.SOUND_BUTTON_CLICK.play()

    def showCurrentVolumeImage(self, surface):
        # 由于音量可变，因此这一内容不能在一开始就结束加载，而应当不断刷新不断显示
        font = pg.font.Font(c.FONT_PATH, 30)
        volume_tips = font.render(f"音量：{round(self.game_info[c.VOLUME]*100):3}%", True, c.LIGHTGRAY)
        volume_tips_rect = volume_tips.get_rect()
        volume_tips_rect.x = 275
        volume_tips_rect.y = 247
        surface.blit(volume_tips, volume_tips_rect)

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.adventure_image, self.adventure_rect)
        surface.blit(self.exit_image, self.exit_rect)
        surface.blit(self.option_button_image, self.option_button_rect)
        surface.blit(self.littleGame_image, self.littleGame_rect)
        if self.game_info[c.LEVEL_COMPLETIONS]:
            surface.blit(self.sunflower_trophy, self.sunflower_trophy_rect)

        # 点到冒险模式后播放动画
        if self.adventure_clicked:
            if (self.current_time - self.adventure_timer) > 150:
                self.adventure_frame_index += 1
                if self.adventure_frame_index >= 2:
                    self.adventure_frame_index = 0
                self.adventure_timer = self.current_time
                self.adventure_image = self.adventure_frames[self.adventure_frame_index]
            if (self.current_time - self.adventure_start) > 3200:
                self.done = True
        # 点到选项按钮后显示菜单
        elif self.option_button_clicked:
            surface.blit(self.big_menu, self.big_menu_rect)
            surface.blit(self.return_button, self.return_button_rect)
            surface.blit(self.volume_plus_button, self.volume_plus_button_rect)
            surface.blit(self.volume_minus_button, self.volume_minus_button_rect)
            self.showCurrentVolumeImage(surface)
            if mouse_pos:
                # 返回
                if self.inArea(self.return_button_rect, *mouse_pos):
                    self.option_button_clicked = False
                    c.SOUND_BUTTON_CLICK.play()
                # 音量+
                elif self.inArea(self.volume_plus_button_rect, *mouse_pos):
                    self.game_info[c.VOLUME] = min(self.game_info[c.VOLUME] + 0.1, 1)
                    # 一般不会有人想把音乐和音效分开设置，故pg.mixer.Sound.set_volume()和pg.mixer.music.set_volume()需要一起用
                    pg.mixer.music.set_volume(self.game_info[c.VOLUME])
                    for i in c.SOUNDS:
                        i.set_volume(self.game_info[c.VOLUME])
                    c.SOUND_BUTTON_CLICK.play()
                # 音量-
                elif self.inArea(self.volume_minus_button_rect, *mouse_pos):
                    self.game_info[c.VOLUME] = max(self.game_info[c.VOLUME] - 0.1, 0)
                    # 一般不会有人想把音乐和音效分开设置，故pg.mixer.Sound.set_volume()和pg.mixer.music.set_volume()需要一起用
                    pg.mixer.music.set_volume(self.game_info[c.VOLUME])
                    for i in c.SOUNDS:
                        i.set_volume(self.game_info[c.VOLUME])
                    c.SOUND_BUTTON_CLICK.play()
        # 没有点到前两者时常规行检测所有按钮的点击和高亮
        else:
            # 先检查选项高亮预览
            self.checkHilight(*pg.mouse.get_pos())
            if mouse_pos:
                self.checkExitClick(mouse_pos)
                self.checkOptionButtonClick(mouse_pos)
                self.checkLittleGameClick(mouse_pos)
                self.checkAdventureClick(mouse_pos)
