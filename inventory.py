'''
Created on Feb 7, 2016

@author: Fereydoun Babaei
'''
import random
import logging
import time
from time import sleep

logging.basicConfig(level=logging.DEBUG, 
                    format='%(message)s',
                    )

class Products(object):
    ''' This is the products class, the parameters it needs are like:
        example: Products("new",{'A':150,'B':150,'C':150,'D':150,'E':150})    
    '''
    def __init__(self, *args):
        ''' Creating a list of products name available in the inventory
        '''                        
        if args[0] == 'new':
            self.Initial_Inventory = args[1]
            self.Current_Inventory = args[1]
            self.Products = list(args[1].keys())
        elif args[0] == 'update':
            for i in args[1].keys():
                print("Product %s is added to the list of products " % i)
                self.Products = list(args[1].keys())
                    
class Inventory(object):
    '''
    This is the Inventory class that has-a instance of Products class
    It manages the inventory of the Products 
    The Inventory constructor gets product:quantity pairs as a dictionary
        example: Inventory("new",{'A':150,'B':150,'C':150,'D':150,'E':150})
    '''
    def __init__(self, *args):
        ''' Instantiate Products class for an instance of the product class is needed
        '''
        self.products = Products(*args)
        ''' Checking for new parameter to initialize inventory  
        '''
        if args[0] == 'new': self.current_inventory = self.products.Initial_Inventory
        self.back_order = {}
        self.available = {}
        self.orders_list = []
        self.executed_orders = []
        self.orders = {}
        self.zero_invntory_items = []
        self.orders_report = {}

    def check_inventory(self):
        ''' This method generates and returns a report of Inventory including 
        a list of items with zero inventory
        '''
        zero_inventory_flag = 0
        for k,v in self.current_inventory.items():
            ''' Creating a flag for total zero inventory (All items with no inventory)
            '''
            zero_inventory_flag += v
            if v == 0:
                logging.warning("\t %s has  0 quantity in the inventory ", k)
                ''' Creating a list of items with zero inventory quantity
                '''
                self.zero_invntory_items.append(k)
        if zero_inventory_flag == 0:
            logging.warning(";;;;;;;;;;\tWARNING: ZERO INVENTORY SYSTEN IS HALTING!\t ;;;;;;;;;;")
            
            self.print_report()
            ''' Returning zero flag to indicate system is halting
            '''
            return zero_inventory_flag, self.current_inventory
        ''' If zero flag is not zero, returns zero inventory items list and current inventory  
        '''
        report = {'List of zero inventory:':self.zero_invntory_items,
                  'Current Inventory:':self.current_inventory}
        print(report)
        return self.zero_invntory_items, self.current_inventory

    def check_zero_inventory(self):
        zero_inventory, current_available_inventory = self.check_inventory()
        if zero_inventory == 0 or len(current_available_inventory) == 0:
            logging.warning("Inventory is down to zero, no more order execution")
            return None  
        else:
            return zero_inventory                   

    def check_item(self,item):
        ''' This function checks and returns a specific item number in the inventory
        '''
        sleep(0.2)
        logging.info("Total inventory for %s = %s", item, self.current_inventory[item])
        return self.current_inventory[item]
    
    def get_item(self, item, n):
        ''' This Function check for "n" number of an item in the inventory, 
        gets what is available of the "n" and updates inventory
        It also create lists of available and back order items
        '''
        self.available.setdefault(item, 0)
        self.back_order.setdefault(item, 0)
        ''' Checking to see if the requested item numbers are available in the inventory
        '''
        if self.current_inventory[item] >= n:
            self.available[item] += n
        else:
            self.back_order[item] = n - self.current_inventory[item]
            self.available[item] = n - self.back_order[item]
        ''' Updating the current inventory numbers for teh item
        '''
        self.current_inventory[item] -= self.available[item]
        print( "Ordered item:", item , "\tAvailable:",self.available[item], "\tBack order: ", self.back_order[item])
#         self.products=Products('update',self.current_inventory)
        
        ''' Returning current inventory '''
        return self.current_inventory
    def print_report(self):
        for k,v in self.orders_report.items():
            print("__"*20, "\nOrder Number:\t", k, "\nName:\t", v['Header'])
            for i in v['Lines']:
                print(i['Product'], '=', i['Quantity'],)                       
        
