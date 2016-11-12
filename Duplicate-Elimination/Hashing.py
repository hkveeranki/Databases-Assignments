class MyHashStore:
    """ Hash Table for Duplicate Elimination"""

    def __init__(self):
        """
        Default Constructor
        """
        self.__set = set()
        pass

    def search(self, key):
        """
        Perform the search
        :param key: key to be searched
        :return: true if found else False
        """
        return key in self.__set

    def insert(self, key):
        """
        Perform Insertion
        :param key: key to be inserted
        """
        self.__set.add(key)
