"""

Xerenity python library
"""

__version__ = "0.1.3"
__author__ = 'Xerenity'

from xerenity.connection.db import Connection
from xerenity.search.series import Series


class Xerenity:

    def __init__(self, username, password):
        self.username: username
        self.password = password
        self.conn = Connection()
        self.conn.login(username=username, password=password)
        self.series: Series = Series(connection=self.conn)
