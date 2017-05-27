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
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType('r'), help="считать входные данные из файла F в формате \"{транзисторы} {этажи}\"")
    parser.add_argument("-c", help="считать входные данные из консоли", action='store_true')
    parser.add_argument("-v", help="выводить ход решения", action='store_true')
    args = parser.parse_args()
    #if bool(args.f) + bool(args.c) / 2 != 1:
    #    parser.print_help()
    #    parser.exit(1)
    if args.f:
        try:
            t, s = map(int, args.f.read().split()[:2])
        except ValueError:
            parser.exit(1, "Не удалось прочитать входные данные")
    elif args.c:
        try:
            print("Отрезок: ", end='')
            beginOrigin, endOrigin = input().split(" ")
            beginOrigin = int(beginOrigin)
            endOrigin = int(endOrigin)
            if beginOrigin > endOrigin:
                    parser.exit(1, "Левая граница отрезка должна быть меньше правой")
            overlay = Seg(beginOrigin, endOrigin)
            print("Число участков разбиения: ", end='')
            t = int(input())
            if t < 0:
                parser.exit(1, "Число отрезков разбиения должно быть неотрицательным")

            print("Введите участки разбиения в формате [начало, конец]")
            segments = set()
            while t > 0:
                first, second = input().split(" ")
                first = int(first)
                second = int(second)
                if first > second:
                    parser.exit(1, "Левая граница отрезка должна быть меньше правой")
                segments.add(Seg(first, second))
                t -= 1
        except ValueError:
            parser.exit(1, "Не удалось прочитать входные данные")
    global verbose
    verbose = args.v
    print("Поиск решения:")

    #segments = {
    #    Seg(1, 4),
    #    Seg(4, 9),
    #    Seg(5, 12)
    #}
    #overlay = Seg(3, 11)
    # 1234
    #    456789
    #     56789...
    #   3456
    print(solve(segments, overlay, zero_sol, inf_sol))

if __name__ == '__main__':
    main()