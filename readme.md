<div align="center">

# 命令探查 0.0.1

</div>

缓解下载了新插件却不会使用的焦虑

使用`scan-all`指令，让bot展示一份简陋甚至错误百出的帮助菜单

使用`scan-search <name>`指令，让bot展示`<name>`相关的内容

使用`scan-list`指令，让bot展示所有模块名

## 效果示例

以安装了`nonebot_plugin_game_collection`为例

`scan-search 赛马`

```
Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '创建赛马'/'赛马创建'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '开始赛马'/'赛马开始'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '暂停赛马'/'赛马暂停'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '赛马事件重载'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '赛马加入'/'加入赛马'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '赛马清空'/'清空赛马'

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调名称] _
[可用命令] [cmds] '赛马重置'/'重置赛马'
```

## 实现原理

遍历`nonebot.matcher.matchers`对象，分析所有`Matcher`
