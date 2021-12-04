import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RangeSlider, Button
import numpy as np
import math
import time
import os

def main():
    ### PRINT THE MAINPAGE ###

    clearConsole()
    print("""
        ###################################################
        ###                                             ###
        ###            GRAPH OF THE EQUATION            ###
        ###              y + zi = (base)^x              ###
        ###                                             ###
        ###---------------------------------------------###
        ###                                             ###
        ###                          z                  ###
        ###      [1] RUN             |   .              ###
        ###                       .  |.    . .          ###
        ###      [2] ABOUT           |  .   .           ###
        ###                        . |_________ x       ###
        ###      [3] EXIT           /  .   .            ###
        ###                        /  .  .              ###
        ###                       y                     ###
        ###                                version: 1.0 ###
        ###################################################\n\n""")
    mainpage_input = input()
    clearConsole()


    ### EVALUATE THE INPUT ###

    if mainpage_input == "1":
        run()
        
    elif mainpage_input == "2":
        print("""
        ###################################################
        ###                                             ###
        ###   Due to lack of free 3D graphing software  ###
        ###   that can use complex numbers, a program   ###
        ###   like this was necessary, in order to      ###
        ###   extinguish my ignited curiosity.          ###
        ###   This program was written using            ###
        ###   python 3.9.1, matplotlib 3.5.0 and        ###
        ###   numpy 1.20.2 to plot the graph of         ###
        ###   the equation y + zi = (base)^x            ###
        ###   with negative bases.                      ### 
        ###                                             ###    
        ###                            -Onurcan Okay    ###
        ###     [1] BACK                 4/12/2021      ###    
        ###     [2] EXIT                                ###
        ###                                version: 1.0 ###
        ###################################################\n\n""")
        page_input = input()
        clearConsole()
        if page_input == "1":
            main()
        elif page_input == "2":
            quit()
        else:
            print("UNKNOWN COMMAND!\n\nEXITTING PROGRAM.")
            time.sleep(2)
            quit()
        
    elif mainpage_input == "3":
        quit()
    
    elif mainpage_input == "31":
        # Funny easter egg
        print("\nhehehehehe XD")
        time.sleep(3.1)
        main()
    
    else:
        print("UNKNOWN COMMAND!\n\nEXITTING PROGRAM...")
        time.sleep(2)
        quit()


