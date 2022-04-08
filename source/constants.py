__author__ = 'wszqkzqk'
START_LEVEL_NUM = 1
START_LITTLE_GAME_NUM = 1

ORIGINAL_CAPTION = 'pypvz'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GRID_X_LEN = 9
GRID_Y_LEN = 5
GRID_X_SIZE = 80
GRID_Y_SIZE = 100


WHITE        = (255, 255, 255)
NAVYBLUE     = ( 60,  60, 100)
SKY_BLUE     = ( 39, 145, 251)
BLACK        = (  0,   0,   0)
LIGHTYELLOW  = (234, 233, 171)
RED          = (255,   0,   0)
PURPLE       = (255,   0, 255)
GOLD         = (255, 215,   0)
GREEN        = (  0, 255,   0)

SIZE_MULTIPLIER = 1.3

# 退出游戏按钮
EXIT = 'exit'
# 当想要一个特殊值时用
NULL = 'null'
# 游戏界面可选的菜单
LITTLE_MENU = 'littleMenu'
BIG_MENU = 'bigMenu'
RETURN_BUTTON = 'returnButton'
RESTART_BUTTON = 'restartButton'
MAINMENU_BUTTON = 'mainMenuButton'
LITTLEGAME_BUTTON = 'littleGameButton'
# 小铲子
SHOVEL = 'shovel'
SHOVEL_BOX = 'shovelBox'


#GAME INFO DICTIONARY KEYS
CURRENT_TIME = 'current time'
LEVEL_NUM = 'level num'

#STATES FOR ENTIRE GAME
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'load screen'
GAME_LOSE = 'game los'
GAME_VICTORY = 'game victory'
LEVEL = 'level'

MAIN_MENU_IMAGE = 'MainMenu'
OPTION_ADVENTURE = 'Adventure'
GAME_LOOSE_IMAGE = 'GameLoose'
GAME_VICTORY_IMAGE = 'GameVictory'

#MAP COMPONENTS
BACKGROUND_NAME = 'Background'
BACKGROUND_TYPE = 'background_type'
INIT_SUN_NAME = 'init_sun_value'
ZOMBIE_LIST = 'zombie_list'

MAP_EMPTY = 0
MAP_EXIST = 1
# 只有南瓜头
MAP_PUMPKIN_ONLY = 2
# 有南瓜头和其他植物
MAP_PUMPKIN_WITH = 3
# 可能还需要给咖啡豆定义一个状态

BACKGROUND_OFFSET_X = 220
MAP_OFFSET_X = 35
MAP_OFFSET_Y = 100

#MENUBAR
CHOOSEBAR_TYPE = 'choosebar_type'
CHOOSEBAR_STATIC = 0
CHOOSEBAR_MOVE = 1
CHOSSEBAR_BOWLING = 2
MENUBAR_BACKGROUND = 'ChooserBackground'
MOVEBAR_BACKGROUND = 'MoveBackground'
PANEL_BACKGROUND = 'PanelBackground'
START_BUTTON = 'StartButton'
CARD_POOL = 'card_pool'

MOVEBAR_CARD_FRESH_TIME = 6000
CARD_MOVE_TIME = 60

#PLANT INFO
PLANT_IMAGE_RECT = 'plant_image_rect'
CAR = 'car'
SUN = 'Sun'
SUNFLOWER = 'SunFlower'
PEASHOOTER = 'Peashooter'
SNOWPEASHOOTER = 'SnowPea'
WALLNUT = 'WallNut'
CHERRYBOMB = 'CherryBomb'
THREEPEASHOOTER = 'Threepeater'
REPEATERPEA = 'RepeaterPea'
CHOMPER = 'Chomper'
CHERRY_BOOM_IMAGE = 'Boom'
PUFFSHROOM = 'PuffShroom'
POTATOMINE = 'PotatoMine'
SQUASH = 'Squash'
SPIKEWEED = 'Spikeweed'
JALAPENO = 'Jalapeno'
SCAREDYSHROOM = 'ScaredyShroom'
SUNSHROOM = 'SunShroom'
ICESHROOM = 'IceShroom'
HYPNOSHROOM = 'HypnoShroom'
WALLNUTBOWLING = 'WallNutBowling'
REDWALLNUTBOWLING = 'RedWallNutBowling'

