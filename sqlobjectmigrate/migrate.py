# -*- coding: utf-8 -*-
import os
import sys
import inspect
import optparse

def up():
    from sqlobjectmigrate.migrationBase import MigrationBase
    from sqlobjectmigrate.version import Version

    projectDir = os.getcwd()
    migrationDir = os.path.abspath(os.path.join(projectDir, 'db'))
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
    for migrationNumber in migrationOrder:
        if not Version.select(Version.q.number == migrationNumber).count():
            subclasses[migrationNumber]().upVersion(migrationNumber)

def down():
    print 'down'

def generate(name):
    print 'generate'
    from mako.template import Template
    import time

    number = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    
    fileNameTemplate = Template('${number}_${name}.py')
    print fileNameTemplate.render(number = number, name = name)
    templateDir = os.path.split(os.path.abspath(__file__))[0]
    templateName = os.path.join(templateDir, 'template.mako')
    fileTemplate = Template(filename = templateName)
    nameCapitalize = name[0].capitalize() + name[1:-1]
    print fileTemplate.render(name = nameCapitalize)

def main(args = sys.argv[1:]):

    parser = optparse.OptionParser()
    parser.add_option('-g', '--generate',
                      dest = 'generate',
                      action = 'store_true',
                      default = False,
                      help = 'Run generator')

    parser.add_option('-u', '--up',
                      dest = 'up',
                      action = 'store_true',
                      default = False,
                      help = 'Up database')

    parser.add_option('-d', '--down',
                      dest = 'down',
                      action = 'store_true',
                      default = False,
                      help = 'Down database')

    options, args = parser.parse_args(args)
    
    if options.generate:
        if len(args) > 0:
            generate(args[0])
        return
    if options.up:
        up()
        return
    if options.down:
        down()
        return

if __name__ == '__main__':
    main()
