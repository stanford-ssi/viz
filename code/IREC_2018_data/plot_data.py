"""Python script for plotting recorded data and producing the html code necessary to host a visualization of it on a webpage.
"""


import pickle
import matplotlib.pyplot as plt, mpld3
import numpy as np
from scipy.fftpack import fft


DATA_SENSORS = ['bmp', 'mma', 'bno', 'gps']
BNO_ACCEL = ['a_x', 'a_y', 'a_z']
BNO_GYRO = ['w_x', 'w_y', 'w_z']
MMA = ['mma_x', 'mma_y']


def load_data():
    """Load the data from the pickle file.

    Returns:
        A dictionary (indices: 0-4) of Pandas dataframes with data from each
        sensor.
    """
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


def vecnorm(*axes):
    """Takes the vector norm across any number of axes.

    Args:
        axes (list of arrays): the axes to find the norm of
    Returns:
        the vector norm as an array
    """
    vecsum = 0
    for axis in axes:
        vecsum += axis**2
    return np.sqrt(vecsum)


def plot_multi_axis(time, axes, labels=None, fname=None):
    """Plots a 3-axis set of data, with the three axes and an envelope.

    Args:
        time (array): time series to plot data against in seconds
        axes (list): the three axes to plot, pre-scaled to desired units
        labels (list): title, xlabel, ylabel, legend labels
        fname (str): name of the file to store the mpld3 html in
    """
    fig = plt.figure(figsize=(10, 6))
    if labels:
        for i in range(len(axes)):
            plt.plot(time, axes[i], label=labels[3][i])
        plt.plot(time, vecnorm(*axes), 'k', label=labels[3][len(axes)])
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        plt.legend(loc='upper left')
    else:
        for i in range(len(axes)):
            plt.plot(time, axes[i])
        plt.plot(time, vecnorm(axes), 'k')
    if fname:
        with open(fname, 'w') as f:
            mpld3.save_html(fig, f)


def skybass_sampling_rates(data):
    """Plots the sampling rates of the Skybass sensors.

    Creates html plots of the data.

    Args:
        data (list of dataframes): data for analysis
    """
    for i in range(4):
        fig = plt.figure()
    TODO: finish



def main():
    """Loads the data, and plots it for the BNO accel and gyro.
    """
    data = load_data()
    # BNO055 absolute orientation sensor
    bno_time = data[2].index / 1e6
    bno_accel_axes = [data[2][bno_str] / 9.8 for bno_str in BNO_ACCEL]
    plot_multi_axis(bno_time, bno_accel_axes,
                    labels=['BNO055 Acceleration',
                            'Time (s)', 'Acceleration (G)',
                            [*BNO_ACCEL, 'magnitude']],
                    fname='bno_accel.html')
    bno_gyro_axes = [data[2][bno_str] for bno_str in BNO_GYRO]
    plot_multi_axis(bno_time, bno_gyro_axes,
                    labels=['BNO055 Roll Rate',
                            'Time (s)', 'Roll Rate (deg/s)',
                            [*BNO_GYRO, 'magnitude']],
                    fname='bno_gyro.html')
    # MMA65XX high-range accelerometer
    mma_time = data[1].index / 1e6
    mma_axes = [data[1][mma_str] / 9.8 for mma_str in MMA]
    plot_multi_axis(mma_time, mma_axes,
                    labels=['MMA65XX High-Range Acceleration',
                            'Time (s)', 'Acceleration (G)',
                            [*MMA, 'magnitude']],
                    fname='mma.html')
    # skybass_sampling_rates(data)


if __name__ == '__main__':
    main()
