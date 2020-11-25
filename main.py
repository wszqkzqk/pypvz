import pygame as pg
from source import tool
from source import constants as c
from source.state import mainmenu, screen, level

if __name__=='__main__':
    # 控制状态机运行
    game = tool.Control()
    state_dict = {c.MAIN_MENU: mainmenu.Menu(),
                  c.GAME_VICTORY: screen.GameVictoryScreen(),
                  c.GAME_LOSE: screen.GameLoseScreen(),
                  c.LEVEL: level.Level()}
    game.setup_states(state_dict, c.MAIN_MENU)
    game.run()