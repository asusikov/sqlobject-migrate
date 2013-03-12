# -*- coding: utf-8 -*-
import os
import sys
import inspect

from sqlobjectmigrate.migrationBase import MigrationBase
from sqlobjectmigrate.version import Version

projectDir = os.getcwd()
migrationDir = os.path.abspath(os.path.join(projectDir, "db"))
sys.path.append(projectDir)
sys.path.append(migrationDir)
import migration

baseCls = MigrationBase
migrationOrder = []
subclasses = {}

for moduleStr in dir(migration):
    module = getattr(migration, moduleStr)
    if inspect.ismodule(module):
        base = os.path.basename(module.__file__)
        migrationNumber = os.path.splitext(base)[0].split('_')[0]
        for clsStr in dir(module):
            cls = getattr(module, clsStr)
            if inspect.isclass(cls):
                if clsStr == baseCls.__name__:
                    continue
                if issubclass(cls, baseCls):
                    migrationOrder.append(migrationNumber)
                    subclasses[migrationNumber] = cls
                    break

Version.createTable(ifNotExists = True)

def main():
    for migrationNumber in migrationOrder:
        if not Version.select(Version.q.number == migrationNumber).count():
            subclasses[migrationNumber]().upVersion(migrationNumber)
