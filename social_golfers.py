import sys
import time
import itertools
from math import factorial


def objective(schedule, g, p):
    n = g * p
    met = [[0] * n for _ in range(n)]
    f = 0
    for week in schedule:
        for group in week:
            if len(group) != p:
                f += abs(len(group) - p)
            for a, b in itertools.combinations(group, 2):
                met[a][b] += 1
    for a in range(n):
        for b in range(a + 1, n):
            if met[a][b] > 1:
                f += met[a][b] - 1
    return f


class GolferDFS:
    def __init__(self, g, p, w, time_limit=None):
        self.g, self.p, self.w = g, p, w
        self.n = g * p
        self.met = [[False] * self.n for _ in range(self.n)]
        self.schedule = []
        self.nodes = 0
        self.time_limit = time_limit
        self.start = None
        self.timed_out = False

    def solve(self):
        self.start = time.time()
        first = [list(range(k * self.p, (k + 1) * self.p)) for k in range(self.g)]
        for group in first:
            for a, b in itertools.combinations(group, 2):
                self.met[a][b] = self.met[b][a] = True
        self.schedule.append(first)
        if self.w == 1:
            return self.schedule
        ok = self._week(1)
        return self.schedule if ok else None

    def _week(self, wk):
        if wk == self.w:
            return True
        self.schedule.append([])
        free = set(range(self.n))
        if self._group(wk, 0, free):
            return True
        self.schedule.pop()
        return False

    def _group(self, wk, gi, free):
        if gi == self.g:
            return self._week(wk + 1)
        first = min(free)
        free.discard(first)
        self.schedule[wk].append([first])
        if self._slot(wk, gi, 1, free):
            return True
        self.schedule[wk].pop()
        free.add(first)
        return False

    def _slot(self, wk, gi, si, free):
        if self.timed_out:
            return False
        if self.time_limit and time.time() - self.start > self.time_limit:
            self.timed_out = True
            return False
        group = self.schedule[wk][gi]
        if si == self.p:
            return self._group(wk, gi + 1, free)
        last = group[-1]
        for cand in sorted(free):
            if cand < last:
                continue
            if any(self.met[cand][m] for m in group):
                continue
            self.nodes += 1
            group.append(cand)
            free.discard(cand)
            for m in group[:-1]:
                self.met[cand][m] = self.met[m][cand] = True
            if self._slot(wk, gi, si + 1, free):
                return True
            for m in group[:-1]:
                self.met[cand][m] = self.met[m][cand] = False
            free.add(cand)
            group.pop()
        return False


def header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_schedule(schedule, g, p):
    width = 3 * p + 1
    print("          " + "".join(f"Grupi {k + 1}".ljust(width + 2) for k in range(g)))
    for i, week in enumerate(schedule):
        groups = "  ".join("[" + ",".join(f"{x:2d}" for x in grp) + "]" for grp in week)
        print(f"  Java {i + 1:2d}  {groups}")
    f = objective(schedule, g, p)
    if f == 0:
        print(f"\n  Kontrolli: f = 0  ->  asnje cift lojtaresh nuk luan dy here ne te njejtin grup")
    else:
        print(f"\n  Kontrolli: f = {f}  ->  orari NUK eshte valid")


def run_instance(g, p, w, time_limit):
    s = GolferDFS(g, p, w, time_limit=time_limit)
    t = time.time()
    res = s.solve()
    return res, s, time.time() - t


def weeks_count(g, p):
    n = g * p
    return factorial(n) // (factorial(p) ** g * factorial(g))


def all_partitions(players, p):
    if not players:
        yield []
        return
    first = players[0]
    for rest in itertools.combinations(players[1:], p - 1):
        group = [first] + list(rest)
        remaining = [x for x in players if x not in group]
        for tail in all_partitions(remaining, p):
            yield [group] + tail


def landscape(g, p, w):
    n = g * p
    parts = list(all_partitions(list(range(n)), p))
    hist = {}
    total = 0
    for combo in itertools.product(parts, repeat=w):
        f = objective(list(combo), g, p)
        hist[f] = hist.get(f, 0) + 1
        total += 1
    header(f"LANDSCAPE  g = {g} grupe, p = {p} lojtare/grup, w = {w} jave  (n = {n} lojtare)")
    print(f"  {'ndarje te mundshme per nje jave':<34}: {len(parts)}")
    print(f"  {f'gjendje gjithsej ({len(parts)}^{w})':<34}: {total}")
    print()
    print("    f   | gjendje  |   % ")
    print("  ------+----------+--------")
    for f in sorted(hist):
        tag = "   <- zgjidhjet" if f == 0 else ""
        print(f"  {f:4d}  | {hist[f]:8d} | {100 * hist[f] / total:6.2f}{tag}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] == "landscape":
        for g, p, w in [(2, 2, 2), (2, 2, 3), (3, 2, 2), (3, 2, 3), (3, 2, 4)]:
            landscape(g, p, w)
        g, p = 8, 4
        header("LANDSCAPE  instanca e detyres: g = 8, p = 4 (n = 32 lojtare)")
        print(f"  {'ndarje te mundshme per nje jave':<34}: {weeks_count(g, p)}  (~{weeks_count(g, p):.2e})")
        for w in (2, 5, 10):
            print(f"  {f'gjendje per w = {w} jave':<34}: ~{float(weeks_count(g, p)) ** w:.2e}")
        print(f"  {'kufiri teorik i javeve':<34}: (n-1)/(p-1) = 31/3 -> 10 jave")
        sys.exit()

    if len(args) == 3:
        g, p, w = map(int, args)
        header(f"SOCIAL GOLFERS  g = {g} grupe, p = {p} lojtare/grup, w = {w} jave  (DFS me backtracking)")
        res, s, dt = run_instance(g, p, w, time_limit=120)
        if res:
            print(f"  Rezultati : zgjidhje u gjet")
            print(f"  nyje      : {s.nodes}")
            print(f"  koha      : {dt:.2f} s")
            print()
            print_schedule(res, g, p)
        elif s.timed_out:
            print(f"  Rezultati : kohe e tejkaluar (120 s) pas {s.nodes} nyjeve, asnje zgjidhje")
        else:
            print(f"  Rezultati : nuk ekziston zgjidhje ({s.nodes} nyje te vizituara)")
        sys.exit()

    g, p = 8, 4
    header("SOCIAL GOLFERS  32 lojtare, 8 grupe x 4 lojtare  (DFS me backtracking)")
    print("  Provohen w = 1, 2, 3, ... jave, me se shumti 60 s per secilen.\n")
    print("   jave | rezultati          |      nyje |    koha")
    print("  ------+--------------------+-----------+---------")
    best = None
    for w in range(1, 11):
        res, s, dt = run_instance(g, p, w, time_limit=60)
        if res:
            print(f"  {w:5d} | OK                 | {s.nodes:9d} | {dt:6.2f} s")
            best = res
        else:
            why = "kohe e tejkaluar" if s.timed_out else "nuk ka zgjidhje"
            print(f"  {w:5d} | {why:18s} | {s.nodes:9d} | {dt:6.2f} s")
            break
    print()
    print(f"  Kufiri teorik: cdo jave nje lojtar takon {p - 1} lojtare te rinj nga {g * p - 1} gjithsej,")
    print(f"  pra me se shumti {(g * p - 1) // (p - 1)} jave.")
    if best:
        header(f"ORARI ME I GJATE I GJETUR: {len(best)} jave")
        print_schedule(best, g, p)
