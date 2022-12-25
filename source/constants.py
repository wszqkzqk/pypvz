import os
import pygame as pg

# 用户数据及日志存储路径
if os.name == "nt": # Windows系统存储路径
    USERDATA_PATH = os.path.expandvars(os.path.join("%APPDATA%", "pypvz", "userdata.json"))
    USERLOG_PATH = os.path.expandvars(os.path.join("%APPDATA%", "pypvz", "run.log"))
else:   # 非Windows系统存储路径
    USERDATA_PATH = os.path.expanduser(os.path.join("~", ".config", "pypvz", "userdata.json"))
    USERLOG_PATH = os.path.expanduser(os.path.join("~", ".config", "pypvz", "run.log"))

# 游戏图片资源路径
PATH_IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "graphics")
# 游戏音乐文件夹路径
PATH_MUSIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources","music")
# 窗口图标
ORIGINAL_LOGO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pypvz-exec-logo.png")
# 字体路径
FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "DroidSansFallback.ttf")

# 窗口标题
ORIGINAL_CAPTION = "pypvz"

# 游戏模式
GAME_MODE = "mode"
MODE_ADVENTURE = "adventure"
MODE_LITTLEGAME = "littleGame"

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
YELLOWGREEN  = ( 55, 200,   0)
LIGHTGRAY    = (107, 108, 145)
PARCHMENT_YELLOW = (207, 146, 83)

# 退出游戏按钮
EXIT = "exit"
HELP = "help"
# 游戏界面可选的菜单
LITTLE_MENU = "littleMenu"
BIG_MENU = "bigMenu"
RESTART_BUTTON = "restartButton"
MAINMENU_BUTTON = "mainMenuButton"
LITTLEGAME_BUTTON = "littleGameButton"
OPTION_BUTTON = "optionButton"
SOUND_VOLUME_BUTTON = "volumeButton"
UNIVERSAL_BUTTON = "universalButton"
# 金银向日葵奖杯
TROPHY_SUNFLOWER = "sunflowerTrophy"
# 小铲子
SHOVEL = "shovel"
SHOVEL_BOX = "shovelBox"
# 一大波僵尸来袭图片
HUGE_WAVE_APPROCHING = "Approching"
# 关卡进程图片
LEVEL_PROGRESS_BAR = "LevelProgressBar"
LEVEL_PROGRESS_ZOMBIE_HEAD = "LevelProgressZombieHead"
LEVEL_PROGRESS_FLAG = "LevelProgressFlag"


# GAME INFO字典键值
CURRENT_TIME = "current time"
PASSED_ALL = "passed all"   # 已完成该模式下的所有游戏，应当显示向日葵奖杯获得界面
LEVEL_NUM = "level num"
LITTLEGAME_NUM = "littleGame num"
LEVEL_COMPLETIONS = "level completions"
LITTLEGAME_COMPLETIONS = "littleGame completions"
GAME_RATE = "game rate"
SOUND_VOLUME = "volume"

# 整个游戏的状态
MAIN_MENU = "main menu"
LOAD_SCREEN = "load screen"
GAME_LOSE = "game lose"
GAME_VICTORY = "game victory"
LEVEL = "level"
AWARD_SCREEN = "award screen"
HELP_SCREEN = "help screen"

# 界面图片文件名
MAIN_MENU_IMAGE = "MainMenu"
OPTION_ADVENTURE = "Adventure"
GAME_LOSE_IMAGE = "GameLose"
GAME_VICTORY_IMAGE = "GameVictory"
AWARD_SCREEN_IMAGE = "AwardScreen"
HELP_SCREEN_IMAGE = "HelpScreen"

# 地图相关内容
BACKGROUND_NAME = "Background"
BACKGROUND_TYPE = "background_type"
INIT_SUN_NAME = "init_sun_value"
ZOMBIE_LIST = "zombie_list"
GAME_TITLE = "title"

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
GRADE_GRAVES = "grade_graves"
# 不同墓碑等级对应的信息，列表位置对应的是墓碑等级
GRAVES_GRADE_INFO = (0, 4, 7, 11)

# 僵尸生成方式
SPAWN_ZOMBIES = "spawn_zombies"
SPAWN_ZOMBIES_AUTO = 1
SPAWN_ZOMBIES_LIST = 0
INCLUDED_ZOMBIES = "included_zombies"
NUM_FLAGS = "num_flags"
INEVITABLE_ZOMBIE_DICT = "inevitable_zombie_list"
SURVIVAL_ROUNDS = "survival_rounds"

