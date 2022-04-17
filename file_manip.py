import os
import random
import pandas as pd



def combine_csv_in_chunks(directory_path_read, directory_path_write, csv_name_list, out_csv_name="combined_files.csv", chunksize=5000):
    #This function combines all csv files provided in the csv_name_list
    #into one csv file. This is done in chunks using pandas.
    out_csv_path = os.path.join(directory_path_write, out_csv_name)
    try:
        os.remove(out_csv_path) #remove the output file from the system if it exists
    except OSError:
        pass #if it does not exist, pass
    write_header = True #write header for first file, first chunk
    for csv_name in csv_name_list:
        in_csv_path = os.path.join(directory_path_read, csv_name)
        with pd.read_csv(in_csv_path, header=0, chunksize=chunksize) as chunk_collection:
            gear_type = csv_name.split('.')[0]
            for chunk in chunk_collection:
                chunk.insert(len(chunk.columns), 'gear_type', gear_type) #add a column to specify the gear type
                chunk.to_csv(out_csv_path, mode='a', sep=',', index=False, header=write_header)
                write_header=False #Do no write header for remaining chunks and remaining files
                

def add_index_in_chunks(directory_path_read, directory_path_write, csv_name, chunksize=5000): #
    #This function adds an auto_incremented index column to a csv files. 
    in_csv_path = os.path.join(directory_path_read, csv_name)
    out_csv_path = os.path.join(directory_path_write, csv_name.split('.')[0]+"_indexed.csv")
    try:
        os.remove(out_csv_path) #remove the output file from the system if it exists
    except OSError:
        pass #if it does not exist, pass
    index = 0;
    with pd.read_csv(in_csv_path, header=0, chunksize=chunksize) as chunk_collection:
        write_header = True #write header for first chunk
        for chunk in chunk_collection:
            index_list = range(index, index+chunk.shape[0]) #sequence of digits from last chunk's last index
            index = index_list[-1] #update index for next chunk as last index in current chunk
            chunk.insert(0, 'index', index_list) #insert an attribute called 'index' coming from index_list
            chunk.to_csv(out_csv_path, mode='a', sep=',', index=False, header=write_header)
            write_header = False #do not write header for remaining chunks
            
            
def remove_records(directory_path, csv_name, vals, chunksize=5000): 
    # This function removes records that do not have an is_fishing value in vals.
    in_csv_path = os.path.join(directory_path, csv_name)
    out_csv_path = os.path.join(directory_path, csv_name.split('.')[0]+"_filtered.csv")
    try:
        os.remove(out_csv_path) #remove the output file from the system if it exists
    except OSError:
        pass #if it does not exist, pass
    with pd.read_csv(in_csv_path, header=0, chunksize=chunksize) as chunk_collection:
        write_header=True
        for chunk in chunk_collection:
            values = vals
            chunk_is_fishing01 = chunk[chunk.is_fishing.isin(values)==True]
            chunk_is_fishing01.to_csv(out_csv_path, mode='a', sep=',', index=False, header=write_header)
            write_header=False
            

def load_data_random_sample(directory_path, csv_name, proportion): 
    #This function loads a random sample of the dataset for analysis.
    #directory_path is your directory path that has the data file, csv_nam is the name of the data file
    #and proportion is the proportion of lines you want to read.
    in_csv_path = os.path.join(directory_path, csv_name)
    out_csv_path = os.path.join(directory_path, "exploratory_sample_file.csv")
    if(os.path.isfile(out_csv_path)): #check if file already exists
        response = input("A sample dataset already exists. Creating another may lead to data snooping. Do you want to make another (yes/no)?")
        if(response.lower()[0]=='y'):
            sample_file = pd.read_csv(in_csv_path, header=0, skiprows=lambda i : i>0 and random.random()>proportion)
            sample_file.to_csv(out_csv_path, mode='a', sep=',', index=False, header=True) #save sample file as csv
            indices_explored = sample_file['index'] #save indices
            try:
                os.remove(os.path.join(directory_path, 'indices_explored.csv')) #remove old indices file
            except OSError:
                pass #pass if file does not exist
            indices_explored.to_csv(os.path.join(directory_path, 'indices_explored.csv'), sep=',', index=False, header=True) #store indices in a csv
            return sample_file
        else:
            print("Sampling aborted, output is the existing file.")
            return pd.read_csv(os.path.join(directory_path, 'exploratory_sample_file.csv'), header=0)
    else:
        sample_file = pd.read_csv(in_csv_path, header=0, skiprows=lambda i : i>0 and random.random()>proportion)
        sample_file.to_csv(out_csv_path, mode='a', sep=',', index=False, header=True)
        indices_explored = sample_file['index']
        indices_explored.to_csv(os.path.join(directory_path, 'indices_explored.csv'), sep=',', index=False, header=True)
        return sample_file


