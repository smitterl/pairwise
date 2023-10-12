import random
import re
import subprocess
import sys
from filters import minimal, pairwise

# holds the vt only filter
ONLY = []
PRINT_ORIGINAL = False
SHOW_STATS = False
APPLY_FILTER = None
OPTIONS = None
TEST_TYPE = "avocado-vt" # older versions of avocado might use 'VT'

def print_help(exit_code):
    print(sys.argv[0] + " [-t] [-s] <-p|-m> [<vt-options>] <--vt-only-filter argument>")
    print()
    print(" The command calls avocado to list test cases and then applies an algorithm to reduce the list of tests, for")
    print(" example by selecting only 2-way coverage over the available variant names (option -p).")
    print(" Please note, the current implementation assumes that avocado-vt test cases are listed with the 'VT' test type.")
    print(" If your avocado version uses another type, please adjust the script `TEST_TYPE` accordingly. You can identify")
    print(" the test type by running a valid avocado list and check the output.")
    print()
    print(" <vt-options> are additional filters enclosed by quotes, e.g. '--vt-type libvirt --vt-machine-type s390-virtio'")
    print(" <vt-only-filter> is a comma separated list of test names")
    print(" by passing flag -t the avocado command result is printed and not filtered")
    print(" by passing flag -s the number of original test names and filtered ones are shown")
    print(" -p selects the pairwise filter selecting all available test cases with maximal coverage of pairs, -s selects the minimal filter selecting all available test cases covering at least all variants")
    print(" EXAMPLE:")
    print()
    print("  The following command avocado list to obtain only those test cases for 'boot_integration' that are applicable")
    print("  the s390-virtio machine type, selects 2-way variant coverage and displays statistics.")
    print()
    print("   python avocado_list.py -s -p '--vt-machine-type s390-virtio --vt-type libvirt' boot_integration")
    print()
    print("  By skipping the statistics you can create a file to use later as your test selection:")
    print()
    print("   python avocado_list.py -p '--vt-machine-type s390-virtio --vt-type libvirt' boot_integration > test_list.only")
    sys.exit(exit_code)

def parse_args():
    if len(sys.argv) == 1:
        print_help(1)

    global ONLY
    global PRINT_ORIGINAL
    global SHOW_STATS
    global APPLY_FILTER
    global OPTIONS

    ONLY = sys.argv[-1]

    if ONLY.startswith("-h"):
        print_help(0)

    if not ("-m" in sys.argv or "-p" in sys.argv):
        print_help(1)
    
    if "-t" in sys.argv: 
        PRINT_ORIGINAL = True

    if "-s" in sys.argv:
        SHOW_STATS = True

    if "-p" in sys.argv:
        APPLY_FILTER = pairwise.pairwise

    if "-m" in sys.argv:
        APPLY_FILTER = minimal.minimal

    if "--" in sys.argv[-2]:
        OPTIONS = sys.argv[-2]


def get_avocado_list():
    test_names = []
    command = ("avocado list %s --vt-only-filter %s" %
               (OPTIONS, ONLY))
    output = subprocess.check_output(command, shell=True).decode()
    for row in output.split('\n'):
        if not row.startswith(TEST_TYPE):
            continue
        test_names.append(re.sub(TEST_TYPE + "\\s+.*autotest-libvirt.", "", row))
    return test_names


if __name__ == '__main__':
    parse_args()
    test_names = get_avocado_list()
    if PRINT_ORIGINAL:
        for name in test_names:
            print(name)
        sys.exit(0)

    random.shuffle(test_names)
    filtered_test_names = APPLY_FILTER(test_names)
    for name in filtered_test_names:
        print(name)

    if SHOW_STATS:
        print()
        print("The number of test cases was reduced"
                  " from %s to %s." % (len(test_names),
                      len(filtered_test_names)))
