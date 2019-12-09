# YouOtterKnow PTT 八卦版爬蟲 LineBot

## PTT 爬蟲 linebot 使用說明
### 加入好友
![id](https://i.imgur.com/unV8WmP.png)

### 初始狀態
一開始加入 linebot 並不會顯示特別提示功能 ,
必須輸入 "start" 方可開始使用本服務 , 接下來只要照著提示輸入即可 . ( 如下圖 )

![id](https://i.imgur.com/nWL6YdM.png)

### 兩種服務
* linebot 提供 " 預設搜尋 " 以及 " 客製化搜尋 " 兩種服務 :
    * 預設搜尋 : 輸入 " 關鍵字 " 並回傳與標題相符之 5 筆最新文章 .
    * 客製化搜尋 : 設定 " 關鍵字 ", " 推文數量 " , " 顯示文章數量 " 做更進階的搜尋 .

### 搜尋流程

![flow](https://i.imgur.com/cGAhfnh.png)

## Finite State Machine
![fsm](https://github.com/MoMoParadox/YouOtterKnow_PTT_gossip_crawl/blob/master/img/show-fsm.png?raw=true)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will always needs a condition to trigger for the transition.

* user
	* 初始輸入: "start"
		* 正式進入linebot服務 , linebot會提供詳細用法

	* 之後輸入: 按照指示輸入即可
		* 請參考上圖

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Heroku
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)

## Deploy
Setting to deploy webhooks on Heroku.


### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
