from handy_dandy_library.file_processing import read_lines
from day21_1 import Garden, Vector


def shape_data(start_square: Vector, iter_count: int = 65, shape_name: str = '',
               verbose: bool = False) -> int:
    garden = Garden.from_lines(read_lines("day_21_1_input.txt"))
    reachable_plots = garden.reachable_plots(iter_count, start_square)
    if verbose:
        garden.update_to_circles(reachable_plots)
        garden.update_to_s([garden.start_square])
        print(garden)
        print(iter_count, start_square)
        print(f"{shape_name}: {len(reachable_plots)}")

    print(f"{shape_name}: {len(reachable_plots)}")
    return len(reachable_plots)


def quadratic(y, n):
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return a * n ** 2 + b * n + c


def main_quadratic():
    number_of_steps = 26501365
    garden = Garden.from_lines(read_lines("day_21_1_input.txt"))
    n = garden.n
    n_half = n // 2

    y = [garden.reachable_plot_count(n_half + i * n) for i in range(3)]
    print(y)
    t = quadratic(y, ((number_of_steps - n_half) // n))
    print(t)


def main():
    w, e = divmod(26501365, 131)
    e -= 65
    print(w, e)
    assert e % 2 == 0

    corner_pents = ["NW_pent", "NE_pent", "SE_pent", "SW_pent"]
    corner_tris = ["NW_tri", "NE_tri", "SE_tri", "SW_tri"]
    shape_names = (["top_triangle", "right_triangle", "bottom_triangle", "left_triangle",
                   "rectangle",
                    "top_pentagon", "right_pentagon", "bottom_pentagon", "left_pentagon"] +
                   corner_tris +
                   corner_pents)

    iterations = (e, e, e, e,
                  130,  # The rectangle is cheeky and shifts over 1 since it's an ODD input
                  130 + e, 130 + e, 130 + e, 130 + e,
                  65 + e, 65 + e, 65 + e, 65 + e,
                  130 + e, 130 + e, 130 + e, 130 + e)

    start_squares = (Vector((0, 65)), Vector((65, 130)), Vector((130, 65)), Vector((65, 0)),
                     Vector((65, 65)),
                     Vector((0, 65)), Vector((65, 130)), Vector((130, 65)), Vector((65, 0)),
                     Vector((0, 0)), Vector((0, 130)), Vector((130, 0)), Vector((130, 130)),
                     Vector((130, 130)), Vector((130, 0)), Vector((0, 0)), Vector((0, 130)))
    assert len(iterations) == len(shape_names) == len(start_squares) == 17
    shapes_data = {shape_name: shape_data(start_square, iteration, shape_name)
                   for shape_name, iteration, start_square in zip(shape_names, iterations, start_squares)}

    for corner_pent in corner_pents:
        shapes_data[corner_pent] *= w - 1

    for corner_tri in corner_tris:
        shapes_data[corner_tri] *= w

    shapes_data["rectangle"] *= (1 + 2 * w * (w - 1))
    t = sum(shapes_data.values())
    print(t)

    # 630414109286588 - too low (TEST METRIC, TO HAVE A MIN BOUND using divmod(k, 131))
    # 632257949158206 - answer via quadratic formula
    # 634097310737742 - too high (divmod(k, 131)) <- current (wrong) answer
    # 640150506668811 - too high (divmod(k, 130))

    # INCORRECT MATHS:
    # w = k // 130
    # Shape Name | Count
    # Rectangle  | 1 + 2 * w * (w - 1)
    # NW pent    | w - 1 (if w > 1)
    # NE pent    | w - 1 (if w > 1)
    # SW pent    | w - 1 (if w > 1)
    # SE pent    | w - 1 (if w > 1)
    # NW tri     | w
    # NE tri     | w
    # SW tri     | w
    # SE tri     | w
    # Bot tri    | 1
    # Top tri    | 1
    # Right tri  | 1
    # Left tri   | 1
    # Top pent   | 1
    # Bot pent   | 1
    # Right pent | 1
    # Left pent  | 1


if __name__ == "__main__":
    # main()
    main_quadratic()
