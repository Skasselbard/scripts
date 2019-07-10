from logging import error, warning, debug
import requests
from json import dumps

# influxql https://docs.influxdata.com/influxdb/v1.7/query_language/data_exploration/
# influxcli https://docs.influxdata.com/influxdb/v1.7/tools/shell/


def pretty(json):
    return dumps(json, indent=1)


class influx:
    connected = False
    host = None
    port = None

    def __init__(self, host="127.0.0.1", port=8086):
        self.host = host
        self.port = port
        self.check_connection

    def query(self, query, db=None):
        request = str.format("http://{}:{}/query?", self.host, self.port)
        if db != None:
            request = str.format("{}db={}", request, db)
        r = requests.get(request, params={'q': query})
        debug(r.url)
        if not r.ok:
            error(r.text)
            r.raise_for_status()
        debug(pretty(r.json()))
        return r.json()

    def check_connection(self):
        try:
            self.query('show databases')
        except Exception as e:
            error("Unable to connect to host: " + str(e))
            return False
        return True

    def show_databases(self):
        return self.query("show databases")

    def show_queries(self):
        return self.query("show queries")

    def show_meassurements(self):
        return self.query("show measurements")

    def show_diagnostics(self):
        return self.query("show diagnostics")

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
        self.query(cmd, database)


db = influx('192.168.1.2', 8086)
# db.host='192.168.1.2'
# db.port=8086
# db.query("")
# db.check_connection()
#db.select("test", measurements=["test"])
print(pretty(db.show_databases()))
print(pretty(db.show_diagnostics()))
print(pretty(db.show_meassurements()))
print(pretty(db.show_queries()))
