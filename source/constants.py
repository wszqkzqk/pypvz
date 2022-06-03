# 冒险模式起始关卡
START_LEVEL_NUM = 1
# 小游戏模式起始关卡
START_LITTLE_GAME_NUM = 1

# 游戏速度倍率（调试用）
GAME_RATE = 1

# 窗口标题
ORIGINAL_CAPTION = 'pypvz'
# 窗口图标
ORIGINAL_LOGO = "pypvz-exec-logo.png"

# 游戏模式
GAME_MODE = 'mode'
MODE_ADVENTURE = 'adventure'
MODE_LITTLEGAME = 'littleGame'

# 窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# 选卡数量
# 最大数量
CARD_MAX_NUM = 10   # 这里以后可以增加解锁功能，从最初的6格逐渐解锁到10格
# 最小数量
CARD_LIST_NUM = CARD_MAX_NUM

# 方格数据
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

# 颜色
WHITE        = (255, 255, 255)
NAVYBLUE     = ( 60,  60, 100)
SKY_BLUE     = ( 39, 145, 251)
BLACK        = (  0,   0,   0)
LIGHTYELLOW  = (234, 233, 171)
RED          = (255,   0,   0)
PURPLE       = (255,   0, 255)
GOLD         = (255, 215,   0)
GREEN        = (  0, 255,   0)

# 退出游戏按钮
EXIT = 'exit'
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
# 一大波僵尸来袭图片
HUGE_WAVE_APPROCHING = 'Approching'
# 关卡进程图片
LEVEL_PROGRESS_BAR = 'LevelProgressBar'
LEVEL_PROGRESS_ZOMBIE_HEAD = 'LevelProgressZombieHead'
LEVEL_PROGRESS_FLAG = 'LevelProgressFlag'


# GAME INFO字典键值
CURRENT_TIME = 'current time'
LEVEL_NUM = 'level num'
LITTLEGAME_NUM = 'littleGame num'

# 整个游戏的状态
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'load screen'
GAME_LOSE = 'game los'
GAME_VICTORY = 'game victory'
LEVEL = 'level'

# 界面图片文件名
MAIN_MENU_IMAGE = 'MainMenu'
OPTION_ADVENTURE = 'Adventure'
GAME_LOSE_IMAGE = 'GameLose'
GAME_VICTORY_IMAGE = 'GameVictory'

# 地图相关内容
BACKGROUND_NAME = 'Background'
BACKGROUND_TYPE = 'background_type'
INIT_SUN_NAME = 'init_sun_value'
ZOMBIE_LIST = 'zombie_list'

# 地图类型
BACKGROUND_DAY = 0
BACKGROUND_NIGHT = 1
BACKGROUND_POOL = 2
BACKGROUND_FOG = 3
BACKGROUND_ROOF = 4
BACKGROUND_ROOFNIGHT = 5
BACKGROUND_WALLNUTBOWLING = 6
BACKGROUND_SINGLE = 7
BACKGROUND_TRIPLE = 8

# 地图类型集合
# 白天场地（泛指蘑菇睡觉的场地）
DAYTIME_BACKGROUNDS = {
                BACKGROUND_DAY, BACKGROUND_POOL,
                BACKGROUND_ROOF, BACKGROUND_WALLNUTBOWLING,
                BACKGROUND_SINGLE, BACKGROUND_TRIPLE,
                }

# 带有泳池的场地
POOL_EQUIPPED_BACKGROUNDS = {
                BACKGROUND_POOL, BACKGROUND_FOG,
                }

# 屋顶上的场地
ON_ROOF_BACKGROUNDS = {
                BACKGROUND_ROOF, BACKGROUND_ROOFNIGHT,
                }

# BACKGROUND_DAY场地的变体
BACKGROUND_DAY_LIKE_BACKGROUNDS = {
                BACKGROUND_DAY, BACKGROUND_SINGLE,
                BACKGROUND_TRIPLE,
                }

# 夜晚地图的墓碑数量等级
GRADE_GRAVES = 'grade_graves'
# 不同墓碑等级对应的信息
GRAVES_GRADE_INFO = (0, 4, 7, 11)

# 僵尸生成方式
SPAWN_ZOMBIES = 'spawn_zombies'
SPAWN_ZOMBIES_AUTO = 'auto'
SPAWN_ZOMBIES_LIST = 'list'
INCLUDED_ZOMBIES = 'included_zombies'
NUM_FLAGS = 'num_flags'
INEVITABLE_ZOMBIE_DICT = 'inevitable_zombie_list'
SURVIVAL_ROUNDS = 'survival_rounds'

