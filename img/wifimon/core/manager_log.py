import logging
import sys
import os
import socket
from logging.handlers import TimedRotatingFileHandler




#FORMATTER 	= logging.Formatter("[%(levelname)s - %(asctime)s - %(filename)s:%(lineno)s] -> %(message)s")
#FORMATTER 			= logging.Formatter("[%(levelname)s - %(asctime)s] -> %(message)s")
FORMATTER           = logging.Formatter("[%(levelname)s - %(asctime)s] -> %(message)s", "%Y-%m-%d %H:%M:%S")
FORMATTER_SYSLOG 	= logging.Formatter("metrics_ap: %(message)s")

LOG_FILE 	= "output/log.log"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_wlc_path = os.path.join(script_dir, LOG_FILE)

LOG_TYPE 	= logging.INFO  # imprime logs desde este estado hacia arriba, para consola y fileLog
SYSLOG_TYPE = logging.INFO  # imprime logs desde este estado hacia arriba, para syslog
# Logging Levels (Leven , valur numeric):
# CRITICAL , 50
# ERROR    , 40
# WARNING  , 30
# INFO     , 20 
# DEBUG    , 10
# NOTSET   , 0


class UDPSysLogHandler(logging.Handler):
    def __init__(self, host, port):
        super().__init__()
        self.syslog_server = host
        self.syslog_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.sock.sendto(msg.encode(), (self.syslog_server, self.syslog_port))
            #print(msg.encode())
            
        except Exception:
            logger.error(f"Error send to Server:{self.syslog_server}, Port: {self.syslog_port}, Message: {record}")


# define handler para dar formato a log por consola
def get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

# define handler para dar formato a log por archivo
def get_file_handler():
	file_handler = TimedRotatingFileHandler(abs_file_wlc_path, when='midnight')
	file_handler.setFormatter(FORMATTER)
	return file_handler


def get_udp_syslog_handler(host, port):
    handler = UDPSysLogHandler(host, port)
    handler.setFormatter(FORMATTER_SYSLOG)  # Usando el FORMATTER_SYSLOG definido previamente
    return handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_TYPE)  # or set to DEBUG if you want to catch debug messages too
    logger.addHandler(get_console_handler())
    
    logger.propagate = False
    return logger

def get_syslogger(logger_name, syslog_host='syslog.server', syslog_port=514):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_TYPE)  # or set to DEBUG if you want to catch debug messages too
    logger.addHandler(get_udp_syslog_handler(syslog_host, syslog_port))
    
    logger.propagate = False
    return logger


# def get_syslogger(logger_name, syslog_host='syslog.server', syslog_port=514):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(LOG_TYPE)

#     # Verifica si ya tiene un handler de tipo UDPSysLogHandler
#     if not any(isinstance(h, UDPSysLogHandler) for h in logger.handlers):
#         logger.addHandler(get_udp_syslog_handler(syslog_host, syslog_port))
    
#     logger.propagate = False
#     return logger






logger    = get_logger("logger_app")


#logger.disabled = True         # for enabled or disabled loggin

