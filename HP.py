from ti_draw import *
from ti_system import *
from random import *
from math import *

# Calculator state globals
x = 0            # the stack: x,y,z,t
y = 0
z = 0
t = 0
xs = ""           # String for entry to x register
second = False    # was last key press 2nd?
isDegrees = True  # Degrees or radians
menu = 0          # What menu are we doing
mem = 0           # A memory for sto, recall
lastEnter = False # Was the last key an "enter"? Need for correct display
errorUp = False   # Is there an error message up?

# Convert x to display string, set to 8 digits of precision
def format_number(n):
    # This seems to do what I want, strip off trailing 0s.
    nx = '{:.8g}'.format(n)
    return nx

# Convert xs to a number, watch for imcomplete numbers
def decode_number(s):
    global x
    # Display could be in binary or hex, after showing a number in that format
    try:
        if 'b' in s or 'B' in s:
            return int(s,2)
        elif 'x' in s or 'X' in s:
            return int(s,16)
        else:
            # Could be crazy stuff: 3.0e- or 3e
            if s.endswith("-"):
                s = s.rstrip("-")
            if s.endswith("e"):
                s = s.rstrip("e")
            # Should be a clean nubmer, use float to convert
            return float(s)
    except:
        disp_error("Number conversion error")
        x = 0
        return 0

def disp_error(s):
    global errorUp
    errorUp = True
    cdraw_text(10,20, "Error")
    cdraw_text(10,40,s)
    cdraw_text(10,60,"Press any key to clear")

def clear_error():
    global errorUp
    errorUp = False;
    clear_rect(0,0,320,80)

# Draw text after clearing the entire line first. Stops the flicker on screen redraw
def cdraw_text(x,y,s):
    clear_rect(0,y-19,320,15) ## CLR YYY ROW
    draw_text(x,y,s)

# Draw the stack on the display
def draw_stack():
    global x, y, z, t, xs

    # cdraw_text(2, 20,"draw_stack: xs is {}".format(xs))
    
    set_color(128,128,128)  # grey
    set_pen("thin", "dotted")

    draw_line(1,90, 320,90)
    draw_line(1,112, 320,112)
    draw_line(1,136, 320,136)
    draw_line(1,162, 320,162)

    set_color(0,0,0) # black pen
    set_pen("medium", "solid")
    cdraw_text(1,112, 'T:{:>29}'.format(format_number(t)))
    cdraw_text(1,136, 'Z:{:>29}'.format(format_number(z)))
    cdraw_text(1,162, 'Y:{:>29}'.format(format_number(y)))
    if len(xs) == 0:
        cdraw_text(1,188, 'X:{:>29}'.format(format_number(x)))
    else:
        cdraw_text(1,188, 'X:{:>29}'.format(xs))

# Draw the menus on the bottom of the screen, takes a properly formatted string
def draw_menu(menus):
    # background color
    set_color(192,192,255) # light blue
    fill_rect(0,190,320,210)

    # Menu banner
    set_color(0,0,0)
    draw_text(2,211,menus)

    # borders on banner
    set_pen("medium", "solid")
    draw_line(1,190,320,190)
    draw_line(64, 190, 64,210)
    draw_line(128, 190, 128,210)
    draw_line(192, 190, 192,210)
    draw_line(256, 190, 256,210)

    # Finally, draw the mode: Deg or Rad
    # Had to do a clear because cdraw wasn't clearing bottom of g in Deg
    clear_rect(290,0,30,20) 
    if isDegrees:
        cdraw_text(290, 20, "Deg")
    else:
        cdraw_text(290, 20, "Rad")
        

# Menu on the bottom of the screen, which has sub-menus
def do_menu(key):
    global menu
    
    if menu == 0:
        menu = key
        if key == 11:
            draw_menu("DROP    DUP   R^    Rv     SWAP")
        elif key == 12:
            draw_menu("RND    FRAC   TRUNC")
        elif key == 13:
            draw_menu("AND    OR     NAND  NOR    NOT ")
        elif key == 14:
            draw_menu("DEC    BIN    HEX")
        elif key == 15:
            draw_menu("DEG    RAD")
    else:
        if menu == 11:
            do_stack(key)
        elif menu == 12:
            do_round(key)
        elif menu == 13:
            do_bool(key)
        elif menu == 14:
            do_base(key)
        elif menu == 15:
            do_deg(key)
        # When done, go back to old menu
        menu = 0
        draw_menu("STACK  ROUND  BOOL  BASE   DEG")

# User has keyed a digit or . or EE. Add to x display string
def add_digit(ds):
    global x, y, t, z, xs, lastEnter

    # ignore extra decimal places
    if ds == "." and xs.count(".") > 0:
        return
    # No . if we are in the exponent...
    if ds == "." and xs.find("e") >= 0:
        return
        
    # If x is a result, we need to push it
    if len(xs) == 0 and x != 0 and lastEnter == False:
        t = z
        z = y
        y = x
    
    xs += ds
    #cdraw_text(2, 40,"add_digit: called with ds {}".format(ds))    
    x = decode_number(xs)

