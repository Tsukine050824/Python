# import math
# import random

# print(math.sqrt(36))
# print(math.pi)

# print(random.randint(1, 50))

# age = 25
# price = 19.99
# first_name = "John"
# print(f"My name is {first_name}.")
# print(f"I am {age} years old.")
# print(f"The price is ${price}.")


# name = input("Enter your name: ")
# print(f"Hello, {name}!")

# first = input("Enter your first number: ")
# second = input("Enter your second number: ")
# sum_result = float(first) + float(second)
# print(f"The sum of {first} and {second} is {sum_result}.")

# Hàm print cơ bản
# print("Xin chào Python!")
# Ten = "Nam"
# Tuoi = 18
# print(f"Tên: {Ten}, Tuổi: {Tuoi}", sep="-")
# A = "A"
# B = "B"
# C = "C"
# print({A}, {B}, {C}, sep=" - ")

# Hàm input cơ bản
# name = input("Nhập tên của bạn: ")
# print(f"Xin chào {name}!")
# age = input("Nhập tuổi của bạn: ")
# print(f"Năm sau bạn sẽ {int(age) + 1} tuổi.")
# A = input("Nhập kí tự A: ")
# B = input("Nhập kí tự B: ")
# C = input("Nhập kí tự C: ")
# print(f"{A} - {B} - {C}")

# Hàm len và type cơ bản
# len là hàm trả về độ dài của một chuỗi, danh sách, tuple, dictionary, set
# type là hàm trả về kiểu dữ liệu của một giá trị
# string = input("Enter a string: ")
# print("chuỗi có số kí tự là", len(string))
# Amen = [10, 20, 30, 40, 50]
# print("List có", len(Amen), "phần tử")
# Dictionary = {"A": 1, "B": 2, "C": 3}
# print("Dictionary có", len(Dictionary), "phần tử")

# x = 100
# y = 3.5
# z = "Python"
# print(type(x), type(y), type(z))

# string = input("Enter a srting: ")
# print(f"The type of the entered value is {type(string)}")
# number = int(input("Enter a number: "))
# print(f"The type of the entered value is {type(number)}")

# Biến đổi kiểu dữ liệu
# a = int(input("Enter first number: "))
# print(a + 10)
# b = float(input("Enter second number: "))
# print(b * 2)
# c = str(input("Enter third value: "))
# print("Số vừa nhập là " + c)

# Hàm list, là trả về một danh sách các phần tử từ 1 chuỗi hoặc 1 dãy số, có thể dùng để chuyển đổi kiểu dữ liệu sang list
# Các phần tử có thể thay đổi
# a = [10, 20, 30, 40, 50]
# print(a)
# string = input("Enter a string: ")
# print(list(string))
# b = list(range(1, 6))
# print(b)

#Hàm tuple, là trả về một bộ các phần tử từ 1 chuỗi hoặc 1 dãy số, các phần tử không thể thay đổi
# a = (1, 2, 3, 4, 5)
# print(a)
# b = tuple(input("Enter a string: "))
# print(b)
# c = tuple(range(1, 6))
# print(c)

#Hàm dictionary, là trả về các cặp key-value, các phần tử có thể thay đổi, và có dữ liệu có nhãn
# a = {"A": 1, "B": 2, "C": 3}
# print(a)
# b = dict(name = "Nam", age = 18)
# print(b)
# c = {"x" : 10, "y" : 20}
# c["z"] = 30
# print(c)

# Hàm set, là trả về một tập hợp các phần tử không trùng lặp, các phần tử có thể thay đổi, và không có dữ liệu có nhãn
# a = {1, 2, 3, 4, 5}
# print(a)
# b = set(input("Enter a string: "))
# print(b)
# c = {1, 2, 3}
# c.add(4)
# print(c)

# Hàm range
# a = list(range(5))
# print(a)
# b = list(range(1, 6))
# print(b)
# c = list(range(2, 12, 2))
# print(c)

