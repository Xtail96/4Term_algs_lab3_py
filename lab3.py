from collections import namedtuple
from math import inf

Seg = namedtuple("Seg", ('x', 'y'))
Sol = namedtuple("Sol", ('sum', 'path'))
inf_sol = Sol(inf, [])
zero_sol = Sol(0, [])

def seg_filter(segments, overlay):
    def cond(seg):
        return seg.x <= overlay.x <= seg.y
    return set(filter(cond, segments))


def solve(segments, overlay, current, best):
    if overlay.x > overlay.y:
        return current
    if current.sum >= best.sum:
        return inf_sol
    segs = seg_filter(segments, overlay)
    if segs:
        for s in segs:
            l = s.y - s.x + 1
            p = solve(segments,
                      Seg(s.y + 1, overlay.y),
                      Sol(current.sum + l, current.path + [s]),
                      best
                      )
            if p.sum < best.sum:
                best = p
        return best
    else:
        return inf_sol


def main():
    segments = {
        Seg(1, 4),
        Seg(4, 9),
        Seg(5, 12)
    }
    overlay = Seg(3, 11)
    # 1234
    #    456789
    #     56789...
    #   3456
    print(solve(segments, overlay, zero_sol, inf_sol))

if __name__ == '__main__':
    main()