import time
import numpy as np


# DP

# overlap sub-problems
def rec_opt(arr, i):
    if i == 0:
        return arr[0]
    if i == 1:
        return max(arr[0], arr[1])
    
    return max(rec_opt(arr, i-2)+arr[i], rec_opt(arr, i-1))

def dp_opt(arr, i):
    opt_arr = [0 for x in range(len(arr))]
    opt_arr[0] = arr[0]
    opt_arr[1] = max(arr[0], arr[1])

    for i in range(2, len(arr)):
        opt_arr[i] = max(opt_arr[i-2]+arr[i], opt_arr[i-1])
    
    return opt_arr[-1]


# this question is very similar to Knapsack problem 
def rec_subset(arr, i, s):
    if s == 0:
        return True
    elif i == 0:
        return arr[i] == s
    elif arr[i] > s:
        return rec_subset(arr, i-1, s)
    else:
        return rec_subset(arr, i-1, s-arr[i]) or rec_subset(arr, i-1, s)

def dp_subset(arr, S):
    opt_arr = np.zeros((len(arr), S+1), dtype=np.bool)
    opt_arr[:, 0] = True
    
    if arr[0] < S:
        opt_arr[0, arr[0]] = True
    
    for i in range(1, len(arr)):
        for s in range(1, S+1):
            if arr[i] > s:
                opt_arr[i, s] = opt_arr[i-1, s]
            else:
                opt_arr[i, s] = opt_arr[i-1, s] or opt_arr[i-1, s-arr[i]]
    x, y = opt_arr.shape
    return opt_arr[x-1, y-1]

# 0-1 Knapsack problem 
def rec_01_knapsack(warr, varr, i, W):
    if i == 0 and warr[0] > W:
        return 0
    if i == 0 and warr[0] <= W:
        return varr[0]
    if warr[i] > W:
        return rec_01_knapsack(warr, varr, i-1, W)

    return max(
        rec_01_knapsack(warr, varr, i-1, W),
        rec_01_knapsack(warr, varr, i-1, W-warr[i]) + varr[i]
    )

def dp_01_knapsack(warr, varr, W):
    opt_arr = np.zeros((len(warr), W+1), dtype=np.int32)
    
    opt_arr[0, warr[0]:] = varr[0]
    opt_arr[:, 0] = 0

    for i in range(1, len(warr)):
        for w in range(W+1):
            if warr[i] > w:
                opt_arr[i, w] = opt_arr[i-1, w]
            else:
                opt_arr[i, w] = max(
                    opt_arr[i-1, w],
                    opt_arr[i-1, w-warr[i]] + varr[i]
                )
    
    x, y = opt_arr.shape
    return opt_arr[x-1, y-1]


def rec_complete_knapsack(warr, varr, i, W):
    if i == 0 and warr[0] > W:
        return 0
    if i == 0 and warr[0] <= W:
        return rec_complete_knapsack(warr, varr, i, W-warr[i]) + varr[i]
    
    if warr[i] > W:
        return rec_complete_knapsack(warr, varr, i-1, W)
    else:
        return max(
            rec_complete_knapsack(warr, varr, i-1, W),
            rec_complete_knapsack(warr, varr, i, W-warr[i]) + varr[i]
        )

def dp_complete_knapsack(warr, varr, W):
    opt_arr = np.zeros((len(warr), W+1), dtype=np.int32)
    opt_arr[:, 0] = 0
    for i in range(W+1):
        opt_arr[0, i] = varr[0] * (i // warr[0])
    
    for i in range(1, len(warr)):
        for w in range(1, W+1):
            if warr[i] > w:
                opt_arr[i, w] = opt_arr[i-1, w]
            else:
                opt_arr[i, w] = max(
                    opt_arr[i-1, w],
                    opt_arr[i, w-warr[i]] + varr[i]
                )
    x, y = opt_arr.shape
    return opt_arr[x-1, y-1]


# 
def rec_minimal_coin(varr, i, S):
    
    if i < 0 or S < 0:
        raise Exception("Invalid parameters")

    if S == 0:
        return 0
    if S == varr[i]:
        return 1
    if i == 0:
        return S
    if S < varr[i]:
        return rec_minimal_coin(varr, i-1, S)

    return min(
        rec_minimal_coin(varr, i, S-varr[i]) + 1,
        rec_minimal_coin(varr, i-1, S)
    )

def dp_minimal_coin(varr, S):
    opt_arr = np.zeros((len(varr), S+1), dtype=np.int32)
    opt_arr[:, 0] = 0
    opt_arr[0, :] = [x for x in range(S+1)]

    # should be very careful! idx and varr[idx]    
    for idx in range(1, len(varr)):
        for s in range(1, S+1):
            if varr[idx] == s:
                opt_arr[idx, s] = 1
            elif s <= varr[idx]:
                opt_arr[idx, s] = opt_arr[idx-1, s]
            else:
                opt_arr[idx, s] = min(
                    opt_arr[idx, s-varr[idx]] + 1,
                    opt_arr[idx-1, s]
                )
    x, y = opt_arr.shape
    return opt_arr[x-1, y-1]

if __name__ == "__main__":

    values = [6,3,5,4,6]
    weights = [3,2,6,5,4]

    for t_w in range(30):
        value1 = rec_01_knapsack(weights, values, len(weights)-1, t_w)
        value2 = dp_01_knapsack(weights, values, t_w)
        print("rec: %d | dp: %d"%(value1, value2))

    for t_w in range(30):
        value1 = rec_complete_knapsack(weights, values, len(weights)-1, t_w)
        value2 = dp_complete_knapsack(weights, values, t_w)
        
        print("w: %d: rec: %d | dp: %d"%(t_w, value1, value2))

    coins = [1, 2, 5, 10]
    count2 = dp_minimal_coin(coins, 5)
    try:
        for money in range(1, 20):
            count1 = rec_minimal_coin(coins, len(coins)-1, money)
            count2 = dp_minimal_coin(coins, money)
            print("for money: %d|least coin: [rec:%d] [dp:%d]" % (money, count1, count2))
    except:
        print("opps")





