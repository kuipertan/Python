
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

line2, = plt.plot([1,2,3,5,4],[5,2,4,3,0],linewidth=2.5, linestyle='-', label='Line 2')
line1, = plt.plot([1,2,3],[4,2,1],linewidth=2.5, linestyle='-', label='Line 1')
plt.legend(('Line2','Line1'), loc='best')
plt.show()
