import copy
from functools import wraps

import allure

from giga_auto.parse.parse_case import ParseCase
from giga_auto.parse.parse_common import ParseCommon
from giga_auto.parse.parse_step import ParseStep
from giga_auto.conf.settings import settings, ManyBusiness


def case_allure_operation(case_data, variables):
    feature_name = variables['feature_variables']['name']
    story_name = variables['story_variables']['name']
    allure.dynamic.feature(feature_name)
    allure.dynamic.story(story_name)
    allure.dynamic.title(case_data['desc'])
    return feature_name, story_name


class CaseVariables:
    feature_name = ''
    story_name = ''
    feature_setup_result = True
    pre_feature_teardown = None
    pre_feature_variables = None
    story_setup_result = True
    pre_stroy_teardown = None
    pre_stroy_variables = None
    error = None


def apply_feature_setup(parse_case, featrue_name):
    # 处理feature setup
    if CaseVariables.feature_name != featrue_name:
        CaseVariables.feature_name = featrue_name
        try:
            parse_case.parse_hook('feature_setup')
        except Exception as e:
            CaseVariables.feature_setup_result = False
            CaseVariables.error = e
            raise
        else:
            CaseVariables.feature_setup_result = True
    elif not CaseVariables.feature_setup_result:
        raise CaseVariables.error


def apply_story_setup(parse_case, story_name):
    # 处理story setup
    if CaseVariables.story_name != story_name:
        CaseVariables.story_name = story_name
        try:
            parse_case.parse_hook('story_setup')
        except Exception as e:
            CaseVariables.story_setup_result = False
            CaseVariables.error = e
            raise
        else:
            CaseVariables.story_setup_result = True
    elif not CaseVariables.story_setup_result:
        raise CaseVariables.error


def case_decorate():
    def _wrapper(func):
        @wraps(func)
        def wrapper(self, case_data, variables, db, service):
            feature_name, story_name = case_allure_operation(case_data, variables)
            parse_case = ParseCase(case_data, variables, ManyBusiness(settings.business, service), db, service)
            parse_case.parse_others()
            parse_case.parse_variables()
            apply_feature_setup(parse_case, feature_name) # 处理feature_setup
            apply_story_setup(parse_case, story_name)   # 处理story_setup
            parse_case.parse_hook('case_setup')  # 处理用例初始化，失败不进入用例执行
            try: # 处理步骤,即用例主体内容
                steps = ParseCommon(case_data['steps'], parse_case.steps).parse_data()
                for step in steps:
                    ParseStep.step_main(step, variables, service, db, parse_case.validate)
            finally:
                parse_case.parse_hook('case_teardown')  # 处理teardown,无论如何都执行teardown操作
                parse_case.parse_hook('story_teardown')  # 根据story_flag标识判断是否需要执行story、feature级别teardown
                parse_case.parse_hook('feature_teardown') # 根据feature_flag标识判断是否需要执行feature级别teardown

        return wrapper

    return _wrapper


def case_parametrize(metafunc):
    import copy
    from giga_auto.utils import right_replace
    from giga_auto.yaml_utils import YamlUtils
    test_module_path = metafunc.module.__file__
    test_function_name = metafunc.function.__name__
    test_data_path = right_replace(test_module_path)
    test_data = YamlUtils(test_data_path).read()  # 读取整个yml文件数据
    feature_variables = test_data.get("variables", None)
    func_data = test_data.get(test_function_name, None)
    if feature_variables is not None and func_data is not None:
        story_variables = func_data.get("variables", {})
        variables = {"feature_variables": feature_variables, "story_variables": story_variables}
        feature_others = {k: test_data[k] for k in test_data if k != "variables" and not k.startswith('test_')}
        others = {k: func_data[k] for k in func_data if k not in ["case_data", "variables"]}
        variables['others'] = {'story': others, 'feature': feature_others}
        case_data = func_data["case_data"]
        case_data = [(case, copy.deepcopy(variables)) for case in case_data]  # 深度copy保证用例间variables隔离
        metafunc.parametrize("case_data,variables", case_data)