PLANT_HEALTH = 300
WALLNUT_HEALTH = 4000
WALLNUT_CRACKED1_HEALTH = 4000//3 * 2
WALLNUT_CRACKED2_HEALTH = 4000//3
WALLNUT_BOWLING_DAMAGE = 370

PRODUCE_SUN_INTERVAL = 7000
FLOWER_SUN_INTERVAL = 24000
SUN_LIVE_TIME = 10000
SUN_VALUE = 25

ICE_SLOW_TIME = 10000

FREEZE_TIME = 7500
ICETRAP = 'IceTrap'

#PLANT CARD INFO
CARD_SUNFLOWER = 'card_sunflower'
CARD_PEASHOOTER = 'card_peashooter'
CARD_SNOWPEASHOOTER = 'card_snowpea'
CARD_WALLNUT = 'card_wallnut'
CARD_CHERRYBOMB = 'card_cherrybomb'
CARD_THREEPEASHOOTER = 'card_threepeashooter'
CARD_REPEATERPEA = 'card_repeaterpea'
CARD_CHOMPER = 'card_chomper'
CARD_PUFFSHROOM = 'card_puffshroom'
CARD_POTATOMINE = 'card_potatomine'
CARD_SQUASH = 'card_squash'
CARD_SPIKEWEED = 'card_spikeweed'
CARD_JALAPENO = 'card_jalapeno'
CARD_SCAREDYSHROOM = 'card_scaredyshroom'
CARD_SUNSHROOM = 'card_sunshroom'
CARD_ICESHROOM = 'card_iceshroom'
CARD_HYPNOSHROOM = 'card_hypnoshroom'
CARD_REDWALLNUT = 'card_redwallnut'

#BULLET INFO
BULLET_PEA = 'PeaNormal'
BULLET_PEA_ICE = 'PeaIce'
BULLET_MUSHROOM = 'BulletMushRoom'
BULLET_DAMAGE_NORMAL = 20

#ZOMBIE INFO
ZOMBIE_IMAGE_RECT = 'zombie_image_rect'
ZOMBIE_HEAD = 'ZombieHead'
NORMAL_ZOMBIE = 'Zombie'
CONEHEAD_ZOMBIE = 'ConeheadZombie'
BUCKETHEAD_ZOMBIE = 'BucketheadZombie'
FLAG_ZOMBIE = 'FlagZombie'
NEWSPAPER_ZOMBIE = 'NewspaperZombie'
BOOMDIE = 'BoomDie'

# 僵尸生命值设置
LOSTHEAD_HEALTH = 70
NORMAL_HEALTH = 200 # 普通僵尸生命值

FLAG_HEALTH = 50
CONEHEAD_HEALTH = 370
BUCKETHEAD_HEALTH = 1100
NEWSPAPER_HEALTH = 200

ATTACK_INTERVAL = 500
ZOMBIE_WALK_INTERVAL = 60  # 僵尸步行间隔

ZOMBIE_START_X = SCREEN_WIDTH + 50

#STATE
IDLE = 'idle'
FLY = 'fly'
EXPLODE = 'explode'
ATTACK = 'attack'
ATTACKED = 'attacked'
DIGEST = 'digest'
WALK = 'walk'
DIE = 'die'
CRY = 'cry'
FREEZE = 'freeze'
SLEEP = 'sleep'

#LEVEL STATE
CHOOSE = 'choose'
PLAY = 'play'

#BACKGROUND
BACKGROUND_DAY = 0
BACKGROUND_NIGHT = 1