# -*- coding: utf-8 -*-
import os
import sys
import inspect
import optparse

def getDbDir():
    return os.path.join(os.getcwd(), 'db')

def getMigrationDir():
    migrationDir = os.path.join(getDbDir(), 'migration')
    return migrationDir

def getInitFilePath():
    return os.path.join(getMigrationDir(), '__init__.py')

def init():
    print '===== init ====='
    if os.path.exists(getDbDir()):
        print '--> db folder exists'
    else:
        print '--> create db folder'
        os.makedirs(getDbDir())
    if os.path.exists(getMigrationDir()):
        print '--> migration folder exists'
    else:
        print '--> create migration folder'
        os.makedirs(getMigrationDir())
    if os.path.exists(getInitFilePath()):
        print '--> init file exists'
    else:
        print '--> create init file'
        open(getInitFilePath(), 'w').close()

def checkFolders():
    if not os.path.exists(getDbDir()):
        print 'Db folder does not exist. Run init command.'
        return False
    if not os.path.exists(getMigrationDir()):
        print 'Migration folder does not exist. Run init command.'
        return False
    if not os.path.exists(getInitFilePath()):
        print 'Init file does not exist. Run init command.'
        return False
    return True

def up():

    if not checkFolders():
        return

    from sqlobjectmigrate.migrationBase import MigrationBase
    from sqlobjectmigrate.version import Version

    sys.path.append(os.getcwd())
    sys.path.append(getDbDir())
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

def generate(name, generateSql):
    print '===== generate migration ====='
    if not checkFolders():
        return 
    from mako.template import Template
    import time

    number = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    
    fileNameTemplate = Template('${number}_${name}')
    fileName = fileNameTemplate.render(number = number, name = name)
    templateDir = os.path.split(os.path.abspath(__file__))[0]
    templateName = os.path.join(templateDir, 'template.mako')
    fileTemplate = Template(filename = templateName)
    nameCapitalize = name[0].capitalize() + name[1:]
    with open(getInitFilePath(), 'a') as initFile:
        initFile.write('__import__(\'migration.%s\')\n' % fileName)
    fullFileName = os.path.join(getMigrationDir(), fileName + '.py')
    print '--> write file %s.py' % fileName
    with open(fullFileName, 'w') as file:
        file.write(fileTemplate.render(name = nameCapitalize))
    if generateSql:
        fullSqlFileName = os.path.join(getMigrationDir(), fileName + '.sql')
        print '--> write sql file %s.sql' % fileName
        open(fullSqlFileName, 'w').close()

def main(args = sys.argv[1:]):

    parser = optparse.OptionParser()

    parser.add_option('-g', '--generate',
        dest = 'generate',
        action = 'store_true',
        default = False,
        help = 'Run generator')

    parser.add_option('--init',
        dest = 'init',
        action = 'store_true',
        default = False,
        help = 'Initialize folders')

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
    parser.add_option('--sql',
        dest = 'generateSql',
        action = 'store_true',
        default = False,
        help = 'Generate with sql file')

    options, args = parser.parse_args(args)
    if options.init:
        init()
        return
    if options.generate:
        if len(args) > 0:
            generate(args[0], options.generateSql)
        return
    if options.up:
        up()
        return
    if options.down:
        down()
        return

if __name__ == '__main__':
    main()
