from collectins.linkedlist import LinkedList, ListNode
import pytest

def test_append_single_element():
    l1 = LinkedList()
    l1.append(1)
    l1.append(2)

    assert l1.head.val == 1
    assert l1.head.next.val == 2
    assert l1.head.next.next is None

def test_append_multiple_elememt():
    l1 = LinkedList()
    l1.append(10)
    l1.append(20)
    l1.append(30)

    assert l1.head.val == 10
    assert l1.head.next.val == 20
    assert l1.head.next.next.val == 30


def test_length_linkedlist():
    l1 = LinkedList()
    l1.append(10)
    assert len(l1) == 1

    l1.append(20)
    assert len(l1) == 2

    l1.append(30)
    assert len(l1) == 3

def test_get_item():
    l1 = LinkedList()
    l1.append(10)

    assert l1[0] == 10

    with pytest.raises(IndexError):
        _ = l1[10]

def test_iter_by_values():
    l1 = LinkedList()
    l1.append(10)
    l1.append(20)
    l1.append(30)
    l1.append(40)
    l1.append(50)

    check = 10
    for val in l1.values():
        assert val == check
        check += 10

def test_iter_by_nodes():
    l1 = LinkedList()
    l1.append(10)
    l1.append(20)
    l1.append(30)

    vals = []

    for node in l1.nodes():
        assert isinstance(node, ListNode)
        vals.append(node.val)

    assert vals == [10, 20, 30]


def test_iter_with_index():
    l1 = LinkedList()
    l1.append(100)
    l1.append(200)
    l1.append(300)

    for index, value in l1:
        assert l1[index] == value
    
def test_index():
    l1 = LinkedList()
    l1.append(10)
    l1.append(30)
    l1.insert(1, 20)

    assert list(l1.values()) == [10, 20, 30]

def test_pop():
    l1 = LinkedList()
    l1.append(10)
    l1.append(20)
    l1.append(30)

    assert l1.pop(1) == 20
    assert list(l1.values()) == [10, 30]

    assert l1.pop() == 30
    assert l1.pop(0) == 10

    with pytest.raises(IndexError):
        l1.pop()  # popping from empty list

def test_contains():
    l1 = LinkedList()
    l1.append(10)
    
    assert 10 in l1
    assert 20 not in l1

def test_reverse_ll():
    l1 = LinkedList()
    l1.append(10)
    l1.append(20)
    l1.append(30)

    l1.reverse()

    assert list(l1.values()) == [30, 20, 10]

def test_clear_ll():
    l1 = LinkedList()
    l1.append(1)

    l1.clear()
    
    assert len(l1) == 0

def test_slice_getitem():
    l1 = LinkedList()
    for v in [10, 20, 30, 40, 50]:
        l1.append(v)

    assert l1[1:4] == [20, 30, 40]
    assert l1[:3] == [10, 20, 30]
    assert l1[::2] == [10, 30, 50]
    assert l1[1:5:2] == [20, 40]
