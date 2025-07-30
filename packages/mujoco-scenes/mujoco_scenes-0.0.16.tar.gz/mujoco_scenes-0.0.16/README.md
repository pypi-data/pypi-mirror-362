# mujoco-scenes

This package contains a collection of utility functions for generating different types of scenes in Mujoco.

This is a programmatic way to compose scene files, inspired by [Mujoco Menagerie](https://github.com/google-deepmind/mujoco_menagerie).

## Usage

To load a robot into a particular scene, you can use the following code:

```python
from mujoco_scenes.mjcf import load_mjmodel

model = load_mjmodel("path/to/robot.xml", "smooth")

# To view the model, you can use:
mujoco.viewer.launch(model)
```
