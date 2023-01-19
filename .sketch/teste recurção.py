import re
import sys
sys.setrecursionlimit(50)


def recusive(target, op=0):
    head = ""
    f = []
    i = op

    while i < len(target):
        current_char = target[i]
        i += 1
        if current_char == "{":
            (i, match_1) = recusive(target, i)
            op = i
            build = [int(head)]
            [build.append(i) for i in match_1]
            f.append(tuple(build))
            head = ""
        elif current_char == "}":
            f.append(target[op:i-1])
            return i, f
        else:
            head += current_char
    return i, f


def break_to_list(target):
    m = []
    for i in re.split(r"{|}", target):
        if not i or i.isspace():
            continue
        m.append([i for i in re.split(r", | |,", i) if i])
    return m

    # while i < len(target):
    #     current_char = target[i]
    #     i += 1
    #     if current_char == "{":
    #         (i, match_1) = recusive(target, i)
    #         op = i
    #         build = [int(head)]
    #         [build.append(i) for i in match_1]
    #         f.append(tuple(build))
    #         head = ""
    #     elif current_char == "}":
    #         f.append(target[op:i-1])
    #         return i, f
    #     else:
    #         head += current_char
    # return i, f


target2 = "1 { 2 { 3 { 4 { 5 {achou}}} 4 { 2 { 1 {ss} } 3 {ws} }}}"
# (1,                                                      )
#    (2,                                                  )
#       (3,                                              )
#          (4,            ), (4,                        )
#             (5,"achou"),      (2,         ), (3, "ws")
#                                  (1, "ss")

target = "o"
print(break_to_list(target))
