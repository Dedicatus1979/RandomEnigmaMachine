# -*- coding:utf-8 -*-
# @Time : 2021/12/27 下午 7:15
# @Author : Dedicatus1979
# @File : enigma.py
# @Software : PyCharm

"""一个模拟三转子恩尼格玛机的程序V2.0，
本程序可以直接交互式使用，也可非交互式使用。
本程序提供两种恩尼格玛机的类型，一种加密范围为26罗马字母（经典模式），另一种的范围是ASCII（非经典模式）。在加密范围外的字符将不被加密。
在经典模式下，大小写不敏感且结果一律为大写字母。非经典模式下，为了防止空格间的混淆，' '(Space 32)将会被替换为'_'(Underline 95)。
因为修改了转子定义的缘故，本版本的加密后的文本与旧版本不兼容！！！（即相等配置下，新老版本加密出来的内容不同！！！）
以下是使用方法的简要说明：
非即时交互模式：
1: import enigma as enm   # 若直接从本程序中使用，则忽略此句，但建议使用另一个文件，将此文件作为包导入。
2: enm.setting(114514, False)  # setting中是用于设置主要信息的，114514设置的是种子，种子可以是任意非0的整数，False代表非经典模式。
3: enm.setSite(1, 1, 4)     # 设置码盘位置，也可直接在setting中设置。
4: text = r'''Hello world!!!''' # 设置想要加密的内容，推荐在ascii模式下使用ascii内的字母，经典模式下同理，使用r与三引号是为了防止出现奇奇怪怪的问题
5: cipher = enm.run(text)
6: print(cipher)
以上结果：
rm[(h*|^mTU{C%          逆推结果：Hello_world!!!
-*-------------------*----------------------*-
即时交互模式：（此模式请直接使用此文件）
1: # 当前恩尼格玛机的种子为 114514，码盘位置为：(0, 0, 0)，模式为经典模式。
2: # 可以通过"/help"获取更多信息。     # /**可以表示输入指令。
3: :-> Hello World!!!               # 自行输入，':->'即表示用户输入
4: FWHMS OYPGG!!!                   # 系统返回的加密值。
5: # 当前码盘位置为： (0, 0, 10)        # 系统返回的当前码盘值
6: :-> /site(0,0,0)           # 使用site指令修改码盘值，若需要在开头输入"/"则需要输入"//"(仅开头需要，若在文本内部，则不需要双写)
7: -------------------------------          # 使用指令后会显示分割线。
8: # 当前码盘位置为： (0, 0, 0)
9: :-> /swap('l','o')               # 调换字母指令，即类似于实际恩尼格玛机的接线板的作用，详细信息请查看setSwap函数的文档。
10: # 当前交换组为： [('L', 'O')]
11: -------------------------------
12: # 当前码盘位置为： (0, 0, 0)
13: :-> Hello World!!!
14: FWZPU LFPAG!!!
15: # 当前码盘位置为： (0, 0, 10)
16: :->
-*-------------------*----------------------*-
Ps；依旧强烈建议使用者阅读一下'Rotor.__address_to_disc_in()'方法的文档，这个文档解释了最核心的模拟码盘旋转的原理与实现。（而且解释的更详细了）
更多关于更新的内容请查看__update__
2021-12-30
@ Dedicatus1979
@ Python 3.10"""

__version__ = 2.0
__function__ = ['setting', 'setSite', 'getSite', 'isClassical', 'setSwap', 'getSwap', 'clearSwap', 'setGroupSwap',
                'deleteGroupSwap', 'run', 'getSeed', 'swap', 'site', 'help']
