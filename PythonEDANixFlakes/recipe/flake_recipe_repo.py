from PythonEDA.repo import Repo
from PythonEDANixFlakes.flake import Flake
from PythonEDANixFlakes.recipe.flake_recipe import FlakeRecipe

from typing import List

class FlakeRecipeRepo(Repo):
    """
    A subclass of Repo that manages Flake recipes.
    """

    def __init__(self):
        """
        Creates a new FlakeRecipeRepo instance.
        """
        super().__init__(FlakeRecipe)

    def find_recipe_classes_by_flake(self, flake: Flake) -> List[FlakeRecipe]:
        """
        Retrieves the recipe classes matching given flake, if any.
        """
        raise NotImplementedError(
            "find_by_flake() must be implemented by subclasses"
        )
