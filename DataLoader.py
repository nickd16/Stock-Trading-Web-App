from torch.utils.data import Dataset
import torch
import typing

class correlatedSet(Dataset):

    def __init__(self, corr_files:list, label_file:str, days: int, seq_len: int):
        """
            Parameters:
            corr_files -> a list of files considered to be correlated
            label_file -> file which contains the optimal trading strategy
            days       -> the amount of previous days to be included in the vector
            seq_len    -> length of each time sequence
        """
        self.seq_len_ = seq_len
        self.days_ = days
        self.data_ = self.extract_info(corr_files)
        self.label_ = self.extract_label(label_file)
        self.size_ = len(self.data_[0])
        self.correlated_files_ = len(corr_files)

    def __len__(self) -> int:
        print(self.size_)
        return self.size_

    def __getitem__(self, index: int):

        index_start = index * self.seq_len_
        index_end   = index * self.seq_len_ + self.days_
        index_last  = (index+1) * (self.seq_len_) + self.days_


        data = []
        while(index_end != index_last):
            data.append( [self.data_[i][index_start:index_end] for i in range(len(self.data_))] )
            index_start+=1
            index_end  +=1


        label = self.label_[index * self.seq_len_ + self.days_]
        data = torch.tensor(data)
        data = data.reshape(self.seq_len_, self.correlated_files_, self.days_)

        print(data)
        print(data.shape)
        return (data, label)
            
    def extract_info(self, files:list) -> list:
        #Iterate through all the files
        #Read them all into  a list
        file_data = []

        for file in files:

            f = open(file, 'r')
            company_info = []

            first = True #skip the first iteration
            while ( line:= f.readline() ):

                if(first):#skipping first
                    first = False
                    continue

                line = line.split(',')
                
                # ADD VOLUME IN LATER
                #if (line[2] == 'N/A'):
                #    line[2] = 3000

                company_info.append( float(line[4]) )

            file_data.append(company_info)
            f.close()

        #Trim to the shortest (so we can match by day)
        #Note the list is 0(most current) -> len(list)(oldest)
        #We can just shave off the oldest and then reverse the list to syncronize

        minimum = float('inf')
        for f_info in file_data:
            if len(f_info) < minimum:
                minimum = len(f_info)
    
        print(minimum)
        updated_size = ((minimum-self.days_) // self.seq_len_) + self.days_
        for i in range(len(file_data)):
            file_data[i] = file_data[i][:updated_size] #Chop off extra data
            file_data[i].reverse() #Oldest to Newest


        return file_data

    def extract_label(self, label_file: str) -> list:
        f = open(label_file, 'r')
        line = f.readline()
        f.close()
        return line.split(' ')









