import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def do_analysis(metrics):
    df = metrics
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])



    # Assuming df is your DataFrame
    # Group the data by 'TargetGroup' and 'Metric'
    grouped = df.groupby(['TargetGroup', 'Metric'])

    # Create a new figure with 4 subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    axs = axs.flatten()  # Flatten the array of subplots for easier indexing

    # Create a dictionary to map metrics to subplot indices
    metric_to_subplot = {
        'RequestCount': 0,
        'HealthyHostCount': 1,
        'UnHealthyHostCount': 2,
        'TargetResponseTime': 3
    }

    # Loop through each group and plot the data
    for (target_group, metric), group_data in grouped:
        ax = axs[metric_to_subplot[metric]]
        ax.plot(group_data['Timestamp'], group_data['Value'], label=f"{target_group}")

        # Add title and labels to each subplot
        ax.set_title(f'Metric: {metric}')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Value')
        ax.legend()

    # Format x-axis to show more data points
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # Set interval to 1 minutes
    plt.gcf().autofmt_xdate()  # Auto-rotate x-axis labels for better visibility



    # Save the plot as an image file + csv
    plt.tight_layout()
    plt.savefig('./data/metrics_plot.png')
    df.to_csv('./data/metrics.csv', index=False)