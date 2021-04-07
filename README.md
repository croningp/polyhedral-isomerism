# polyhedral isomers

Determines number of isomers for certain chemical compounds with geometric structures

## Method A:
Written in java. Compile and run _Octahedron.java_. <br>
Explanation: Geometries are stored as length 12 bit strings. Each bit index maps to an octahedron *half edge* site, and the presence or absence of a bond at this location is denoted by 0 or 1, respectively. Valid strings are appended to the variable _octs_. Print out of _octs.size()_ gives number of entities at each iteration. Output of final _octs_ is given in _octahedra.txt_

## Method B:

Written in python. To use: run main.py. <br>
Explanation: Geometries are stored as a list of _Node_ objects, which have attributes _origin_ (numpy array) and _bonds_ (list of numpy arrays). _Origin_ denotes the cartesian location of the Node and each _bond_ in _bonds_ represents a vector from the _origin_ towards a neighbouring Node _origin_. Each Node has four neighbours, which results in 16 different bonding possibilities (1x0, 4x1, 6x2, 4x3 and 1x4 bonds). For an octahedron, the six nodes, each with 16 bonding configurations represents the *node pool* and combinations of these are used to generate all possible isomer configurations. 


## Authors

All software was written as part of the [Cronin Lab 2019](http://www.chem.gla.ac.uk/cronin/)

* [Dr. Edward Lee](mailto:Edward.Lee@glasgow.ac.uk)
* [Dr. Deliang Long](mailto:Deliang.Long@glasgow.ac.uk)


---

## License

[![MIT](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/220px-MIT_logo.svg.png)](https://opensource.org/licenses/MIT)