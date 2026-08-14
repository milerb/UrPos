from datetime import datetime


class Utils:
    """
    Class for holding small utilities that dont need a separate class.
    """

    @staticmethod
    def get_current_date() -> str:
        return datetime.now().strftime("%Y-%m-%d")
