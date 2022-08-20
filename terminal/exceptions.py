class PluginNotFoundError(Exception):
    """Error raised when the plugin cannot be found."""

    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.message = f"Unable to load the plugin {plugin_name}."
        super().__init__(self.message)


class PluginNotFoundWarning(Warning):
    """Warning raised when the plugin cannot be found."""

    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.message = f"Unable to load the plugin {plugin_name}."
        super().__init__(self.message)


class CommandRegistrationConflict(Exception):
    """Exception raised when multiple commands are registered to the same keyword"""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = f"Multiple commands registered on {keyword}."
        super().__init__(self.message)


class CommandNotFoundError(Exception):
    """Exception raised when the command is not found."""

    def __init__(self, keyword: str):
        self.keyword = keyword
        self.message = f"Command not found: {keyword}"
        super().__init__(self.message)
