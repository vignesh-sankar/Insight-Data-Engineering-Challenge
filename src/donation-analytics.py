import datetime
import math
import re
import sys
dict1 = dict()
dict2 = dict()
def arraySort(array_list):
    for loop_var in range(1,len(array_list)):
        curr_val = float(array_list[loop_var])
        pos= loop_var
        while pos > 0 and float(array_list[pos-1]) > float(curr_val):
            array_list[pos]=array_list[pos-1]
            pos = pos-1
        array_list[pos]=curr_val
if(len(sys.argv) != 4):
    print("Wrong number of arguments\n")
else:
    output_fh = open(sys.argv[3],"w+")

    with open(sys.argv[2],"r") as percent_file:
        for line in percent_file:
            percentile = int(line)

    with open(sys.argv[1],"r") as input_file:
        for line in input_file:
            line_split = line.split("|")
            if(len(line_split) != 21):
                continue

        
            #OTHER_ID
            if(len(line_split[15]) != 0):
                continue
        
            #TRANSACTION_AMT
            if((line_split[14] is not None) and (float(line_split[14]) > 0)):
                tr_amt = line_split[14]
            else:
                continue
        
            #CMTE_ID
            if(line_split[0] is not None):
                cmte_id = line_split[0]
            else:
                continue
       
        
            #NAME
            if(line_split[7] is None):
                continue
            else:
                name = re.sub(r'\s', '',line_split[7])
                name = name.replace(',','')
                if not name.isalpha():
                    continue
            
            #Zip Code
            if(len(line_split[10]) >= 5):
                zip_code = line_split[10][0:5]
            else:
                continue
        
            #Date
            if(len(line_split[13]) != 8):
                continue

            month = line_split[13][0:2]
            day = line_split[13][2:4]
            year = line_split[13][-4:]
            try:
                newDate = datetime.datetime(int(year),int(month),int(day))

            except ValueError:
                continue
            tr_date = line_split[13]
        
            key = name+zip_code

            if (dict1.get(key) == None):
                postings = {}
                postings["year"] = year
                val = cmte_id+"|"+tr_amt
                postings["value"] = [val]
                dict1[key] = postings
            else:
                stored_year = dict1[key]["year"]
                if stored_year > year:
                    dict1_val = dict1[key]["value"]
                    dict1[key]["year"] = year
                    new_val = cmte_id + "|" + tr_amt
                    dict1[key]["value"] = [new_val]
                    for list_val in dict1_val:
                        dict1_cmte , dict1_tr_amt = list_val.split("|")
                        key_dict2 = dict1_cmte+zip_code+stored_year
                        if dict2.get(key_dict2) is None:
                            dict2[key_dict2] = [float(dict1_tr_amt)]
                        else:
                            sample_list = dict2.get(key_dict2)
                            sample_list.append(float(dict1_tr_amt))
                            arraySort(sample_list)
                            dict2[key_dict2] = sample_list
                elif stored_year == year:
                    sample_list = list()
                    sample_list = dict1[key]["value"]
                    val = cmte_id+"|"+tr_amt
                    sample_list.append(val)
                    dict1[key]["value"] = sample_list
                else:
                    key_dict2 = cmte_id+zip_code+year
                    if dict2.get(key_dict2) is None:
                        dict2[key_dict2] = [float(tr_amt)]
                        if(float(tr_amt) == int(tr_amt)):
                            tr_amt = int(tr_amt)
                        write_file_content = cmte_id+"|"+zip_code+"|"+year+"|"+str(tr_amt)+"|"+str(tr_amt)+"|1"
                        output_fh.write(write_file_content)
                        output_fh.write("\n")
                    else:
                        temp = list()
                        temp = dict2[key_dict2]
                        temp.append(float(tr_amt))
                        new_amt = sum(temp)
                        arraySort(temp)
                        pos = math.ceil((percentile * len(temp))/100)
                        percentile_amt = temp[pos-1]
                        total_count = len(temp)
                        dict2[key_dict2] = temp
                        if(float(percentile_amt) == int(percentile_amt)):
                            percentile_amt = int(percentile_amt)
                        if(float(new_amt) == int(new_amt)):
                            new_amt = int(new_amt)
                        write_file_content = cmte_id+"|"+zip_code+"|"+year+"|"+str(percentile_amt)+"|"+str(new_amt)+"|"+str(total_count)
                        output_fh.write(write_file_content)
                        output_fh.write("\n")

                    
    output_fh.close()
