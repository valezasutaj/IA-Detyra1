import sys
import time
import random
from collections import deque

PUZZLES = {
    "easy": (
        "003020600"
        "900305001"
        "001806400"
        "008102900"
        "700000008"
        "006708200"
        "002609500"
        "800203009"
        "005010300"
    ),
    "medium": (
        "000000907"
        "000420180"
        "000705026"
        "100904000"
        "050000040"
        "000507009"
        "920108000"
        "034059000"
        "507000000"
    ),
    "hard": (
        "800000000"
        "003600000"
        "070090200"
        "050007000"
        "000045700"
        "000100030"
        "001000068"
        "008500010"
        "090000400"
    ),
}


def parse(s):
    return [int(c) for c in s]


def grid_lines(board):
    lines = []
    for r in range(9):
        if r % 3 == 0 and r:
            lines.append("------+-------+------")
        row = ""
        for c in range(9):
            if c % 3 == 0 and c:
                row += "| "
            v = board[r * 9 + c]
            row += (str(v) if v else ".") + " "
        lines.append(row.rstrip())
    return lines


def show(board):
    for line in grid_lines(board):
        print("  " + line)


def show_side_by_side(left, right, title_left, title_right):
    a, b = grid_lines(left), grid_lines(right)
    print(f"  {title_left:<21}     {title_right}")
    print(f"  {'-' * 21}     {'-' * 21}")
    for x, y in zip(a, b):
        print(f"  {x:<21}     {y}")


UNITS = []
for r in range(9):
    UNITS.append([r * 9 + c for c in range(9)])
for c in range(9):
    UNITS.append([r * 9 + c for r in range(9)])
for br in range(3):
    for bc in range(3):
        UNITS.append([(br * 3 + r) * 9 + bc * 3 + c for r in range(3) for c in range(3)])

PEERS = [set() for _ in range(81)]
for unit in UNITS:
    for i in unit:
        PEERS[i].update(j for j in unit if j != i)


def objective(board):
    f = 0
    for unit in UNITS:
        vals = [board[i] for i in unit if board[i]]
        f += len(vals) - len(set(vals))
    return f


def is_solved(board):
    return all(board) and objective(board) == 0


def candidates(board, i):
    used = {board[j] for j in PEERS[i]}
    return [v for v in range(1, 10) if v not in used]


def bfs(board, stats=None):
    queue = deque([(tuple(board), 0)])
    expanded = 0
    max_queue = 1
    per_level = {}

    while queue:
        node, depth = queue.popleft()
        expanded += 1
        per_level[depth] = per_level.get(depth, 0) + 1

        best_i, best_c = None, None
        for i in range(81):
            if node[i] == 0:
                c = candidates(node, i)
                if best_c is None or len(c) < len(best_c):
                    best_i, best_c = i, c
                    if len(c) <= 1:
                        break

        if best_i is None:
            if objective(node) == 0:
                if stats is not None:
                    stats.update(expanded=expanded, max_queue=max_queue, per_level=per_level)
                return list(node)
            continue

        if not best_c:
            continue

        for v in best_c:
            child = list(node)
            child[best_i] = v
            queue.append((tuple(child), depth + 1))
        max_queue = max(max_queue, len(queue))

    if stats is not None:
        stats.update(expanded=expanded, max_queue=max_queue, per_level=per_level)
    return None


def header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def solve_level(name):
    board = parse(PUZZLES[name])
    empty = board.count(0)
    header(f"SUDOKU  niveli {name.upper()}  (BFS me backtracking)")
    print(f"  qeli te dhena        : {81 - empty}")
    print(f"  qeli te zbrazeta     : {empty}")
    print(f"  hapesira e kerkimit  : 9^{empty} ~ {9.0 ** empty:.2e}")
    print()
    stats = {}
    t = time.time()
    sol = bfs(board, stats)
    dt = time.time() - t
    if sol:
        show_side_by_side(board, sol, "Enigma", "Zgjidhja")
        print()
        ok = is_solved(sol)
        print(f"  Rezultati            : {'zgjidhje valide' if ok else 'GABIM'} (f = {objective(sol)}, "
              f"{'asnje konflikt' if ok else 'ka konflikte'})")
    else:
        show(board)
        print("\n  Rezultati            : nuk u gjet zgjidhje")
    print(f"  nyje te zgjeruara    : {stats['expanded']}")
    print(f"  radha maksimale      : {stats['max_queue']}")
    print(f"  thellesia e zgjidhjes: {max(stats['per_level'])}")
    print(f"  koha                 : {dt:.3f} s")
    lv = stats["per_level"]
    levels = sorted(lv)
    print()
    print("  Nyje per nivel te pemes (nivel = sa qeli ka mbushur kerkimi):")
    for start in range(0, len(levels), 10):
        chunk = levels[start:start + 10]
        print(f"    nivel {chunk[0]:2d}-{chunk[-1]:2d}: " + " ".join(f"{lv[d]:5d}" for d in chunk))


def landscape(name, samples=100000):
    random.seed(1)
    board = parse(PUZZLES[name])
    empties = [i for i in range(81) if board[i] == 0]
    hist = {}
    for _ in range(samples):
        b = list(board)
        for i in empties:
            b[i] = random.randint(1, 9)
        f = objective(b)
        hist[f] = hist.get(f, 0) + 1
    header(f"LANDSCAPE  niveli {name.upper()}  ({len(empties)} qeli te zbrazeta, {samples} mbushje te rastit)")
    print(f"  f minimal   : {min(hist)}")
    print(f"  f maksimal  : {max(hist)}")
    print(f"  f mesatar   : {sum(f * c for f, c in hist.items()) / samples:.1f}")
    print(f"  zgjidhja    : f = 0 (nuk u gjet asnjehere me mbushje te rastit)")
    top = sorted(hist.items(), key=lambda x: -x[1])[:5]
    print("  vlerat me te shpeshta te f:")
    for f, c in sorted(top):
        print(f"    f = {f:3d} : {c:6d} mostra ({100 * c / samples:.1f} %)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "landscape":
        for name in PUZZLES:
            landscape(name)
    elif args:
        solve_level(args[0])
    else:
        for name in PUZZLES:
            solve_level(name)
