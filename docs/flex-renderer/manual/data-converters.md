# Data Converters

You can specify a data converter within an expression to transform data. To do this, add a comma and the word `Converter` after the main expression, followed by the converter name after the `=` character.

Example:

![Page 50 Image 01](../images/page-50-image-01.png)

## Parameters

You can also pass parameters to the converter.

### Single Parameter

To pass a single parameter, add `Parameter={parameterValue}` after the converter name (separated by a comma).

Syntax:
`Expression, Converter={ConverterName}, Parameter={Value}`

Example:

![Page 50 Image 02](../images/page-50-image-02.png)

### Multiple Parameters

Some converters require more than one parameter. To pass them, use the `Parameters` keyword and separate parameters with semicolons.

Syntax:
`Expression, Converter={ConverterName}, Parameters={Name1}:{Value1};{Name2}:{Value2}`

Example:

![Page 50 Image 03](../images/page-50-image-03.png)

> **Note:** The order of the parameters is not important.

## Converters List

The following table lists available converters that take one parameter or no parameters.

| Converter Name | Description | Parameter Type | Example |
| --- | --- | --- | --- |
| `StringToLower` | Converts string to lower case. | - | `"ABC"` -> `"abc"` |
| `StringToUpper` | Converts string to upper case. | - | `"abc"` -> `"ABC"` |
| `StringEquals` | Compares with another string. | `string` | `"str1"`, `"str1"` -> `true` |
| `StringNotEquals` | Compares with another string for inequality. | `string` | `"str1"`, `"str1"` -> `false` |
| `EmptyObjectToFalse` | Converts null or empty value to `false`. | - | `""` -> `false` |
| `EmptyObjectToTrue` | Converts null or empty value to `true`. | - | `""` -> `true` |
| `BoolReverse` | Inverts boolean value. | - | `true` -> `false` |
| `NumberZeroToEmpty` | Converts 0 to empty string. | - | `0` -> `""` |
| `NumberEquals` | Compares with a number. | `int` (number) | `0`, `5` -> `false` |
| `NumberNotEquals` | Compares with a number for inequality. | `int` (number) | `0`, `5` -> `true` |
| `NumberGreater` | Checks if value is greater than parameter. | `int` (number) | `0`, `5` -> `false` |
| `NumberLess` | Checks if value is less than parameter. | `int` (number) | `0`, `5` -> `true` |
| `NumberAbs` | Returns absolute value. | - | `-10` -> `10` |
| `NumberAdd` | Adds parameter to value. | `int`, `float` | `5`, `2` -> `7` |
| `NumberSubtract` | Subtracts parameter from value. | `int`, `float` | `5`, `2` -> `3` |
| `NumberMultiply` | Multiplies value by parameter. | `int`, `float` | `5`, `2` -> `10` |
| `NumberDivide` | Divides value by parameter. | `int`, `float` | `5`, `2` -> `3` |
| `DateToDayOfMonth` | Returns day number of the date. | `string` (locale*), optional | `01.12.2022` -> `1` |
| `DateToMonth` | Returns month number of the date. | `string` (locale*), optional | `01.12.2022` -> `12` |
| `DateToMonthInWords` | Returns month name. | `string` (locale*), optional | `01.12.2022` -> `"december"`<br>`01.12.2022`, `"es_ES"` -> `"diciembre"` |
| `DateToYear` | Returns year of the date. | `string` (locale*), optional | `01.12.2022` -> `2022` |
| `DateToTime` | Returns time of the date. | `string` (locale*), optional | `01.12.2022 0:00:00` -> `"0:00"` |
| `TemperatureCelciusToFahrenheit` | Converts Celsius to Fahrenheit. | - | - |
| `NumberGroupWithSeparator` | Separates groups of digits with a custom character. | `string` | `5500`, `.` -> `5.500` |
| `EnumEquals` | Compares enumeration value with a string. | `string` | - |
| `StringAdd` | Appends another string. | `string` | - |
| `StringFormat` | Substitutes the string parameter into the original string (replacing `"SUB"`). | `string` | `'202SUB'`, `'2'` -> `'2022'` |
| `StringFormatReverse` | Substitutes the original string into the parameter string (replacing `"SUB"`). | `string` | `'2'`, `'202SUB'` -> `'2022'` |
| `PercentOf` | Calculates percentage (value is part, parameter is total). | `int` | `10`, `100` -> `10` |
| `PercentTo` | Calculates percentage (value is total, parameter is part). | `int` | `100`, `10` -> `10` |
| `NumberIsEven` | Checks if number is even. | - | `1` -> `false` |
| `NumberIsOdd` | Checks if number is odd. | - | `1` -> `true` |
| `TruncateString` | Truncates string to length, adding "..." if needed. | `int` | `"Long string"`, `5` -> `"Long..."` |


## Converters with Multiple Parameters

| Converter Name | Description | Parameters | Example |
| --- | --- | --- | --- |
| `DateCustomFormat` | Custom format of date and/or time. | `format` (string): <https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings><br>`locale`* (string, optional): culture info, see [Additional Information](#additional-information) | "date(01.12.2022)", "format:yyyy; locale:en-US" -> "2022" |

### Additional Information

**Numeric formatting**: Uses a string to format numbers. For example, a number `1` with a string format `00` returns `01`.
More info: [Standard numeric format strings](https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings)

**Culture info (locale)**: Used to represent data using a specific culture info (locale), defined by culture code.
Examples: `"en-US"`, `"fr-FR"`.
- The value `"current"` uses the current culture (depends on end user’s machine settings).
- The value `"invariant"` uses the invariant culture (default if culture is not specified).

More info about culture codes: [Culture Codes List](https://gist.github.com/hikalkan/afe23b47c30fea418f607561d277c510)

