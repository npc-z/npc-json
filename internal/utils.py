import inspect
import os
from datetime import datetime

from rich import print


def log(*args, **kw):
    now = str(datetime.now()).rsplit(".")[0]
    # 0 represents this line
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]

    info = inspect.getframeinfo(frame)
    file = info.filename
    path = os.path.realpath(file)
    func = info.function
    lineno = info.lineno

    print(f'{now} - File "{path}", line {lineno}\n', *args, **kw)
