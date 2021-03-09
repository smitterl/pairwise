SEP = "."

def parts(line):
    p = line.split(SEP)
    return p

def pairwise_covered(candidates, line_parts):
    for i in range(len(line_parts) - 1):
        for j in range(i + 1, len(line_parts)):
            cand_i_j = [x for x in candidates if
                    x[i] == line_parts[i] and
                    x[j] == line_parts[j]]
            if not cand_i_j:
                return False
    return True

def pairwise(lines):
    diag = [] 

    for line in lines:

        line_parts = parts(line)
        if line_parts in diag:
            continue
        
        candidates = [x for x in diag if len(x) == len(line_parts)]
        if not (candidates and
                pairwise_covered(candidates, line_parts)):
            diag.append(line_parts)
            continue

    return [".".join(x) for x in diag] 


import unittest

test_lines = [
        "a1.b1.c1",
        "a1.b1.c2",
        "a1.b2.c1",
        "a1.b2.c2",
        "a2.b1.c1",
        "a2.b1.c2",
        "a2.b2.c1",
        "a2.b2.c2",
        "a1.d1"
        ]

class TestDiagonal(unittest.TestCase):

    def test_pairwise(self):
        pairwised = pairwise(test_lines)
        self.assertEqual(pairwised, [
            "a1.b1.c1",
            "a1.b1.c2",
            "a1.b2.c1",
            "a1.b2.c2",
            "a2.b1.c1",
            "a2.b1.c2",
            "a2.b2.c1",
            "a1.d1"])

if __name__ == '__main__':
    unittest.main()
