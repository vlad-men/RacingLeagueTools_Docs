# Block Types and Block Options

Individual properties required for a specific type of block are placed in separate objects called **Block Options** (e.g., `ImageOptions`). It is not always necessary to specify this object if default values are sufficient.

The following sections describe properties for specific block options.

## Image

**BlockType:** `image`
**BlockOptions:** `ImageOptions`

Used to display an image.

| Property | Type | Description |
| --- | --- | --- |
| `Path` | `string` | Specifies the data object or path to the image file (`.png`, `.jpg`, `.jpeg`). |
| `DefaultPath` | `string` | Used if retrieving an image from `Path` fails. |
| `HorizontalAlignment` | `enum` | Options: `Left`, `Center`, `Right`. |
| `VerticalAlignment` | `enum` | Options: `Top`, `Center`, `Bottom`. |
| `Opacity` | `int` | Opacity level. |
| `Rotation` | `int` | Rotates the image clockwise around its center. Supports values beyond -360/360. |

### Path Specification

The `Path` property (or `Source` property of the block) can be specified as:


**Relative path**: e.g., `separators/separator_red.png`. Specifies the full path relative to the `images` folder in the theme root (or layout/layer).


## Text

**BlockType:** `text`
**BlockOptions:** `TextOptions`

Used to display text.

| Property | Type | Description |
| --- | --- | --- |
| `Text` | `string` | The text content to display. |
| `FontName` | `string` | Font family. Defaults to global variable `FontNameDefault` if empty. |
| `FontSize` | `int` | Font size. Defaults to global variable `FontSizeDefault` if empty. |
| `FontStyle` | `enum` | Options: `Regular`, `Bold`, `Italic`, `BoldItalic`. (Experimental). |
| `Foreground` | `color` | Text color. Defaults to global variable `ForegroundDefault` if empty. |
| `TextAlignment` | `enum` | Options: `Start`, `End`, `Center`. (Experimental). |
| `HorizontalAlignment` | `enum` | Options: `Left`, `Center`, `Right`. |
| `VerticalAlignment` | `enum` | Options: `Top`, `Center`, `Bottom`. |
| `LineSpacing` | `int` | Spacing between lines. |
| `Wrap` | `bool` | Enables text wrapping. (Experimental). To make the text wrap, it may need to force the width of the text block. Dev in progress. |
| `Rotation` | `int` | Rotates text clockwise around its center. |
| `ColorizeRating` | `ColorizeRatingOptions` | Sets foreground color based on rating value. |



### ColorizeRatingOptions

| Property | Type | Description |
| --- | --- | --- |
| `IsEnabled` | `bool` | Enables or disables the block. |
| `Level` | `int` | Value (0-100) determining the color. |
| `GradientStops` | `List<GradientStop>` | List of gradient stops for custom color assignment. If not specified, default values are used. |

### GradientStop

| Property | Type | Description |
| --- | --- | --- |
| `Color` | `color` | Specific color override. |
| `Offset` | `int` | Offset value (0-100). |

## Stack and Dock

**BlockTypes:** `stack`, `dock`
**BlockOptions:** `PanelOptions`

Container blocks that arrange nested blocks.

### Stack

Arranges nested (inner) blocks sequentially.

![Stack layout example](../images/page-25-image-01.png)

### Dock

Similar to Stack, with the following differences:

-   By default, it fills all available space (`StretchWidth` or `StretchHeight` is true, depending on `Orientation`).
-   If inner blocks specify alignment, Dock uses this to dock them to the sides.
-   Only one inner block can specify center alignment.

![Dock layout example](../images/page-25-image-02.png)

### PanelOptions Properties

| Property | Type | Description |
| --- | --- | --- |
| `Orientation` | `enum` | Options: `Horizontal`, `Vertical`. |
| `HorizontalDirection` | `enum` | Options: `LeftToRight`, `RightToLeft`. |
| `VerticalDirection` | `enum` | Options: `TopToBottom`, `BottomToTop`. |
| `Spacing` | `int` | Spacing in pixels between inner blocks. |

## ItemStack

**BlockType:** `itemstack`
**BlockOptions:** `ItemStackOptions`, `PanelOptions`

Similar to Stack, but inner blocks are generated automatically based on a data collection. The `Items` property is ignored.

| Property | Type | Description |
| --- | --- | --- |
| `ItemSource` | `string` | Data access expression for the collection/list. |
| `ItemTemplate` | `block` | Template for inner blocks. |
| `SortMember` | `string` | Property name for sorting the collection. Can be data access expression. |
| `OrderBy` | `string` | Property name for sorting (supports `OrderBy2`, `OrderBy3`). |
| `OrderByDescending` | `string` | Property name for descending sort (supports `OrderByDescending2`, `3`). |
| `FilterMember` | `string` | Property name for filtering the collection. Can be data access expression. |
| `FilterMemberValue` | `string` | Value to filter by. |
| `Reverse` | `bool` | Reverses the collection order. |
| `Limit` | `int` | Limits the number of items. |
| `IndexStart` | `int` | Starting index of the collection. |
| `IndexEnd` | `int` | Ending index of the collection. |
| `TakeItemIndex` | `int` | Selects a single item by index (will be consist only of one item by specified index). |
| `TakeItemsFirst` | `int` | Selects the first N items. |
| `TakeItemsLast` | `int` | Selects the last N items. |
| `CollectionPart` | `string` | Specifies a part of the collection (e.g., "1/3" for the first third). |