__update__ = """V2.0更新说明：
    1.添加了交换字母的功能，此功能是用于模拟恩尼格玛机的接线板功能。
    2.本次更新除了核心代码，如转子的实现没有修改外，全部都重写了一遍，相比于之前版本也优化了不少的地方。
    3.简化了使用方法，使其更适合面向人类。
    4.优化了所有接口函数的文档与数据类型，其中deleteGroupSwap(group)函数为了向低版本兼容，没有写作deleteGroupSwap(group:list|tuple)，但在文档中写明了接收数据的类型。
    5.在交互模式下添加了使用函数的功能。
    6.修改了转子的定义，由先前的(0, 1, 2)分别对应恩尼格玛机的右码盘，中码盘，左码盘改为了对应恩尼格玛机的左码盘，中码盘，右码盘。使其更符合人类直觉而非Python的直觉。
    7.正因修改了转子的定义，导致此版本与旧版本的加密后的文本不一致。
    8.移除了在非交互式模式下使用交互模式的方法，因为没有意义。
    9.移除了"码盘值在输入超过93或25的数值时自动转换为93或25以内的数字"的特性，因为不符合人类直觉，一个码盘最大只有93，怎么可能会有94呢？
    10.替代"码盘值在输入超过93或25的数值时自动转换为93或25以内的数字"的特性的特性是：当输入超过最大值后直接报错。
    11.因为取消了"码盘值在输入超过93或25的数值时自动转换为93或25以内的数字"的特性，导致从ascii模式转换为经典模式后码盘依旧停留在ascii模式上。
    12.解决"从ascii模式转换为经典模式后码盘依旧停留在ascii模式上"的bug的方法是：每次设定（setting）修改模式时，若未指定转子位置，则默认为(0,0,0)。
# ------------------
历史版本：
V1.2 2021-11-5      更新说明：略
v1.1 2021-11-4      更新说明：略"""

import random


def setting(seed: int, classical=False, code_site: tuple = (0, 0, 0)):
    """setting(seed: int, classical=False, code_site: tuple=(0, 0, 0)),
    本函数用于定义恩尼格玛机的初始设定，其包括种子seed，码盘位置code_site以及是否为经典模式classical，
    seed: 本恩尼格玛机的随机种子，即类似于恩尼格玛的生产批次与型号，同一个种子的恩尼格玛机转子内部接线相同。
    classical: 本恩尼格玛有两个工作模式，一个为经典模式True，还有一个为非经典模式False，在经典模式下，只有26个字母会被加密，而在非经典模式下，加密范围扩充到整个ascii。
    code_site: 恩尼格玛机的转子位置，恩尼格玛从左往右三个转子编号分别为0，1，2。转子的位置取值范围与当前恩尼格玛的工作模式有关。"""
    if classical:
        Ro.disc_num = 26
    else:
        Ro.disc_num = 94
    if (index := len(code_site)) != 3:
        raise Exception('The values quantity of "code_site" must 3. "code_site"内只能有3个值。')
    for i in range(index):
        if code_site[i] >= Ro.disc_num:
            raise Exception('The index %d of "code_site" is out of the range. "code_site"的第 %d 位超出了最大范围。' % (i, i))
    Ro.code_site = list(code_site)
    Ro.create_setting(seed)
    Ro.seed = seed
    return [getSeed(), isClassical(), getSite()]


def setSite(site0: int, site1: int, site2: int):
    """setSite(site0: int, site1: int, site2: int),
    本函数用于定义恩尼格玛机的转子位置，按转子左中右的顺序写入转子左中右当前的值。
    例如希望将转子拨到(1, 1, 4)的位置，
    则输入: setSite(1, 1, 4)
    即可。输入值不能大于转子最大值
    """
    site = (site0, site1, site2)
    for i in range(3):
        if site[i] >= Ro.disc_num:
            raise Exception('The index %d of "site" is out of the range. "site"的第 %d 位超出了最大范围。' % (i, i))
    Ro.code_site = list(site)
    return getSite()


def getSite() -> tuple:
    """getSite() -> tuple,
    本函数用于获取当前恩尼格玛机的转子位置，顺序为转子0，1，2 左中右"""
    return tuple(Ro.code_site)


def isClassical() -> bool:
    """isClassical() -> bool,
    本函数的返回值表示是否为经典模式，例如返回True，即表示当前为经典模式"""
    if Ro.disc_num == 26:
        return True
    else:
        return False


def setSwap(beswap: str, swap: str):
    """setSwap(beswap: str, swap: str),
    本函数用于设置交换的字母，其模拟的是恩尼格玛机的电线。
    本函数仅支持交换26字母，不支持整个ascii，且最多交换6组字母。
    beswap: 被交换的字母
    swap: 与被交换字母交换的字母"""
    if not (len(beswap) == 1 and beswap.isalpha() and len(swap) == 1 and swap.isalpha()):
        raise Exception('The "swap" and "beswap" must be an alpha and only one. "swap"与"beswap"必须且只能有一个字母。')
    if (beswap.upper() in En.swap[0]) or (swap.upper() in En.swap[0]):
        raise Exception('The alpha have been swapped. 字母已经被交换过了。')
    if len(En.swap[0]) < 12:
        En.swap[0] += [beswap.upper(), swap.upper()]
        En.swap[1] += [swap.upper(), beswap.upper()]
    else:
        raise Exception('There are already 6 "swap groups". 已有6组交换组了。')
    return getSwap()


