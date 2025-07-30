class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self._size = 0

    def append(self, val) -> None:
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
        self._size += 1

    def prepend(self, val) -> None:
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert(self, index, val) -> None:
        if index < 0 or index > self._size:
            raise IndexError("Index out of bound")
        if index == 0:
            self.prepend(val)
            return
        new_node = ListNode(val)
        temp = self.head
        for _ in range(index - 1):
            temp = temp.next
        new_node.next = temp.next
        temp.next = new_node
        self._size += 1

    def pop(self, index=-1):
        if self._size == 0:
            raise IndexError("Pop from empty list")
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bound")

        temp = self.head
        if index == 0:
            val = temp.val
            self.head = temp.next
        else:
            for _ in range(index - 1):
                temp = temp.next
            val = temp.next.val
            temp.next = temp.next.next
        self._size -= 1
        return val

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += self._size
            if index < 0 or index >= self._size:
                raise IndexError("Index out of bound")
            temp = self.head
            for _ in range(index):
                temp = temp.next
            return temp.val
        elif isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            result = []
            temp = self.head
            count = 0
            while temp:
                if start <= count < stop and (count - start) % step == 0:
                    result.append(temp.val)
                temp = temp.next
                count += 1
            return result
        else:
            raise TypeError("Invalid argument type")

    def __contains__(self, value):
        temp = self.head
        while temp:
            if temp.val == value:
                return True
            temp = temp.next
        return False

    def __iter__(self):
        temp = self.head
        index = 0
        while temp:
            yield index, temp.val
            temp = temp.next
            index += 1

    def values(self):
        temp = self.head
        while temp:
            yield temp.val
            temp = temp.next

    def nodes(self):
        temp = self.head
        while temp:
            yield temp
            temp = temp.next

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev

    def clear(self):
        self.head = None
        self._size = 0

    def __str__(self):
        return " -> ".join(str(v) for v in self.values())
