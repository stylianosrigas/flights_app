# import numpy as np
# import matplotlib.pyplot as plt
#
# x = np.arange(0, 5, 0.1);
# y = np.sin(x)
# plt.show(plt.plot(x, y))


"""
=========================
Simple animation examples
=========================

This example contains two animations. The first is a random walk plot. The
second is an image animation.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = plt.figure()
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([96, 170, 306, 116, 273, 103, 79, 121, 367])
my_xticks = ['23/11/2017 - 25/11/2017', '30/11/2017 - 02/12/2017', '07/12/2017 - 09/12/2017', '14/12/2017 - 16/12/2017', '21/12/2017 - 23/12/2017', '28/12/2017 - 30/12/2017', '04/01/2018 - 06/01/2018', '11/01/2018 - 13/01/2018', '18/01/2018 - 20/01/2018']
plt.xticks(x, my_xticks)
plt.title('Scrooge Travel')
plt.plot(x, y)
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)


# plt.show()
datess = []
dates = [['23/11/2017', '25/11/2017'], ['30/11/2017', '02/12/2017'], ['07/12/2017', '09/12/2017'], ['14/12/2017', '16/12/2017'], ['21/12/2017', '23/12/2017'], ['28/12/2017', '30/12/2017'], ['04/01/2018', '06/01/2018'], ['11/01/2018', '13/01/2018'], ['18/01/2018', '20/01/2018']]
for i in range(len(dates)):
    datess.append(i)
print datess
