class EmptyStackError(Exception):
    pass


class Stack:
    def __init__(self):
        self.stack = []
        self.__size = 0

    def top(self):
        """
        Returns the top element of the stack
        :return:
        """
        if self.__size == 0:
            raise EmptyStackError
        return self.stack[0]

    def pop(self):
        """
        Removes the top element of the stack and returns it
        :return:
        """
        if self.__size == 0:
            raise EmptyStackError
        self.__size -= 1
        return self.stack.pop(0)

    def push(self, obj):
        """
        Adds an element to the top of the stack
        :param obj:
        :return:
        """
        self.stack.insert(0, obj)
        self.__size += 1

    def is_empty(self) -> bool:
        """
        Returns true if the stack is empty
        :return:
        """
        return self.__size == 0

    def size(self) -> int:
        """
        Returns the size of the stack
        :return:
        """
        return self.__size
    
    def __str__(self):
        return str(self.stack)
