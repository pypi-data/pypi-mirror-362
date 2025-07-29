import pandas as pd
import matplotlib.pyplot as plt

def generate_report(log_file="usage_log.csv"):
    df = pd.read_csv(log_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    report = df['window'].value_counts().head(10)

    print("Top Applications Used:")
    print(report)

    report.plot(kind='bar', title="Top 10 Applications Used")
    plt.xlabel("Application")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
