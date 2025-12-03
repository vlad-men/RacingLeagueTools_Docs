# Variables

Variables are key-value pairs (`Dictionary<string, object>`) used to store data.

![Variable definition](../images/page-42-image-01.png)

## Definition and Priority

Variables can be defined at multiple levels. The priority order, from lowest to highest, is as follows:

1. `%theme_folder%/globals/global_vars.json` (Lowest priority)
2. `%theme_folder%/vars/`
3. `%layout_folder%/vars/`
4. `%layer_folder%/vars/`
5. Localization variables
6. Public properties/variables
7. Block `Vars` property (Highest priority)

When defined in a separate file, the JSON root must be an object containing key-value pairs. File names and internal folder hierarchy within `vars` folders do not affect functionality; only the variable name matters. Variables with the same name cannot exist at the same level.

Variables can be overridden at different levels, similar to components and styles. Variables defined in the immediate parent block have the highest priority, while those in `global_vars.json` have the lowest.

## Usage

Variables are accessed using expressions.

![Variable usage in expression](../images/page-42-image-02.png)

Variable names must not contain spaces or dots.
