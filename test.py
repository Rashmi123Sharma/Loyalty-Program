# matrix=[
#     [1,2,3,4],
#     [5,6,7,8],
#     [9,10,11,12],
#     [13,14,15,16]
# ]




# current_status='top' #left bottom right

# sol=[]
# while 1:
#     for i in matrix:
#         print(i)
#     print('-----------------')
#     if current_status=='top':
#         if len(matrix)==0:
#             break
#         sol.extend(matrix[0])
#         matrix.pop(0)
#         current_status='right'
#     elif current_status=='right':
#         if len(matrix)==0:
#             break
#         for i in range(len(matrix)):
#             sol.append(matrix[i][-1])
#             matrix[i].pop(-1)
#         current_status='bottom'
#     elif current_status=='bottom':
#         if len(matrix)==0:
#             break
#         sol.extend(matrix[-1][::-1])
#         matrix.pop(-1)
#         current_status='left'
#     elif current_status=='left':
#         if len(matrix)==0:
#             break
#         for i in range(len(matrix)-1,0-1,-1):
#             sol.append(matrix[i][0])
#             matrix[i].pop(0)
#         current_status='top'
    
    
    
# print(sol)



matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]
          
for i in matrix[0]:
    print(i)
print(matrix[1][-1])
a=matrix[-1][::-1]
for j in a:
     print(j)
print(matrix[1][0])
