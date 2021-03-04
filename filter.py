SEP = "."

def parts(line):
    p = line.split(SEP)
    return p

def pairwise(lines):
    diag = []

    for line in lines:
        
        if line in diag:
            continue
        
        line_parts = parts(line)
        candidates = [x for x in diag if len(parts(x)) == len(line_parts)]

        if len(candidates) == 0:
            diag.append(line)
            continue
        
        has_partial_rep = [False]*len(line_parts)
        
        for cand in candidates:
            cand_parts = parts(cand)
            for i in range(len(line_parts)):
                if cand_parts[i] == line_parts[i]:
                    has_partial_rep[i] = True

        if not all(has_partial_rep):
           diag.append(line)
           continue

    return diag


import unittest

test_lines = [
        "a1.b1.c1",
        "a1.b1.c2",
        "a1.b2.c1",
        "a1.b2.c2",
        "a1.d1"
        ]

class TestDiagonal(unittest.TestCase):

    def test_pairwise(self):
        pairwised = pairwise(test_lines)
        self.assertEqual(pairwised, ["a1.b1.c1", "a1.b1.c2", "a1.b2.c1", "a1.d1"])

if __name__ == '__main__':
    unittest.main()