class Order(object):
    ''' This is the Order class that generates an order, and communicates 
    the new order with the Inventory class
    Order class requires an instance of inventory to be passed to as a parameter
    product order can be in a dictionary ({'A':2,'B':3...}  format or as key,value map format(A=2) 
    '''
    def __init__(self, inventory,**kwargs):
        ''' Instantiating a new inventory instance
        '''
        self.inventory = inventory  
        ''' Formatting order
        '''      
        self.order = {'Header':'','Lines':[]}
        '''  Generating a random order number
        '''
        self.order_number = random.randrange(100,1000,3)
        ''' Assign the order name to the Header 
        '''      
        self.order['Header'] = kwargs.get('Name')
        ''' Adding order number to orders_list in the inventory
        '''
        self.inventory.orders_list.append(self.order_number)
        ''' Checking number of products in order, for one product order , quantity should be more than zero 
        ''' 
        print('++'*20, "\n\tCurrent Inventory products:\n\t", self.inventory.current_inventory.keys())
        '''  Validating items for each product in the order
        '''
        for i in kwargs.keys():
            if not isinstance(kwargs.get(i), int):
                ''' Checking for order name, (Name:" " key value)
                '''
                continue

            if kwargs.get(i) <= 0 or kwargs.get(i) > 5:
                ''' checking the number of items for each product ordered to be between 1 to 5
                '''
                if i in kwargs.keys() and i in self.inventory.current_inventory.keys(): 
                    ''' Making sure i is in the current_invnetory
                    '''
                    logging.warning("\tCan't order:\t %s for %s\n\tQuantity is between 0 to 5", kwargs[i], i)
                continue                

            if i in self.inventory.current_inventory.keys() and self.inventory.check_item(i) < kwargs[i]:
                ''' Checking available inventory for each product in the order
                '''                
                logging.warning('Not enough %s in the inventory, added to the back order list' % i)
            ''' Formating line = {'Product':'A', 'Quantity':0} '''
            line = {}
            line['Product'] = i
            line['Quantity'] = kwargs.get(i)
            ''' Forming ['Lines'] list '''
            self.order['Lines'].append(line)
        inventory.orders_report[self.order_number] = self.order
        print("\nHere is the order report:\n", self.inventory.orders_report)
        
    def place_order(self):
        ''' This method checks the order['Lines'] and for each element validates the order,
        get the order from the inventory, update the inventory, created a list of available and
        a list of back order quantities for each item on the list.
        At the end it returns order number for the line 
        '''
        print("="*20,"\nPlacing order number:", self.order_number)
        for i in self.order['Lines']:
            print('+'*20)
            if i['Quantity'] > 5:
                logging.warning("\tCannot order more than 5 of %s item", i['Product'])
                continue                
            else:
                self.inventory.get_item(i['Product'], i['Quantity'])
        print("="*20, "\nReport for order number:", self.order_number)
        print("Available items:\n\t",self.inventory.available, "\nBack order items:\n\t",self.inventory.back_order)
        print("Current Inventory:\n\t", self.inventory.current_inventory)
        self.inventory.available = {}
        self.inventory.back_order = {}
        ''' Returning order number ...
        '''
        return self.order_number

class Allocator(object):
    ''' The Allocator class is for creating a list or orders with a
    unique key to be used for setting priority of orders execution.
    It is used for executing orders that were logged in an inventory 
    instance that is passed to this class as a parameter. 
    This class observes the inventory allocation and creates final report 
    for the case of zero total inventory of all the products ...
    '''
    def __init__(self, inventory, **kwargs):
        self.order = kwargs
        self.orders = {}
        self.inventory = inventory
        sleep(1)
        ''' Generating a time stamp for the order that was entered
        ''' 
        self.orders.setdefault(time.ctime(), self.order)
        self.inventory.orders[time.ctime()] = self.order

    def get_order(self):
        ''' This function can find an order by order number
        '''
        for k,v in self.inventory.orders_report.items():
            print("__"*50, "\nOrder Number:\t", k, "\nOrder:\t", v)
            
        print("\nOrders with order numbers:\n", self.inventory.orders_report)
        return self.inventory.orders_report
    
    def execute_orders(self):
        ''' This function execute orders that have been entered to the system
        It sorts the orders by their time stamps and execute one at the time 
        in order they were entered!
        '''
        keys = sorted(self.inventory.orders)
        print("Sorted KEYS >>>>\t ", keys)
        for k in keys:
            if self.inventory.check_zero_inventory == 0: 
                self.inventory.print_report()
                exit()
            else:
                v = self.inventory.orders[k]
                order = Order(self.inventory, **v)
                order_number = order.place_order()                 
                print(">>\tREPORT\t<<"*3, "\n\t" ,self.inventory.check_inventory())
                self.inventory.executed_orders.append(order_number)           
        
if __name__ == '__main__':
   
    orders = {
        'o1' : {'Name':'HBF','A':2, 'B':1,'C':0,'D':3,'E':4},
        'o2' : {'Name':'RBF','A':5,'B':3,'C':4,'D':5,'E':5},
        'o3' : {'Name':'FF', 'A':2, 'B':1,'C':0,'D':7,'E':4},
        'o4' : {'Name':'fb', 'A':5,'B':3,'C':4,'D':5,'E':5}
    }
    product_dict = {'A':150,'B':150,'C':150,'D':150,'E':150}
    inventory = Inventory('new',product_dict)
    print("\n\tPlacing and Executing Orders!",)
#     for o in orders.values():
#         allocator = Allocator(inventory, **o)
#         print("__"*40,"\nEntering Order Number ", o) 
    
    o = {'Name':'HBF','A':2, 'B':1,'C':3,'D':3,'E':4}           
    for i in range(10):
        allocator = Allocator(inventory, **o)
        print("__"*40,"\nEntering Order Number ", i, o)
    
    allocator.execute_orders()
    allocator.get_order()

    
