def range_sum_naive(data, left, right):
    result = 0
    for i in range(left, right + 1):
        result += data[i]
    return result


def build_prefix(data):
    prefix = [0] * (len(data) + 1)
    for i in range(len(data)):
        prefix[i + 1] = prefix[i] + data[i]
    return prefix


def range_sum_prefix(prefix, left, right):
    return prefix[right + 1] - prefix[left]


class FenwickTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (self.n + 1)
        for i in range(self.n):
            self.update(i, data[i])

    def update(self, index, delta):
        if index < 0 or index >= self.n:
            raise IndexError("Индекс вне массива")
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, index):
        if index < -1 or index >= self.n:
            raise IndexError("Индекс вне массива")
        i = index + 1
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & -i
        return result

    def range_sum(self, left, right):
        if left < 0 or right >= self.n or left > right:
            raise IndexError("Некорректный диапазон")
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        if self.n == 0:
            raise ValueError("Массив должен быть непустым")
        self.S = 1
        while self.S < self.n:
            self.S *= 2
        self.tree = [0] * (2 * self.S)
        self.minimum = [float("inf")] * (2 * self.S)
        self.maximum = [float("-inf")] * (2 * self.S)
        for i in range(self.n):
            position = self.S + i
            self.tree[position] = data[i]
            self.minimum[position] = data[i]
            self.maximum[position] = data[i]
        for i in range(self.S - 1, 0, -1):
            self.pull(i)

    def pull(self, i):
        self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
        self.minimum[i] = min(self.minimum[2 * i], self.minimum[2 * i + 1])
        self.maximum[i] = max(self.maximum[2 * i], self.maximum[2 * i + 1])

    def query(self, left, right):
        return self.query_stats(left, right)[0]

    def query_stats(self, left, right):
        if left < 0 or right >= self.n or left > right:
            raise IndexError("Некорректный диапазон")
        left += self.S
        right += self.S
        total = 0
        smallest = float("inf")
        largest = float("-inf")
        while left <= right:
            if left % 2 == 1:
                total += self.tree[left]
                smallest = min(smallest, self.minimum[left])
                largest = max(largest, self.maximum[left])
                left += 1
            if right % 2 == 0:
                total += self.tree[right]
                smallest = min(smallest, self.minimum[right])
                largest = max(largest, self.maximum[right])
                right -= 1
            left //= 2
            right //= 2
        return total, smallest, largest

    def update(self, index, value):
        if index < 0 or index >= self.n:
            raise IndexError("Индекс вне массива")
        i = self.S + index
        self.tree[i] = value
        self.minimum[i] = value
        self.maximum[i] = value
        i //= 2
        while i >= 1:
            self.pull(i)
            i //= 2
