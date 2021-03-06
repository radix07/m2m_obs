from jinja2 import Markup
import time
from datetime import datetime,timedelta

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):                
        return Markup("<script>document.write(moment(\"%s\").%s);</script>" % (self.timestamp, format))

    def renderRaw(self, format):                
        return Markup("<script>document.write(moment(%s).%s);</script>" % (self.timestamp, format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

    def epoch(self):
        return self.renderRaw("calendar()")
