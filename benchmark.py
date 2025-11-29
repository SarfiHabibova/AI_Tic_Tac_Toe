"""benchmark.py
Small helper to measure node counts and time for minimax vs alpha-beta
and with/without move ordering. Use to produce performance tables.
"""
import time
from game import initial_state
from search import minimax, minimax_ab, Instrument, search

def bench_empty_3x3():
    state = initial_state(3,3)
    instr = Instrument()
    t0 = time.time()
    v1, a1 = minimax(state, instr)
    t1 = time.time()
    nm_minimax = instr.node_count
    time_minimax = t1 - t0

    instr.reset()
    t0 = time.time()
    v2, a2 = minimax_ab(state, instr, use_ordering=False)
    t1 = time.time()
    nm_ab_noord = instr.node_count
    time_ab_noord = t1 - t0

    instr.reset()
    t0 = time.time()
    v3, a3 = minimax_ab(state, instr, use_ordering=True)
    t1 = time.time()
    nm_ab_ord = instr.node_count
    time_ab_ord = t1 - t0

    print("Minimax: nodes", nm_minimax, "time", time_minimax, "val", v1, "act", a1)
    print("AB no ordering: nodes", nm_ab_noord, "time", time_ab_noord, "val", v2, "act", a2)
    print("AB with ordering: nodes", nm_ab_ord, "time", time_ab_ord, "val", v3, "act", a3)

if __name__ == '__main__':
    bench_empty_3x3()