# Delete key: remove the last char typed
def do_delete():
    global x, xs
    if len(xs) > 0:
        xs = xs[:-1]  
    x = decode_number(xs)

# Change sign key
def chs():
    global xs,x
    eindex = xs.find("e")

    if len(xs) < 1:
        xs = format_number(x)

    # if no exponent, just prepend -
    if eindex < 0:
        if xs.startswith("-"):
            xs = xs.lstrip("-")
        else:
            xs = "-" + xs
        x = -x
    else:
        # We saw an exponent, so like 3e4
        pieces = xs.split("e")
        if pieces[1].startswith("-"):
            xs = pieces[0] + "e" + pieces[1].lstrip("-")
        else:
            xs = pieces[0] + "e-" + pieces[1]
    draw_stack()


# The EE exponent key
def doee():
    global xs
    # Ignore if added again
    if xs.find("e") != -1:
        return
    if len(xs) < 1:
        return
    xs = xs + "e"
    draw_stack()

# User hit enter
def enter():
    global x, y, t, z, xs
    t = z
    z = y
    y = x
    xs = ""
    draw_stack()

# Clear key
def do_clear():
    global x, y, z, t, xs, second
    # 2nd key does clear all
    if second:
        t = 0
        z = 0
        y = 0
    x = 0
    xs = ""
    draw_stack()

# Clean up after an operation on x and y
def after_double_op():
    global y, t, z, xs
    y = z
    z = t
    xs = ""
    draw_stack()

# Clean up after an operation on x
def after_single_op():
    global xs
    xs = ""
    draw_stack()

# Hand the submenu keys for the STACK commands
def do_stack(key):
    global x,y,z,t,xs

    # In case we were mid-entry, grab value
    if len(xs) > 0:
        x = decode_number(xs)
    
    if key == 11:    # drop
        x = y
        y = z
        z = t
    elif key == 12:  # dup
        t = z
        z = y
        y = x
    elif key == 13:  # roll up
        r = t # save off...
        t = z
        z = y
        y = x
        x = r
    elif key == 14:  # roll down
        r = t # save off...
        t = x
        x = y
        y = z
        z = r
    elif key == 15:  # swap
        r = x # save off...
        x = y
        y = r

    xs = ""
    draw_stack()

# Handle the submenu keys for ROUND
def do_round(key):
    global x,xs

    # In case we were mid-entry, grab value
    if len(xs) > 0:
        x = decode_number(xs)
    
    if key == 11:    # round
        x = round(x)
    elif key == 12:  # frac
        x = x - int(x)
    elif key == 13:  # trunc
        x = trunc(x)
    xs = ""
    draw_stack()

# Handle the submenu keys for DEG
def do_deg(key):
    global isDegrees
    if key == 11:
        isDegrees = True
    else:
        isDegrees = False


# Hand the submenu keys for BOOL
def do_bool(key):
    global x, y, xs

    # In case we were mid-entry, grab value
    if len(xs) > 0:
        x = decode_number(xs)

    ix = int(x)
    iy = int(y)
    
    if key == 11:    # and
        x = ix & iy
        after_double_op()
    elif key == 12:  # or
        x = ix | iy
        after_double_op()
    elif key == 13:  # nand
        x = ~(ix & iy)
        after_double_op()
    elif key == 14:  # nor
        x = ~(ix | iy)
        after_double_op()
    elif key == 15:  # not
        x = ~ix
        after_single_op()
    xs = ""
    draw_stack()
    
# Handle the submenu keys for BASE
def do_base(key):
    global x, xs
    
    # In case we were mid-entry, grab value
    if len(xs) > 0:
        x = decode_number(xs)

    ix = int(x)
    
    if key == 11:    # dec
        xs = format_number(x)
    elif key == 12:  # bin
        xs = bin(int(x))
    elif key == 13:  # hex
        xs = hex(int(x))
    draw_stack() 

# Add key
def add():
    global x, y
    x = x + y
    after_double_op()

# subtract key
def sub():
    global x, y
    x = y - x
    after_double_op()

# multiply key
def mul():
    global x, y, t, z, xs, second
    if second:
        t = z
        z = y
        y = x
        x = e     # math.e
        xs = ""
        draw_stack()
    else:
        x = x * y
        after_double_op()

# Divide key
def div():
    global x, y, t, z, xs, second
    if second:
        t = z
        z = y
        y = x
        x = pi
        xs = ""
        draw_stack()
    else:
        try:
            x = y / x
        except:
            disp_error("Divide by zero error")
            return
        after_double_op()

