def insert(dct, lst): 
    for x in lst[:-2]: 
        dct[x] = dct = dct.get(x, dict()) 
    dct.update({lst[-2]: lst[-1]}) 
      
  
def convert_nested(dct): 
    # empty dict to store the result 
    result = dict() 
  
    # create an iterator of lists  
    # representing nested or hierarchial flow 
    lsts = ([*k.split("_"), v] for k, v in dct.items()) 
  
    # insert each list into the result 
    for lst in lsts: 
        print(lst) 
    return result 
          
# initialising_dictionary 
ini_dict = {'Geeks_for_for':1}#,'Geeks_for_geeks':4} 
            #'for_geeks_Geeks':3,'geeks_Geeks_for':7} 
  
# priniting initial dictionary 
print ("initial_dictionary", str(ini_dict)) 
  
# code to convert ini_dict to nested  
# dictionary splitting_dict_keys 
_split_dict = [[*a.split('_'), b] for a, b in ini_dict.items()] 
  
  
# printing final dictionary 
print ("final_dictionary", str(convert_nested(ini_dict))) 