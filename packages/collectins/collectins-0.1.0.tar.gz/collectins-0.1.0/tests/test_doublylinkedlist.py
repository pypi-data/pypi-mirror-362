import pytest
from collectins.doublylinkedlist import DoublyLinkedList


def test_append():
    dll = DoublyLinkedList()
    dll.append(10)
    dll.append(20)
    assert list(dll) == [10, 20]
    assert len(dll) == 2

def test_prepend():
    dll = DoublyLinkedList()
    dll.prepend(10)
    dll.prepend(5)
    assert list(dll) == [5, 10]
    assert len(dll) == 2

def test_insert():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(3)
    dll.insert(1, 2)
    assert list(dll) == [1, 2, 3]
    assert len(dll) == 3

def test_pop():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    assert dll.pop(1) == 2
    assert list(dll) == [1, 3]
    assert dll.pop() == 3
    assert list(dll) == [1]
    assert dll.pop(0) == 1
    assert len(dll) == 0

def test_len():
    dll = DoublyLinkedList()
    assert len(dll) == 0
    dll.append(100)
    assert len(dll) == 1

def test_getitem_index():
    dll = DoublyLinkedList()
    for i in [10, 20, 30]:
        dll.append(i)
    assert dll[0] == 10
    assert dll[2] == 30
    assert dll[-1] == 30
    with pytest.raises(IndexError):
        _ = dll[5]

def test_getitem_slice():
    dll = DoublyLinkedList()
    for i in range(1, 6):
        dll.append(i)
    assert dll[1:4] == [2, 3, 4]
    assert dll[:3] == [1, 2, 3]
    assert dll[::2] == [1, 3, 5]

def test_contains():
    dll = DoublyLinkedList()
    dll.append(10)
    dll.append(20)
    assert 10 in dll
    assert 30 not in dll

def test_reverse():
    dll = DoublyLinkedList()
    for i in [1, 2, 3]:
        dll.append(i)
    dll.reverse()
    assert list(dll) == [3, 2, 1]

def test_reversed_builtin():
    dll = DoublyLinkedList()
    for i in [1, 2, 3]:
        dll.append(i)
    assert list(reversed(dll)) == [3, 2, 1]

def test_str_output():
    dll = DoublyLinkedList()
    for i in [10, 20, 30]:
        dll.append(i)
    assert str(dll) == "10 <-> 20 <-> 30"
