## Python版植物大战僵尸

植物大战僵尸游戏的Python实现，基于[marblexu的项目进行创作](https://github.com/marblexu/PythonPlantsVsZombies)，部分代码也整合自[callmebg的项目](https://github.com/callmebg/PythonPlantsVsZombies)

**本项目为个人python语言学习的练习项目，仅供个人学习和研究使用，不得用于其他用途。如果这个游戏侵犯了版权，请联系我删除**

* 已有的植物：向日葵，豌豆射手，坚果墙，寒冰射手，樱桃炸弹，双发射手，三线射手，大嘴花，小喷菇，土豆雷，地刺，胆小菇，倭瓜，火爆辣椒，阳光菇，寒冰菇，魅惑菇，火炬树桩，睡莲，杨桃，咖啡豆，海蘑菇，高坚果，缠绕水草，毁灭菇，墓碑吞噬者，大喷菇，大蒜，南瓜头
* 已有的僵尸：普通僵尸，旗帜僵尸，路障僵尸，铁桶僵尸，读报僵尸，橄榄球僵尸，鸭子救生圈僵尸，铁门僵尸，撑杆跳僵尸，冰车僵尸，潜水僵尸
* 使用JSON文件记录关卡信息数据
  * 在0.8.18.0及以后直接用python记录关卡的不可变数据，JSON目前仅用于用户存档
* 支持选择植物卡片
* 支持白昼模式，夜晚模式，泳池模式，浓雾模式（暂时没有加入雾），传送带模式和坚果保龄球模式
* 支持背景音乐播放
  * 支持调节音量
* 支持音效
  * 支持与背景音乐一起调节音量
* 支持全屏模式
  * 按`F`键进入全屏模式，按`U`键恢复至窗口模式
* 支持用小铲子移除植物
* 支持分波生成僵尸
* 支持“关卡进程”进度条显示
* 夜晚模式支持墓碑以及从墓碑生成僵尸
* 含有泳池的模式支持在最后一波时从泳池中自动冒出僵尸
* 支持保存进度
  * Windows下默认进度文件的保存路径为`~\AppData\Roaming\pypvz\userdata.json`
  * 其他操作系统为`~/.config/pypvz/userdata.json`
  * 存档为JSON文件，如果出现因存档损坏而造成程序无法启动，可以手动编辑修复或者删除该文件重试
    * 0.8.12.0版本后理论上不可能因为存档损坏而无法启动，如果有，请在[issues](https://github.com/wszqkzqk/pypvz/issues)中报告bug
      * 仍然有可能因为升级后变量名不同而丢失存档的进度信息，这种情况手动编辑恢复即可
* 支持错误日志记录
  * Windows下默认日志文件的保存路径为`~\AppData\Roaming\pypvz\run.log`
  * 其他操作系统为`~/.config/pypvz/run.log`
* 支持自定义游戏速度倍率
  * 保存在游戏存档文件中，可以通过修改`game rate`值更改速度倍率
* 游戏完成成就显示
  * 任意一游戏模式全部完成显示银向日葵奖杯
  * 所有模式全部完成显示金向日葵奖杯
  * 光标移动到向日葵奖杯上是显示当前各个模式通关次数
* 含有游戏帮助界面 QwQ

## 环境要求

* `Python3` （建议 >= 3.10，最好使用最新版）
* `Python-Pygame` （建议 >= 2.0，最好使用最新版）

## 开始游戏

### 使用仓库源代码

先克隆仓库内容，再运行`pypvz.py`：

```shell
git clone https://github.com/wszqkzqk/pypvz.git
cd pypvz
python pypvz.py
```

### 使用Windows可执行文件

下载`pypvz.exe`文件，双击运行即可
- 可以在仓库的[`Releases`](https://github.com/wszqkzqk/pypvz/releases)页面中[下载最新版（点击跳转）](https://github.com/wszqkzqk/pypvz/releases/latest)（推荐）：
  - 使用GCC编译
  - 程序包含名称、版本等信息
  - 得到的验证最多
  - 并非每次提交都会更新，更新可能不及时
- 也可以直接下载GitHub Workflow[自动利用Nuitka构建的版本（点击跳转）](https://github.com/wszqkzqk/pypvz/releases/tag/Latest)（推荐）：
  - 使用MSVC编译
  - 每次合并提交到主分支时更新
  - 得到的验证较多
  - 服务器构建，编译环境更纯粹，冗余更少，体积更小
- 还可以下载GitHub Workflow[自动利用Pyinstaller构建的版本（点击跳转）](https://github.com/wszqkzqk/pypvz/releases/tag/Current.Version.Built.with.Pyinstaller)：
  - 在程序闪退时有报错窗口弹出
  - 程序性能较差，不推荐
- 均仅支持64位操作系统
- 不依赖python、pygame等外部环境，开箱即用

### 使用Linux可执行文件

由于Linux几乎都标配了Python环境，因此本程序不太重视Linux下可执行的单文件的维护，因此没有手动构建版，只能下载自动构建的软件包。可以在仓库的[`Releases`](https://github.com/wszqkzqk/pypvz/releases)页面中[下载最新版（点击跳转）](https://github.com/wszqkzqk/pypvz/releases/latest)。

## 方法

* 使用鼠标收集阳光,种植植物
* 对于已经存在存档的用户，可以在`~\AppData\Roaming\pypvz\userdata.json`（Windows）或`~/.config/pypvz/userdata.json`（其他操作系统）中修改当前关卡：
  * 冒险模式：
    * 白昼模式——单行草皮：1
    * 白昼模式——三行草皮：2
    * 白昼模式：3~5
    * 夜晚模式：6~8
    * 泳池模式：9~11
    * 浓雾模式（暂时没有雾）：12
  * 小游戏模式：
    * 坚果保龄球：1
    * 传送带模式（白天）：2
    * 传送带模式（黑夜）：3
    * 传送带模式（泳池）：4
    * 坚果保龄球(II)：5
  * 目前暂时按照以上设定，未与原版相符
* 可以通过修改存档JSON文件中的`game rate`值来调节游戏速度倍率

## Windows单文件封装

### 使用Nuitka进行构建

编译依赖：
- `Python3` （建议 >= 3.10，最好使用最新版）
- `Python-Pygame` （建议 >= 2.0，最好使用最新版）
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
nuitka --mingw64 --standalone `
        --onefile `
        --show-progress `
        --show-memory `
        --output-dir=release `
        --windows-icon-from-ico=pypvz.ico `
        --include-data-dir=resources=resources `
        --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libogg-0.dll=libogg-0.dll `
        --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libopus-0.dll=libopus-0.dll `
        --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libopusfile-0.dll=libopusfile-0.dll `
        --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libvorbisfile-3.dll=libvorbisfile-3.dll `
        --include-data-file=C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\libvorbis-0.dll=libvorbis-0.dll `
        --lto=yes `
        --windows-disable-console `
        --windows-product-name=pypvz `
        --windows-company-name=wszqkzqk.dev `
        --windows-file-description="pypvz" `
        --windows-product-version=0.8.2.0 `
        pypvz.py
```

* 其中`C:\Users\17265\AppData\Local\Programs\Python\Python310\Lib\site-packages\pygame\xxx.dll`应当替换为`xxx.dll`实际所在路径，`--output-dir=`后应当跟实际需要输出的路径，绝对路径或者相对路径均可
* 由于仅复制了`opus`与`vorbis`的解码器，故要求所有背景音乐都要以opus或vorbis编码
* `--windows-product-version=`表示版本号信息，所跟内容格式必须为`x.x.x.x`
* 建议开启`--lto=yes`选项优化链接，如果编译失败可以关闭此选项

可执行文件生成路径为`./release/pypvz.exe`

如果只需要在本地生成编译文件测试，则只需要执行：

``` cmd
nuitka --mingw64 `
    --follow-imports `
    --show-progress `
    --output-dir=test-build `
    --windows-icon-from-ico=pypvz.ico `
    --windows-product-name=pypvz `
    --windows-company-name=wszqkzqk.dev `
    --windows-file-description=pypvz `
    --windows-disable-console `
    --windows-product-version=0.8.2.0 `
    pypvz.py
```

这样生成的程序只能在具有相同python环境的机器上运行

### 使用pyinstaller进行构建

- 由于pyinstaller构建的程序运行效率显著较nuitka构建的程序低下，并且程序体积也往往比nuitka构建的程序大，因此本项目并不推荐使用pyinstaller构建
- 但是因为pyinstaller直接封装了所导入的库中的全部内容，使用pyinstaller构建时不需要手动添加媒体解码库
- pyinstaller并没有涉及python源代码优化、C源代码生成以及C源代码编译链接过程，因此编译速度显著快于nuitka

编译依赖：
- `Python3` （建议 >= 3.10，最好使用最新版）
- `Python-Pygame` （建议 >= 2.0，最好使用最新版）
- `Pyinstaller`

编译参考命令：
``` cmd
pyinstaller -F pypvz.py `
                  --distpath ./release `
                  --noconsole `
                  --add-data="resources;./resources" `
                  --add-data="pypvz-exec-logo.png;./pypvz-exec-logo.png" `
                  -i ./pypvz.ico
```

可执行文件生成路径为`./release/pypvz.exe`

### 使用Github Workflow进行自动构建

直接复制本项目下的`.github/workflows`下的文件，进行少许改动即可满足大多数需求

## 已知bug

以下问题囿于个人目前的能力与精力，没有修复：
* 冷冻的僵尸未用蓝色滤镜标识
  * 这个想不到很好的实现方法，可能会想一种替代方案
* 魅惑的僵尸未用红色滤镜标识
  * 这个可能会作为一种“特性”
* 南瓜头显示不正常
* 墓碑吞噬者吞噬墓碑过程中被吞噬的墓碑顶端不会消失

**欢迎提供[Pull requests](https://github.com/wszqkzqk/pypvz/pulls)或修复方法建议，也欢迎在这里反馈新的bug()**

## ~~画大饼~~计划（不保证实施）

* 增加关卡进程进度条
  * 该功能自0.5.4已实现
* 增加保存数据文件以存储用户进度的功能
  * 该功能自0.8.0.0已实现
* 增加调整音量的功能
  * `pg.mixer.music.set_volume()`
  * 可以用`音量+`、`音量-`按钮实现
  * 注意字体颜色渲染
  * 该功能自0.8.14.0已实现
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
        * 自0.7.10.0起已实现
      * 圆形范围烟雾
    * 碾压
      * 倭瓜
        * 已实现
  * 爆炸
    * 一般爆炸
      * 樱桃炸弹、爆炸坚果与玉米加农炮炮弹
        * 已实现
      * 毁灭菇
        * 自0.7.6.0已实现
    * 火焰爆炸
      * 火爆辣椒
        * 已实现
    * 非灰烬类爆炸
      * 土豆雷
        * 已实现
  * 从地面刺伤
    * 已实现
  * 缠绕与拖拽
    * 自0.7.5.0已实现
    * 与原版有所区别，设定上秒杀任意僵尸
  * 吞噬
    * 已实现
    * 与原版有所区别，设定上秒杀任意僵尸
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
* 增加关卡前的本关僵尸预览
* 鼠标移动到植物上时显示部分信息，类似图鉴功能

## 截屏

![截屏1](/screenshots/screenshot-1.webp)
![截屏2](/screenshots/screenshot-2.webp)
![截屏3](/screenshots/screenshot-3.webp)
![截屏4](/screenshots/screenshot-4.webp)
![截屏5](/screenshots/screenshot-5.webp)
![截屏6](/screenshots/screenshot-6.webp)
![截屏7](/screenshots/screenshot-7.webp)
![截屏8](/screenshots/screenshot-8.webp)
![截屏9](/screenshots/screenshot-9.webp)
![截屏10](/screenshots/screenshot-10.webp)
![截屏11](/screenshots/screenshot-11.webp)
![截屏12](/screenshots/screenshot-12.webp)
![截屏13](/screenshots/screenshot-13.webp)
![截屏14](/screenshots/screenshot-14.webp)
![截屏15](/screenshots/screenshot-15.webp)
![截屏16](/screenshots/screenshot-16.webp)
![截屏17](/screenshots/screenshot-17.webp)
![截屏18](/screenshots/screenshot-18.webp)
![截屏19](/screenshots/screenshot-19.webp)
![截屏20](/screenshots/screenshot-20.webp)
![截屏21](/screenshots/screenshot-21.webp)
![截屏22](/screenshots/screenshot-22.webp)
![截屏23](/screenshots/screenshot-23.webp)

## 关于日志与反馈

对于闪退情况，Linux用户与Windows下的python源代码运行用户可以直接在终端中复制出崩溃日志进行反馈。

Windows单文件封装版本无法通过终端显示日志，需要在日志文件中寻找崩溃原因
* Windows默认日志文件路径为`~\AppData\Roaming\pypvz\run.log`
* 其他操作系统为`~/.config/pypvz/run.log`，但一般可以在终端中显示时用终端中的输出即可
