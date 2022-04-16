import random
import pygame as pg
from .. import tool
from .. import constants as c

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 要把记录信息改成元组的话这里又得改
        # 而且不同场地还不一样
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def isValid(self, map_x, map_y):
        if (map_x < 0 or map_x >= self.width or
            map_y < 0 or map_y >= self.height):
            return False
        return True
    
    # 判断能否种植
    def isMovable(self, map_x, map_y):
        # 目前没有南瓜头，所以用是否为空判断
        # 可将南瓜头新定义一个状态（如：2），基于此进一步判断
        # 应当改成元组，保存南瓜头、花盆、睡莲等状态
        # 当然，不用元组的话字符串也行，但是得把判断植物写在母函数中，并且需要更多参数
        # 这样返回的就是一个具体信息，而非bool值了
        # 到时候还要改一下变量名，还叫isMovable不合适
        return (self.map[map_y][map_x] == c.MAP_EMPTY)
    
    def getMapIndex(self, x, y):
        x -= c.MAP_OFFSET_X
        y -= c.MAP_OFFSET_Y
        return (x // c.GRID_X_SIZE, y // c.GRID_Y_SIZE)
    
    def getMapGridPos(self, map_x, map_y):
        return (map_x * c.GRID_X_SIZE + c.GRID_X_SIZE//2 + c.MAP_OFFSET_X,
                map_y * c.GRID_Y_SIZE + c.GRID_Y_SIZE//5 * 3 + c.MAP_OFFSET_Y)
    
    def setMapGridType(self, map_x, map_y, type):
        self.map[map_y][map_x] = type

    def getRandomMapIndex(self):
        map_x = random.randint(0, self.width-1)
        map_y = random.randint(0, self.height-1)
        return (map_x, map_y)

    def showPlant(self, x, y):
        pos = None
        map_x, map_y = self.getMapIndex(x, y)
        if self.isValid(map_x, map_y) and self.isMovable(map_x, map_y):
            pos = self.getMapGridPos(map_x, map_y)
        return pos
