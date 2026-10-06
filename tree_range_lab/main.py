import random
import sys
import time

from bst import Node, insert, build_bst, search, preorder, inorder, postorder
from bst import delete, height, balance_factor, rotate_right, rotate_left, show_tree
from ranges import range_sum_naive, build_prefix, range_sum_prefix
from ranges import FenwickTree, SegmentTree


KEYS = [8, 4, 12, 2, 6, 10, 14]
EXAMPLE = [5, 2, 7, 3, 6, 1, 4, 8]
CHECK_RANGES = [(0, 0), (0, 7), (2, 6), (1, 5), (7, 7), (3, 4)]


def task1():
    root = Node(8)
    root.left = Node(4)
    root.right = Node(12)
    root.left.left = Node(2)
    root.left.right = Node(6)
    root.right.left = Node(10)
    root.right.right = Node(14)
    print("Корень:", root.key)
    print("Потомки корня:", root.left.key, root.right.key)
    print("Один из листьев:", root.left.left.key)
    show_tree(root)


def task2():
    root = None
    for key in KEYS:
        root = insert(root, key)
    print("Порядок вставки:", KEYS)
    show_tree(root)


def task3():
    root = build_bst(KEYS)
    for key in [4, 14, 5]:
        node, visited = search(root, key)
        print("Ключ:", key, "Найден:", node is not None, "Посещено:", visited)


def task4():
    root = build_bst(KEYS)
    print("Preorder:", preorder(root))
    print("Inorder:", inorder(root))
    print("Postorder:", postorder(root))


def task5():
    root = build_bst(KEYS)
    print("Исходное дерево:")
    show_tree(root)
    for key, case in [(2, "лист"), (4, "один потомок"), (8, "два потомка")]:
        print("Удаляю", key, "—", case)
        print("До:", inorder(root))
        root = delete(root, key)
        show_tree(root)
        print("После:", inorder(root))


def task6():
    for values in [KEYS, [2, 4, 6, 8, 10, 12, 14]]:
        root = build_bst(values)
        node, visited = search(root, values[-1])
        print("Вставка:", values)
        print("Высота:", height(root), "Поиск:", node.key, "Посещено:", visited)
        show_tree(root)


def task7():
    cases = [("LL", [30, 20, 10]), ("RR", [10, 20, 30]),
             ("LR", [30, 10, 20]), ("RL", [10, 30, 20])]
    for case, values in cases:
        root = build_bst(values)
        print(case, "Вставка:", values, "BF до:", balance_factor(root))
        show_tree(root)
        if case == "LL":
            root = rotate_right(root)
        elif case == "RR":
            root = rotate_left(root)
        elif case == "LR":
            root.left = rotate_left(root.left)
            root = rotate_right(root)
        else:
            root.right = rotate_right(root.right)
            root = rotate_left(root)
        print("После поворотов, BF:", balance_factor(root))
        show_tree(root)
        print("Inorder:", inorder(root))


def make_experiment():
    generator = random.Random(42)
    data = []
    for i in range(100_000):
        data.append(generator.randint(-100, 100))
    queries = []
    for i in range(1000):
        left = generator.randrange(len(data))
        right = generator.randrange(len(data))
        if left > right:
            left, right = right, left
        queries.append((left, right))
    return data, queries


def task8():
    data, queries = make_experiment()
    results = []
    started = time.perf_counter()
    for left, right in queries:
        results.append(range_sum_naive(data, left, right))
    elapsed = time.perf_counter() - started
    print("Элементов:", len(data), "Запросов:", len(queries), "Seed: 42")
    print("Время обычного цикла, с:", round(elapsed, 6))
    for i in range(3):
        left, right = queries[i]
        expected = sum(data[left:right + 1])
        print("Диапазон:", queries[i], "Сумма:", results[i], "sum():", expected)
    print("Контрольная сумма 1000 ответов:", sum(results))


def task9():
    data, queries = make_experiment()
    naive_results = []
    started = time.perf_counter()
    for left, right in queries:
        naive_results.append(range_sum_naive(data, left, right))
    naive_time = time.perf_counter() - started
    started = time.perf_counter()
    prefix = build_prefix(data)
    build_time = time.perf_counter() - started
    prefix_results = []
    started = time.perf_counter()
    for left, right in queries:
        prefix_results.append(range_sum_prefix(prefix, left, right))
    query_time = time.perf_counter() - started
    print("Данные и 1000 диапазонов совпадают с заданием 8: seed 42")
    print("Обычный цикл, с:", round(naive_time, 6))
    print("Построение prefix, с:", round(build_time, 6))
    print("1000 запросов prefix, с:", round(query_time, 6))
    print("Построение и запросы вместе, с:", round(build_time + query_time, 6))
    print("Все 1000 ответов совпали:", naive_results == prefix_results)
    small = EXAMPLE.copy()
    old_prefix = build_prefix(small)
    small[2] = 10
    print("После замены A[2] = 10, старый prefix:", range_sum_prefix(old_prefix, 2, 6))
    print("Правильная сумма:", sum(small[2:7]))
    print("Новые префиксы:", build_prefix(small))


