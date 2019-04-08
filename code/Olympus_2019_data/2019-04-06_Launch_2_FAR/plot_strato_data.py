"""Script to plot Altitude and Velociy of Stratologger data.

Raw and filtered altitude are shown. A Savitzky-Golay filter with window length
101 and polynomial order 2 is used. This corresponds to approximately five
seconds of flight data at Stratologger's 20Hz sampling rate. The window length
is chosen to smooth mach transition dips in the data, but not provide too much
filtering.

Author: Matthew Pauly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
import matplotlib.patches as mpatches
from scipy.signal import savgol_filter


def make_plot():
    df = pd.read_csv('dataOlympus2019-04-06.csv')
    time = df['Time']
    alt = df['Altitude']
    alt_filt = savgol_filter(alt, 101, 2)
    num_pts = len(time)
    vel = np.zeros(num_pts)
    for i in range(1, num_pts-1):
        vel[i] = (alt_filt[i+1] - alt_filt[i-1]) / (time[i+1] - time[i-1])

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax2.patch.set_alpha(0.0)  # necessary for mpld3 to work with twinx()

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Altitude (ft)')
    ax2.set_ylabel('Velocity (ft/s)')

    color1 = plt.cm.viridis(0)
    color2 = plt.cm.viridis(0.5)
    color3 = plt.cm.viridis(.9)

    ax1.plot(time, alt, color=color1, label='Raw Altitde')
    ax1.plot(time, alt_filt, color=color2, label='Filtered Altitde')
    ax2.plot(time[1:-1], vel[1:-1], color=color3, label='Velocity from Filtered')

    patch1 = mpatches.Patch(color=color1, label='Raw Altitde')
    patch2 = mpatches.Patch(color=color2, label='Filtered Altitde')
    patch3 = mpatches.Patch(color=color3, label='Velocity from Filtered')

    plt.legend(handles=[patch1, patch2, patch3])
    plt.title('Olympus 2019-04-06 Altitude and Velocity')
    plt.savefig('Olympus_2019-04-06_altitude_velocity.png')
    with open('figure.html', 'w') as f:
        mpld3.save_html(fig, f)
    plt.show()


if __name__ == '__main__':
    make_plot()
