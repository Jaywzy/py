# 利用ChatGPT自动翻译sgml文件


## 环境搭建：
- python安装selenium：`pip install selenium`
- 根据自己的Chrome版本，安装webdriver驱动。[国内镜像Chrome](https://registry.npmmirror.com/binary.html?path=chromedriver/)
- poe.com上新建一个bot，设置bot模型为ChatGPT，prompt可参考我的设置：
  > 你是一个翻译官，帮助我翻译LightDB的文档。 我会把sgml代码片段发你，帮我翻译成中文，请保留其中sgml标签。 翻译结果不要有遗漏，也不需要补充多余内容，只返回给我翻译结果。 翻译结果以代码块形式展示，并与原文的缩进保持一致。
- 用你的bot地址替换poeBot.py中`BOT_URL`常量
- 运行`python poeBot.py 'login'`，手动登录一次，生成cookie文件，以后脚本会自动登录
- 考虑bot答案的不可控，也可以就使用我建好的bot，那么就不用替换常量了，但仍需手动登录一次获取cookie

------

## 使用方法：
- 将需要翻译的sgml文件放入sgml文件夹中
- 执行命令: `python .\auto_trans_sgml.py .\sgml\ .\sgml\ .\sgml-cn\`

------

## 可能碰到的问题
- bot答案不符合预期
  > 预期流程：我们将需要翻译的片段通过代码块发给bot，bot作为翻译工具，将翻译好的内容也是通过代码块返回，脚本通过copy按钮获取答案。如果答案不符合预期，可能要先调教一下bot，或调整prompt，且bot有4到5个模型轮换，风格会有所不同，此为不可控因素。应该可以直接使用我的bot，名为LightDBDocBoy，目前比较稳定。
- bot频繁超时
  > 超时两次以上脚本会自动重启浏览器，重新连接bot
- 翻译结果没有放在代码块中，导致无法复制
  > 脚本会自动要求bot将翻译结果放在代码块中
- 内容超长，导致答案无法复制
  > 如果翻译的内容超长，请缩放浏览器，保证所有答案在一页内能看到
- 脚本工作时pc不可锁屏