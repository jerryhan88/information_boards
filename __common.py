MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
DOW = {
    MON: 'MON',
    TUE: 'TUE',
    WED: 'WED',
    THR: 'THR',
    FRI: 'FRI',
    SAT: 'SAT',
    SUN: 'SUN'
    }
WEEKENDS = [SAT, SUN]

# Singapore Public Holidays
HOLIDAYS2009 = [
            (2009, 1, 1),    # New Year's Day, Thursday, 1 January 2009
            (2009, 1, 26),    # Chinese New Year, Monday, 26 January 2009
            (2009, 1, 27),    # Chinese New Year, Tuesday, 27 January 2009
            (2009, 4, 10),    # Good Friday, Friday, 10 April 2009
            (2009, 5, 1),     # Labour Day, Friday, 1 May 2009
            (2009, 5, 9),     # Vesak Day, Saturday, 9 May 2009
            (2009, 8, 10),    # National Day, Sunday*, 9 August 2009
            (2009, 9, 21),    # Hari Raya Puasa, Sunday*, 20 September 2009
            (2009, 11, 16),   # Deepavali, Sunday*, 15 November 2009
            (2009, 11, 27),   # Hari Raya Haji, Friday, 27 November 2009
            (2009, 12, 25),   # Christmas Day, Friday, 25 December 2009
]
HOLIDAYS2010 = [
            (2010, 1, 1),  # New Year's Day, Friday, 1 January 2010
            (2010, 2, 16),  # Chinese New Year, Sunday*, 14 February 2010
            (2010, 2, 15),  # Chinese New Year, Monday, 15 February 2010
            (2010, 4, 2),  # Good Friday, Friday, 2 April 2010
            (2010, 5, 1),  # Labour Day, Saturday, 1 May 2010
            (2010, 5, 28),  # Vesak Day, Friday, 28 May 2010
            (2010, 8, 9),  # National Day, Monday, 9 August 2010
            (2010, 9, 10),  # Hari Raya Puasa, Friday, 10 September 2010
            (2010, 11, 5),  # Deepavali, Friday, 5 November 2010
            (2010, 11, 17),  # Hari Raya Haji, Wednesday, 17 November 2010
            (2010, 11, 17),  # Christmas Day, Saturday, 25 December 2010
]

HOURS = list(range(6, 24)) + [0, 1]
TERMINALS1 = ['T1', 'T2', 'T3', 'B', 'X']
TERMINALS2 = ['T1', 'T2', 'T3', 'T4', 'X']

#
_rgb = lambda r, g, b: (r / float(255), g / float(255), b / float(255))
clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    'yellow',
    _rgb(220, 220, 220),  # gray
    _rgb(255, 165, 0),  # orange
    'black'
)
mlists = (
    'o',  #    circle
    'v',  #    triangle_down
    '^',  #    triangle_up
    '<',  #    triangle_left
    '>',  #    triangle_right
    's',  #    square
    'p',  #    pentagon
    '*',  #    star
    '+',  #    plus
    'x',  #    x
    'D',  #    diamond
    'h',  #    hexagon1
    '1',  #    tri_down
    '2',  #    tri_up
    '3',  #    tri_left
    '4',  #    tri_right
    '8',  #    octagon
    'H',  #    hexagon2
    'd',  #    thin_diamond
    '|',  #    vline
    '_',  #    hline
    '.',  #    point
    ',',  #    pixel

    'D',  #    diamond
    '8',  #    octagon
    )

FIGSIZE = (8, 6)