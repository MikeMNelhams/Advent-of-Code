from day9_1 import MovieTheatre


def main():
    test_movie_theatre = MovieTheatre("puzzle9_1_test_input.txt")
    assert test_movie_theatre.largest_hull_inscribed_rectangle_area() == 24

    movie_theatre = MovieTheatre("puzzle9_1.txt")
    t = movie_theatre.largest_hull_inscribed_rectangle_area()
    assert t == 1461987144


if __name__ == "__main__":
    main()
