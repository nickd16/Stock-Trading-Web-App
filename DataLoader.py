from torch.utils.data import Dataset
import torch
import typing

class correlatedSet(Dataset):

    def __init__(self, corr_files:list, label_file:str, days: int):
        """
            Parameters:
            corr_files -> a list of files considered to be correlated
            label_file -> file which contains the optimal trading strategy
            days  -> the amount of previous days to be included in the vector
        """
        self.data_ = self.extract_info(corr_files)
        self.label_ = self.extract_label(label_file)
        self.days_ = days
        self.size_ = len(self.data_[0])

    def __len__(self) -> int:
        return self.size_ - self.days_

    def __getitem__(self, index: int):

        assert(index < self.size_ - self.days_) #Make sure index is not out of bounds
        data = [comp_info[index:index+self.days_] for comp_info in self.data_] #NOT INCLUSIVE
        label = self.label_[index]

        data = torch.tensor(data)

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
                company_info.append( (line[2], line[4]) )

            file_data.append(company_info)
            f.close()

        #Trim to the shortest (so we can match by day)
        #Note the list is 0(most current) -> len(list)(oldest)
        #We can just shave off the oldest and then reverse the list to syncronize

        minimum = float('inf')
        for f_info in file_data:
            if len(f_info) < minimum:
                minimum = len(f_info)

        for i in range(len(file_data)):
            file_data[i] = file_data[i][:minimum] #Chop off extra data
            file_data[i].reverse() #Oldest to Newest

        return f_info

    def extract_label(self, label_file: str) -> list:
        f = open(label_file, 'r')
        lines = f.readlines()
        f.close()
        return lines.split(' ')









