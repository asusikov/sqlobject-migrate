import sqlobject

class Version(sqlobject.SQLObject):

    number = sqlobject.UnicodeCol(length = 125)