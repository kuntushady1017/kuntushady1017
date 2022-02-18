from main import bubblesort, check_negative_number, ArrayInRangeError
import array as arr


def interger_array_main(num = arr.array('i', [])):
    try:
        if check_negative_number(num) != 0 and len(num) <= 5:
            #sorting the array using bubble method of sorting
            bubblesort(num)
            #adding the smallest element and largest element in the array
            number = num[0] + num[len(num) - 1]
            #returning the sum of smallest element and largest element in the array
            return number
        
        elif len(num) > 5:
            if len(num) > 5:
                print (ArrayInRangeError(len(num)))
    
        else:
            #returning 0 cause array contain negative number
            if check_negative_number(num) == 0 and len(num) <= 5:
                return check_negative_number(num)
            
    except ValueError:
        #returning excaptions if array has more than 5 elements 
        print("Not array")
        


num = arr.array('i', [60,90,98,90,300,87])
new_array = interger_array_main(num)
print(new_array)