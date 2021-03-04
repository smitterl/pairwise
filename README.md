https://github.com/avocado-framework/avocado-vt/ uses cartesian_config to create list of test cases over the largest possible set of test parameter combinations, i.e. variants.

The `pairwise` takes a list of test case names (p1.p2.p3, e.g. virsh.domstats.argument) and filters out test cases whose test parameter values, represented by the variant name, have already been covered in another test case earlier in the list.

An example of what will be filtered can be seen in the unit test.

Example:

A filtered output could look like:
```bash
# python3 filter_avocado_list.py -s virsh.boot,boot_integration
virsh.boot.loadparm
virsh.boot.by_seabios.positive_test.options.boot.hd.file_disk.boot_dev.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.file_disk.boot_dev.os_loader.valid_loader_type.no_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.file_disk.boot_dev.os_loader.no_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.file_disk.boot_order.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.block_disk.boot_dev.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.network_disk.ceph.boot_dev.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.network_disk.ceph.boot_dev.os_loader.valid_loader_type.no_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.network_disk.ceph.boot_dev.os_loader.no_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.network_disk.ceph.boot_order.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.hd.network_disk.glusterfs.boot_dev.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.cdrom.boot_dev.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.cdrom.boot_dev.os_loader.valid_loader_type.no_readonly
virsh.boot.by_seabios.positive_test.options.boot.cdrom.boot_dev.os_loader.no_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.boot.cdrom.boot_order.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.options.no_boot.os_loader.valid_loader_type.valid_readonly
virsh.boot.by_seabios.positive_test.boot_order_big_integer
virsh.boot.by_seabios.positive_test.two_same_boot_dev
virsh.boot.by_seabios.negative_test.not_existing_loader
virsh.boot.by_seabios.negative_test.not_existing_loader_type
virsh.boot.by_seabios.negative_test.not_existing_boot_dev
virsh.boot.by_seabios.negative_test.special_boot_order.negative
virsh.boot.by_seabios.negative_test.special_boot_order.character
virsh.boot.by_seabios.negative_test.special_boot_order.zero
boot_integration.by_qemu_on_s390.boot_dev.check_menu
boot_integration.by_qemu_on_s390.boot_dev.boot_non_default

The number of test cases was reduced from 52 to 26.
```

The filter can be double checked by
```bash
# python3 filter_avocado_list.py -t virsh.boot,boot_integration > original.list
# python3 filter_avocado_list.py virsh.boot,boot_integration > filtered.list
diff -y filtered.list original.list
```
