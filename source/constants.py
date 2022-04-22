START_LEVEL_NUM = 1
START_LITTLE_GAME_NUM = 1

ORIGINAL_CAPTION = 'pypvz'

# 游戏模式
MODE_ADVENTURE = 'adventure'
MODE_LITTLEGAME = 'littleGame'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# 一般
GRID_X_LEN = 9
GRID_Y_LEN = 5
GRID_X_SIZE = 80
GRID_Y_SIZE = 100
# 带有泳池
GRID_POOL_X_LEN = GRID_X_LEN
GRID_POOL_Y_LEN = 6
GRID_POOL_X_SIZE = GRID_X_SIZE
GRID_POOL_Y_SIZE = 85
# 屋顶
GRID_ROOF_X_LEN = GRID_X_LEN
GRID_ROOF_Y_LEN = GRID_Y_LEN
GRID_ROOF_X_SIZE = GRID_X_SIZE
GRID_ROOF_Y_SIZE = 85

# 游戏速度倍率（调试用）
GAME_RATE = 1

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
LITTLEGAME_NUM = 'littleGame num'

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

#BACKGROUND
BACKGROUND_DAY = 0
BACKGROUND_NIGHT = 1
BACKGROUND_POOL = 2
BACKGROUND_FOG = 3
BACKGROUND_ROOF = 4
BACKGROUND_ROOFNIGHT = 5
BACKGROUND_WALLNUTBOWLING = 6
BACKGROUND_SINGLE = 7
BACKGROUND_TRIPLE = 8

MAP_PLANT = 'plantnames'
MAP_SLEEP = 'sleep' # 有没有休眠的蘑菇，作是否能种植咖啡豆的判断
MAP_PLOT_TYPE = 'plotType'
MAP_GRASS = 'grass'
MAP_WATER = 'water'
MAP_TILE = 'tile'  # 指屋顶上的瓦片
MAP_DAMAGED = 'damaged'
MAP_STATE_EMPTY = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_GRASS}  # 由于同一格显然不可能种两个相同的植物，所以用集合
MAP_STATE_WATER = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_WATER}
MAP_STATE_TILE = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_TILE}

BACKGROUND_OFFSET_X = 220
MAP_OFFSET_X = 35
MAP_OFFSET_Y = 100
MAP_POOL_OFFSET_X = 42  # 暂时还不清楚数据
MAP_POOL_OFFSET_Y = 115 # 暂时还不清楚数据
MAP_ROOF_OFFSET_X = 35  # 暂时还不清楚数据
MAP_ROOF_OFFSET_Y = 105 # 暂时还不清楚数据

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
LILYPAD = 'LilyPad'
TORCHWOOD = 'TorchWood'

PLANT_HEALTH = 300
WALLNUT_HEALTH = 4000
WALLNUT_CRACKED1_HEALTH = 4000//3 * 2
WALLNUT_CRACKED2_HEALTH = 4000//3
WALLNUT_BOWLING_DAMAGE = 550

PRODUCE_SUN_INTERVAL = 4250 # 基准
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
CARD_LILYPAD = 'card_lilypad'
CARD_TORCHWOOD = 'card_torchwood'

#BULLET INFO
# 子弹类型
BULLET_PEA = 'PeaNormal'
BULLET_PEA_ICE = 'PeaIce'
BULLET_FIREBALL = 'Fireball'
BULLET_MUSHROOM = 'BulletMushRoom'
# 子弹伤害
BULLET_DAMAGE_NORMAL = 20
BULLET_DAMAGE_FIREBALL_BODY = 27 # 这是火球本体的伤害，注意不是40，本体(27) + 溅射(13)才是40
BULLET_DAMAGE_FIREBALL_RANGE = 13
# 子弹效果
BULLET_EFFECT_ICE = 'ice'
BULLET_EFFECT_UNICE = 'unice'

#ZOMBIE INFO
ZOMBIE_IMAGE_RECT = 'zombie_image_rect'
ZOMBIE_HEAD = 'ZombieHead'
NORMAL_ZOMBIE = 'Zombie'
CONEHEAD_ZOMBIE = 'ConeheadZombie'
BUCKETHEAD_ZOMBIE = 'BucketheadZombie'
FLAG_ZOMBIE = 'FlagZombie'
NEWSPAPER_ZOMBIE = 'NewspaperZombie'
BOOMDIE = 'BoomDie'

# 对僵尸的攻击类型设置
ZOMBIE_DEAFULT_DAMAGE = 'helmet2First'
ZOMBIE_HELMET_2_FIRST = 'helmet2First'  # 优先攻击二类防具
ZOMBIE_COMMON_DAMAGE = 'commonDamage'   # 优先攻击僵尸与一类防具的整体
ZOMBIE_RANGE_DAMAGE = 'rangeDamage' # 范围攻击，同时伤害二类防具与(僵尸与一类防具的整体)
ZOMBIE_ASH_DAMAGE = 'ashDamage' # 灰烬植物攻击，直接伤害本体
ZOMBIE_WALLNUT_BOWLING_DANMAGE = 'wallnutBowlingDamage' # 坚果保龄球冲撞伤害

# 僵尸生命值设置
LOSTHEAD_HEALTH = 70
NORMAL_HEALTH = 200 # 普通僵尸生命值

CONEHEAD_HEALTH = 370
BUCKETHEAD_HEALTH = 1100
NEWSPAPER_HEALTH = 150

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
