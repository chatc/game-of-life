from cell_core import *
from unit_test.test_cases import test_dic

cells = Cells()

# for pattern in test_dic:
#     cells.load_pattern(pattern)
#     cells.unit_test(10)

cells.load_pattern(test_dic[6])
cells.unit_test(10)
