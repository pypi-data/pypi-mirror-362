# دالة الجمع
def Addition(a, b):
    return a + b

# دالة الطرح
def subtraction(a, b):
    return a - b

# دالة الضرب
def multiplication(a, b):
    return a * b

# دالة القسمة
def division(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

# دالة الاس والاساس
def Exponent(a, b):
    return a ** b

# دالة القسمة ثم الترجيع الى اي عدد صحيح
def Floor_Divide(a, b):
    return a // b

# دالة الحصول على اخر رقم عندما نقسم الرقمين
def Modulo_function(a, b):
    return a % b

# دالة اكبر من
def find_max(a, b):
    if a > b:
        return a
    else:
        return b
    
# دالة اصغر من
def find_min(a, b):
    if a < b:
        return a
    else:
        return b
    
# دالة حسب الارقام المشتركة
def AND(a, b):
    return a & b

# دالة حسب الارقام المشتركة وغير المشتركة
def OR(a, b):
    return a | b

# دالة حسب الارقام غير المشتركة
def XOR(a, b):
    return a ^ b

# دالة زيح الارقام من اخر اليسار الى اول اليمين
def Left_shift(a, b):
    return a << b

# دالة تزيح الارقام من اول اليمين الى اخر اليسار
def Right_shift	(a, b):
    return a >> b

# دالة حساب مساحة المربع
def Area_of_the_square(a, b):
    return a * b

# دالة حساب مساحة المثلث
def triangle_area(a, b):
    return 0.5 * a * b

# دالة حساب مساحة شبه المنحرف
def trapezoid_area(a, b, c):
    return 0.5 * (a + b) * c

#دالة حساب مساحة الدائرة
def circle_area(a):
    return 3.141592653589793 * a * a

# دالة حساب مساحة الخماسي
def pentagon_area(a):
    return (5 * a ** 2) / (4 * 0.726542528)

# دالة حساب مساحة السداسي
def hexagon_area(a):
    return (3 * (3 ** 0.5) * a ** 2) / 2

# دالة حساب مساحة السباعي
def heptagon_area(a):
    return (7 * a **2) / (4 * 0.48175)

# دالة حساب مساحة الثماني
def octagon_area(a):
    return 2 * (1 + 2**0.5) * a**2

# التساعي
def nonagon_area(side):
    return (9 * side**2) / (4 * 0.8391)

# العشاري
def decagon_area(side):
    return (5 * side**2) / (2 * 0.32492)

# مساحة المكعب
def cube_area(side):
    return 6 * side ** 2

# مساحة الهرم الرباعي
def pyramid_area(base_side, slant_height):
    base_area = base_side ** 2
    triangle_area = 0.5 * base_side * slant_height
    return base_area + 4 * triangle_area

# مساحة الهرم الخماسي
def pentagonal_pyramid_area(base_side, slant_height):
    base_area = (5 * base_side ** 2) / (4 * 0.726542528)
    lateral_area = 5 * (0.5 * base_side * slant_height)
    return base_area + lateral_area

# مساحة المخروط
def cone_total_area(radius, slant_height):
    lateral_area = 3.141592653589793 * radius * slant_height
    base_area = 3.141592653589793 * radius ** 2
    return lateral_area + base_area

# مساحة الكرة
def sphere_area(radius):
    return 4 * 3.141592653589793 * radius ** 2

# مساحة الأسطوانة
def cylinder_total_area(radius, height):
    lateral_area = 2 * 3.141592653589793 * radius * height
    base_area = 2 * 3.141592653589793 * radius ** 2
    return lateral_area + base_area

# التسلسلات الهندسية
def geometric_series_sum(a1, r, n):
    return a1 * (1 - r**n) / (1 - r) if r != 1 else a1 * n

# التسلسلات الهندسية
def arithmetic_series_sum(a1, an, n):
    return n * (a1 + an) / 2

# المسافة بين نقطتين
def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# التحقق اذا كان عددا اوليا
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# أعداد فيبوناتشي
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# نظرية فيثاغورس
def pythagorean_theorem(a=None, b=None, c=None):
    if c is None:
        return (a**2 + b**2)**0.5
    elif a is None:
        return (c**2 - b**2)**0.5
    else:
        return (c**2 - a**2)**0.5
    
# اشباه الجمل
def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

# رسم دالة خطي
def plot_function(f, x_min, x_max, width=50):
    for y in range(10, -11, -1):
        line = ""
        for x in range(x_min, x_max + 1):
            if abs(f(x) - y) < 0.5:
                line += "●"
            else:
                line += " "
        print(line)

# الجذور التربيعية
def sqrt(n):
    x = n
    while True:
        root = 0.5 * (x + n/x)
        if abs(root - x) < 1e-10:
            return root
        x = root

# دالة الاحتمال بالنسبة المئوية
def probability(favorable, total):
    return f"{round((favorable / total) * 100)}%"

# دالة التوزيع الاحتمالي المئوي
def probability_distribution(*outcomes):
    total = sum(outcomes)
    return [f"{round((x/total)*100)}%" for x in outcomes]

# دالة احتمالية العملة المعدنية
def coin_probability(heads, tails):
    total = heads + tails
    return f"رأس: {round((heads/total)*100)}%، ذيل: {round((tails/total)*100)}%"

# ضرب المصفوفات
def matrix_mult(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) 
             for j in range(len(B[0]))] for i in range(len(A))]


