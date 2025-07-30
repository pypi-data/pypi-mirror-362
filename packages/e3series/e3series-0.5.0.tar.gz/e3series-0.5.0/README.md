# Python wrapper for the E3.series COM interface

python e3series is a wrapper library for the E3.series COM interface.
The library enhances the automatic code completion and static program verification for python programs that automate E3.series.

This library requires a working instance of the software Zuken E3.series.

## Getting Started

Install the library via pip:
```
pip install e3series
```

Use the library:
```python
import e3series as e3

app = e3.Application()
app.PutInfo(0, "hello, world!")
```

For more samples you can visit the git repository [https://github.com/Pat711/E3SeriesPythonSamples](https://github.com/Pat711/E3SeriesPythonSamples).


## Releasenotes

#### Version 0.5
 - New Function ConfiguratorInterface.SwapSymbol (2026 26.01, 2027 27.00)
 - New Functions AttributeDefinitionInterface.GetAttributeListValues and AttributeDefinitionInterface.GetValueListName (2025 25.34, 2026 26.01, 2027 27.00)
 - New Function SlotInterface.GetDefinedRotation (2026 26.01, 2027 27.00)
 - Fix: The functions SetCrimpingRules and GetCrimpingRules in the DbeModelPinInterface had a wong variable type
 - Fix: Type of the parameter additionalAttributes of DbeApplicationInterface.GetComponentList
 - New enum type GraphType
 - New enum type SymbolType
 - New enum type ComponentType
 - New enum type ComponentSubType 

#### Version 0.4
- Added `language` to the `e3series.tools.StartArguments`.
- Fixed a bug in variant to dict conversion
- Fix: `e3series.tools.start()` modifies the args argument if a string list is provided and `wait_for_com` is True.
- Fix: `e3series.tools.start(keep_alive=False)` does not work if the script process is not already in a process-job.
- Fix: A bug lead to empty lists inside dictionaries
- Added treatment for dict [IN] parameters
- settings parameter of Device.GetTerminalPlanSettings() and Job.GetTerminalPlanSettings() actually is [IN/OUT], not [IN], corrected this in the library. The Documentation is currently wrong. Providing a non empty dict enables you to only get specified settings.
- Added the following enum types for usage with the AttributeDefinitionInterface: AD_Direction, AD_Owner, AD_Ratio, AD_Type, AD_UniqueValue

#### Version 0.3
- Added `e3series.tools.E3seriesOutput` to redirect the output of the print function to the E3.series message window.

#### Version 0.2
- First Release. Contains wrappers for all COM-Objects of the E3.series release 26.0.

#### Version 0.1
- Placeholder package with no content.