import ast
from printtab import printtab
import os

if __name__ == '__main__':
    f = open('log.txt', 'r')
    tab = f.read()
    tab = tab.split('\n')
    for elem in tab:
        # try:
        elem = ast.literal_eval(elem)
        # print(elem)
        for i in range(1, 8000000):
            pass
        os.system('clear')
        if (len(elem) > 0):
            printtab(elem)
        # except:
        #     print('END')
    # x = ast.literal_eval(x)