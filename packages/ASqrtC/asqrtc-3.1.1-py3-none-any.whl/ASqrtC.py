__author__='Sebastian Trumbore'
__author_email__='Trumbore.Sebastian@gmail.com'


def find_largest_I(q2, number_int):
    a = q2 * 10
    # Predict I Using Simple Estimation (Linear)
    I = (number_int // (a + 1))  # Prevent Division By 0
    if I > 9:
        I = 9

    # Check Downard First, Overshoot Is Unlikely
    while I > 0 and (a + I) * I > number_int:
        I -= 1

    # Insurance Upward Check (Max 1 Step)
    while I < 9 and (a + I + 1) * (I + 1) <= number_int:
        I += 1

    return I


def sqrt(number, decimal_length=2):
    # Check If Input Is Numeric
    if not isinstance(number, (int, float)):
        raise TypeError("Error: Input must be a number.")

    # Check For Negative Values
    if number < 0:
        raise ValueError("Error: Number must be non-negative.")

    # Sqrt Calculations
    i = 0
    j = 0
    broken_number = []

    number_str = str(int(number)) if "." not in str(number) else str(number)
    if len(number_str) % 2 == 1 and "." not in number_str:
        broken_number.append(number_str[i])
        i += 1
    elif len(number_str) % 2 == 0 and "." in number_str:
        broken_number.append(number_str[i])
        i += 1

    j = int(-(-(len(number_str) - i / 2) // 1))
    for counter in range(int(j)):
        if not len(number_str) < i + 1:
            if "." in number_str[i:i + 2]:
                broken_number.append(number_str[i:i + 3])
                i += 3
            else:
                broken_number.append(number_str[i:i + 2])
                i += 2

    q = ""
    q2 = 0
    number_int = 0
    d_placement = len(broken_number)

    for counter in range(len(broken_number) + int(decimal_length)):
        if number_int == 0 and counter > len(broken_number):
            pass
        else:
            if counter >= len(broken_number):
                number_int *= 100
            else:
                number_int = int(str(number_int) + broken_number[counter])

            I = find_largest_I(q2, number_int)
            number_int -= (q2 * 10 + I) * I
            q2 = int(q2) * 10 + I * 2
            q += str(I)

    answer = q[:d_placement] + "." + q[d_placement:]
    return answer
