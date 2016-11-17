import sys


class Btree:
    """Class to Handle the whole Btree"""

    def __init__(self, t):
        """
        Default constructor for B-Tree
        :param t:  minimum degree of the Tree
        """
        self.root = None
        self.t = t
        pass

    def insert(self, key):
        """
        Insert the given key into the B-Tree
        :param key: key to be inserted
        """
        if self.root is None:
            self.root = Node(self.t, True)
            self.root.keys[0] = key
            self.root.n += 1
        else:
            if self.root.is_full():
                new_root = Node(self.t, False)
                new_root.children[0] = self.root
                new_root.splitChild(0, new_root.children[0])
                i = 0
                if new_root.keys[0] < key:
                    i += 1
                new_root.children[i].insert(key)
                self.root = new_root
            else:
                self.root.insert(key)

    def search(self, key):
        """
        Search the given key in the B-Tree
        :param key: key to be searched
        :return: True if key is found else False
        """
        if self.root is not None:
            return self.root.search(key) is not None
        return False

    def traverse(self):
        """
        Perform Traversal of the Tree
        """
        if self.root is not None:
            self.root.traverse()


class Node:
    """Class for the Node of BTree"""

    def __init__(self, t, leaf):
        """
        Constructor for the class
        :param t: minimum degree
        :param leaf: is it a leaf or not a boolean argument
        """
        self.t = t
        self.leaf = leaf
        self.keys = [None] * (2 * t - 1)
        self.children = [None] * (2 * t)
        self.n = 0
        pass

    def insert(self, key):
        """
        Insert the given Key recursively
        :param key: Key to be Inserted
        """
        i = self.n - 1
        if self.leaf:
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
            self.n += 1
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            if self.children[i + 1].is_full():
                self.splitChild(i + 1, self.children[i + 1])
                if self.keys[i + 1] < key:
                    i += 1
            self.children[i + 1].insert(key)

    def traverse(self):
        """
            Function to aid traversal of the Tree.
            Performs the Traversal of the Node
        """
        i = 0
        while i < self.n:
            if not self.leaf:
                self.children[i].traverse()
            print(self.keys[i])
            i += 1
        if not self.leaf:
            self.children[i].traverse()

    def search(self, key):

        """
        Search the key in the Node recursively
        :param key: the key to be searched
        :return: None if there is no such key else the key
        """
        i = 0
        while i < self.n and key > self.keys[i]:
            i += 1
        if i < self.n and self.keys[i] == key:
            return self.keys[i]
        if self.leaf:
            return None
        return self.children[i].search(key)

    def splitChild(self, index, child):
        """
        Split the given child and at the given index of parent
        :param index: index at which the children should be attached
        :param child: child which is to be split
        """
        # Make the new child
        # sys.stderr.write("Splitting a Node\n")
        new_child = Node(child.t, child.leaf)
        # Copy the old keys to New one
        for i in range(self.t - 1):
            new_child.keys[i] = child.keys[i + self.t]
        new_child.n = self.t - 1

        if not child.leaf:
            # Move the last children of old child  to new child
            for i in range(self.t):
                new_child.children[i] = child.children[i + self.t]
        child.n = self.t - 1

        # Create Space for the new Child
        for i in range(self.n, index, -1):
            self.children[i + 1] = self.children[i]
        # insert New Child
        self.children[index + 1] = new_child
        # shift the keys to accommodate New key
        for i in range(self.n - 1, index - 1, -1):
            self.keys[i + 1] = self.keys[i]
        # Insert middle of child
        self.keys[index] = child.keys[self.t - 1]
        self.n += 1

    def is_full(self):
        """
        Utility function to check whether the node is full or not
        """
        return self.n == 2 * self.t - 1

    def __str__(self):
        """
        Utility function to wrap the Node as a string with info
        """
        return "Keys: " + str(self.keys) + " Leaf: " + str(self.leaf) \
               + " Children: " + str(map(str, self.children)) + \
               " n:" + str(self.n)
