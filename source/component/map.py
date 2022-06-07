import random
import pygame as pg
from .. import tool
from .. import constants as c

class Map():
    def __init__(self, background_type):
        self.background_type = background_type
        # 注意：从0开始编号
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            self.width = c.GRID_POOL_X_LEN
            self.height = c.GRID_POOL_Y_LEN
            self.gridHeightSize = c.GRID_POOL_Y_SIZE
            self.map = [[(c.MAP_STATE_EMPTY(), c.MAP_STATE_WATER())[y in {2, 3}] for x in range(self.width)] for y in range(self.height)]
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            self.width = c.GRID_ROOF_X_LEN
            self.height = c.GRID_ROOF_Y_LEN
            self.gridHeightSize = c.GRID_ROOF_Y_SIZE
            self.map = [[c.MAP_STATE_TILE() for x in range(self.width)] for y in range(self.height)]
        elif self.background_type == c.BACKGROUND_SINGLE:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.gridHeightSize = c.GRID_Y_SIZE
            self.map = [[(c.MAP_STATE_UNAVAILABLE(), c.MAP_STATE_EMPTY())[y == 2] for x in range(self.width)] for y in range(self.height)]
        elif self.background_type == c.BACKGROUND_TRIPLE:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.gridHeightSize = c.GRID_Y_SIZE
            self.map = [[(c.MAP_STATE_UNAVAILABLE(), c.MAP_STATE_EMPTY())[y in {1, 2, 3}] for x in range(self.width)] for y in range(self.height)]
        else:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.gridHeightSize = c.GRID_Y_SIZE
            self.map = [[c.MAP_STATE_EMPTY() for x in range(self.width)] for y in range(self.height)]

    def isValid(self, map_x, map_y):
        if (map_x < 0 or map_x >= self.width or
            map_y < 0 or map_y >= self.height):
            return False
        return True

    # 判断位置是否可用
    # 暂时没有写紫卡植物的判断方法
    # 由于紫卡植物需要移除以前的植物，所以可用另外定义一个函数
    def isAvailable(self, map_x, map_y, plantName):
        # 咖啡豆和墓碑吞噬者的判别最为特殊
        if plantName == c.COFFEEBEAN:
            if self.map[map_y][map_x][c.MAP_SLEEP] and (plantName not in self.map[map_y][map_x][c.MAP_PLANT]):
                return True
            else:
                return False
        if plantName == c.GRAVEBUSTER:
            if (c.GRAVE in self.map[map_y][map_x][c.MAP_PLANT]):
                return True
            else:
                return False
        # 被非植物障碍占据的格子对于一般植物不可种植
        if any((i in c.NON_PLANT_OBJECTS) for i in self.map[map_y][map_x][c.MAP_PLANT]):
            return False
        if self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_GRASS:  # 草地
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plantName not in c.WATER_PLANTS:
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 没有植物肯定可以种植
                    return True
                elif (all((i in {'花盆（未实现）', '南瓜头（未实现）'}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植；判断方法：并集
                    return True
                else:
                    return False
            else:
                return False
        elif self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_TILE: # 屋顶
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plantName not in c.WATER_PLANTS:
                if '花盆（未实现）' in self.map[map_y][map_x][c.MAP_PLANT]:
                    if (all((i in {'花盆（未实现）', '南瓜头（未实现）'}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                    and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植；判断方法：并集
                        if plantName in {c.SPIKEWEED}: # 不能在花盆上种植的植物
                            return False
                        else:
                            return True
                elif plantName == '花盆（未实现）': # 这一格本来没有花盆而且新来的植物是花盆，可以种
                    return True
                else:
                    return False
            else:
                return False
        elif self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_WATER:   # 水里
            if plantName in c.WATER_PLANTS:   # 是水生植物
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 只有无植物时才能在水里种植水生植物
                    return True
                else:
                    return False
            else:   # 非水生植物，依赖睡莲
                if c.LILYPAD in self.map[map_y][map_x][c.MAP_PLANT]:
                    if (all((i in {c.LILYPAD, '南瓜头（未实现）'}) for i in self.map[map_y][map_x][c.MAP_PLANT])
                    and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])):
                        if plantName in {c.SPIKEWEED, c.POTATOMINE, '花盆（未实现）'}: # 不能在睡莲上种植的植物
                            return False
                        else:
                            return True
                    else:
                        return False
                else:
                    return False
        else:   # 不可种植区域
            return False
    
    def getMapIndex(self, x, y):
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            x -= c.MAP_POOL_OFFSET_X
            y -= c.MAP_POOL_OFFSET_Y
            return (x // c.GRID_POOL_X_SIZE, y // c.GRID_POOL_Y_SIZE)
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            x -= c.MAP_ROOF_OFFSET_X
            y -= c.MAP_ROOF_OFFSET_X
            gridX = x // c.GRID_ROOF_X_SIZE
            if gridX >= 5:
                gridY = y // c.GRID_ROOF_Y_SIZE
            else:
                gridY = (y - 20*(6 - gridX)) // 85
            return (gridX, gridY)
        else:
            x -= c.MAP_OFFSET_X
            y -= c.MAP_OFFSET_Y
            return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)
    
    def getMapGridPos(self, map_x, map_y):
        if self.background_type in c.POOL_EQUIPPED_BACKGROUNDS:
            return (map_x * c.GRID_POOL_X_SIZE + c.GRID_POOL_X_SIZE//2 + c.MAP_POOL_OFFSET_X,
                    map_y * c.GRID_POOL_Y_SIZE + c.GRID_POOL_Y_SIZE//5 * 3 + c.MAP_POOL_OFFSET_Y)
        elif self.background_type in c.ON_ROOF_BACKGROUNDS:
            return (map_x * c.GRID_ROOF_X_SIZE + c.GRID_ROOF_X_SIZE//2 + c.MAP_ROOF_OFFSET_X,
                    map_y * c.GRID_ROOF_Y_SIZE + 20 * max(0, (6 - map_y)) + c.GRID_ROOF_Y_SIZE//5 * 3 + c.MAP_POOL_OFFSET_Y)
        else:
            return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X,
                    map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)
    
    def setMapGridType(self, map_x, map_y, plot_type):
        self.map[map_y][map_x][c.MAP_PLOT_TYPE] = plot_type

    def addMapPlant(self, map_x, map_y, plantName, sleep=False):
        self.map[map_y][map_x][c.MAP_PLANT].add(plantName)
        self.map[map_y][map_x][c.MAP_SLEEP] = sleep
    
    def removeMapPlant(self, map_x, map_y, plantName):
        self.map[map_y][map_x][c.MAP_PLANT].discard(plantName)

    def getRandomMapIndex(self):
        map_x = random.randint(0, self.width-1)
        map_y = random.randint(0, self.height-1)
        return (map_x, map_y)

    def checkPlantToSeed(self, x, y, plantName):
        pos = None
        map_x, map_y = self.getMapIndex(x, y)
        if self.isValid(map_x, map_y) and self.isAvailable(map_x, map_y, plantName):
            pos = self.getMapGridPos(map_x, map_y)
        return pos
