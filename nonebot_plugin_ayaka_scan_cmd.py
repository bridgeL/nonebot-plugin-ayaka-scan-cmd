'''扫描当前所有matcher，总结命令'''
from itertools import chain
from nonebot.matcher import matchers, Matcher
from nonebot.rule import CommandRule, RegexRule, EndswithRule, KeywordsRule, FullmatchRule, StartswithRule, ShellCommandRule
from ayaka import AyakaBox

box = AyakaBox("命令探查")


def get_info(m: Matcher):
    handle_names = [h.call.__name__ for h in m.handlers]
    handle_locs = list(set(h.call.__module__ for h in m.handlers))
    handle_docs = [h.call.__doc__ for h in m.handlers if h.call.__doc__]
    if not handle_docs:
        handle_docs = ["无"]
    checker_names = []
    for checker in m.rule.checkers:
        call = checker.call
        if isinstance(call, CommandRule):
            info = "[cmds] "
            info += "/".join(
                repr(c)
                for cmds in call.cmds for c in cmds
            )
        elif isinstance(call, ShellCommandRule):
            info = "[shellcmd] "
            info += "/".join(
                repr(c)
                for cmds in call.cmds for c in cmds
            )
        elif isinstance(call, KeywordsRule):
            info = "[keywords] "
            info += "/".join(repr(c) for c in call.keywords)
        elif isinstance(call, RegexRule):
            info = "[regex] "
            info += repr(call.regex)
        elif isinstance(call, StartswithRule):
            info = "[startwith] "
            info += repr(call.msg)
        elif isinstance(call, EndswithRule):
            info = "[endwith] "
            info += repr(call.msg)
        elif isinstance(call, FullmatchRule):
            info = "[fullmatch] "
            info += repr(call.msg)
        else:
            info = "[other] 未知指令"
        checker_names.append(info)
    checker_names.sort()
    info = f"[模块名称] {m.module_name}"
    info += "\n[回调位置] " + "/".join(handle_locs)
    info += "\n[回调名称] " + "/".join(handle_names)
    info += "\n[可用命令]\n  " + "\n  ".join(checker_names)
    info += "\n[回调注释] " + "\n".join(handle_docs)
    return info


@box.on_cmd(cmds=["scan-all"])
async def scan_all():
    ms = list(chain(*matchers.values()))
    items = [get_info(m) for m in ms]
    items.sort()
    await box.send_many(items)


@box.on_cmd(cmds=["scan-list"])
async def scan_list():
    ms = list(chain(*matchers.values()))
    names = set()
    for m in ms:
        names.add(m.module_name)
        for h in m.handlers:
            names.add(h.call.__module__)
    names = list(names)
    names.sort()
    await box.send("\n".join(names))


@box.on_cmd(cmds=["scan-search"])
async def scan_search():
    ms = list(chain(*matchers.values()))
    items = [get_info(m) for m in ms]
    key = str(box.arg)
    items = [item for item in items if key in item]
    items.sort()
    await box.send_many(items)
