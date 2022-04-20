import random
import pygame as pg
from .. import tool
from .. import constants as c
from copy import deepcopy

class Map():
    def __init__(self, background_type):
        self.background_type = background_type
        if self.background_type in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
            self.width = c.GRID_POOL_X_LEN
            self.height = c.GRID_POOL_Y_LEN
            self.map = [[(deepcopy(c.MAP_STATE_EMPTY), deepcopy(c.MAP_STATE_WATER))[y in {2, 3}] for x in range(self.width)] for y in range(self.height)]
        elif self.background_type in {c.BACKGROUND_ROOF, c.BACKGROUND_ROOFNIGHT}:
            self.width = c.GRID_ROOF_X_LEN
            self.height = c.GRID_ROOF_Y_LEN
            self.map = [[deepcopy(c.MAP_STATE_TILE) for x in range(self.width)] for y in range(self.height)]
        else:
            self.width = c.GRID_X_LEN
            self.height = c.GRID_Y_LEN
            self.map = [[deepcopy(c.MAP_STATE_EMPTY) for x in range(self.width)] for y in range(self.height)]

    def isValid(self, map_x, map_y):
        if (map_x < 0 or map_x >= self.width or
            map_y < 0 or map_y >= self.height):
            return False
        return True
    
    # 判断位置是否可用
    # 暂时没有写紫卡植物的判断方法
    # 由于紫卡植物需要移除以前的植物，所以可用另外定义一个函数
    # 注意咖啡豆生效后需要同时将植物的睡眠状态和格子的睡眠记录改变
    def isAvailable(self, map_x, map_y, plantName):
        if self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_GRASS:  # 草地
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plantName not in {c.LILYPAD, '海蘑菇（未实现）', '缠绕水草（未实现）'}: # 这里的集合也可以换成存储在某一文件中的常数的表达
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 没有植物肯定可以种植
                    return True
                elif ((self.map[map_y][map_x][c.MAP_PLANT] | {'花盆（未实现）', '南瓜头（未实现）'} == {'花盆（未实现）', '南瓜头（未实现）'})
                    and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植；判断方法：并集
                    return True
                elif plantName == '咖啡豆（未实现）' and self.map[map_y][map_x][c.MAP_SLEEP]:
                    return True
                else:
                    return False
            else:
                return False
        elif self.map[map_y][map_x][c.MAP_PLOT_TYPE] == c.MAP_TILE: # 屋顶
            # 首先需要判断植物是否是水生植物，水生植物不能种植在陆地上
            if plantName not in {c.LILYPAD, '海蘑菇（未实现）', '缠绕水草（未实现）'}: # 这里的集合也可以换成存储在某一文件中的常数的表达
                if '花盆（未实现）' in self.map[map_y][map_x][c.MAP_PLANT]:
                    if ((self.map[map_y][map_x][c.MAP_PLANT] | {'花盆（未实现）', '南瓜头（未实现）'} == {'花盆（未实现）', '南瓜头（未实现）'})
                        and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植；判断方法：并集
                        return True
                elif plantName == '花盆（未实现）': # 这一格本来没有花盆而且新来的植物是花盆，可以种
                    return True
                elif plantName == '咖啡豆（未实现）' and self.map[map_y][map_x][c.MAP_SLEEP]:
                    return True
                else:
                    return False
            else:
                return False
        else:   # 水里
            if plantName in {c.LILYPAD, '海蘑菇（未实现）', '缠绕水草（未实现）'}:   # 是水生植物
                if not self.map[map_y][map_x][c.MAP_PLANT]: # 只有无植物时才能在水里种植水生植物
                    return True
                else:
                    return False
            else:   # 非水生植物，依赖睡莲
                if c.LILYPAD in self.map[map_y][map_x][c.MAP_PLANT]:
                    if ((self.map[map_y][map_x][c.MAP_PLANT] | {c.LILYPAD, '花盆（未实现）', '南瓜头（未实现）'} == {c.LILYPAD, '花盆（未实现）', '南瓜头（未实现）'})
                        and (plantName not in self.map[map_y][map_x][c.MAP_PLANT])): # 例外植物：集合中填花盆和南瓜头，只要这里没有这种植物就能种植；判断方法：并集
                        return True
                    else:
                        return False
                else:
                    return False
    
    def getMapIndex(self, x, y):
        # 引入新地图后需要增加这里的内容
        if self.background_type in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
            x -= c.MAP_POOL_OFFSET_X
            y -= c.MAP_POOL_OFFSET_Y
            return (x // c.GIRD_POOL_X_SIZE, y // c.GRID_POOL_Y_SIZE)
        elif self.background_type in {c.BACKGROUND_ROOF, c.BACKGROUND_ROOFNIGHT}:
            x -= c.MAP_ROOF_OFFSET_X
            y -= c.MAP_ROOF_OFFSET_X
            girdX = x // c.GRID_ROOF_X_SIZE
            if girdX >= 5:
                gridY = y // c.GRID_ROOF_Y_SIZE
            else:
                gridY = (y - 20*(6 - girdX)) // 85
            return (girdX, gridY)
        else:
            x -= c.MAP_OFFSET_X
            y -= c.MAP_OFFSET_Y
            return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)
    
    def getMapGridPos(self, map_x, map_y):
        if self.background_type in {c.BACKGROUND_POOL, c.BACKGROUND_FOG}:
            return (map_x * c.GRID_ROOF_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_ROOF_OFFSET_X,
                    map_y * c.GRID_ROOF_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_ROOF_OFFSET_Y)
        elif self.background_type in {c.BACKGROUND_ROOF, c.BACKGROUND_ROOFNIGHT}:
            return (map_x * c.GRID_POOL_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_POOL_OFFSET_X,
                    map_y * c.GRID_POOL_Y_SIZE + 20 * max(0, (6 - map_y)) + c.GRID_Y_SIZE//5 * 3 + c.MAP_POOL_OFFSET_Y)
        else:
            return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X,
                    map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)
    
    def setMapGridType(self, map_x, map_y, type):
        self.map[map_y][map_x] = type

    def addMapPlant(self, map_x, map_y, plantName, sleep=False):
        self.map[map_y][map_x][c.MAP_PLANT].add(plantName)
        self.map[map_y][map_x][c.MAP_SLEEP] = sleep
    
    def removeMapPlant(self, map_x, map_y, plantName):
        self.map[map_y][map_x][c.MAP_PLANT].remove(plantName)

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
