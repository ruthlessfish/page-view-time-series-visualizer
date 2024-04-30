import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 parse_dates=['date'], 
                 index_col='date', 
                 header=0, 
                 names=['date', 'page_views'])

# Clean data
min_page_views = df['page_views'].quantile(0.025)
max_page_views = df['page_views'].quantile(0.975)
df = df[df['page_views'].between(min_page_views, max_page_views)]


def draw_line_plot():
    # Draw line plot
    start_date = df.index.min()
    end_date = df.index.max()
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot(ax=ax,
            title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019', 
            xlabel='Date', 
            ylabel='Page Views',
            color='red',
            legend=False)
    ax.set_xlim(start_date, end_date)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.strftime('%Y')
    df_bar['month'] = df_bar.index.strftime('%B').astype('category')
    df_bar['month'] = df_bar['month'].cat.set_categories(months, ordered=True)
    df_bar = df_bar.groupby(['year', 'month'], sort=False, observed=True)['page_views'].mean().reset_index()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.barplot(x='year', 
                y='page_views', 
                data=df_bar, 
                hue='month', 
                palette='tab20', 
                ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(nrows=1, 
                                   ncols=2, 
                                   figsize=((df_box['year'].max() - df_box['year'].min() + 1) * 2, 10))
 
    fig, (ax1, ax2) = plt.subplots(nrows=1, 
                                   ncols=2, 
                                   figsize=((df_box['year'].max() - df_box['year'].min() + 1) * 2, 10))

    sns.boxplot(x='year', 
                y='page_views', 
                data=df_box, 
                palette='tab10',
                ax=ax1)

    sns.boxplot(x='month', 
                y='page_views', 
                data=df_box, 
                palette='tab10',
                ax=ax2, 
                order=months)

    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    # fig.savefig('box_plot.png')
    return fig
