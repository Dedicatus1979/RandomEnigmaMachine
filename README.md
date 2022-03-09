# RandomEnigmaMachine
A simple pseudorandomness rotors Enigma machine with Python.    一个简易的使用Python编写的伪随机转子恩尼格玛机
这是一个模拟伪随机转子的三转子恩尼格玛机的程序
本程序可以直接交互式使用，也可非交互式使用。
本程序提供两种恩尼格玛机的类型，一种加密范围为26罗马字母（经典模式），另一种的范围是ASCII（非经典模式）。在加密范围外的字符将不被加密。
在经典模式下，大小写不敏感且结果一律为大写字母。非经典模式下，为了防止空格间的混淆，' '(Space ASCII 32)将会被替换为'_'(Underline ASCII 95)。
