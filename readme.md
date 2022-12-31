<div align="center">

# 命令探查 0.0.1

</div>

缓解下载了新插件却不会使用的焦虑

使用`scan-all`指令，让bot展示一份简陋甚至错误百出的帮助菜单

使用`scan-search <name>`指令，让bot展示`<name>`相关的内容

使用`scan-list`指令，让bot展示所有模块名

## 实现原理

遍历`nonebot.matcher.matchers`对象，分析所有`Matcher`
