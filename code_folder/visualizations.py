
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Standard data manipulation packages
import pandas as pd
import numpy as np

# System and Image manipulation packages
import PIL
from PIL import Image


def another(vc_obj, column_text, caption_txt, file_name):

    tb_styles = {'selector': 'table',
            'props':[( 'width', '100%')]}

    th_styles={'selector': 'th',
               'props': [('border', "1"),
                         ("border-color", "black"),
                         ('border-style','solid'),
                         ('border-width','1px'),
                         ('font-family', 'verdana'),
                         ('white-space', 'nowrap'),
                         ('width', '75%'),
                         ("text-align", "left")]
              }



    td_styles = {'selector': 'td',
                 'props': [('font-family', 'verdana'),
                           ('border', "1"),
                           ("border-color", "black"),
                           ('border-style','solid'),
                           ('border-width','1px'),
                           ('white-space', 'nowrap'),
                           ('padding-right',"10px"),
                          ('padding',"10px")]
                }

    cap_style = {'selector':'caption',
                'props':[('font-family', 'verdana'),
                         ('white-space', 'nowrap'),
                        ("font-size", "large")]}


    type(file_name)
    test_df =vc_obj.to_frame()
    test_df.columns = [column_text]
    
    improved =test_df.style.set_table_attributes('style="border-collapse:collapse"')\
                     .set_table_styles([tb_styles, th_styles,td_styles,cap_style]).set_caption(caption_txt)
    html = improved.render()
    path = './images/'+file_name+'.png'
    print(path)
    imgkit.from_string(html, path)

    with Image(filename=path) as img:
        img.trim(Color("WHITE"))
        img.save(filename=path)
    