# 地图单元格属性
MAP_PLANT = "plantnames"
MAP_SLEEP = "sleep" # 有没有休眠的蘑菇，作是否能种植咖啡豆的判断
MAP_PLOT_TYPE = "plot_type"
# 地图单元格区域类型
MAP_GRASS = "grass"
MAP_WATER = "water"
MAP_TILE = "tile"  # 指屋顶上的瓦片
MAP_UNAVAILABLE = "unavailable" # 指完全不能种植物的地方，包括无草皮的荒地和坚果保龄球等红线右侧

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
CHOOSEBAR_TYPE = "choosebar_type"
CHOOSEBAR_STATIC = 0
CHOOSEBAR_MOVE = 1
CHOOSEBAR_BOWLING = 2
MENUBAR_BACKGROUND = "ChooserBackground"
MOVEBAR_BACKGROUND = "MoveBackground"
PANEL_BACKGROUND = "PanelBackground"
START_BUTTON = "StartButton"
CARD_POOL = "card_pool"

# 关于植物栏的像素设置
PANEL_Y_START = 87
PANEL_X_START = 22
PANEL_Y_INTERNAL = 69
PANEL_X_INTERNAL = 53
BAR_CARD_X_INTERNAL = 51

# 植物卡片信息索引
PLANT_NAME_INDEX = 0
CARD_INDEX = 1
SUN_INDEX = 2
FROZEN_TIME_INDEX = 3

# 传送带模式中的刷新间隔和移动速率
MOVEBAR_CARD_FRESH_TIME = 6000
CARD_MOVE_TIME = 60

# 其他显示物
CAR = "car"
SUN = "Sun"

# plant子类非植物对象（这里的是不包括阳光、子弹的拟植物对象）
NON_PLANT_OBJECTS = {
                HOLE := "Hole",
                ICEFROZENPLOT := "IceFrozenPlot",
                GRAVE := "Grave",
}

# 植物相关信息
PLANT_IMAGE_RECT = "plant_image_rect"
BOOM_IMAGE = "Boom"

