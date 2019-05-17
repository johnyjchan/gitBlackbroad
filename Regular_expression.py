# -*- encoding:utf-8 -*-
"""
    author:cyj
    stupid regular expression implementation that only support to parse patterns involve operator '( )' , '|'
"""
import time

PATTERN = '(1|2)0(2|1)'
TEST_CASES = ['01020101001', '111202000', '111100321111111', '2222010122103213',\
              '222111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111112010122103213']

def timer(func):
    def get_runtime(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        print(func.__name__,' spend time:', end - start)

    return get_runtime


class PatternNode(object):
    def __init__(self):
        self.next = None
        self.options = []

    def hasNext(self):
        return True if self.next != None else False


class RetrievePattern(object):
    @staticmethod
    def compile_pattern(pattern):
        index = 0
        head = node = PatternNode()
        while index < len(pattern):
            next_node = PatternNode()
            ascii_code = ord(pattern[index])
            az = ascii_code >= ord('a') and ascii_code <= ord('z')
            AZ = ascii_code >= ord('A') and ascii_code <= ord('Z')
            zeroNine = ascii_code >= ord('0') and ascii_code <= ord('9')
            if az or AZ or zeroNine:
                next_node.options = [pattern[index]]
                node.next = next_node
                node = next_node
            elif '(' == pattern[index]:
                right_boundary = pattern[index:].find(')')
                if -1 == right_boundary:
                    raise Exception("could not parse PATTERN")
                else:
                    next_node.options = pattern[index+1:right_boundary + index].split('|')
                index = right_boundary + index
                node.next = next_node
                node = next_node
            else:
                raise Exception("could not parse character")
            index += 1
        return head.next


class AutoMachine(object):
    def load_test_case(self, test_case, head):
        for index in range(len(test_case)):
            if self.state_transition(test_case, index, head):
                return True
        return False

    def state_transition(self, test_case, index, head):
        while index < len(test_case):
            if not test_case[index] in head.options:
                return False
            elif test_case[index] in head.options and head.hasNext():
                index = index + 1
                head = head.next
            elif test_case[index] in head.options and not head.hasNext():
                return True


RetrievePattern = RetrievePattern()
AutoMachine = AutoMachine()


@timer
def stupid_regular_expression_match_one(PATTERN, TEST_CASES):
    linkList_pattern = RetrievePattern.compile_pattern(PATTERN)
    for test_case in TEST_CASES:
        print(AutoMachine.load_test_case(test_case, linkList_pattern))

stupid_regular_expression_match_one(PATTERN, TEST_CASES)
