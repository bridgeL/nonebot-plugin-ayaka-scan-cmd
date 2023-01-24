'''扫描当前所有matcher，总结命令'''
import re
import json
from loguru import logger
from random import sample
from asyncio import sleep
from itertools import chain
from nonebot.matcher import matchers, Matcher
from nonebot.rule import CommandRule, RegexRule, EndswithRule, KeywordsRule, FullmatchRule, StartswithRule, ShellCommandRule, ToMeRule
from pydantic import BaseModel
from ayaka import AyakaCat, resource_download, bridge

cat = AyakaCat("命令探查")
pt = re.compile(r"nonebot[_-]plugin[_-]")
pt2 = re.compile(r"^(plugins(_test)?|src)\.")

plugins: list["PluginInfo"] = []
nb_shop_data: list["NbShopPluginInfo"] = []


def short_name(name: str):
    name = pt2.sub("", name)
    name = name.split(".")[0]
    name = pt.sub("", name)
    return name


@bridge.on_startup
async def download():
    nb_shop_data.clear()
    logger.info("nb商店数据更新中...")
    try:
        data = await resource_download("https://raw.githubusercontent.com/nonebot/nonebot2/master/website/static/plugins.json")
    except:
        pass
    else:
        data = json.loads(data)
        for d in data:
            nb_shop_data.append(NbShopPluginInfo(**d))
        logger.info("nb商店数据更新完毕")


class NbShopPluginInfo(BaseModel):
    module_name: str
    project_link: str
    name: str
    desc: str
    author: str
    homepage: str

    def relative(self, name: str):
        return name in self.module_name or name in self.desc

    def get_info(self):
        items = [
            f"名称：{self.name}",
            f"描述：{self.desc}",
            f"作者：{self.author}",
            f"包名：{self.module_name}",
            f"主页：{self.homepage}",
        ]
        return "\n".join(items)


class RuleInfo(BaseModel):
    type: str = ""
    args: list[str] = []

    def get_info(self):
        if self.args:
            info = " / ".join(self.args)
            return f"[{self.type}]{info}"
        return self.type


class HandlerInfo(BaseModel):
    module: str = ""
    name: str = ""
    doc: str = ""

    def is_useful(self):
        info = self.name + self.doc
        info = info.replace("_", "").strip()
        return info

    def get_info(self):
        info = self.name
        if self.doc:
            info += f"({self.doc})"
        return info


class MatcherInfo(BaseModel):
    rules: list[RuleInfo] = []
    handlers: list[HandlerInfo] = []

    def get_info(self):
        items = []
        if self.rules:
            if len(self.rules) == 1:
                items.append(f"规则：{self.rules[0].get_info()}")
            else:
                items.append("多规则：")
                for r in self.rules:
                    items.append("  " + r.get_info())

        handlers = [h for h in self.handlers if h.is_useful()]
        if handlers:
            if len(handlers) == 1:
                items.append(f"回调：{handlers[0].get_info()}")
            else:
                items.append("多回调：")
                for h in handlers:
                    items.append("  " + h.get_info())

        return "\n".join(items)


class PluginInfo(BaseModel):
    name: str = ""
    matchers: list[MatcherInfo] = []
    meta: dict = {}

    def get_infos(self):
        info = f"插件名：{self.name}\nmatcher数量：{len(self.matchers)}"
        items = [info]
        if self.meta:
            items.append("- 插件元数据 -")
            for k, v in self.meta.items():
                if v:
                    if len(str(v)) < 50:
                        items.append(f"[{k}] {v}")
                    else:
                        items.append(f"[{k}]\n{v}")

        if self.matchers:
            items.append("- 解析出的matcher信息 -")
            for m in self.matchers:
                item = m.get_info()
                if item not in items:
                    items.append(item)

        return items


def get_plugin(plugin_name: str, auto_create: bool = True):
    for plugin in plugins:
        if plugin.name == plugin_name:
            return plugin
    if not auto_create:
        return
    plugin = PluginInfo(name=plugin_name)
    plugins.append(plugin)
    return plugin


async def scan_all():
    plugins.clear()
    ms = list(chain(*matchers.values()))
    for m in ms:
        name = short_name(m.module_name)
        plugin = get_plugin(name)
        if not plugin.meta:
            meta = getattr(m.module, "__plugin_meta__", None)
            if meta:
                plugin.meta = vars(meta)
        plugin.matchers.append(scan_matcher(m))
        await sleep(0)
    plugins.sort(key=lambda x: x.name)


def scan_matcher(matcher: Matcher):
    m = MatcherInfo()
    for dependent in matcher.handlers:
        m.handlers.append(scan_handler(dependent.call))

    for dependent in matcher.rule.checkers:
        m.rules.append(scan_checker(dependent.call))
    return m


def scan_handler(func):
    doc = ""
    if func.__doc__:
        doc = func.__doc__
    return HandlerInfo(
        module=short_name(func.__module__),
        name=func.__name__,
        doc=doc,
    )


def scan_checker(func):
    if isinstance(func, (CommandRule, ShellCommandRule)):
        return RuleInfo(
            type="命令",
            args=list(chain(*func.cmds))
        )

    if isinstance(func, KeywordsRule):
        return RuleInfo(
            type="关键词",
            args=func.keywords
        )

    if isinstance(func, RegexRule):
        return RuleInfo(
            type="正则",
            args=[func.regex]
        )

    if isinstance(func, ToMeRule):
        return RuleInfo(type="@机器人")

    if isinstance(func, (StartswithRule, EndswithRule, FullmatchRule)):
        return RuleInfo(
            type=func.__class__.__name__,
            args=[func.msg]
        )

    return RuleInfo(type="[未知]")


cat.set_rest_cmds(cmds={"exit", "退出"})


@cat.on_cmd(cmds="命令探查")
async def scan_handle():
    '''唤醒猫猫，并扫描全部matchers'''
    await cat.wakeup()
    await cat.send_help()
    await scan_all()
    await show_all_plugin_names()


@cat.on_cmd(cmds="列表", states="*")
async def show_all_plugin_names():
    '''展示插件列表'''
    info = "\n".join(f"[{i}] {p.name}" for i, p in enumerate(plugins))
    await cat.send(info)


@cat.on_cmd(cmds="查看", states="*")
async def show_plugin_info():
    '''<编号>/<插件名> 展示插件信息'''
    if cat.nums:
        n = cat.nums[0]
        if n < 0 or n >= len(plugins):
            return await cat.send("超出范围了呢")
        plugin = plugins[n]
    else:
        plugin = get_plugin(cat.arg, False)
        if not plugin:
            return await cat.send("没有这个插件呢")

    await cat.send_many(plugin.get_infos())


@cat.on_cmd(cmds="商店", states="*")
async def show_plugin_info_in_shop():
    '''<编号>/<插件名> 在商店中查找该插件'''
    if not nb_shop_data:
        await cat.send("没有获取到商店数据，尝试下载...")
        await download()
        await cat.send("下载成功，请重新发送指令")
        return

    if cat.nums:
        n = cat.nums[0]
        if n < 0 or n >= len(plugins):
            return await cat.send("超出范围了呢")
        name = plugins[n].name
    else:
        name = cat.arg

    ps = [p for p in nb_shop_data if p.relative(name)]
    if not ps:
        return await cat.send("商店中没有这个插件呢")

    items = [
        f"查找插件 {name}",
        f"共找到{len(ps)}个结果"
    ]
    if len(ps) > 30:
        ps = sample(ps, 30)
        items.append("结果太多，仅展示随机抽取的30个")

    items.extend(p.get_info() for p in ps)
    await cat.send_many(items)