def getSwap() -> list:
    """getSwap() -> list,
    本函数以列表形式返回当前交换的字母，例如返回：
    [('a','c'), ('d','b')]
    即表示本恩尼格玛机有两组交换值，一组为'a'与'c'，一组为'b'与'd'，最多支持6组字母交换。"""
    swaplist = []
    for i in range(int(len(En.swap[0]) / 2)):
        swaplist.append((En.swap[0][2 * i], En.swap[0][2 * i + 1]))
    return swaplist


def clearSwap():
    """clearSwap(),
    本函数将所有已创建的字母交换值清空，即清空getSwap()中的内容。"""
    En.swap = [[], []]
    return getSwap()


def setGroupSwap(group: list):
    """setGroupSwap(group: list),
    本函数为setSwap()的组函数版，可以一次性交换多组字母，其参数group需要一个列表list，其格式为：
    [('a','c'), ['b','d']]，一个大的列表中套最多6个小列表或元组，一个列表或元组表示的便是其中的两个字母交换了。
    交换的字母组总数为6，包括setSwap()中设定的。"""
    if len(group) >= 6:
        raise Exception('The maximum size of "group" is 6. "group"最大为6。')
    if len(En.swap[0]) + 2 * len(group) > 12:
        raise Exception('The total of "swap group" will be greater than 6. "swap group"的总数将会超过6。')
    for i in group:
        setSwap(i[0], i[1])
    return getSwap()


def deleteGroupSwap(group):
    """deleteGroupSwap(group: list | tuple),
    删除一组交换字母，一组内可以有多组不同的交换字母，例如：[('a','c'), ['b','d']]
    也可以只有一个，当只有一个时，可以直接以一个元组的形式输入，例如：[('a','c')]或('a','c')。"""
    if isinstance(group, tuple) and len(group) == 2:
        for i in group:
            En.swap[0].remove(i.upper())
            En.swap[1].remove(i.upper())
    elif isinstance(group, list):
        for i in group:
            for j in i:
                En.swap[0].remove(j.upper())
                En.swap[1].remove(j.upper())
    else:
        raise Exception('Format error. 格式错误。')
    return getSwap()


def run(text: str) -> str:
    """run(text: str) -> str,
    本函数用于输入需要加密的文字，输入类型应该为字符串。以及返回加密后的文字，输出为字符串。"""
    if Ro.disc_num == 45:
        raise Exception('Have not setting. 没有进行设置。')
    return En.outText(text)


def getSeed() -> int:
    """getSeed() -> int,
    本函数用于返回当前恩尼格玛机的种子"""
    return Ro.seed


def swap(beswap: str, swap: str):
    """swap(beswap: str, swap: str),
    本函数与setSwap()函数功能相同，建议在交互模式下使用本函数，在其余模式下使用setSwap函数"""
    return setSwap(beswap, swap)


def site(site0: int, site1: int, site2: int):
    """site(site0: int, site1: int, site2: int),
    与setSite()函数功能一样，建议在交互模式下使用本函数，在其余模式下使用setSite函数"""
    return setSite(site0, site1, site2)


def help(*args) -> str:
    """help(*args) -> str,
    本函数用于帮助使用者了解函数的使用方法，
    help('all')将会返回所有可以使用help函数的函数名，
    help('doc')将会返回本文件的系统文档，
    help('**')help内输入一个字符串将会返回这个函数的使用方法。"""
    if not args:
        return help.__doc__
    elif len(args) == 1 and args[0] == 'all':
        return str(__function__)
    elif len(args) == 1 and args[0] == 'doc':
        return __doc__
    elif len(args) == 1 and args[0] in __function__:
        return eval(args[0]).__doc__
    else:
        return 'Undefined function. 未定义函数。'


