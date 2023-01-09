import json
import numpy as np
from time import sleep
import locale
import re
import random
import array


class utils:
    def convertDictToArray(self, dict):
        new_lis = list(dict.items())
        con_arr = np.array(new_lis)
        return con_arr

    def acceptParser(self, argument):
        return argument.replace("*", "")

    def remove_urls(self, vTEXT):
        vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
        if (vTEXT is None):
            vTEXT = "```[check-links-bellow]```"
        elif (vTEXT == "``` ```"):
            vTEXT = "```[check-links-bellow]```"
        elif (vTEXT == "```\n```"):
            vTEXT = "```[check-links-bellow]```"
        elif (len(vTEXT) < 1):
            vTEXT = "```[check-links-bellow]```"
        else:
            vText = vTEXT
        return (vTEXT)

    def ncomma(self, num):
        if (len(str(num))):
            return '{:>,.0f}'.format(num)
        else:
            return '0'

    def reshapeArray(self, lst, n):
        return [lst[i * n:(i + 1) * n] for i in range(len(lst) // n)]

    def splitArray(self, a, n):
        k, m = divmod(len(a), n)
        return list((a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)))