# 植物卡片信息汇总（包括植物名称, 卡片名称, 阳光, 冷却时间）
PLANT_CARD_INFO = (# 元组 (植物名称, 卡片名称, 阳光, 冷却时间)
            (PEASHOOTER := "Peashooter",
                CARD_PEASHOOTER := "card_peashooter",
                100,
                7500),
            (SUNFLOWER := "SunFlower",
                CARD_SUNFLOWER := "card_sunflower",
                50,
                7500),
            (CHERRYBOMB := "CherryBomb",
                CARD_CHERRYBOMB := "card_cherrybomb",
                150,
                50000),
            (WALLNUT := "WallNut",
                CARD_WALLNUT := "card_wallnut",
                50,
                30000),
            (POTATOMINE := "PotatoMine",
                CARD_POTATOMINE := "card_potatomine", 
                25,
                30000),
            (SNOWPEASHOOTER := "SnowPea",
                CARD_SNOWPEASHOOTER := "card_snowpea",
                175,
                7500),
            (CHOMPER := "Chomper",
                CARD_CHOMPER := "card_chomper",
                150,
                7500),
            (REPEATERPEA := "RepeaterPea",
                CARD_REPEATERPEA := "card_repeaterpea",
                200,
                7500),
            (PUFFSHROOM := "PuffShroom",
                CARD_PUFFSHROOM := "card_puffshroom",
                0,
                7500),
            (SUNSHROOM := "SunShroom",
                CARD_SUNSHROOM := "card_sunshroom",
                25,
                7500),
            (FUMESHROOM := "FumeShroom",
                CARD_FUMESHROOM := "card_fumeshroom",
                75,
                7500),
            (GRAVEBUSTER := "GraveBuster",
                CARD_GRAVEBUSTER := "card_gravebuster",
                75,
                7500),
            (HYPNOSHROOM := "HypnoShroom",
                CARD_HYPNOSHROOM := "card_hypnoshroom",
                75,
                30000),
            (SCAREDYSHROOM := "ScaredyShroom",
                CARD_SCAREDYSHROOM := "card_scaredyshroom",
                25,
                7500),
            (ICESHROOM := "IceShroom",
                CARD_ICESHROOM := "card_iceshroom",
                75,
                50000),
            (DOOMSHROOM := "DoomShroom",
                CARD_DOOMSHROOM := "card_doomshroom",
                125,
                50000),
            (LILYPAD := "LilyPad",
                CARD_LILYPAD := "card_lilypad",
                25,
                7500),
            (SQUASH := "Squash",
                CARD_SQUASH := "card_squash",
                50,
                30000),
            (TANGLEKLEP := "TangleKlep",
                CARD_TANGLEKLEP := "card_tangleklep",
                25,
                30000),
            (THREEPEASHOOTER := "Threepeater",
                CARD_THREEPEASHOOTER := "card_threepeashooter",
                325,
                7500),
            (JALAPENO := "Jalapeno",
                CARD_JALAPENO := "card_jalapeno",
                125,
                50000),
            (SPIKEWEED := "Spikeweed",
                CARD_SPIKEWEED := "card_spikeweed",
                100,
                7500),
            (TORCHWOOD := "TorchWood",
                CARD_TORCHWOOD := "card_torchwood",
                175,
                7500),
            (TALLNUT := "TallNut",
                CARD_TALLNUT := "card_tallnut",
                125,
                30000),
            (SEASHROOM := "SeaShroom",
                CARD_SEASHROOM := "card_seashroom",
                0,
                30000),
            (STARFRUIT := "StarFruit",
                CARD_STARFRUIT := "card_starfruit",
                125,
                7500),
            (PUMPKINHEAD := "PumpkinHead",
                CARD_PUMPKINHEAD := "card_pumpkinhead",
                125,
                30000),
            (COFFEEBEAN := "CoffeeBean",
                CARD_COFFEEBEAN := "card_coffeebean",
                75,
                7500),
            (GARLIC := "Garlic",
                CARD_GARLIC := "card_garlic",
                50,
                7500),
            # 应当保证这3个在一般模式下不可选的特殊植物恒在最后
            (WALLNUTBOWLING := "WallNutBowling",
                CARD_WALLNUT := "card_wallnut",
                0,
                0),
            (REDWALLNUTBOWLING := "RedWallNutBowling",
                CARD_REDWALLNUT := "card_redwallnut",
                0,
                0),
            (GIANTWALLNUT := "GiantWallNut",
                CARD_GIANTWALLNUT := "card_giantwallnut",
                0,
                0),
)

# 卡片中的植物名称与索引序号的对应关系，指定名称以得到索引值
PLANT_CARD_INDEX = {item[PLANT_NAME_INDEX]: index for (index, item) in enumerate(PLANT_CARD_INFO)}

# 指定了哪些卡可选（排除坚果保龄球特殊植物）
CARDS_TO_CHOOSE = range(len(PLANT_CARD_INFO) - 3)


# 植物集体属性集合
# 也许以后有必要的可以重新加入到对象的属性中
# 在生效时不用与僵尸进行碰撞检测的对象（即生效时不可发生被僵尸啃食的事件）
SKIP_ZOMBIE_COLLISION_CHECK_WHEN_WORKING = {
                # 注意爆炸坚果的触发也是啃食类碰撞，因此只能算作爆炸后不检测
                SQUASH, ICESHROOM,
                REDWALLNUTBOWLING, CHERRYBOMB,
                JALAPENO, DOOMSHROOM,
                POTATOMINE,
}

# 所有可能不用与僵尸进行碰撞检测的对象
CAN_SKIP_ZOMBIE_COLLISION_CHECK = ( # 这里运用了集合运算
                # 注意这个外围的小括号是用来换行的
                # 各个部分末！尾！千！万！不！能！加！逗！号！！！

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
                ICEFROZENPLOT, HOLE,
                GRAVE, JALAPENO,
                REDWALLNUTBOWLING, CHERRYBOMB,
                GIANTWALLNUT,
}

# 直接水生植物
WATER_PLANTS = {
                LILYPAD, SEASHROOM,
                TANGLEKLEP,
}

# 攻击状态检查类型
CHECK_ATTACK_NEVER = 0
CHECK_ATTACK_ALWAYS = 1

