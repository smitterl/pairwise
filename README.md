https://github.com/avocado-framework/avocado-vt/ uses cartesian_config to create list of test cases over all test parameter combinations.

The `pairwise` takes a list of test case names (p1.p2.p3, e.g. virsh.domstats.argument) and filters out test cases whose test parameter values, represented by the partial test name, have already been covered in another test case earlier in the list.

An example of what wil be filtered can be seen in the unit test.
