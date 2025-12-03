# Layers

Each layout can include any number of layers (minimum 1). Every layer lives in a JSON file that defines a root block, usually a container that holds child blocks.

## Layer Location Options

Layer files can be stored either in dedicated subfolders or directly inside the layout folder. Both options can coexist in the same layout.

**Subfolder option.** Place the layer folder inside the layout folder and start its name with `layer`. Inside that folder add one JSON file with any name. Optional subfolders `vars`, `components`, `styles`, `triggers` can hold assets owned by the layer.

![Layer folder structure](../images/page-12-image-03.png)

**File option.** Place the JSON file directly in the layout folder and start its name with `layer`.

![Layer file in layout folder](../images/page-12-image-04.png)


## Layer Naming and Order

- For the subfolder option, the folder name becomes the layer name.
- For the file option, the file name becomes the layer name.
- Rendering order follows the alphabetical order of layer names. A typical setup uses two layers: background and main.

## Background Layer Behavior

- If `BlockRoot.Width` or `BlockRoot.Height` is missing, the renderer sets it to the final image size.
- If a background dimension exceeds the final image size (maximum width or height across layers), the layer is cropped.
- If a background dimension is smaller than the final image size, the layer is scaled up.

## Layer Example

Example layer content in a JSON editor:

![Layer JSON structure](../images/page-13-image-01.png)

## Asset Inheritance

The layer folder can include the following optional folders:

- `images`
- `vars`
- `components`
- `styles`
- `triggers`

The same folder names can appear in the layout root or theme root. When a resource exists at multiple levels, the renderer checks the layer folder first, then the layout folder, and finally the theme folder. This lookup order applies to assets referenced from JSON as well as components and styles defined inside the layer file.
