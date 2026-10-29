# Installation Instructions

Astra Tags is distributed through the Unity Asset Store as a UPM package, so you install it from the Package Manager, and its runtime and editor content then appears under **Packages** in the Project window. The optional samples are imported separately, when you need them.

## Prerequisites

- Use a Unity version that meets the [requirements](requirements.md)
- Acquire Astra Tags from the Unity Asset Store using the Unity account signed into the Editor
- Connect to the internet so the Package Manager can access the account's packages

## Install Astra Tags

Let's install the package in an existing Unity project:

1. Open `Window > Package Management > Package Manager`
2. Select **My Assets** and search for **Astra Tags**
3. Select the package and, if multiple versions are offered, choose the version to install
4. Select **Install** and wait for Unity to finish resolving the package and compiling scripts

Astra Tags should now be installed as a UPM package and visible under **Packages** in the Project window. Unity documents this route in [Install a UPM package from the Asset Store](https://docs.unity3d.com/6000.2/Documentation/Manual/upm-ui-install2.html).

## Check the installation

Use a disposable tag to check that both the runtime assets and editor tools are available:

1. Check the Console for compilation errors after Unity finishes compiling
2. Open `Tools > Astra Tags > Tag Manager` and confirm that the window opens
3. Select a folder under `Assets` in the Project window, then use `Assets > Create > Astra Tags > Tag` to create a test tag
4. Select the tag and confirm that its Inspector shows its tag configuration

You can start with an empty tag hierarchy, since installing the package does not need any existing project tags. See the [introduction](introduction.md) for the tag model, and [Package Configuration and the Registry](workflows/package-configuration.md) for the registry setup.

## Import samples

The package manifest declares **Examples** and **Stress Test**. Their source is stored in `Samples~`; import a sample to make its scripts available in the project:

1. Select the installed **Astra Tags** package in the Package Manager
2. Open its **Samples** section
3. Select **Import** for **Examples**, **Stress Test**, or each sample in turn
4. Wait for Unity to copy the selected sample into `Assets` and finish compiling its scripts

The Package Manager's sample import action is separate from package installation. Unity describes it in [Create samples for packages](https://docs.unity3d.com/6000.2/Documentation/Manual/cus-samples.html).

After importing a sample, its scene-builder menu becomes available:

| Sample | Scene-builder menu | Generated scene |
|---|---|---|
| Examples | `Tools > Astra Tags > Samples > Build Examples Scene` | `Assets/AstraTagsExamples/AstraTagsExamples.unity` |
| Stress Test | `Tools > Astra Tags > Samples > Build Stress Test Scene` | `Assets/AstraTagsStressTest/AstraTagsStressTest.unity` |

Importing the scripts and generating a scene are two separate actions: each builder creates its scene and supporting assets on its own, after the scripts are imported. Save the current scene before using either builder, because both create a new scene in single-scene mode.

## If a package or sample is missing

If Astra Tags does not appear under **My Assets**, check that the Editor is signed into the account that acquired it and let the package list refresh.

If a sample-builder menu is missing, confirm that the corresponding sample has been imported, then check the Console for compilation errors. The optional sample scripts only become active once you import the sample.
