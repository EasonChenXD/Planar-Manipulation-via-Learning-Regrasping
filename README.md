## Planar Manipulation via Learning Regrasping


### Dataset

The objects in our dataset are from the Mechanical Components Benchmark (MCB). 

* `dataset/MCB_A_total.zip`: contain decomposed mesh files, related URDF files, and collected stable placement poses.
* `dataset_display/dataset_display.py`: display the collected stable placements.

### Installation

    pip install numpy pandas scipy glob
    pip install pybullet

### Data Preparation

Unzip the `./dataset/MCB_A_total.zip` and save in `./dataset`.

### Display Dataset

    cd ./dataset_display
    python dataset_display.py

