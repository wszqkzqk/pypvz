import os
import pygame as pg
from abc import abstractmethod
from .. import tool
from .. import constants as c

class Screen(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    @abstractmethod
    def startup(self, current_time, persist):
        pass

    def setupImage(self, name, frame_rect=(0, 0, 800, 600), color_key=c.BLACK):
        # 背景图本身
        self.image = tool.get_image(tool.GFX[name], *frame_rect, colorkey=color_key)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # 按钮
        frame_rect = (0, 0, 111, 26)
        ## 主菜单按钮
        self.main_menu_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
        self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
        self.main_menu_button_image_rect.x = 620
        ### 主菜单按钮上的文字
        font = pg.font.Font(c.FONT_PATH, 18)
        main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
        main_menu_text_rect = main_menu_text.get_rect()
        main_menu_text_rect.x = 29
        ## 继续按钮
        self.next_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
        self.next_button_image_rect = self.next_button_image.get_rect()
        self.next_button_image_rect.x = 70
        ### 继续按钮上的文字
        if name == c.GAME_VICTORY_IMAGE:
            next_text = font.render("下一关", True, c.NAVYBLUE)
            next_text_rect = next_text.get_rect()
            next_text_rect.x = 29
            self.next_button_image_rect.y = self.main_menu_button_image_rect.y = 555
        else:
            next_text = font.render("重新开始", True, c.NAVYBLUE)
            next_text_rect = next_text.get_rect()
            next_text_rect.x = 21
            self.next_button_image_rect.y = self.main_menu_button_image_rect.y = 530
        self.next_button_image.blit(next_text, next_text_rect)
        self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
        self.image.blit(self.next_button_image, self.next_button_image_rect)
        self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)

    def update(self, surface, current_time, mouse_pos, mouse_click):
        surface.fill(c.WHITE)
        surface.blit(self.image, self.rect)
        if mouse_pos:
            # 点到继续
            if self.inArea(self.next_button_image_rect, *mouse_pos):
                self.next = c.LEVEL
                self.done = True
            # 点到主菜单
            elif self.inArea(self.main_menu_button_image_rect, *mouse_pos):
                self.next = c.MAIN_MENU
                self.done = True

class GameVictoryScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.image_name = c.GAME_VICTORY_IMAGE
    
    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = persist
        self.setupImage(self.image_name)
        pg.display.set_caption("pypvz: 战斗胜利！")
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(c.PATH_MUSIC_DIR, "zenGarden.opus"))
        pg.mixer.music.play(-1, 0)
        pg.mixer.music.set_volume(self.game_info[c.SOUND_VOLUME])

class GameLoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.image_name = c.GAME_LOSE_IMAGE
    
    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = persist
        self.setupImage(self.image_name, (-118, -40, 800, 600), c.WHITE)
        pg.display.set_caption("pypvz: 战斗失败！")
        # 停止播放原来关卡中的音乐
        pg.mixer.music.stop()