def run():
    """
    Run the plotting code.
    """

    ### INITIALIZE PLOT ###

    init_base = -2 # Initial base of the graph
    init_x_intrvl = (-5,5) # Initial x inter of the graph
    xs = create_xs(init_x_intrvl) # Initial x values
    
    # Assign y and z values using the f function
    ys, zs = f(init_base, xs)

    # Create a figure and 3D axis
    fig = plt.figure()
    fig.suptitle(f"$y + zi = ({init_base:.2f})^x$")
    ax = plt.axes(projection='3d', proj_type = 'ortho')
    ax.set_box_aspect((1, 1, 1))
    
    # Plot the initial x, y, z values
    line, = ax.plot(xs, ys, zs)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")

    # Set y and z limits    
    abs_max = findAbsMax(line.get_data_3d()[1], line.get_data_3d()[2])
    ax.set_ylim((-abs_max, abs_max))
    ax.set_zlim((-abs_max, abs_max))

    
    ### ADD WIDGETS ###

    # Add Slider for changing the base
    def updateBase(val):
        """
        Update the base of the plot when base changed.
        
        Args:
            val (float): the new base of the graph
        """
        # Plot the new graph
        xs = create_xs(x_interval.val)
        res = f(val, xs)
        line.set_data_3d(xs, res[0], res[1])
        
        # Format the plot accordingly to the new base
        fig.suptitle(f"$y + zi = ({val:.2f})^x$")
        abs_max = findAbsMax(line.get_data_3d()[1], line.get_data_3d()[2])
        ax.set_ylim((-abs_max, abs_max))
        ax.set_zlim((-abs_max, abs_max))

    base_slider = Slider(
        ax=plt.axes((0.3,0.05,0.5,0.02)),
        label="base",
        valmin=-5,
        valmax=5,
        valinit=init_base,
        valstep=0.05,
        initcolor='none')
    
    base_slider.on_changed(updateBase)


    # Add RangeSlider for changing the interval of x
    def updateInterval(val):
        """
        Update the interval of x when x_interval changed.
        
        Args:
            val: iterable of length 2, contains the endpoints of the interval

        Returns:
            xs: iterable containing the x values for the interval
        """
        xs = create_xs(val)
        res = f(base_slider.val, xs)
        line.set_data_3d(xs, res[0], res[1])
        ax.set_xlim(val)

        # Set y and z limits
        abs_max = findAbsMax(line.get_data_3d()[1], line.get_data_3d()[2])
        ax.set_ylim((-abs_max, abs_max))
        ax.set_zlim((-abs_max, abs_max))
        return xs

    x_interval = RangeSlider(
        ax=plt.axes((0.3,0.02,0.5,0.02)),
        label="x interval",
        valmin=-20,
        valmax=20,
        valinit=(-5, 5))
    x_interval.on_changed(updateInterval)

    # Add Buttons for different views angles
    def updateView(plane):
        """
        Update the view (camera position) for the graph.

        Args:
            plane (str): "xy" or "xz" or "yz"
        """
        if plane == "xy":
            ax.view_init(elev=90,azim=-90)
        elif plane == "xz":
            ax.view_init(elev=0,azim=-90)
        elif plane == "yz":
            ax.view_init(elev=0,azim=0)

    def updateViewXY(btn_rls):
        updateView("xy")
    def updateViewXZ(btn_rls):
        updateView("xz")
    def updateViewYZ(btn_rls):
        updateView("yz")

    xy_button = Button(
        ax=plt.axes((0.05,0.9,0.18,0.05)),
        label="xy plane view"
    )
    xy_button.on_clicked(updateViewXY)

    xz_button = Button(
        ax=plt.axes((0.05,0.8,0.18,0.05)),
        label="xz plane view"
    )
    xz_button.on_clicked(updateViewXZ)

    yz_button = Button(
        ax=plt.axes((0.05,0.7,0.18,0.05)),
        label="yz plane view"
    )
    yz_button.on_clicked(updateViewYZ)
    

    plt.show()

def f(base, x_values):
    """
    Return the y_values and z_values for the equation
    y_values + z_values*j = (base)**x_values

    Args:
        x_values (numpy.ndarray)
        base (float)

    Returns:
        A list containing y_values and z_values

        [y_values (numpy.ndarray),
         z_values (numpy.ndarray)]
    """
    cmplx_res = (base + 0j)**x_values
    y_value = cmplx_res.real
    z_value = cmplx_res.imag

    return [y_value, z_value]

def create_xs(interval):
    """
    Create xs on a given interval.
    
    Args:
        interval: iterable containing endpoints
    
    Return:
        xs (numpy.ndarray)
    """
    interval_length = interval[1] - interval[0]
    point_density = pointDenstiy(interval)
    # np.logspace is used here instead of np.linspace or np.arange because resulting plots were less pointy
    # x values are created by manupilating np.logspace values to fit to the interval of x
    res = interval[1] + 1 - np.logspace(
        start=0, 
        stop=math.log(interval_length + 1), 
        num=point_density, 
        base=math.e)
    return res

def pointDenstiy(interval):
    """
    Return the calculated point_density for a given interval.

    Args:
        interval (tuple): (float, float)
    
    Returns:
        plot_density (int)
    """
    diff = interval[1] - interval[0]
    res = int(diff * 100)
    return res

def findAbsMax(arr0, arr1):
    """
    Return the absolute maximum value in two np.ndarrays
    """
    abs_max_00 = abs(arr0.max())
    abs_max_01 = abs(arr0.min())
    abs_max_0 = max(abs_max_00, abs_max_01)
    abs_max_10 = abs(arr1.max())
    abs_max_11 = abs(arr1.min())
    abs_max_1 = max(abs_max_10, abs_max_11)
    abs_max = max(abs_max_0,abs_max_1)
    return abs_max

def clearConsole():
    """Clear the console"""
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

if __name__ == "__main__":
    main()