## Grid

**BlockType:** `grid`
**BlockOptions:** `GridOptions`

Container for arranging inner blocks in a grid.

![Grid layout example](../images/page-27-image-01.png)

The Grid calculates column widths and row heights based on inner block dimensions. Use `GridCol` and `GridRow` properties on inner blocks to place them. Only one block per cell.

| Property | Type | Description |
| --- | --- | --- |
| `Rows` | `List<GridRowDefinition>` | Definitions for grid rows. |
| `Cols` | `List<GridColDefinition>` | Definitions for grid columns. |

### GridRowDefinition

| Property | Type | Description |
| --- | --- | --- |
| `Height` | `int` | Height of the row. |
| `IsStretchHeight` | `bool` | If true, fills available vertical space (only one row can be true). |

### GridColDefinition

| Property | Type | Description |
| --- | --- | --- |
| `Width` | `int` | Width of the column. |
| `IsStretchWidth` | `bool` | If true, fills available horizontal space (only one column can be true). |

## Canvas

**BlockType:** `canvas`
**BlockOptions:** `CanvasOptions`

A container that arranges inner blocks manually. Each inner block must define `PositionX` and `PositionY` to indicate its top-left coordinate. `CanvasOptions` currently contains no properties.

## Table

**BlockType:** `table`
**BlockOptions:** `TableOptions`

Generates blocks as a table based on a collection/list. The `Items` property is not used.

| Property | Type | Description |
| --- | --- | --- |
| `ItemsSource` | `string` | Data access expression for the collection/list. |
| `HeaderTemplate` | `block` | Template for table headers. |
| `HeaderHeight` | `int` | Height of the header row. |
| `RowHeight` | `int` | Height of data rows. |
| `RowCount` | `int` | Number of rows. |
| `ColSpacing` | `int` | Spacing between columns. |
| `RowSpacing` | `int` | Spacing between rows. |
| `SeparatorSpace` | `int` | Additional space if a column is a separator. |
| `GroupSpaceReduction` | `int` | Space reduction between columns with the same `GroupId`. |
| `Columns` | `List<TableColumnDefinition>` | Definitions for table columns. |

*Note: Sorting and filtering properties (`SortMember`, `FilterMember`, etc.) are identical to `ItemStack`.*

### TableColumnDefinition

| Property | Type | Description |
| --- | --- | --- |
| `Width` | `int` | Width of the column. |
| `MarginLeft` | `int` | Left margin. |
| `MarginRight` | `int` | Right margin. |
| `IsStretchWidth` | `bool` | If true, fills available horizontal space. |
| `Header` | `string` | Text for the header template (will be replace text property of any text block of header template). |
| `RenderIf` | `bool` | Conditional rendering flag. |
| `Template` | `block` | Template for each item in the column. |
| `IsSeparator` | `bool` | Indicates if the column is a separator. |
| `GroupId` | `int` | Groups columns to adjust spacing (same group Id (>0) can be set for several column to bring them closer to each other in the column space). |
| `MultiColumnHeadersSource` | `string` | Data expression (only for collection/list) for multicolumn headers. |
| `MultiColumnItemsSource` | `string` | Data expression (only for collection/list) for multicolumn items. |
| `MultiColumnHeaderTemplate` | `block` | Template for multicolumn items. |

### Multicolumn

A feature for expanding one column into multiple columns.

![Multicolumn layout example](../images/page-29-image-01.jpeg)

## Shape

**BlockType:** `shape`
**BlockOptions:** `ShapeOptions`

Displays a simple geometric figure.

| Property | Type | Description |
| --- | --- | --- |
| `ShapeType` | `enum` | Options: `rectangle`, `ellipse`. |
| `Fill` | `color` | Fill color. |
| `Rotation` | `int` | Rotates the shape clockwise around its center. |

## Component

**BlockType:** `component`
**BlockOptions:** `ComponentOptions`

Used to reuse complex blocks across different places in a layer or layout.

| Property | Type | Description |
| --- | --- | --- |
| `Vars` | `Dictionary<string, object>` | Variables passed to the component. |

## ColorizeOptions

**BlockOptions:** `ColorizeOptions`

Describes how the background or final image of a block should be colored.

| Property | Type | Description |
| --- | --- | --- |
| `Enabled` | `bool` | Enables colorization. |
| `Color` | `color` | Target color. |
| `BlendPercentage` | `int` | Blend percentage (0-100). |
| `AlphaCompositionMode` | `enum` | Composition mode. Possible values: `SrcOver`, `Src`, `SrcAtop`, `SrcIn`, `SrcOut`, `Dest`, `DestAtop`, `DestOver`, `DestIn`, `DestOut`, `Clear`, `Xor`. Can be empty/null. Default: `SrcATop`. |
| `ColorBlendingMode` | `enum` | Blending mode. Possible values: `Normal`, `Multiply`, `Add`, `Subtract`, `Screen`, `Darken`, `Lighten`, `Overlay`, `HardLight`. Can be empty/null. Default: `Screen`. |
