# coding: utf-8

import logging
import os
import time
from functools import partial

FORMAT = "%(message)s"
INFO = 1

logging.addLevelName(INFO, 'INFO')

class FileHandler(logging.FileHandler):
	def __init__(self, *args, **kwargs):
		''' filename, mode='a', encoding=None, delay=False '''
		super(FileHandler, self).__init__(*args, **kwargs)

	def emit(self, record):
		super(FileHandler, self).emit(record)

_mylog = logging.getLogger('cllog')
_mylog.setLevel(INFO)

_log_filename = os.environ.get('PRIVATE_LOG_FILE', 'cllog.log')
_fh = FileHandler(_log_filename)
_fh.setFormatter(logging.Formatter(FORMAT))
_mylog.addHandler(_fh)

_info = partial(_mylog.log, INFO)

def log(robot=None, log_type=None, name=None, status=None, result=None, note=None):
    '''Record log
    Args:
        robot: robot unique id, required
        log_type: transaction or action, required
        name: unique transaction or action name, required
        status: start or finish, required
        result: success or fail, needed if status=finish
        note: additional information, optional
    Returns:
        None 
    '''
    if (not robot) or (not log_type) or (not name) or (not status):
        return

    if (log_type != 'transaction') and (log_type != 'action'):
        return

    if (status != 'start') and (status != 'finish'):
        return

    if status == 'finish':
        if (result != 'success') and (result != 'fail'):
            return

    timestamp = int(time.time()*1000)
    message = '[%d][%s][%s][%s][%s]' % (timestamp, robot, log_type, name, status)

    if result:
        message = '%s[%s]' % (message, result)

    if note:
        message = '%s[%s]' % (message, note)

    _info(message)

if __name__ == '__main__':
    log('robot1', 'transaction', 'login', 'start')
    log('robot1', 'action', 'step1', 'start')
    log('robot1', 'action', 'step1', 'finish', 'success')
    log('robot1', 'action', 'step2', 'start')
    log('robot1', 'action', 'step2', 'finish', 'fail', 'some exception happened')
    log('robot1', 'transaction', 'login', 'finish', 'success')