class Rotor(object):
    """这个是恩尼格玛机的转子部分"""

    def __init__(self):
        """用于模拟转子所必须的参数与内容"""
        self.seed = 114514
        self.disc_num = 45
        self.code_site = [0, 0, 0]
        self.__disc_0 = ''
        self.__disc_1 = ''
        self.__disc_2 = ''
        self.__disc_re = ''

    def create_setting(self, seed):
        """用于创建初始设定，反射板与转子"""
        seeds = self.__create_seeds(seed)
        self.__disc_0 = self.__create_disc(seeds[0])
        self.__disc_re = self.__create_disc_re(seeds[1])
        self.__disc_2 = self.__create_disc(seeds[2])
        self.__disc_1 = self.__create_disc(seeds[3])

    def cipher(self, address_in):
        """这个方法即是整个转子组，也就是加密的主函数，输入一个字母的位置，输出其通过三个转子，一个反射板后的字母位置"""
        disc2_out = self.__address_to_address(address_in, self.code_site[2], self.__disc_2)
        disc1_out = self.__address_to_address(disc2_out, self.code_site[1], self.__disc_1)
        disc0_out = self.__address_to_address(disc1_out, self.code_site[0], self.__disc_0)
        disc_re_out = self.__address_to_address(disc0_out, 0, self.__disc_re)
        disc0_in = self.__address_to_address(disc_re_out, self.code_site[0], self.__disc_0)
        disc1_in = self.__address_to_address(disc0_in, self.code_site[1], self.__disc_1)
        disc2_in = self.__address_to_address(disc1_in, self.code_site[2], self.__disc_2)
        return disc2_in

    def accumulator(self):
        """一个累加器，用于每加密完一个字母后进行的拨动码盘的操作，顺带进个位"""
        carry_0 = (self.code_site[2] + 1) // self.disc_num
        carry_1 = (self.code_site[1] + carry_0) // self.disc_num
        self.code_site[2] = (self.code_site[2] + 1) % self.disc_num
        self.code_site[1] = (self.code_site[1] + carry_0) % self.disc_num
        self.code_site[0] = (self.code_site[0] + carry_1) % self.disc_num

    def __create_seeds(self, seed):
        """将初始的随机数种子扩充为标准长度（10位）的随机数种子以及再生成四个种子
        基本原理：将最初始的seed作为随机数种子，从[0，1)中随机一个数，将这个数乘以1e10，再将最初始的seed乘上这个数值，取最后10位，
        若不满10位，则再次进行上述操作。其余的随机数种子的原理类似。"""
        if seed == 0:
            raise Exception('Seed must not 0. 种子不能为0。')
        seeds = []
        random.seed(seed)
        rate = int(random.random() * 1e10)
        while abs(seed) < 1e10:
            seed *= rate
        new_seed = int(seed % 1e10)
        for i in range(4):
            random.seed(new_seed)
            new_seed *= int(random.random() * 1e10)
            new_seed = int(new_seed % 1e10)
            seeds.append(new_seed)
        return seeds

    def __create_disc(self, seed):
        """输入种子，用于生成码盘
        基本原理：生成一个乱序的列表与字典，循环code_disc_num次，如果字典的第[i]与字典的第[x[-1]]同时为空，
        则将x[-1]与i同时赋值给字典第[i]与字典第[x[-1]]，同时从列表中删除这两个值。"""
        random.seed(seed)
        code_disc = {key: '' for key in range(self.disc_num)}
        random.shuffle(x := [i for i in range(self.disc_num)])
        for i in range(self.disc_num):
            if code_disc[i] == '' and code_disc[x[-1]] == '':
                code_disc[i], code_disc[x[-1]] = x[-1], i
                if i == x[-1]:
                    x.pop()
                else:
                    x.pop()
                    x.remove(i)
        return code_disc

    def __create_disc_re(self, seed):
        """输入种子，生成一个反射板的实例
        基本原理与生成码盘的基本相同，但反射板不能出现键值对中键与值相同的情况，所以加了一条，如果相同的话，那就将x[-1]与x[0]交换，
        这样就能保证在所有键值对非空的情况下，每个键值对中，键与值的值不同。"""
        random.seed(seed)
        code_disc_re = {key: '' for key in range(self.disc_num)}
        random.shuffle(x := [i for i in range(self.disc_num)])
        for i in range(self.disc_num):
            if code_disc_re[i] == '' and code_disc_re[x[-1]] == '':
                if i == x[-1]:
                    x[-1], x[0] = x[0], x[-1]
                code_disc_re[i], code_disc_re[x[-1]] = x[-1], i
                x.pop()
                x.remove(i)
        return code_disc_re

    def __address_to_disc_in(self, address, stir):
        """在拨动stir次后码盘输入端口处的位置与输入端口的映射，以下是对码盘与位置的详细解释：
        假设有一个四码位的码盘(code)。输入的每个字符的位置(address)是恒定的，例如'A'对应位置0，'B'对应位置1，
        码盘上有8个端口，一端输入(in)，一端输出(out)，假设端口间的映射关系是i0->o1，i1->o0，i2->o3，i3->o2，
        再假设初始阶段，即码盘转动0次的时候，位置0对应的端口是i0，位置1对应的端口是i1，位置2对应的端口的是i2。则，转动四次的的所有情况如下：
        转动次数:            0             1             2               3               4
            字母所在的位置：[0,1,2,3]   ->[0,1,2,3]    ->[0,1,2,3]     ->[0,1,2,3]      ->[0,1,2,3]     ->
         字母所对应的i端口：[0,1,2,3]   ->[1,2,3,0]    ->[2,3,0,1]     ->[3,0,1,2]      ->[0,1,2,3]     ->
        i端口所对应的o端口：[1,0,3,2]   ->[0,3,2,1]    ->[3,2,1,0]     ->[2,1,0,3]      ->[1,0,3,2]     ->
          o端口所在的位置：[1,0,3,2]   ->[3,2,1,0]    ->[1,0,3,2]     ->[3,2,1,0]      ->[1,0,3,2]     ->
        通过上表可以归纳总结出下方公式，而下方公式也就是实现通过输入码盘、码盘转动次数、字母的位置、
        得出映射(reflect)转换后的位置，以便给下一个码盘使用的方法。（好长的定语...其实我自己都快读不懂什么意思了...）
        V2.0版本新加注释：将一个码盘转子看作三个部分，第一个部分是"将字母映射到转子输入"记作fx；第二个部分是"转子内部的接线"，即将一个字母映射为另一个字母
        也就是输入至输出的映射，将这个部分记作gx；第三个部分便是"将转子输出映射回字母"，这个字母与fx中的字母不是同一个字母，这里的字母更多的指的是一个地址，
        将其记作hx（上面那一段中的"字母"两字出现了多次的词义变换，下面的解释应该更好一点）。
        依旧以上文的表格为例，假设现在转子转动了2次，假设地址为0的字母是A，1的字母为B。现在我们输入了A，A经过fx将字母的地址映射到转子的输入，也就是f(0)=2。
        此时，我们输入的字母为"A"，其所触发的是转子的2号端口。现在经过转子的内部接线，将转子的输入映射到输出，即g(2)=3。此时，我们输入的端口为2，输出的端口为3。
        转子的输出同样存在有一个位置，这个位置与输出口间的映射就是hx，即h(3)=1。此时，表明的含义是输出口2所在的位置是1，即字母B。其整个过程的含义便是三个映射的复合，
        即：h( g( f(A) ) ) = B。"""
        disc_in = (address + stir % self.disc_num) % self.disc_num
        return disc_in

    def __disc_out_to_address(self, disc_out, stir):
        """内部方法，在拨动stir次后码盘输处端口与输出端口处的位置的映射。原理同上
        即，本方法就是所谓的hx。gx在哪里？gx就是self.__disc_1、2、3、re这四个。"""
        address = (disc_out - stir % self.disc_num) % self.disc_num
        return address

    def __address_to_address(self, address, stir, code_disc):
        """这个方法就是：h( g( f(A) ) )，code_disc是一个字典，也就是self.__disc_1、2、3、re这四个。
        输入一个地址，输出一个地址。"""
        disc_in = self.__address_to_disc_in(address, stir)
        disc_out = code_disc[disc_in]
        address = self.__disc_out_to_address(disc_out, stir)
        return address


