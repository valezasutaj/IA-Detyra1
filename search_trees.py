import sys
from collections import deque


def header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_tree(root, successors, fmt, valid, max_depth, is_goal=None):
    counts = {}

    def rec(state, action, depth, prefix, last, path):
        counts[depth] = counts.get(depth, 0) + 1
        branch = "" if depth == 0 else ("`-- " if last else "|-- ")
        lines = fmt(state).split("\n")
        note = ""
        expand = True
        if not valid(state):
            note = "  X (jovalide)"
            expand = False
        elif state in path:
            note = "  (perseritje)"
            expand = False
        elif is_goal and is_goal(state):
            note = "  <-- GOAL"
        head = (action + ": " if action else "") + lines[0] + note
        print(prefix + branch + head)
        child_prefix = prefix + ("" if depth == 0 else ("    " if last else "|   "))
        for ln in lines[1:]:
            print(child_prefix + ln)
        if not expand or depth == max_depth:
            return
        kids = successors(state)
        for i, (act, s2) in enumerate(kids):
            rec(s2, act, depth + 1, child_prefix, i == len(kids) - 1, path | {state})

    print(f"  Pema deri ne thellesi {max_depth}:")
    print("  Shenimet: X = gjendje jovalide, (perseritje) = gjendje e pare me heret ne kete rruge,")
    print("            te dyja nuk zgjerohen me tej. <-- GOAL = gjendja e synuar.")
    print()
    rec(root, None, 0, "  ", True, frozenset())
    print()
    print("  Nyje per nivel: " + ", ".join(f"thellesia {d}: {counts[d]}" for d in sorted(counts))
          + f"   (gjithsej {sum(counts.values())})")


PUZZLE_START = (1, 2, 3,
                4, 0, 6,
                7, 5, 8)
PUZZLE_GOAL = (1, 2, 3,
               4, 5, 6,
               7, 8, 0)


