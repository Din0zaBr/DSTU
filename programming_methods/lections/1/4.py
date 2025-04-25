class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head is None

    def InsertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def InsertAtHead(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def Delete(self, key):
        current = self.head
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if current is None:
            return  # Key not found
        if prev is None:
            self.head = current.next  # Key is in the head
        else:
            prev.next = current.next  # Bypass the current node

    def DeleteAtHead(self):
        if self.head is None:
            return
        self.head = self.head.next

    def Search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return current
            current = current.next
        return None

    def Reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def hasCycle(self):
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def getNthFromEnd(self, n):
        main_ptr = ref_ptr = self.head
        count = 0
        while count < n:
            if ref_ptr is None:
                return None  # n is greater than the number of nodes
            ref_ptr = ref_ptr.next
            count += 1
        while ref_ptr:
            main_ptr = main_ptr.next
            ref_ptr = ref_ptr.next
        return main_ptr.data if main_ptr else None

    def removeDuplicates(self):
        current = self.head
        prev = None
        seen = set()
        while current:
            if current.data in seen:
                prev.next = current.next  # Bypass the current node
            else:
                seen.add(current.data)
                prev = current
            current = current.next

    def printList(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("NULL")


# Пример использования
if __name__ == "__main__":
    ll = LinkedList()
    ll.InsertAtEnd(1)
    ll.InsertAtEnd(2)
    ll.InsertAtEnd(3)
    ll.InsertAtEnd(4)
    ll.printList()  # 1 -> 2 -> 3 -> 4 -> NULL

    ll.Reverse()
    ll.printList()  # 4 -> 3 -> 2 -> 1 -> NULL

    print(ll.hasCycle())  # False

    ll.InsertAtEnd(2)
    ll.InsertAtEnd(3)
    ll.removeDuplicates()
    ll.printList()  # 4 -> 3 -> 2 -> 1 -> NULL

    print(ll.getNthFromEnd(2))  # 2
