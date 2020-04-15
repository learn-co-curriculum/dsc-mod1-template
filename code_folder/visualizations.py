# visualization packages
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

import seaborn as sns

from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

# Standard data manipulation packages
import pandas as pd
import numpy as np

# Is a python wrapper for wkhtmltoimage. would need to install wkhtmltoimage to have it work locally 
# Note - I've only seen this work on Macs, there is some trouble getting it to work with PCs
import imgkit

# Image manipulation packages. PIL stands for Pillow. you need to `pip install Pillow`
import PIL
from PIL import Image, ImageOps


""" The css works with the pandas.dataframe.style object to data summaries be formatted nicely"""


# Css for table style
tb_styles = {'selector': 'table',
            'props':[('margin','0')]}

# Css for table headers
th_styles = {'selector': 'th', 
             'props': [('border', "1"),
                     ("border-color", "black"),
                     ('border-style','solid'),
                     ('border-width','1px'),
                     ('font-family', 'verdana'),
                     ('white-space', 'nowrap'),
                       ('width', '75%'),
                     ("text-align", "left")]}

# Css for data rows
td_styles = {'selector': 'td',
             'props': [('font-family', 'verdana'),
                       ('border', "1"),
                       ("border-color", "black"),
                       ('border-style','solid'),
                       ('border-width','1px'),
                       ('white-space', 'nowrap'),
                       ('padding-right',"10px"),
                       ('padding',"10px")]}

# Css for table title
cap_style = {'selector':'caption',
             'props':[('font-family', 'verdana'),
                      ('white-space', 'nowrap'),
                      ("font-size", "large")]}

options = {'quiet': ''}



def value_counts_table(vc_obj, caption_txt, file_name):
    """This function:
        - takes a pd.Series output from value_counts() and converts it to a pd.DataFrame
        - formats the css and html to make it look nice
        - renders the html
        - converts the html to a PNG file
        - crops the image
        - saves the updated image file
        
        
        Parameters
        ----------
        vc_obj : series
            Output from a summary table created by using value_counts()
        caption_txt : string
            Title of table
        file_name : string
            what you want the file to be named
        
        Returns
        -------
        file_name.png : saves image of converted value_counts output"""    
        
    # Takes a pd.Series output from value_counts() and converts it to a pd.DataFrame        
    test_df =vc_obj.to_frame()        
    test_df.columns = ["count"]

    # Formats the css and html to make it look nice
    improved = test_df.style.format('{:,.0f}').set_table_attributes('style="border-collapse:collapse"')\
                     .set_table_styles([tb_styles, th_styles,td_styles,cap_style]).set_caption(caption_txt)
    # Renders the html
    html = improved.render()

    # Renders the html & saves as image
    path = './images/'+file_name+'.png'
    imgkit.from_string(html, path, options=options)

    # Crops the image
    
    ## PIL opens image
    im = Image.open(path)
    
    ## Inverts the colors of the image, because getbbox looks for black boundaries, not white ones
    inverted = ImageOps.invert(im.convert('RGB'))
    
    ## Get the automated boundaries box from the inverted file
    boxed = inverted.getbbox()
    
    ## Slaps those crop boundaries on the orginal image
    cropped_image=im.crop(boxed)

    # BAM, saves the cropped image file over the orignal
    cropped_image.save(path)
    pass




""" Setting parameters for matplotlib outside of the function, since I will reuse them multiple times
    It's also something I can quickly copy and paste from one script to another, personal preference"""

# Set specific parameters for the visualizations
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'xtick.minor.bottom':True,
          'ytick.labelsize': med,
          'figure.titlesize': large}



# Set style parameters
sns.set_style("ticks", { 'axes.spines.top': False, 'axes.spines.right': False, "xtick.major.size": med, "xtick.minor.size": 8, 'axes.titlesize': large, 'ytick.labelsize': med})
plt.rcParams.update(params)

def time_series_plot(dataset,title,xlab,ylab,file_name):
        """This function:
        - takes a pd.Series output from value_counts() and converts it to a pd.DataFrame
        - formats the css and html to make it look nice
        - renders the html
        - converts the html to a PNG file
        - crops the image
        - saves the updated image file
        
        
        Parameters
        ----------
        dataset : DataFrame
            Output from a summary table created by using value_counts()
        title : string
            Title on graph
        xlab : string
        ylab : string
        file_name : string
            what you want the image file to be named

        Returns
        -------
        file_name.png : saves image of matplotlib output""" 
    
    # assign argument values to variables
    file_name = file_name
    title = title
    xlab = xlab
    ylab = ylab
    data = dataset.copy()

    # Create figure container
    fig = plt.figure(figsize=(16, 10), dpi=80) 

    
    # Creates one subplot within our figure and uses the classes fig and ax
    fig, ax = plt.subplots(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')

    # Loops through species catagory and adds them to the plot
    for col_name in summed_df.columns.tolist():
        ax.plot(summed_df.index, col_name, data=data)

    # Format the ticks
    
    ## X Axis    
    ### Specify variables I want to use
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator(interval=3)  # every month
    years_fmt = mdates.DateFormatter('%b-%Y')
    mon_fmt = mdates.DateFormatter('%b')

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_minor_formatter(mon_fmt)

    ## Y Axis format
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # Sets the limits of the x-axis: round to nearest years.
    datemin = np.datetime64(summed_df.index.min(), 'Y')
    datemax = np.datetime64(summed_df.index[-1], 'Y') + np.timedelta64(1, 'Y')
    ax.set_xlim(datemin, datemax)

    # Dynamically sets a bunch of labels
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.legend()

    # Specifies I want the grid for BOTH level of tick marks
    ax.grid(True, which="both")

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate(which='both')

    path = './images/'+file_name+'.png'
    plt.savefig(path)
    pass