# 范围爆炸植物，即灰烬植物与寒冰菇
ASH_PLANTS_AND_ICESHROOM = {
                REDWALLNUTBOWLING, CHERRYBOMB,
                JALAPENO, DOOMSHROOM,
                ICESHROOM,
}

# 白天要睡觉的植物
CAN_SLEEP_PLANTS = {
    PUFFSHROOM, SUNSHROOM,
    FUMESHROOM, HYPNOSHROOM,
    SCAREDYSHROOM, ICESHROOM,
    DOOMSHROOM, SEASHROOM,
}

# 选卡不推荐选择理由
REASON_WILL_SLEEP = 1
REASON_SLEEP_BUT_COFFEE_BEAN = 2
REASON_OTHER = 3

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
ICETRAP = "IceTrap"

# 子弹信息
# 子弹类型
BULLET_PEA = "PeaNormal"
BULLET_PEA_ICE = "PeaIce"
BULLET_FIREBALL = "Fireball"
BULLET_MUSHROOM = "BulletMushRoom"
BULLET_SEASHROOM = "BulletSeaShroom"
FUME = "Fume"
# 子弹伤害
BULLET_DAMAGE_NORMAL = 20
BULLET_DAMAGE_FIREBALL_BODY = 27 # 这是火球本体的伤害，注意不是40，本体(27) + 溅射(13)才是40
BULLET_DAMAGE_FIREBALL_RANGE = 13   # 原版溅射伤害会随着僵尸数量增多而减少，这里相当于做了一个增强
# 子弹效果
BULLET_EFFECT_ICE = "ice"
BULLET_EFFECT_UNICE = "unice"

# 特殊子弹
# 杨桃子弹
# 子弹名称
BULLET_STAR = "StarBullet"
# 子弹方向
STAR_FORWARD_UP = "forwardUp"   # 向前上方
STAR_FORWARD_DOWN = "forwardDown"   #向前下方
STAR_BACKWARD = "backward"  #向后
STAR_UPWARD = "upward"  # 向上
STAR_DOWNWARD = "downward"  # 向下

# 有爆炸图片的子弹
BULLET_INDEPENDENT_BOOM_IMG = { BULLET_PEA, BULLET_PEA_ICE,
                                BULLET_MUSHROOM, BULLET_SEASHROOM,
                                BULLET_STAR, 
}

# 僵尸信息
ZOMBIE_IMAGE_RECT = "zombie_image_rect"
ZOMBIE_HEAD = "ZombieHead"
NORMAL_ZOMBIE = "Zombie"
CONEHEAD_ZOMBIE = "ConeheadZombie"
BUCKETHEAD_ZOMBIE = "BucketheadZombie"
FLAG_ZOMBIE = "FlagZombie"
NEWSPAPER_ZOMBIE = "NewspaperZombie"
FOOTBALL_ZOMBIE = "FootballZombie"
DUCKY_TUBE_ZOMBIE = "DuckyTubeZombie"
CONEHEAD_DUCKY_TUBE_ZOMBIE = "ConeheadDuckyTubeZombie"
BUCKETHEAD_DUCKY_TUBE_ZOMBIE = "BucketheadDuckyTubeZombie"
SCREEN_DOOR_ZOMBIE = "ScreenDoorZombie"
POLE_VAULTING_ZOMBIE = "PoleVaultingZombie"
ZOMBONI = "Zomboni"
SNORKELZOMBIE = "SnorkelZombie"

BOOMDIE = "BoomDie"

# 对僵尸的攻击类型设置
ZOMBIE_DEAFULT_DAMAGE = ZOMBIE_HELMET_2_FIRST = "helmet2First"  # 优先攻击二类防具
ZOMBIE_COMMON_DAMAGE = "commonDamage"   # 优先攻击僵尸与一类防具的整体
ZOMBIE_RANGE_DAMAGE = "rangeDamage" # 范围攻击，同时伤害二类防具与(僵尸与一类防具的整体)
ZOMBIE_ASH_DAMAGE = "ashDamage" # 灰烬植物攻击，直接伤害本体
ZOMBIE_WALLNUT_BOWLING_DANMAGE = "wallnutBowlingDamage" # 坚果保龄球冲撞伤害

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
IDLE = "idle"
FLY = "fly"
EXPLODE = "explode"
ATTACK = "attack"
ATTACKED = "attacked"
DIGEST = "digest"
WALK = "walk"
DIE = "die"
CRY = "cry"
FREEZE = "freeze"
SLEEP = "sleep"

