# 利用ChatGPT自动翻译sgml文件


## 环境搭建：
1. python安装selenium：`pip install selenium`
2. 根据自己的Chrome版本，安装webdriver驱动。[国内镜像Chrome](https://registry.npmmirror.com/binary.html?path=chromedriver/)


## 前期准备：
- poe.com上新建一个bot，设置bot的promote为翻译sgml文档专用，可参考我的设置：
  > 你是一个翻译官，帮助我翻译LightDB的文档。 我会把sgml代码片段发你，帮我翻译成中文，请保留其中sgml标签。 翻译结果不要有遗漏，也不需要补充多余内容，只返回给我翻译结果。 翻译结果以代码块形式展示，并与原文的缩进保持一致。
- 用你的bot地址替换poeBot.py中`BOT_URL`常量
- 运行`python poeBot.py 'login'`，手动登录一次，生成cookie文件，以后脚本会自动登录


## 使用方法：
1. 将需要翻译的sgml文件放入sgml文件夹中
2. 执行命令: `python .\auto_trans_sgml.py .\sgml\ .\sgml\ .\sgml-cn\`