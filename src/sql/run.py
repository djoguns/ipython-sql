import sqlalchemy
import types
import prettytable
import sys

class ResultSet(list):
    def __init__(self, sqlaproxy, sql, config):
        self.keys = sqlaproxy.keys()
        self.sql = sql
        self.limit = config.get('limit')
        style_name = config.get('style', 'DEFAULT')
        self.style = prettytable.__dict__[style_name.upper()]
        if sqlaproxy.returns_rows:
            if self.limit:
                list.__init__(self, sqlaproxy.fetchmany(size=self.limit))
            else:
                list.__init__(self, sqlaproxy.fetchall())
            self.pretty = prettytable.PrettyTable(self.keys)
            for row in self:
                self.pretty.add_row(row)
            self.pretty.set_style(self.style)
        else:
            list.__init__(self, [])
            self.pretty = None
    def _repr_html_(self):
        if self.pretty:
            return self.pretty.get_html_string()
        else:
            return None
    def __str__(self, *arg, **kwarg):
        return str(self.pretty or '')

def run(conn, sql, config):
    if sql.strip():
        statement = sqlalchemy.sql.text(sql)
        return ResultSet(conn.session.execute(statement), sql, config) 
    else:
        return 'Connected: %s' % conn.name
     