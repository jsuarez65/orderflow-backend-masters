
import structlog, logging

class LogConfiguration:
    
    @staticmethod
    def configure():

        logging.basicConfig(
            level=logging.INFO,   
            filename="master_service.log",
            filemode="a",          
            format="%(asctime)s [%(levelname)s] %(message)s")

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer("message"),
                structlog.dev.ConsoleRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
            )

    @staticmethod
    def getLogger():
        return structlog.get_logger()
