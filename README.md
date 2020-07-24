# Basically, I am monkey

## Requirements

You should have a working installation of python 3.6+

## Installation

If you are downloading the project from scratch, follow these steps:

First, download the project to a folder and open the command window on that folder. Then, create a new environment
```
python3 -m venv monkey-environment
```
You should now activate the new environment. On Windows, run:
```
monkey-environment/Scripts/activate
```
On Unix or MacOS, run:
```
source monkey-environment/bin/activate
```
Now it's time to install the requirements. While the environment is active, run:
```
pip3 install -r requirements.txt
```
And that's it! You can now run the simulation

## Configuration

The settings can be found in the first few lines of `runapp.py`. Try changing them and running `runapp.py` with different configurations.

## Archiving

Once you run the simulation and the game ends, a CSV file with information about the game called `archives.csv` will be generated.