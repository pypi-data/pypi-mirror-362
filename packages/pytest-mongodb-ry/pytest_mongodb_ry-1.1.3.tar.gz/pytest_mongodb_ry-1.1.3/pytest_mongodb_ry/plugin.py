import json
import os
import time
from datetime import datetime
from typing import Optional, List, Dict
import pymongo
import pytest


class MongoClient(object):
    _alive = {}

    def __new__(cls, url, *args, **kwargs):
        '''
        享元模式处理
        :param url:
        :param args:
        :param kwargs:
        '''
        if url in cls._alive.keys():
            return cls._alive.get(url)
        else:
            NewObject = object.__new__(cls)
            cls._alive.update({url: NewObject})
            return NewObject

    def __init__(self, url, Database):
        '''
        生成访问mongodb的实例
        :param url: mongodb的地址
        '''
        self.client = pymongo.MongoClient(f"mongodb://{url}")[Database]

    def insert(self, table, documents: Optional[List[Dict]]):
        '''
        新增数据至mongodb，返回对应新增的id值
        :param table:
        :param documents:
        :return:
        '''
        collection = self.client[table]
        x = collection.insert_many(documents)
        return x.inserted_ids

    def select(self, table, data: dict, sortdata: str):
        '''
        从mongodb对应文档中查询数据查询对应数据
        :param table:文档名
        :param data:指定的查询条件
        :return:
        '''
        collection = self.client[table]
        result = collection.find(data).sort(sortdata, -1)
        return result.to_list()

def pytest_addoption(parser):
    '''
    新增对应参数
    :param parser:
    :return:
    '''
    parser.addini(
        name="Mode",
        default="",
        help="模式选择：one.单个接口读取；more.套件模式读取用例"
    )
    parser.addini(
        name="is_Mongodb",
        default="",
        help="是否开启对应mongodb开关"
    )
    parser.addini(
        name="MongoDb_url",
        default="",
        help="mongodb对应路径"
    )
    parser.addini(
        name="MgTable",
        default="",
        help="mongodb的库名"
    )
    parser.addini(
        name="Collection",
        default="",
        help="mongodb的Collection名"
    )
    parser.addini(
        name="Package_Collection",
        default="",
        help="mongodb的测试套件Collection名"
    )
    parser.addini(
        name="MongoDb_SQL",
        default="",
        help="mongodb的查询SQL"
    )
    parser.addini(
        name="Author",
        default="",
        help="使用者"
    )

    parser.addoption(
        "--is_Mongodb",
        default="",
        help="是否开启对应mongodb开关"
    )
    parser.addoption(
        "--Mode",
        default="",
        help="模式选择：one.单个接口读取；more.套件模式读取用例"
    )

    parser.addoption(
        "--MongoDb_url",
        default="",
        help="mongodb对应路径"
    )
    parser.addoption(
        "--MgTable",
        default="",
        help="mongodb的库名"
    )
    parser.addoption(
        "--Collection",
        default="",
        help="mongodb的Collection名"
    )
    parser.addoption(
        "--Package_Collection",
        default="",
        help="mongodb的测试套件Collection名"
    )
    parser.addoption(
        "--MongoDb_SQL",
        default="",
        help="mongodb的查询SQL"
    )
    parser.addoption(
        "--Author",
        default="",
        help="使用者"
    )


Config_dict = []  # Mongodb基本配置信息
test_result = []  # 测试结果集合
error_result = [] #错误结果集合
rootdir = None  # 项目根目录


