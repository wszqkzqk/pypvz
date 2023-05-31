import random
from .. import constants as c

# 记录植物种植情况的地图管理工具
class Map():
    def __init__(self, background_type:int):
        self.background_type = background_type
        # 注意：从0开始编号
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            self.width = c.GRID_POOL_X_LEN
            self.height = c.GRID_POOL_Y_LEN
            self.grid_height_size = c.GRID_POOL_Y_SIZE
            self.map =  [   [self.initMapGrid(c.MAP_WATER) if 2 <= y <= 3
                                else self.initMapGrid(c.MAP_GRASS)
                            for x in range(self.width)
                            ]
                        for y in range(self.height)
                        ]
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            self.width = c.GRID_ROOF_X_LEN
            self.height = c.GRID_ROOF_Y_LEN
            self.grid_height_size = c.GRID_ROOF_Y_SIZE
            self.map =  [   [self.initMapGrid(c.MAP_TILE)
                            for x in range(self.width)
                            ]
                        for y in range(self.height)
                        ]
        elif self.background_type == c.BACKGROUND_SINGLE:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.grid_height_size = c.GRID_Y_SIZE
            self.map =  [   [self.initMapGrid(c.MAP_GRASS) if y ==2
                                else self.initMapGrid(c.MAP_UNAVAILABLE)
                            for x in range(self.width)
                            ]
                        for y in range(self.height)
                        ]
        elif self.background_type == c.BACKGROUND_TRIPLE:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.grid_height_size = c.GRID_Y_SIZE
            self.map =  [   [self.initMapGrid(c.MAP_GRASS) if 1 <= y <= 3
                                else self.initMapGrid(c.MAP_UNAVAILABLE)
                            for x in range(self.width)
                            ]
                        for y in range(self.height)
                        ]
        else:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.grid_height_size = c.GRID_Y_SIZE
            self.map =  [   [self.initMapGrid(c.MAP_GRASS)
                            for x in range(self.width)
                            ]
                        for y in range(self.height)
                        ]

    def isValid(self, map_x:int, map_y:int) -> bool:
        if ((0 <= map_x < self.width)
        and (0 <= map_y < self.height)):
            return True
        return False

    # 地图单元格状态
    # 注意是可变对象，不能直接引用
    # 由于同一格显然不可能种两个相同的植物，所以用集合
    def initMapGrid(self, plot_type:str) -> set:
        return {c.MAP_PLANT:set(), c.MAP_SLEEP:False, c.MAP_PLOT_TYPE:plot_type}

    # 判断位置是否可用
    # 暂时没有写紫卡植物的判断方法
    # 由于紫卡植物需要移除以前的植物，所以可用另外定义一个函数
    def isAvailable(self, map_x:int, map_y:int, plant_name:str) -> bool:
        # 咖啡豆和墓碑吞噬者的判别最为特殊
        if plant_name == c.COFFEEBEAN:
            if (self.map[map_y][map_x][c.MAP_SLEEP]
            and (plant_name not in self.map[map_y][map_x][c.MAP_PLANT])):
                return True
            else:
                return False
        if plant_name == c.GRAVEBUSTER:
            if (c.GRAVE in self.map[map_y][map_x][c.MAP_PLANT]
            and (plant_name not in self.map[map_y][map_x][c.MAP_PLANT])):
                return True
            else:
                return False
        # 被非植物障碍占据的格子对于一般植物不可种植
        if any((i in c.NON_PLANT_OBJECTS) for i in self.map[map_y][map_x][c.MAP_PLANT]):
            return False
        if self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_GRASS:  # 草地
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plant_name not in c.WATER_PLANTS:
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 没有植物肯定可以种植
                    return True
                elif (all((i in {"花盆（未实现）", c.PUMPKINHEAD}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                and (plant_name not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植
                    return True
                elif ((plant_name == c.PUMPKINHEAD)
                and (c.PUMPKINHEAD not in self.map[map_y][map_x][c.MAP_PLANT])):   # 没有南瓜头就能种南瓜头
                    return True
                else:
                    return False
            else:
                return False
        elif self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_TILE: # 屋顶
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plant_name not in c.WATER_PLANTS:
                if "花盆（未实现）" in self.map[map_y][map_x][c.MAP_PLANT]:
                    if (all((i in {"花盆（未实现）", c.PUMPKINHEAD}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                    and (plant_name not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植
                        if plant_name in {c.SPIKEWEED}: # 不能在花盆上种植的植物
                            return False
                        else:
                            return True
                    elif ((plant_name == c.PUMPKINHEAD)
                    and (c.PUMPKINHEAD not in self.map[map_y][map_x][c.MAP_PLANT])):    # 有花盆且没有南瓜头就能种南瓜头
                        return True
                    else:
                        return False
                elif plant_name == "花盆（未实现）": # 这一格本来没有花盆而且新来的植物是花盆，可以种
                    return True
                else:
                    return False
            else:
                return False
        elif self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_WATER:   # 水里
            if plant_name in c.WATER_PLANTS:   # 是水生植物
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 只有无植物时才能在水里种植水生植物
                    return True
                else:
                    return False
            else:   # 非水生植物，依赖睡莲
                if c.LILYPAD in self.map[map_y][map_x][c.MAP_PLANT]:
                    if (all((i in {c.LILYPAD, c.PUMPKINHEAD}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                    and (plant_name not in self.map[map_y][map_x][c.MAP_PLANT])):
                        if plant_name in {c.SPIKEWEED, c.POTATOMINE, "花盆（未实现）"}: # 不能在睡莲上种植的植物
                            return False
                        else:
                            return True
                    elif ((plant_name == c.PUMPKINHEAD)
                    and (c.PUMPKINHEAD not in self.map[map_y][map_x][c.MAP_PLANT])):   # 在睡莲上且没有南瓜头就能种南瓜头
                        return True
                    else:
                        return False
                else:
                    return False
        else:   # 不可种植区域
            return False
    
    def getMapIndex(self, x:int, y:int) -> tuple[int, int]:
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            x -= c.MAP_POOL_OFFSET_X
            y -= c.MAP_POOL_OFFSET_Y
            return (x // c.GRID_POOL_X_SIZE, y // c.GRID_POOL_Y_SIZE)
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            x -= c.MAP_ROOF_OFFSET_X
            y -= c.MAP_ROOF_OFFSET_X
            grid_x = x // c.GRID_ROOF_X_SIZE
            if grid_x >= 5:
                grid_y = y // c.GRID_ROOF_Y_SIZE
            else:
                grid_y = (y - 20*(6 - grid_x)) // 85
            return (grid_x, grid_y)
        else:
            x -= c.MAP_OFFSET_X
            y -= c.MAP_OFFSET_Y
            return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)
    
    def getMapGridPos(self, map_x:int, map_y:int) -> tuple[int, int]:
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            return (map_x * c.GRID_POOL_X_SIZE + c.GRID_POOL_X_SIZE//2 + c.MAP_POOL_OFFSET_X,
                    map_y * c.GRID_POOL_Y_SIZE + c.GRID_POOL_Y_SIZE//5 * 3 + c.MAP_POOL_OFFSET_Y)
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            return (map_x * c.GRID_ROOF_X_SIZE + c.GRID_ROOF_X_SIZE//2 + c.MAP_ROOF_OFFSET_X,
                    map_y * c.GRID_ROOF_Y_SIZE + 20 * max(0, (6 - map_y)) + c.GRID_ROOF_Y_SIZE//5 * 3 + c.MAP_POOL_OFFSET_Y)
        else:
            return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X,
                    map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)
    
    def setMapGridType(self, map_x:int, map_y:int, plot_type:str):
        self.map[map_y][map_x][c.MAP_PLOT_TYPE] = plot_type

    def addMapPlant(self, map_x:int, map_y:int, plant_name:int, sleep:bool=False):
        self.map[map_y][map_x][c.MAP_PLANT].add(plant_name)
        self.map[map_y][map_x][c.MAP_SLEEP] = sleep
    
    def removeMapPlant(self, map_x:int, map_y:int, plant_name:str):
        self.map[map_y][map_x][c.MAP_PLANT].discard(plant_name)

    def getRandomMapIndex(self) -> tuple[int, int]:
        map_x = random.randint(0, self.width-1)
        map_y = random.randint(0, self.height-1)
        return (map_x, map_y)

    def checkPlantToSeed(self, x:int, y:int, plant_name:str) -> tuple[int, int]:
        pos = None
        map_x, map_y = self.getMapIndex(x, y)
        if self.isValid(map_x, map_y) and self.isAvailable(map_x, map_y, plant_name):
            pos = self.getMapGridPos(map_x, map_y)
        return pos

# 保存具体关卡地图信息常数
# 冒险模式地图
LEVEL_MAP_DATA = (
# 第0关：测试模式地图
{
    c.BACKGROUND_TYPE:  2,
    c.GAME_TITLE: "隐藏测试关卡",
    c.INIT_SUN_NAME:    5000,
    c.SHOVEL:           1,
    c.SPAWN_ZOMBIES:    c.SPAWN_ZOMBIES_LIST,
    c.ZOMBIE_LIST:(
        {"time":0, "map_y":5, "name":"Zomboni"},
        {"time":1000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":2000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":3100, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":4500, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":5000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":6000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":7000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":8000, "map_y":4, "name":"ScreenDoorZombie"},
        {"time":0, "map_y":1, "name":"NewspaperZombie"},
        {"time":0, "map_y":0, "name":"PoleVaultingZombie"},
        {"time":6000, "map_y":0, "name":"FootballZombie"},
        {"time":0, "map_y":3, "name":"ConeheadDuckyTubeZombie"},
        {"time":0, "map_y":2, "name":"SnorkelZombie"},
        {"time":90000, "map_y":2, "name":"ConeheadDuckyTubeZombie"}
    )
},
# 第1关：单行草皮
{
    c.BACKGROUND_TYPE: 7,
    c.GAME_TITLE: "白天 1-1",
    c.INIT_SUN_NAME: 150,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES:(c.NORMAL_ZOMBIE,),
    c.NUM_FLAGS:1
},
# 第2关：三行草皮
{
    c.BACKGROUND_TYPE: 8,
    c.GAME_TITLE: "白天 1-2",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES:(c.NORMAL_ZOMBIE,),
    c.NUM_FLAGS:1
},
# 第3关
{
    c.BACKGROUND_TYPE: 0,
    c.GAME_TITLE: "白天 1-3",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES:(c.NORMAL_ZOMBIE,),
    c.NUM_FLAGS:2
},
# 第4关
{
    c.BACKGROUND_TYPE: 0,
    c.GAME_TITLE: "白天 1-4",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE, c.POLE_VAULTING_ZOMBIE),
    c.NUM_FLAGS:2
},
# 第5关 目前白天最后一关
{
    c.BACKGROUND_TYPE: 0,
    c.GAME_TITLE: "白天 1-5",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.POLE_VAULTING_ZOMBIE, c.BUCKETHEAD_ZOMBIE),
    c.NUM_FLAGS:3
},
# 第6关 目前夜晚第一关
{
    c.BACKGROUND_TYPE: 1,
    c.GAME_TITLE: "黑夜 2-1",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE,
                            c.NEWSPAPER_ZOMBIE),
    c.NUM_FLAGS:2
},
# 第7关
{
    c.BACKGROUND_TYPE: 1,
    c.GAME_TITLE: "黑夜 2-2",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE,
                            c.SCREEN_DOOR_ZOMBIE,),
    c.NUM_FLAGS: 2,
    c.GRADE_GRAVES: 2,
},
# 第8关 目前为夜晚最后一关
{
    c.BACKGROUND_TYPE: 1,
    c.GAME_TITLE: "黑夜 2-3",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.NEWSPAPER_ZOMBIE,
                            c.CONEHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.SCREEN_DOOR_ZOMBIE, c.FOOTBALL_ZOMBIE),
    c.INEVITABLE_ZOMBIE_DICT:   {   # 这里改用python实现了以后，键不再用字符串，改用数字
                                    # 仍然要注意字典值是元组
                                    10: (c.NEWSPAPER_ZOMBIE,),
                                    20: (c.SCREEN_DOOR_ZOMBIE,),
                                    30: (c.FOOTBALL_ZOMBIE,),
                                    },
    c.NUM_FLAGS: 3,
    c.GRADE_GRAVES: 3,
},
# 第9关 目前为泳池模式第一关
{
    c.BACKGROUND_TYPE: 2,
    c.GAME_TITLE: "泳池 3-1",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.CONEHEAD_ZOMBIE,),
    c.NUM_FLAGS:2
},
# 第10关
{
    c.BACKGROUND_TYPE: 2,
    c.GAME_TITLE: "泳池 3-2",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.CONEHEAD_ZOMBIE, c.SNORKELZOMBIE),
    c.INEVITABLE_ZOMBIE_DICT: {30: (c.SNORKELZOMBIE,)},
    c.NUM_FLAGS:3
},
# 第11关
{
    c.BACKGROUND_TYPE: 2,
    c.GAME_TITLE: "泳池 3-3",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (c.NORMAL_ZOMBIE, c.ZOMBONI),
    c.INEVITABLE_ZOMBIE_DICT: {30: (c.ZOMBONI,)},
    c.NUM_FLAGS:3
},
# 第12关 目前为泳池最后一关
{
    c.BACKGROUND_TYPE: 2,
    c.GAME_TITLE: "泳池 3-4",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.ZOMBONI,
                            c.BUCKETHEAD_ZOMBIE,
                            c.CONEHEAD_ZOMBIE, c.SNORKELZOMBIE),
    c.INEVITABLE_ZOMBIE_DICT: {40: (c.ZOMBONI,)},
    c.NUM_FLAGS:4
},
# 第13关 目前为浓雾第一关 尚未完善
{
    c.BACKGROUND_TYPE: 3,
    c.GAME_TITLE: "浓雾 4-1",
    c.INIT_SUN_NAME: 50,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.NEWSPAPER_ZOMBIE,
                            c.ZOMBONI, c.FOOTBALL_ZOMBIE,
                            c.CONEHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE),
    c.NUM_FLAGS:4
},
)



# 玩玩小游戏地图
LITTLE_GAME_MAP_DATA = (
# 第0关 测试
{
    c.BACKGROUND_TYPE: 3,
    c.GAME_TITLE: "隐藏测试关卡",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_MOVE,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.NEWSPAPER_ZOMBIE,
                            c.ZOMBONI, c.FOOTBALL_ZOMBIE,
                            c.CONEHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE),
    c.NUM_FLAGS:4,
    c.CARD_POOL: {  c.LILYPAD: 300,
                    c.STARFRUIT: 400,
                    c.PUMPKINHEAD: 100,
                    c.SEASHROOM: 100,
                    c.SPIKEWEED: 100,
                    }
},
# 第1关 坚果保龄球
{
    c.BACKGROUND_TYPE: 6,
    c.GAME_TITLE: "坚果保龄球",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_BOWLING,
    c.SHOVEL: 0,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.POLE_VAULTING_ZOMBIE, c.BUCKETHEAD_ZOMBIE,),
    c.NUM_FLAGS:2,
    c.CARD_POOL: {  c.WALLNUTBOWLING: 300,
                    c.REDWALLNUTBOWLING: 100,}
},
# 第2关 白天 大决战
{
    c.BACKGROUND_TYPE: 0,
    c.GAME_TITLE: "大决战（白天）",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_MOVE,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.POLE_VAULTING_ZOMBIE, c.BUCKETHEAD_ZOMBIE,),
    c.NUM_FLAGS:3,
    c.CARD_POOL: {  c.PEASHOOTER: 200,
                    c.SNOWPEASHOOTER: 100,
                    c.WALLNUT: 100,
                    c.CHERRYBOMB: 100,
                    c.REPEATERPEA: 200,
                    c.CHOMPER: 100,
                    c.POTATOMINE: 100,}
},
# 第3关 夜晚 大决战
{
    c.BACKGROUND_TYPE: 1,
    c.GAME_TITLE: "大决战（黑夜）",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_MOVE,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.FOOTBALL_ZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.NEWSPAPER_ZOMBIE, c.SCREEN_DOOR_ZOMBIE),
    c.NUM_FLAGS:3,
    c.CARD_POOL: {  c.PUFFSHROOM: 100,
                    c.SCAREDYSHROOM: 100,
                    c.ICESHROOM: 70,
                    c.HYPNOSHROOM: 100,
                    c.DOOMSHROOM: 50,
                    c.GRAVEBUSTER: 100,
                    c.FUMESHROOM: 200},
    c.GRADE_GRAVES:3
},
# 第4关 泳池 大决战
{
    c.BACKGROUND_TYPE: 2,
    c.GAME_TITLE: "大决战（泳池）",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_MOVE,
    c.SHOVEL: 1,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.SNORKELZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.ZOMBONI,),
    c.NUM_FLAGS:4,
    c.CARD_POOL: {  c.LILYPAD: 300,
                    c.TORCHWOOD: 100,
                    c.TALLNUT: 100,
                    c.TANGLEKLEP: 100,
                    c.SPIKEWEED: 100,
                    c.SQUASH: 100,
                    c.JALAPENO: 50,
                    c.THREEPEASHOOTER: 400,}
},
# 第5关 坚果保龄球2
{
    c.BACKGROUND_TYPE: 6,
    c.GAME_TITLE: "坚果保龄球(II)",
    c.CHOOSEBAR_TYPE: c.CHOOSEBAR_BOWLING,
    c.SHOVEL: 0,
    c.SPAWN_ZOMBIES:c.SPAWN_ZOMBIES_AUTO,
    c.INCLUDED_ZOMBIES: (   c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE,
                            c.POLE_VAULTING_ZOMBIE, c.BUCKETHEAD_ZOMBIE,
                            c.NEWSPAPER_ZOMBIE, c.SCREEN_DOOR_ZOMBIE),
    c.NUM_FLAGS:3,
    c.CARD_POOL: {  c.WALLNUTBOWLING: 500,
                    c.REDWALLNUTBOWLING: 100,
                    c.GIANTWALLNUT:100,}
},
)

# 总关卡数
TOTAL_LEVEL = len(LEVEL_MAP_DATA)
TOTAL_LITTLE_GAME = len(LITTLE_GAME_MAP_DATA)
