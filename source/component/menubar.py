import random
import pygame as pg
from .. import tool
from .. import constants as c


def getSunValueImage(sun_value):
    # for pack, must include ttf
    font = pg.font.Font(c.FONT_PATH, 14)
    font.bold = True
    width = 35
    msg_image = font.render(str(sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
    msg_rect = msg_image.get_rect()
    msg_w = msg_rect.width

    image = pg.Surface((width, 17))
    x = width - msg_w

    image.fill(c.LIGHTYELLOW)
    image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
    image.set_colorkey(c.BLACK)
    return image

def getCardPool(data):
    card_pool = {c.PLANT_CARD_INFO[c.PLANT_CARD_INDEX[card_name]]: data[card_name]
                    for card_name in data}
    return card_pool

class Card():
    def __init__(self, x:int, y:int, index:int, scale:float=0.5, not_recommend=0):
        self.info = c.PLANT_CARD_INFO[index]
        self.loadFrame(self.info[c.CARD_INDEX], scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # 绘制植物阳光消耗大小
        font = pg.font.Font(c.FONT_PATH, 12)
        self.sun_cost_img = font.render(str(self.info[c.SUN_INDEX]), True, c.BLACK)
        self.sun_cost_img_rect = self.sun_cost_img.get_rect()
        sun_cost_img_x = 32 - self.sun_cost_img_rect.w
        self.orig_image.blit(self.sun_cost_img,
                            (sun_cost_img_x, 52, self.sun_cost_img_rect.w, self.sun_cost_img_rect.h))
        
        self.index = index
        self.sun_cost = self.info[c.SUN_INDEX]
        self.frozen_time = self.info[c.FROZEN_TIME_INDEX]
        self.frozen_timer = -self.frozen_time
        self.refresh_timer = 0
        self.select = True
        self.clicked = False
        self.not_recommend = not_recommend
        if self.not_recommend:
            self.orig_image.set_alpha(128)
            self.image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            self.image.blit(self.orig_image, (0,0), (0, 0, self.rect.w, self.rect.h))
        else:
            self.image = self.orig_image
            self.image.set_alpha(255)

    def loadFrame(self, name, scale):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.image = self.orig_image

    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
        self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def canClick(self, sun_value, current_time):
        if self.sun_cost <= sun_value and (current_time - self.frozen_timer) > self.frozen_time:
            return True
        return False

    def canSelect(self):
        return self.select

    def setSelect(self, can_select):
        self.select = can_select
        if can_select:
            if self.not_recommend % 2:
                self.orig_image.set_alpha(128)
                self.image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
                self.image.blit(self.orig_image, (0,0), (0, 0, self.rect.w, self.rect.h))
            else:
                self.image = self.orig_image
                self.image.set_alpha(255)
        else:
            self.orig_image.set_alpha(64)
            self.image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            self.image.blit(self.orig_image, (0,0), (0, 0, self.rect.w, self.rect.h))

    def setFrozenTime(self, current_time):
        self.frozen_timer = current_time

    def createShowImage(self, sun_value, current_time):
        # 有关是否满足冷却与阳光条件的图片形式
        time = current_time - self.frozen_timer
        if time < self.frozen_time: #cool down status
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            frozen_image = self.orig_image
            frozen_image.set_alpha(128)
            frozen_height = ((self.frozen_time - time)/self.frozen_time) * self.rect.h
            
            image.blit(frozen_image, (0,0), (0, 0, self.rect.w, frozen_height))
            self.orig_image.set_alpha(192)
            image.blit(self.orig_image, (0,frozen_height),
                       (0, frozen_height, self.rect.w, self.rect.h - frozen_height))
        elif self.sun_cost > sun_value: #disable status
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            self.orig_image.set_alpha(192)
            image.blit(self.orig_image, (0,0), (0, 0, self.rect.w, self.rect.h))
        elif self.clicked:
            image = pg.Surface((self.rect.w, self.rect.h))  # 黑底
            chosen_image = self.orig_image
            chosen_image.set_alpha(128)
            
            image.blit(chosen_image, (0,0), (0, 0, self.rect.w, self.rect.h))
        else:
            image = self.orig_image
            image.set_alpha(255)
        return image

    def update(self, sun_value, current_time):
        if (current_time - self.refresh_timer) >= 250:
            self.image = self.createShowImage(sun_value, current_time)
            self.refresh_timer = current_time

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 植物栏
class MenuBar():
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 26
        self.setupCards(card_list)

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def update(self, current_time):
        self.current_time = current_time
        for card in self.card_list:
            card.update(self.sun_value, self.current_time)

    def createImage(self, x, y, num):
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x,0))
        self.image.set_colorkey(c.BLACK)
    
    def setupCards(self, card_list):
        self.card_list = []
        x = self.card_offset_x
        y = 8
        for index in card_list:
            x += c.BAR_CARD_X_INTERNAL
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canClick(self.sun_value, self.current_time):
                    result = (c.PLANT_CARD_INFO[card.index][c.PLANT_NAME_INDEX], card)
                else:
                    # 播放无法使用该卡片的警告音
                    c.SOUND_CANNOT_CHOOSE_WARNING.play()
                break
        return result
    
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
            self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def decreaseSunValue(self, value):
        self.sun_value -= value

    def increaseSunValue(self, value):
        self.sun_value += value
        if self.sun_value > 9990:
            self.sun_value = 9990

    def setCardFrozenTime(self, plant_name):
        for card in self.card_list:
            if c.PLANT_CARD_INFO[card.index][c.PLANT_NAME_INDEX] == plant_name:
                card.setFrozenTime(self.current_time)
                break

    def drawSunValue(self):
        self.value_image = getSunValueImage(self.sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.rect.bottom - 24
        
        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)

# 关卡模式选植物的界面
class Panel():
    def __init__(self, card_list, sun_value, background_type=c.BACKGROUND_DAY):
        self.loadImages(sun_value)
        self.selected_cards = []
        self.selected_num = 0
        self.background_type = background_type
        self.setupCards(card_list)

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        return tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def loadImages(self, sun_value):
        self.menu_image = self.loadFrame(c.MENUBAR_BACKGROUND)
        self.menu_rect = self.menu_image.get_rect()
        self.menu_rect.x = 0
        self.menu_rect.y = 0

        self.panel_image = self.loadFrame(c.PANEL_BACKGROUND)
        self.panel_rect = self.panel_image.get_rect()
        self.panel_rect.x = 0
        self.panel_rect.y = c.PANEL_Y_START

        
        self.value_image = getSunValueImage(sun_value)
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 21
        self.value_rect.y = self.menu_rect.bottom - 24

        self.button_image =  self.loadFrame(c.START_BUTTON)
        self.button_rect = self.button_image.get_rect()
        self.button_rect.x = 155
        self.button_rect.y = 547

    def setupCards(self, card_list):
        self.card_list = []
        x = c.PANEL_X_START - c.PANEL_X_INTERNAL
        y = c.PANEL_Y_START + 38 - c.PANEL_Y_INTERNAL
        for i, index in enumerate(card_list):
            if i % 8 == 0:
                x = c.PANEL_X_START - c.PANEL_X_INTERNAL
                y += c.PANEL_Y_INTERNAL
            x += c.PANEL_X_INTERNAL
            plant_name = c.PLANT_CARD_INFO[index][c.PLANT_NAME_INDEX]
            if (plant_name in c.WATER_PLANTS
            and self.background_type not in c.POOL_EQUIPPED_BACKGROUNDS):
                not_recommend = c.REASON_OTHER
            elif (plant_name == c.GRAVEBUSTER
            and self.background_type != c.BACKGROUND_NIGHT):
                not_recommend = c.REASON_OTHER
            elif (plant_name in c.CAN_SLEEP_PLANTS
            and self.background_type in c.DAYTIME_BACKGROUNDS):
                not_recommend = c.REASON_WILL_SLEEP
            elif (plant_name == c.COFFEEBEAN
            and self.background_type not in c.DAYTIME_BACKGROUNDS):
                not_recommend = c.REASON_OTHER
            # 还有屋顶场景，以及其他植物没有实现的植物没有写进来
            else:
                not_recommend = 0
            self.card_list.append(Card(x, y, index, 0.5, not_recommend))

    def checkCardClick(self, mouse_pos):
        delete_card = None
        for card in self.selected_cards:
            if delete_card: # when delete a card, move right cards to left
                card.rect.x -= c.BAR_CARD_X_INTERNAL
            elif card.checkMouseClick(mouse_pos):
                self.deleteCard(card.index)
                delete_card = card

        if delete_card:
            self.selected_cards.remove(delete_card)
            self.selected_num -= 1
            # 播放点击音效
            c.SOUND_TAPPING_CARD.play()
            if delete_card.info[c.PLANT_NAME_INDEX] == c.COFFEEBEAN:
                for i in self.card_list:
                    if i.not_recommend == c.REASON_SLEEP_BUT_COFFEE_BEAN:
                        i.not_recommend = c.REASON_WILL_SLEEP
                        i.orig_image.set_alpha(128)
                        i.image = pg.Surface((i.rect.w, i.rect.h))  # 黑底
                        i.image.blit(i.orig_image, (0,0), (0, 0, i.rect.w, i.rect.h))

        if self.selected_num >= c.CARD_MAX_NUM:
            return

        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canSelect():
                    self.addCard(card)
                    # 播放点击音效
                    c.SOUND_TAPPING_CARD.play()
                    if card.info[c.PLANT_NAME_INDEX] == c.COFFEEBEAN:
                        for i in self.card_list:
                            if i.not_recommend == c.REASON_WILL_SLEEP:
                                i.not_recommend = c.REASON_SLEEP_BUT_COFFEE_BEAN
                                i.image = i.orig_image
                                i.image.set_alpha(255)
                break

    def addCard(self, card:Card):
        card.setSelect(False)
        y = 8
        x = 77 + self.selected_num * c.BAR_CARD_X_INTERNAL
        self.selected_cards.append(Card(x, y, card.index))
        self.selected_num += 1

    def deleteCard(self, index):
        self.card_list[index].setSelect(True)

    def checkStartButtonClick(self, mouse_pos):
        if self.selected_num < c.CARD_LIST_NUM:
            return False

        x, y = mouse_pos
        if (self.button_rect.x <= x <= self.button_rect.right and
            self.button_rect.y <= y <= self.button_rect.bottom):
           return True
        return False

    def getSelectedCards(self):
        card_index_list = []
        for card in self.selected_cards:
            card_index_list.append(card.index)
        return card_index_list

    def draw(self, surface):
        self.menu_image.blit(self.value_image, self.value_rect)
        surface.blit(self.menu_image, self.menu_rect)
        surface.blit(self.panel_image, self.panel_rect)
        for card in self.card_list:
            card.draw(surface)
        for card in self.selected_cards:
            card.draw(surface)

        if self.selected_num >= c.CARD_LIST_NUM:
            surface.blit(self.button_image, self.button_rect)

# 传送带模式的卡片
class MoveCard():
    def __init__(self, x, y, card_name, plant_name, scale=0.5):
        self.loadFrame(card_name, scale)
        self.rect = self.orig_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = 1
        self.clicked = False
        self.image = self.createShowImage()

        self.card_name = card_name
        self.plant_name = plant_name
        self.move_timer = 0
        self.select = True

    def loadFrame(self, name, scale):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.orig_image = tool.get_image(frame, 0, 0, width, height, c.BLACK, scale)
        self.orig_rect = self.orig_image.get_rect()
        self.image = self.orig_image

    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
            self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def createShowImage(self):
        # 新增卡片时显示图片
        if self.rect.w < self.orig_rect.w: #create a part card image
            image = pg.Surface([self.rect.w, self.rect.h])
            if self.clicked:
                self.orig_image.set_alpha(128)
            else:
                self.orig_image.set_alpha(255)
            image.blit(self.orig_image, (0, 0), (0, 0, self.rect.w, self.rect.h))
            self.rect.w += 1
        else:
            if self.clicked:
                image = pg.Surface([self.rect.w, self.rect.h])  # 黑底
                self.orig_image.set_alpha(128)
                
                image.blit(self.orig_image, (0,0), (0, 0, self.rect.w, self.rect.h))
            else:
                self.orig_image.set_alpha(255)
                image = self.orig_image
        return image

    def update(self, left_x, current_time):
        if self.move_timer == 0:
            self.move_timer = current_time
        elif (current_time - self.move_timer) >= c.CARD_MOVE_TIME:
            if self.rect.x > left_x:
                self.rect.x -= 1
            self.image = self.createShowImage()
            self.move_timer += c.CARD_MOVE_TIME

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# 传送带
class MoveBar():
    def __init__(self, card_pool):
        self.loadFrame(c.MOVEBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 0
        
        self.card_start_x = self.rect.x + 8
        self.card_end_x = self.rect.right - 5
        self.card_pool = card_pool
        self.card_pool_name = tuple(self.card_pool.keys())
        self.card_pool_weight = tuple(self.card_pool.values())
        self.card_list = []
        self.create_timer = -c.MOVEBAR_CARD_FRESH_TIME

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def createCard(self):
        if len(self.card_list) > 0 and self.card_list[-1].rect.right > self.card_end_x:
            return False
        x = self.card_end_x
        y = 6
        selected_card = random.choices(self.card_pool_name, self.card_pool_weight)[0]
        self.card_list.append(MoveCard(x, y, selected_card[c.CARD_INDEX], selected_card[c.PLANT_NAME_INDEX]))
        return True

    def update(self, current_time):
        self.current_time = current_time
        left_x = self.card_start_x
        for card in self.card_list:
            card.update(left_x, self.current_time)
            left_x = card.rect.right + 1

        if (self.current_time - self.create_timer) > c.MOVEBAR_CARD_FRESH_TIME:
            if self.createCard():
                self.create_timer = self.current_time

    def checkCardClick(self, mouse_pos):
        result = None
        for index, card in enumerate(self.card_list):
            if card.checkMouseClick(mouse_pos):
                result = (card.plant_name, card)
                break
        return result
    
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if (self.rect.x <= x <= self.rect.right and
            self.rect.y <= y <= self.rect.bottom):
            return True
        return False

    def deleateCard(self, card):
        self.card_list.remove(card)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)
