import os
import json
import sys
import pygame as pg
from random import randint
from .. import tool
from .. import constants as c
from ..component import map, plant, zombie, menubar

class Level(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.map_y_len = c.GRID_Y_LEN
        self.map = map.Map(c.GRID_X_LEN, self.map_y_len)

        # 暂停状态
        self.pause = False
        self.pauseTime = 0

        # 默认显然不用显示菜单
        self.showLittleMenu = False
        
        self.loadMap()
        self.setupBackground()
        self.initState()

    def loadMap(self):
        modeList = ['adventure', 'littleGame']
        if c.LITTLEGAME_BUTTON in self.game_info:
            map_file = 'littleGame_' + str(self.game_info[c.LITTLEGAME_NUM]) + '.json'
            mode = 'littleGame'
        else:
            map_file = 'level_' + str(self.game_info[c.LEVEL_NUM]) + '.json'
            mode = 'adventure'
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'resources' , 'data', 'map', map_file)
        # 最后一关之后应该结束了
        try:
            f = open(file_path)
            self.map_data = json.load(f)
            f.close()
        except Exception as e:
            print("游戏结束")
            self.done = True
            self.next = c.MAIN_MENU
            pg.mixer.music.stop()
            pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
            pg.mixer.music.play(-1, 0)
            return
        if self.map_data[c.SHOVEL] == 0:
            self.hasShovel = False
        else:
            self.hasShovel = True

        # 同时播放音乐
        global bgm
        if mode == modeList[0]: # 冒险模式
            if self.game_info[c.LEVEL_NUM] in {0, 1, 2}:    # 白天关卡
                bgm = 'dayLevel.opus'
            elif self.game_info[c.LEVEL_NUM] in {3}:    # 夜晚关卡
                bgm = 'nightLevel.opus'
        elif mode == modeList[1]:   # 小游戏模式
            if self.game_info[c.LITTLEGAME_NUM] in {1}:   # 传送带大战
                bgm = 'battle.opus'
            elif self.game_info[c.LITTLEGAME_NUM] in {2}:    # 坚果保龄球
                bgm = 'bowling.opus'
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", bgm))
        pg.mixer.music.play(-1, 0)

    def setupBackground(self):
        img_index = self.map_data[c.BACKGROUND_TYPE]
        self.background_type = img_index
        self.background = tool.GFX[c.BACKGROUND_NAME][img_index]
        self.bg_rect = self.background.get_rect()

        self.level = pg.Surface((self.bg_rect.w, self.bg_rect.h)).convert()
        self.viewport = tool.SCREEN.get_rect(bottom=self.bg_rect.bottom)
        self.viewport.x += c.BACKGROUND_OFFSET_X

    
    def setupGroups(self):
        self.sun_group = pg.sprite.Group()
        self.head_group = pg.sprite.Group()

        self.plant_groups = []
        self.zombie_groups = []
        self.hypno_zombie_groups = [] #zombies who are hypno after eating hypnoshroom
        self.bullet_groups = []
        for i in range(self.map_y_len):
            self.plant_groups.append(pg.sprite.Group())
            self.zombie_groups.append(pg.sprite.Group())
            self.hypno_zombie_groups.append(pg.sprite.Group())
            self.bullet_groups.append(pg.sprite.Group())
    
    def setupZombies(self):
        def takeTime(element):
            return element[0]

        self.zombie_list = []
        # 目前设置为从JSON文件中读取僵尸出现的时间、种类、位置信息，以后可以将时间设置为模仿原版的机制，位置设置为随机数
        for data in self.map_data[c.ZOMBIE_LIST]:
            if 'map_y' in data.keys():
                self.zombie_list.append((data['time'], data['name'], data['map_y']))
            else:
                self.zombie_list.append((data['time'], data['name']))
        self.zombie_start_time = 0
        self.zombie_list.sort(key=takeTime)

    def setupCars(self):
        self.cars = []
        for i in range(self.map_y_len):
            _, y = self.map.getMapGridPos(0, i)
            self.cars.append(plant.Car(-25, y+20, i))
    
    # 更新函数每帧被调用，将鼠标事件传入给状态处理函数
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = self.pvzTime(current_time)
        if self.state == c.CHOOSE:
            self.choose(mouse_pos, mouse_click)
        elif self.state == c.PLAY:
            self.play(mouse_pos, mouse_click)

        self.draw(surface)

    def pvzTime(self, current_time):
        # 扣除暂停时间
        if not self.pause:
            self.beforePauseTime = current_time - self.pauseTime
        else:
            self.pauseTime = current_time - self.beforePauseTime
        return self.beforePauseTime

    def initBowlingMap(self):
        print('initBowlingMap')
        for x in range(3, self.map.width):
            for y in range(self.map.height):
                self.map.setMapGridType(x, y, c.MAP_COMMON_PLANT)

    def initState(self):
        # 小游戏才有CHOOSEBAR_TYPE
        if c.CHOOSEBAR_TYPE in self.map_data:
            self.bar_type = self.map_data[c.CHOOSEBAR_TYPE]
        else:
            self.bar_type = c.CHOOSEBAR_STATIC

        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.initChoose()
        else:
            card_pool = menubar.getCardPool(self.map_data[c.CARD_POOL])
            self.initPlay(card_pool)
            if self.bar_type == c.CHOSSEBAR_BOWLING:
                self.initBowlingMap()

    def initChoose(self):
        self.state = c.CHOOSE
        self.panel = menubar.Panel(menubar.all_card_list, self.map_data[c.INIT_SUN_NAME])

    def choose(self, mouse_pos, mouse_click):
        if mouse_pos and mouse_click[0]:
            self.panel.checkCardClick(mouse_pos)
            if self.panel.checkStartButtonClick(mouse_pos):
                self.initPlay(self.panel.getSelectedCards())

    def initPlay(self, card_list):
        self.state = c.PLAY
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar = menubar.MenuBar(card_list, self.map_data[c.INIT_SUN_NAME])
        else:
            self.menubar = menubar.MoveBar(card_list)
        
        # 是否拖住植物或者铲子
        self.drag_plant = False
        self.drag_shovel = False

        self.hint_image = None
        self.hint_plant = False
        # 0:白天 1:夜晚 2:泳池 3:浓雾 4:屋顶 5:月夜 6:坚果保龄球
        # 还准备加入    -1:单行草皮 -2:三行草皮 但是目前没有找到图（
        if self.background_type in {0, 2, 4, -1, -2} and self.bar_type == c.CHOOSEBAR_STATIC:
            self.produce_sun = True
        else:
            self.produce_sun = False
        self.sun_timer = self.current_time

        self.removeMouseImage()
        self.setupGroups()
        self.setupZombies()
        self.setupCars()

        # 地图有铲子才添加铲子
        if self.hasShovel:
            #  导入小铲子
            frame_rect = [0, 0, 71, 67]
            self.shovel = tool.get_image_menu(tool.GFX[c.SHOVEL], *frame_rect, c.BLACK, 1.1)
            self.shovel_rect = self.shovel.get_rect()
            frame_rect = [0, 0, 77, 75]
            self.shovel_positon = (550, 2)
            self.shovel_box = tool.get_image_menu(tool.GFX[c.SHOVEL_BOX], *frame_rect, c.BLACK, 1.1)
            self.shovel_box_rect = self.shovel_box.get_rect()
            self.shovel_rect.x = self.shovel_box_rect.x = self.shovel_positon[0]
            self.shovel_rect.y = self.shovel_box_rect.y = self.shovel_positon[1] 

        self.setupLittleMenu()

    # 小菜单
    def setupLittleMenu(self):
        # 具体运行游戏必定有个小菜单, 导入菜单和选项
        frame_rect = [0, 0, 108, 31]
        self.little_menu = tool.get_image_menu(tool.GFX[c.LITTLE_MENU], *frame_rect, c.BLACK, 1.1)
        self.little_menu_rect = self.little_menu.get_rect()
        self.little_menu_rect.x = 650
        self.little_menu_rect.y = 0 

        frame_rect = [0, 0, 500, 500]
        self.big_menu = tool.get_image_menu(tool.GFX[c.BIG_MENU], *frame_rect, c.BLACK, 1.1)
        self.big_menu_rect = self.big_menu.get_rect()
        self.big_menu_rect.x = 150
        self.big_menu_rect.y = 0

        frame_rect = [0, 0, 342, 87]
        self.return_button = tool.get_image_menu(tool.GFX[c.RETURN_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = 220
        self.return_button_rect.y = 440

        frame_rect = [0, 0, 207, 45]
        self.restart_button = tool.get_image_menu(tool.GFX[c.RESTART_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.x = 295
        self.restart_button_rect.y = 325

        frame_rect = [0, 0, 206, 43]
        self.mainMenu_button = tool.get_image_menu(tool.GFX[c.MAINMENU_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.mainMenu_button_rect = self.mainMenu_button.get_rect()
        self.mainMenu_button_rect.x = 299
        self.mainMenu_button_rect.y = 372

    # 检查小菜单有没有被点击
    def checkLittleMenuClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.little_menu_rect.x and x <= self.little_menu_rect.right and
           y >= self.little_menu_rect.y and y <= self.little_menu_rect.bottom):
            return True
        return False

    # 检查小菜单的返回有没有被点击
    def checkReturnClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.return_button_rect.x and x <= self.return_button_rect.right and
           y >= self.return_button_rect.y and y <= self.return_button_rect.bottom):
            return True
        return False

    # 检查小菜单的重新开始有没有被点击
    def checkRestartClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.restart_button_rect.x and x <= self.restart_button_rect.right and
           y >= self.restart_button_rect.y and y <= self.restart_button_rect.bottom):
            return True
        return False
    
    # 检查小菜单的主菜单有没有被点击
    def checkMainMenuClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.mainMenu_button_rect.x and x <= self.mainMenu_button_rect.right and
           y >= self.mainMenu_button_rect.y and y <= self.mainMenu_button_rect.bottom):
            return True
        return False

    # 用小铲子移除植物
    def shovelRemovePlant(self, mouse_pos):
        x, y = mouse_pos
        map_x, map_y = self.map.getMapIndex(x, y)
        for i in self.plant_groups[map_y]:
            if (x >= i.rect.x and x <= i.rect.right and
                y >= i.rect.y and y <= i.rect.bottom):
                self.killPlant(i, shovel=True)
                # 使用后默认铲子复原
                self.drag_shovel = not self.drag_shovel
                self.removeMouseImagePlus()
                return 

    # 检查小铲子的位置有没有被点击
    # 方便放回去
    def checkShovelClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.shovel_box_rect.x and x <= self.shovel_box_rect.right and
           y >= self.shovel_box_rect.y and y <= self.shovel_box_rect.bottom):
            return True
        return False

    def play(self, mouse_pos, mouse_click):
        # 原版阳光掉落机制需要
        # 已掉落的阳光
        self.fallenSun = 0

        # 如果暂停
        if self.showLittleMenu:
            # 设置暂停状态
            self.pause = True
            # 暂停播放音乐
            pg.mixer.music.pause()
            if mouse_click[0]:
                if self.checkReturnClick(mouse_pos):
                    # 终止暂停，停止显示菜单
                    self.pause = False
                    self.showLittleMenu = False
                    # 继续播放音乐
                    pg.mixer.music.unpause()
                elif self.checkRestartClick(mouse_pos):
                    self.done = True
                    self.next = c.LEVEL
                    pg.mixer.music.stop()
                    pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", bgm))
                    pg.mixer.music.play(-1, 0)
                elif self.checkMainMenuClick(mouse_pos):
                    self.done = True
                    self.next = c.MAIN_MENU
                    #self.persist = {c.CURRENT_TIME:0, c.LEVEL_NUM:c.START_LEVEL_NUM} # 应该不能用c.LEVEL_NUM:c.START_LEVEL_NUM
                    self.persist = {c.CURRENT_TIME:0, c.LEVEL_NUM:self.persist[c.LEVEL_NUM], c.LITTLEGAME_NUM:self.persist[c.LITTLEGAME_NUM]}
                    pg.mixer.music.stop()
                    pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
                    pg.mixer.music.play(-1, 0)
            return

        if self.zombie_start_time == 0:
            self.zombie_start_time = self.current_time
        elif len(self.zombie_list) > 0:
            data = self.zombie_list[0]  # 因此要求僵尸列表按照时间顺序排列
            # data内容排列：[0]:时间 [1]:名称 [2]:坐标
            if  data[0] <= (self.current_time - self.zombie_start_time):
                if len(data) == 3:
                    self.createZombie(data[1], data[2])
                    self.zombie_list.remove(data)
                else:   # len(data) == 2 没有指定map_y
                    self.createZombie(data[1])
                    self.zombie_list.remove(data)

        for i in range(self.map_y_len):
            self.bullet_groups[i].update(self.game_info)
            self.plant_groups[i].update(self.game_info)
            self.zombie_groups[i].update(self.game_info)
            self.hypno_zombie_groups[i].update(self.game_info)
            # 清除走出去的魅惑僵尸
            for zombie in self.hypno_zombie_groups[i]:
                if zombie.rect.x > c.SCREEN_WIDTH:
                    zombie.kill()

        self.head_group.update(self.game_info)
        self.sun_group.update(self.game_info)
        
        if self.produce_sun:
            # 原版阳光掉落机制：(已掉落阳光数*100 ms + 4250 ms) 与 9500 ms的最小值，再加 0 ~ 2750 ms 之间的一个数
            if (self.current_time - self.sun_timer) > min(c.PRODUCE_SUN_INTERVAL + 100*self.fallenSun, 9500) + randint(0, 2750):
                self.sun_timer = self.current_time
                map_x, map_y = self.map.getRandomMapIndex()
                x, y = self.map.getMapGridPos(map_x, map_y)
                self.sun_group.add(plant.Sun(x, 0, x, y))
                self.fallenSun += 1
        
        # wcb 添加
        # 检查有没有捡到阳光
        clickedSun = False
        clickedCardsOrMap = False
        if not self.drag_plant and not self.drag_shovel and mouse_pos and mouse_click[0]:
            for sun in self.sun_group:
                if sun.checkCollision(mouse_pos[0], mouse_pos[1]):
                    self.menubar.increaseSunValue(sun.sun_value)
                    clickedSun = True

        # 拖动植物或者铲子
        if not self.drag_plant and mouse_pos and mouse_click[0] and not clickedSun:
            result = self.menubar.checkCardClick(mouse_pos)
            if result:
                self.setupMouseImage(result[0], result[1])
                clickedCardsOrMap = True
        elif self.drag_plant:
            if mouse_click[1]:
                self.removeMouseImage()
                clickedCardsOrMap = True
            elif mouse_click[0]:
                if self.menubar.checkMenuBarClick(mouse_pos):
                    self.removeMouseImage()
                else:
                    self.addPlant()
            elif mouse_pos is None:
                self.setupHintImage()
        elif self.drag_shovel:
            if mouse_click[1]:
                self.removeMouseImagePlus()

        # 检查是否点击菜单
        if mouse_click[0] and (not clickedSun) and (not clickedCardsOrMap):
            if self.checkLittleMenuClick(mouse_pos):
                # 暂停 显示菜单
                self.showLittleMenu = True
            elif self.checkShovelClick(mouse_pos):
                self.drag_shovel = not self.drag_shovel
                if not self.drag_shovel:
                    self.removeMouseImagePlus()
            elif self.drag_shovel:
                # 移出这地方的植物
                self.shovelRemovePlant(mouse_pos)

        for car in self.cars:
            car.update(self.game_info)

        self.menubar.update(self.current_time)


        # 检查碰撞啥的
        self.checkBulletCollisions()
        self.checkZombieCollisions()
        self.checkPlants()
        self.checkCarCollisions()
        self.checkGameState()

    def createZombie(self, name, map_y=None):
        # 有指定时按照指定生成，无指定时随机位置生成
        # 0:白天 1:夜晚 2:泳池 3:浓雾 4:屋顶 5:月夜
        if map_y == None:
            if self.map_data[c.BACKGROUND_TYPE] in {0, 1, 4, 5}:
                map_y = randint(0, 4)
            # 情况复杂：分水路和陆路，不能简单实现，需要另外加判断
            # 0, 1, 4, 5路为陆路，2, 3路为水路
            elif self.map_data[c.BACKGROUND_TYPE] in {2, 3}:
                if name in {}:  # 这里还没填，以后加了泳池模式填：水生僵尸集合
                    map_y = randint(2, 3)
                elif name == '这里应该换成气球僵尸的名字（最好写调用的变量名，最好不要直接写，保持风格统一）':
                    map_y = randint(0, 5)
                else:   # 陆生僵尸
                    map_y = randint(0, 3)
                    if map_y >= 2:   # 后两路的map_y应当+2
                        map_y += 2

        # 新增的僵尸也需要在这里声明
        x, y = self.map.getMapGridPos(0, map_y)
        if name == c.NORMAL_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NormalZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.CONEHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ConeHeadZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.BUCKETHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.BucketHeadZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.FLAG_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.FlagZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.NEWSPAPER_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NewspaperZombie(c.ZOMBIE_START_X, y, self.head_group))

    # 能否种植物的判断：
    # 调用self.map.showPlant(x, y)
    # 先判断位置是否合法 isValid(map_x, map_y)
    # 再判断位置是否可用 isMovable(map_x, map_y)
    # 因为现在还没有做南瓜头，所以目前判断的是map[map_y][map_x]是否为空（c.MAP_EMPTY，即0）
    # 写了南瓜头需要改这个验证
    def canSeedPlant(self):
        x, y = pg.mouse.get_pos()
        return self.map.showPlant(x, y)
        
    # 种植物
    def addPlant(self):
        pos = self.canSeedPlant()
        if pos is None:
            return

        if self.hint_image is None:
            self.setupHintImage()
        x, y = self.hint_rect.centerx, self.hint_rect.bottom
        map_x, map_y = self.map.getMapIndex(x, y)

        # 新植物也需要在这里声明
        if self.plant_name == c.SUNFLOWER:
            new_plant = plant.SunFlower(x, y, self.sun_group)
        elif self.plant_name == c.PEASHOOTER:
            new_plant = plant.PeaShooter(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.SNOWPEASHOOTER:
            new_plant = plant.SnowPeaShooter(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.WALLNUT:
            new_plant = plant.WallNut(x, y)
        elif self.plant_name == c.CHERRYBOMB:
            new_plant = plant.CherryBomb(x, y)
        elif self.plant_name == c.THREEPEASHOOTER:
            new_plant = plant.ThreePeaShooter(x, y, self.bullet_groups, map_y)
        elif self.plant_name == c.REPEATERPEA:
            new_plant = plant.RepeaterPea(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.CHOMPER:
            new_plant = plant.Chomper(x, y)
        elif self.plant_name == c.PUFFSHROOM:
            new_plant = plant.PuffShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.POTATOMINE:
            new_plant = plant.PotatoMine(x, y)
        elif self.plant_name == c.SQUASH:
            new_plant = plant.Squash(x, y)
        elif self.plant_name == c.SPIKEWEED:
            new_plant = plant.Spikeweed(x, y)
        elif self.plant_name == c.JALAPENO:
            new_plant = plant.Jalapeno(x, y)
        elif self.plant_name == c.SCAREDYSHROOM:
            new_plant = plant.ScaredyShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.SUNSHROOM:
            new_plant = plant.SunShroom(x, y, self.sun_group)
        elif self.plant_name == c.ICESHROOM:
            new_plant = plant.IceShroom(x, y)
        elif self.plant_name == c.HYPNOSHROOM:
            new_plant = plant.HypnoShroom(x, y)
        elif self.plant_name == c.WALLNUTBOWLING:
            new_plant = plant.WallNutBowling(x, y, map_y, self)
        elif self.plant_name == c.REDWALLNUTBOWLING:
            new_plant = plant.RedWallNutBowling(x, y)

        if new_plant.can_sleep and self.background_type == c.BACKGROUND_DAY:
            new_plant.setSleep()
        self.plant_groups[map_y].add(new_plant)
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar.decreaseSunValue(self.select_plant.sun_cost)
            self.menubar.setCardFrozenTime(self.plant_name)
        else:
            self.menubar.deleateCard(self.select_plant)

        if self.bar_type != c.CHOSSEBAR_BOWLING:
            self.map.setMapGridType(map_x, map_y, c.MAP_COMMON_PLANT)
        self.removeMouseImage()
        #print('addPlant map[%d,%d], grid pos[%d, %d] pos[%d, %d]' % (map_x, map_y, x, y, pos[0], pos[1]))

    def setupHintImage(self):
        pos = self.canSeedPlant()
        if pos and self.mouse_image:
            if (self.hint_image and pos[0] == self.hint_rect.x and
                pos[1] == self.hint_rect.y):
                return
            width, height = self.mouse_rect.w, self.mouse_rect.h
            image = pg.Surface([width, height])
            image.blit(self.mouse_image, (0, 0), (0, 0, width, height))
            image.set_colorkey(c.BLACK)
            image.set_alpha(128)
            self.hint_image = image
            self.hint_rect = image.get_rect()
            self.hint_rect.centerx = pos[0]
            self.hint_rect.bottom = pos[1]
            self.hint_plant = True
        else:
            self.hint_plant = False

    def setupMouseImage(self, plant_name, select_plant):
        frame_list = tool.GFX[plant_name]
        if plant_name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[plant_name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x, y = 0, 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h

        if (plant_name == c.POTATOMINE or plant_name == c.SQUASH or
            plant_name == c.SPIKEWEED or plant_name == c.JALAPENO or
            plant_name == c.SCAREDYSHROOM or plant_name == c.SUNSHROOM or
            plant_name == c.ICESHROOM or plant_name == c.HYPNOSHROOM or
            plant_name == c.WALLNUTBOWLING or plant_name == c.REDWALLNUTBOWLING):
            color = c.WHITE
        else:
            color = c.BLACK
        self.mouse_image = tool.get_image(frame_list[0], x, y, width, height, color, 1)
        self.mouse_rect = self.mouse_image.get_rect()
        self.drag_plant = True
        self.plant_name = plant_name
        self.select_plant = select_plant

    def removeMouseImage(self):
        self.drag_plant = False
        self.mouse_image = None
        self.hint_image = None
        self.hint_plant = False

    # 移除小铲子
    def removeMouseImagePlus(self):
        self.drag_shovel = False
        self.shovel_rect.x = self.shovel_positon[0]
        self.shovel_rect.y = self.shovel_positon[1]

    def checkBulletCollisions(self):
        collided_func = pg.sprite.collide_circle_ratio(0.7)
        for i in range(self.map_y_len):
            for bullet in self.bullet_groups[i]:
                if bullet.state == c.FLY:
                    zombie = pg.sprite.spritecollideany(bullet, self.zombie_groups[i], collided_func)
                    if zombie and zombie.state != c.DIE:
                        zombie.setDamage(bullet.damage, bullet.ice)
                        bullet.setExplode()
    
    def checkZombieCollisions(self):
        if self.bar_type == c.CHOSSEBAR_BOWLING:
            ratio = 0.6
        else:
            ratio = 0.5
        collided_func = pg.sprite.collide_circle_ratio(ratio)
        for i in range(self.map_y_len):
            hypo_zombies = []
            for zombie in self.zombie_groups[i]:
                if zombie.state != c.WALK:
                    continue
                plant = pg.sprite.spritecollideany(zombie, self.plant_groups[i], collided_func)
                if plant:
                    if plant.name == c.WALLNUTBOWLING:
                        if plant.canHit(i):
                            zombie.setDamage(c.WALLNUT_BOWLING_DAMAGE)
                            plant.changeDirection(i)
                    elif plant.name == c.REDWALLNUTBOWLING:
                        if plant.state == c.IDLE:
                            plant.setAttack()
                    elif plant.name != c.SPIKEWEED:
                        zombie.setAttack(plant)

            for hypno_zombie in self.hypno_zombie_groups[i]:
                if hypno_zombie.health <= 0:
                    continue
                zombie_list = pg.sprite.spritecollide(hypno_zombie,
                               self.zombie_groups[i], False,collided_func)
                for zombie in zombie_list:
                    if zombie.state == c.DIE:
                        continue
                    if zombie.state == c.WALK:
                        zombie.setAttack(hypno_zombie, False)
                    if hypno_zombie.state == c.WALK:
                        hypno_zombie.setAttack(zombie, False)

    def checkCarCollisions(self):
        for car in self.cars:
            for zombie in self.zombie_groups[car.map_y]:
                if zombie and zombie.state != c.DIE and (not zombie.lostHead) and zombie.rect.x <= 0:
                    car.setWalk()
                if zombie.rect.x <= car.rect.x:
                    zombie.health = 0
                    zombie.kill()
            if car.dead:
                self.cars.remove(car)

    def boomZombies(self, x, map_y, y_range, x_range):
        for i in range(self.map_y_len):
            if abs(i - map_y) > y_range:
                continue
            for zombie in self.zombie_groups[i]:
                if ((abs(zombie.rect.centerx - x) <= x_range) or
                ((zombie.rect.right - (x-x_range) > 20) or (zombie.rect.right - (x-x_range))/zombie.rect.width > 0.15, ((x+x_range) - zombie.rect.left > 20) or ((x+x_range) - zombie.rect.left)/zombie.rect.width > 0.15)[zombie.rect.x > x]):  # 这代码不太好懂，后面是一个判断僵尸在左还是在右，前面是一个元组，[0]是在左边的情况，[1]是在右边的情况
                    zombie.health -= 1800
                    if zombie.health <= 0:
                        zombie.setBoomDie()

    def freezeZombies(self, plant):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.left <= c.SCREEN_WIDTH:
                    zombie.setFreeze(plant.trap_frames[0])
                    zombie.setDamage(20)    # 寒冰菇还有全场20的伤害

    def killPlant(self, plant, shovel=False):
        x, y = plant.getPosition()
        map_x, map_y = self.map.getMapIndex(x, y)
        if self.bar_type != c.CHOSSEBAR_BOWLING:
            # 更改地图类型、添加南瓜头、睡莲、花盆后可能也需要改这里
            self.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
        # 用铲子铲不用触发植物功能
        if not shovel:
            if (plant.name == c.CHERRYBOMB or plant.name == c.JALAPENO or
                plant.name == c.REDWALLNUTBOWLING):
                self.boomZombies(plant.rect.centerx, map_y, plant.explode_y_range,
                                plant.explode_x_range)
            elif plant.name == c.ICESHROOM and plant.state != c.SLEEP:
                self.freezeZombies(plant)
            elif plant.name == c.HYPNOSHROOM and plant.state != c.SLEEP:
                zombie = plant.kill_zombie
                zombie.setHypno()
                _, map_y = self.map.getMapIndex(zombie.rect.centerx, zombie.rect.bottom)
                self.zombie_groups[map_y].remove(zombie)
                self.hypno_zombie_groups[map_y].add(zombie)
            elif (plant.name == c.POTATOMINE and not plant.is_init):    # 土豆雷不是灰烬植物，不能用Boom
                zombie.setDamage(1800)
        # 避免僵尸在用铲子移除植物后还在原位啃食
        plant.health = 0
        plant.kill()

    def checkPlant(self, plant, i):
        zombie_len = len(self.zombie_groups[i])
        if plant.name == c.THREEPEASHOOTER:
            if plant.state == c.IDLE:
                if zombie_len > 0:
                    plant.setAttack()
                elif (i-1) >= 0 and len(self.zombie_groups[i-1]) > 0:
                    plant.setAttack()
                elif (i+1) < self.map_y_len and len(self.zombie_groups[i+1]) > 0:
                    plant.setAttack()
            elif plant.state == c.ATTACK:
                if zombie_len > 0:
                    pass
                elif (i-1) >= 0 and len(self.zombie_groups[i-1]) > 0:
                    pass
                elif (i+1) < self.map_y_len and len(self.zombie_groups[i+1]) > 0:
                    pass
                else:
                    plant.setIdle()
        elif plant.name == c.CHOMPER:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack(zombie, self.zombie_groups[i])
                    break
        elif plant.name == c.POTATOMINE:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack()
                    break
        elif plant.name == c.SQUASH:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack(zombie, self.zombie_groups[i])
                    break
        elif plant.name == c.SPIKEWEED:
            can_attack = False
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    can_attack = True
                    break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack(self.zombie_groups[i])
            elif plant.state == c.ATTACK and not can_attack:
                plant.setIdle()
        elif plant.name == c.SCAREDYSHROOM:
            need_cry = False
            can_attack = False
            for zombie in self.zombie_groups[i]:
                if plant.needCry(zombie):
                    need_cry = True
                    break
                elif plant.canAttack(zombie):
                    can_attack = True
            if need_cry:
                if plant.state != c.CRY:
                    plant.setCry()
            elif can_attack:
                if plant.state != c.ATTACK:
                    plant.setAttack()
            elif plant.state != c.IDLE:
                plant.setIdle()
        elif(plant.name == c.WALLNUTBOWLING or
             plant.name == c.REDWALLNUTBOWLING):
            pass
        else:
            can_attack = False
            if (plant.state == c.IDLE and zombie_len > 0):
                for zombie in self.zombie_groups[i]:
                    if plant.canAttack(zombie):
                        can_attack = True
                        break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack()
            elif (plant.state == c.ATTACK and not can_attack):
                plant.setIdle()

    def checkPlants(self):
        for i in range(self.map_y_len):
            for plant in self.plant_groups[i]:
                if plant.state != c.SLEEP:
                    self.checkPlant(plant, i)
                if plant.health <= 0:
                    self.killPlant(plant)

    def checkVictory(self):
        if len(self.zombie_list) > 0:
            return False
        for i in range(self.map_y_len):
            if len(self.zombie_groups[i]) > 0:
                return False
        return True
    
    def checkLose(self):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.right < -10 and (not zombie.lostHead):
                    return True
        return False

    def checkGameState(self):
        if self.checkVictory():
            if c.LITTLEGAME_BUTTON in self.game_info:
                self.game_info[c.LITTLEGAME_NUM] += 1
            else:
                self.game_info[c.LEVEL_NUM] += 1
            self.next = c.GAME_VICTORY
            self.done = True
        elif self.checkLose():
            self.next = c.GAME_LOSE
            self.done = True

    def drawMouseShow(self, surface):
        if self.hint_plant:
            surface.blit(self.hint_image, self.hint_rect)
        x, y = pg.mouse.get_pos()
        self.mouse_rect.centerx = x
        self.mouse_rect.centery = y
        surface.blit(self.mouse_image, self.mouse_rect)
    
    def drawMouseShowPlus(self, surface):
        x, y = pg.mouse.get_pos()
        self.shovel_rect.centerx = x
        self.shovel_rect.centery = y
        surface.blit(self.shovel, self.shovel_rect)

    def drawZombieFreezeTrap(self, i, surface):
        for zombie in self.zombie_groups[i]:
            zombie.drawFreezeTrap(surface)

    def draw(self, surface):
        self.level.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.level, (0,0), self.viewport)
        if self.state == c.CHOOSE:
            self.panel.draw(surface)
        elif self.state == c.PLAY:
            if self.hasShovel:
                # 画铲子
                surface.blit(self.shovel_box, self.shovel_box_rect)
                surface.blit(self.shovel, self.shovel_rect)
            # 画小菜单
            surface.blit(self.little_menu, self.little_menu_rect)

            self.menubar.draw(surface)
            for car in self.cars:
                car.draw(surface)
            for i in range(self.map_y_len):
                self.plant_groups[i].draw(surface)
                self.zombie_groups[i].draw(surface)
                self.hypno_zombie_groups[i].draw(surface)
                self.bullet_groups[i].draw(surface)
                self.drawZombieFreezeTrap(i, surface)
            self.head_group.draw(surface)
            self.sun_group.draw(surface)

            if self.drag_plant:
                self.drawMouseShow(surface)
            
            if self.hasShovel and self.drag_shovel:
                self.drawMouseShowPlus(surface)

            if self.showLittleMenu:
                surface.blit(self.big_menu, self.big_menu_rect)
                surface.blit(self.return_button, self.return_button_rect)
                surface.blit(self.restart_button, self.restart_button_rect)
                surface.blit(self.mainMenu_button, self.mainMenu_button_rect)