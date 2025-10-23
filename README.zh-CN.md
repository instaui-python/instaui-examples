# insta-examples

<div align="center">

简体中文| [English](./README.md)

</div>
 
## 📖 介绍
本项目是一个基于 instaui 的示例项目，展示了 instaui 及其周边库的使用示例。

在线网址: [在线示例](https://instaui-python.github.io/instaui-examples/)

> 由于国内 cdn 速度限制，第一次访问时可能会长时间加载


## 完全离线 web 页面
本项目可以生成完全离线的本地网页。

你需要安装好 `uv`。

初始化环境
```shell
uv sync --all-groups
```

生成离线本地网页
```shell
uv run src/main.py --offline
```

生成的网页文件位于 `website` 文件夹中。
