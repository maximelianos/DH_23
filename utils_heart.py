# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
# Import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
import sklearn as sklearn


def load_dataset(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    return df

def scale_data(df):
    # Initialize the scaler
    scaler = MinMaxScaler()
    # Fit and transform the dataset
    df_scaled = pd.DataFrame(scaler.fit_transform (df[['Beats','Intensity','Steps']]), columns=['Beats', 'Intensity', 'Steps'])

    return df_scaled

def get_user_ids(df):
    return df["Id"].unique()

def get_data_for_user(user_id, df):
    return df[df["Id"] == user_id]

def drop_rows_with_missing_values(df):
    # Drop rows where there is a missing value
    df.dropna(inplace=True)

def check_for_missing_values(df):
    # Check for missing values
    df.isnull().sum()


def plot_time_series_plot(df):
    #Import necessary libraries

    # Time series plots
    plt.figure(figsize=(15 , 5))

    # Plot for Beats
    plt.subplot(1 , 3 , 1)
    plt.plot(df['Beats'])
    plt.title('Time Series Plot for Beats')

    # Plot for Intensity
    plt.subplot(1 , 3 , 2)
    plt.plot( df ['Intensity'])
    plt.title( 'Time Series Plot for Intensity')

    # Plot for Steps
    plt.subplot(1 , 3 , 3)
    plt.plot( df ['Steps'])
    plt.title('Time Series Plot for Steps')

    plt.tight_layout()
    
 #Histograms to observe distributions
def plot_histograms(df):
    plt.figure ( figsize =(18 , 6) )

    # Histogram for Calories
    plt.subplot(1 , 3 , 1)
    plt.hist(df ['Beats'] , bins =20)
    plt.title('Histogram for Beats')

    # Histogram for Intensity
    plt.subplot (1 , 3 , 2)
    plt.hist ( df ['Intensity'] , bins =20)
    plt.title ('Histogram for Intensity')

    # Histogram for Average Intensity
    plt.subplot (1 , 3 , 3)
    plt.hist ( df ['Steps'] , bins =20)
    plt.title ('Histogram for Steps')

    plt.tight_layout()
    plt.show()