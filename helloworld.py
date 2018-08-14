import time


# DP

arr = [1, 2, 4, 1, 7, 8, 3]
# arr = [4, 1, 1, 9, 10]

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

W = 10
values = [6,3,5,4,6]
weights = [2,2,6,5,4]

# 0-1 Knapsack problem 
def rec_knapsack(warr, varr, i, W):
    if i == 0 and warr[0] > W:
        return 0
    if i == 0 and warr[0] <= W:
        return varr[0]
    if warr[i] > W:
        return rec_knapsack(warr, varr, i-1, W)

    return max(
        rec_knapsack(warr, varr, i-1, W),
        rec_knapsack(warr, varr, i-1, W-warr[i]) + varr[i]
    )



max_value = rec_knapsack(weights, values, len(weights)-1, W)
print(max_value)






