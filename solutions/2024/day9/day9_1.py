from handy_dandy_library.file_processing import read_lines


class FileCompactor:
    def __init__(self, line: str):
        self.n = len(line[0])
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
        m = len(self.contiguous_file)
        gaps = []
        file_blocks = [None for _ in range(self.n // 2 + 1)]

        i = 0
        file_block_index = 0
        while i < m:
            file_block_size = 0
            file_block_start = i
            while i < m and self.contiguous_file[i] != -1:
                if file_block_size > 0 and self.contiguous_file[i] != self.contiguous_file[i - 1]:
                    file_blocks[file_block_index] = (file_block_start, file_block_size)
                    file_block_index += 1
                    file_block_size = 0
                    file_block_start = i

                file_block_size += 1
                i += 1

            file_blocks[file_block_index] = (file_block_start, file_block_size)
            file_block_index += 1

            gap_size = 0
            gap_start = i
            while i < m and self.contiguous_file[i] == -1:
                gap_size += 1
                i += 1
            if gap_size > 0:
                gaps.append([gap_start, gap_size])

        return self.__contiguous_block_defragment_checksum(file_blocks, gaps)

    def __contiguous_block_defragment_checksum(self, file_blocks, gaps):
        return sum(self.__contiguous_block_weight(file_block_size, file_block_start, gaps) for file_block_start, file_block_size in reversed(file_blocks))

    def __contiguous_block_weight(self, file_block_size: int, file_block_start: int, gaps: list[list[int, int]]):
        file_id = self.contiguous_file[file_block_start]
        total = 0
        moved = False
        for gap_index, (gap_start, gap_size) in enumerate(gaps):
            if gap_start >= file_block_start:
                break

            if file_block_size <= gap_size:
                moved = True
                total += gap_start * file_block_size * file_id
                gaps[gap_index][0] = gap_start + file_block_size
                gaps[gap_index][1] = gap_size - file_block_size
                break
        if not moved:
            total += file_block_start * file_block_size * file_id
        return total + ((file_block_size * (file_block_size - 1)) // 2) * file_id


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
