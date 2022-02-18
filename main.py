#sorting method of the array bubble sort 
def bubblesort(sample_array):
    for j in range(len(sample_array)-1,0,-1):
        for i in range(j):
            if sample_array[i]> sample_array[i+1]:
                temp = sample_array[i] 
                sample_array[i] = sample_array[i+1] 
                sample_array[i+1] = temp
    return sample_array


#checking if array consist a negetive number
def check_negative_number(sample_array):
    for i in range(len(sample_array)):
        if sample_array[i] < 0:
            return 0
        


#raising an exception if the array length is exceed
class ArrayInRangeError(Exception):
    """Exception raised for errors in the number elements.

    Attributes:
        num -- element of the array great than 5
        message -- explanation of the error
    """

    def __init__(self, num, message="Array out of range there are more than 5 elements"):
        self.num = num
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.num} -> {self.message}'

            
                
