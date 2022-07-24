#!/usr/bin/env python
import pygame as pg
import logging
import traceback
import os
from logging.handlers import RotatingFileHandler
from source import tool
from source import constants as c
from source.state import mainmenu, screen, level

if __name__=='__main__':
    # 日志设置
    if not os.path.exists(os.path.dirname(c.USERLOG_PATH)):
        os.makedirs(os.path.dirname(c.USERLOG_PATH))
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler = RotatingFileHandler(c.USERLOG_PATH, "a", 1024*1024, 0, "utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    try:
        # 控制状态机运行
        game = tool.Control()
        state_dict = {  c.MAIN_MENU:    mainmenu.Menu(),
                        c.GAME_VICTORY: screen.GameVictoryScreen(),
                        c.GAME_LOSE:    screen.GameLoseScreen(),
                        c.LEVEL:        level.Level()
                        }
        game.setup_states(state_dict, c.MAIN_MENU)
        game.run()
    except:
        logger.error(f'\n{traceback.format_exc()}') 
