# MRI RF Coil Open Data Standard (MRCODS)

<img src="/figures/IRM_siemens_avec_antennes.png" width=400>

---

Magnetic resonance imaging (MRI) scanners are designed to accommodate different radio frequency (RF) coils depending on the region of the body being imaged and other scan requirements.
The scanner must therefore be able to identify the type of coil that is connected, its capabilities and operating parameters.
In the past this function was implemented using incompatible, vendor-specific proprietary protocols that typically identify the coil with a unique code which is then associated with a specific data file on the scanner.
In addition to being a closed, proprietary approach, it is also prone to accidental mismatching, spoofing (intentionally presenting a code belonging to another coil), missing data files, or other errors.
This repository introduces an [open standard](https://en.wikipedia.org/wiki/Open_standard) consisting of a data format and transmission protocol to allow the scanner to identify an RF coil's information consistently across different platforms.
[The standard](mrcods.md) also introduces the ability to identify and track an individual coil, e.g., for quality assurance purposes, logging errors, etc. This feature is impossible with the basic coil ID/file method (multiple coils of the same model cannot be distinguished by the system).

## [Read the Standard](mrcods.md)

## Available Implementations

The repositories provides implementations of the standard to read/write from/to an I<sup>2</sup>C EEPROM in different languages and with different masters. Scripts and documention are contained in the relevant folders.

## License
![CClicense](https://i.creativecommons.org/l/by-nd/4.0/88x31.png)\
[The standard](mrcods.md) is licensed under a [Creative Commons Attribution-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nd/4.0/) (CC-BY-ND).\
All available implementations are licensed under the Apache License Version 2.0. For further information, please refer to the relevant LICENSE file.

## Contributors (alphabetical order)
Nicola De Zanche, Umberto Zanovello

## How to Contribute

Contributions are welcome. Please use the [issue tracker](https://github.com/umbertozanovello/OpenStandard-CoilID/issues) to submit comments and requests.
