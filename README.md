![logo](./logo.png)

## 简介

Soro 是一款 Mac 端的智能助手。

可通过语音控制电脑，对系统和应用进行操作。



![img](./img.gif)





## 使用示例

- “打开网易云音乐”
- “关闭微信”
- “打开浏览器”
- “打开百度网站”
- “输入热门新闻”
- “点击搜索”
- “刷新网站”
- “关闭浏览器”
- “说个笑话”





## 安装配置

1. 下载仓库到本地： `git clone https://github.com/axin7/soro.git`
2. 下载[词向量模型文件](https://www.yun.cn/s/99ab5d78827b4e8ba84f4c78b9039b99)放置到 `/data` 目录下
3. 安装相关依赖： `pipenv install`
4. 在 `process/config.py` 中设置百度语音识别参数

> kenlm 安装失败使用该方法：`pip install https://github.com/kpu/kenlm/archive/master.zip`





## 快速开始

1. 进入虚拟环境 `pipenv shell`  (或其他方法)
2. 启动 Rasa 服务 `rasa run -m models --enable-api --endpoints endpoints.yml`
3. 启动 Rasa Action 服务 `rasa run actions`
4. 启动 Soro 服务 `python run.py`
5. 语音与 Soro 进行交互





## 待办事项

- [ ] 操作浏览器
  - [x] 打开/关闭
  - [x] 点击
  - [x] 刷新
  - [x] 打开网站
  - [ ] 输入
  - [ ] 更多 selenium 操作支持

- [ ] QA/闲聊
	- [x] 基础
	- [ ] 其他

- [ ] 系统操作
  - [x] 打开/关闭应用
  - [ ] 截图
  - [ ] 显示/隐藏文件夹
  - [ ] 锁屏
  - [ ] ......
- [ ] 更多复杂任务对话
- [ ] 远程控制电脑(钉钉、企业微信）
  - [ ] 通信管道
  - [ ] 支持所有操作