# 地图单元格属性
MAP_PLANT = 'plantnames'
MAP_SLEEP = 'sleep' # 有没有休眠的蘑菇，作是否能种植咖啡豆的判断
MAP_PLOT_TYPE = 'plotType'
# 地图单元格区域类型
MAP_GRASS = 'grass'
MAP_WATER = 'water'
MAP_TILE = 'tile'  # 指屋顶上的瓦片
MAP_UNAVAILABLE = 'unavailable' # 指完全不能种植物的地方，包括无草皮的荒地和坚果保龄球等红线右侧
# 地图单元格状态
MAP_STATE_EMPTY = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_GRASS}  # 由于同一格显然不可能种两个相同的植物，所以用集合
MAP_STATE_WATER = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_WATER}
MAP_STATE_TILE = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_TILE}
MAP_STATE_UNAVAILABLE = {MAP_PLANT:set(), MAP_SLEEP:False, MAP_PLOT_TYPE:MAP_UNAVAILABLE}

# 地图相关像素数据
BACKGROUND_OFFSET_X = 220
MAP_OFFSET_X = 35
MAP_OFFSET_Y = 100
MAP_POOL_OFFSET_X = 42
MAP_POOL_OFFSET_Y = 115
MAP_ROOF_OFFSET_X = 35  # 暂时还不清楚数据
MAP_ROOF_OFFSET_Y = 105 # 暂时还不清楚数据

# 泳池前端陆地部分
MAP_POOL_FRONT_X = SCREEN_WIDTH - 15

# 植物选择菜单栏、传送带菜单栏等类型设定
CHOOSEBAR_TYPE = 'choosebar_type'
CHOOSEBAR_STATIC = 0
CHOOSEBAR_MOVE = 1
CHOSSEBAR_BOWLING = 2
MENUBAR_BACKGROUND = 'ChooserBackground'
MOVEBAR_BACKGROUND = 'MoveBackground'
PANEL_BACKGROUND = 'PanelBackground'
START_BUTTON = 'StartButton'
CARD_POOL = 'card_pool'

# 关于植物栏的像素设置
PANEL_Y_START = 87
PANEL_X_START = 22
PANEL_Y_INTERNAL = 69
PANEL_X_INTERNAL = 53
BAR_CARD_X_INTERNAL = 51

# 所选植物信息索引
PLANT_NAME_INDEX = 0
CARD_INDEX = 1
SUN_INDEX = 2
FROZEN_INDEX = 3

# 传送带模式中的刷新间隔和移动速率
MOVEBAR_CARD_FRESH_TIME = 6000
CARD_MOVE_TIME = 60

# 其他显示物
CAR = 'car'
SUN = 'Sun'
# 植物相关信息
PLANT_IMAGE_RECT = 'plant_image_rect'
# 植物名称
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
STARFRUIT = 'StarFruit'
COFFEEBEAN = 'CoffeeBean'
SEASHROOM = 'SeaShroom'
TALLNUT = 'TallNut'
TANGLEKLEP = 'TangleKlep'
DOOMSHROOM = 'DoomShroom'
ICE_FROZEN_PLOT = 'IceFrozenPlot'
HOLE = 'Hole'
GRAVE = 'Grave'
GRAVEBUSTER = 'GraveBuster'
FUMESHROOM = 'FumeShroom'
GARLIC = 'Garlic'


# 植物集体属性集合
# 在生效时不用与僵尸进行碰撞检测的对象
SKIP_ZOMBIE_COLLISION_CHECK_WHEN_WORKING = {
                # 注意爆炸坚果的触发也是啃食类碰撞，因此这里不能省略
                SQUASH, ICESHROOM,
                REDWALLNUTBOWLING, CHERRYBOMB,
                JALAPENO, DOOMSHROOM,
                POTATOMINE,
                }

# 非植物对象
NON_PLANT_OBJECTS = {
                HOLE, ICE_FROZEN_PLOT,
                GRAVE,
                }

# 所有可能不用与僵尸进行碰撞检测的对象
CAN_SKIP_ZOMBIE_COLLISION_CHECK = ( # 这里运用了集合运算
                # 生效时不检测的植物
                SKIP_ZOMBIE_COLLISION_CHECK_WHEN_WORKING |
                # 非植物对象
                NON_PLANT_OBJECTS |
                # 地刺类
                {SPIKEWEED, }
                )

