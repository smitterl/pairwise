https://github.com/avocado-framework/avocado-vt/ uses cartesian_config to create list of test cases over the largest possible set of test parameter combinations, i.e. variants.

The `pairwise` takes a list of test case names (p1.p2.p3, e.g. virsh.domstats.argument) and filters out test cases whose test parameter values, represented by the variant name, have already been covered in another test case earlier in the list.

An example of what wil be filtered can be seen in the unit test.
