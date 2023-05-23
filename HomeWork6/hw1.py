"""
Given a dictionary (tree), that can contains multiple nested structures.
Write a function, that takes element and finds the number of occurrences
of this element in the tree.

Tree can only contains basic structures like:
    str, list, tuple, dict, set, int, bool
"""
from typing import Any


# Example tree:
example_tree = {
    "first": ["RED", "BLUE"],
    "second": {
        "simple_key": ["simple", "list", "of", "RED", "valued"],
    },
    "third": {
        "abc": "BLUE",
        "jhl": "RED",
        "complex_key": {
            "key1": "value1",
            "key2": "RED",
            "key3": ["a", "lot", "of", "values", {"nested_key": "RED"}],
        }
     },
    "fourth": "RED",
}


def count_occurrences(tree: dict, element: Any) -> int:
    count = 0

    def traverse(node):
        nonlocal count
        if isinstance(node, dict):
            for value in node.values():
                traverse(value)
        elif isinstance(node, (list, tuple, set)):
            for item in node:
                traverse(item)
        elif node == element:
            count += 1

    traverse(tree)
    return count


if __name__ == '__main__':
    print(count_occurrences(example_tree, "RED"))  # 6