# 死亡时不触发音效的对象
PLANT_DIE_SOUND_EXCEPTIONS = {
                WALLNUTBOWLING, TANGLEKLEP,
                ICE_FROZEN_PLOT, HOLE,
                GRAVE, JALAPENO,
                REDWALLNUTBOWLING, CHERRYBOMB,
                }

# color_key为白色的对象
PLANT_COLOR_KEY_WHITE = {
                POTATOMINE, SPIKEWEED,
                JALAPENO, SCAREDYSHROOM,
                SUNSHROOM, ICESHROOM,
                HYPNOSHROOM, SQUASH,
                WALLNUTBOWLING, REDWALLNUTBOWLING,
                }

# 直接水生植物
WATER_PLANTS = {
                LILYPAD, SEASHROOM,
                TANGLEKLEP,
                }

# 不用使用通用方法检验攻击状态的植物
PLANT_NON_CHECK_ATTACK_STATE = (    # 这里运用了集合运算
                {# 单独指定攻击状态的植物
                WALLNUTBOWLING,
                # 没有攻击状态的植物
                WALLNUT, TALLNUT,
                TORCHWOOD, SUNFLOWER,
                SUNSHROOM, COFFEEBEAN,
                GRAVEBUSTER, LILYPAD,
                HYPNOSHROOM, GARLIC,
                } |
                # 非植物类
                NON_PLANT_OBJECTS
                )

# 范围爆炸植物，即灰烬植物与寒冰菇
ASH_PLANTS_AND_ICESHROOM = {
                REDWALLNUTBOWLING, CHERRYBOMB,
                JALAPENO, DOOMSHROOM,
                ICESHROOM,
                }


# 植物生命值
PLANT_HEALTH = 300
WALLNUT_HEALTH = 4000
WALLNUT_CRACKED1_HEALTH = WALLNUT_HEALTH//3 * 2
WALLNUT_CRACKED2_HEALTH = WALLNUT_HEALTH//3
TALLNUT_HEALTH = 8000
TALLNUT_CRACKED1_HEALTH = TALLNUT_HEALTH//3 * 2
TALLNUT_CRACKED2_HEALTH = TALLNUT_HEALTH//3
GARLIC_HEALTH = 450
GARLIC_CRACKED1_HEALTH = GARLIC_HEALTH//3 * 2
GARLIC_CRACKED2_HEALTH = GARLIC_HEALTH//3
# 坚果保龄球攻击伤害
WALLNUT_BOWLING_DAMAGE = 550

# 阳光生成属性
PRODUCE_SUN_INTERVAL = 4250 # 基准
FLOWER_SUN_INTERVAL = 24000
SUN_LIVE_TIME = 10000
SUN_VALUE = 25

# 僵尸冷冻
ICE_SLOW_TIME = 10000
MIN_FREEZE_TIME = 4000
ICETRAP = 'IceTrap'

# 植物卡片名称
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
CARD_STARFRUIT = 'card_starfruit'
CARD_COFFEEBEAN = 'card_coffeebean'
CARD_SEASHROOM = 'card_seashroom'
CARD_TALLNUT = 'card_tallnut'
CARD_TANGLEKLEP = 'card_tangleklep'
CARD_DOOMSHROOM = 'card_doomshroom'
CARD_GRAVEBUSTER = 'card_gravebuster'
CARD_FUMESHROOM = 'card_fumeshroom'
CARD_GARLIC = 'card_garlic'


