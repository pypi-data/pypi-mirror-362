from __future__ import print_function
import sys
from .runtime import BuiltinFunction
import json


PYTHON3 = (sys.version[0] == '3')

if PYTHON3:
    # For Python 3.0 and later
    from urllib.request import urlopen
else:
    # Fall back to Python 2's urllib2
    from urllib import urlopen

def tamil_urlopen(*args):
    html = urlopen(*args)
    return html

def tamil_urlread(html):
    data = html.read()
    if not PYTHON3:
        return data.decode("utf-8")
    return data

def tamil_urlclose(html):
    html.close()

def Load_URL_APIs(interpreter):
    interpreter.add_builtin("urlopen",tamil_urlopen,nargin=1,ta_alias="இணைய_இணைப்பு_திற")
    interpreter.add_builtin("urlread",tamil_urlread,nargin=1,ta_alias="இணைய_இணைப்பு_படி")
    interpreter.add_builtin("urlclose",tamil_urlclose,nargin=1,ta_alias="இணைய_இணைப்பு_மூடு")
    # JSON
    interpreter.add_builtin("json_loads",json.loads,nargin=1)
    interpreter.add_builtin("json_load",json.load,nargin=1)
    interpreter.add_builtin("json_dump",json.dump,nargin=1)
    interpreter.add_builtin("json_dumps",json.dumps,nargin=1)