# 关卡状态
CHOOSE = "choose"
PLAY = "play"

# 加载矩形碰撞范围 用于消除文件边框影响
# 植物
PLANT_RECT = {
        BULLET_PEA:             {"x":28, "y":0, "width":28, "height":34},
        BULLET_PEA_ICE:         {"x":26, "y":0, "width":30, "height":34},
        CHOMPER:                {"x":0, "y":0, "width":100, "height":114},
        PUFFSHROOM:             {"x":0, "y":28, "width":35, "height":38},
        f"{PUFFSHROOM}Sleep":   {"x":1, "y":0, "width":39, "height":65},
        BULLET_MUSHROOM:        {"x":0, "y":1, "width":55, "height":21},
        BULLET_SEASHROOM:       {"x":0, "y":1, "width":55, "height":21},
        POTATOMINE:             {"x":0, "y":0, "width":75, "height":55},
        SQUASH:                 {"x":10, "y":140, "width":80, "height":86},
        f"{SQUASH}Aim":         {"x":10, "y":140, "width":80, "height":86},
        SPIKEWEED:              {"x":3, "y":0, "width":80, "height":35}
}
# 僵尸
ZOMBIE_RECT = {
        NORMAL_ZOMBIE:                  {"x":62, "width":90},
        f"{NORMAL_ZOMBIE}Attack":       {"x":62, "width":90},
        f"{NORMAL_ZOMBIE}LostHead":     {"x":62, "width":90},
        f"{NORMAL_ZOMBIE}LostHeadAttack":{"x":62, "width":90},
        f"{NORMAL_ZOMBIE}Die":          {"x":0, "width":164},
        BOOMDIE:                        {"x":68, "width":80},
        CONEHEAD_ZOMBIE:                {"x":80, "width":80},
        f"{CONEHEAD_ZOMBIE}Attack":     {"x":79, "width":87},
        BUCKETHEAD_ZOMBIE:              {"x":54, "width":90},
        f"{BUCKETHEAD_ZOMBIE}Attack":   {"x":46, "width":90},
        FLAG_ZOMBIE:                    {"x":56, "width":110},
        f"{FLAG_ZOMBIE}Attack":         {"x":60, "width":100},
        f"{FLAG_ZOMBIE}LostHead":       {"x":55, "width":110},
        f"{FLAG_ZOMBIE}LostHeadAttack": {"x":55, "width":110},
        NEWSPAPER_ZOMBIE:               {"x":48, "width":92},
        f"{NEWSPAPER_ZOMBIE}Attack":    {"x":48, "width":92},
        f"{NEWSPAPER_ZOMBIE}NoPaper":   {"x":40, "width":98},
        f"{NEWSPAPER_ZOMBIE}NoPaperAttack":{"x":48, "width":92},
        f"{NEWSPAPER_ZOMBIE}LostHead":  {"x":44, "width":96},
        f"{NEWSPAPER_ZOMBIE}LostHeadAttack":{"x":48, "width":92},
        f"{NEWSPAPER_ZOMBIE}Die":       {"x":0, "width":100},
        f"{DUCKY_TUBE_ZOMBIE}Die":      {"x":55, "width":105},
        f"{DUCKY_TUBE_ZOMBIE}LostHead": {"x":55, "width":105},
        SCREEN_DOOR_ZOMBIE:             {"x":41, "width":100},
        f"{SCREEN_DOOR_ZOMBIE}Attack":  {"x":41, "width":100},
}   # 这里还有懒得写代码的补加，用循环实现
for _part1 in (DUCKY_TUBE_ZOMBIE, CONEHEAD_DUCKY_TUBE_ZOMBIE, BUCKETHEAD_DUCKY_TUBE_ZOMBIE):
    for _part2 in ("", "Attack", "Swim"):
        ZOMBIE_RECT[f"{_part1}{_part2}"] = {"x":55, "width":105}


# 音效
def _getSound(filename):
    return pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(__file__)) ,"resources", "sound", filename))
