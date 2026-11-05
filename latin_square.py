import sys
import time
import itertools


def objective(grid, n):
    f = 0
    for r in range(n):
        vals = [v for v in grid[r] if v]
        f += len(vals) - len(set(vals))
    for c in range(n):
        vals = [grid[r][c] for r in range(n) if grid[r][c]]
        f += len(vals) - len(set(vals))
    return f


def print_grid(grid):
    for row in grid:
        print("     " + " ".join(f"{v:2d}" for v in row))


class LatinSearch:
    def __init__(self, n, reduced=False):
        self.n = n
        self.grid = [[0] * n for _ in range(n)]
        self.row_used = [0] * n
        self.col_used = [0] * n
        self.nodes = 0
        self.reduced = reduced
        if reduced:
            for i in range(n):
                self.place(0, i, i + 1)
                if i:
                    self.place(i, 0, i + 1)

    def place(self, r, c, v):
        self.grid[r][c] = v
        self.row_used[r] |= 1 << v
        self.col_used[c] |= 1 << v

    def remove(self, r, c, v):
        self.grid[r][c] = 0
        self.row_used[r] &= ~(1 << v)
        self.col_used[c] &= ~(1 << v)

    def fixed(self, r, c):
        return self.reduced and (r == 0 or c == 0)

    def backtracking(self, depth=0):
        n = self.n
        if depth == n * n:
            return True
        r, c = divmod(depth, n)
        if self.fixed(r, c):
            return self.backtracking(depth + 1)
        used = self.row_used[r] | self.col_used[c]
        for v in range(1, n + 1):
            if used >> v & 1:
                continue
            self.nodes += 1
            self.place(r, c, v)
            if self.backtracking(depth + 1):
                return True
            self.remove(r, c, v)
        return False

    def dls(self, depth, limit):
        n = self.n
        if depth == n * n:
            return objective(self.grid, n) == 0
        if depth == limit:
            return False
        r, c = divmod(depth, n)
        if self.fixed(r, c):
            return self.dls(depth + 1, limit)
        used = self.row_used[r] | self.col_used[c]
        for v in range(1, n + 1):
            if used >> v & 1:
                continue
            self.nodes += 1
            self.place(r, c, v)
            if self.dls(depth + 1, limit):
                return True
            self.remove(r, c, v)
        return False

    def iddfs(self, time_limit=120):
        self.iterations = []
        self.timed_out = False
        start = time.time()
        total = 0
        for limit in range(0, self.n * self.n + 1):
            self.nodes = 0
            found = self.dls(0, limit)
            self.iterations.append((limit, self.nodes))
            total += self.nodes
            if found:
                self.nodes = total
                return True
            if time.time() - start > time_limit:
                self.timed_out = True
                break
        self.nodes = total
        return False


def landscape(n):
    hist = {}
    cells = n * n
    for vals in itertools.product(range(1, n + 1), repeat=cells):
        grid = [list(vals[r * n:(r + 1) * n]) for r in range(n)]
        f = objective(grid, n)
        hist[f] = hist.get(f, 0) + 1
    total = n ** cells
    header(f"LANDSCAPE  n = {n}  ({n}^{cells} = {total} mbushje te plota)")
    print("    f   | gjendje  |   %")
    print("  ------+----------+--------")
    for f in sorted(hist):
        tag = "   <- katroret latine" if f == 0 else ""
        print(f"  {f:4d}  | {hist[f]:8d} | {100 * hist[f] / total:6.2f}{tag}")


def header(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "landscape":
        for n in (2, 3):
            landscape(n)
        sys.exit()

    n = int(args[0]) if args else 5
    reduced = "full" not in args

    header(f"LATIN SQUARE  n = {n}   (hapesira e kerkimit {n}^{n * n} ~ {float(n) ** (n * n):.2e})")

    print("\n  1) Backtracking (DFS)\n")
    s = LatinSearch(n)
    t = time.time()
    s.backtracking()
    print_grid(s.grid)
    print()
    print(f"  Kontrolli : f = {objective(s.grid, n)}" + ("  (katror latin valid)" if objective(s.grid, n) == 0 else "  (GABIM)"))
    print(f"  nyje      : {s.nodes}")
    print(f"  koha      : {time.time() - t:.3f} s")

    print("\n  2) IDDFS" + (" - rreshti dhe kolona e pare te fiksuara ne 1..n" if reduced else " - pa asnje fiksim") + "\n")
    s = LatinSearch(n, reduced=reduced)
    t = time.time()
    ok = s.iddfs()
    dt = time.time() - t
    if not ok:
        if s.timed_out:
            print(f"  Kohe e tejkaluar (120 s): {s.nodes} nyje, u perfunduan iteracionet deri te limit = {s.iterations[-1][0]} nga {n * n}")
        else:
            print("  nuk u gjet")
        sys.exit()
    print_grid(s.grid)
    print()
    print(f"  Kontrolli : f = {objective(s.grid, n)}" + ("  (katror latin valid)" if objective(s.grid, n) == 0 else "  (GABIM)"))
    print(f"  iteracione: {len(s.iterations)}  (limit = 0 .. {n * n})")
    print(f"  nyje      : {s.nodes} gjithsej")
    print(f"  koha      : {dt:.3f} s")
    print()
    print("  Nyje te vizituara ne cdo iteracion (limit -> nyje):")
    its = s.iterations
    for start in range(0, len(its), 7):
        chunk = its[start:start + 7]
        print("    " + "  ".join(f"{l:2d} -> {k:8d}" for l, k in chunk))
