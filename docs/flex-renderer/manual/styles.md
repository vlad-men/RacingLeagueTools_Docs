# Styles

Styles allow applying the same set of properties to different blocks. A style is essentially a block that can contain any nested options (TextOptions, ImageOptions, etc.). The `BlockType` and `Items` properties within a style are ignored.

When a style is referenced, the renderer looks for it in the resources and applies its property values to the requesting block. Properties defined directly in the block take precedence over style properties.

## Style Locations

Styles can be defined in two locations:

1.  **"styles" folder** (at the theme, layout, or layer level).

    Any custom internal folder hierarchy is allowed. There are two formats for JSON files:

    - **One file (.json) — one style:**

      The style block is the JSON root.

      ```json
      {
        "StyleName": "RegularTextStyle",
        "BlockType": "text"
      }
      ```

    - **One file (.json) — many styles:**

      The root is an array of blocks.

      ```json
      [
        {
          "StyleName": "TableHeaderStyle",
          "BlockType": "text"
        },
        {
          "StyleName": "DriverAvatarStyle",
          "BlockType": "image"
        }
      ]
      ```

    There are two ways to refer to a specific style:

    - **By Style Name:**

      Specify the `StyleName` property.

      ```json
      {
        "BlockType": "image",
        "Style": "DriverAvatarStyle"
      }
      ```

    - **By Relative Path:**

      Specify the relative file path and file name (without extension). This requires the file to contain a single style. The path must start with a slash.

      ```json
      {
        "BlockType": "text",
        "Style": "/textStyles/regularTextStyle"
      }
      ```

2.  **Directly in the layer code**

    Block containers (stack, dock, itemstack, canvas, table) have a `Styles` property. This property defines an array of styles available to all children down the hierarchy.

    ![Styles property in block containers](../images/page-36-image-01.png)

## Style Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `StyleName` | `string` | Yes | The name of the style. Required unless referenced by file path. |
| `StyleBasedOn` | `string` | No | The name or path of the parent style. |

## Styles Hierarchy

Styles can form a hierarchy. For example, style A can be the parent of styles B and C. Children inherit all parent properties but can override them or add new ones. To specify a parent, use the `StyleBasedOn` property. The parent style must be defined higher in the search hierarchy.

## Style Usage

To use a style, specify its name or path in the `Style` property. All block types support this property.

![Style usage example](../images/page-36-image-02.png)

## Finding the Required Style

The process for finding a style is identical to finding a component. See [Components](components.md).
