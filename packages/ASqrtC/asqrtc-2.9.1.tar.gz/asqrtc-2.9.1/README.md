# Accurate-Sqrt-Calculator (ASqrtC)
ASqrtC is a fast and accurate square root calculator with no size limit.
It delivers exact results to any specified number of decimal places.
It is 100% accurate.
ASqrtC outperforms Python’s built-in math and decimal modules in speed when calculating less then ~7500 decimal places.

**How to Use**
1. Install the package using pip.
2. Import it in your script.
3. Call ASqrtC.sqrt(number, decimal_places) — replacing number with the value you want the square root of, and decimal_places with how many digits after the decimal you'd like.
4. That’s it! It’s that easy.

**If You Receive An Error Like:**

    ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits
    
**Then Add The Following Code to the Top of Your Project:**

    import sys
    sys.set_int_max_str_digits(0)

This removes Python’s built-in limit on large integer string conversions.


**Note: This project does not support negative, imaginary, or complex numbers.**
