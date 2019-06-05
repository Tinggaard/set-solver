"""File to keep track of the different types of attributes, for the solver"""


ATR_COLOR_GREEN = 1
ATR_COLOR_PURPLE = 2
ATR_COLOR_RED = 3

ATR_FILL_STRIPED = 1
ATR_FILL_FULL = 2
ATR_FILL_EMPTY = 3

ATR_SHAPE_PEANUT = 1
ATR_SHAPE_PILL = 2
ATR_SHAPE_RHOMBUS = 3


def ATR_COLOR(val):
    if val == 1:
        return "green"
    elif val == 2:
        return "purple"
    elif val == 3:
        return "red"
    return

def ATR_FILL(val):
    if val == 1:
        return "striped"
    elif val == 2:
        return "full"
    elif val == 3:
        return "empty"
    return

def ATR_SHAPE(val):
    if val == 1:
        return "peanut"
    elif val == 2:
        return "pill"
    elif val == 3:
        return "rhombus"
    return