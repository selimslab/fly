import logging
from typing import Dict, List, Optional, Set
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as plticker


class TargetPlotter:    
    def plot_targets(self, df: pd.DataFrame):
        print(f"there are {len(df)} targets")

        print(df.head())
        try:
            ax = sns.scatterplot(x='latitude', y='longitude', data=df, hue='icao_address')

            ax.xaxis.set_major_locator(self._get_axis_interval())
            ax.yaxis.set_major_locator(self._get_axis_interval())
            # plt.close("all")
            plt.show()


        except Exception as e:
            logging.info(f"error plotting targets: {e}")
            pass  
    
    @staticmethod
    def _get_axis_interval(resolution = 1):
        return plticker.MultipleLocator(base=resolution) # this locator puts ticks at regular intervals
