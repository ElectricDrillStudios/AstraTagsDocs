# Requirements

Astra Tags declares **Unity 6.2** (`6000.2`) as its minimum editor version in the package manifest. Compatibility with earlier Unity versions is not established.

## Dependencies

Astra Tags is a standalone package. Its manifest declares no additional package dependencies, and its runtime assembly references no other custom assemblies.

| Component | Requirements |
|---|---|
| Runtime | Unity engine assemblies; no additional Astra package |
| Editor tools | Unity Editor and the Astra Tags runtime assembly |
| Examples sample | Astra Tags runtime; Unity Editor for the scene builder |
| Stress Test sample | Astra Tags runtime; Unity Editor for the scene builder |

Astra Framework and Odin Inspector are not required. The sample assembly definitions do not add dependencies on other packages.

See [Relationship to other tag systems](introduction.md#relationship-to-other-tag-systems) for the distinction between Astra Tags and Astra Framework tags.

## Before using the package

- Open the project with an editor meeting the minimum Unity version
- Allow Unity to finish importing and compiling scripts before opening the package's editor tools
- Use the [introduction](introduction.md) to distinguish tag assets, tag sets, runtime containers, and queries

The samples include editor scripts that generate their scenes and supporting assets. Running a scene builder is a separate action from making its sample scripts available in the project.
