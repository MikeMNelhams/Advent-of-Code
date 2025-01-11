from handy_dandy_library.file_processing import read_lines

from day23_1 import LanParty


def tests():
    lan_party = LanParty(read_lines("puzzle23_1_test_input1.txt"))

    assert lan_party.lan_password == "co,de,ka,ta"


def main():
    tests()

    lan_party = LanParty(read_lines("puzzle23_1.txt"))

    assert lan_party.lan_password == "df,kg,la,mp,pb,qh,sk,th,vn,ww,xp,yp,zk"


if __name__ == "__main__":
    main()
