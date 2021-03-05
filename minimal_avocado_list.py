import re
import subprocess
import sys
from minimal_filter import minimal

# holds the vt only filter
ONLY = []
PRINT_ORIGINAL = False
SHOW_STATS = False

def print_help(exit_code):
    print(sys.argv[0] + " [-t] [-s] <--vt-only-filter argument>")
    print()
    print(" <vt-only-filter> is a comma separated list of test names")
    print(" by passing flag -t the avocado command result is printed and not filtered")
    print(" by passing flag -s the number of original test names and filtered ones are shown")
    sys.exit(exit_code)

def parse_args():
    if len(sys.argv) == 1:
        print_help(1)

    global ONLY
    ONLY = sys.argv[-1]

    if ONLY.startswith("-h"):
        print_help(0)
    
    if "-t" in sys.argv: 
        global PRINT_ORIGINAL
        PRINT_ORIGINAL = True

    if "-s" in sys.argv:
        global SHOW_STATS
        SHOW_STATS = True

def get_avocado_list():
    test_names = []
    command = ("avocado list --vt-type libvirt --vt-machine-type s390-virtio"
               " --vt-only-filter %s --paginator off" % ONLY)
    output = subprocess.check_output(command, shell=True).decode()
    for row in output.split('\n'):
        if not row.startswith("VT"):
            continue
        test_names.append(re.sub("VT\\s+.*autotest-libvirt.", "", row))
    return test_names


if __name__ == '__main__':
    parse_args()
    test_names = get_avocado_list()
    if PRINT_ORIGINAL:
        for name in test_names:
            print(name)
        sys.exit(0)

    filtered_test_names = minimal(test_names)
    for name in filtered_test_names:
        print(name)

    if SHOW_STATS:
        print()
        print("The number of test cases was reduced"
                  " from %s to %s." % (len(test_names),
                      len(filtered_test_names)))