class AwardScreen(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    def setupImage(self):
        # 主体
        frame_rect = (0, 0, 800, 600)
        self.image = tool.get_image(tool.GFX[c.AWARD_SCREEN_IMAGE], *frame_rect)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # 文字
        # 标题处文字
        font = pg.font.Font(c.FONT_PATH, 37)
        title_text = font.render("您获得了新的战利品！", True, c.PARCHMENT_YELLOW)
        title_text_rect = title_text.get_rect()
        title_text_rect.x = 220
        title_text_rect.y = 23
        self.image.blit(title_text, title_text_rect)
        
        # 按钮
        frame_rect = (0, 0, 111, 26)
        if self.show_only_one_option:
            ## 主菜单按钮
            self.main_menu_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
            self.main_menu_button_image_rect.x = 343
            self.main_menu_button_image_rect.y = 520
            ### 主菜单按钮上的文字
            font = pg.font.Font(c.FONT_PATH, 18)
            main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
            main_menu_text_rect = main_menu_text.get_rect()
            main_menu_text_rect.x = 29
            self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
            self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)

            # 绘制向日葵奖杯
            if (self.game_info[c.LEVEL_COMPLETIONS] and self.game_info[c.LITTLEGAME_COMPLETIONS]):
                frame_rect = (157, 0, 157, 269)
                intro_title = "金向日葵奖杯"
                intro_content = "您已通过所有关卡，获得此奖励！"
            else:
                frame_rect = (0, 0, 157, 269)
                intro_title = "银向日葵奖杯"
                if self.game_info[c.LEVEL_COMPLETIONS]:
                    intro_content = "您已完成冒险模式，获得此奖励！"
                else:
                    intro_content = "您已完成玩玩小游戏，获得此奖励！"
            sunflower_trophy_image = tool.get_image_alpha(tool.GFX[c.TROPHY_SUNFLOWER], *frame_rect, scale=0.7)
            sunflower_trophy_rect = sunflower_trophy_image.get_rect()
            sunflower_trophy_rect.x = 348
            sunflower_trophy_rect.y = 108
            self.image.blit(sunflower_trophy_image, sunflower_trophy_rect)

            # 绘制介绍标题
            font = pg.font.Font(c.FONT_PATH, 22)
            intro_title_img = font.render(intro_title, True, c.PARCHMENT_YELLOW)
            intro_title_rect = intro_title_img.get_rect()
            intro_title_rect.x = 333
            intro_title_rect.y = 305
            self.image.blit(intro_title_img, intro_title_rect)

            # 绘制介绍内容
            font = pg.font.Font(c.FONT_PATH, 15)
            intro_content_img = font.render(intro_content, True, c.NAVYBLUE)
            intro_content_rect = intro_content_img.get_rect()
            intro_content_rect.x = 290
            intro_content_rect.y = 370
            self.image.blit(intro_content_img, intro_content_rect)
        else:
            ## 继续按钮
            self.next_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.next_button_image_rect = self.next_button_image.get_rect()
            self.next_button_image_rect.x = 70
            ### 继续按钮上的文字
            font = pg.font.Font(c.FONT_PATH, 18)
            next_text = font.render("继续", True, c.NAVYBLUE)
            next_text_rect = next_text.get_rect()
            next_text_rect.x = 37
            ## 主菜单按钮
            self.main_menu_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
            self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
            self.main_menu_button_image_rect.x = 620
            self.next_button_image_rect.y = self.main_menu_button_image_rect.y = 540
            ### 主菜单按钮上的文字
            main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
            main_menu_text_rect = main_menu_text.get_rect()
            main_menu_text_rect.x = 29
            self.next_button_image.blit(next_text, next_text_rect)
            self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
            self.image.blit(self.next_button_image, self.next_button_image_rect)
            self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = persist
        if (c.PASSED_ALL in self.game_info) and (not self.game_info[c.PASSED_ALL]):
            self.show_only_one_option = False
        else:
            self.show_only_one_option = True
        self.setupImage()
        pg.display.set_caption("pypvz: 您获得了新的战利品！")
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(c.PATH_MUSIC_DIR, "zenGarden.opus"))
        pg.mixer.music.play(-1, 0)
        pg.mixer.music.set_volume(self.game_info[c.SOUND_VOLUME])

    def update(self, surface, current_time, mouse_pos, mouse_click):
        surface.blit(self.image, self.rect)
        if mouse_pos:
            # 检查主菜单点击
            if self.inArea(self.main_menu_button_image_rect, *mouse_pos):
                self.next = c.MAIN_MENU
                self.done = True
            elif not self.show_only_one_option:
                if self.inArea(self.next_button_image_rect, *mouse_pos):
                    self.next = c.LEVEL
                    self.done = True

class HelpScreen(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = persist
        self.setupImage()
        pg.display.set_caption("pypvz: 帮助")
        pg.mixer.music.stop()
        c.SOUND_HELP_SCREEN.play()

    def setupImage(self):
        # 主体
        frame_rect = (-100, -50, 800, 600)
        self.image = tool.get_image(tool.GFX[c.HELP_SCREEN_IMAGE], *frame_rect, colorkey=(0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        # 主菜单按钮
        frame_rect = (0, 0, 111, 26)
        self.main_menu_button_image = tool.get_image_alpha(tool.GFX[c.UNIVERSAL_BUTTON], *frame_rect)
        self.main_menu_button_image_rect = self.main_menu_button_image.get_rect()
        self.main_menu_button_image_rect.x = 343
        self.main_menu_button_image_rect.y = 500
        ### 主菜单按钮上的文字
        font = pg.font.Font(c.FONT_PATH, 18)
        main_menu_text = font.render("主菜单", True, c.NAVYBLUE)
        main_menu_text_rect = main_menu_text.get_rect()
        main_menu_text_rect.x = 29
        self.main_menu_button_image.blit(main_menu_text, main_menu_text_rect)
        self.image.blit(self.main_menu_button_image, self.main_menu_button_image_rect)

    def update(self, surface, current_time, mouse_pos, mouse_click):
        surface.fill(c.BLACK)
        surface.blit(self.image, self.rect)
        if mouse_pos:
            # 检查主菜单点击
            if self.inArea(self.main_menu_button_image_rect, *mouse_pos):
                self.next = c.MAIN_MENU
                self.done = True
