import uvicorn

LOG_LEVEL: str = "DEBUG"
FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        }
    },
    "loggers": {
        "simple_example": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            # "propagate": False
        }
    },
}


def init_loggers(logger_name: str = "simple_example"):
    formatter = uvicorn.logging.DefaultFormatter(FORMAT)
