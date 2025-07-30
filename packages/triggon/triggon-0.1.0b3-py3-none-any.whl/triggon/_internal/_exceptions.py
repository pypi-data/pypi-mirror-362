SYMBOL = "*"


class InvalidArgumentError(ValueError): 
    pass


class MissingLabelError(KeyError):
    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return f"Label '{self.label}' is missing."


class _UnsetExitError(Exception):
    def __init__(self):
        super().__init__(
            "Please set `exit_point()` before calling this function."
        )


class _ExitEarly(Exception): 
    pass

   