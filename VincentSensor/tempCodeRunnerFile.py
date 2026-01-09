import math
def int_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    return math.sqrt(mx**2+my**2)
print(int_margin(0,0,3,4))