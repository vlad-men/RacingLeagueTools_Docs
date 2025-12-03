# Components

Components allow reusing the same block configuration across different places, layers, or layouts. Fundamentally, a **component is a block**. It can contain any type of block (text, image, table, etc.) and any complex internal block hierarchy if the root block is a block-container.

When the code references a component, the renderer locates the component in the resources, copies it entirely, and substitutes it into the calling location.

## Component Location

Components can be defined in external files or directly within the layer code.

### External Files

Components can be stored in a `components` folder at the theme, layout, or layer level. Any custom internal folder hierarchy is allowed.

There are two formats for JSON files describing components:

**1. Single Component File**

One file (`.json`) contains one component. The component block itself is the JSON root.

```json
{
  "ComponentName": "MainHeader",
  "BlockType": "text"
}
```

**2. Multiple Components File**

One file (`.json`) contains an array of components.

```json
[
  {
    "ComponentName": "MainHeader",
    "BlockType": "text"
  },
  {
    "ComponentName": "Footer",
    "BlockType": "stack"
  }
]
```

### Inline Definition

Block-containers (stack, dock, itemstack, canvas, table) have a `Components` property. This property allows defining an array of components available to all children down the hierarchy.

![Inline component definition](../images/page-32-image-01.png)

## Component Definition Properties

When defining a component (either in a file or inline), the following properties apply to the root block of the component.

| Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `ComponentName` | `string` | Yes | Unique name for the component. Required unless the component is a single file referenced by path. |

## Component Usage

To use a component, define a block with `BlockType` set to `component` and specify the component name or path.

| Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `BlockType` | `string` | Yes | Must be set to `component`. |
| `Component` | `string` | Yes | The name of the component or the relative file path. |
| `Vars` | `object` | No | Dictionary of variables to substitute within the component. |

### Referencing Methods

**1. By Name**

Specify the `ComponentName` defined in the component source.

```json
{
  "BlockType": "component",
  "Component": "Footer"
}
```

**2. By File Path**

Specify the relative file path and file name (without extension). This requires the file to contain a single populated component. The path must start with a slash `/`.

```json
{
  "BlockType": "component",
  "Component": "/headers/mainHeader"
}
```

![Component usage example](../images/page-32-image-02.png)

## Component Resolution Logic

When the renderer encounters a block of type `component` (and no direct file path is provided), it searches for the component in the following order:

1.  Checks the `Components` property of the immediate parent block.
2.  Checks the `Components` property of the grandparent block, continuing up the hierarchy.
3.  If not found in the block hierarchy, the renderer checks external files.
4.  Searches in `%layer_folder%/components/subfolder` (if the layer is in a separate folder).
5.  Searches in `%layout_folder%/components/folder`.
6.  Searches in `%theme_folder%/components/`.
7.  If the component is not found, the renderer generates an error.

## Component Variables

Components can define internal variables using angle brackets `< >`. This allows dynamic content substitution when the component is used.

### Basic Substitution

To define a variable within a component, use the syntax `<variable_name>` in any property value.

![Variable definition in component](../images/page-33-image-01.png)

In this example, `<header>` is a variable. When the component is used, define the value for this variable using the `Vars` property inside `ComponentOptions`.

![Variable substitution using Vars](../images/page-33-image-02.png)

The renderer replaces `<header>` with the string "DRIVER OF THE DAY". The variable name in `Vars` must exactly match the text inside the brackets.

### Expression Substitution

If a component needs to use an expression but the data object is not known in the component's context, use the "dot trick".

**Syntax:** `<{expression}>`

The dot inside the expression within angle brackets changes the substitution logic. The renderer only replaces the left side of the expression (relative to the first dot).

**Example:**

Component definition:
`<{data_object.Value}>`

Usage configuration:
`"Vars": { "data_object": "Item" }`

Result:
`{Item.Value}`

**Practical Scenario:**

1.  **Usage Context:** The component is invoked where `Item` is the relevant data object.

    ![Expression variable usage](../images/page-34-image-01.png)

2.  **Component Context:** The component defines a generic variable `data`.

    ![Component definition with expression](../images/page-34-image-02.png)

The renderer replaces the variable (`data`) with the value declared in `Vars` (`Item.Value0`).

*   Original Component Expression: `<{data.Value}>`
*   Variable Mapping: `data` -> `Item.Value0`
*   Final Expression: `{Item.Value0.Value}`

The final expression combines the part declared where the component is invoked (left side) and the part declared in the component itself (right side).
