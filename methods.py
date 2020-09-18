"""
User-defined functions for Spoti
"""
import os
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pandas as pd
from PyPDF2 import PdfFileMerger
import numpy as np

def number_of_calls(x):                 
    # Takes the total number of songs in a playlist that's passed to it as an 
    # argument and returns the number of call Spoti will make to Spotify's API
    y = x / 100
    z = math.ceil(y)
    return z

def create_csv(df):
    # Converts the Pandas dataframe into a csv file and notifies the user
    # of the file's location
    file_name = 'Features.csv'
    csv = df.to_csv(file_name)
    cwd = os.getcwd()
    print('Audio features have been downloaded and saved as {} in {}'.
    format(file_name, cwd))

def plotdata(csv,total):
    # Reads the csv file that's passed to it as an argument and uses 
    # matplotlib to plot data from the csv file.  Graphs are saved as seperate 
    # and pds files and user is notified of their location. 
    data = pd.read_csv(csv, index_col=0)        # specify index
     
    # Creates scatter plots
    plt.scatter(data['energy'], data['valence'], color='g',  marker='o')
    plt.xlabel('Energy')
    plt.ylabel('Valence')
    plt.title('Energy & Valence Scatter Plot')
    file1 = 'Energy_Valence_Scatter.pdf'
    plt.savefig(file1)              # Create pdf file to be merged for later
    plt.close()
    
    # Creates histograms 
    plt.hist(data['energy'], color = 'purple')
    plt.xlabel('Energy')
    plt.ylabel('Number of Songs')
    plt.title('Energy-Histogram')
    file2 = 'Energy_histogram.pdf'
    plt.savefig(file2)
    plt.close()
    
    plt.hist(data['danceability'], color='red')
    plt.xlabel('Danceability')
    plt.ylabel('Number of Songs')
    plt.title('Danceability-Histogram')
    file3 = 'Danceability_histogram.pdf'
    plt.savefig(file3)
    plt.close()
    
    plt.hist(data['tempo'], color='c')
    plt.xlabel('Tempo')
    plt.ylabel('Number of Songs')
    plt.title('Tempo-Histogram')
    file4 = 'Tempo_histogram.pdf'
    plt.savefig(file4)
    plt.close()

    # Creates a stackplot
    labels = ['Valence', 'Energy', 'Danceability']
    plt.stackplot(data.index, data['valence'], data['energy'], data['danceability'],
                  labels=labels, colors=['m','c','k'])
    plt.legend()
    plt.xlabel('Index of Songs')
    plt.title('StackPlot')
    file5 = 'Stackplot.pdf'
    plt.savefig(file5)
    plt.close()

    # Merges the pdfs files into one by using PyPDF2
    pdfs = [file1, file2, file3, file4, file5]
    merger = PdfFileMerger()
    for pdf in pdfs:
       merger.append(pdf)
    merger.write("Graphs.pdf")
    merger.close() 
    file_name = 'Graphs.pdf'
    cwd = os.getcwd()
    print('Data has been plotted and saved as {} in {}'.
    format(file_name, cwd))
    
    os.remove(file1)                # Delete pdf files afer merging 
    os.remove(file2)               
    os.remove(file3)
    os.remove(file4)
    os.remove(file5)
    
    # Creates a 3d graph 
    cm = plt.get_cmap("seismic")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    col = np.arange(total)
    
    ax.scatter(data['energy'], data['danceability'], data['valence'], 
               c=col, marker='o', cmap=cm)

    ax.set_xlabel('Energy')
    ax.set_ylabel('Danceability')
    ax.set_zlabel('Valence')
    plt.show()
    plt.close()

