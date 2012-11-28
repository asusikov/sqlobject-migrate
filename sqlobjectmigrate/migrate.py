# -*- coding: utf-8 -*-
import os
import sys
import inspect

dirName = os.path.dirname(os.path.abspath(__file__))
dirName = os.path.abspath(os.path.join(dirName, os.path.pardir))
sys.path.append(dirName)
from sqlobjectmigrate.migrationBase import MigrationBase

# Получать снаружи
projectDir = "/home/sas/bigbird/trunk"

migrationDir = os.path.abspath(os.path.join(projectDir, "db"))
sys.path.append(projectDir)
sys.path.append(migrationDir)

import migration

baseCls = MigrationBase
subclasses = []

for moduleStr in dir(migration):
    module = getattr(migration, moduleStr)
    if inspect.ismodule(module):
        for clsStr in dir(module):
            cls = getattr(module, clsStr)
            if inspect.isclass(cls):
                if clsStr == baseCls.__name__:
                    continue
                if issubclass(cls, baseCls):
                    subclasses.append(cls)

for migrationClass in subclasses:
    migrationClass().up()