# 植物卡片信息汇总（包括植物名称, 卡片名称, 阳光, 冷却时间）
PLANT_CARD_INFO = (# 元组 (植物名称, 卡片名称, 阳光, 冷却时间)
            (PEASHOOTER,
                CARD_PEASHOOTER,
                100,
                7500),
            (SUNFLOWER,
                CARD_SUNFLOWER,
                50,
                7500),
            (CHERRYBOMB,
                CARD_CHERRYBOMB,
                150,
                50000),
            (WALLNUT,
                CARD_WALLNUT,
                50,
                30000),
            (POTATOMINE,
                CARD_POTATOMINE, 
                25,
                30000),
            (SNOWPEASHOOTER,
                CARD_SNOWPEASHOOTER,
                175,
                7500),
            (CHOMPER,
                CARD_CHOMPER,
                150,
                7500),
            (REPEATERPEA,
                CARD_REPEATERPEA,
                200,
                7500),
            (PUFFSHROOM,
                CARD_PUFFSHROOM,
                0,
                7500),
            (SUNSHROOM,
                CARD_SUNSHROOM,
                25,
                7500),
            (FUMESHROOM,
                CARD_FUMESHROOM,
                75,
                7500),
            (GRAVEBUSTER,
                CARD_GRAVEBUSTER,
                75,
                7500),
            (HYPNOSHROOM,
                CARD_HYPNOSHROOM,
                75,
                30000),
            (SCAREDYSHROOM,
                CARD_SCAREDYSHROOM,
                25,
                7500),
            (ICESHROOM,
                CARD_ICESHROOM,
                75,
                50000),
            (DOOMSHROOM,
                CARD_DOOMSHROOM,
                75,
                50000),
            (LILYPAD,
                CARD_LILYPAD,
                25,
                7500),
            (SQUASH,
                CARD_SQUASH,
                50,
                30000),
            (TANGLEKLEP,
                CARD_TANGLEKLEP,
                25,
                30000),
            (THREEPEASHOOTER,
                CARD_THREEPEASHOOTER,
                325,
                7500),
            (JALAPENO,
                CARD_JALAPENO,
                125,
                50000),
            (SPIKEWEED,
                CARD_SPIKEWEED,
                100,
                7500),
            (TORCHWOOD,
                CARD_TORCHWOOD,
                175,
                7500),
            (TALLNUT,
                CARD_TALLNUT,
                125,
                30000),
            (SEASHROOM,
                CARD_SEASHROOM,
                125,
                30000),
            (STARFRUIT,
                CARD_STARFRUIT,
                125,
                7500),
            (COFFEEBEAN,
                CARD_COFFEEBEAN,
                75,
                7500),
            (GARLIC,
                CARD_GARLIC,
                50,
                7500),
            # 应当保证这两个在一般模式下不可选的特殊植物恒在最后
            (WALLNUTBOWLING,
                CARD_WALLNUT,
                0,
                0),
            (REDWALLNUTBOWLING,
                CARD_REDWALLNUT,
                0,
                0),
            )

# 指定了哪些卡可选（排除坚果保龄球特殊植物）
CARDS_TO_CHOOSE = range(len(PLANT_CARD_INFO) - 2)


# 子弹信息
# 子弹类型
BULLET_PEA = 'PeaNormal'
BULLET_PEA_ICE = 'PeaIce'
BULLET_FIREBALL = 'Fireball'
BULLET_MUSHROOM = 'BulletMushRoom'
BULLET_SEASHROOM = 'BulletSeaShroom'
FUME = 'Fume'
# 子弹伤害
BULLET_DAMAGE_NORMAL = 20
BULLET_DAMAGE_FIREBALL_BODY = 27 # 这是火球本体的伤害，注意不是40，本体(27) + 溅射(13)才是40
BULLET_DAMAGE_FIREBALL_RANGE = 13
# 子弹效果
BULLET_EFFECT_ICE = 'ice'
BULLET_EFFECT_UNICE = 'unice'

# 特殊子弹
# 杨桃子弹
# 子弹名称
BULLET_STAR = 'StarBullet'
# 子弹方向
STAR_FORWARD_UP = 'forwardUp'   # 向前上方
STAR_FORWARD_DOWN = 'forwardDown'   #向前下方
STAR_BACKWARD = 'backward'  #向后
STAR_UPWARD = 'upward'  # 向上
STAR_DOWNWARD = 'downward'  # 向下

# 僵尸信息
ZOMBIE_IMAGE_RECT = 'zombie_image_rect'
ZOMBIE_HEAD = 'ZombieHead'
NORMAL_ZOMBIE = 'Zombie'
CONEHEAD_ZOMBIE = 'ConeheadZombie'
BUCKETHEAD_ZOMBIE = 'BucketheadZombie'
FLAG_ZOMBIE = 'FlagZombie'
NEWSPAPER_ZOMBIE = 'NewspaperZombie'
FOOTBALL_ZOMBIE = 'FootballZombie'
DUCKY_TUBE_ZOMBIE = 'DuckyTubeZombie'
CONEHEAD_DUCKY_TUBE_ZOMBIE = 'ConeheadDuckyTubeZombie'
BUCKETHEAD_DUCKY_TUBE_ZOMBIE = 'BucketheadDuckyTubeZombie'
SCREEN_DOOR_ZOMBIE = 'ScreenDoorZombie'
POLE_VAULTING_ZOMBIE = 'PoleVaultingZombie'
ZOMBONI = 'Zomboni'
SNORKELZOMBIE = 'SnorkelZombie'

