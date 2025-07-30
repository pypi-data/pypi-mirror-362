import sys
import numpy as np

sys.path.insert(0, '../src/FinToolsAP/')

import Bond



def main():
    b = Bond.Bond(yild = 0.03, tenor = 3, principal = 100, compounding = 1, coupon_rate = 0.04)
    
    b1 = Bond.Bond(yild = 0.03, tenor = 1)
    print(b1)
    print(b1.price)

    



if __name__ == "__main__":
    main()