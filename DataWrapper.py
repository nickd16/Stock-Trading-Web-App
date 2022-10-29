from torch.utils.data import Dataset
from DataLoader import correlatedSet
import typing
import torch
import os


class wrappedSet(Dataset):

    def __init__(self, days:int, seq_len: int ):
        """
            Parameters:
            days    -> the amount of previous days to be included in the vector
            seq_len -> length of each time sequence
        """

        #List of Correlated information  {  Main.csv: [Corr1, Corr2, ...] , .... }
            correlations = {}
            self.data_ = []
            self.days_ = days
            self.seq_len_ = seq_len
            self.size_ = 0

            path = os.getcwd()
            for file in os.listdir(path):

                if(file == "labels"):
                    continue
                
                self.data_.append(correlatedSet(correlations[file], os.path.join(path+"/labels", file[:file.index('.')] + "_labels.txt") , self.days_, self.seq_len_))
                self.size_ += len(self.data_[-1])

    def __len__(self) -> int:
        return self.size_
    
    def __getitem__(self, index) -> torch.Tensor:
        prev_ind = -1
        curr_ind =  0
        passed   =  0

        while(curr_ind < self.size_):
            if passed > index:
                break

            passed += len(self.data[curr_ind])
            prev_ind +=1
            curr_ind +=1

        curr_ind =  index - (passed - len(self.data_[curr_ind]))

        return self.data_[prev_ind][curr_ind]
