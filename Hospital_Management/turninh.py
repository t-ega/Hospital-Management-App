# def testing(ops):
#     record = list()
#     for i in ops:
#         try:
#             record.append(int(i))
#         except ValueError as e:
#             pass
#         if i.upper() == 'C' and len(record) >= 1:
#             record.pop()
#         if i.upper() == 'D' and len(record) >= 2:
#             record.append(2 * int(record[-1]))
#         if i == '+' and len(record) >= 2:
#             cal = int(record[-2]) + int(record[-1])
#             record.append(cal)
#
#     return sum(record)
#
#
# if __name__ == '__main__':
#     ops = ['5', '-2', '4', 'C', 'D', '9', '+', '+']
#
#     print(testing(ops))