# رسم منحنى دالة
def plot(f, x_range=(-10, 10), width=60):
    for y in range(10, -11, -1):
        line = ['■' if abs(f(x/2) - y/2) < 0.25 else ' ' for x in range(*x_range)]
        print(''.join(line))

# خوارزمية إقليدس
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

# التحويل من عشري الى ثنائي
def decimal_to_binary(n):
    return bin(n)[2:] if n != 0 else '0'

# لتحويل من عشري إلى ستة عشري
def decimal_to_hex(n):
    hex_chars = "0123456789ABCDEF"
    result = []
    while n > 0:
        result.append(hex_chars[n % 16])
        n = n // 16
    return ''.join(reversed(result)) or '0'

# التحويل من ستة عشري إلى عشري
def hex_to_decimal(hex_str):
    hex_dict = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
                '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
    return sum(hex_dict[c] * 16**i for i, c in enumerate(reversed(hex_str.upper())))

# التحويل من عشري إلى ثماني
def decimal_to_octal(n):
    oct_digits = []
    while n > 0:
        oct_digits.append(str(n % 8))
        n = n // 8
    return ''.join(reversed(oct_digits)) or '0'

# التحويل من ثماني إلى عشري
def octal_to_decimal(oct_str):
    return sum(int(d) * 8**i for i, d in enumerate(reversed(oct_str)))

# تحويل عام بين أي نظامين (من 2 إلى 36)
def base_convert(number, from_base, to_base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # تحويل إلى عشري أولًا
    decimal = sum(digits.index(c) * from_base**i 
               for i, c in enumerate(reversed(str(number).upper())))
    # التحويل من عشري إلى النظام الهدف
    result = []
    while decimal > 0:
        result.append(digits[decimal % to_base])
        decimal = decimal // to_base
    return ''.join(reversed(result)) or '0'


# دوال رياضية متقدمة
def cube_root(n, precision=0.0001):
    guess = n
    while True:
        new_guess = (2 * guess + n / (guess * guess)) / 3
        if abs(new_guess - guess) < precision:
            return new_guess
        guess = new_guess

def natural_log(x, precision=0.0001):
    if x <= 0:
        return float('-inf')
    result = 0.0
    term = (x - 1) / (x + 1)
    i = 1
    while True:
        current_term = term ** (2 * i - 1) / (2 * i - 1)
        if abs(current_term) < precision:
            break
        result += 2 * current_term
        i += 1
    return result

# دوال هندسية متقدمة
def ellipse_area(a, b):
    return 3.14159 * a * b

def torus_volume(R, r):
    return 2 * 3.14159**2 * R * r**2

# دوال نظرية الأعداد المتقدمة
def euler_phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n = n // p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def divisor_sigma(n, k=1):
    total = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            count = 0
            while n % p == 0:
                n //= p
                count += 1
            total *= (p**(k*(count+1))-1)//(p**k-1)
        p += 1
    if n > 1:
        total *= (n**(k*(1+1))-1)//(n**k-1)
    return total

# دوال المعادلات التفاضلية
def euler_method(f, x0, y0, h, x_end):
    x = [x0]
    y = [y0]
    while x[-1] < x_end:
        y_new = y[-1] + h * f(x[-1], y[-1])
        x_new = x[-1] + h
        x.append(x_new)
        y.append(y_new)
    return x, y

# دوال التحليل العددي
def bisection_method(f, a, b, tol=1e-6):
    if f(a) * f(b) >= 0:
        raise ValueError("يجب أن تكون قيم الدالة عند النقطتين مختلفة الإشارة")
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
