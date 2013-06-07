from version import Version
from sqlobject import sqlhub
import os

class MigrationBase(object):

    def getSameSqlFile(self, file):
        fileName = os.path.abspath(file)
        return os.path.splitext(fileName)[0] + '.sql'

    def runSqlFile(self, fileName):
        print '--> run sql from %s' % fileName
        read_data = None
        with open(fileName, 'r') as f:
            read_data = f.read()
        if read_data:
            sqlhub.getConnection().query(read_data)

    def getColumnDefinition(self, objectClass, columnName):
        return objectClass.sqlmeta.columnDefinitions[columnName].withClass(objectClass.sqlmeta.soClass)

    def addColumn(self, objectClass, columnName):
        print '--> add column %s to %s' % (columnName, objectClass.sqlmeta.table)
        sqlhub.getConnection().addColumn(objectClass.sqlmeta.table, self.getColumnDefinition(objectClass, columnName))

    def deleteColumn(self, objectClass, columnName):
        print '--> remove column %s from %s' % (columnName, objectClass.sqlmeta.table)
        sqlhub.getConnection().delColumn(objectClass.sqlmeta, self.getColumnDefinition(objectClass, columnName))

    def up(self):
        pass

    def upVersion(self, number):
    	print '===== migration up - %s =====' % number
        self.up()
        Version(number = number)
