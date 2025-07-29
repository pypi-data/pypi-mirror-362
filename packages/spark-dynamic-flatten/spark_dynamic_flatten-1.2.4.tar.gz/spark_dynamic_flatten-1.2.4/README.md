# spark_dynamic_flatten

Tools to dynamically flatten nested schemas with spark based on configuration and compare pyspark dataframe schemas.

## Description

This project provides tools for working with (Py)Spark dataframes, including functionality to dynamically flatten nested data structures and compare schemas. It is designed to help users manage complex data transformations and schema validations in PySpark.

## Features

- Dynamically flatten nested PySpark dataframes based on configuration (only flatten what is needed).
- Compare schemas of different PySpark dataframes.
- Utility functions for schema manipulation and validation.

## Installation

To install the dependencies for this project, you can use [Poetry](https://python-poetry.org/). Ensure you have Python 3.8 or higher installed.

1. Clone the repository:
   ```sh
   git clone https://github.com/hardykoepf/spark_dynamic_flatten.git
   cd spark_dynamic_flatten

2. Alternatively this is on pypi:
```
pip install pyspark-dynamic-flatten
```

## Classes within this solution

The solution consists of three classes implementing specific trees:
- Tree: Basic tree class implementing standard tree data stucture with nodes referencing to the parent node and to the children nodes
- SchemaTree: Inherited from Tree. Especially for handling schemas of (pyspark) spark dataframes. With this class you can for example generate a json config file for Flatten class based on a dataframe schema.
- FlattenTree: Inherited from Tree. Especially for flattening a nested schema of spark dataframe

Also besides the trees, a TreeManager offers methods for creating a tree based on json file, json string or spark schema.  
  
The flattening is executed within the Flatten class.

### General tree functions

The trees are defined to be self managed. This means there is no separation between a tree and node in implementation.  
  
To get a quick overview how the tree is looking like, the method print() is printing the tree:
```
root_node_of_tree.print()
```
  
If you need to have the tree as list, the function get_tree_as_list() will return a list with the complete path to every node.
```
root_node_of_tree.get_tree_as_list()
```
  
The method get_tree_layered() will return the tree as a nested list. Which means the layers are represented by a separate list with the nodes of this layer. The outer list keeps all the lists together.  
The list on index 0 from outer list holds the nodes of layer 1. On index 1 represents layer 2 and so on.  
[[nodes_layer_1], [nodes_layer_2], [nodes_layer_3], [nodes_layer_4], ...]
```
root_node_of_tree.get_tree_layered()
```

#### Comparing Trees
Comparing trees is really helpful. Therefore you can use the equals function.
This will work for all kind of trees and will return True if the two trees you compare are equal.

```
from spark_dynamic_flatten import TreeManager

tree_schema1 = TreeManager.from_struct_type(df1.schema)
tree_schema2 = TreeManager.from_struct_type(df2.schema)

if tree_schema1.equals(tree_schema2):
    print("Schemas are equal")
```

#### Symmetric difference of Trees
To see, how trees differ in both directions, the symmetric_difference function will return a set of tuples (every tuple represents is one node/path).
Enhancing above example with symmetric_difference:

```
from spark_dynamic_flatten import TreeManager

tree_schema1 = TreeManager.from_struct_type(df1.schema)
tree_schema2 = TreeManager.from_struct_type(df2.schema)

if tree_schema1.equals(tree_schema2):
    print("Schemas are equal")
else:
    difference = tree_schema1.symmetric_difference(tree_schema2)
    print("Following symmetric differences (set of tuples):)
    print(difference)
```

#### Subtraction of Trees
you can also subtract one tree from another and see what paths will remain.
The result will be a set of tuples (every tuple represents is one node/path).
It's more or less similar to symmetric_difference, but subtract only works in one direction.

```
from spark_dynamic_flatten import TreeManager

tree_schema1 = TreeManager.from_struct_type(df1.schema)
tree_schema2 = TreeManager.from_struct_type(df2.schema)

if tree_schema1.equals(tree_schema2):
    print("Schemas are equal")
else:
    difference = tree_schema1.subtract(tree_schema2)
    print("Following differences when subtracting tree_schema2 from tree_schema1 (set of tuples):)
    print(difference)
```

#### Intersection of trees
Instead of searching for differences, you can search for intersection of two trees. 
Result will be the "lowest common denominator" of both trees.  
The result of this function will not be a simple set - it will return the common part of the trees.
When there are no common parts, the result will be None.  
This will be helpful when you have two Schemas and search for similarities.

```
from spark_dynamic_flatten import TreeManager

tree_schema1 = TreeManager.from_struct_type(df1.schema)
tree_schema2 = TreeManager.from_struct_type(df2.schema)

common_denominator =  tree_schema1.intersection(tree_schema2, only_by_names=True)
if common_denominator:
    common_denominator.print()
```


## Usage

Because two different use cases are implemented, we have to separate. But the use-cases behind these classes are related to each other.  

### Schemas

For importing a spark schema as a structured tree, you have the option to use a Json file representing a spark schema, or you can import a json string representing a schema or at least using directly a StrucType.  
In general, when creating a tree the TreeManager comes into play. The TreeManager offers methods for generating the right type of tree.  
Especially for schemas, following static methods are offered (creating a Tree of SchemaTree instance nodes):
- TreeManager.from_struct_type(struct) -> TreeManager
- TreeManager.from_schema_json_string(json_str) -> TreeManager
- TreeManager.from_schema_json_file(json_file) -> TreeManager

For Schemas, the nodes are instances of SchemaTree class.


#### Generate configuration for fully flattening a dataframe

After parsing the schema of dataframe to a tree object, we generate the json config we can use for completely flatten the dataframe (or modify if we only need specific fields flattened).  
In general this package should be used if you don't need to fully flatten. So only take whats needed as configuration.
But be also aware: leaf nodes can have the same name in different branches.  
When there are "duplicates", the name will be incremented by a number to be unique. This behaviour can be preserved when defining an alias in configuration for the duplicates.

```
from spark_dynamic_flatten import TreeManager

tree_schema1 = TreeManager.from_struct_type(df1.schema)
json_string = tree_schema1.generate_fully_flattened_json()
```

### Flatten
 
The configuration for flatten a nested structure is defined by the path to the leaf fields separated by a dot.  
E.g. node1.node2.node3.leaf_field  
For every path/field a alias and also the boolean if the field should be an identifier (key) for the flattened table is defined.  
To summarize, for every path/field to be flattened, a dictionary with following keys has to be defined:
- path
- alias
- is_identifier

E.g.:  
{"path": "node1.node2.node3.leaf_field", "alias": "leaf_alias", "is_identifier": False}  
  
At least, the paths are collected by an outer dict with the key "field_paths"  
E.g.:
```
{ "field_paths": [
    {"path": "node1.node2.node3.leaf_field", "alias": "leaf_alias", "is_identifier": False},
    {"path": "node11.node22.node33.leaf_field2", "alias": None, "is_identifier": False}
    ]
}

```
This json configuration could be generated based on a Dataframe schema. See above example with using method "generate_fully_flattened_json" based on a SchemaTree.  
  
To import the configuration, you have the option to have it as json file, json string or within a dict. Therefore again the TreeManager is used.
- TreeManager.from_flatten_type(struct) -> FlattenTree
- TreeManager.from_flatten_json_string(json_str) -> FlattenTree
- TreeManager.from_flatten_json_file(json_file) -> FlattenTree
  
When a FlattenTree was instanciated by the configuration, you use this instance together with the Dataframe to be flattened and call flatten method of class Flatten:
```
from spark_dynamic_flatten import TreeManager
from spark_dynamic_flatten import FlattenTree
from spark_dynamic_flatten import Flatten

root_tree = TreeManager.from_flatten_json_string(json_string)
df_flattened = Flatten.flatten(df1, root_tree)

```
  
The flatten method has to additional optional attributes called:
- rename_columns: Renames the colums of flattened Dataframe to its leaf nodes (or alias when an alias was defined in configuration)
- filter_null_rows: When only identifier columns will have meaningful values and all non-identifying columns will have NULL values, these rows will be filtered in flattened Dataframe.