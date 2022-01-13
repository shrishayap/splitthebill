import re
import pytesseract

def img_to_dict(image):
    #text from image, if not image, raise error
    text = pytesseract.image_to_string(image)
    text = text.upper()

    #splits to lines
    lines = text.split("\n")
    #Regex for price
    price = re.compile("[$]?[0-9]*[.,][0-9]{2}")

    #Finds first instance of a price 
    #Splices everything else out before (irrelevent)
    for line in lines:
        if price.search(line):
            start = line
            index = lines.index(start)
            lines = lines[index:]
            break
    
    #Finds the final price, the 'total due'. If 
    #cannot be found, then returns error
    
    price_reg = re.compile("[0-9]*[.,][0-9]{2}")
    all_prices = price_reg.findall(text)
    total = all_prices[-1]

    #Eliminates everything after the 'final, total price'
    for i in range(len(lines)):
        if total in lines[len(lines) - 1 - i]:
            lines = lines[:len(lines) - i]
            break


    
    #now lines is the list of lines that contain relevent info only

    #Finds index of prices in lists
    idx_of_prices = []
    for line in lines:
        if price_reg.search(line):
            idx_of_prices.append(lines.index(line))

    #Splits into individual items with a dict
    dct = {}
    for i in range(len(idx_of_prices)):
        string_to_add = ""
        try:
            for line in lines[idx_of_prices[i]:idx_of_prices[i+1]]:
                string_to_add = string_to_add + line + ' '
        except IndexError:
            string_to_add = string_to_add + lines[-1] + ' '
        #now string_to_add is an entire item

        #Isolates price (and turns to float for calcs)
        price = re.findall("[$]?[0-9]*[.,][0-9]{2}",string_to_add)[0]
        price = price.replace(',','.')
        price = price.replace('$', '')
        price = float(price)
        #

        #Removes the price for just the description
        description = re.sub("[$]?[0-9]*[.,][0-9]{2}", '',string_to_add)
        #
        description = description.upper()
        #Adds description : price to dict
        dct[description] = price
        #
    return dct
    

def get_tax(dct):
    '''
    With an input of the dict, it parses out the tax for calcs
    :param dict: a dicitonary with item: price
    :return: tax, the float for tax
    '''
    for item in dct:
        if "TAX" in item:
            tax = dct[item]
            return tax
    return 0.00

def get_tip(dct):
    '''
    With an input of the dict, it parses out the tip for calcs
    :param dict: a dicitonary with item: price
    :return: tip, the float for tip
    '''
    for item in dct:
        if "TIP" in item:
            tip = dct[item]
            return tip
    return 0.00

def only_items(dct):
    '''
    With an input of the dict, it only takes items, disregards, 
    total, tax, etc
    :return: only items
    '''
    item_dict = {}
    for item in dct:
        if re.findall("(SUB)?(.)?(TOTAL)", item):
            start_end = item
            break
        else:
            item_dict[item] = dct[item]
    
    return item_dict

def payout(names, who_dict, prices, tax, tip):
    '''
    Using a list of names, and a dicitonary of who bought what item, It tells
    you the total amount each person owes
    '''
    #creates payout dict with 0 dollars owed per person
    payout_dict = {}
    for name in names:
        payout_dict[name] = 0
    
    for item in who_dict:
        #how many ppl bought certain item
        if not who_dict[item] == "none":
            num_ppl = len(who_dict[item])
            people = who_dict[item]

            for name in people:
                payout_dict[name] += prices[item] / num_ppl


    #finds relative percentage of order total to help with tax and tip calcs
    total = 0
    for name in payout_dict:
        total += payout_dict[name]
    
    rel_percents = {}
    for name in payout_dict:
        rel_percents[name] = payout_dict[name] / total

    for name in payout_dict:
        payout_dict[name] +=  (float(tip) + float(tax)) * rel_percents[name]
    
            
    return payout_dict

