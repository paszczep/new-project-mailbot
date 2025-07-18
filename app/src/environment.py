from os import environ
from typing import Literal


class Environment:
    @staticmethod
    def variables(scope: Literal["postgres", "email"]) -> dict:
        """Zaczytaj zmienne środowiskowe z określonym przedroskiem."""
        return {
            key.split("_")[1]: value
            for key, value in environ.items()
            if key.startswith(scope)
        }
