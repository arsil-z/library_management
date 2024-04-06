import sys


# Time Complexity = O(N) where n is the size of the array
# Space Complexity = O(1) as we are not using any extra spact
def max_sum_subarray(array):
    """
    The intuition of the algorithm is not to consider the subarray
    as a part of the answer if it's sum is less than 0.
    A subarray with a sum less than 0 will always reduce our answer
    and so this type of subarray cannot be a part of the subarray with
    maximum sum
    :param array:
    :return:
    """
    len_of_array = len(array)
    if len_of_array == 0:
        return 'Invalid input'

    if len_of_array == 1:
        return array[0]

    maximum = -sys.maxsize-1
    sum = 0

    for i in range(len_of_array):
        sum += array[i]

        if sum > maximum:
            maximum = sum

        if sum < 0:
            sum = 0

    return maximum


print(max_sum_subarray(([-2, 1, -3, 4, -1, 2, 1, -5, 4])))

