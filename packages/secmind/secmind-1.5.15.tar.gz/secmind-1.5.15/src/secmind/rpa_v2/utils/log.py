import io
import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class LogWrapper:

    def __init__(self):
        self.__init_logging()

    def __init_logging(self):
        self.__log_stream = io.StringIO()
        self.__handler = logging.StreamHandler(self.__log_stream)
        self.__handler.setLevel(logging.DEBUG)
        self.__handler.setFormatter(formatter)
        self.__logger = logging.getLogger()
        logging.basicConfig(level=logging.DEBUG)
        self.__logger.addHandler(self.__handler)
        self.__logger.get_log_text_with_close = self.__get_log_text_with_close

    def get_logger(self):
        return self.__logger

    def __get_log_text_with_close(self):
        log_contents = self.__log_stream.getvalue()
        self.__log_stream.close()
        self.__handler.close()
        self.__logger.removeHandler(self.__handler)
        return log_contents
