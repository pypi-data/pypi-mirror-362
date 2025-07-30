import os
from idlelib.replace import replace
from typing import Any

import allure

from giga_auto.base_class import Response
from giga_auto.parse.parse_base import ParseBase
from giga_auto.conf.settings import settings


class ParseCommon(ParseBase):

    def __init__(self, data,common):
        self.data=data # $steps_1
        self.common=common # {'steps_1': [{'function': "${generate_str($length)}","extract":{'paramData':'$'}}]}

    def parse_data(self):
        new_data=[]
        for item in self.data:
            if not isinstance(item, str): 
                new_data.append(item)
            else:
                k=self.pattern_var.findall(item)[0][1]
                apply_data=self.common[k]
                new_data.extend(apply_data)
        return new_data

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
