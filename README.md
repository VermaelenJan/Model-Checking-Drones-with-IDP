# Model Checking Drones with IDP

This repository contains all relevant files concerning the IDP model, used to verify properties on the behaviour of (the autopilot of) a drone. The different parts contributing to the repository are stated below.

## IDP model

The file `model.idp` holds the current model of the drone and world around it, along with the relevant verifications.
To run an IDP model, [the IDP system](https://dtai.cs.kuleuven.be/software/idp/try) is required. Further, IDP comes with an editor to render the code of the model, using the appropriate logical operators.

The IDP model outputs the results of the verifications and calls the visualisation on the last output, which gets saved in the directory `\Vis\output models` as `last_output`.

## Visualization

The directory `\Vis` contains a small script (consisting of 3 small Python files) to visualise the flight of a drone, as it is outputted by the IDP model. This script is directly invoked by the main procedure in the model. Further, it is also possible to manually call the script.

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install matplotlib.

```bash
pip install matplotlib
```

### Usage
To manually call the plotting script, call
```bash
Vis\main.py scenario
```
where `scenario` can be either
```bash
last_output   - to (re-)visualize the scenario that was last outputted by IDP
normal_flight - to load and visualize a normal flight in which the Goal is reached
low_battery   - to load and visualize a scenario where the drone returns Home due to low battery
```
(which are named correspondingly the files in `\Vis\output models`).


The directory `\Vis\plots` (currently) contains a saved visualization of a drone aborting its mission, due to a low battery signal. (More on this in `\Vis\visualization.pdf`.)

## Structures and Experiments

The directory `Structures and Experiments` contains all the used Structures for the different experiments, accompanied by their output. They are present in `.txt` format (allowing portability of the structures into the model), as well as in a PDF (`Experiments.pdf`) for a better readable experience.

## Policy

The directory `Policy` contains `Policy.pdf`, the complete (Planning and Target) policy, expressed in IDP syntax, as well as in natural language.
The directory `Policy\Completeness Policy` contains the proof for the completeness of the Planning Policy.

## README

For obvious reasons, this repository also contains the file you are currently reading.


## Context
This research was originally done as part of a thesis for obtaining the degree Master of Science in Engineering, Computer Science, Artificial Intelligence.