def pytest_generate_tests(metafunc):
    # 获取对应配置信息
    global Config_dict
    Config_dict = {
        "author": metafunc.config.inicfg.get("Author") if not (metafunc.config.option.Author) else (
            metafunc.config.option.Author),
        "mode": metafunc.config.inicfg.get("Mode") if not (metafunc.config.option.Mode) else (
            metafunc.config.option.Mode),
        "is_MongoDb": metafunc.config.inicfg.get("is_Mongodb") if not (metafunc.config.option.is_Mongodb) else (
            metafunc.config.option.is_Mongodb),
        "url": metafunc.config.inicfg.get("MongoDb_url") if not (metafunc.config.option.MongoDb_url) else (
            metafunc.config.option.MongoDb_url),
        "database": metafunc.config.inicfg.get("MgTable") if not (metafunc.config.option.MgTable) else (
            metafunc.config.option.MgTable),
        "collection": metafunc.config.inicfg.get("Collection") if not (metafunc.config.option.Collection) else (
            metafunc.config.option.Collection),
        "package_collection": metafunc.config.inicfg.get("Package_Collection") if not (metafunc.config.option.Package_Collection) else (
            metafunc.config.option.Package_Collection),
        "Sql_Path": metafunc.config.inicfg.get("MongoDb_SQL") if not (metafunc.config.option.MongoDb_SQL) else (
            metafunc.config.option.MongoDb_SQL)
    }
    if Config_dict['is_MongoDb'].upper() == "TRUE":
        # 获取项目对应路径
        global rootdir
        rootdir = metafunc.config._parser.extra_info['rootdir']
        jsondir = rootdir + f"/{Config_dict['Sql_Path']}"
        # 开启对应进程
        Client = MongoClient(Config_dict['url'], Config_dict['database'])
        with open(jsondir, encoding="utf-8") as f:
            SQL_data = json.loads(f.read())

        test_data = []
        if Config_dict['mode'].upper() == "MORE":
            for i in SQL_data['select']:
                test_data += Client.select(Config_dict["package_collection"], i, "create_time")
            # 套件模式读取用例
            for i in test_data:
                i['reqs'] = []
                i['mode'] = Config_dict['mode']
                # 获取每个套件包含的接口详情
                for j in i['paths']:
                    i['reqs'] += Client.select(Config_dict["collection"], {"request.path": j, "epic":i["epic"]}, "create_time")
                del i['paths']
        else:
            # 读取对应SQL数据
            for i in SQL_data['select']:
                test_data += Client.select(Config_dict["collection"], i,"create_time")
            for z in test_data:
                z['mode'] = 'one'
        if "data" in metafunc.fixturenames:
            metafunc.parametrize("data", test_data)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    每个测试用例结束时触发
    """
    # 获取钩子方法的调用结果，返回一个result对象
    out = yield
    # 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    # 获取当前的测试用例数据
    caseInfo = item.__dict__['callspec'].params['data']
    # 构建测试结果字典
    if report.when == "call":
        global test_result, error_result
        # if report.outcome == "failed":
        #     report.longrepr = f"{report.longrepr}\n{call.excinfo}"
        data = {
                "epic": caseInfo['epic'],
                "type": caseInfo['type'],
                "feature": caseInfo['feature'],
                "story": caseInfo['story'],
                "author": caseInfo['author'],
                "outcome": report.outcome,  # 测试结果（'passed', 'failed', 'skipped' 等）
                # "exception_info": report.longrepr,
                "start_time": datetime.fromtimestamp(report.start).strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.fromtimestamp(report.stop).strftime("%Y-%m-%d %H:%M:%S"),
                "duration": report.duration}
        mode = caseInfo.get('mode', 'one')
        if mode.upper() == "MORE":
            # 套件模式读取用例
            data['paths'] = caseInfo['reqs']
            data["id"] = caseInfo['_id']
        else:
            data["title"] = caseInfo['title']
            data["env"] = caseInfo['env']
            data["path"] =  caseInfo['request']['path']
            data["method"] = caseInfo['request']['method']
        # test_result.append(data)
        if report.outcome == "failed":
            error_result.append(data)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集测试结果，生成测试报告
    """
    try:
        reports = []
        reports.append({
            "author": Config_dict['author'],
            "total": terminalreporter._numcollected,
            "passed": len(terminalreporter.stats.get('passed', [])),
            "failed": len(terminalreporter.stats.get('failed', [])),
            "error": len(terminalreporter.stats.get('error', [])),
            "skipped": len(terminalreporter.stats.get('skipped', [])),
            "duration": datetime.now().timestamp() - terminalreporter._sessionstarttime,
            "success_rate": (len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100),
            "create_time": datetime.now(),
            # "test_result": test_result,
            "error_result": error_result
        })
        # 创建 MongoClient 实例，进行插入操作
        Client = MongoClient(Config_dict['url'], Config_dict['database'])
        Client.insert("api_report", reports)
    except Exception as e:
        # 插入失败时，输出错误信息并将 test_result 保存到 JSON 文件
        result_dir = os.path.join(rootdir, "package", "json_package")
        os.makedirs(result_dir, exist_ok=True)
        result_filename = os.path.join(result_dir, f"test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        # 将 test_result 转为 JSON 格式并保存
        with open(result_filename, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=4)