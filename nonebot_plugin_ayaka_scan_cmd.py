'''扫描当前所有matcher，总结命令'''
from itertools import chain
from nonebot.matcher import matchers, Matcher
from nonebot.rule import CommandRule, RegexRule, EndswithRule, KeywordsRule, FullmatchRule, StartswithRule, ShellCommandRule
from ayaka import AyakaBox

box = AyakaBox("命令探测")


def get_info(m: Matcher):
    handle_names = [h.call.__name__ for h in m.handlers]
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
            info = "[other] "
            info += getattr(call, "__name__", "未知checker")
        checker_names.append(info)
    checker_names.sort()
    info = f"[模块名称] {m.module_name}\n"
    info += "[回调名称] " + "\n".join(handle_names) + "\n"
    info += "[可用命令] " + "\n".join(checker_names)
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
    names = list(set(m.module_name for m in ms))
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
