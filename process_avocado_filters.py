"""
This script takes as input a list of job names.

It expects vt-no-filters and vt-only-filters to be
defined in files of the same name, suffixed accordingly
with ".only" or ".no".

For each job name it will call avocado with these filters
and additional arguments to create a new vt-only-filters
for execution on s390x.

The script supposes that the avocado_list.py script can
be called successfully, e.g. in a python venv where
avocado has been bootstrapped with --vt-type libvirt
previously.
"""
import re
import sys
import yaml

from os import path
from os import popen

def get_config(config_path):
    """
    Sample config file:

    output_dir: /tmp/job-filters
    job_names:
        - function-cpu
        - function-virtual_disk
    """
    with open(config_path) as f:
        return yaml.safe_load(f)


def write_file(output_path, content):
    with open(output_path, 'w') as f:
        f.write(content)


def create_file(job_name, output_dir):
    """
    Creates a new file to include the vt-only-filters on s390x
    in output_dir. It assumes that for the job name there are
    already two files containing the full original vt-no-filters
    and vt-only-filters with corresponding suffixes in the same path.
    """
    whitespace = re.compile(r'\s+')

    no_file_path = path.join(output_dir, job_name + ".no")
    only_file_path = path.join(output_dir, job_name + ".only")

    cmd_no_filter = "paste -s -d, %s" % no_file_path
    no_filter = popen(cmd_no_filter).read()
    no_filter = re.sub(whitespace, '', no_filter)

    cmd_only_filter = "paste -s -d, %s" % only_file_path
    only_filter = popen(cmd_only_filter).read()
    only_filter = re.sub(whitespace, '', only_filter)

    cmd = ("python avocado_list.py -m '--vt-type libvirt"
           " --vt-no-filter \"%s\" --vt-machine-type s390-virtio'"
           " \"%s\" | sort" % (no_filter, only_filter))
    s390x_only = popen(cmd).read().strip('\n')

    write_file(path.join(output_dir, job_name + "-s390x.only"), s390x_only)

def create_files(config_path):
    config = get_config(config_path)
    for job_name in config['job_names']:
        create_file(job_name, config['output_dir'])


if __name__ == "__main__":
    create_files(sys.argv[1])
