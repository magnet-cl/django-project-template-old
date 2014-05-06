# Bootstrap Customized

This is a customized version of bootstrap. 

To enable bootstrap updates only two files are modified:

* variables.less: Only changed allowed is to value of the variables
* variables.less: Only changed allowed if it's backwards compatible (mixings
accepting the same parameters)
* bootstrap.less: Only changed allowed is to add @import "custom.less"; 

All further changes need to be added in the custom.less file