class Enigma(object):
    """这个是恩尼格玛机的除转子外的主体部分。"""

    def __init__(self):
        """用于模拟一台恩尼格玛机所必要的参数与内容"""
        self.swap = [[], []]
        self.__alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.__ascii = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''

    def __ischr(self, chr):
        """用于判定本字符是否需要被加密"""
        inalpha = chr in self.__alphabet
        inascii = chr in self.__ascii
        if Ro.disc_num == 94 and inascii:
            return True
        elif Ro.disc_num == 26 and inalpha:
            return True
        else:
            return False

    def __encryption(self, chra):
        """将字符加密用的方法"""
        if Ro.disc_num == 94:
            asc = 95 if ord(chra) == 32 else ord(chra)
            out_asc = Ro.cipher(asc - 33) + 33
            return chr(out_asc)
        else:
            asc = ord(chra.upper())
            out_asc = Ro.cipher(asc - 65) + 65
            return chr(out_asc)

    def __swapchr(self, beswap):
        """将字符交换用的方法"""
        if beswap.upper() in self.swap[0]:
            replace = self.swap[1][self.swap[0].index(beswap.upper())]
            if beswap.upper() == beswap:
                return replace
            else:
                return replace.lower()
        else:
            return beswap

    def outText(self, text):
        """将字符加密为另一串字符并输出"""
        out_char = ''
        textlist = list(text)
        for i in textlist:
            if self.__ischr(i):
                i = self.__swapchr(i)
                cha = self.__encryption(i)
                Ro.accumulator()
                cha = self.__swapchr(cha)
                out_char += cha
            else:
                out_char += i
        return out_char


