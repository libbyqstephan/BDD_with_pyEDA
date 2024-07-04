#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:37:58 2024

@author: libbystephan
"""
import pyeda
from pyeda.inter import *
import numpy as np

# finds all node combos for all valid edges in RR
def gen_edge_combos(nodes):
    edges = []
    for i in nodes:
        for j in nodes:
            condition = ((i+3)%32 == j%32) or ((i+8)%32 == j%32)
            if condition == True:
                edges.append([i,j])
    return edges

# generate boolean expression to represent given node
# in 'binary' (i.e. string form of ~x[0] & x[1] & ...)
def gen_expression(node_num, node_letter):   
    binary_rep = '{0:05b}'.format(node_num)
    bool_string = ''
    for i in range(5):
        if binary_rep[i] == '0':
            bool_string += '~'
        bool_string += node_letter + '[' + str(i) + ']'
        if i != 4:
            bool_string += ' & '
    return bool_string

# iterate through all nodes and append to create one large
# bool expression (used for EVEN and PRIME)
def EP_bdd_exp(nodes, node_letter):
    bdd_exp = ''
    for i in range(len(nodes)):
        bdd_exp += gen_expression(nodes[i], node_letter)
        if i != len(nodes)-1:
            bdd_exp += ' | '
    return bdd_exp

# iterate through all nodes and append to create one large
# bool expression (used specifically for RR)
def RR_bdd_exp(node_combos):
    bdd_exp = ''
    for i in range(len(node_combos)):
        bdd_exp += gen_expression(node_combos[i][0],'x') + ' & ' + gen_expression(node_combos[i][1],'y')
        if i != len(node_combos)-1:
            bdd_exp += ' | '
    return bdd_exp

# creates RR2 from RR
def gen_RR2(RR_first, RR_second,x,y,z):
    RR_first = RR_first.compose({y[0]: z[0], y[1]: z[1], y[2]: z[2], y[3]: z[3], y[4]: z[4]})
    RR_second = RR_second.compose({x[0]: z[0], x[1]: z[1], x[2]: z[2], x[3]: z[3], x[4]: z[4]})
    RR2 = (RR_first & RR_second)
    RR2 = RR2.smoothing(z)
    return RR2

# creates RR2* from RR2
def gen_RR2_star(RR2,x,y,z):
    H = RR2
    while True:
        H_prime = H
        H = H_prime | gen_RR2(H_prime, RR2, x,y,z)
        if H == H_prime:
            break
    RR2_star = H
    return RR2_star

# creates a dictionary to represent the 5 bits of num
# used as a helper for test case's restrict()
def gen_dict(num, var):
    binary_rep = '{0:05b}'.format(num)
    dictionary = {}
    for i in range(5):  
        dictionary.update({var[i]: int(binary_rep[i])})
    return dictionary


#%%

def main():
    # k = 5

    nodes = list(range(32))
    even = list(range(0,31,2))
    prime = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)
    
    # generate BDD's for EVEN, PRIME, RR
    edges = gen_edge_combos(nodes)
    RR = expr2bdd(expr(RR_bdd_exp(edges)))
    EVEN = expr2bdd(expr(EP_bdd_exp(even, 'y')))
    PRIME = expr2bdd(expr(EP_bdd_exp(prime, 'x')))
    
    # STEP 3.1 Test BDD's for RR, EVEN, PRIME
    print("----Test Cases for Step 3.1----")
    test = RR.restrict({**gen_dict(27,x), **gen_dict(3,y)})
    print("RR(27,3) = ",bool(test))
    test = RR.restrict({**gen_dict(16,x), **gen_dict(20,y)})
    print("RR(16,20) = ",bool(test))
    test = EVEN.restrict(gen_dict(14,y))
    print("EVEN(14) = ",bool(test))
    test = EVEN.restrict(gen_dict(13,y))
    print("EVEN(13) = ",bool(test))
    test = PRIME.restrict(gen_dict(7,x))
    print("PRIME(7) = ",bool(test))
    test = PRIME.restrict(gen_dict(2,x))
    print("PRIME(2) = ",bool(test))
    print('\n')

    # generate BDD for RR2
    RR2 = gen_RR2(RR, RR,x,y,z)
        
    # STEP 3.2 TEST BDD for RR2
    print("----Test Cases for Step 3.2----")
    test = RR2.restrict({**gen_dict(27,x), **gen_dict(6,y)})
    print("RR2(27,6) = ",bool(test))
    test = RR2.restrict({**gen_dict(27,x), **gen_dict(9,y)})
    print("RR2(27,9) = ",bool(test))
    print('\n')
    
    # STEP 3.3 create bdd for RR2*
    RR2_star= gen_RR2_star(RR2,x,y,z)
    
    # STEP 3.4 verify truth value of statement A
    apple = (EVEN & RR2_star).smoothing(y)
    fish = (not PRIME) or apple
    result = not(not(fish.smoothing(x)))
    print("----Result for Step 3.4----")
    print("The truth value for Statement A is: ",result)

if __name__ == "__main__":
    main()
