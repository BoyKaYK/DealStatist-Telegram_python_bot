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
        


db = Skins_data_base()
#db.add_new_item()
#db.read_items()



