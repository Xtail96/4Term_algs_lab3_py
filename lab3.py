from collections import namedtuple
from math import inf

Seg = namedtuple("Seg", ('x', 'y'))
Sol = namedtuple("Sol", ('sum', 'path'))
inf_sol = Sol(inf, set())
zero_sol = Sol(0, set())

level = 0

def seg_filter(segments, overlay):
    def cond(seg):
        return seg.x <= overlay.x <= seg.y
    if verbose :
    	print(" " * level, "Набор отрезков, покрывающих исходный:", set(filter(cond, segments)))
    	#print()
    return set(filter(cond, segments))


def solve(segments, overlay, current, best):
	global level
	level += 2
	if overlay.x > overlay.y:
		if verbose:
			print(" " * level, "Дошли до листа; Текущая комбнация = ", current)
		level -= 2
		return current
	if current.sum >= best.sum:
		if verbose:
			print(" " * level, "Сумма отрезков больше лучшей из найденных", current)
		level -= 2
		return inf_sol
	segs = seg_filter(segments, overlay)
	if segs:
		for s in segs:
			if verbose:
				print(" " * level, "Просматриваемый отрезок: ", s)
			l = s.y - s.x + 1
			p = solve(segments, Seg(s.y + 1, overlay.y), Sol(current.sum + l, current.path | {s}), best)
			if p.sum < best.sum:
				best = p
				if verbose:
					print(" " * level, "Найдено более хорошее решение: ", best)
			elif verbose:
				print(" " * level, "Решение осталось прежним: ", best)
		level -= 2	
		return best
	elif verbose:
		print(" " * level, "Не смогли покрыть отрезок: ", inf_sol)
		return inf_sol
	else:
		return inf_sol


def main():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType('r'), help="считать входные данные из файла F")
    parser.add_argument("-c", help="считать входные данные из консоли", action='store_true')
    parser.add_argument("-v", help="выводить ход решения", action='store_true')
    args = parser.parse_args()
    if bool(args.f) + bool(args.c) / 2 == 0:
        parser.print_help()
        parser.exit(1)
    if args.f:
        try:
            #t, s = map(int, args.f.read().split()[:2])
            beginOrigin, endOrigin = args.f.readline().split(" ")
            beginOrigin = int(beginOrigin)
            endOrigin = int(endOrigin)
            if beginOrigin > endOrigin:
                    parser.exit(1, "Левая граница отрезка должна быть меньше либо равна правой")
            overlay = Seg(beginOrigin, endOrigin)
            print("Исходный отрезок: [" + str(beginOrigin) + "; " + str(endOrigin) + "]")

            count = args.f.readline()
            count = int(count)
            if count < 0:
                parser.exit(1, "Число отрезков разбиения должно быть неотрицательным")
            print(count)
            
            segments = set()
            for i in range(count):
                first, second = args.f.readline().split(" ")
                first = int(first)
                second = int(second)
                if first > second:
                    parser.exit(1, "Левая граница отрезка должна быть меньше либо равна правой")
                segments.add(Seg(first, second))
            print(segments)

        except ValueError:
            parser.exit(1, "Не удалось прочитать входные данные")
    elif args.c:
        try:
            print("Отрезок: ", end='')
            beginOrigin, endOrigin = input().split(" ")
            beginOrigin = int(beginOrigin)
            endOrigin = int(endOrigin)
            if beginOrigin > endOrigin:
                parser.exit(1, "Левая граница отрезка должна быть меньше либо равна правой")
            overlay = Seg(beginOrigin, endOrigin)
            print("Число участков разбиения: ", end='')
            t = int(input())
            if t < 0:
                parser.exit(1, "Число отрезков разбиения должно быть неотрицательным")

            print("Введите участки разбиения в формате [начало, конец]")
            segments = set()
            for i in range(t):
                first, second = input().split(" ")
                first = int(first)
                second = int(second)
                if first > second:
                    parser.exit(1, "Левая граница отрезка должна быть меньше либо равна правой")
                segments.add(Seg(first, second))
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