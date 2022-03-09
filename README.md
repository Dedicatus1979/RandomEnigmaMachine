# RandomEnigmaMachine
A simple pseudorandomness rotors Enigma machine with Python.    一个简易的使用Python编写的伪随机转子恩尼格玛机

这是一个模拟伪随机转子的三转子恩尼格玛机的程序，
本程序可以作为小程序直接运行交互式使用，也可作为库导入非交互式使用。

本程序可通过修改随机数生成种子来达到修改转子内部接线的功能，故本程序模拟的恩尼格玛机*与实际的恩尼格玛机加密结果完全不同*。

本程序提供两种恩尼格玛机的类型，一种加密范围为26罗马字母（经典模式），另一种的范围是ASCII（ASCII模式）。在加密范围外的字符将不被加密。

在经典模式下，大小写不敏感且结果一律为大写字母。非经典模式下，为了防止空格间的混淆，" "(Space ASCII 32)将会被替换为"_"(Underline ASCII 95)。

## 程序函数说明
| 函数     |    函数说明            |
| ---------- | -------------- |
| setting    | 用于定义恩尼格玛机的初始设定，其包括种子seed，码盘位置code_site以及是否为经典模式classical |
| database   | 数据库         |
| collection | 数据表         |
| path       | 下载的色图路径 |
| APPKEY     | 腾讯ai的appkey |
| APPID      | 腾讯ai的appid  |
| username   | pixiv的用户名  |
| password   | pixiv的密码    |
