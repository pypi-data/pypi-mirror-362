import os
from typing import Any

import allure

from giga_auto.base_class import Response
from giga_auto.parse.parse_base import ParseBase
from giga_auto.conf.settings import settings, ManyBusiness
from giga_auto.base_class import OperationApi
from giga_auto.parse.parse_common import ParseCommon


class ParseStep(ParseBase):

    def __init__(self, step_data, case_variables, business, db_instance):
        """这里的business是ManyBusiness对象，db_instace是数据库实例"""
        self.variables = case_variables
        self.step_data = step_data
        self.business = business
        self.business.db = db_instance

    def parse_condition(self):
        conditions=[]
        for k in self.step_data:
            if k.startswith('condition'):
                assert isinstance(self.step_data[k], list), "condition must be list"
                conditions.append(self.step_data[k])
        self.traversal_assignments(conditions)
        conditions=[all(c) for c in conditions]
        return not conditions or any(conditions)

    def parse_params(self, key='params'):
        params = self.step_data.get(key, {})
        if isinstance(params, str):
            self.step_data[key] = self.traversal_assignments(params)
        else:
            self.traversal_assignments(params)

    def parse_files(self):
        files = self.step_data.get('files', None)
        if files is None:
            return {}
        file_values = []
        for k, path in files.items():
            if isinstance(path, str): path = [path]
            # path不是列表就是字符串，传错了会直接抛异常文件不存在
            for p in path:
                p = os.path.join(settings.Constants.STATIC_DIR, p.replace('\\', os.sep).replace('/', os.sep))
                file_values.append((k, (os.path.basename(p), open(p, 'rb'))))
        return {'files': file_values}

    def parse_validate(self, response):
        """处理断言，先处理数据库或者变量取值，在处理content开头的值"""
        validate = self.step_data.get('validate', [])
        self.traversal_assignments(validate)
        self._content_validate(validate, response)
        self.step_data['validate'] = validate

    def _content_validate(self, validates, res):
        """根据规则解析"""
        res = Response(res)
        for val in validates:
            for k, v in val.items():
                actual = v[0]
                if isinstance(actual, str):
                    if actual.startswith('content') or actual.startswith('response'):
                        actual = getattr(res, actual)
                v[0] = actual

    def parse_extract(self, response):
        """获取吐出变量更新到variables"""
        response = Response(response)
        extract = self.step_data.get('extract', {})
        for k, v in extract.items():
            allure.attach(f'获取变量key:{k},值路径：{v}')
            extract[k] = getattr(response, v)
        self.variables.update(extract)

    def parse_function(self):
        """解析除接口请求之外的步骤,只可能调用business函数,必须以function作为步骤标识"""
        self.step_data['function'] = self.traversal_assignments(self.step_data['function'])
        return self.step_data['function']

    def get_func(self, value: str) -> Any:
        method = getattr(self.business, value)
        if method:
            return method
        else:
            raise AttributeError(f'business未获取到属性{value}')

    def get_var(self, value: str) -> Any:
        mid_value = self.variables
        if '.' in value:
            for k in value.split('.'):
                if not k.strip(): continue
                mid_value = mid_value[k] if isinstance(mid_value, dict) else mid_value[int(k)]
        else:
            mid_value = mid_value[value]
        return mid_value

    @staticmethod
    def step_main(step, variables, service, db, common_validate):
        """这里的db参数都是DBOperation类"""
        # 根据service和account_key获取登录用户信息加到variables中,优先级step>case_variable>feature_variable
        account_key = step.get('account_key') or variables.get('account_key') or 'admin'
        service = step.get('service') or variables.get('service') or service
        variables.update(settings.admin_config[service][account_key])  # 更新登录用户信息，user,pwd
        db_instance = db.get(service, step.get('db_key', None)) # 获取数据库实例，db_key是因为美国drp存在多个数据库
        parse_step = ParseStep(step, variables, ManyBusiness(settings.business, service), db_instance)
        if not parse_step.parse_condition(): # 判断条件为false，就不走该步骤
            return
        if 'params' in step:  # 根据params判断是否走接口请求
            api_request = OperationApi().aggregate_api[service](
                service=service, account_key=account_key, reload_login=step.pop('reload_login', False),
                need_login=step.get('need_login', True))
            parse_step.parse_params()
            files = parse_step.parse_files()
            params = step['params']
            assert 'files' not in params, 'params不能出现files键值'
            params.update(files)
            api_method = step.get('api_method', None) or variables['api_method']
            resp = getattr(api_request, api_method)(**params)
        else:
            resp = parse_step.parse_function()  # 处理函数步骤
        parse_step.parse_extract(resp)
        step['validate'] = ParseCommon(step.get('validate', []), common_validate).parse_data()
        parse_step.parse_validate(resp)
        settings.assert_class().validate(step['validate'])
