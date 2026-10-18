HP RPN emulator for TI-Evo

This is python code to emulate an HP calculator on your TI-Evo. It uses the python engine to do math, so it may not give exactly the same results as your TI-Evo would.

The display starts up with the X, Y, Z, and T registers all set to 0. Along the bottom are the function keys menu, showing STACK, ROUND, BOOL, BASE, and DEG. You can enter an number by using the digit keys, then press Enter to push it onto the stack. Enter another number, then push '+' to add them. It supports the usual operations, including trig functions like sin, asin, etc. 

Use the function keys to get into sub-menus. The STACK menu gives you a submenu to operate on the stack and do things like DUP and SWAP. ROUND gives you an option of rounding, truncating, or getting the fractional part of a number. BOOL will do and, or, nand, nor, and not on the X and Y registers. BASE will show the X register in a different base, either hex or binary. Finally, DEG switches between degrees and radians - the program starts in degress.

Here are what the keys do (from top to bottom). Note that keys not mentioned, are not implemented.

```
Function keys : As mentioned above: STACK, ROUND, BOOL, BASE, and DEG

2nd           : Combines to do 2nd operation on key

quit          : Quits the program

del           : Deletes last character in X

clear         : Clears x

y^x           : y^x. 2nd does root

sin           : sin(x). 2nd does asin

cos           : cos(x). 2nd does acos

tan           : tan(x). 2nd does atan

/             : y divides x. 2nd does pi

x^2           : x^2. 2nd does sqrt

EE            : Exponent (enter 'e' in X display)

'*'           : multiply x * y. 2nd does e (2.7)

log           : log base 10. 2nd does 10^x

7-9           : digit keys

'-'           : y - x

ln            : natural log of x. 2nd does e^x

4-6           : digit keys

'+'           : x + y

sto           : sto number to memory. 2nd does recall

1-3           : digit keys

Home          : Exits program un-gracefully

0             : digit 0

.             : Enter decimal place in X

(-)           : Change sign of x, or in exponent. Ex: 2e-2

Enter

```


Source code is at: https://github.com/reesley/HP

Feel free to use it as you like
