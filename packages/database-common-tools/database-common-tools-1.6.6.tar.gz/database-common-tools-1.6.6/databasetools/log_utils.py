import logging
from logging import handlers
import multiprocessing
from multiprocessing import Process, Queue
from queue import Empty

# MultiprocessingLogHandler
class MultiprocessingLogHandler(logging.Handler):
    def __init__(self, filename, mode='a', time_unit='D', backup_count=3, encoding='utf-8'):
        logging.Handler.__init__(self)
        self.queue = Queue(-1)
        self.handler = handlers.TimedRotatingFileHandler(filename, when=time_unit, backupCount=backup_count, encoding=encoding, delay=True)
        self.handler.mode = mode
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(process)d - %(levelname)s: %(message)s')) 
        self.listener = multiprocessing.Process(target=self.listen)
        self.listener.start()

    def listen(self):
        while True:
            try:
                record = self.queue.get(timeout=1)
                if record is None:
                    break
                self.handler.emit(record)
            except Empty:
                # 忽略队列为空的异常，继续等待新记录
                continue
            except Exception:
                import sys
                print(sys.exc_info())

    def emit(self, record):
        try:
            self.queue.put(record)
        except Exception as e:
            import sys
            print(sys.exc_info())

    def close(self):
        self.queue.put(None)
        self.listener.join()
        self.handler.close()
        logging.Handler.close(self)

def setup_logging(log_file, time_unit='D', backupCount=3, encoding='utf-8'):
    """
    Setup logging configuration.
        
    :param log_file: Path to the log file
    :param time_unit: time unit
    :param backupCount: log backup count
    :param encoding:  text encode
    """
    log_format = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s: %(message)s')
    handler = handlers.TimedRotatingFileHandler(filename=log_file, when=time_unit, backupCount=backupCount, encoding=encoding, delay=True)
    handler.setFormatter(log_format)
    logger = logging.getLogger(log_file)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def setup_multiprocess_logging(log_file, mode='a', time_unit='D', backupCount=3, encoding='utf-8'):
    """
    Setup Multiprocess logging configuration.
        
    :param log_file: Path to the log file
    :param time_unit: time unit
    :param backupCount: log backup count
    :param encoding:  text encode
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = MultiprocessingLogHandler(log_file, mode, time_unit, backupCount, encoding)
    logger.addHandler(handler)
    return logger, handler
