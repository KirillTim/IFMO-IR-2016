class SkipList(object):
    def __init__(self, arr, interval=1000):
        self.arr = arr
        self.interval = interval
        self.points = []
        for i, num in enumerate(self.arr):
            x = num / interval
            if len(self.points) == 0 or x > self.arr[self.points[-1]] / interval:
                self.points.append(i)
        self.arr_p = 0
        self.points_p = 0

    def reset_iter(self):
        self.arr_p = 0
        self.points_p = 0

    def find_next(self, x):
        if self.arr[self.arr_p] == x:
            return x
        while self.points_p + 1 < len(self.points) and self.arr[self.points[self.points_p + 1]] < x:
            self.points_p += 1
        self.arr_p = self.points[self.points_p]
        while self.arr_p < len(self.arr) and self.arr[self.arr_p] < x:
            self.arr_p += 1
        return self.arr[self.arr_p] if self.arr_p < len(self.arr) and self.arr[self.arr_p] >= x else None


if __name__ == '__main__':
    sl = SkipList([1, 2, 3, 10, 11, 12, 20, 25, 100, 1000], interval=10)
    assert sl.find_next(10) == 10
    assert sl.find_next(25) == 25
    assert sl.find_next(2000) is None
    sl.reset_iter()
    assert sl.find_next(2) == 2
    assert sl.find_next(3) == 3
    assert sl.find_next(5) == 10
    assert sl.find_next(6) == 10
    assert sl.find_next(10) == 10
    assert sl.find_next(12) == 12
    assert sl.find_next(17) == 20
    assert sl.find_next(42) == 100
    assert sl.find_next(120) == 1000
    assert sl.find_next(200) == 1000
