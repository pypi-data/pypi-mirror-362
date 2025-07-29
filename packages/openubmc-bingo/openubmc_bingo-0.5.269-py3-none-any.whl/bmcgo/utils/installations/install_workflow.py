#!/usr/bin/env python3
# encoding=utf-8
# 描述：安装流程配置
# Copyright (c) 2025 Huawei Technologies Co., Ltd.
# openUBMC is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from typing import Dict, List
from pathlib import Path
import yaml
from bmcgo.utils.tools import Tools
from bmcgo.utils.installations import install_consts


tools = Tools("install")


class InstallWorkflow:
    logger = tools.log
    _workflows: Dict[str, List[str]] = {}
    search_paths: List[Path] = [Path(__file__).resolve().parent / install_consts.PLUGIN_INSTALL_PLAN_PATH]

    @classmethod
    def discover_workflows(cls):
        for path in cls.search_paths:
            if not path.exists():
                cls.logger and cls.logger.warning(f"未找到安装配置路径：{str(path)}, 跳过")
                continue

            for yml_file in path.glob("*.yml"):
                with open(yml_file) as conf:
                    cls._workflows[yml_file.stem] = yaml.safe_load(conf)

    @classmethod
    def parse(cls, name: str) -> List[str]:
        workflow = cls._workflows.get(name)
        if not workflow:
            raise ValueError(f"未找到安装配置：{str(workflow)}")
        return workflow

    @classmethod
    def add_plan_dir(cls, directory: Path):
        if directory not in cls.search_paths:
            cls.search_paths.append(directory)

    @classmethod
    def get_all_plans(cls):
        return cls._workflows.keys()