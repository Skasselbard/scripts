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

    def check_connection(self):
        if self.host == None:
            hoststring = "127.0.0.1"
        elif self.port == None:
            hoststring = self.host
        else:
            hoststring = self.host + " -port=" + self.port
        try:
            cmd = str.format(
                "influx -host={} -execute 'show databases'", hoststring)
            debug(cmd)
            raw_call(cmd, True)
        except Exception as e:
            error("Unable to connect to host: " + str(e))
            return False
        return True


db = influx()
db.host = '192.168.1.'
db.check_connection()
