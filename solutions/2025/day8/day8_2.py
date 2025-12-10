from day8_1 import ElectricJunctionBoxes


def main():
    test_junction_boxes = ElectricJunctionBoxes("puzzle8_1_test_input.txt")
    assert test_junction_boxes.final_circuit_connection_x_product() == 25272

    junction_boxes = ElectricJunctionBoxes("puzzle8_1.txt")
    t = junction_boxes.final_circuit_connection_x_product()
    print(t)


if __name__ == "__main__":
    main()
