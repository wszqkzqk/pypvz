## Python版植物大战僵尸

植物大战僵尸游戏的Python实现
  
`仅供个人学习和非商业用途。如果这个游戏侵犯了版权，请告诉我`
  
* 已有的植物：向日葵，豌豆射手，坚果墙，寒冰射手，樱桃炸弹，三线射手，大嘴花，小喷菇，土豆雷，地刺，胆小菇，倭瓜，火爆辣椒，阳光菇，寒冰菇，魅惑菇
* 已有的僵尸：普通僵尸，旗帜僵尸，路障僵尸，铁桶僵尸，读报僵尸
* 使用 JSON 格式的文件存储进度数据 (例如僵尸出现的位置和时间，背景信息)
* 支持选择植物卡片
* 支持白昼模式，夜晚模式，传送带模式和坚果保龄球模式

## 环境要求

* Python >= 3.7 
* Python-Pygame >= 1.9

## 开始游戏

### 使用仓库源代码

```shell
python main.py
```

## 方法

* 使用鼠标收集阳光,种植植物。
* 你可以通过更改 source/constants.py 中的 START＿LEVEL＿NUM 的数值来更改起始关卡：
  * 1 和 2：白昼模式
  * 3：夜晚模式
  * 4：传送带模式
  * 5：坚果保龄球模式
* **注意：目前单文件发布版本不支持自定义调整关卡**

## Windows单文件封装

先在仓库所在文件夹执行：

``` powershell
nuitka --mingw --standalone --onefile --show-progress --show-memory --output-dir=out --windows-icon-from-ico=out/pypvz.ico main.py
```

再及时在单文件编译前于同一文件夹中执行（注意执行时间也不要早于Nuitka解析文件结构开始时间）：

``` powershell
mkdir out\main.dist\pygame
mkdir out\main.dist\source
ln out\freesansbold.ttf out\main.dist\pygame\freesansbold.ttf
New-Item -Path out\main.dist\resources -ItemType Junction -Value resources
New-Item -Path out\main.dist\source\data -ItemType Junction -Value source\data
```

## 截屏

![截屏1](/demo/demo1.webp)
![截屏2](/demo/demo2.webp)
![截屏3](/demo/demo3.webp)
