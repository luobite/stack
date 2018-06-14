# -*- coding:utf-8 -*-
class Stack(object):
    def __init__(self):
        self.__list=[]

    def push(self,item):
        '''添加元素'''
        self.__list.append(item)

    def pop(self):
        '''弹出栈顶元素'''
        return self.__list.pop()
    def peek(self):
        '''返回栈顶元素'''
        if self.__list:
            return self.__list[-1]
        else:
            return None
    def is_empty(self):

        return self.__list==[]

    def size(self):
        return len(self.__list)
'''if __name__=='__main__':
    s=Stack()
    s.push(1)
    s.push(2)
    print s.pop()
    print s.pop()'''

def bubble_sort(lists):
    count=len(lists)
    for i in range(0,count):
        for j in range(i+1,count):
            if lists[i]<lists[j]:
                lists[i],lists[j]=lists[j],lists[i]
    return lists
list1=[9,7,2,10,5,1,100]
a=bubble_sort(list1)
print a