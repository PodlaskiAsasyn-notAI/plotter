import matplotlib.pyplot as plt

def visualize_contours(all_contours):
    """
    Wizualizuje listę ścieżek z punktami, numeruje kolejność konturów
    i dodaje strzałki kierunkowe.
    """
    if not all_contours:
        print("Brak konturów do wyświetlenia!")
        return

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab10.colors  # Paleta różnych kolorów dla kolejnych ścieżek

    for idx, contour in enumerate(all_contours):
        if not contour:
            continue

        xs = [pt[0] for pt in contour]
        ys = [pt[1] for pt in contour]
        color = colors[idx % len(colors)]

        # 1. Rysowanie linii ścieżki i samych punktów
        ax.plot(xs, ys, color=color, linewidth=1.5, alpha=0.7)
        ax.scatter(xs, ys, color=color, s=15, zorder=3)

        # 2. Oznaczenie początku ścieżki z numerem kolejności (przydatne dla slicera/CNC)
        start_x, start_y = xs[0], ys[0]
        ax.scatter(start_x, start_y, color='red', s=45, zorder=4)
        ax.text(start_x, start_y, f" #{idx + 1}", fontsize=10, fontweight='bold', color='black', zorder=5)

        # 3. Strzałka wskazująca kierunek rysowania (na pierwszym segmencie)
        if len(contour) >= 2:
            dx = xs[1] - xs[0]
            dy = ys[1] - ys[0]
            ax.annotate(
                '',
                xy=(xs[0] + dx, ys[0] + dy),
                xytext=(xs[0], ys[0]),
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5),
                zorder=4
            )

    # Układ współrzędnych SVG ma (0,0) w lewym górnym rogu
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Wizualizacja konturów SVG (kolejność, punkty i zwrot)", fontsize=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.show()


# --- PRZYKŁAD UŻYCIA Z TWOIM PARSEREM ---
if __name__ == "__main__":
    from elements import svg_to_equidistant_points

    kontury = svg_to_equidistant_points("example.svg", density=0.5)
    visualize_contours(kontury)
    pass
