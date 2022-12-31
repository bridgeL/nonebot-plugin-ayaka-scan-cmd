<div align="center">

# 命令探查 0.0.3

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
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '创建赛马'/'赛马创建'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '加入赛马'/'赛马加入'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '清空赛马'/'赛马清空'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '赛马事件重载'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '赛马开始'/'开始赛马'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '赛马暂停'/'暂停赛马'
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] nonebot_plugin_game_collection
[回调位置] nonebot_plugin_game_collection
[回调名称] _
[可用命令]
  [cmds] '赛马重置'/'重置赛马'
[回调注释] 无
```

以安装了`nonebot_plugin_ayaka_games`为例

`scan-search suspect`

```
Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] box_entrance
[可用命令]
  [cmds] '谁是卧底'
  [other] 未知指令
[回调注释] 打开应用

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] exit_play
[可用命令]
  [cmds] 'exit'/'退出'
  [other] 未知指令
[回调注释] 无

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] exit_room
[可用命令]
  [cmds] 'exit'/'退出'
  [other] 未知指令
[回调注释] 关闭游戏

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] join
[可用命令]
  [cmds] 'join'/'加入'
  [other] 未知指令
[回调注释] 加入房间

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] leave
[可用命令]
  [cmds] '离开'/'leave'
  [other] 未知指令
[回调注释] 离开房间

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] play_info
[可用命令]
  [cmds] '信息'/'info'
  [other] 未知指令
[回调注释] 展示投票情况

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] room_info
[可用命令]
  [cmds] '信息'/'info'
  [other] 未知指令
[回调注释] 展示房间内成员列表

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] start
[可用命令]
  [cmds] 'start'/'begin'/'开始'
  [other] 未知指令
[回调注释] 开始游戏

Ayaka Bot(123) 说：
[模块名称] ayaka.box
[回调位置] ayaka_games.plugins.who_is_suspect
[回调名称] vote
[可用命令]
  [cmds] 'vote'/'投票'
  [other] 未知指令
[回调注释] 请at你要投票的对象，一旦投票无法更改
```


## 实现原理

遍历`nonebot.matcher.matchers`对象，分析所有`Matcher`
