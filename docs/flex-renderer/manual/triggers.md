# Triggers

Triggers change block properties or options based on specific conditions. Each block can include a list of triggers defined as `TriggerItem` objects.

![Trigger structure](../images/page-38-image-01.png)

## TriggerItem

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `Condition` | `any` | Yes | Condition under which the trigger activates. If `ConditionValue` is not set, treated as boolean (0 = false, >0 = true). If `ConditionValue` is set, `Conditon` can be any type/value (it will be forcibly converted to string type during comparison). |
| `ConditionValue` | `any` | No | Value to compare against `Condition`. Both are converted to strings for comparison. |
| `ConditionAnd` | `any` | No | Additional condition (implement AND logic). If `ConditionAndValue` is not set: it is assumed that `bool` value is used (can be `number` type, 0 = false, >0 = true). If `ConditionAndValue` is set, `ConditonAnd` can be any type/value (it will be forcibly converted to string type during comparison) |
| `ConditionAndValue` | `any` | No | Value to compare against `ConditionAnd`. |
| `ConditionOr` | `any` | No | Additional condition (OR logic). Treated as boolean if `ConditionOrValue` is not set. |
| `ConditionOrValue` | `any` | No | Value to compare against `ConditionOr`. |
| `Setters` | `TriggerPropertyItem[]` | No | List of property setters to apply when the trigger is active. |
| `TriggerName` | `string` | No | Defines the name of the trigger for external reference. |
| `Trigger` | `string` | No | Specifies the name of an external trigger to use. |

## TriggerPropertyItem

| Property | Type | Description |
| --- | --- | --- |
| `Property` | `string` | Full path to the block property (e.g., `Foreground` or `TextOptions.Foreground`). |
| `Var` | `string` | Name of the block variable to override. Automatically added if not defined. |
| `ComponentVar` | `string` | Name of the component variable to override. Automatically added if not defined. |
| `Value` | `object` | Value to apply. Can be a primitive, an options object (e.g., `ImageOptions`), or `ColorizeOptions`. |

![Trigger property item](../images/page-39-image-01.png)

The `TriggerPropertyItem` structure primarily overrides block properties but can also override block or component variables. To do this, define `Var` or `ComponentVar` instead of `Property`. The `Value` applies to the specified target.

If only one property needs to be overridden, the `Setters` list can be omitted. Specify `Property` (or `Var`/`ComponentVar`) and `Value` directly in the trigger object.

![Simplified trigger definition](../images/page-39-image-02.png)

## External Triggers

Triggers can be defined in external files and referenced by name or path, similar to components and styles. This allows reusing the same trigger in different places.

![External trigger reference](../images/page-40-image-01.png)

![External trigger usage](../images/page-40-image-02.png)

When a trigger is referenced, the renderer searches for it in the resources, copies it, and substitutes it into the calling location.

External triggers are stored in the `Triggers` folder at the theme, layout, or layer level. Custom internal folder hierarchies are allowed.

There are two formats for JSON files describing triggers:

1. One file containing one trigger:

   ```json
   {
     "TriggerName": "ShowLapsTrigger",
     "Condition": "..."
   }
   ```

2. One file containing multiple triggers:

   ```json
   [
     {
       "TriggerName": "ShowLapsTrigger",
       "Condition": "..."
     },
     {
       "TriggerName": "ShowWeatherTrigger",
       "Condition": "..."
     }
   ]
   ```

In the first case, the root object is the `TriggerItem`. In the second case, the root is an array of `TriggerItem` objects.

There are two ways to refer to a specific trigger:

- Specify the trigger name (defined in the `TriggerName` property):

  ```json
  {
    "Trigger": "ShowLapsTrigger"
  }
  ```

- Specify the relative file path and file name (without extension). This requires the file to contain a single trigger. The path must start with a slash:

  ```json
  {
    "Trigger": "/headerTriggers/ShowLapsTrigger"
  }
  ```
