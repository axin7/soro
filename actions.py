# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import subprocess
from typing import Any, Dict, List, Text

from helium import click, go_to, kill_browser, refresh, start_chrome, write
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from requests_html import HTMLSession

from process.model import App

session = HTMLSession()

class OpenApp(Action):
    """打开软件"""

    def name(self) -> Text:
        return "action_open_app"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        appname = tracker.get_slot('app_name')
        if appname:
            path = App.select(App.path).where(App.tag.contains(appname))[0].path
            command = ['open',path]
            subprocess.run(command)
            dispatcher.utter_message("已打开")
            tracker.slots = {'app_name':''}
        else:
            dispatcher.utter_message("抱歉，没有识别到软件名")
        return []


class CloseApp(Action):
    """关闭软件"""

    def name(self) -> Text:
        return "action_close_app"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        appname = tracker.get_slot('app_name')
        print(f'app_name词槽为：{appname}')
        if appname:
            command = ['killall',appname]
            subprocess.run(command)
            dispatcher.utter_message("已关闭")
            tracker.slots = {'app_name':''}
        else:
            dispatcher.utter_message("抱歉，没有识别到软件名")
        return []


class OpenBrowser(Action):
    """打开浏览器"""

    def name(self) -> Text:
        return "action_open_browser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        start_chrome()
        dispatcher.utter_message("已打开")
        return []


class CloseBrowser(Action):
    """关闭浏览器"""

    def name(self) -> Text:
        return "action_close_browser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        kill_browser()
        dispatcher.utter_message("已关闭")
        return []


class RefreshBrowser(Action):
    """刷新浏览器"""

    def name(self) -> Text:
        return "action_refresh_browser"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        refresh()
        dispatcher.utter_message("已刷新")
        return []


class OpenWeb(Action):
    """打开网页"""

    def name(self) -> Text:
        return "action_open_web"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        web_name = tracker.get_slot('web_name')
        url = tracker.get_slot('url')

        
        if web_name:
            search_url = f"https://www.dogedoge.com/results?q={web_name}官网"
            r = session.get(search_url)
            result_list = r.html.find(".result__a",first=True).absolute_links
            web_url = list(result_list)[0]
            go_to(web_url)
            tracker.slots = {'web_name':''}
            dispatcher.utter_message("已打开")

        elif url:
            go_to(url)
            tracker.slots = {'url':''}
            dispatcher.utter_message("已打开")

        else:
            dispatcher.utter_message("抱歉，无法识别要打开的网站")
        return []


class Click(Action):
    """点击"""

    def name(self) -> Text:
        return "action_click"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        element_name = tracker.get_slot('element_name')
        if element_name:
            click(element_name)
            tracker.slots = {'element_name':''}
            dispatcher.utter_message("已点击")

        else:
            dispatcher.utter_message("抱歉，无法识别元素名称")
        return []


class Write(Action):
    """输入"""

    def name(self) -> Text:
        return "action_write"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        keyword = tracker.get_slot('keyword')
        if keyword:
            write(keyword)
            tracker.slots = {'keyword':''}
            dispatcher.utter_message("已输入")

        else:
            dispatcher.utter_message("抱歉，无法识别关键词名称")
        return []