import math


list_0 = [True]# answer is False
list_1 = [False, True, True]# answer is False
list_2 = [True, False, True]# answer is True
list_3 = [False, True, True, False, True] # answer is True

# # function to check normal occlusion
# def normal_check(_list):
#     init_state = True
#     for i in _list[1:]:
#         init_state = init_state and i
#     return init_state

# function to check normal occlusion
# def normal_check(_list):
#     return True and all(_list[1:])


def normal_check(_list):
    if len(_list) == 0:
        return False
    return all(_list[1:])


if __name__ == "__main__":
    print(normal_check(list_0))
    print(normal_check(list_1))
    print(normal_check(list_2))
    print(normal_check(list_3))