def task10():
    data = EXAMPLE.copy()
    tree = FenwickTree(data)
    print("Массив:", data)
    print("tree[1..n]:", tree.tree[1:])
    print("Префикс индексов 0..6:", tree.prefix_sum(6))
    for left, right in CHECK_RANGES:
        print((left, right), "Фенвик:", tree.range_sum(left, right),
              "sum():", sum(data[left:right + 1]))
    delta = 10 - data[2]
    data[2] = 10
    tree.update(2, delta)
    print("Замена A[2]: 7 -> 10; delta =", delta)
    print("tree[1..n]:", tree.tree[1:])
    print("После обновления [2, 6]:", tree.range_sum(2, 6), "sum():", sum(data[2:7]))


def task11():
    data = EXAMPLE.copy()
    tree = SegmentTree(data)
    print("Массив:", data, "S:", tree.S)
    print("Суммы в вершинах tree[1..]:", tree.tree[1:])
    for left, right in CHECK_RANGES:
        print((left, right), "Дерево:", tree.query(left, right),
              "sum():", sum(data[left:right + 1]))
    data[2] = 6
    tree.update(2, 6)
    print("Замена A[2]: 7 -> 6")
    for left, right in CHECK_RANGES:
        print((left, right), "После:", tree.query(left, right),
              "sum():", sum(data[left:right + 1]))


def task12():
    data = EXAMPLE.copy()
    tree = SegmentTree(data)
    for left, right in CHECK_RANGES:
        part = data[left:right + 1]
        expected = (sum(part), min(part), max(part))
        print((left, right), "(Сумма, минимум, максимум):", tree.query_stats(left, right),
              "Обычные функции:", expected)
    data[5] = -5
    tree.update(5, -5)
    print("После A[5] = -5, весь массив:", tree.query_stats(0, 7))


def task13():
    root = build_bst(KEYS)
    print("Идентификаторы датчиков по порядку:", inorder(root))
    for sensor_id in [8, 999]:
        node, visited = search(root, sensor_id)
        print("Датчик:", sensor_id, "Найден:", node is not None, "Посещено:", visited)
    selected_id = 8
    node, visited = search(root, selected_id)
    if node is None:
        print("Выбранный датчик не найден")
        return
    data = []
    for i in range(1000):
        data.append(i % 100)
    fenwick = FenwickTree(data)
    segment = SegmentTree(data)
    queries = [(0, 9), (120, 130), (125, 125), (0, 999), (700, 709)]
    print("Выбран датчик:", selected_id, "Количество измерений:", len(data))
    for stage in ["До изменения", "После изменения"]:
        if stage == "После изменения":
            index = 125
            value = 200
            delta = value - data[index]
            data[index] = value
            fenwick.update(index, delta)
            segment.update(index, value)
            print("Измерение 125: 25 -> 200; delta =", delta)
        print(stage)
        for left, right in queries:
            naive = range_sum_naive(data, left, right)
            fast = fenwick.range_sum(left, right)
            total, smallest, largest = segment.query_stats(left, right)
            print((left, right), "Цикл:", naive, "Фенвик:", fast,
                  "Дерево:", total, "Минимум:", smallest, "Максимум:", largest,
                  "Суммы совпали:", naive == fast == total)


if __name__ == "__main__":
    tasks = [task1, task2, task3, task4, task5, task6, task7,
             task8, task9, task10, task11, task12, task13]
    if len(sys.argv) > 2:
        raise SystemExit("Запуск: python main.py [номер задания 1..13]")
    if len(sys.argv) == 2:
        if not sys.argv[1].isdigit() or not 1 <= int(sys.argv[1]) <= 13:
            raise SystemExit("Укажите номер задания от 1 до 13")
        numbers = [int(sys.argv[1])]
    else:
        numbers = range(1, 14)
    for number in numbers:
        print("\n=== Задание", number, "===")
        tasks[number - 1]()
