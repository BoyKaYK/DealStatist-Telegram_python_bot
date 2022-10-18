from float_parser import get_fv_list


def compare_fv(max_value,item_name):
    url = f'https://steamcommunity.com/market/listings/730/{item_name}' 
    fv_list = get_fv_list(url)
    acceptable_fv = []
    for i in range(len(fv_list)):
        if float(max_value) >= float(fv_list[i]):
            acceptable_fv.append(float(fv_list[i]))
        else:
            continue
    return acceptable_fv

#print(compare_fv(0.25))