def puzzle_successors(s):
    i = s.index(0)
    r, c = divmod(i, 3)
    out = []
    for act, dr, dc in (("U", -1, 0), ("D", 1, 0), ("L", 0, -1), ("R", 0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            t = list(s)
            t[i], t[j] = t[j], t[i]
            out.append((act, tuple(t)))
    return out


def puzzle_fmt(s):
    rows = []
    for r in range(3):
        rows.append(" ".join("_" if v == 0 else str(v) for v in s[r * 3:r * 3 + 3]))
    return "\n".join(rows)


MC_START = (3, 3, 0)
MC_GOAL = (0, 0, 1)
MC_MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def mc_valid(s):
    m, c, b = s
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False
    if m and c > m:
        return False
    if (3 - m) and (3 - c) > (3 - m):
        return False
    return True


def mc_successors(s):
    m, c, b = s
    out = []
    for dm, dc in MC_MOVES:
        if b == 0:
            ns = (m - dm, c - dc, 1)
        else:
            ns = (m + dm, c + dc, 0)
        if 0 <= ns[0] <= 3 and 0 <= ns[1] <= 3:
            out.append((f"{dm}M{dc}C", ns))
    return out


def mc_fmt(s):
    m, c, b = s
    return f"({m}M,{c}C,{'majtas' if b == 0 else 'djathtas'})"


def mc_bfs():
    parent = {MC_START: None}
    q = deque([MC_START])
    while q:
        s = q.popleft()
        if s == MC_GOAL:
            path = []
            while s:
                path.append(s)
                s = parent[s][0] if parent[s] else None
            return path[::-1]
        for act, s2 in mc_successors(s):
            if mc_valid(s2) and s2 not in parent:
                parent[s2] = (s, act)
                q.append(s2)
    return None


RWS_EMP, RWS_DAYS = 4, 7
RWS_LEN = RWS_EMP * RWS_DAYS
RWS_SHIFTS = "DN-"
RWS_MAX_WORK = 5
RWS_MIN_OFF = 2
RWS_MAX_OFF = 4


def blocks_ok(t):
    i = 0
    while i < len(t):
        j = i
        while j < len(t) and (t[j] == "-") == (t[i] == "-"):
            j += 1
        if t[i] != "-":
            if j - i > RWS_MAX_WORK:
                return False
        else:
            if j - i > RWS_MAX_OFF:
                return False
            if i > 0 and j < len(t) and j - i < RWS_MIN_OFF:
                return False
        i = j
    return True


def rws_valid(s):
    t = s + s if len(s) == RWS_LEN else s
    if "ND" in t:
        return False
    if not blocks_ok(t):
        return False
    for d in range(RWS_DAYS):
        col = [s[p] for p in range(d, len(s), RWS_DAYS)]
        if col.count("D") > 1 or col.count("N") > 1 or col.count("-") > RWS_EMP - 2:
            return False
    return True


def rws_successors(s):
    if len(s) == RWS_LEN:
        return []
    return [(sh, s + sh) for sh in RWS_SHIFTS]


def rws_fmt(s):
    return f'"{s}"' if s else "(zbrazet)"


def rws_dfs():
    stack = [""]
    nodes = 0
    while stack:
        s = stack.pop()
        nodes += 1
        if len(s) == RWS_LEN:
            return s, nodes
        for _, s2 in reversed(rws_successors(s)):
            if rws_valid(s2):
                stack.append(s2)
    return None, nodes


def rws_print_roster(cycle):
    days = ["Hen", "Mar", "Mer", "Enj", "Pre", "Sht", "Die"]
    print("            " + " ".join(f"{d:>3}" for d in days))
    for w in range(RWS_EMP):
        print(f"  Java {w + 1}:   " + " ".join(f"{cycle[w * 7 + d]:>3}" for d in range(7)))
    print("  (punetori 1 fillon nga java 1, punetori 2 nga java 2, e keshtu me radhe)")


if __name__ == "__main__":
    args = sys.argv[1:]
    which = args[0] if args else "all"
    depth = int(args[1]) if len(args) > 1 else None

    if which in ("all", "puzzle"):
        header("SEARCH TREE 1: 8-PUZZLE")
        print("  Gjendja: tabela 3x3, _ = vendi i zbrazet. Veprimi = levizja e vendit te zbrazet")
        print("  (U = lart, D = poshte, L = majtas, R = djathtas).")
        print("  Gjendja fillestare: 1 2 3 / 4 _ 6 / 7 5 8     Goal: 1 2 3 / 4 5 6 / 7 8 _")
        print()
        print_tree(PUZZLE_START, puzzle_successors, puzzle_fmt, lambda s: True,
                   depth or 2, is_goal=lambda s: s == PUZZLE_GOAL)

    if which in ("all", "mc"):
        header("SEARCH TREE 2: MISSIONARIES AND CANNIBALS")
        print("  Gjendja: (misionare ne bregun e majte, kanibale ne bregun e majte, ana e barkes).")
        print("  Veprimi: kush hip ne barke, p.sh. 1M1C = nje misionar dhe nje kanibal.")
        print("  Fillimi: (3M,3C,majtas)     Goal: (0M,0C,djathtas)")
        print()
        print_tree(MC_START, mc_successors, mc_fmt, mc_valid, depth or 3,
                   is_goal=lambda s: s == MC_GOAL)
        path = mc_bfs()
        print()
        print(f"  Zgjidhja me e shkurter (gjetur me BFS): {len(path) - 1} hapa")
        for i in range(1, len(path)):
            act = next(a for a, s2 in mc_successors(path[i - 1]) if s2 == path[i])
            print(f"    hapi {i:2d}: {mc_fmt(path[i - 1]):18s} --{act}-->  {mc_fmt(path[i])}")

    if which in ("all", "rws"):
        header("SEARCH TREE 3: ROTATING WORKFORCE SCHEDULING")
        print(f"  {RWS_EMP} punetore, cikli = {RWS_EMP} jave x 7 dite = {RWS_LEN} pozita, shifts: D = dite, N = nate, - = pushim")
        print(f"  Kerkesa: cdo dite te javes 1 D dhe 1 N. Kufizimet: pa N->D, max {RWS_MAX_WORK} dite pune rresht,")
        print(f"  pushimi {RWS_MIN_OFF}-{RWS_MAX_OFF} dite rresht.")
        print("  Gjendja: shift-et e caktuara deri tani per pozitat 0, 1, 2, ... te ciklit.")
        print()
        print_tree("", rws_successors, rws_fmt, rws_valid, depth or 3)
        cycle, nodes = rws_dfs()
        print()
        print(f"  Nje cikel i plote i gjetur me DFS + backtracking ({nodes} nyje):")
        print(f'    "{cycle}"')
        print()
        rws_print_roster(cycle)
