# xpmtd


This package is for keeping track of rawdata and derivatives directory structures.
The core principle is that filepaths are deterministic following the NIU
NeuroBlueprint principles (https://neuroblueprint.neuroinformatics.dev/latest/index.html)

Ideally, this package should free users from having to define paths to any
of their data and provide a comfortable api for accessing different data.

TODO: combine with datashuttle


The user needs to specify the path to the root raw data, and the path to the
root derivatives data and a mouse name.

This will then be used to look for and organise the different data sources,
where they have been specified. E.g. for Behaviour, Neuropixels,
and Histological data.

Some example code:

```python
from metadata import MouseMetadata

rawdata_directory = "/path/to/rawdata/"
derivatives_directory = "/path/to/derivatives/"
mouse_id = "mouse_1"

metadata = MouseMetadata(
                           mouse_id,
                           rawdata_directory,
                           derivatives_directory,
                           )                           
``` 

This metadata object can then be used directly in different python
scripts to access and generate filepaths of different types down to 
the session and run level when needed and only needs to be defined 
once per mouse. e.g.:

```python
import run_behaviour analysis # (or whatever)
for s in metadata.sessions:
    behaviour_directory = s.behav_derivatives
    run_behaviour_analysis(behaviour_directory)

```




