from pydantic import ValidationError


class DataDecodingError(Exception):

    @property
    def message(self):
        return self.args[0]

    @property
    def error(self) -> ValidationError:
        return self.args[1]
