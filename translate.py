import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, TypeVar, Callable, Type, cast
import pymongo


player_id = 10003
HSRScanData_file_path= r"test/json1/HSRScanData.json"
# 链接本地mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
# 数据库
db = client['lunarcore']
# 集合
collection_item = db['items']
collection_avatar = db['avatars']




T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Skills:
    basic: int
    skill: int
    ult: int
    talent: int

    @staticmethod
    def from_dict(obj: Any) -> 'Skills':
        assert isinstance(obj, dict)
        basic = from_int(obj.get("basic"))
        skill = from_int(obj.get("skill"))
        ult = from_int(obj.get("ult"))
        talent = from_int(obj.get("talent"))
        return Skills(basic, skill, ult, talent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["basic"] = from_int(self.basic)
        result["skill"] = from_int(self.skill)
        result["ult"] = from_int(self.ult)
        result["talent"] = from_int(self.talent)
        return result


@dataclass
class Character:
    key: str
    level: int
    ascension: int
    eidolon: int
    skills: Skills
    traces: Dict[str, bool]

    @staticmethod
    def from_dict(obj: Any) -> 'Character':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        level = from_int(obj.get("level"))
        ascension = from_int(obj.get("ascension"))
        eidolon = from_int(obj.get("eidolon"))
        skills = Skills.from_dict(obj.get("skills"))
        traces = from_dict(from_bool, obj.get("traces"))
        return Character(key, level, ascension, eidolon, skills, traces)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["level"] = from_int(self.level)
        result["ascension"] = from_int(self.ascension)
        result["eidolon"] = from_int(self.eidolon)
        result["skills"] = to_class(Skills, self.skills)
        result["traces"] = from_dict(from_bool, self.traces)
        return result


@dataclass
class LightCone:
    key: str
    level: int
    ascension: int
    superimposition: int
    location: str
    lock: bool
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'LightCone':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        level = from_int(obj.get("level"))
        ascension = from_int(obj.get("ascension"))
        superimposition = from_int(obj.get("superimposition"))
        location = from_str(obj.get("location"))
        lock = from_bool(obj.get("lock"))
        id = from_str(obj.get("_id"))
        return LightCone(key, level, ascension, superimposition, location, lock, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["level"] = from_int(self.level)
        result["ascension"] = from_int(self.ascension)
        result["superimposition"] = from_int(self.superimposition)
        result["location"] = from_str(self.location)
        result["lock"] = from_bool(self.lock)
        result["_id"] = from_str(self.id)
        return result


@dataclass
class Substat:
    key: str
    value: float

    @staticmethod
    def from_dict(obj: Any) -> 'Substat':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        value = from_float(obj.get("value"))
        return Substat(key, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["value"] = to_float(self.value)
        return result


@dataclass
class Relic:
    set: str
    slot: str
    rarity: int
    level: int
    mainstat: str
    substats: List[Substat]
    location: str
    lock: bool
    discard: bool
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Relic':
        assert isinstance(obj, dict)
        set = from_str(obj.get("set"))
        slot = from_str(obj.get("slot"))
        rarity = from_int(obj.get("rarity"))
        level = from_int(obj.get("level"))
        mainstat = from_str(obj.get("mainstat"))
        substats = from_list(Substat.from_dict, obj.get("substats"))
        location = from_str(obj.get("location"))
        lock = from_bool(obj.get("lock"))
        discard = from_bool(obj.get("discard"))
        id = from_str(obj.get("_id"))
        return Relic(set, slot, rarity, level, mainstat, substats, location, lock, discard, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["set"] = from_str(self.set)
        result["slot"] = from_str(self.slot)
        result["rarity"] = from_int(self.rarity)
        result["level"] = from_int(self.level)
        result["mainstat"] = from_str(self.mainstat)
        result["substats"] = from_list(lambda x: to_class(Substat, x), self.substats)
        result["location"] = from_str(self.location)
        result["lock"] = from_bool(self.lock)
        result["discard"] = from_bool(self.discard)
        result["_id"] = from_str(self.id)
        return result


@dataclass
class HsrScanData:
    source: str
    version: int
    light_cones: List[LightCone]
    relics: List[Relic]
    characters: List[Character]

    @staticmethod
    def from_dict(obj: Any) -> 'HsrScanData':
        assert isinstance(obj, dict)
        source = from_str(obj.get("source"))
        version = from_int(obj.get("version"))
        light_cones = from_list(LightCone.from_dict, obj.get("light_cones"))
        relics = from_list(Relic.from_dict, obj.get("relics"))
        characters = from_list(Character.from_dict, obj.get("characters"))
        return HsrScanData(source, version, light_cones, relics, characters)

    def to_dict(self) -> dict:
        result: dict = {}
        result["source"] = from_str(self.source)
        result["version"] = from_int(self.version)
        result["light_cones"] = from_list(lambda x: to_class(LightCone, x), self.light_cones)
        result["relics"] = from_list(lambda x: to_class(Relic, x), self.relics)
        result["characters"] = from_list(lambda x: to_class(Character, x), self.characters)
        return result


def hsr_scan_data_from_dict(s: Any) -> HsrScanData:
    return HsrScanData.from_dict(s)


def hsr_scan_data_to_dict(x: HsrScanData) -> Any:
    return to_class(HsrScanData, x)


def read_data():
    with open(HSRScanData_file_path, "r", encoding="utf-8") as f:
        data = f.read()
        hsr_scan_data = hsr_scan_data_from_dict(json.loads(data))
    return hsr_scan_data
    pass


def read_hanbook():
    name_to_id = {}
    with open("test/Handbook.txt", "r", encoding="utf-8") as f:
        data = f.read()
        data = data.split("\n")
        for line in data:
            #     如果只包含一个冒号，则分割，后面的作为key，前面的作为value
            if line.count(":") == 1:
                key, value = line.split(":")
                # 去处key和value的前后空格
                key = key.strip()
                value = value.strip()
                if not name_to_id.get(value):
                    name_to_id[value] = key
            # # 如果包含多个冒号，则分割，第一个作为key，后面的作为value
            # elif line.count(":")>1:
            #     key,*value=line.split(":")
            #     print(key,":".join(value))
            # # 如果不包含冒号，则直接打印
            # else:
            #     pass
        return name_to_id
        pass


relic_chi_eng = {
    '充能': "Energy Regeneration Rate",
    "效果抵抗": "Effect RES",
    '冰伤': "Ice DMG Boost",
    '击破特攻': "Break Effect",
    '固定攻击': "ATK",
    '固定生命': "HP",
    '固定防御': "DEF",
    '效果命中': "Effect Hit Rate",
    '暴击伤害': "CRIT DMG",
    '暴击率': "CRIT Rate",
    '治疗量': "Outgoing Healing Boost",
    '火伤': "Fire DMG Boost",
    '物理伤害': "Physical DMG Boost",
    '百分比攻击': "ATK_",
    '百分比生命': "HP_",
    '百分比防御': "DEF_",
    '虚数伤害': "Imaginary DMG Boost",
    '速度': "SPD",
    '量子伤害': "Quantum DMG Boost",
    '雷伤': "Lightning DMG Boost",
    '风伤': "Wind DMG Boost",
    "躯干": "Body",
    "脚部": "Feet",
    "手部": "Hands",
    "头部": "Head",
    "连接绳": "Link Rope",
    "位面球": "Planar Sphere", }


def get_relic_id():
    with open("test/json1/holyrelicnmain.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    label_set = set()
    relic_id_dict = {}
    for i in data:
        relic_id_dict[i['label']] = i['children']
    for key, value in relic_id_dict.items():
        pass
        value_dict = {}
        for i in value:
            label_set.add(i['label'])
            value_dict[i['label']] = i['value'][1]
        relic_id_dict[key] = value_dict
        # relic_id_dict[]
    # pprint(label_set)
    with open("test/json1/holyrelicnx.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    relic_id_sub_dict = {}
    for i in data:
        relic_id_sub_dict[i['label']] = i['value']

    #     按照relic_chi_eng的key，将relic_id_dict的key，它的value是一个字典，其中的key也需要替换，以及relic_id_sub_dict的key进行替换
    # 注意避免'dictionary keys changed during iteration'错误
    for key in list(relic_id_dict.keys()):
        if key in relic_chi_eng:
            relic_id_dict[relic_chi_eng[key]] = relic_id_dict.pop(key)
    # 它的value是一个字典，其中的key也需要替换
    for key in relic_id_dict:
        for sub_key in list(relic_id_dict[key].keys()):
            if sub_key in relic_chi_eng:
                relic_id_dict[key][relic_chi_eng[sub_key]] = relic_id_dict[key].pop(sub_key)
    for key in list(relic_id_sub_dict.keys()):
        if key in relic_chi_eng:
            relic_id_sub_dict[relic_chi_eng[key]] = relic_id_sub_dict.pop(key)

    return relic_id_dict, relic_id_sub_dict

    pass


si_jian = [
    "云无留迹的过客套装",
    "野穗伴行的快枪手套装",
    "净庭教宗的圣骑士套装",
    "密林卧雪的猎人套装",
    "街头出身的拳王套装",
    "戍卫风雪的铁卫套装",
    "熔岩锻铸的火匠套装",
    "繁星璀璨的天才套装",
    "激奏雷电的乐队套装",
    "晨昏交界的翔鹰套装",
    "流星追迹的怪盗套装",
    "盗匪荒漠的废土客套装",
    "宝命长存的莳者套装",
    "骇域漫游的信使套装",
    "毁烬焚骨的大公套装",
    "幽锁深牢的系囚套装",
    "死水深潜的先驱套装",
    "机心戏梦的钟表匠套装",
]

er_jian = [
    "太空封印站套装",
    "不老者的仙舟套装",
    "泛银河商业公司套装",
    "筑城者的贝洛伯格套装",
    "星体差分机套装",
    "停止转动的萨尔索图套装",
    "盗贼公国塔利亚套装",
    "生命的翁瓦克套装",
    "繁星竞技场套装",
    "折断的龙骨套装",
    "苍穹战线格拉默套装",
    "梦想之地匹诺康尼套装",
]

relic_name_chi_eng_dict = {'不老者的仙舟': 'Fleet of the Ageless',
                           '云无留迹的过客': 'Passerby of Wandering Cloud',
                           '停止转动的萨尔索图': 'Inert Salsotto',
                           '净庭教宗的圣骑士': 'Knight of Purity Palace',
                           '太空封印站': 'Space Sealing Station',
                           '宝命长存的莳者': 'Longevous Disciple',
                           '密林卧雪的猎人': 'Hunter of Glacial Forest',
                           '幽锁深牢的系囚': 'Prisoner in Deep Confinement',
                           '戍卫风雪的铁卫': 'Guard of Wuthering Snow',
                           '折断的龙骨': 'Broken Keel',
                           '星体差分机': 'Celestial Differentiator',
                           '晨昏交界的翔鹰': 'Eagle of Twilight Line',
                           '机心戏梦的钟表匠': 'Watchmaker, Master of Dream Machinations',
                           '梦想之地匹诺康尼': 'Penacony Land of the Dreams',
                           '死水深潜的先驱': 'Pioneer Diver of Dead Waters',
                           '毁烬焚骨的大公': 'The Ashblazing Grand Duke',
                           '泛银河商业公司': 'Pan-Cosmic Commercial Enterprise',
                           '流星追迹的怪盗': 'Thief of Shooting Meteor',
                           '激奏雷电的乐队': 'Band of Sizzling Thunder',
                           '熔岩锻铸的火匠': 'Firesmith of Lava-Forging',
                           '生命的翁瓦克': 'Sprightly Vonwacq',
                           '盗匪荒漠的废土客': 'Wastelander of Banditry Desert',
                           '盗贼公国塔利亚': 'Talia: Kingdom of Banditry',
                           '筑城者的贝洛伯格': 'Belobog of the Architects',
                           '繁星璀璨的天才': 'Genius of Brilliant Stars',
                           '繁星竞技场': 'Rutilant Arena',
                           '苍穹战线格拉默': 'Firmament Frontline Glamoth',
                           '街头出身的拳王': 'Champion of Streetwise Boxing',
                           '野穗伴行的快枪手': 'Musketeer of Wild Wheat',
                           '骇域漫游的信使': 'Messenger Traversing Hackerspace'}


def relic_name_chi_eng():
    with open("test/json1/holyrelicname.json", "r", encoding="utf-8") as f:
        data: list[dict] = json.load(f)
    temp_dict = {}
    for i in data:
        temp_dict[i['label']] = i['children']
    # temp_dict前四个key的value，都是列表，从四个列表中每个取一个元素，组成一个新的列表，然后添加到一个列表中，重复这个过程直到value取完
    result_list = []

    while True:
        new_list = []
        keys = list(temp_dict.keys())[:4]  # 获取前四个键
        for key in keys:
            if len(temp_dict[key]) > 0:
                new_list.append(temp_dict[key].pop(0))
            else:
                keys.remove(key)  # 如果列表已经空了，从keys中移除该键

        if len(new_list) > 0:
            result_list.append(new_list)
        else:
            break
    # 对temp_dict的最后两个key进行相同的操作
    result_list2 = []
    while True:
        new_list = []
        keys = list(temp_dict.keys())  # 获取前四个键
        for key in keys:
            if len(temp_dict[key]) > 0:
                new_list.append(temp_dict[key].pop(0))
            else:
                keys.remove(key)  # 如果列表已经空了，从keys中移除该键

        if len(new_list) > 0:
            result_list2.append(new_list)
        else:
            break
    # 我现在只需要列表中每个字典的value
    result_list = [[i['value'] for i in j] for j in result_list]
    result_list.append([61171, 61172, 61173, 61174])
    result_list.append([61181, 61182, 61183, 61184])
    # 这里手动添加两个新的列表
    result_list2 = [[i['value'] for i in j] for j in result_list2]

    # 现在result_list就是四件套，列表的索引表示套装，列表元素也是列表，这个列表就表示头，手，身体，脚
    # result_list2就是两件套，列表的索引表示套装，列表元素也是列表，这个列表就表示球，绳

    # result_list对应si_jian，result_list2对应er_jian
    # 用si_jian和result_list，er_jian和result_list2，将它们合并成一个字典
    si_jian_dict = {}
    er_jian_dict = {}
    for i in range(len(si_jian)):
        si_jian_dict[si_jian[i][:-2]] = result_list[i]
    for i in range(len(er_jian)):
        er_jian_dict[er_jian[i][:-2]] = result_list2[i]
    # 根据relic_name_chi_eng，将si_jian_dict和er_jian_dict的key进行替换
    for key in list(si_jian_dict.keys()):
        if key in relic_name_chi_eng_dict:
            si_jian_dict[relic_name_chi_eng_dict[key]] = si_jian_dict.pop(key)
    for key in list(er_jian_dict.keys()):
        if key in relic_name_chi_eng_dict:
            er_jian_dict[relic_name_chi_eng_dict[key]] = er_jian_dict.pop(key)
    return si_jian_dict, er_jian_dict

    pass



def get_RelicSubAffixConfig():

    with open("test/json1/RelicSubAffixConfig.json", "r", encoding='utf-8') as f:
        subaffix: dict = json.load(f)
    for star_number, value in subaffix.items():
        for key, affix in value.items():
            base_value = affix['BaseValue']['Value']
            step_value = affix['StepValue']['Value']
            if base_value == 0.05184:
                pass
            temp_list = [2 * i for i in range(1, 7)]
            #         一个词条最多强化6次，temp_list表示每个强化级别下step_value可能的次数
            aff = affix["step_dict"] = {}
            for index, value in enumerate(temp_list):
                aff[index] = []
                b_value = base_value * (index + 1)
                bb_value=Decimal(b_value).quantize(Decimal('0.001'),rounding='ROUND_DOWN')
                aff[index].append(bb_value)
                for i in range(1, value + 1):
                    # 目前存在浮点数计算误差，需要解决
                    temp_value=b_value + step_value * i
                    # 保留四位小数
                    temp_value = Decimal(temp_value).quantize(Decimal('0.001'),rounding='ROUND_DOWN')
                    aff[index].append(temp_value)
    return subaffix

def get_relic_detail(substat: Substat, rarity: int):
    subAffix = get_RelicSubAffixConfig()
    ddict = subAffix[str(rarity)]

    # temp_list=[]
    # for key,value in ddict.items():
    #     temp_list.append(value['key'])
    relic_id_dict, relic_id_sub_dict = get_relic_id()

    # subs = substat.key.value
    subs = substat.key
    num = substat.value
    if subs.endswith("_"):
        num = num / 100
    pass
    num = Decimal(num).quantize(Decimal('0.001'), rounding='ROUND_UP')
    count = None
    step = None
    try:
        id = relic_id_sub_dict[subs]
    except:
        # 不知道'CRIT Rate_'的’_‘有什么意义
        subs = subs.replace("_", "")
        id = relic_id_sub_dict[subs]
    dictt = ddict[str(id)]['step_dict']
    # # 判断num在哪个区间
    # for key in dictt:
    #     if num >= dictt[key][0] and num <= dictt[key][-1]:
    #         count = key
    #         break

    # 计算num与每个列表的最大值和最小值的差值，返回两个差值均最小的列表的索引
    count = min(range(len(dictt)), key=lambda i: abs(dictt[i][0] - num) + abs(dictt[i][-1] - num))

    if count is None:
        # 不要判断是0，也就是if not count
        count = 1
        num = dictt[0][0]
    for i in dictt[count]:
        # 寻找列表中与num最接近的值，返回索引
        # if i == num:
        #     step = dictt[count].index(i)
        #     break
        # elif i > num:
        #     # step = dictt[count].index(i) - 1
        #     step = dictt[count].index(i) - 1
        # break

        # 计算列表中所有值与num的差值，返回最小值的索引
        step = min(range(len(dictt[count])), key=lambda i: abs(dictt[count][i] - num))

    return {
        "id": id,
        "count": count + 1,
        "step": step
    }


def name_to_id():
    hsr_scan_data = read_data()
    name_to_id = read_hanbook()
    relic_id_dict, relic_id_sub_dict = get_relic_id()
    si_jian_dict, er_jian_dict = relic_name_chi_eng()
    slot_list_1 = ["Head", "Hands", "Body", "Feet"]
    slot_list_2 = ["Planar Sphere", "Link Rope"]

    print("开始转换")

    for light_con in hsr_scan_data.light_cones:
        light_con.location = name_to_id.get(light_con.location, light_con.location)
        light_con.key = name_to_id[light_con.key]
    for avater in hsr_scan_data.characters:
        avater.key = name_to_id.get(avater.key, 8001)
    #     8001-8004均是旅行者

    # # 保留前50个圣遗物
    # 测试用
    # hsr_scan_data.relics = hsr_scan_data.relics[:50]

    for relic in hsr_scan_data.relics:
        # if relic.location.value != "Dr. Ratio":
        #     continue
        try:
            ddict = si_jian_dict[relic.set]
            index = slot_list_1.index(relic.slot)
        #     ddict = si_jian_dict[relic.set.value]
        #             index = slot_list_1.index(relic.slot.value)
        except:
            try:
                # ddict = er_jian_dict[relic.set.value]
                ddict = er_jian_dict[relic.set]
            except:
                #     逗号变空格
                valuee = relic.set
                # valuee = relic.set.value 移除了enum
                valuee = valuee.replace(",", "")
                valuee = valuee.replace(":", "")
                # relic.set.value被enum限制，所以不赋值
                ddict = er_jian_dict[valuee]
            # index = slot_list_2.index(relic.slot.value)
            index = slot_list_2.index(relic.slot)
        relic.id = ddict[index]
        if relic.rarity == 4:
            relic.id = relic.id - 10000
        #     这里就是int，别管提示
        elif relic.rarity == 3:
            relic.id = relic.id - 20000
        elif relic.rarity == 2:
            relic.id = relic.id - 30000
        # 现在relic有了正确的id，slot，set属性不重要了
        # rarity属性也不重要了，因为不同星级的仪器的编号也不一样
        # relic.set= name_to_id[relic.set.value]
        ddict = relic_id_dict[relic.slot]
        # ddict = relic_id_dict[relic.slot.value]
        try:
            relic.mainAffix = ddict[relic.mainstat]
            # relic.mainAffix = ddict[relic.mainstat.value]
        except:
            relic.mainAffix = ddict[relic.mainstat + "_"]
            # relic.mainAffix = ddict[relic.mainstat.value + "_"]
        rarity = relic.rarity
        relic.subAffixes = [get_relic_detail(substat, rarity) for substat in relic.substats]
        # relic.location = name_to_id.get(relic.location.value, relic.location.value)
        relic.location = name_to_id.get(relic.location, relic.location)
    print("转换完成")
    return hsr_scan_data
    pass




def insert_relic_detail(relic: Relic):
    # relic数据示例：
    '''
{
  "ownerUid": 10002,
  "itemId": 63036,
  "count": 1,
  "level": 15,
  "exp": 0,
  "totalExp": 0,
  "promotion": 0,
  "rank": 0,
  "locked": false,
  "discarded": false,
  "mainAffix": 4,
  "subAffixes": [
    {
      "id": 4,
      "count": 1,
      "step": 2
    },
    {
      "id": 12,
      "count": 3,
      "step": 6
    },
    {
      "id": 10,
      "count": 1,
      "step": 2
    },
    {
      "id": 7,
      "count": 4,
      "step": 8
    }
  ],
  "equipAvatar": 0
}
    '''
    # 我觉得基本上找不到一样的圣遗物
    # 插入数据
    if relic.location == "TrailblazerPreservation":
        relic.location = 8001
    collection_item.insert_one(
        {
            "ownerUid": player_id,
            "itemId": relic.id,
            "count": 1,
            "level": relic.level,
            "exp": 0,
            "totalExp": 0,
            "promotion": 0,
            "rank": 0,
            "locked": relic.lock,
            "discarded": relic.discard,
            "mainAffix": int(relic.mainAffix),
            "subAffixes": relic.subAffixes,
            "equipAvatar": 0 if relic.location == "" else int(relic.location)
        })
    print(f"插入圣遗物{relic.id}成功")

    pass


def insert_light_cone(light_cone: LightCone):
    '''
    在数据库中：
    {
  "ownerUid": 10002,
  "itemId": 23014,
  "count": 1,
  "level": 1,
  "exp": 0,
  "totalExp": 0,
  "promotion": 0,
  "rank": 1,
  "locked": false,
  "discarded": false,
  "mainAffix": 0,
  "equipAvatar": 0
}
    :param light_cone:
    :return:
    '''
    if light_cone.location == "TrailblazerPreservation":
        light_cone.location = 8001

    collection_item.insert_one(
        # 由于光锥有一摸一样的，所以不能用update_one
        {"ownerUid": player_id,
         "itemId": int(light_cone.key),
         "count": 1,
         "level": light_cone.level,
         "exp": 0,
         "totalExp": 0,
         "promotion": light_cone.ascension,
         "rank": light_cone.superimposition,
         "locked": light_cone.lock,
         "discarded": False,
         "mainAffix": 0,
         "equipAvatar": 0 if light_cone.location == "" else int(light_cone.location)
         })
    print(f"插入光锥{light_cone.key}成功")


def insert_character(avater: Character):
    '''
    在数据库中：
    {
  "ownerUid": 10001,
  "avatarId": 1105,
  "data": {
    "rank": 0,
    "skills": {
      "1105001": 1,
      "1105002": 1,
      "1105003": 1,
      "1105004": 1,
      "1105007": 1
    }
  },
  "level": 1,
  "exp": 0,
  "promotion": 0,
  "rewards": 0,
  "timestamp": {
    "$numberLong": "1705820023"
  },
  "currentHp": 10000,
  "currentSp": 0,
  "extraLineupHp": 0,
  "extraLineupSp": 0
}
    :param avater:
    :return:
    '''

    # 主角的行迹和命座莫名的保存在heroPaths集合，从8001到8004,01和02是男女，03和04是什么怪？
    # 而且这个集合更换账号就会清空，所以可能需要制作一个脚本来快速插入信息
    # TODO

    trace_dict = {}
    traces = avater.traces
    id = str(avater.key)
    # 有的key是int，有的是str
    if traces['ability_1']:
        trace_dict[id + "101"] = 1
    if traces['ability_2']:
        trace_dict[id + "102"] = 1
    if traces['ability_3']:
        trace_dict[id + "103"] = 1
    if traces['stat_1']:
        trace_dict[id + "201"] = 1
    if traces['stat_2']:
        trace_dict[id + "202"] = 1
    if traces['stat_3']:
        trace_dict[id + "203"] = 1
    if traces['stat_4']:
        trace_dict[id + "204"] = 1
    if traces['stat_5']:
        trace_dict[id + "205"] = 1
    if traces['stat_6']:
        trace_dict[id + "206"] = 1
    if traces['stat_7']:
        trace_dict[id + "207"] = 1
    if traces['stat_8']:
        trace_dict[id + "208"] = 1
    if traces['stat_9']:
        trace_dict[id + "209"] = 1
    if traces['stat_10']:
        trace_dict[id + "210"] = 1

    collection_avatar.update_one(
        filter={"ownerUid": player_id, "avatarId": int(avater.key)},
        update={'$set': {
            "ownerUid": player_id,
            "avatarId": int(avater.key),
            "data": {
                "rank": avater.eidolon,
                #   命座
                "skills": {
                    id + "001": avater.skills.basic,
                    id + "002": avater.skills.skill,
                    id + "003": avater.skills.ult,
                    id + "004": avater.skills.talent,
                    id + "007": 1,
                    #     007秘技
                    **trace_dict
                }
            },
            "level": avater.level,
            "exp": 0,
            "promotion": avater.ascension,
            #       等级
            "rewards": 0,
            "timestamp": 1705820023,
            #     时间戳有问题
            "currentHp": 10000,
            "currentSp": 0,
            "extraLineupHp": 0,
            "extraLineupSp": 0
        }}, upsert=True)
    print(f"插入角色{avater.key}成功")


def insert_database(hsr_scan_data: HsrScanData):
    for avater in hsr_scan_data.characters:
        insert_character(avater)

    for i in hsr_scan_data.light_cones:
        insert_light_cone(i)

    for relic in hsr_scan_data.relics:
        insert_relic_detail(relic)


if __name__ == '__main__':
    hsr_scan_data = name_to_id()
    insert_database(hsr_scan_data)
    pass
