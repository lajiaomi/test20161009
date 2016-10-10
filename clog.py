# coding: utf-8

import os
import sys
import time
import inspect
import datetime
import threading


# FORMAT_V1 = 'T{pid} {asctime} [{filename}:{lineno:>4}] {message}'
FORMAT_TF = '[{timestamp}][{uid}][{level_name}][{message}][{status}]'

# class _LoggerObject(object):
#     def __init__(self, logger, trans, action):
#         self.logger = logger
#         self.trans = trans
#         self.action = action
        
#     def start(self, name):
#         self.logger._write('%s/%s begin', self.trans, self.action, start=True)
    
#     def success(self):
#         self.logger._write('%s/%s success', self.trans, self.action, start=False)

#     def error(self):
#         self.logger._write('%s/%s fail', self.trans, self.action, start=False)

#     def __enter__(self):
#         self.logger._write('%s/%s begin', self.trans, self.action, start=True)
    
#     def __exit__(self, type, value, traceback):
#         # TODO(ssx): fix here
#         if traceback:
#             self.logger._write('%s/%s fail', self.trans, self.action, start=False)
#         else:
#             self.logger._write('%s/%s success', self.trans, self.action, start=False)

#     def __call__(self, fn):
#         def inner(*args, **kwargs):
#             self.logger._write('%s/%s begin', self.trans, self.action)
#             try:
#                 ret = fn(*args, **kwargs)
#                 self.logger._write('%s/%s success', self.trans, self.action)
#                 return ret
#             except Exception, e:
#                 self.logger._write('%s/%s fail', self.trans, self.action)
#                 raise e
#         return inner


class _Logger(object):
    lock = threading.Lock()

    def __init__(self, file=None, auto_flush=True, format=FORMAT_TF):
        self._format = format
        self._auto_flush = auto_flush
        if file:
            self._fobj = open(file, 'a')
        else:
            self._fobj = sys.stdout
    
    def flush(self):
        if self._fobj and self._fobj != sys.stdout:
            self._fobj.flush()
    
    def _write(self, message, depth=2, **kwargs):
        depth = kwargs.pop('depth', 2)
        uid = str(os.getpid()) + '-' + str(kwargs.pop('uid', 0))
        # message = str_format % args if args else str_format
        frame, filename, line_number, function_name, lines, index = inspect.stack()[depth]
        props = dict(
            asctime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            filename=os.path.basename(filename),
            lineno=line_number,
            message=message,
            uid=uid,
            timestamp=int(time.time()*1000),
        )
        for k, v in kwargs.items():
            if not props.get(k):
                props[k] = v

        output = self._format.format(**props) #'T{pid} {asctime} [{filename}:{lineno:>4}] {message}'.format(**props)
        output = output.rstrip() + '\n'

        self.lock.acquire()
        try:
            self._fobj.write(output)
        finally:
            self.lock.release()
        
        if self._auto_flush:
            self.flush()
        
    def start(self, name, uid=None):
        self._write(name, level_name='Action', status='Start', uid=uid) #'%s/%s begin', self.trans, self.action, start=True)
    
    def success(self, name, uid=None):
        self._write(name, level_name='Action', status='End][Success', uid=uid)

    def error(self, name, reason='', uid=None):
        self._write(name, level_name='Action', status='End][error][' + reason, uid=uid)


_instances = {}

def getLogger(filename=None):
    if filename is None:
        filename = os.getenv('CLOUDLOAD_LOG_FILE') or 'cl.log'
    if _instances.get(filename):
        return _instances[filename]
    ret = _instances[filename] = _Logger(filename)
    return ret


if __name__ == '__main__':
    log = getLogger('out.log')

    log.start("Login", uid=19202)
    log.success("Login", uid=19202)

    log = getLogger()
    log.start("Logout", uid=19203)
    log.error("Logout", "something went wrong", uid=19203)
