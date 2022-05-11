import os
import json
import sys
import pygame as pg
from random import randint, uniform, choices
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

        # 暂停状态
        self.pause = False
        self.pauseTime = 0

        # 默认显然不用显示菜单
        self.showLittleMenu = False
        
        # 导入地图参数
        self.loadMap()
        self.map = map.Map(self.map_data[c.BACKGROUND_TYPE])
        self.map_y_len = self.map.height
        self.setupBackground()
        self.initState()

    def loadMap(self):
        if self.game_info[c.GAME_MODE] == c.MODE_LITTLEGAME:
            map_file = 'littleGame_' + str(self.game_info[c.LITTLEGAME_NUM]) + '.json'
        elif self.game_info[c.GAME_MODE] == c.MODE_ADVENTURE:
            map_file = 'level_' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'resources' , 'data', 'map', map_file)
        # 最后一关之后应该结束了
        try:
            f = open(file_path)
            self.map_data = json.load(f)
            f.close()
        except Exception as e:
            print("成功通关！")
            if self.game_info[c.GAME_MODE] == c.MODE_LITTLEGAME:
                self.game_info[c.LEVEL_NUM] = c.START_LEVEL_NUM
            elif self.game_info[c.GAME_MODE] == c.MODE_LITTLEGAME:
                self.game_info[c.LITTLEGAME_NUM] = c.START_LITTLE_GAME_NUM
            self.done = True
            self.next = c.MAIN_MENU
            pg.mixer.music.stop()
            pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
            pg.mixer.music.play(-1, 0)
            return
        # 是否有铲子的信息：无铲子时为0，有铲子时为1，故直接赋值即可
        self.hasShovel = self.map_data[c.SHOVEL]

        # 同时指定音乐
        # 缺省音乐为进入的音乐，方便发现错误
        self.bgm = 'intro.opus'
        if c.CHOOSEBAR_TYPE in self.map_data:  # 指定了choosebar_type的传送带关
            if self.map_data[c.CHOOSEBAR_TYPE] == c.CHOSSEBAR_BOWLING:   # 坚果保龄球
                self.bgm = 'bowling.opus'
            elif self.map_data[c.CHOOSEBAR_TYPE] == c.CHOOSEBAR_MOVE:  # 传送带
                self.bgm = 'battle.opus'
        else:   # 一般选卡关，非传送带
            # 白天类
            if self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_DAY, c.BACKGROUND_SINGLE, c.BACKGROUND_TRIPLE}:
                self.bgm = 'dayLevel.opus'
            # 夜晚
            elif self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_NIGHT}:
                self.bgm = 'nightLevel.opus'
            # 泳池
            elif self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_POOL}:
                self.bgm = 'poolLevel.opus'
            # 浓雾
            elif self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_FOG}:
                self.bgm = 'fogLevel.opus'

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


    # 按照规则生成每一波僵尸
    # 可以考虑将波刷新和一波中的僵尸生成分开
    # useableZombie是指可用的僵尸种类的元组
    # inevitableZombie指在本轮必然出现的僵尸，输入形式为字典: {波数1:(僵尸1, 僵尸2……), 波数2:(僵尸1, 僵尸2……)……}
    def createWaves(self, useableZombies, numFlags, survivalRounds=0, inevitableZombieDict=None):

        waves = []

        self.numFlags = numFlags

        # 权重值
        weights = []
        for zombie in useableZombies:
            weights.append(self.createZombieInfo[zombie][1])

        # 按照原版pvz设计的僵尸容量函数，是从无尽解析的，但是普通关卡也可以遵循
        for wave in range(1, 10 * numFlags + 1):
            volume = int(int((wave + survivalRounds*20)*0.8)/2) + 1
            zombieList = []

            # 大波僵尸情况
            if wave % 10 == 0:
                # 容量增大至2.5倍
                volume = int(volume*2.5)
                # 先生成旗帜僵尸
                zombieList.append(c.FLAG_ZOMBIE)
                volume -= self.createZombieInfo[c.FLAG_ZOMBIE][0]

            # 传送带模式应当增大僵尸容量
            if (self.bar_type != c.CHOOSEBAR_STATIC):
                volume += 2

            if inevitableZombieDict and (str(wave) in inevitableZombieDict):
                for newZombie in inevitableZombieDict[str(wave)]:
                    zombieList.append(newZombie)
                    volume -= self.createZombieInfo[newZombie][0]
                if volume < 0:
                    print('警告：第{}波中手动设置的僵尸级别总数超过上限！'.format(wave))

            # 防止因为僵尸最小等级过大，使得总容量无法完全利用，造成死循环的检查机制
            minCost = self.createZombieInfo[min(useableZombies, key=lambda x:self.createZombieInfo[x][0])][0]
            
            while (volume >= minCost) and (len(zombieList) < 50):
                newZombie = choices(useableZombies, weights)[0]
                # 普通僵尸、路障僵尸、铁桶僵尸有概率生成水中变种
                if self.background_type in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
                    # 有泳池第一轮的第四波设定上生成水生僵尸
                    if survivalRounds == 0 and wave == 4:
                        if newZombie in self.convertZombieInPool:
                            newZombie = self.convertZombieInPool[newZombie]
                    elif survivalRounds > 0 or wave > 4:
                        if randint(1, 3) == 1:  # 1/3概率水上，暂时人为设定
                            if newZombie in self.convertZombieInPool:
                                newZombie = self.convertZombieInPool[newZombie]
                if self.createZombieInfo[newZombie][0] <= volume:
                    zombieList.append(newZombie)
                    volume -= self.createZombieInfo[newZombie][0]
            waves.append(zombieList)
            #print(wave, zombieList, len(zombieList))

        self.waves = waves

        # 针对有泳池的关卡
        # 表示尚未生成最后一波中从水里冒出来的僵尸
        self.createdZombieFromPool = False


    # 僵尸的刷新机制
    def refreshWaves(self, current_time, survivalRounds=0):
        # 最后一波或者大于最后一波
        # 如果在夜晚按需从墓碑生成僵尸
        # 否则直接return
        if self.waveNum >= self.map_data[c.NUM_FLAGS] * 10:
            if self.map_data[c.BACKGROUND_TYPE] == c.BACKGROUND_NIGHT:
                # 生长墓碑
                if not self.graveInLevelAdded:
                    if current_time - self.waveTime > 100:
                        # 墓碑最多有12个
                        if len(self.graveSet) < 12:
                            unoccupied = []
                            occupied = []
                            # 遍历能生成墓碑的区域
                            for mapY in range(0, 4):
                                for mapX in range(4, 8):
                                    # 为空、为毁灭菇坑、为冰道时看作未被植物占据
                                    if ((not self.map.map[mapY][mapX][c.MAP_PLANT]) or
                                        (all((i in {c.HOLE, c.ICE_FROZEN_PLOT}) for i in self.map.map[mapY][mapX][c.MAP_PLANT]))):
                                        unoccupied.append((mapX, mapY))
                                    # 已有墓碑的格子不应该放到任何列表中
                                    elif c.GRAVE not in self.map.map[mapY][mapX][c.MAP_PLANT]:
                                        occupied.append((mapX, mapY))
                            if unoccupied:
                                target = unoccupied[randint(0, len(unoccupied) - 1)]
                                mapX, mapY = target
                                posX, posY = self.map.getMapGridPos(mapX, mapY)
                                self.plant_groups[mapY].add(plant.Grave(posX, posY))
                                self.map.map[mapY][mapX][c.MAP_PLANT].add(c.GRAVE)
                                self.graveSet.add((mapX, mapY))
                            elif occupied:
                                target = occupied[randint(0, len(occupied) - 1)]
                                mapX, mapY = target
                                posX, posY = self.map.getMapGridPos(mapX, mapY)
                                for i in self.plant_groups[mapY]:
                                    checkMapX, _ = self.map.getMapIndex(i.rect.centerx, i.rect.bottom)
                                    if mapX == checkMapX:
                                        if i.name not in {c.HOLE, c.ICE_FROZEN_PLOT}:
                                            i.health = 0
                                self.plant_groups[mapY].add(plant.Grave(posX, posY))
                                self.map.map[mapY][mapX][c.MAP_PLANT].add(c.GRAVE)
                                self.graveSet.add((mapX, mapY))
                            self.graveInLevelAdded = True
                # 从墓碑中生成僵尸
                if not self.graveZombieCreated:
                    if current_time - self.waveTime > 1500:
                        for item in self.graveSet:
                            itemX, itemY = self.map.getMapGridPos(*item)
                            self.zombie_groups[item[1]].add(zombie.NormalZombie(itemX, itemY, self.head_group))
                        self.graveZombieCreated = True
            elif self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
                if not self.createdZombieFromPool:
                    if current_time - self.waveTime > 1500:
                        for i in range(3):
                            # 水中倒数四列内可以在此时产生僵尸。共产生3个
                            mapX, mapY = randint(5, 8), randint(2, 3)
                            itemX, itemY = self.map.getMapGridPos(mapX, mapY)
                            # 用随机数指定产生的僵尸类型
                            # 带有权重
                            zombieType = randint(1, 6)
                            if zombieType == 1:
                                self.zombie_groups[mapY].add(zombie.BucketHeadDuckyTubeZombie(itemX, itemY, self.head_group))
                            elif zombieType <= 3:
                                self.zombie_groups[mapY].add(zombie.ConeHeadDuckyTubeZombie(itemX, itemY, self.head_group))
                            else:
                                self.zombie_groups[mapY].add(zombie.DuckyTubeZombie(itemX, itemY, self.head_group))
                        self.createdZombieFromPool = True
            return

        # 还未开始出现僵尸
        if (self.waveNum == 0):
            if (self.waveTime == 0):    # 表明刚刚开始游戏
                self.waveTime = current_time
            else:
                if (survivalRounds == 0) and (self.bar_type == c.CHOOSEBAR_STATIC): # 首次选卡等待时间较长
                    if current_time - self.waveTime >= 18000:
                        self.waveNum += 1
                        self.waveTime = current_time
                        self.waveZombies = self.waves[self.waveNum - 1]
                        self.numZombie = len(self.waveZombies)
                        pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "zombieComing.ogg")).play()
                else:
                    if (current_time - self.waveTime >= 6000):
                        self.waveNum += 1
                        self.waveTime = current_time
                        self.waveZombies = self.waves[self.waveNum - 1]
                        self.numZombie = len(self.waveZombies)
                        pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "zombieComing.ogg")).play()
            return
        if (self.waveNum % 10 != 9):
            if ((current_time - self.waveTime >= 25000 + randint(0, 6000)) or (self.bar_type != c.CHOOSEBAR_STATIC and current_time - self.waveTime >= 12500 + randint(0, 3000))):
                self.waveNum += 1
                self.waveTime = current_time
                self.waveZombies = self.waves[self.waveNum - 1]
                self.numZombie = len(self.waveZombies)
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "zombieVoice.ogg")).play()
        else:
            if ((current_time - self.waveTime >= 45000) or (self.bar_type != c.CHOOSEBAR_STATIC and current_time - self.waveTime >= 25000)):
                self.waveNum += 1
                self.waveTime = current_time
                self.waveZombies = self.waves[self.waveNum - 1]
                self.numZombie = len(self.waveZombies)
                # 一大波时播放音效
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "hugeWaveApproching.ogg")).play()
                return
            elif ((current_time - self.waveTime >= 43000) or (self.bar_type != c.CHOOSEBAR_STATIC and current_time - self.waveTime >= 23000)):
                self.showHugeWaveApprochingTime = current_time
        
        numZombies = 0
        for i in range(self.map_y_len):
            numZombies += len(self.zombie_groups[i])
        if (numZombies / self.numZombie < uniform(0.15, 0.25)) and (current_time - self.waveTime > 4000):
            # 当僵尸所剩无几并且时间过了4000 ms以上时，改变时间记录，使得2000 ms后刷新僵尸（所以需要判断剩余时间是否大于2000 ms）
            if self.bar_type == c.CHOOSEBAR_STATIC:
                if current_time - 43000 < self.waveTime:    # 判断剩余时间是否有2000 ms
                    self.waveTime = current_time - 43000    # 即倒计时2000 ms
            else:
                if current_time - 23000 < self.waveTime:    # 判断剩余时间是否有2000 ms
                    self.waveTime = current_time - 23000    # 即倒计时2000 ms


    # 旧机制，目前仅用于调试
    def setupZombies(self):
        def takeTime(element):
            return element[0]

        self.zombie_list = []
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
            self.cars.append(plant.Car(-40, y+20, i))
    
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
        for x in range(3, self.map.width):
            for y in range(self.map.height):
                self.map.setMapGridType(x, y, c.MAP_STATE_UNAVAILABLE) # 将坚果保龄球红线右侧设置为不可种植任何植物

    def initState(self):
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
        self.panel = menubar.Panel(menubar.cards_to_choose, self.map_data[c.INIT_SUN_NAME])

        # 播放选卡音乐
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "chooseYourSeeds.opus"))
        pg.mixer.music.play(-1, 0)

    def choose(self, mouse_pos, mouse_click):
        if mouse_pos and mouse_click[0]:
            self.panel.checkCardClick(mouse_pos)
            if self.panel.checkStartButtonClick(mouse_pos):
                self.initPlay(self.panel.getSelectedCards())

    def initPlay(self, card_list):

        # 播放bgm
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", self.bgm))
        pg.mixer.music.play(-1, 0)

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

        # 种植植物后应当刷新僵尸的攻击对象，当然，默认初始时不用刷新
        self.refreshZombieAttack = False

        # 0:白天 1:夜晚 2:泳池 3:浓雾 4:屋顶 5:月夜 6:坚果保龄球
        # 还准备加入    7:单行草皮 8:三行草皮 但是目前没有找到图（
        if self.background_type in {0, 2, 4, 7, 8} and self.bar_type == c.CHOOSEBAR_STATIC:
            self.produce_sun = True
        else:
            self.produce_sun = False
        self.sun_timer = self.current_time

        self.removeMouseImage()
        self.setupGroups()
        if (c.ZOMBIE_LIST in self.map_data.keys()) and self.map_data[c.SPAWN_ZOMBIES] == c.SPAWN_ZOMBIES_LIST:
            self.setupZombies()
        else:
            # 僵尸波数数据及僵尸生成数据
            self.waveNum = 0   # 还未出现僵尸时定义为0
            self.waveTime = 0
            self.waveZombies = []
            self.numZombie = 0
            # 新的僵尸生成机制：级别——权重生成
            self.createZombieInfo = {# 生成僵尸:(级别, 权重)
                c.NORMAL_ZOMBIE:(1, 4000),
                c.FLAG_ZOMBIE:(1, 0),
                c.CONEHEAD_ZOMBIE:(2, 4000),
                c.BUCKETHEAD_ZOMBIE:(4, 3000),
                c.NEWSPAPER_ZOMBIE:(2, 1000),
                c.FOOTBALL_ZOMBIE:(7, 2000),
                c.DUCKY_TUBE_ZOMBIE:(1, 0),  # 作为变种，不主动生成
                c.CONEHEAD_DUCKY_TUBE_ZOMBIE:(2, 0),    # 作为变种，不主动生成
                c.BUCKETHEAD_DUCKY_TUBE_ZOMBIE:(4, 0),  # 作为变种，不主动生成
                c.SCREEN_DOOR_ZOMBIE:(4, 3500),
                c.POLE_VAULTING_ZOMBIE:(2, 2000),
                }
            # 将僵尸与水上变种对应
            self.convertZombieInPool = {c.NORMAL_ZOMBIE:c.DUCKY_TUBE_ZOMBIE,
                                        c.CONEHEAD_ZOMBIE:c.CONEHEAD_DUCKY_TUBE_ZOMBIE,
                                        c.BUCKETHEAD_ZOMBIE:c.BUCKETHEAD_DUCKY_TUBE_ZOMBIE}

            # 暂时没有生存模式，所以 survivalRounds = 0
            if c.INEVITABLE_ZOMBIE_DICT in self.map_data.keys():
                self.createWaves(   useableZombies=self.map_data[c.INCLUDED_ZOMBIES],
                                    numFlags=self.map_data[c.NUM_FLAGS],
                                    survivalRounds=0,
                                    inevitableZombieDict=self.map_data[c.INEVITABLE_ZOMBIE_DICT])
            else:
                self.createWaves(   useableZombies=self.map_data[c.INCLUDED_ZOMBIES],
                                    numFlags=self.map_data[c.NUM_FLAGS],
                                    survivalRounds=0)
        self.setupCars()

        # 地图有铲子才添加铲子
        if self.hasShovel:
            #  导入小铲子
            frame_rect = [0, 0, 71, 67]
            self.shovel = tool.get_image_menu(tool.GFX[c.SHOVEL], *frame_rect, c.BLACK, 1.1)
            self.shovel_rect = self.shovel.get_rect()
            frame_rect = [0, 0, 77, 75]
            self.shovel_positon = (608, 1)
            self.shovel_box = tool.get_image_menu(tool.GFX[c.SHOVEL_BOX], *frame_rect, c.BLACK, 1.1)
            self.shovel_box_rect = self.shovel_box.get_rect()
            self.shovel_rect.x = self.shovel_box_rect.x = self.shovel_positon[0]
            self.shovel_rect.y = self.shovel_box_rect.y = self.shovel_positon[1] 

        self.setupLittleMenu()

        self.setupLevelProgressBarImage()
        
        self.setupHugeWaveApprochingImage()
        self.showHugeWaveApprochingTime = -2000 # 防止设置为0时刚刚打开游戏就已经启动红字

        if self.map_data[c.BACKGROUND_TYPE] == c.BACKGROUND_NIGHT:
            if c.GRADE_GRAVES in self.map_data:
                gradeGraves = self.map_data[c.GRADE_GRAVES]
            # 缺省为少量墓碑
            else:
                gradeGraves = c.GRADE1_GRAVES
            
            if gradeGraves == c.GRADE1_GRAVES:
                graveVolume = 4
            elif gradeGraves == c.GRADE2_GRAVES:
                graveVolume = 7
            elif gradeGraves >= c.GRADE3_GRAVES:
                graveVolume = 11
            else:
                graveVolume = 0
            self.graveSet = set()
            while len(self.graveSet) < graveVolume:
                mapX = randint(4, 8)    # 注意是从0开始编号
                mapY = randint(0, 4)
                self.graveSet.add((mapX, mapY))
            if self.graveSet:
                for i in self.graveSet:
                    mapX, mapY = i
                    posX, posY = self.map.getMapGridPos(mapX, mapY)
                    self.plant_groups[mapY].add(plant.Grave(posX, posY))
                    self.map.map[mapY][mapX][c.MAP_PLANT].add(c.GRAVE)
            self.graveZombieCreated = False
            self.graveInLevelAdded = False


    # 小菜单
    def setupLittleMenu(self):
        # 具体运行游戏必定有个小菜单, 导入菜单和选项
        frame_rect = (0, 0, 108, 31)
        self.little_menu = tool.get_image_menu(tool.GFX[c.LITTLE_MENU], *frame_rect, c.BLACK, 1.1)
        self.little_menu_rect = self.little_menu.get_rect()
        self.little_menu_rect.x = 690
        self.little_menu_rect.y = 0 

        frame_rect = (0, 0, 500, 500)
        self.big_menu = tool.get_image_menu(tool.GFX[c.BIG_MENU], *frame_rect, c.BLACK, 1.1)
        self.big_menu_rect = self.big_menu.get_rect()
        self.big_menu_rect.x = 150
        self.big_menu_rect.y = 0

        frame_rect = (0, 0, 342, 87)
        self.return_button = tool.get_image_menu(tool.GFX[c.RETURN_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = 220
        self.return_button_rect.y = 440

        frame_rect = (0, 0, 207, 45)
        self.restart_button = tool.get_image_menu(tool.GFX[c.RESTART_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.restart_button_rect = self.restart_button.get_rect()
        self.restart_button_rect.x = 295
        self.restart_button_rect.y = 325

        frame_rect = (0, 0, 206, 43)
        self.mainMenu_button = tool.get_image_menu(tool.GFX[c.MAINMENU_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.mainMenu_button_rect = self.mainMenu_button.get_rect()
        self.mainMenu_button_rect.x = 299
        self.mainMenu_button_rect.y = 372

    # 一大波僵尸来袭图片显示
    def setupHugeWaveApprochingImage(self):
        frame_rect = (0, 0, 492, 80)
        self.huge_wave_approching_image = tool.get_image_menu(tool.GFX[c.HUGE_WAVE_APPROCHING], *frame_rect, c.BLACK, 1)
        self.huge_wave_approching_image_rect = self.huge_wave_approching_image.get_rect()
        self.huge_wave_approching_image_rect.x = 140    # 猜的
        self.huge_wave_approching_image_rect.y = 250    # 猜的

    # 关卡进程显示设置
    def setupLevelProgressBarImage(self):
        # 注意：定位一律采用与主进度条的相对位置

        # 主进度条
        frame_rect = (0, 0, 158, 26)
        self.level_progress_bar_image = tool.get_image_menu(tool.GFX[c.LEVEL_PROGRESS_BAR], *frame_rect, c.BLACK, 1)
        self.level_progress_bar_image_rect = self.level_progress_bar_image.get_rect()
        self.level_progress_bar_image_rect.x = 600      # 猜的
        self.level_progress_bar_image_rect.y = 565      # 猜的

        # 僵尸头
        frame_rect = (0, 0, 23, 25)
        self.level_progress_zombie_head_image = tool.get_image_menu(tool.GFX[c.LEVEL_PROGRESS_ZOMBIE_HEAD], *frame_rect, c.BLACK, 1)
        self.level_progress_zombie_head_image_rect = self.level_progress_zombie_head_image.get_rect()
        self.level_progress_zombie_head_image_rect.x = self.level_progress_bar_image_rect.x + 75      # 猜的
        self.level_progress_zombie_head_image_rect.y = self.level_progress_bar_image_rect.y - 3      # 猜的

        # 旗帜（这里只包括最后一面）
        frame_rect = (0, 0, 20, 18)
        self.level_progress_flag = tool.get_image_menu(tool.GFX[c.LEVEL_PROGRESS_FLAG], *frame_rect, c.BLACK, 1)
        self.level_progress_flag_rect = self.level_progress_flag.get_rect()
        self.level_progress_flag_rect.x = self.level_progress_bar_image_rect.x - 78     # 猜的
        self.level_progress_flag_rect.y = self.level_progress_bar_image_rect.y - 3      # 猜的

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
                if i.name in {c.HOLE, c.ICE_FROZEN_PLOT, c.GRAVE}:
                    continue
                # 优先移除花盆、睡莲上的植物而非花盆、睡莲本身
                if len(self.map.map[map_y][map_x][c.MAP_PLANT]) >= 2:
                    if c.LILYPAD in self.map.map[map_y][map_x][c.MAP_PLANT]:
                        if i.name == c.LILYPAD:
                            continue
                    elif '花盆（未实现）' in self.map.map[map_y][map_x][c.MAP_PLANT]:
                        if i.name == '花盆（未实现）':
                            continue
                self.killPlant(i, shovel=True)
                # 使用后默认铲子复原
                self.drag_shovel = not self.drag_shovel
                self.removeMouseImagePlus()
                return 

    # 检查小铲子的位置有没有被点击
    # 方便放回去
    def checkShovelClick(self, mouse_pos):
        x, y = mouse_pos
        if( self.hasShovel and
            x >= self.shovel_box_rect.x and x <= self.shovel_box_rect.right and
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
                    # 播放点击音效
                    pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()
                elif self.checkRestartClick(mouse_pos):
                    self.done = True
                    self.next = c.LEVEL
                    pg.mixer.music.stop()
                    pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", self.bgm))
                    pg.mixer.music.play(-1, 0)
                    # 播放点击音效
                    pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()
                elif self.checkMainMenuClick(mouse_pos):
                    self.done = True
                    self.next = c.MAIN_MENU
                    #self.persist = {c.CURRENT_TIME:0, c.LEVEL_NUM:c.START_LEVEL_NUM} # 应该不能用c.LEVEL_NUM:c.START_LEVEL_NUM
                    self.persist = {c.CURRENT_TIME:0, c.LEVEL_NUM:self.persist[c.LEVEL_NUM], c.LITTLEGAME_NUM:self.persist[c.LITTLEGAME_NUM]}
                    pg.mixer.music.stop()
                    pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
                    pg.mixer.music.play(-1, 0)
                    # 播放点击音效
                    pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()
            return

        if (c.ZOMBIE_LIST in self.map_data.keys()) and self.map_data[c.SPAWN_ZOMBIES] == c.SPAWN_ZOMBIES_LIST:
            # 旧僵尸生成方式
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
        else:
            # 新僵尸生成方式
            self.refreshWaves(self.current_time)
            for i in self.waveZombies:
                self.createZombie(i)
            else:
                self.waveZombies = []


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
                    # 播放收集阳光的音效
                    pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "collectSun.ogg")).play()

        # 拖动植物或者铲子
        if not self.drag_plant and mouse_pos and mouse_click[0] and not clickedSun:
            result = self.menubar.checkCardClick(mouse_pos)
            if result:
                self.setupMouseImage(result[0], result[1])
                clickedCardsOrMap = True
                # 播放音效
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "clickCard.ogg")).play()
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
                # 播放点击音效
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()
            elif self.checkShovelClick(mouse_pos):
                self.drag_shovel = not self.drag_shovel
                if not self.drag_shovel:
                    self.removeMouseImagePlus()
                # 播放点击铲子的音效
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "shovel.ogg")).play()
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
        # 0:白天 1:夜晚 2:泳池 3:浓雾 4:屋顶 5:月夜 6:坚果保龄球
        if map_y == None:
            # 情况复杂：分水路和陆路，不能简单实现，需要另外加判断
            # 0, 1, 4, 5路为陆路，2, 3路为水路
            if self.map_data[c.BACKGROUND_TYPE] in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
                if name in {c.DUCKY_TUBE_ZOMBIE, c.CONEHEAD_DUCKY_TUBE_ZOMBIE, c.BUCKETHEAD_DUCKY_TUBE_ZOMBIE}:  # 水生僵尸集合
                    map_y = randint(2, 3)
                elif name == '这里应该换成气球僵尸的名字（最好写调用的变量名，最好不要直接写，保持风格统一）':
                    map_y = randint(0, 5)
                else:   # 陆生僵尸
                    map_y = randint(0, 3)
                    if map_y >= 2:   # 后两路的map_y应当+2
                        map_y += 2
            elif self.map_data[c.BACKGROUND_TYPE] == c.BACKGROUND_SINGLE:
                map_y = 2
            elif self.map_data[c.BACKGROUND_TYPE] == c.BACKGROUND_TRIPLE:
                map_y = randint(1, 3)
            else:
                map_y = randint(0, 4)

        if not ((c.ZOMBIE_LIST in self.map_data.keys()) and self.map_data[c.SPAWN_ZOMBIES] == c.SPAWN_ZOMBIES_LIST):
            # 旗帜波出生点右移
            if self.waveNum % 10:
                hugeWaveMove = 0
            else:
                hugeWaveMove = 40
        else:
            hugeWaveMove = 0
        x, y = self.map.getMapGridPos(0, map_y)
        # 新增的僵尸也需要在这里声明
        if name == c.NORMAL_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NormalZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.CONEHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ConeHeadZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.BUCKETHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.BucketHeadZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.FLAG_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.FlagZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.NEWSPAPER_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NewspaperZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.FOOTBALL_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.FootballZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.DUCKY_TUBE_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.DuckyTubeZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.CONEHEAD_DUCKY_TUBE_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ConeHeadDuckyTubeZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.BUCKETHEAD_DUCKY_TUBE_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.BucketHeadDuckyTubeZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.SCREEN_DOOR_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ScreenDoorZombie(c.ZOMBIE_START_X + randint(-20, 20) + hugeWaveMove, y, self.head_group))
        elif name == c.POLE_VAULTING_ZOMBIE:
            # 撑杆跳生成位置不同
            self.zombie_groups[map_y].add(zombie.PoleVaultingZombie(c.ZOMBIE_START_X + randint(70, 80) + hugeWaveMove, y, self.head_group))

    # 能否种植物的判断：
    # 先判断位置是否合法 isValid(map_x, map_y)
    # 再判断位置是否可用 isMovable(map_x, map_y)
    def canSeedPlant(self, plantName):
        x, y = pg.mouse.get_pos()
        return self.map.checkPlantToSeed(x, y, plantName)
        
    # 种植物
    def addPlant(self):
        pos = self.canSeedPlant(self.plant_name)
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
            new_plant = plant.ThreePeaShooter(x, y, self.bullet_groups, map_y, self.map.background_type)
        elif self.plant_name == c.REPEATERPEA:
            new_plant = plant.RepeaterPea(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.CHOMPER:
            new_plant = plant.Chomper(x, y)
        elif self.plant_name == c.PUFFSHROOM:
            new_plant = plant.PuffShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.POTATOMINE:
            new_plant = plant.PotatoMine(x, y)
        elif self.plant_name == c.SQUASH:
            new_plant = plant.Squash(x, y, self.map.map[map_y][map_x][c.MAP_PLANT])
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
        elif self.plant_name == c.LILYPAD:
            new_plant = plant.LilyPad(x, y)
        elif self.plant_name == c.TORCHWOOD:
            new_plant = plant.TorchWood(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.STARFRUIT:
            new_plant = plant.StarFruit(x, y, self.bullet_groups[map_y], self)
        elif self.plant_name == c.COFFEEBEAN:
            new_plant = plant.CoffeeBean(x, y, self.plant_groups[map_y], self.map.map[map_y][map_x], self.map, map_x)
        elif self.plant_name == c.SEASHROOM:
            new_plant = plant.SeaShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.TALLNUT:
            new_plant = plant.TallNut(x, y)
        elif self.plant_name == c.TANGLEKLEP:
            new_plant = plant.TangleKlep(x, y)
        elif self.plant_name == c.DOOMSHROOM:
            new_plant = plant.DoomShroom(x, y, self.map.map[map_y][map_x])
        elif self.plant_name == c.GRAVEBUSTER:
            new_plant = plant.GraveBuster(x, y, self.plant_groups[map_y], self.map, map_x)
            # 播放吞噬音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "gravebusterchomp.ogg")).play()
        elif self.plant_name == c.FUMESHROOM:
            new_plant = plant.FumeShroom(x, y, self.bullet_groups[map_y], self.zombie_groups[map_y])


        if new_plant.can_sleep and self.background_type in {c.BACKGROUND_DAY, c.BACKGROUND_POOL, c.BACKGROUND_ROOF, c.BACKGROUND_WALLNUTBOWLING, c.BACKGROUND_SINGLE, c.BACKGROUND_TRIPLE}:
            new_plant.setSleep()
            mushroomSleep = True
        else:
            mushroomSleep = False
        self.plant_groups[map_y].add(new_plant)
        # 种植植物后应当刷新僵尸的攻击对象
        # 这里用植物名称代替布尔值，保存更多信息
        self.refreshZombieAttack = new_plant.name
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar.decreaseSunValue(self.select_plant.sun_cost)
            self.menubar.setCardFrozenTime(self.plant_name)
        else:
            self.menubar.deleateCard(self.select_plant)

        if self.bar_type != c.CHOSSEBAR_BOWLING:
                self.map.addMapPlant(map_x, map_y, self.plant_name, sleep=mushroomSleep)
        self.removeMouseImage()

        # 播放种植音效
        pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "plant.ogg")).play()

    def setupHintImage(self):
        pos = self.canSeedPlant(self.plant_name)
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
            # 花盆、睡莲图片应当下移一些
            if self.plant_name in {c.LILYPAD, '花盆（未实现）', c.TANGLEKLEP}:
                self.hint_rect.centerx = pos[0]
                self.hint_rect.bottom = pos[1] + 25
            else:
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

        if (plant_name in { c.POTATOMINE, c.SPIKEWEED,
                            c.JALAPENO, c.SCAREDYSHROOM,
                            c.SUNSHROOM, c.ICESHROOM,
                            c.HYPNOSHROOM, c.SQUASH,
                            c.WALLNUTBOWLING, c.REDWALLNUTBOWLING,
                            }):
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
        for i in range(self.map_y_len):
            for bullet in self.bullet_groups[i]:
                if bullet.name == c.FUME:
                    continue
                # elif bullet.name == c.BULLET_STAR:
                #     collided_func = pg.sprite.collide_circle_ratio(1)
                # else:
                #    collided_func = pg.sprite.collide_circle_ratio(0.7)
                collided_func = pg.sprite.collide_mask
                if bullet.state == c.FLY:
                    # 利用循环而非内建精灵组碰撞判断函数，处理更加灵活，可排除已死亡僵尸
                    for zombie in self.zombie_groups[i]:
                        if collided_func(zombie, bullet):
                            if zombie.state != c.DIE:
                                zombie.setDamage(bullet.damage, effect=bullet.effect, damageType=c.ZOMBIE_DEAFULT_DAMAGE)
                                bullet.setExplode()
                                # 火球有溅射伤害
                                if bullet.name == c.BULLET_FIREBALL:
                                    for rangeZombie in self.zombie_groups[i]:
                                        if abs(rangeZombie.rect.x - bullet.rect.x) <= (c.GRID_X_SIZE // 2):
                                            rangeZombie.setDamage(c.BULLET_DAMAGE_FIREBALL_RANGE, effect=False, damageType=c.ZOMBIE_DEAFULT_DAMAGE)
                                break
                        

    def checkZombieCollisions(self):
        # if self.bar_type == c.CHOSSEBAR_BOWLING:
        #     ratio = 0.6
        # else:
        #     ratio = 0.5
        # collided_func = pg.sprite.collide_circle_ratio(ratio)
        for i in range(self.map_y_len):
            hypo_zombies = []
            for zombie in self.zombie_groups[i]:
                if zombie.name in {c.POLE_VAULTING_ZOMBIE} and (not zombie.jumped):
                    collided_func = pg.sprite.collide_rect_ratio(0.6)
                else:
                    collided_func = pg.sprite.collide_mask
                if zombie.state != c.WALK:
                    if zombie.state != c.ATTACK:
                        continue
                    if (((zombie.prey.name not in {c.LILYPAD, "花盆（未实现）"}) and (self.refreshZombieAttack != "南瓜头（未实现）")) or (not self.refreshZombieAttack)):
                        continue
                if zombie.canSwim and (not zombie.swimming):
                    continue
                
                # 以下代码为了实现各个功能，极其凌乱，尚未优化性能
                attackableCommonPlants = []
                attackableBackupPlant = []
                # 利用更加精细的循环判断啃咬优先顺序
                for plant in self.plant_groups[i]:
                    if collided_func(plant, zombie):
                        if plant.name in {"南瓜头（未实现）"}:
                            targetPlant = plant
                            break
                        elif plant.name in {c.LILYPAD, "花盆（未实现）"}:
                            attackableBackupPlant.append(plant)
                        # 注意要剔除掉两个“假植物”，以及不能被啃的地刺
                        elif plant.name not in {c.HOLE, c.ICE_FROZEN_PLOT, c.GRAVE, c.SPIKEWEED}:
                            attackableCommonPlants.append(plant)
                else:
                    if attackableCommonPlants:
                        # 默认为最右侧的一个植物
                        targetPlant = max(attackableCommonPlants, key=lambda i: i.rect.x)
                    elif attackableBackupPlant:
                        targetPlant = max(attackableBackupPlant, key=lambda i: i.rect.x)
                        map_x, map_y = self.map.getMapIndex(targetPlant.rect.centerx, targetPlant.rect.centery)
                        if len(self.map.map[map_y][map_x][c.MAP_PLANT]) >= 2:
                            for actualTargetPlant in self.plant_groups[i]:
                                # 检测同一格的其他植物
                                if self.map.getMapIndex(actualTargetPlant.rect.centerx, actualTargetPlant.rect.bottom) == (map_x, map_y):
                                    if actualTargetPlant.name in {"南瓜头（未实现）"}:
                                        targetPlant = actualTargetPlant
                                        break
                                    elif actualTargetPlant.name not in {c.LILYPAD, "花盆（未实现）"}:
                                        attackableCommonPlants.append(actualTargetPlant)
                            else:
                                if attackableCommonPlants:
                                    targetPlant = attackableCommonPlants[-1]
                    else:
                        targetPlant = None

                if targetPlant:
                    # 撑杆跳的特殊情况
                    if zombie.name in {c.POLE_VAULTING_ZOMBIE} and (not zombie.jumped):
                        if not zombie.jumping:
                            zombie.jumpMap_x, zombie.jumpMap_y = self.map.getMapIndex(targetPlant.rect.centerx, targetPlant.rect.centery)
                            zombie.jumpMap_x, zombie.jumpMap_y = min(c.GRID_X_LEN, zombie.jumpMap_x), min(self.map_y_len, zombie.jumpMap_y)
                            jumpX = targetPlant.rect.x - c.GRID_X_SIZE * 0.6
                            if c.TALLNUT in self.map.map[zombie.jumpMap_y][zombie.jumpMap_x][c.MAP_PLANT]:
                                zombie.setJump(False, jumpX)
                            else:
                                zombie.setJump(True, jumpX)
                        else:
                            if c.TALLNUT in self.map.map[zombie.jumpMap_y][zombie.jumpMap_x][c.MAP_PLANT]:
                                zombie.setJump(False, zombie.jumpX)
                            else:
                                zombie.setJump(True, zombie.jumpX)
                        continue

                    if targetPlant.name == c.WALLNUTBOWLING:
                        if targetPlant.canHit(i):
                            zombie.setDamage(c.WALLNUT_BOWLING_DAMAGE, damageType=c.ZOMBIE_WALLNUT_BOWLING_DANMAGE)
                            # 注意：以上语句为通用处理，以后加入了铁门僵尸需要单独设置直接冲撞就直接杀死
                            # 可以给坚果保龄球设置attacked属性，如果attacked就秒杀（setDamage的攻击类型此时设置为COMMMON）铁门
                            targetPlant.changeDirection(i)
                            # 播放撞击音效
                            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "bowlingimpact.ogg")).play()
                    elif targetPlant.name == c.REDWALLNUTBOWLING:
                        if targetPlant.state == c.IDLE:
                            targetPlant.setAttack()
                    else:
                        zombie.setAttack(targetPlant)

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

        else:
            self.refreshZombieAttack = False    # 生效后需要解除刷新设置

    def checkCarCollisions(self):
        for car in self.cars:
            for zombie in self.zombie_groups[car.map_y]:
                if zombie and zombie.state != c.DIE and (not zombie.lostHead) and zombie.rect.centerx <= 0:
                    car.setWalk()
                if zombie.rect.centerx <= car.rect.x:
                    zombie.health = 0
                    zombie.kill()
            if car.dead:
                self.cars.remove(car)

    def boomZombies(self, x, map_y, y_range, x_range, effect=False):
        for i in range(self.map_y_len):
            if abs(i - map_y) > y_range:
                continue
            for zombie in self.zombie_groups[i]:
                if ((abs(zombie.rect.centerx - x) <= x_range) or
                ((zombie.rect.right - (x-x_range) > 20) or (zombie.rect.right - (x-x_range))/zombie.rect.width > 0.2, ((x+x_range) - zombie.rect.left > 20) or ((x+x_range) - zombie.rect.left)/zombie.rect.width > 0.2)[zombie.rect.x > x]):  # 这代码不太好懂，后面是一个判断僵尸在左还是在右，前面是一个元组，[0]是在左边的情况，[1]是在右边的情况
                    if effect == c.BULLET_EFFECT_UNICE:
                        zombie.ice_slow_ratio = 1
                    zombie.setDamage(1800, damageType=c.ZOMBIE_ASH_DAMAGE)
                    if zombie.health <= 0:
                        zombie.setBoomDie()

    def freezeZombies(self, plant):
        # 播放冻结音效
        pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "freeze.ogg")).play()

        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.left <= c.SCREEN_WIDTH:
                    zombie.setFreeze(plant.trap_frames[0])
                    zombie.setDamage(20, damageType=c.ZOMBIE_RANGE_DAMAGE)    # 寒冰菇还有全场20的伤害

    def killPlant(self, targetPlant, shovel=False):
        x, y = targetPlant.getPosition()
        map_x, map_y = self.map.getMapIndex(x, y)

        # 用铲子铲不用触发植物功能
        if not shovel:
            if targetPlant.name in {c.CHERRYBOMB, c.REDWALLNUTBOWLING}:
                self.boomZombies(targetPlant.rect.centerx, map_y, targetPlant.explode_y_range,
                                targetPlant.explode_x_range)
            elif (targetPlant.name == c.DOOMSHROOM) and (targetPlant.state != c.SLEEP):
                x, y = targetPlant.originalX, targetPlant.originalY
                map_x, map_y = self.map.getMapIndex(x, y)
                self.boomZombies(targetPlant.rect.centerx, map_y, targetPlant.explode_y_range,
                                targetPlant.explode_x_range)
                for i in self.plant_groups[map_y]:
                    checkMapX, _ = self.map.getMapIndex(i.rect.centerx, i.rect.bottom)
                    if map_x == checkMapX:
                        i.health = 0
                self.plant_groups[map_y].add(plant.Hole(x, y, self.map.map[map_y][map_x][c.MAP_PLOT_TYPE]))
                self.map.map[map_y][map_x][c.MAP_PLANT].add(c.HOLE)
            elif targetPlant.name == c.JALAPENO:
                self.boomZombies(targetPlant.rect.centerx, map_y, targetPlant.explode_y_range,
                                targetPlant.explode_x_range, effect=c.BULLET_EFFECT_UNICE)
            elif targetPlant.name == c.ICESHROOM and targetPlant.state != c.SLEEP:
                self.freezeZombies(targetPlant)
            elif targetPlant.name == c.HYPNOSHROOM and targetPlant.state != c.SLEEP:
                zombie = targetPlant.zombie_to_hypno
                zombie.setHypno()
                _, map_y = self.map.getMapIndex(zombie.rect.centerx, zombie.rect.bottom)
                self.zombie_groups[map_y].remove(zombie)
                self.hypno_zombie_groups[map_y].add(zombie)
            elif (targetPlant.name == c.POTATOMINE and not targetPlant.is_init):    # 土豆雷不是灰烬植物，不能用Boom
                for zombie in self.zombie_groups[map_y]:
                    # 双判断：发生碰撞或在攻击范围内
                    if ((pg.sprite.collide_mask(zombie, targetPlant)) or
                    (abs(zombie.rect.centerx - x) <= targetPlant.explode_x_range)):
                        zombie.setDamage(1800, damageType=c.ZOMBIE_RANGE_DAMAGE)
            # 对于墓碑：移除存储在墓碑集合中的坐标
            # 注意这里是在描述墓碑而非墓碑吞噬者
            elif targetPlant.name == c.GRAVE:
                self.graveSet.remove((map_x, map_y))
            elif targetPlant.name not in {c.WALLNUTBOWLING, c.TANGLEKLEP}:
                # 触发植物死亡音效
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "plantDie.ogg")).play()
        else:
            # 用铲子移除植物时播放音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "plant.ogg")).play()

        # 整理地图信息
        if self.bar_type != c.CHOSSEBAR_BOWLING:
            self.map.removeMapPlant(map_x, map_y, targetPlant.name)
        # 将睡眠植物移除后更新睡眠状态
        if targetPlant.state == c.SLEEP:
            self.map.map[map_y][map_x][c.MAP_SLEEP] = False

        # 避免僵尸在用铲子移除植物后还在原位啃食
        targetPlant.health = 0
        targetPlant.kill()

    def checkPlant(self, plant, i):
        zombie_len = len(self.zombie_groups[i])
        # 没有攻击状态的植物
        if plant.name in {  c.WALLNUTBOWLING, c.REDWALLNUTBOWLING,
                            c.WALLNUT, c.TALLNUT,
                            c.TORCHWOOD, c.SUNFLOWER,
                            c.SUNSHROOM, c.COFFEEBEAN,
                            c.GRAVEBUSTER, c.LILYPAD}:
            pass
        elif plant.name == c.THREEPEASHOOTER:
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
        elif plant.name == c.STARFRUIT:
            can_attack = False
            for zombie_group in self.zombie_groups: # 遍历循环所有僵尸
                for zombie in zombie_group:
                    if plant.canAttack(zombie):
                        can_attack = True
                        break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack()
            elif (plant.state == c.ATTACK and not can_attack):
                plant.setIdle()
        elif plant.name == c.TANGLEKLEP:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack(zombie, self.zombie_groups[i])
                    break
        else:
            can_attack = False
            if (zombie_len > 0):
                for zombie in self.zombie_groups[i]:
                    if plant.canAttack(zombie):
                        can_attack = True
                        break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack()
            elif (plant.state == c.ATTACK and (not can_attack)):
                plant.setIdle()

    def checkPlants(self):
        for i in range(self.map_y_len):
            for plant in self.plant_groups[i]:
                if plant.state != c.SLEEP:
                    self.checkPlant(plant, i)
                if plant.health <= 0:
                    self.killPlant(plant)

    def checkVictory(self):
        if (c.ZOMBIE_LIST in self.map_data.keys()) and self.map_data[c.SPAWN_ZOMBIES] == c.SPAWN_ZOMBIES_LIST:
            if len(self.zombie_list) > 0:
                return False
            for i in range(self.map_y_len):
                if len(self.zombie_groups[i]) > 0:
                    return False
            return True
        else:
            if self.waveNum < self.map_data[c.NUM_FLAGS] * 10:
                return False
            for i in range(self.map_y_len):
                if len(self.zombie_groups[i]) > 0:
                    return False
            return True
    
    def checkLose(self):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.right < -20 and (not zombie.lostHead) and zombie.state != c.DIE:
                    return True
        return False

    def checkGameState(self):
        if self.checkVictory():
            if self.game_info[c.GAME_MODE] == c.MODE_LITTLEGAME:
                self.game_info[c.LITTLEGAME_NUM] += 1
            elif self.game_info[c.GAME_MODE] == c.MODE_ADVENTURE:
                self.game_info[c.LEVEL_NUM] += 1
            self.next = c.GAME_VICTORY
            self.done = True
            # 播放胜利音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "win.ogg")).play()
        elif self.checkLose():
            self.next = c.GAME_LOSE
            self.done = True
            # 播放失败音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "lose.ogg")).play()
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "scream.ogg")).play()

    def drawMouseShow(self, surface):
        if self.hint_plant:
            surface.blit(self.hint_image, self.hint_rect)
        x, y = pg.mouse.get_pos()
        self.mouse_rect.centerx = x
        self.mouse_rect.centery = y
        surface.blit(self.mouse_image, self.mouse_rect)
    
    def drawMouseShowPlus(self, surface):   # 拖动铲子时的显示
        x, y = pg.mouse.get_pos()
        self.shovel_rect.centerx = x
        self.shovel_rect.centery = y
        # 铲子接近植物时会高亮提示
        map_x, map_y = self.map.getMapIndex(x, y)
        surface.blit(self.shovel, self.shovel_rect)
        for i in self.plant_groups[map_y]:
            if (x >= i.rect.x and x <= i.rect.right and
                y >= i.rect.y and y <= i.rect.bottom):
                if i.name in {c.HOLE, c.ICE_FROZEN_PLOT, c.GRAVE}:
                    continue
                # 优先选中睡莲、花盆上的植物
                if len(self.map.map[map_y][map_x][c.MAP_PLANT]) >= 2:
                    if c.LILYPAD in self.map.map[map_y][map_x][c.MAP_PLANT]:
                        if i.name == c.LILYPAD:
                            continue
                    elif '花盆（未实现）' in self.map.map[map_y][map_x][c.MAP_PLANT]:
                        if i.name == '花盆（未实现）':
                            continue
                i.highlightTime = self.current_time
                return

    def drawZombieFreezeTrap(self, i, surface):
        for zombie in self.zombie_groups[i]:
            zombie.drawFreezeTrap(surface)


    def showLevelProgress(self, surface):
        # 画进度条框
        surface.blit(self.level_progress_bar_image, self.level_progress_bar_image_rect)

        # 按照当前波数生成僵尸头位置
        self.level_progress_zombie_head_image_rect.x = self.level_progress_bar_image_rect.x - int((150 * self.waveNum) / (self.map_data[c.NUM_FLAGS] * 10)) + 145      # 常数为预计值
        self.level_progress_zombie_head_image_rect.y = self.level_progress_bar_image_rect.y - 3      # 常数为预计值

        # 填充的进度条信息
        # 常数为预计值
        filledBarRect = (self.level_progress_zombie_head_image_rect.x + 3, self.level_progress_bar_image_rect.y + 6, int((150 * self.waveNum) / (self.map_data[c.NUM_FLAGS] * 10)) + 5, 9)
        # 画填充的进度条
        pg.draw.rect(surface, c.GREEN, filledBarRect)
        
        # 画旗帜
        for i in range(self.numFlags):
            self.level_progress_flag_rect.x = self.level_progress_bar_image_rect.x + int((150*i)/self.numFlags) + 5   # 常数是猜的
            # 当指示进度的僵尸头在旗帜左侧时升高旗帜
            if self.level_progress_flag_rect.x - 7 >= self.level_progress_zombie_head_image_rect.x:
                self.level_progress_flag_rect.y = self.level_progress_bar_image_rect.y - 15  # 常数是猜的
            else:
                self.level_progress_flag_rect.y = self.level_progress_bar_image_rect.y - 3  # 常数是猜的
            surface.blit(self.level_progress_flag, self.level_progress_flag_rect)
        
        # 画僵尸头
        surface.blit(self.level_progress_zombie_head_image, self.level_progress_zombie_head_image_rect)


    def draw(self, surface):
        self.level.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.level, (0,0), self.viewport)
        if self.state == c.CHOOSE:
            self.panel.draw(surface)
        # 以后可能需要插入一个预备的状态（预览显示僵尸、返回战场）
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

            if not ((c.ZOMBIE_LIST in self.map_data.keys()) and self.map_data[c.SPAWN_ZOMBIES] == c.SPAWN_ZOMBIES_LIST):
                self.showLevelProgress(surface)
                if self.current_time - self.showHugeWaveApprochingTime <= 2000:
                    surface.blit(self.huge_wave_approching_image, self.huge_wave_approching_image_rect)
