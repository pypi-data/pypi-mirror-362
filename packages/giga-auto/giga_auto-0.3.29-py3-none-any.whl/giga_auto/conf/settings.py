import inspect
import os
import importlib


class ManyBusiness:

    def __init__(self, module_map, service_key):
        self._business = module_map['default'].copy()
        self._business.extend(module_map.get(service_key, []))
        self._check_repeate = False
        self._db = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, _db):
        self._db = _db
        for business in self._business:
            business.db = _db

    def __check_repeate(self):
        method_name_list = []
        for m in self._business:
            method_name_list.extend([name for name, obj in inspect.getmembers(m)
                                     if inspect.isfunction(obj) and obj.__module__ == m.__name__])
        repeat_method = list(filter(lambda x: method_name_list.count(x) > 1, method_name_list))
        assert not repeat_method, f'出现重复方法名：{repeat_method}'
        self._check_repeate = True

    def __getattr__(self, item):
        if not self._check_repeate:
            self.__check_repeate()
        for business in self._business:
            if hasattr(business, item):
                return getattr(business, item)
        else:
            raise AttributeError('%s is not found in %s business' % (item, self.service_key))


class LazySettings(object):

    def __init__(self):
        self._settings = None

    def __dynamic_import_business(self, file, business_dir, module_map, key=None):
        file_path = os.path.join(business_dir, file)
        module_path = os.path.relpath(file_path, self.Constants.BASE_DIR).replace(os.sep, '.')[:-3]
        module = importlib.import_module(module_path)
        key = key or file.replace('.py', '')
        if key in module_map:
            module_map[key].append(module)
        else:
            module_map[key] = [module]

    def __get_module_map(self):
        module_map = {'default': [importlib.import_module('giga_auto.parse.business')]}
        try:
            module_map['default'].append(importlib.import_module('common.business'))
        except ModuleNotFoundError:
            pass
        business_dir = os.path.join(self.Constants.BASE_DIR, 'business')
        for file in os.listdir(business_dir):
            if file.endswith('.py') and file.replace('.py', '') in self.ServiceKey.config.values():
                self.__dynamic_import_business(file, business_dir, module_map)
            elif file in settings.ServiceKey.config.values():
                module_map[file] = []
                for root, dirs, files in os.walk(os.path.join(business_dir, file)):
                    for f in files:
                        if f.endswith('.py') and not f.startswith('__'):
                            self.__dynamic_import_business(f, root, module_map, file)
        return module_map

    def _set_business(self, name):
        if name == 'business':
            if not hasattr(self, '_business'):
                self._business = self.__get_module_map()
            return self._business
        return None

    def _set_assert_class(self, name):
        if name == 'assert_class':
            return self._get_class(name, 'giga_auto.assert_utils.AssertUtils')
        return None

    def _set_login_class(self, name):
        if name == 'login_class':
            return self._get_class(name, 'common.login.Login')
        return None

    def _get_module(self, name, default=None):
        """必须"""
        module_path: str = getattr(self._settings, name.upper(), default)
        if module_path is None:
            raise ValueError('%s is not set in settings' % name.upper())
        return importlib.import_module(module_path)

    def _get_class(self, name, default=None):
        assert_class_path: str = getattr(self._settings, name.upper(), default)
        if assert_class_path is None:
            raise ValueError('%s is not set in settings' % name.upper())
        module, class_obj = assert_class_path.rsplit('.', 1)
        return getattr(importlib.import_module(module), class_obj)

    def _set_main(self, name):
        return (self._set_business(name)
                or self._set_assert_class(name)
                or self._set_login_class(name)
                or getattr(self._settings, name))

    def __getattr__(self, name):
        if self._settings is None:
            module_path = os.environ['GIGA_SETTINGS_MODULE']
            self._settings = importlib.import_module(module_path)
        return self._set_main(name)


settings = LazySettings()