# Sqr key, does sqrt too
def dosqr():
    global x, second
    if second:
        try:
            x = sqrt(x)
        except:
            disp_error("Negative sqrt ignored")
            return
    else:
        x = x * x
    after_single_op()

# Root key, does power too
def doroot():
    global x,y,second
    try:
        if second:
            x = pow(x, 1.0/y)
        else:
            x = pow(x, y)
    except:
        disp_error("Negative root ignored")
        return
    after_double_op()

# log key, does e^x too
def doetox():
    global x, second
    try:
        if second:
            x = pow(e, x)
        else:
            x = log(x) # Log is ln
    except:
        disp_error("Log out of domain")
        return
    after_single_op()
    
# log10 key, does 10^x too
def dotenx():
    global x,second
    try:
        if second:
            x = pow(10.0, x)
        else:
            x = log10(x)
    except:
        disp_error("Log out of domain")
        return
    after_single_op()

# STO and RCL for one memory.
def domem():
    global second, x, mem
    global y, t, z, xs
    if second:
        # recall
        t = z
        z = y
        y = x
        xs = ""
        x = mem
        xs = format_number(x)
    else:
        # store
        mem = x
    draw_stack

# sin key, does asin too
def dosin():
    global x, isDegrees, second
    try:
        if second:
            if isDegrees:
                x = degrees(asin(x))
            else:
                x = asin(x)
        else:
            if isDegrees:
                x = sin(radians(x))
            else:
                x = sin(x)
    except:
        disp_error("Illegal value for sin/asin")
        return
    after_single_op()

# cos key, does acos too
def docos():
    global x, isDegrees, second
    try:
        if second:
            if isDegrees:
                x = degrees(acos(x))
            else:
                x = acos(x)
        else:
            if isDegrees:
                x = cos(radians(x))
            else:
                x = cos(x)
    except:
        disp_error("Illegal value for cos/acos")
        return
    after_single_op()

# tan key, does atan too
def dotan():
    global x, isDegrees, second
    try:
        if second:
            if isDegrees:
                x = degrees(atan(x))
            else:
                x = atan(x)
        else:
            if isDegrees:
                x = tan(radians(x))
            else:
                x = tan(x)
    except:
        disp_error("Illegal value for tan/atan")
        return
       
    after_single_op()

# Master key processing handler. A giant if/then/else tree
def process_key(key):
    global second, lastEnter

    #cdraw_text(10,40,"process key {}".format(key))
    # The 2nd key, need to trap first
    if key == 21:
        second = True
        return

    # Row 1 : Menus
    if key == 11:
        stackmenu()  
    elif key == 12:
        roundmenu()  
    elif key == 13:
        boolmenu()  
    elif key == 14:
        basemenu()  
    elif key == 15:
        degreemenu()  

    # Row 2
    elif key == 23:
        do_delete()
    
    # Row 4
    elif key == 45:
        do_clear()

    # Row 5
    elif key == 51:
        doroot()
    elif key == 52:
        dosin()
    elif key == 53:
        docos()
    elif key == 54:
        dotan()
    elif key == 55:
        div()

    # Row 6
    elif key == 61:  # x^2
        dosqr()
    elif key == 62:  # EE Key
        doee()
    elif key == 65:  # * key
        mul()

    # Row 7
    elif key == 71:  # 10^x
        dotenx()
    elif key == 72:
        add_digit("7")
    elif key == 73:
        add_digit("8")
    elif key == 74:
        add_digit("9")
    elif key == 75:
        sub()

    # Row 8
    elif key == 81:  # e^x
        doetox()
    elif key == 82:
        add_digit("4")
    elif key == 83:
        add_digit("5")
    elif key == 84:
        add_digit("6")
    elif key == 85:
        add()

    # Row 9
    elif key == 91:  # sto/rcl
        domem()
    elif key == 92:
        add_digit("1")
    elif key == 93:
        add_digit("2")
    elif key == 94:
        add_digit("3")
        
    elif key == 102:
        add_digit("0")
    elif key == 103:
        add_digit(".")
    elif key == 104:  # (-) key
        chs()
    elif key == 105:  # enter key
        enter()

    # Set the lastEnter flag to help handle how X is displayed after Enter pressed
    if key == 105:
        lastEnter = True
    else:
        lastEnter = False
        
    # Clear second flag after it is handled
    second = False

##    
## MAIN loop of this program
##
draw_menu("STACK  ROUND  BOOL  BASE   DEG")
while True:
    draw_stack()
    key = wait_key()

    if errorUp:
        clear_error()
        continue

    # Look for menu key
    if key <= 15:
        do_menu(key)
        continue
    else:
        menu = 0
    
    # exit on quit or Home. Note, I can't catch Home, but I tried :)
    if key == 22 or key == 101:
        break;

    process_key(key)
    
 
