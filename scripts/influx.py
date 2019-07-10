from logging import error, warning, debug
import requests
from json import dumps

# influxql https://docs.influxdata.com/influxdb/v1.7/query_language/data_exploration/
# influxcli https://docs.influxdata.com/influxdb/v1.7/tools/shell/

# https://docs.influxdata.com/influxdb/v1.7/query_language/spec/#dates-times
timeformat = "%Y-%m-%d %H:%M:%S"  # plus microseconds -> seems to be isoformat


def pretty(json):
    return dumps(json, indent=1)


class Influx:
    host = None
    port = None
    database = None
    show = None

    def __init__(self, host="127.0.0.1", port=8086):
        self._construct(host, port)
        self.check_connection()
        self.database = _DataBase(host, port)
        self.show = _Show(host, port)

    # break recursion
    def _construct(self, host, port):
        self.host = host
        self.port = port

    def check_connection(self):
        request = str.format("http://{}:{}/ping", self.host, self.port)
        try:
            requests.get(request)
        except Exception as e:
            error("Unable to connect to host: " + str(e))
            return False
        return True

    def _query(self, query, db=None):
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

    def _write(self, data, db=None):
        request = str.format("http://{}:{}/write?", self.host, self.port)
        if db != None:
            request = str.format("{}db={}", request, db)
        r = requests.post(request, {'q': data})
        debug(r.url)
        if not r.ok:
            error(r.text)
            r.raise_for_status()
        debug(pretty(r.json()))
        return r.json()

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
        self._query(cmd, database)


class _DataBase(Influx):
    def __init__(self, host, port):
        self._construct(host, port)

    def create(self, name):
        return self._query(str.format('create database "{}"', name))

    def drop(self, name):
        return self._query(str.format('drop database "{}"', name))


class _Show(Influx):
    def __init__(self, host, port):
        self._construct(host, port)

    def databases(self):
        return self._query("show databases")

    def queries(self):
        return self._query("show queries")

    def meassurements(self):
        return self._query("show measurements")

    def diagnostics(self):
        return self._query("show diagnostics")


db = Influx('192.168.1.2', 8086)
# db.select("test", measurements=["test"])
# print(pretty(db.show_diagnostics()))
# print(pretty(db.show_meassurements()))
# print(pretty(db.show_queries()))
# print(db.database.drop("asda"))
print(pretty(db.show.databases()))
