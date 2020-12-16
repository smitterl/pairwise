https://github.com/avocado-framework/avocado-vt/ uses cartesian_config to create list of test cases over all test parameter combinations.

The `pairwise` function applies the technique of pairwise testing, that is, it takes a list of test case names (p1.p2.p3, e.g. virsh.domstats.argument) and filters auto only two-way combinations.

And example of what wil be filtered can be seen in the unit test.

More info on pairwise tesing

"In computer science, all-pairs testing or pairwise testing is a combinatorial method of software testing that, for each pair of input parameters to a system (typically, a software algorithm), tests all possible discrete combinations of those parameters. Using carefully chosen test vectors, this can be done much faster than an exhaustive search of all combinations of all parameters, by "parallelizing" the tests of parameter pairs."
(source: https://en.wikipedia.org/wiki/All-pairs_testing)
