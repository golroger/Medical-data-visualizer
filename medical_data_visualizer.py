import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def fun(x):
    if x == 1 :
        return 0
    elif x > 1 :
        return 1
      
# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df["IBM"] = df["weight"] / (df["height"]/100)**2
df["overweight"] =1
df["overweight"].where(df["IBM"] > 25 , 0,True )

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["gluc"]=df["gluc"].apply(fun) 
df["cholesterol"] = df["cholesterol"].apply(fun)

# Draw Categorical Plot
def draw_cat_plot():
  
  df_plot = df.iloc[: , 7 :]
  

  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  
  df_cat =  pd.melt(df_plot , id_vars= "cardio" , value_vars=  ["active","alco","cholesterol","gluc","overweight","smoke"])
  
  # Draw the catplot with 'sns.catplot()'
  cat_plot = sns.catplot(data=df_cat, x="variable" , col="cardio", hue="value", kind= "count")
  cat_plot.set_ylabels("total")
  # Get the figure for the output
 
  fig= cat_plot.fig
  
  # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heat_map():
  # Clean the data
  df_heat=df[(df['ap_lo'] <= df['ap_hi'])]
  df_heat = df_heat[(df_heat['height'] >= df_heat['height'].quantile(0.025))]
  df_heat = df_heat[(df_heat['height'] <= df_heat['height'].quantile(0.975))]
  df_heat = df_heat[(df_heat['weight'] <= df_heat['weight'].quantile(0.975))]
  df_heat = df_heat[(df_heat['weight'] >= df_heat['weight'].quantile(0.025))]
  df_heat=df_heat.drop(columns="IBM")
  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.triu(np.ones_like(corr))

  # Set up the matplotlib figure
  fig, ax =  plt.subplots()

  # Draw the heatmap with 'sns.heatmap()'
  ax= sns.heatmap(data=corr,mask=mask, annot=True,fmt=".1f", center =0, vmax =0.3 , vmin =-0.16,cbar_kws={"shrink": 0.5, 'ticks': [-0.08, 0.00, 0.08, 0.16, 0.24]})
  # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig
