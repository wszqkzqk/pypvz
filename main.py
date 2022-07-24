#!/usr/bin/env python
import pygame as pg
import sys
import os
from source import tool
from source import constants as c
from source.state import mainmenu, screen, level

if __name__=='__main__':
    # 控制状态机运行
    if not os.path.exists(os.path.dirname(c.USERLOG_PATH)):
                os.makedirs(os.path.dirname(c.USERLOG_PATH))
    sys.stderr = open(c.USERLOG_PATH, "w")
    game = tool.Control()
    state_dict = {  c.MAIN_MENU:    mainmenu.Menu(),
                    c.GAME_VICTORY: screen.GameVictoryScreen(),
                    c.GAME_LOSE:    screen.GameLoseScreen(),
                    c.LEVEL:        level.Level()
                    }
    game.setup_states(state_dict, c.MAIN_MENU)
    game.run()

