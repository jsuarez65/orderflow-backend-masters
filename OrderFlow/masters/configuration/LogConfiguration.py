
import structlog, logging

class LogConfiguration:
    
    @staticmethod
    def configure():

        logging.basicConfig(
            level=logging.INFO,   
            filename="master_service.log",
            filemode="a",          

            format="%(message)s")

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.add_log_level,
                structlog.dev.ConsoleRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory()
        )

    @staticmethod
    def getLogger():
        return structlog.get_logger()
