# pyRinocitologia

Central repository for Rinocitologia project developed as an undergraduate thesis.
The purpose of this repository is to contains all development code allowing




## Design Philosophy
* Reproducibility
* Process automation
* Explicit is better than implicit
* Infrastructure built around data

(nothing new! based on: [12factor](https://12factor.net/) & [cookiecutter data science](http://drivendata.github.io/cookiecutter-data-science/))

## Data Gathering 


#### Data Gathering Workflow Diagram
![](https://drive.google.com/uc?id=1DLjIHESDzRHFE9W1zJzMDOFPxOe6otdL)

### Tools
Various utilities script has been developed

###### note:
image annotation tool : [VGG Image Annotation (VIA)](http://www.robots.ox.ac.uk/~vgg/software/via/)

### Warnings
 The python interpreter cwd (Current Working Directory)
 must be set to the **root directory**/parent directory of __/src__ folder 
 eg:
 ```python
import os
os.chdir("..")
```
or equivalently, call python interpreter from the parent directory:
 ```bash
python <parent dir>/src <script name>
```
or add to [PYTHONPATH](https://docs.python.org/3.6/using/cmdline.html#environment-variables) the parent directory:
 ```bash
export PYTHONPATH=<root directory>
python <script name>
```


(if you use pyCharm IDE this is done automatically in run configuration)

----

