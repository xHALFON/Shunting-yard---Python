from abc import ABC
from numpy import double
from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def calc(self)->double:
        pass

# implement the classes here
class Num():
    def __init__(self, t):
        self.x = t

    def calc(self):
        return self.x


class BinExp(Expression):
    def __init__(self, a:Num, b:Num):
        super().__init__()
        self.a = a
        self.b = b

    def calc(self) ->double:
        pass

class Minus(BinExp):
    def calc(self):
        return self.a.calc() - self.b.calc()

class Plus(BinExp):
    def calc(self):
        return self.a.calc() + self.b.calc()

class Mul(BinExp):
    def calc(self):
        return self.a.calc() * self.b.calc()

class Div(BinExp):
    def calc(self):
        return self.a.calc() / self.b.calc()

#implement the parser function here
def parser(expression)->double: #'5+3*(4-1)' #20*20+(-15)*((-4)-35+(-15))
    res = 0.0
    num = 0.0
    level = 0
    stack = []
    flag = 0
    flag2 = 0
    flag3 = 0
    que = []
    qeu2 = []
    while len(expression) > 0: #(-54)+86*((-80)-58)   #(5*4+3)-1                (-69)*(-69)+43*((-9)-(99)+43)
        if expression[0] != '+' and expression[0] != '-' and expression[0] != '*' and expression[0] != '/':
            if expression[0] != '(' and expression[0] != ")":
                while expression[0] != '+' and expression[0] != '-' and expression[0] != '*' and expression[0] != '/' and expression[0] != '(' and expression[0] != ")":
                    num = num*10 + int(expression[0])
                    expression = expression[1:]
                    if len(expression) == 0:
                        break
                if flag2 == 1:
                    num = num * -1
                    que.append(num)
                    num = 0.0
                    flag2 = 0
                else:
                    que.append(num)
                    num = 0.0
                    flag2 = 0
                    flag = 0
            elif expression[0] == '(':
                level = 0
                flag = 1
                stack.append(expression[0])
                expression = expression[1:]
            elif expression[0] == ')':
                flag3 = 1
                while stack[-1] != '(':
                    que.append(stack.pop(-1))
                    flag3 = 0
                stack.pop(-1)
                expression = expression[1:]
                if(len(expression) == 0):
                    break
                if expression[0] == '-':
                    expression = expression[1:]
                    flag2 = 1
                    flag3 = 0
                    stack.append('+')
                if flag3 == 1 and len(stack) > 0:
                    if stack[-1] == '-':
                        stack.pop(-1)
                        stack.append('+')
                        que[-1] = que[-1]*-1
                        flag3 = 0
                stack2 = stack[:]
                while(len(stack2) > 0):
                    if stack2[0] == '(' or stack2[0] == '+' or stack2[0] == '-':
                        level = 1
                    elif stack2[0] == '*' or stack2[0] == '/':
                        level = 2
                    stack2.pop(0)

        elif expression[0] == '+' or expression[0] == '-':
            if level > 1:
                while level > 1:
                    que.append(stack.pop(-1))
                    if len(stack) == 0:
                        level = 1
                        break
                    if(stack[-1] == '+' or stack[-1] == '-' or stack[-1] == '('):
                        level = 1
            if flag == 1:
                flag2 = 1
                flag = 0
                expression = expression[1:]
                continue
            if len(stack) == 0:
                stack.append(expression[0])
                expression = expression[1:]
                continue
            if stack[-1] == '*' or stack[-1] == '/':
                que.append(expression[0])
                expression = expression[1:]
            else:
                stack.append(expression[0])
                expression = expression[1:]
        elif expression[0] == '*' or expression[0] == '/' or expression[0] == '(' or expression[0] == ')':
            level = 2
            stack.append(expression[0])
            expression = expression[1:]

    while len(stack) > 0:
        que.append(stack.pop(-1))

    temp = 0.0
    temp2 = 0.0
    arit = ''
    while len(que) > 0:
        while que[0] != '+' and que[0] != '-' and que[0] != '*' and que[0] != '/':
            stack.append(que.pop(0))
        if len(stack) != 0:
            temp = stack.pop(-1)
        else:
            temp = 0.0
        if len(stack) == 0: # if the number is invalid (wrong answer)
            arit = que.pop(0)
            if(arit == '+'):
                temp = temp + que.pop(0)
            elif(arit == '-'):
                temp = temp - que.pop(0)
            elif(arit == '*'):
                temp = temp * que.pop(0)
            elif(arit == '/'):
                temp = temp / que.pop(0)
            stack.append(temp)
            temp = 0.0
        else:
            arit = que.pop(0)
            temp2 = stack.pop(-1)
            if (arit == '+'):
                temp2 = temp2 + temp
            elif (arit == '-'):
                temp2 = temp2 - temp
            elif (arit == '*'):
                temp2 = temp2 * temp
            elif (arit == '/'):
                temp2 = temp2 / temp
            stack.append(temp2)
            temp = 0.0
            temp2 = 0.0

    return stack.pop(-1)