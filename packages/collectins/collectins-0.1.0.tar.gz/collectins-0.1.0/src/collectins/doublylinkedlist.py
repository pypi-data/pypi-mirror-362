class DoublyListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, val):
        new_node = DoublyListNode(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def prepend(self, val):
        new_node = DoublyListNode(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert(self, index, val):
        if index < 0 or index > self._size:
            raise IndexError("Index out of bound")

        if index == 0:
            self.prepend(val)
            return
        if index == self._size:
            self.append(val)
            return

        new_node = DoublyListNode(val)
        current = self.head
        for _ in range(index):
            current = current.next

        prev_node = current.prev
        new_node.prev = prev_node
        new_node.next = current
        prev_node.next = new_node
        current.prev = new_node
        self._size += 1

    def pop(self, index=-1):
        if self._size == 0:
            raise IndexError("Pop from empty list")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise IndexError("Index out of bound")

        current = self.head
        for _ in range(index):
            current = current.next

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        self._size -= 1
        return current.val

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += self._size

            if index < 0 or index >= self._size:
                raise IndexError("Index out of bound")

            current = self.head
            for _ in range(index):
                current = current.next
            return current.val

        elif isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            result = []
            current = self.head
            count = 0
            while current:
                if start <= count < stop and (count - start) % step == 0:
                    result.append(current.val)
                current = current.next
                count += 1
            return result

        else:
            raise TypeError("Invalid argument type")

    def __contains__(self, value):
        current = self.head
        while current:
            if current.val == value:
                return True
            current = current.next
        return False

    def reverse(self):
        current = self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self.head, self.tail = self.tail, self.head

    def __iter__(self):
        current = self.head
        while current:
            yield current.val
            current = current.next

    def __reversed__(self):
        current = self.tail
        while current:
            yield current.val
            current = current.prev

    def __str__(self):
        return " <-> ".join(str(v) for v in self)