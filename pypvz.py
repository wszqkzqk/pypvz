#!/usr/bin/env python
import logging
import traceback
import os
import pygame as pg
from logging.handlers import RotatingFileHandler
# 由于在后续本地模块中存在对pygame的调用，在此处必须完成pygame的初始化
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"]="0" # 设置临时环境变量以避免Linux下禁用x11合成器
pg.init()

from source import tool
from source import constants as c
from source.state import mainmenu, screen, level

if __name__ == "__main__":
    # 日志设置
    if not os.path.exists(os.path.dirname(c.USERLOG_PATH)):
        os.makedirs(os.path.dirname(c.USERLOG_PATH))
    logger = logging.getLogger("main")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    fileHandler = RotatingFileHandler(c.USERLOG_PATH, "a", 1_000_000, 0, "utf-8")
    # 设置日志文件权限，Unix为644，Windows为可读写；Python的os.chmod与Unix chmod相同，但要显式说明8进制
    os.chmod(c.USERLOG_PATH, 0o644)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    try:
        # 控制状态机运行
        game = tool.Control()
        state_dict = {  c.MAIN_MENU:    mainmenu.Menu(),
                        c.GAME_VICTORY: screen.GameVictoryScreen(),
                        c.GAME_LOSE:    screen.GameLoseScreen(),
                        c.LEVEL:        level.Level(),
                        c.AWARD_SCREEN: screen.AwardScreen(),
                        c.HELP_SCREEN:  screen.HelpScreen(),
                        }
        game.setup_states(state_dict, c.MAIN_MENU)
        game.run()
    except:
        print() # 将日志输出与上文内容分隔开，增加可读性
        logger.error(f"\n{traceback.format_exc()}") 
