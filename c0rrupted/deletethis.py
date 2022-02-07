# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:19:00 2021

@author: User
"""

a = [3,4,5,1,2]
for i in range(len(a) - 2):
	a.append(a.pop(0))
print(a)