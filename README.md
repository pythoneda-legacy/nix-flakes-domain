# Nix Flakes in PythonEDA

This package includes the domain of Nix Flakes in PythonEDA.

This package provides:
- [PythonEDANixFlakes/description.py](PythonEDANixFlakes/description.py): Support for Nix Flakes descriptions.
- [PythonEDANixFlakes/flake.py](PythonEDANixFlakes/flake.py): An abstraction for a Nix Flake.
- [PythonEDANixFlakes/flake_available.py](PythonEDANixFlakes/flake_available.py): An event emitted when a Flake is already available.
- [PythonEDANixFlakes/flake_created.py](PythonEDANixFlakes/flake_created.py): An event emitted when a Flake has been created.
- [PythonEDANixFlakes/flake_in_progress.py](PythonEDANixFlakes/flake_in_progress.py): A temporary entity representing an incomplete flake.
- [PythonEDANixFlakes/flake_repo.py](PythonEDANixFlakes/flake_repo.py): A repository for Nix Flakes.
- [PythonEDANixFlakes/flake_requested.py](PythonEDANixFlakes/flake_requested.py): An event requesting a flake.
- [PythonEDANixFlakes/license.py](PythonEDANixFlakes/license.py): License types.
- [PythonEDANixFlakes/build/build_flake_requested.py](PythonEDANixFlakes/build/build_flake_requested.py): An event requesting building a flake.
- [PythonEDANixFlakes/build/flake_builder.py](PythonEDANixFlakes/build/flake_builder.py): A builder for Nix Flakes.
- [PythonEDANixFlakes/build/flake_built.py](PythonEDANixFlakes/build/flake_built.py): An event when a flake has been built successfully.
- [PythonEDANixFlakes/recipe/base_flake_recipe.py](PythonEDANixFlakes/recipe/base_flake_recipe.py): Base class for Flake recipes.
- [PythonEDANixFlakes/recipe/empty_flake_metadata_section_in_recipe_toml.py](PythonEDANixFlakes/recipe/empty_flake_metadata_section_in_recipe_toml.py): Error detected when the metadata section in a recipe.toml is empty.
- [PythonEDANixFlakes/recipe/empty_flake_section_in_recipe_toml.py](PythonEDANixFlakes/recipe/empty_flake_section_in_recipe_toml.py): Error detected when the flake section in a recipe.toml is empty.
- [PythonEDANixFlakes/recipe/flake_recipe.py](PythonEDANixFlakes/recipe/flake_recipe.py): A Flake recipe (instructions on how to create a flake).
- [PythonEDANixFlakes/recipe/flake_recipe_repo.py](PythonEDANixFlakes/recipe/flake_recipe_repo.py): Repository of Flake recipes.
- [PythonEDANixFlakes/recipe/formatted_flake.py](PythonEDANixFlakes/recipe/formatted_flake.py): A decorated Nix Flake to be used in templates.
- [PythonEDANixFlakes/recipe/formatted_flake_python_package.py](PythonEDANixFlakes/recipe/formatted_flake_python_package.py): A decorated [https://github.com/pythoneda/python-package/PythonEDAPythonPackages/python_package.py](Python Package) packaged as a Nix Flake, to be used in templates.
- [PythonEDANixFlakes/recipe/formatted_nixpkgs_python_package.py](PythonEDANixFlakes/recipe/formatted_nixpkgs_python_package.py): A decorated [https://github.com/pythoneda/python-package/PythonEDAPythonPackages/python_package.py](Python Package) already in Nixpkgs, to be used in templates.
- [PythonEDANixFlakes/recipe/formatted_python_package.py](PythonEDANixFlakes/recipe/formatted_python_package.py): A decorated [https://github.com/pythoneda/python-package/PythonEDAPythonPackages/python_package.py](Python Package) to be used in templates.
- [PythonEDANixFlakes/recipe/formatted_python_package_list.py](PythonEDANixFlakes/recipe/formatted_python_package_list.py): A decorated list of [https://github.com/pythoneda/python-package/PythonEDAPythonPackages/python_package.py](Python Packages). 
- [PythonEDANixFlakes/recipe/missing_flake_section_in_recipe_toml.py](PythonEDANixFlakes/recipe/missing_flake_section_in_recipe_toml.py): Error detected when the flake section in a recipe.toml is missing.
- [PythonEDANixFlakes/recipe/missing_flake_version_spec_in_recipe_toml.py](PythonEDANixFlakes/recipe/missing_flake_version_spec_in_recipe_toml.py):
- [PythonEDANixFlakes/recipe/missing_recipe_toml.py](PythonEDANixFlakes/recipe/missing_recipe_toml.py): Error detected when the required recipe.toml files is missing in a recipe.
- [PythonEDANixFlakes/recipe/missing_type_in_flake_metadata_section_in_recipe_toml.py](PythonEDANixFlakes/recipe/missing_type_in_flake_metadata_section_in_recipe_toml.py): Error detected when the "type" attribute in the flake metadata section in a recipe.toml is missing. 
- [PythonEDANixFlakes/recipe/more_than_one_flake_in_recipe_toml.py]( [PythonEDANixFlakes/recipe/more_than_one_flake_in_recipe_toml.py): Error detected when more than flake is specified in a recipe.toml file.
- [PythonEDANixFlakes/recipe/recipe_does_not_support_placeholder.py](PythonEDANixFlakes/recipe/recipe_does_not_support_placeholder.py): Error detected when a placeholder in a template is not supported by the recipe.
    