# 所有音效的元组，用一波海象算子表达，免得要维护两个
SOUNDS = (  # 程序交互等
            SOUND_TAPPING_CARD              := _getSound("tap.ogg"),
            SOUND_HELP_SCREEN               := _getSound("helpScreen.ogg"),
            # 植物
            SOUND_FIREPEA_EXPLODE           := _getSound("firepea.ogg"),
            SOUND_BULLET_EXPLODE            := _getSound("bulletExplode.ogg"),
            SOUND_SHOOT                     := _getSound("shoot.ogg"),
            SOUND_SNOWPEA_SPARKLES          := _getSound("snowPeaSparkles.ogg"),
            SOUND_BOMB                      := _getSound("bomb.ogg"),
            SOUND_BIGCHOMP                  := _getSound("bigchomp.ogg"),
            SOUND_PUFF                      := _getSound("puff.ogg"),
            SOUND_POTATOMINE                := _getSound("potatomine.ogg"),
            SOUND_SQUASHING                 := _getSound("squashing.ogg"),
            SOUND_SQUASH_HMM                := _getSound("squashHmm.ogg"),
            SOUND_PLANT_GROW                := _getSound("plantGrow.ogg"),
            SOUND_MUSHROOM_WAKEUP           := _getSound("mushroomWakeup.ogg"),
            SOUND_TANGLE_KELP_DRAG          := _getSound("tangleKelpDrag.ogg"),
            SOUND_DOOMSHROOM                := _getSound("doomshroom.ogg"),
            SOUND_GRAVEBUSTER_CHOMP         := _getSound("gravebusterchomp.ogg"),
            SOUND_FUME                      := _getSound("fume.ogg"),
            # 僵尸
            SOUND_ZOMBIE_ENTERING_WATER     := _getSound("zombieEnteringWater.ogg"),
            SOUND_ZOMBIE_ATTACKING          := _getSound("zombieAttack.ogg"),
            SOUND_FREEZE                    := _getSound("freeze.ogg"),
            SOUND_HYPNOED                   := _getSound("hypnoed.ogg"),
            SOUND_NEWSPAPER_RIP             := _getSound("newspaperRip.ogg"),
            SOUND_NEWSPAPER_ZOMBIE_ANGRY    := _getSound("newspaperZombieAngry.ogg"),
            SOUND_POLEVAULT_JUMP            := _getSound("polevaultjump.ogg"),
            SOUND_ZOMBONI                   := _getSound("zomboni.ogg"),
            SOUND_ZOMBONI_EXPLOSION         := _getSound("zomboniExplosion.ogg"),
            # 关卡中
            SOUND_CAR_WALKING               := _getSound("carWalking.ogg"),
            SOUND_ZOMBIE_COMING             := _getSound("zombieComing.ogg"),
            SOUND_ZOMBIE_VOICE              := _getSound("zombieVoice.ogg"),
            SOUND_HUGE_WAVE_APPROCHING      := _getSound("hugeWaveApproching.ogg"),
            SOUND_BUTTON_CLICK              := _getSound("buttonclick.ogg"),
            SOUND_COLLECT_SUN               := _getSound("collectSun.ogg"),
            SOUND_CLICK_CARD                := _getSound("clickCard.ogg"),
            SOUND_SHOVEL                    := _getSound("shovel.ogg"),
            SOUND_PLANT                     := _getSound("plant.ogg"),
            SOUND_BOWLING_IMPACT            := _getSound("bowlingimpact.ogg"),
            SOUND_PLANT_DIE                 := _getSound("plantDie.ogg"),
            SOUND_EVILLAUGH                 := _getSound("evillaugh.ogg"),
            SOUND_LOSE                      := _getSound("lose.ogg"),
            SOUND_WIN                       := _getSound("win.ogg"),
            SOUND_SCREAM                    := _getSound("scream.ogg"),
            SOUND_CANNOT_CHOOSE_WARNING     := _getSound("cannotChooseWarning.ogg"),
            SOUND_FINAL_FANFARE             := _getSound("finalfanfare.ogg"),
)

# 记录本地存储文件初始值
INIT_USERDATA = {   
                LEVEL_NUM:              1,
                LITTLEGAME_NUM:         1,
                LEVEL_COMPLETIONS:      0,
                LITTLEGAME_COMPLETIONS: 0,
                GAME_RATE:              1,
                SOUND_VOLUME:           1,
}

# 无穷大常量
INF = float("inf")  # python传递字符串性能较低，故在这里对inf声明一次，以后仅需调用即可，虽然真正的用处是可以自动补全（
