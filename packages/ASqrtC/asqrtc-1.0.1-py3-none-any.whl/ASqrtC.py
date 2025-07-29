__author__='Sebastian Trumbore'
__author_email__='Trumbore.Sebastian@gmail.com'


def sqrt(number, decimal_length=2):
    try:
        float(number)
        if number < 0:
            print("\033[0;31m" + ">> Error, invalid number; number must be positive.")
            return ""
        i = 0
        j = 0
        broken_number = []
        if len(str(number)) % 2 == 1 and "." not in str(number):
            broken_number.append(str(number)[i])
            i += 1
        elif len(str(number)) % 2 == 0 and "." in str(number):
            broken_number.append(str(number)[i])
            i += 1
        j = int(-(- (len(str(number)) - i / 2) // 1))
        for counter in range(int(j)):
            if not len(str(number)) < i + 1:
                if "." in str(number)[i] + str(number)[i + 1]:
                    broken_number.append(
                        str(number)[i] + str(number)[i + 1] + str(number)[i + 2]
                    )
                    i += 3
                else:
                    broken_number.append(str(number)[i] + str(number)[i + 1])
                    i += 2
        q = ""
        q2 = 0
        number = ""
        d_placement = len(broken_number)
        for counter in range(len(broken_number) + int(decimal_length)):
            if number == 0 and counter > len(broken_number):
                pass
            else:
                if counter >= len(broken_number):
                    number *= 100
                else:
                    number = round(int(str(number) + broken_number[counter]))
                I = 0
                while int(str(q2) + str(I)) * int(I) <= int(number):
                    I += 1
                I -= 1
                number -= int(str(q2) + str(I)) * int(I)
                q2 = int(q2) * 10 + int(I) * 2
                q = str(q) + str(I)
        answer = str(q[:d_placement:]) + "." + str(q[d_placement::])
        return answer
    except:
        print("\033[0;31m" + ">> Error, invalid number")
        return ""
