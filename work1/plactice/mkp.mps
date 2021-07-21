NAME mkp
OBJSENSE MAX
ROWS
 N  OBJ
 L  Capacity(1)
 L  Capacity(2)
COLUMNS
    MARKER    'MARKER'                 'INTORG'
    x(1)      OBJ       16
    x(1)      Capacity(1)  2
    x(1)      Capacity(2)  3000
    x(2)      OBJ       19
    x(2)      Capacity(1)  3
    x(2)      Capacity(2)  3500
    x(3)      OBJ       23
    x(3)      Capacity(1)  4
    x(3)      Capacity(2)  5100
    x(4)      OBJ       28
    x(4)      Capacity(1)  5
    x(4)      Capacity(2)  7200
    MARKER    'MARKER'                 'INTEND'
RHS
    RHS1      Capacity(1)  7
    RHS1      Capacity(2)  10000
BOUNDS
 BV BND1      x(1)    
 BV BND1      x(2)    
 BV BND1      x(3)    
 BV BND1      x(4)    
ENDATA
