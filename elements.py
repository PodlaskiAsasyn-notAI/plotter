import math
from bisect import bisect_left
import progressbar
from svgelements import SVG, Path, Shape


def _sample_subpath_equidistant(subpath, delta_s, lut_steps=500):
    """
    Równomiernie próbkuje obiekt Path/Subpath wzdłuż długości łuku (nie punktów kontrolnych).
    Wykorzystuje subpath.point(t) oraz stół wyszukiwań (LUT) z interpolacją.
    """
    # 1. Zbudowanie Look-Up Table (długość skumulowana -> parametr t)
    lut = [(0.0, 0.0)]
    total_len = 0.0
    prev_pt = subpath.point(0.0)

    for step in range(1, lut_steps + 1):
        t = step / lut_steps
        curr_pt = subpath.point(t)
        dist = math.hypot(curr_pt.x - prev_pt.x, curr_pt.y - prev_pt.y)
        total_len += dist
        lut.append((total_len, t))
        prev_pt = curr_pt

    if total_len == 0.0:
        return []

    # 2. Wyznaczenie liczby odcinków na podstawie pożądanego kroku delta_s
    num_segments = max(1, round(total_len / delta_s))
    lengths = [entry[0] for entry in lut]

    points = []
    for i in range(num_segments + 1):
        s = (i / num_segments) * total_len

        # Wyszukiwanie binarne i interpolacja parametru t
        idx = bisect_left(lengths, s)
        if idx <= 0:
            t = 0.0
        elif idx >= len(lut):
            t = 1.0
        else:
            s0, t0 = lut[idx - 1]
            s1, t1 = lut[idx]
            factor = (s - s0) / (s1 - s0) if s1 != s0 else 0.0
            t = t0 + factor * (t1 - t0)

        pt = subpath.point(t)
        points.append((float(pt.x), float(pt.y)))

    return points


def svg_to_equidistant_points(svg_file_path, density=5):
    """
    Parsuje plik SVG i generuje punkty o stałym kroku odległości.

    density: liczba punktów na 10 jednostek długości
    """
    delta_s = 10.0 / density
    svg = SVG.parse(svg_file_path)

    # 1. Zbieramy wszystkie podobiegi (subpaths) do przetworzenia
    subpaths_to_process = []
    for element in svg.elements():
        if not isinstance(element, Shape):
            continue

        # svgelements aplikuje transformacje przy tworzeniu Path(element)
        path = Path(element)
        for sp in path.as_subpaths():
            p = Path(sp)
            if len(p) > 0:
                subpaths_to_process.append(p)

    total_contours = len(subpaths_to_process)
    if total_contours == 0:
        print("Nie znaleziono żadnych ścieżek do przetworzenia.")
        return []

    all_contours = []
    total_points_generated = 0

    # 2. Konfiguracja paska postępu progressbar2
    # Pokazuje numer konturu, pasek procentowy, czas oraz sumaryczną liczbę wygenerowanych punktów
    widgets = [
        'Przetwarzanie konturów: ', progressbar.Counter(), f'/{total_contours} ',
        progressbar.Bar(marker='=', left='[', right=']'),
        ' ', progressbar.Percentage(),
        ' | Punkty: ', progressbar.Variable('points', format='{formatted_value}'),
        ' | ', progressbar.ETA()
    ]

    bar = progressbar.ProgressBar(max_value=total_contours, widgets=widgets)
    bar.start()

    for idx, subpath in enumerate(subpaths_to_process):
        # Generujemy punkty równomiernie leżące na krzywej
        points = _sample_subpath_equidistant(subpath, delta_s=delta_s)

        if points:
            all_contours.append(points)
            total_points_generated += len(points)

        # Aktualizujemy pasek postępu oraz zmienną z łączną liczbą punktów
        bar.update(idx + 1, points=total_points_generated)

    bar.finish()
    return all_contours


if __name__ == "__main__":
    kontury = svg_to_equidistant_points("example.svg", density=5)
    print(f"\nUkończono! Wygenerowano {sum(len(c) for c in kontury)} punktów w {len(kontury)} konturach.")