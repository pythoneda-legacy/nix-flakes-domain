class MissingFlakeSectionInRecipeToml(Exception):
    """
    A recipe.toml does not include a [flake] section.
    """

    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
