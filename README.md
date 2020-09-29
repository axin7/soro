# Soro



## 介绍

Soro 是一款 Mac 端的智能助手。

可通过语音控制电脑，对系统和应用进行操作。



## 安装方法

1. `git clone https://github.com/axin7/soro.git`
2. 下载[词向量模型文件](https://www.yun.cn/s/be03749ab7fc43a3b535d225011d38bf)放置到 `/data` 目录下
3. 安装相关依赖 `pipenv install`

> kenlm 安装失败使用该方法*：*`pip install https://github.com/kpu/kenlm/archive/master.zip`



## 使用方法

1. 进入虚拟环境 `pipenv shell`  (或其他方法)
2. 启动 Rasa 服务 `rasa run -m models --enable-api --endpoints endpoints.yml`
3. 启动 Rasa Action 服务 `rasa run actions`
4. 启动 Soro 服务 `python run.py`
5. 语音与 Soro 进行交互

