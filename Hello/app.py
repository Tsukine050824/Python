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

# Hàm list 
# a = [10, 20, 30, 40, 50]
# print(a)
# string = input("Enter a string: ")
# print(list(string))
# b = list(range(1, 6))
# print(b)

#Hàm tuple
# a = (1, 2, 3, 4, 5)
# print(a)
# b = tuple(input("Enter a string: "))
# print(b)
# c = tuple(range(1, 6))
# print(c)

#Hàm dictionary
# a = {"A": 1, "B": 2, "C": 3}
# print(a)
# b = dict(name = "Nam", age = 18)
# print(b)
# c = {"x" : 10, "y" : 20}
# c["z"] = 30
# print(c)

# Hàm set
a = {1, 2, 3, 4, 5}
print(a)
b = set(input("Enter a string: "))
print(b)
c = {1, 2, 3}
c.add(4)
print(c)