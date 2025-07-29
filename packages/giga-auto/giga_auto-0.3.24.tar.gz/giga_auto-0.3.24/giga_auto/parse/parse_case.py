import copy
from typing import Any

from giga_auto.parse.parse_base import ParseBase
from giga_auto.parse.parse_step import ParseStep


class ParseCase(ParseBase):

    def __init__(self, case_data, case_variables, business, db, service):
        self._variables = case_variables
        self.variables = {}
        self.case_data = case_data
        self.business = business
        self.db = db  # 这里的db是一个DBOperation实例
        self.business.db = db.get(service) if isinstance(db, dict) else db # 这里是一个数据库连接实例
        self.service = service

    def parse_variables(self):
        self._parse_feature_varialbes()
        self._parse_story_variables()
        self._parse_case_variables()

    def parse_others(self):
        """
        获取story公共的step、validate
        获取feature、story、case级别的setup以及teardown
        """
        others = self._variables.pop("others", {})
        feature, story = others.get("feature", {}), others.get('story', {})
        self.validate = {}
        self.steps = {}
        for k in story:
            if k.startswith('validate'):
                self.validate[k] = story[k]
            if k.startswith('steps'):
                self.steps[k] = story[k]
        self.feature_setup = feature.get("setup", [])
        self.feature_teardown = feature.get("teardown", [])
        self.story_setup = story.get("setup", [])
        self.story_teardown = story.get("teardown", [])
        self.case_setup = self.case_data.get("setup", [])
        self.case_teardown = self.case_data.get("teardown", [])

    def _parse_feature_varialbes(self):
        variables = self._variables.pop("feature_variables")
        self.traversal_assignments(variables)
        self.variables.update(variables)

    def parse_hook(self, hook_name='feature_setup'):
        """
        hook_name: feature_setup,feature_teardown,story_setup,story_teardown
        """
        assert hook_name in [
            'feature_setup', 'feature_teardown', 'story_setup', 'story_teardown', 'case_setup', 'case_teardown'], \
            "请检查hook_name，范围为：feature_setup,feature_teardown,story_setup,story_teardown,case_setup,case_teardown"
        if hook_name == 'story_teardown' and self.case_data.get('story_flag', None) is None:
            return
        if hook_name == 'feature_teardown' and self.case_data.get('feature_flag', None) is None:
            return
        for hook in getattr(self, hook_name):
            ParseStep.step_main(hook, self.variables, self.service, self.db, self.validate)

    def _parse_story_variables(self):
        variables = self._variables.pop("story_variables")
        self.traversal_assignments(variables)
        self.variables.update(variables)

    def _parse_case_variables(self):
        variables = self.case_data.pop("variables", {})
        self.traversal_assignments(variables)
        self.variables.update(variables)
        self._variables.update(self.variables)

    def get_func(self, value: str) -> Any:
        method = getattr(self.business, value)
        if method:
            return method
        else:
            raise AttributeError(f"business未获取到属性{value}")

    def get_var(self, value: str) -> Any:
        return self.variables[value]
