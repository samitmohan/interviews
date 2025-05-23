"""
Implementation of an auto-balanced binary tree (AVL Tree)!
Includes detailed rotation diagrams and full insertion/deletion logic.
"""

import math
import random
from typing import Any


class MyQueue:
    """
    A basic FIFO queue used for level-order traversal of the tree.
    """

    def __init__(self) -> None:
        self.data: list[Any] = []
        self.head: int = 0
        self.tail: int = 0

    def is_empty(self) -> bool:
        return self.head == self.tail

    def push(self, data: Any) -> None:
        self.data.append(data)
        self.tail += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty")
        ret = self.data[self.head]
        self.head += 1
        return ret

    def count(self) -> int:
        return self.tail - self.head

    def print_queue(self) -> None:
        print(self.data)
        print("**************")
        print(self.data[self.head : self.tail])


class MyNode:
    """
    A class representing a node in the AVL tree.
    """

    def __init__(self, data: Any) -> None:
        self.data = data
        self.left: MyNode | None = None
        self.right: MyNode | None = None
        self.height: int = 1

    def get_data(self) -> Any:
        return self.data

    def get_left(self) -> MyNode | None:
        return self.left

    def get_right(self) -> MyNode | None:
        return self.right

    def get_height(self) -> int:
        return self.height

    def set_data(self, data: Any) -> None:
        self.data = data

    def set_left(self, node: MyNode | None) -> None:
        self.left = node

    def set_right(self, node: MyNode | None) -> None:
        self.right = node

    def set_height(self, height: int) -> None:
        self.height = height


def get_height(node: MyNode | None) -> int:
    return 0 if node is None else node.get_height()


def right_rotation(node: MyNode) -> MyNode:
    r"""
            A                      B
           / \                    / \
          B   C                  Bl  A
         / \       -->          /   / \
        Bl  Br                 UB Br  C
       /
     UB
    UB = unbalanced node
    """
    print("right rotation node:", node.get_data())
    ret = node.get_left()
    assert ret is not None
    node.set_left(ret.get_right())
    ret.set_right(node)
    node.set_height(max(get_height(node.get_left()), get_height(node.get_right())) + 1)
    ret.set_height(max(get_height(ret.get_left()), get_height(ret.get_right())) + 1)
    return ret


def left_rotation(node: MyNode) -> MyNode:
    """
    a mirror symmetry rotation of the right_rotation
    """
    print("left rotation node:", node.get_data())
    ret = node.get_right()
    assert ret is not None
    node.set_right(ret.get_left())
    ret.set_left(node)
    node.set_height(max(get_height(node.get_left()), get_height(node.get_right())) + 1)
    ret.set_height(max(get_height(ret.get_left()), get_height(ret.get_right())) + 1)
    return ret


def lr_rotation(node: MyNode) -> MyNode:
    r"""
            A              A                    Br
           / \            / \                  /  \
          B   C    LR    Br  C       RR       B    A
         / \       -->  /  \         -->    /     / \
        Bl  Br         B   UB              Bl    UB  C
             \        /
             UB     Bl
    RR = right_rotation   LR = left_rotation
    """
    left_child = node.get_left()
    assert left_child is not None
    node.set_left(left_rotation(left_child))
    return right_rotation(node)


def rl_rotation(node: MyNode) -> MyNode:
    right_child = node.get_right()
    assert right_child is not None
    node.set_right(right_rotation(right_child))
    return left_rotation(node)


def insert_node(node: MyNode | None, data: Any) -> MyNode:
    if node is None:
        return MyNode(data)

    if data < node.get_data():
        node.set_left(insert_node(node.get_left(), data))
        if get_height(node.get_left()) - get_height(node.get_right()) == 2:
            left_child = node.get_left()
            assert left_child is not None
            if data < left_child.get_data():
                node = right_rotation(node)
            else:
                node = lr_rotation(node)
    else:
        node.set_right(insert_node(node.get_right(), data))
        if get_height(node.get_right()) - get_height(node.get_left()) == 2:
            right_child = node.get_right()
            assert right_child is not None
            if data < right_child.get_data():
                node = rl_rotation(node)
            else:
                node = left_rotation(node)

    node.set_height(max(get_height(node.get_left()), get_height(node.get_right())) + 1)
    return node


def get_left_most(root: MyNode) -> Any:
    while root.get_left():
        root = root.get_left()
    return root.get_data()


def del_node(root: MyNode, data: Any) -> MyNode | None:
    if data < root.get_data():
        if root.get_left():
            root.set_left(del_node(root.get_left(), data))
    elif data > root.get_data():
        if root.get_right():
            root.set_right(del_node(root.get_right(), data))
    else:
        if root.get_left() and root.get_right():
            temp_data = get_left_most(root.get_right())
            root.set_data(temp_data)
            root.set_right(del_node(root.get_right(), temp_data))
        elif root.get_left():
            return root.get_left()
        elif root.get_right():
            return root.get_right()
        else:
            return None

    left_child = root.get_left()
    right_child = root.get_right()

    if get_height(right_child) - get_height(left_child) == 2:
        assert right_child is not None
        if get_height(right_child.get_right()) >= get_height(right_child.get_left()):
            root = left_rotation(root)
        else:
            root = rl_rotation(root)
    elif get_height(right_child) - get_height(left_child) == -2:
        assert left_child is not None
        if get_height(left_child.get_left()) >= get_height(left_child.get_right()):
            root = right_rotation(root)
        else:
            root = lr_rotation(root)

    root.set_height(max(get_height(left_child), get_height(right_child)) + 1)
    return root


class AVLtree:
    """
    Wrapper class for AVL tree supporting insert, delete, and string display.
    """

    def __init__(self) -> None:
        self.root: MyNode | None = None

    def get_height(self) -> int:
        return get_height(self.root)

    def insert(self, data: Any) -> None:
        print("insert:" + str(data))
        self.root = insert_node(self.root, data)

    def del_node(self, data: Any) -> None:
        print("delete:" + str(data))
        if self.root is None:
            print("Tree is empty!")
            return
        self.root = del_node(self.root, data)

    def __str__(self) -> str:
        output = ""
        q = MyQueue()
        q.push(self.root)
        layer = self.get_height()
        if layer == 0:
            return output
        cnt = 0
        while not q.is_empty():
            node = q.pop()
            space = " " * int(math.pow(2, layer - 1))
            output += space
            if node is None:
                output += "*"
                q.push(None)
                q.push(None)
            else:
                output += str(node.get_data())
                q.push(node.get_left())
                q.push(node.get_right())
            output += space
            cnt += 1
            for i in range(100):
                if cnt == math.pow(2, i) - 1:
                    layer -= 1
                    if layer == 0:
                        output += "\n*************************************"
                        return output
                    output += "\n"
                    break
        output += "\n*************************************"
        return output


if __name__ == "__main__":
    t = AVLtree()
    lst = list(range(10))
    random.shuffle(lst)
    for i in lst:
        t.insert(i)
        print(str(t))
    random.shuffle(lst)
    for i in lst:
        t.del_node(i)
        print(str(t))