# Hàm min, max, sum
# a = [5, 10, 15, 20]
# print("Min:", min(a))
# print("Max:", max(a))
# print("Sum:", sum(a))
# string = input("Enter numbers separated by spaces: ")
# print("Min:", min(string.split()))
# print("Max:", max(string.split()))
# print("Sum:", sum(map(int, string.split())))

# Hàm Sorted
# a = [7, 3, 9, 1]
# print(sorted(a, reverse=True))
# string = input("Enter a string seperated by spaces: ")
# print(sorted(string.split()))

# Hàm zip
# names = ["An", "Binh", "Cuong"]
# scores = [7, 8, 9]
# print(list(zip(names, scores)))
# for name, score in zip(names, scores):
#     print(f"{name}: {score}")

# Hàm enumerate
# a = ["Python", "Java", "C++"]
# for index, value in enumerate(a):
#     print(f"Index: {index}, Value: {value}")
# for inde, val in enumerate(a, start=1):
#     print(f"Index: {inde}, Value: {val}")

# Hàm map
# numbers = [1, 2, 3, 4, 5]
# result = list(map(lambda x: x * 2, numbers))
# print(result)  # Output: [2, 4, 6, 8, 10]
# ggez = input("Enter numbers separated by spaces: ")
# mapped_result = list(map(int, ggez.split()))
# print(mapped_result)

# Hàm filter
# nums = [3, 7, 10, 15, 20, 25]
# filtered_nums = list(filter(lambda x: x >= 10, nums))
# print(filtered_nums)  # Output: [10, 15, 20, 25]
# string = input("Enter numbers separated by spaces: ")
# filtered_result = list(filter(lambda x: int(x) % 3 == 0, string.split()))
# print(filtered_result)

# Hàm all và any
# a = [2, 4, 6, 8]
# print(all(x % 2 == 0 for x in a))
# b = [1, 3, 5, 8]
# print(any (x % 2 == 0 for x in b))
# string = input("Enter numbers separated by spaces: ")
# numbers = list(map(int, string.split()))
# print(all(x > 0 for x in numbers))
# print(any(x < 0 for x in numbers))

# Hàm instance
# x = 10
# y = "Python"
# z = 3.5
# print(isinstance(x, int))
# print(isinstance(y, str))
# print(isinstance(z, float))
# value = input("Enter a value: ")
# try:
#     num = float(value)
#     print(isinstance(num, (int, float)))
# except ValueError:
#     print("False")

#Hàm open
# file = open("data.txt", "w")
# file.write("Python is awesome")
# f = open("data.txt", "r")
# content = f.read()
# print(content)
# f.close()

#Hàm ẩn danh (lambda)
# nums = [1, 2, 3, 4, 5]
# result = list(map(lambda x: x * 3, nums))
# print(result)

# nums2 = [10, 15, 20, 25, 30]
# result2 = list(filter(lambda x: x > 15, nums2))
# print(result2)

# nums3 = 9
# square = (lambda x: x * x)(nums3)
# print(square)

# student = [("An", 7), ("Binh", 9), ("Cuong", 8)]
# sorted_students = sorted(student, key=lambda x: x[1])
# print(sorted_students)

#Hàm iter and next
# nums = [10, 20, 30]
# iterator = iter(nums)
# print(next(iterator))
# print(next(iterator))
# print(next(iterator))

# string = "Python"
# str_iterator = iter(string)
# print(next(str_iterator))
# print(next(str_iterator))
# print(next(str_iterator))
# print(next(str_iterator))
# print(next(str_iterator))
# print(next(str_iterator))

# print(list(iterator))
# print(list(iterator))

# class EvenNumbers:
#     def __init__(self, max):
#         self.max = max
#         self.num = 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.num <= self.max:
#             current = self.num
#             self.num += 2
#             return current
#         else:
#             raise StopIteration
        
# even_numbers = EvenNumbers(10)
# for number in even_numbers:
#     print(number)   

#Hàm decorator

