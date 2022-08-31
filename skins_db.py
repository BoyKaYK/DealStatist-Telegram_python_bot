from time import sleep

class Skins_data_base:
    def add_new_item(user,item):

        file = open('skins.txt','a')
        file.write(f"{item}\n")
        file.close()
   
    def read_items(user):
        
        read_file = open('skins.txt','r')
        items_list = read_file.read().splitlines()
        read_file.close()
        print(items_list)
        return items_list

    def add_inventory_item(user,item,market_link):

        file = open('inventory.txt','a',encoding="utf-8")
        file.write(f"{item}\n{market_link}\n")
        file.close()

    def read_inventory_item(user):

        read_file = open('inventory.txt','r',encoding="utf-8")
        items_list = read_file.read().splitlines()
        read_file.close()
        print(items_list)
        return items_list


        


db = Skins_data_base()
#db.add_new_item()
#db.read_items()



