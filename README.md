# RandomEnigmaMachine
A simple pseudorandomness rotors Enigma machine with Python.    一个简易的使用Python编写的伪随机转子恩尼格玛机

这是一个模拟伪随机转子的三转子恩尼格玛机的程序，
本程序可以作为小程序直接运行交互式使用，也可作为库导入非交互式使用。

本程序可通过修改随机数生成种子来达到修改转子内部接线的功能，故本程序模拟的恩尼格玛机*与实际的恩尼格玛机加密结果完全不同*。

本程序提供两种恩尼格玛机的类型，一种加密范围为26罗马字母（经典模式），另一种的范围是ASCII（ASCII模式）。在加密范围外的字符将不被加密。

在经典模式下，大小写不敏感且结果一律为大写字母。非经典模式下，为了防止空格间的混淆，" "(Space ASCII 32)将会被替换为"_"(Underline ASCII 95)。

## 简易使用方法说明
非交互模式：
```
import enigma as enm          # 建议将此文件作为包导入。
enm.setting(114514, False)    # setting中是用于设置主要信息的，114514设置的是种子，种子可以是任意非0的整数，False代表非经典模式。
enm.setSite(1, 1, 4)          # 设置码盘位置，也可直接在setting中设置。
text = r'''Hello world!!!'''  # 设置想要加密的内容，推荐在ascii模式下使用ascii内的字母，经典模式下同理，使用r与三引号是为了防止出现奇奇怪怪的问题
cipher = enm.run(text)
print(cipher)
```
以上返回：“rm[(h*|^mTU{C%”

### 函数功能说明
| 函数         |    函数说明            |
| ----------   | -------------- |
| setting      | 定义初始设定，其包括种子seed，码盘位置code_site以及是否为经典模式classical |
| setSite      | 设置转子位置，按转子左中右的顺序写入转子码盘左中右当前的值         |
| getSite      | 返回当前的转子位置，顺序为转子0，1，2 左中右 |
| isClassical  | 返回是否为经典模式，True表示经典模式 |
| getSeed      | 返回当前的随机数种子 |
| setSwap      | 设置交换的字母，其模拟的是恩尼格玛机的接线板 |
| getSwap      | 以列表形式返回当前交换的字母  |
| clearSwap    | 将所有已创建的字母交换值清空  |
| setGroupSwap | setSwap的组函数版，可以一次性交换多组字母    |
| deleteGroupSwap | 删除一组交换字母，一组内可以有多组不同的交换字母 |
| swap | 与setSwap函数功能相同，建议在交互模式下使用本函数，在其余模式下使用setSwap函数 |
| site | 与setSite函数功能一样，建议在交互模式下使用本函数，在其余模式下使用setSite函数 |
| run  | 输入需要加密的文字，以及返回加密后的文字 |
| help | 用于帮助使用者了解函数的使用方法 |