BOOMDIE = 'BoomDie'

# 对僵尸的攻击类型设置
ZOMBIE_DEAFULT_DAMAGE = 'helmet2First'
ZOMBIE_HELMET_2_FIRST = 'helmet2First'  # 优先攻击二类防具
ZOMBIE_COMMON_DAMAGE = 'commonDamage'   # 优先攻击僵尸与一类防具的整体
ZOMBIE_RANGE_DAMAGE = 'rangeDamage' # 范围攻击，同时伤害二类防具与(僵尸与一类防具的整体)
ZOMBIE_ASH_DAMAGE = 'ashDamage' # 灰烬植物攻击，直接伤害本体
ZOMBIE_WALLNUT_BOWLING_DANMAGE = 'wallnutBowlingDamage' # 坚果保龄球冲撞伤害

# 僵尸生命值设置
# 有关本体
NORMAL_HEALTH = 200 # 普通僵尸生命值
POLE_VAULTING_HEALTH = 333
ZOMBONI_HEALTH = 1280
# 冰车损坏点
ZOMBONI_DAMAGED1_HEALTH = 2 * ZOMBONI_HEALTH // 3 + 70
ZOMBONI_DAMAGED2_HEALTH = ZOMBONI_HEALTH // 3 + 70
# 掉头后僵尸的生命值
LOSTHEAD_HEALTH = 70
POLE_VAULTING_LOSTHEAD_HEALTH = 167
# 有关一类防具
CONEHEAD_HEALTH = 370
BUCKETHEAD_HEALTH = 1100
FOOTBALL_HELMET_HEALTH = 1400
# 有关二类防具
NEWSPAPER_HEALTH = 150
SCREEN_DOOR_HEALTH = 1100

# 僵尸行动信息
ATTACK_INTERVAL = 500
ZOMBIE_ATTACK_DAMAGE = 50
ZOMBIE_WALK_INTERVAL = 60  # 僵尸步行间隔

# 僵尸生成位置
ZOMBIE_START_X = SCREEN_WIDTH + 30  # 场宽度不一样，用于拟合


# 僵尸集体属性集合
# 僵尸生成信息字典：包含生成僵尸名称、僵尸级别、生成权重
CREATE_ZOMBIE_DICT = {  # 生成僵尸:(级别, 权重)
                NORMAL_ZOMBIE:                  (1, 4000),
                FLAG_ZOMBIE:                    (1, 0),
                CONEHEAD_ZOMBIE:                (2, 4000),
                BUCKETHEAD_ZOMBIE:              (4, 3000),
                NEWSPAPER_ZOMBIE:               (2, 1000),
                FOOTBALL_ZOMBIE:                (7, 2000),
                DUCKY_TUBE_ZOMBIE:              (1, 0), # 作为变种，不主动生成
                CONEHEAD_DUCKY_TUBE_ZOMBIE:     (2, 0), # 作为变种，不主动生成
                BUCKETHEAD_DUCKY_TUBE_ZOMBIE:   (4, 0), # 作为变种，不主动生成
                SCREEN_DOOR_ZOMBIE:             (4, 3500),
                POLE_VAULTING_ZOMBIE:           (2, 2000),
                ZOMBONI:                        (7, 2000),
                SNORKELZOMBIE:                  (3, 2000),
                }

# 记录陆生僵尸的水生变种
CONVERT_ZOMBIE_IN_POOL = {
                NORMAL_ZOMBIE:      DUCKY_TUBE_ZOMBIE,
                CONEHEAD_ZOMBIE:    CONEHEAD_DUCKY_TUBE_ZOMBIE,
                BUCKETHEAD_ZOMBIE:  BUCKETHEAD_DUCKY_TUBE_ZOMBIE,
                }

# 水上僵尸集合
WATER_ZOMBIE = {
                DUCKY_TUBE_ZOMBIE, CONEHEAD_DUCKY_TUBE_ZOMBIE,
                BUCKETHEAD_DUCKY_TUBE_ZOMBIE, SNORKELZOMBIE,
                }


# 状态类型
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

# 关卡状态
CHOOSE = 'choose'
PLAY = 'play'

# 无穷大常量
INF = float('inf')
