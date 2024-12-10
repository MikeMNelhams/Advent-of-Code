from handy_dandy_library.file_processing import read_lines


class FileCompactor:
    def __init__(self, line: str):
        self.n = len(line[0])
        print(line)
        self.contiguous_file = self.__contiguous_file(line[0])

    def __contiguous_file(self, line: str) -> list[int]:
        if self.n <= 0:
            raise ValueError
        if self.n <= 2:
            return [int(line[0])]

        compacted_files = []
        id_current = 0
        for i in range(self.n):
            x = int(line[i])
            if not i & 1:
                for _ in range(x):
                    compacted_files.append(id_current)
                id_current += 1
            else:
                for _ in range(x):
                    compacted_files.append(-1)

        return compacted_files

    def compacted_file_checksum(self) -> int:
        contiguous_file = [x for x in self.contiguous_file]
        m = len(contiguous_file)
        remaining_count = sum(1 if x != -1 else 0 for x in contiguous_file)

        left = 0
        right = m - 1
        while remaining_count > 0:
            while left < right and contiguous_file[left] != -1:
                left += 1
            while left < right and contiguous_file[right] == -1:
                right -= 1
            contiguous_file[left] = contiguous_file[right]
            contiguous_file[right] = -1
            remaining_count -= 1

        compacted_files = [x for x in contiguous_file if x != -1]
        return sum(i * x for i, x in enumerate(compacted_files))

    def compacted_file_checksum2(self) -> int:
        contiguous_file = [x for x in self.contiguous_file]
        m = len(contiguous_file)
        gaps = []
        file_blocks = []

        i = 0
        while i < m:
            file_block_size = 0
            file_block_start = i
            while i < m and contiguous_file[i] != -1:
                if file_block_size > 0 and contiguous_file[i] != contiguous_file[i - 1]:
                    file_blocks.append((file_block_start, file_block_size))
                    file_block_size = 0
                    file_block_start = i

                file_block_size += 1
                i += 1

            file_blocks.append((file_block_start, file_block_size))

            gap_size = 0
            gap_start = i
            while i < m and contiguous_file[i] == -1:
                gap_size += 1
                i += 1
            if gap_size > 0:
                gaps.append((gap_start, gap_size))

        file_blocks.reverse()

        for file_block_start, file_block_size in file_blocks:
            file_id = contiguous_file[file_block_start]

            for gap_index, (gap_start, gap_size) in enumerate(gaps):
                if gap_start >= file_block_start:
                    break

                if file_block_size <= gap_size:
                    for i in range(file_block_size):
                        contiguous_file[gap_start + i] = file_id
                        contiguous_file[file_block_start + i] = -1
                    gaps[gap_index] = (gap_start + file_block_size, gap_size - file_block_size)
                    break

        return sum(i * x for i, x in enumerate(contiguous_file) if x != -1)


def tests():
    file_compactor = FileCompactor(read_lines("puzzle9_1_test_input1.txt"))

    t1 = file_compactor.compacted_file_checksum()
    assert t1 == 1928


def main():
    tests()

    file_compactor = FileCompactor(read_lines("puzzle9_1.txt"))
    t2 = file_compactor.compacted_file_checksum()
    assert t2 == 6334655979668


if __name__ == "__main__":
    main()
