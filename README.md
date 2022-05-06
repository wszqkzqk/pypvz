## Python版植物大战僵尸

植物大战僵尸游戏的Python实现，基于[marblexu的项目进行创作](https://github.com/marblexu/PythonPlantsVsZombies)，部分代码也整合自[callmebg的项目](https://github.com/callmebg/PythonPlantsVsZombies)
  
**本项目为个人python语言学习的练习项目，仅供个人学习和研究使用，不得用于其他用途。如果这个游戏侵犯了版权，请联系我删除**

* 已有的植物：向日葵，豌豆射手，坚果墙，寒冰射手，樱桃炸弹，三线射手，大嘴花，小喷菇，土豆雷，地刺，胆小菇，倭瓜，火爆辣椒，阳光菇，寒冰菇，魅惑菇，火炬树桩，睡莲，杨桃，咖啡豆，海蘑菇
* 已有的僵尸：普通僵尸，旗帜僵尸，路障僵尸，铁桶僵尸，读报僵尸，橄榄球僵尸，鸭子救生圈僵尸，铁门僵尸
* 使用 JSON 文件记录关卡信息数据 
* 支持选择植物卡片
* 支持白昼模式，夜晚模式，泳池模式，传送带模式和坚果保龄球模式
* 支持背景音乐播放
* 支持音效
* 支持全屏模式
  * 按`F`键进入全屏模式，按`U`键恢复至窗口模式
* 支持用小铲子移除植物
* 支持分波生成僵尸
* 支持“关卡进程”进度条显示

## 环境要求

* `Python` >= 3.7 
* `Python-Pygame` >= 1.9

## 开始游戏

### 使用仓库源代码

先克隆仓库内容，再运行`main.py`：

```shell
git clone https://github.com/wszqkzqk/pypvz.git
cd pypvz
python main.py
```

### 使用Windows可执行文件

在本仓库的`Release`页面中下载`pypvz.exe`文件，双击运行即可
- 仅支持64位操作系统

## 方法

* 使用鼠标收集阳光,种植植物
* 你可以通过更改`source/constants.py`中的`START_LEVEL_NUM`的数值来更改冒险模式的起始关卡，更改`START_LITTLE_GAME_NUM`的数值来更改小游戏的起始关卡：
  * 冒险模式：
    * 1 和 2：白昼模式
    * 3：夜晚模式
    * 4：泳池模式
  * 小游戏模式：
    * 1：传送带模式
    * 2：坚果保龄球模式
* 可以通过修改`source/constants.py`中的`GAME_RATE`来调节游戏速度倍率
* **注意：目前单文件发布版本不支持自定义调整关卡**

## Windows单文件封装

编译依赖：
- `Python` >= 3.7
- `Python-Pygame` >= 1.9
- `Nuitka`
- `MinGW-w64`（或其他C编译器）
- `ccache`
- `depends`
- `python-zstandard`（可选）

**在编译环境安装不全时，Nuitka可以自动安装MinGW-w64、ccache和depends**

- 由于目前Nuitka打包尚存bug，无法自动封装`pygame`中用来解码音频的相关`.dll`文件，因此需要手动在编译命令中添加
  - 对于`mp3`编码，需要添加`libmpg123-0.dll`
  - 对于`vorbis`编码，需要添加`libogg-0.dll`，`libvorbis-0.dll`和`libvorbisfile-3.dll`
  - 对于`opus`编码，需要添加`libogg-0.dll`，`libopus-0.dll`和`libopusfile-0.dll`
- 以添加`opus`和`vorbis`编码的背景音乐支持为例，编译需执行以下命令：

``` cmd
git clone https://github.com/wszqkzqk/pypvz.git
cd pypvz
nuitka --mingw64 --standalone --onefile --show-progress --show-memory --output-dir=out --windows-icon-from-ico=pypvz.ico --include-data-dir=resources=resources --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libogg-0.dll=libogg-0.dll --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libopus-0.dll=libopus-0.dll --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libopusfile-0.dll=libopusfile-0.dll --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libvorbisfile-3.dll=libvorbisfile-3.dll --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libvorbis-0.dll=libvorbis-0.dll --windows-disable-console --windows-product-name=pypvz --windows-company-name=null --windows-file-description="植物大战僵尸的Python实现" --windows-product-version=0.6.9.0 main.py
```

* 其中`C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\xxx.dll`应当替换为`xxx.dll`实际所在路径
* 由于仅复制了`opus`与`vorbis`的解码器，故要求所有背景音乐都要以opus或vorbis编码
* `--windows-product-version=`所跟内容格式必须为`x.x.x.x`

可执行文件生成路径为`./out/main.exe`

## 已知bug

以下问题囿于个人目前的能力与精力，没有修复：
* 植物刚刚种植会立刻攻击，而非像原版一样有间歇时间
* 冷冻的僵尸未用蓝色滤镜标识
  * 这个想不到很好的实现方法，可能会想一种替代方案
* 魅惑的僵尸未用红色滤镜标识
  * 这个可能会作为一种“特性”

**欢迎提供[Pull requests](https://github.com/wszqkzqk/pypvz/pulls)或修复方法建议，也欢迎在这里反馈新的bug()**

## ~~画大饼~~计划（不保证实施）

* 增加关卡进程进度条
  * 该功能自0.5.4已实现
* 增加保存数据文件以存储用户进度的功能
* 增加调整音量的功能
  * `pg.mixer.music.set_volume()`
  * 可以用`音量+`、`音量-`按钮实现
  * 注意字体颜色渲染
* 关卡开始前增加预览界面
* 增加解锁与选关功能
  * 目前的设想与原版不同，在完成两轮冒险模式（初始冒险模式 + 戴夫选关的冒险模式）后可以自主选关~~（当然现在只是画饼）~~
* 更改僵尸生成方式
  * 使僵尸生成更随机化，由JSON记录改为随机数生成
    * 该功能自0.5.0已经基本实现
    * 使用原版设定，每面旗帜出10波僵尸，9个小波，1个大波
    * 采用手机版设定，无尽模式没有红眼计数和变速设定，每波红眼权重为1000，平均分布
  * 增加僵尸死亡后有概率掉落奖励的机制
* 增加更多植物、僵尸类型与游戏功能、模式，尽量符合原版基本设计
* 细分伤害种类
  * 实体
    * 一般子弹实体——普通伤害且无特殊效果
      * 豌豆
        * 已实现
      * 孢子
        * 已实现
      * 星星
        * 已实现
      * 尖刺
    * 特殊子弹实体——非普通伤害或有特殊效果
      * 冰豌豆（减速）
        * 已实现
      * 火豌豆（2倍伤害、带有1x1溅射）
        * 已实现
    * 投掷
      * 西瓜（4倍伤害，带有3x3溅射）
      * 冰瓜（4倍伤害，带有3x3溅射伤害与减速）
      * 玉米粒
      * 黄油（2倍伤害，定格）
      * 卷心菜（2倍伤害）
    * 烟雾
      * 线形范围烟雾
      * 圆形范围烟雾
    * 碾压
      * 倭瓜
        * 已实现
  * 爆炸
    * 一般爆炸
      * 樱桃炸弹、爆炸坚果与玉米加农炮炮弹
        * 已实现
      * 毁灭菇
    * 火焰爆炸
      * 火爆辣椒
        * 已实现
    * 非灰烬类爆炸
      * 土豆雷
        * 已实现
  * 从地面刺伤
    * 已实现
  * 缠绕与拖拽
  * 吞噬
    * 已实现
  * 特殊
    * 魅惑
      * 已实现
    * 移除铁制防具
    * 全场伤害与冰冻
      * 已实现
    * 撞击
      * 坚果保龄球撞击
        * 已实现
      * 巨型坚果保龄球撞击
    * 吹走
* 增加部分音效
  * 如爆炸、打击等
  * 自0.6.9已部分实现

## 截屏

![截屏1](/demo/demo1.webp)
![截屏2](/demo/demo2.webp)
![截屏3](/demo/demo3.webp)
![截屏4](/demo/demo4.webp)
![截屏5](/demo/demo5.webp)
![截屏6](/demo/demo6.webp)
![截屏7](/demo/demo7.webp)
![截屏8](/demo/demo8.webp)
![截屏9](/demo/demo9.webp)
![截屏10](/demo/demo10.webp)
![截屏11](/demo/demo11.webp)
![截屏12](/demo/demo12.webp)
![截屏13](/demo/demo13.webp)