class Interactive(object):
    """这个是用来实时交互时使用的类。主要用于处理实时情况下的指令信息。"""
    def __init__(self):
        self.text = ''
        self.__key = 'wap'
        self.__fuc_low = ['setting', 'setsite', 'getsite', 'isclassical', 'setswap', 'getswap', 'clearswap',
                          'setgroupswap', 'deletegroupswap', 'run', 'getseed', 'swap', 'site', 'help']

    def handle_text(self,text):
        """用于在交互模式下输入text"""
        self.text = text
        if self.__isdef():
            return self.__dodef()
        else:
            return run(self.text)

    def __isdef(self):
        """判读输入信息是否为函数"""
        if self.text[0] == '/' and self.text[1] != '/':
            self.text = self.text[1:]
            return True
        elif self.text[0] == '/' and self.text[1] == '/':
            self.text = self.text[1:]
            return False
        else:
            return False

    def __dodef(self):
        """执行函数的方法"""
        fuc = self.text.split('(', 1)
        if fuc[0].lower() not in self.__fuc_low:
            return 'Undefined function. 未定义函数。'
        try:
            if fuc[0] == 'run':
                print('Can not use "run". 不能使用"run"。')
            else:
                if len(fuc) == 1:
                    out = eval(__function__[self.__fuc_low.index(fuc[0].lower())] + '()')
                    self.__isprint(out, fuc[0])
                else:
                    out = eval(__function__[self.__fuc_low.index(fuc[0].lower())] + '(' + fuc[1])
                    self.__isprint(out, fuc[0])
        except:
            return 'Function format error. 函数格式错误。'
        else:
            return '-------------------------------'

    def __isprint(self, out, fuc):
        """设置执行完函数后的返回。"""
        if isinstance(out, bool):
            if out:
                print('# 当前为经典模式。')
            else:
                print('# 当前为ASCII模式。')
        if isinstance(out, int) and not isinstance(out, bool):
            print('# 当前系统种子为：', out)
        if isinstance(out, str):
            print('#', out)
        if fuc == 'setting':
            print('# 当前系统种子为：', out[0], '，', end='')
            print('码盘值为：', out[2], '，', end='')
            if out[1]:
                print('经典模式。')
            else:
                print('ASCII模式。')
        if self.__key in fuc:
            print('# 当前交换组为：', out)


Ro = Rotor()
En = Enigma()

if __name__ == '__main__':
    In = Interactive()
    setting(114514, True, (0, 0, 0))
    print('# 当前恩尼格玛机的种子为 114514，码盘位置为：(0, 0, 0)，模式为经典模式。')
    print('# 可以通过"/help"获取更多信息。')
    while True:
        out = In.handle_text(input(':-> '))
        print(out)
        print('# 当前码盘位置为：', getSite())
