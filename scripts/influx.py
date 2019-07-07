from scripts.shellcalls import *
from logging import error, warning, debug

# influxql https://docs.influxdata.com/influxdb/v1.7/query_language/data_exploration/
# influxcli https://docs.influxdata.com/influxdb/v1.7/tools/shell/


def check_installed():
    if not is_installed("influx"):
        install("influxdb-client")


class influx:
    connected = False
    host = None
    port = None

    def __init__(self):
        check_installed()

    def execute(self, influx_ql_cmd, database=None):
        if self.host == None:
            hoststring = "127.0.0.1"
        elif self.port == None:
            hoststring = self.host
        else:
            hoststring = self.host + " -port=" + self.port
        cmd = str.format("influx -host={} -execute '{}'",
                         hoststring, influx_ql_cmd)
        if database != None:
            cmd = str.format('{} -database="{}"', cmd, database)
        debug(cmd)
        raw_call(cmd, True)

    def check_connection(self):
        try:
            self.execute('show databases')
        except Exception as e:
            error("Unable to connect to host: " + str(e))
            return False
        return True

    def select(self, database, keys=[], tags=[], measurements=[], condition=""):
        """
            SELECT key1 .. keyN, tag1 .. tagN FROM measurements, WHERE condition
            Ignores tags if no keys where provided
        """
        # function to add quotes around items with map
        def add_quotes(string):
            return '"' + string + '"'
        if keys == []:
            # select all
            select_clause = '*'
        else:
            # join keys and tags if there are any
            keys = map(add_quotes, keys)
            select_clause = ', '.join(keys)
            if tags != []:
                tags = map(add_quotes, tags)
                select_clause = ', '.join(tags)
                ', '.join((keys, tags))
        if measurements == []:
            # need a measurement
            raise ValueError("No measurements given")
        measurements = map(add_quotes, measurements)
        # check for a where clause and adapt cmd
        cmd = "SELECT " + select_clause + " FROM " + ', '.join(measurements)
        if condition != "":
            cmd = cmd + " WHERE " + condition
        self.execute(cmd, database)


db = influx()
db.host = '192.168.1.2'
db.check_connection()
db.select("test", measurements=["test"])
