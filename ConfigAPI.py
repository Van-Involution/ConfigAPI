# -*- coding: utf-8 -*-
import os
import yaml

PLUGIN_METADATA = {
    'id': 'config_api',
    'version': '0.0.1',
    'name': 'ConfigAPI',
    'description': 'Plugin config api',
    'author': ['hanbings','zhang_anzhi'],
    'link': 'https://github.com/hanbings/ConfigAPI'
}

class Config:
    def __init__(self, plugin_name, default: dict, config_name=None):
        # 注册默认项
        self.default = default
        # 建立该插件配置文件文件夹
        self.dir = os.path.join('config', plugin_name)
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        # 处理配置文件名称
        if config_name is None:
            config_name = plugin_name
        self.path = os.path.join(self.dir, f'{config_name}.yml')
        # 初始化
        self.data = None
        self._check()

    def _check(self):
        self._read()
        save_flag = False
        for key, value in self.default.items():
            if key not in self.data.keys():
                self.data[key] = value
                save_flag = True
        if save_flag:
            self._save()

    def _read(self):
        if os.path.isfile(self.path):
            with open(self.path) as f:
                self.data = yaml.safe_load(f)
        else:
            self.data = self.default
            self._save()

    def _save(self):
        with open(self.path, 'w') as f:
            yaml.dump(self.data, f)

    def __getitem__(self, key):
        if key not in self.data.keys():
            raise ValueError(key + ' is not in configuration')
        else:
            return self.data[key]

    def get(self, key):
        if key not in self.data.keys():
            raise ValueError(key + ' is not in configuration')
        else:
            return self.data[key]

    def set(self, key, value):
        """set configuration item"""
        if key not in self.default.keys():
            raise ValueError(key + ' has not registered')
        else:
            self.data[key] = value
            self._save()

    def reload(self):
        """reload config from file"""
        self._check()

    def reset_default(self):
        """reset all configuration to default"""
        self.data = self.default
        self._save()

    def get_default(self, key):
        """get default configuration item"""
        if key not in self.data.keys():
            raise ValueError(key + ' is not in configuration')
        else:
            return self.default[key]
