#1 integer operations

num1 =5
num2 =8
result = num1 + num2
print("Sum:", result)

#2 Float operations

float_num1 = 5.0
float_num2 = 2.5
result = float_num1 * float_num2
print("product:", result)

#3 String Concatenation

string1 = "my "
string2 = "world"
result = string1+""+string2
print(result)

#4 List Manipulation

my_list = [1,2,2,4,5]
my_list.append(6)
print("updated list:",my_list)

#5 Tuple Operations

my_tuple = (1,2,3,4,5)
print("length of tuple:",len(my_tuple))

#6 Dictionary usage

my_dict = {'a':1, 'b':2, 'c':3}
print("value of 'b':", my_dict['b'])

#7 Set operations

set1 = {1,2,3,4,5}
set2 = {4,5,6,7,8}
result = set1.intersection(set2)
print("Intersection:",result)

#8 Boolean Operations:
bool1 = True
bool2 = False
result = bool1 and bool2
print("Result of AND:",result)

#9 Complex number operations:
Complex1 = 2+3j
Complex2 = 1-2j
result = Complex1 * Complex2
print("product of complex numbers:",result)

#10 Type Conversion
num_str = "123"
num_int = int(num_str)
print("Converted Integer:",num_int)

# Mathematical/Logical
#Math Liberary

import math
num = 16
result = math.sqrt(num)
print("Square Root:",result)

#Math Liberary-Power
import math
num = 16
result = math.sqrt(num)
print("Square Root:", result)

import math
base = 2
exponent = 3
result = math.pow(base, exponent)
print("Power:", result)


import math
angle = 45
result = math.sin(math.radians(angle))
print("Sine of 45 degrees:", result)


import math
num = 5
result = math.factorial(num)
print("Factorial of 5:", result)


import math
num = 4.3
result = math.ceil(num)
print("Ceiling of 4.3:", result)


import math
num = 100
result = math.log10(num)
print("Logarithm base 10 of 100:", result)


logic1 = True
logic2 = False
result = logic1 and logic2
print("Result of Logical AND:", result)

logic1 = True
logic2 = False
result = logic1 or logic2
print("Result of Logical OR:", result)


logic = True
result = not logic
print("Result of Logical NOT:", result)


logic1 = True
logic2 = False
result = logic1 ^ logic2
print("Result of Logical XOR:", result)
