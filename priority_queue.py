__author__ = 'Antares'


class PriorityQueue(object):
    """
    Implementation of "Minimum Priority Queue", a.k.a. "min heap".
    Items with the same priority are popped according to the order they were added to the queue.
    Put an item that is already in the queue will overwrite the previous priority of this item.
    """
    def __init__(self):
        """

        :rtype : object
        :return:
        """
        self._queue = []
        self._table = {}
        self._count = 0

    def put(self, priority, item):
        """
        put an item into the priority queue.
        Put an item that is already in the queue will overwrite the previous priority of this item.
        :param priority:
        :param item:
        :return:
        """
        if item not in self._table:
            self._queue.append((priority, self._count, item))  # append the item to the end of the list
            i = len(self._queue) - 1
            self._table[item] = i  # add the item to the table  # ONLY edit table after operation of the queue
            self.float(i)  # float it up the tree
        else:
            i = self._table[item]
            self._queue[i] = (priority, self._count, item)  # add the item to the list. So far the index didn't change
            self.float(i)
            self.sink(i)
        self._count += 1

    def pop(self):
        """
        pop the item at top of tree, and adjust the tree to maintain invariant
        :return:
        """
        item = self._queue[0]  # get the tuple at the top of the tree
        last = self._queue.pop()  # pop the tuple at the end of the tree
        self._table.pop(last[2])
        if self._queue:  # if the tree is not empty
            self._queue[0] = last  # put the last tuple to the top
            self._table[last[2]] = 0  # update table
            self._table.pop(item[2])  # remove the original item from table
            self.sink(0)  # and sink it down
        return item[2]

    def float(self, i):
        """
        float an item up the tree to maintain the invariant of the priority queue
        :param i:
        :return:
        """
        while True:
            p = self.parent(i)  # find the parent
            if (p is not None) and (self._queue[i] < self._queue[p]):  # there's a parent and it's less than the child
                self.exchange(i, p)  # exchange them
                i = p  # update the index
            else:
                return

    def sink(self, i):
        """
        sink an item down the tree to maintain the invariant of the priority queue
        :param i:
        :return:
        """
        while True:
            c_left, c_right = self.children(i)  # get the two children
            if c_left is None:  # if has no child
                return
            # if has at least one child, then find the smaller one
            c = c_left if (c_right is None) else (c_left if (self._queue[c_left] < self._queue[c_right]) else c_right)
            if self._queue[i] < self._queue[c]:  # if smaller than the children
                return
            # actually greater than the children
            self.exchange(i, c)  # exchange them
            i = c  # update index

    @staticmethod
    def parent(child):
        """
        find the parent of a child, return None if no such parent
        :param child:
        :return:
        """
        if child == 0:
            return None
        else:
            return int((child+1)/2)-1

    def children(self, parent):
        """
        find the two children of a parent. return a tuple of indices of the two children.
        Index would be None if no such child
        :param parent:
        :return:
        """
        c_left = parent*2+1
        c_right = parent*2+2
        return (c_left if c_left < len(self._queue) else None), (c_right if c_right < len(self._queue) else None)

    def exchange(self, i, j):
        """
        swap two tuples in the queue
        :param i:
        :param j:
        :return:
        """
        temp = self._queue[i]
        self._queue[i] = self._queue[j]
        self._queue[j] = temp

        self._table[self._queue[i][2]] = i  # update table
        self._table[self._queue[j][2]] = j

    def is_empty(self):
        return not self._queue

    def get_top_priority(self):
        """
        get the priority of the top of the tree
        :return:
        """
        return self._queue[0][0]


def main():
    pq = PriorityQueue()

    pq.put(1, "one")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(4, "four")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(2, "two")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(5, "five")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(3, "three")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(0, "zero")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(0, "x")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(4, "x")
    print(pq._queue)
    print(pq._table, "\n")
    pq.put(2, "x")
    print(pq._queue)
    print(pq._table, "\n")

    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")
    print(pq.pop())
    print(pq._queue)
    print(pq._table, "\n")


if __name__ == '__main__':
    main()
