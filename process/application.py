"""
该模块对系统的应用进行查询
"""
import pprint
import subprocess
import time
from pathlib import Path
from pprint import pprint

from parse import compile


def user_app_list(path=Path('/Applications')):
    """获取用户应用列表
    
    :param path: 用户应用的系统绝对路径

    :return applist: 应用列表。用于提取实体后，查询路径，进行启动、关闭等操作
    :return app_kw_dict 应用关键词词典。用于提取实体
    """
    applist = []
    app_kw_dict = {}

    # 遍历 application 目录
    for app in path.iterdir():
        appname = app.name.replace('.app', '')
        appinfo = {
            "name": appname,
            "tag": [],
            "path": f"/Applications/{app.name}"
        }
        appinfo['tag'].append(appname)

        tag_list = [appname]

        # 遍历每个app子目录中符合标准的文件，从中取 CFBundleDisplayName 值,保存为tag
        for file in app.rglob('InfoPlist.strings'):
            if file.is_file():
                # print(file)
                try:
                    with open(file, 'rb') as f:
                        content = f.read().decode('utf-16').splitlines()
                        p = compile('"CFBundleDisplayName" = "{name}";')
                        for r in content:
                            result = p.parse(r)
                            if result:
                                tag = result["name"]
                                appinfo["tag"].append(tag)
                                tag_list.append(tag)
                            else:
                                p = compile('CFBundleDisplayName = "{name}";')
                                result = p.parse(r)
                                if result:
                                    tag = result["name"]
                                    appinfo["tag"].append(tag)
                                    tag_list.append(tag)
                        appinfo["tag"] = list(set(appinfo["tag"]))  # 去重
                        tag_list = list(set(tag_list))
                except Exception as ex:
                    # print(f"出错文件为{file}")
                    continue

        applist.append(appinfo)
        app_kw_dict[appname] = tag_list

    return applist, app_kw_dict


def sys_app_list(path=Path('/System/Applications')):
    """获取系统应用列表
    
    :param path：系统应用的系统绝对路径
    :return applist: 应用列表。用于提取实体后，查询路径，进行启动、关闭等操作
    :return app_kw_dict 应用关键词词典。用于提取实体
    """
    applist = []
    app_kw_dict = {}

    # 遍历 application 目录
    for app in path.iterdir():
        appname = app.name.replace('.app', '')
        appinfo = {
            "name": appname,
            "tag": [],
            "path": f"/System/Applications/{app.name}"
        }
        appinfo['tag'].append(appname)

        tag_list = [appname]

        # 遍历每个app子目录中符合标准的文件，从中取 CFBundleDisplayName 值
        for file in app.rglob('./InfoPlist.strings'):
            if file.is_file():
                # 复制 InfoPlist.strings 至tests文件下
                command_copy_file = ['cp', file, 'tests/']
                subprocess.run(command_copy_file)
                # 转换 InfoPlist.strings 为xml格式
                command_convert_to_xml = ['plutil','-convert','xml1','tests/InfoPlist.strings']
                subprocess.run(command_convert_to_xml)

                path = 'tests/InfoPlist.strings'
                with open(path, 'r') as f:
                    content = f.read().replace('\t','').splitlines()
                    # print(content)
                    try:
                        index_name = content.index('<key>CFBundleDisplayName</key>') + 1
                        name = content[index_name].replace('<string>','').replace('</string>','')
                        # print(name)
                        appinfo["tag"].append(name)
                        tag_list.append(name)
                    except Exception as ex:
                        # print(ex)
                        content

                command_remove_file = ['rm', 'tests/InfoPlist.strings']
                subprocess.run(command_remove_file)

                appinfo["tag"] = list(set(appinfo["tag"]))  # 去重
                tag_list = list(set(tag_list))

        applist.append(appinfo)
        app_kw_dict[appname] = tag_list
    return applist, app_kw_dict


# if __name__ == "__main__":
#     st = time.time()
#     applist, app_kw_dict = app_list(APP_PATH)
#     save_app(applist, app_kw_dict)
#     # query = App.select(App.path).where(App.tag.contains('企业微信'))
#     # for i in query:
#     #     pprint.pprint(i.path)

#     end = time.time()
#     print(end-st)
