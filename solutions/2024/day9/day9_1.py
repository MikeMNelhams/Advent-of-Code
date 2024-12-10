from handy_dandy_library.file_processing import read_lines


from collections import deque


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
        gaps, file_blocks = self.__gaps_and_file_blocks()

        total = 0
        gap_index = 0
        m = len(gaps)
        while gap_index < m:
            gap_start, gap_size = gaps[gap_index]

            while gap_size > 0:
                rightmost_index = -1
                rightmost_size = -1
                rightmost_file_id = -1

                for file_block_size, file_block_list in enumerate(file_blocks[:gap_size + 1]):
                    if not file_block_list:
                        continue

                    file_block_start, file_id = file_block_list[-1]

                    if file_block_start <= gap_start or file_block_start <= rightmost_index:
                        continue

                    rightmost_index = file_block_start
                    rightmost_size = file_block_size
                    rightmost_file_id = file_id

                if rightmost_size == -1:
                    break

                total += (gap_start * rightmost_size + ((rightmost_size * (rightmost_size - 1)) // 2)) * rightmost_file_id
                gap_start += rightmost_size
                gap_size -= rightmost_size
                file_blocks[rightmost_size].pop()

            gap_index += 1

        for file_block_size, file_block_list in enumerate(file_blocks):
            if not file_block_list:
                continue

            total += sum((file_block_start * file_block_size + ((file_block_size * (file_block_size - 1)) // 2)) * file_id
                         for file_block_start, file_id in file_block_list)

        return total

    def __gaps_and_file_blocks(self) -> (list[tuple[int, int]], list[list[int, int]]):
        m = len(self.contiguous_file)
        gaps = []
        file_blocks = [[] for _ in range(10)]
        i = 0
        file_id = 0
        while i < m:
            file_block_size = 0
            file_block_start = i
            while i < m and self.contiguous_file[i] != -1:
                if file_block_size > 0 and self.contiguous_file[i] != self.contiguous_file[i - 1]:
                    file_blocks[file_block_size].append((file_block_start, file_id))
                    file_id += 1
                    file_block_size = 0
                    file_block_start = i

                file_block_size += 1
                i += 1

            file_blocks[file_block_size].append((file_block_start, file_id))
            file_id += 1

            gap_size = 0
            gap_start = i
            while i < m and self.contiguous_file[i] == -1:
                gap_size += 1
                i += 1
            if gap_size > 0:
                gaps.append((gap_start, gap_size))
        return gaps, file_blocks


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
