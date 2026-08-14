import logging


class LogHandler:
    """Class for logging."""

    # use this in the main file only.
    @staticmethod
    def config() -> None:
        """
        Main logging config.
        Use this only in the main filke for setting up root config.
        """
        logging.basicConfig(
            filename="newpos.log",
            filemode="a",
            format="%(asctime)s:%(levelname)s:%(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=logging.DEBUG,
            encoding="utf-8",
        )

    @staticmethod
    def logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
