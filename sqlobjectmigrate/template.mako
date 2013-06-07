from sqlobjectmigrate.migrationBase import MigrationBase

class ${name}(MigrationBase):

	def up(self):
	%if sql:
		self.runSqlFile(self.getSameSqlFile(__file__))
	%else:
		pass
	%endif