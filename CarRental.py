from random import randint
from datetime import datetime, timedelta
from math import ceil


Customers=[]         #Customers (clients)

CarInventory=[]     #Cars in the inventory
RentalCars=[]       #Cars for rent

RENTAL_BASIS = ['hourly','daily','weekly']
BASE_RENTAL_BASIS_PRICES = [20.0,100.0,500.0] # rates for hourly, daily, weekly


#Default Car Props
CARDIDPREFIX = 1100

#Default Car Props
USERIDPREFIX = 98001

MAKERS = ['HONDA','TOYOTA','TESLA','GM','HYUNDAI','FORD']
YEARS=['2020','2023','2021','2022']
NAMES=['LOOF','BOOY','TRAVA','MOOS','KLAS','LEPA','SERTA','PALLI','TIVAA','WESLY','SKANA']
PLATES=['483h42','fo393j','49k493','0or83e','u37djw','3k283c','2sl73j','wsl329']

COLORS=['blue','red','white','silver','black','yellow']
STYLES=['sedan','SUV','Van','hatchback','pickup','sports']
VERSIONS=['basic','standard','luxury']
ENGINES=['gas','hybrid','electric','hydrogen']
DOORS=['2','4']
PASSENGERS=['2','4','5','8','9']




class Car:
    def __init__(self,carId,maker='HONDA',year='2021',name='TRAVA',plate='493mh4',
                 color='white',style='sedan',version='standard',
                 engine='electric',doors='4',passengers='5',price_category=2):
        self.id=carId
        self.maker=maker
        self.year=year
        self.name=name
        self.plate=plate
        self.color=color
        self.style=style
        self.version=version
        self.engine=engine
        self.doors=doors
        self.passengers=passengers
        self.price_category=price_category


class CarRentalService(Car):
    def __init__(self,carId,maker,year,name,plate,color,style,version,engine,doors,passengers,price_category,
                 status='available',rent_times=0,rent_pricing=BASE_RENTAL_BASIS_PRICES,rental_rate=[],rental_amout=0,
                 start_date='',return_date='',client_id=0):
        super().__init__(carId,maker,year,name,plate,color,style,version,engine,doors,passengers,price_category)  #inherit all props from the parent
        self.status = status
        self.rent_times = rent_times
        self.rent_pricing = [round(x*price_category) for x in rent_pricing]
        self.rental_rate = rental_rate
        self.rental_amout = rental_amout
        self.start_date = start_date
        self.return_date = return_date
        self.client_id = client_id
     

# Create a class for customers and define a constructor in it
class Customer:
    def __init__(self,UserId,FullName,Mobile,DriverLicense):
        self.id=UserId
        self.fullname=FullName
        self.mobile=Mobile
        self.driver_license=DriverLicense
    
    def create_customer():
        
        print(""" Insert Client Information:
              
                  """)
        
        customerId= USERIDPREFIX+len(Customers)

        existingUser=False

        getInput=True
        while getInput:

            Mobile = int(input("Mobile: "))

            oldCustomer = list(x for x in Customers if x.mobile == Mobile)

            if len(oldCustomer)>0:
                return oldCustomer

            FullName = str(input("FullName: "))
            DriverLicense = str(input("Driver License: "))

            if(FullName!='' and Mobile!='' and DriverLicense!=''):
                getInput=False

        #Create customer
        newCustomer  = Customer(customerId,FullName,Mobile,DriverLicense)
        Customers.append(newCustomer)

        return newCustomer
    



class CarRental:
    def __init__(self):
        pass

    def add_cars_to_system(self, num_cars=10):
                
        for i in range(num_cars):
            
            # Create Car Id
            carId = CARDIDPREFIX+1+i

            maker=MAKERS[randint(0,len(MAKERS)-1)]    #Choose a random maker
            year=YEARS[randint(0,len(YEARS)-1)]    #Choose a random year
            name=NAMES[randint(0,len(NAMES)-1)]    #Choose a random name
            plate=PLATES[randint(0,len(PLATES)-1)]    #Choose a random plate

            color=COLORS[randint(0,len(COLORS)-1)]    #Choose a random color
            style=STYLES[randint(0,len(STYLES))-1]    #Choose a random style
            version=VERSIONS[randint(0,len(VERSIONS)-1)]    #Choose a random version
            engine=ENGINES[randint(0,len(ENGINES))-1]    #Choose a random engine
            doors=DOORS[randint(0,len(DOORS))-1]    #Choose a random doors
            passengers=PASSENGERS[randint(0,len(PASSENGERS))-1]    #Choose a random passingers

            price_category = 1.0  #Lowest price (base)

            if(maker=='TESLA'):
                engine='electric'
                price_category = 1.2
            elif(engine=='hydrogen'):
                maker='HYUNDAI'
                price_category = 1.2
            
            if version=='luxury' and style=='pickup':
                price_category = 5*price_category
            elif version=='luxury':
                price_category = 4*price_category
            elif style=='sports':
                price_category = 3*price_category
            elif style=='pickup' or style=='SUV' or style=='Van':
                price_category = price_category+2
            
            if int(passengers)>6:
                price_category = price_category+2


            new_car = Car(carId,maker,year,name,plate,color,style,version,engine,doors,
                          passengers,price_category)
            CarInventory.append(new_car)

            new_rental_car = CarRentalService(carId,maker,year,name,plate,color,style,
                                              version,engine,doors,passengers,price_category)
            RentalCars.append(new_rental_car)

            
        print(num_cars," cars created succesfully.")
        return True
 



    def start(self,cars=10):        
        self.add_cars_to_system(cars) #Add 10 cars to system

    
    def show_cars(self):      
        print("Cars In Inventory:")
        for car in CarInventory:
            print(
                """
                ID: {}
                Maker: {}
                Year: {}
                Name: {}
                Plate: {}
                Color: {}
                Style: {}
                Version: {}
                Engine: {}
                Doors: {}
                Passengers: {}
                Price Category: {}
                """.format(car.id,car.maker,car.year,car.name,car.plate,car.color,car.style,
                           car.version,car.engine,car.doors,car.passengers,car.price_category))


    # - Define a method to display the rented cars. 
    def get_rented_cars(self):
        
        ## Filter cars that are available
        RentedCars = list(filter(lambda x: (x.status == 'RENTED'), RentalCars))

        if len(RentedCars)<1:
            print("""

            SORRY, NO CARS HAD BEEN RENTED
            
            """)
            return 0
        

        print("Cars in Rental: ",len(RentedCars))

        for car in RentedCars:
 
            print("Client ID: "+str(car.client_id))
        
            #Get Customer info:
            customerObj = list(x for x in Customers if int(x.mobile) == int(car.client_id))[0]
            #customerObj = filter(lambda x: (x.mobile == car.client_id), Customers)

            print(
                """
                ID=\033[1m{}\033[0;0m
                Maker: {}
                Year: {}
                Name: {}
                Plate: {}
                Color: {}
                Style: {}
                Version: {}
                Engine: {}
                Doors: {}
                Passengers: {}
                ==
                Status: {}
                Selected rental [rate, price(USD)]: {}    
                Rental date: {}
                Expected Return date: {}
                Customer Name: {} 
                """.format(car.id,car.maker,car.year,car.name,car.plate,
                            car.color,car.style,car.version,car.engine,car.doors,
                            car.passengers,
                            car.status,
                            car.rental_rate,car.start_date,
                            car.return_date,
                            customerObj.fullname))

        return RentedCars
    


    # - Define a method to display the available cars. 
    def get_available_cars(self):
        
        ## Filter cars that are available
        AvailableCarsForRent = list(filter(lambda x: (x.status == 'available'), RentalCars))

        print("Avalable cars: ",len(AvailableCarsForRent))

        count=0
        for car in AvailableCarsForRent:
            count+=1
            print(
                """
                ID=\033[1m{}\033[0;0m
                Maker: {}
                Year: {}
                Name: {}
                Plate: {}
                Color: {}
                Style: {}
                Version: {}
                Engine: {}
                Doors: {}
                Passengers: {}
                ==
                status: {}     
                times rented: {}
                pricing (hourly,daily,weekly): ${} USD  
                """.format(car.id,car.maker,car.year,car.name,car.plate,
                           car.color,car.style,car.version,car.engine,car.doors,
                           car.passengers,
                           car.status,car.rent_times if car.rent_times>0 else 'never',car.rent_pricing))
        
        return AvailableCarsForRent

    # Print customer receipt 
    def print_rental_receipt(self,car):

        print("""
              - CAR RENTAL CUSTOMER RECEIPT -
              """)

        print(
            """
            ==
            VEHICLE:
            ==
            ID=\033[1m{}\033[0;0m
            Maker: {}
            Year: {}
            Name: {}
            Plate: {}
            Color: {}
            Style: {}
            Version: {}
            Engine: {}
            Doors: {}
            Passengers: {}
            ==
            RENTAL SERVICE INFORMATION:
            ==
            Status: {}
            Selected rental [rate, price(USD)]: {}    
            Rental date: {}
            Return date: {}
            """.format(car.id,car.maker,car.year,car.name,car.plate,
                        car.color,car.style,car.version,car.engine,car.doors,
                        car.passengers,
                        car.status,
                        car.rental_rate,car.start_date,
                        car.return_date))
            


    def choose_return_car(self):

        carsRented = self.get_rented_cars()

        if(carsRented==0):
            return 0

        print(""" SELECT RETURNING CAR
              What is the ID of the car you want to return?

              * Type '0' to Finish.
              """)
        
        exists=True
        while exists:

            userInput = int(input("Type the ID of the car you want to return: "))

            if userInput==0:
                return 0
            
            # -ensure that the requested number of cars is both positive 
            # and less than the total number of available cars
            car = list(filter(lambda x: (x.id == userInput), carsRented))
            
            # This will be true as long as the user do not select a valid Car Id (available)        
            exists = len(car)==0    
            
            car_quantity = len(car)
            if userInput<0 or car_quantity > len(carsRented):
                response = {'code':99,'message':'car quantity must be positive and less than available cars'}
                return response
            
        return userInput 
    


    def choose_car(self):

        AvailableCarsForRent = self.get_available_cars()

        print(""" SELECT YOUR RENTAL CAR
              What is the ID of the car you want to rent?

              * Type '0' to Finish.
              """)
        
        exists=True
        while exists:

            userInput = int(input("Type the ID of the car you want to rent: "))

            if userInput==0:
                return 0
            
            # -ensure that the requested number of cars is both positive 
            # and less than the total number of available cars
            car = list(filter(lambda x: (x.id == userInput), AvailableCarsForRent))
            
            # This will be true as long as the user do not select a valid Car Id (available)        
            exists = len(car)==0    
            
            car_quantity = len(car)
            if userInput<0 or car_quantity > len(AvailableCarsForRent):
                response = {'code':99,'message':'car quantity must be positive and less than available cars'}
                return response
            
        return userInput    #Return the CarId input by the user



    def choose_rental_basis(self):

        units=['hours','days','weeks']

        print("""Choose your Rental Basis:
          1 - Hourly
          2 - Daily
          3 - Weekly
              
          * Type '0' to Exit and Cancel All.
                  """)
        
        waitingInput=True
        while waitingInput:
            basis = int(input("Type your rental basis [1,2,3]: "))

            if basis>0 and basis<4:
                waitingInput=False
            elif basis==0:
                return 0,0


        print(f""" Usage Time Need it?
              How many {units[basis-1]} you need it?

              * Type '0' to Exit and Cancel All.
                  """)
        
        
        amount = 1

        waitingInput=True
        while waitingInput:
            amount = int(input(f'Type the {units[basis-1]} you need (7 max)'))
            if amount>0 and amount<8:
                waitingInput=False
            elif amount==0:
                return 0,0

        return basis,amount


    def main_menu(self):

        print(""" HOW CAN WE SERVE YOU?:
          1 - See Available Cars
          2 - Rent Car
          3 - Return Car
  
        * Type '0' to Terminate App.
                  """)
        
        waitingInput=True
        while waitingInput:
            userSelection = int(input("Choose your option [1,2,3]: "))
            if userSelection>=0 and userSelection<4:
                waitingInput=False

        return userSelection
    

    # Create method for renting cars on an hourly, daily, and weekly basis.
    # Define a method that returns the cars based on rental time, 
    # rental mode (hourly, daily, or weekly), and the number of cars rented.
    def rent_car(self):
      
        numberCarsRented=0

        TotalPriceToPay = 0.00

        rentingService=True
        while rentingService:

            #Customer choose the car
            carToRent = self.choose_car()

            if carToRent==0:                
                rentingService=False
                continue


            print(f"""
                You selected car ID: {carToRent}
                """)

            #User select rental basis
            rentBasis,rate_basis_amount = self.choose_rental_basis()

            if rentBasis==0:
                rentingService=False
                continue
  

            #Get customer information
            customer = Customer.create_customer()
            
            numberCarsRented+=1

            #rentedCar = [x for x in RentalCars if x.id==carToRent]
            for rentedCar in list(filter(lambda x: (x.id == carToRent), RentalCars)):

                rentedCar.status = 'RENTED'
                rentedCar.rent_times+=1
                
                rate_basis = RENTAL_BASIS[rentBasis-1]

                priceRates = rentedCar.rent_pricing
                price = priceRates[rentBasis-1]
                rentedCar.rental_rate=[rate_basis,price]

                rentedCar.rental_amout = rate_basis_amount

                TotalPriceToPay+=price*rate_basis_amount*1.00  

                rentedCar.client_id = customer.mobile

                # - Store the rental time of a car in a variable. You can later use this variable in 
                # the bill when returning the car        
                rentedCar.start_date = datetime.now()

                #Expected return time
                if (rate_basis=='hourly'):
                    rentedCar.return_date = datetime.now() + timedelta(hours=int(rate_basis_amount))
                elif (rate_basis=='weekly'):
                    rentedCar.return_date = datetime.now() + timedelta(weeks=int(rate_basis_amount))
                else:
                    #default is daily rental basis
                    rentedCar.return_date = datetime.now() + timedelta(days=int(rate_basis_amount))
                
                self.print_rental_receipt(rentedCar)
                
        #End of while
        else:
            if(numberCarsRented>0):
                print(f"""
                    ---
                            Customer Name:          {customer.fullname}
                            Customer ID:            {customer.mobile}
                             
                            You Rented:             {numberCarsRented} cars.
                            You will need to pay:   ${TotalPriceToPay} USD
                            
                            Thank you for your preference!
                    ---
                """)

        #Finish Rental
        return numberCarsRented, TotalPriceToPay
    


    #Create method to return car
    def return_car(self):

        TotalPriceToPay = 0.00
        numberCarsReturned = 0

        # print("""
        # Write Client Mobile Number (id):
              
        # """)
        # Mobile = int(input("Mobile: "))

        # oldCustomer = list(x for x in Customers if x.mobile == Mobile)

        # if len(oldCustomer)<1:
        #     print("This customer doesn't exist")
        #     return "Customer not found"


        rentingService=True
        while rentingService:

            #Customer choose the car
            carToReturn = self.choose_return_car()

            if carToReturn==0:                
                rentingService=False
                continue


            print(f"""
                You selected car ID: {carToReturn}
                """)

            numberCarsReturned += 1

            #rentedCar = [x for x in RentalCars if x.id==carToRent]
            for rentedCar in list(filter(lambda x: (x.id == carToReturn), RentalCars)):


                #calculate the rental period
                rentalTime = rentedCar.start_date

                [rate_basis,price] = rentedCar.rental_rate      #[rate_basis,price]

                timeDifference = datetime.now()-rentalTime

                rental_period =  timeDifference.days # In days

                if rate_basis=='hourly':                    
                    rental_period =  ceil(rental_period/24) # In hours
                elif rate_basis == 'weekly':
                    rental_period =  ceil(rental_period/7) # In weeks

                if rental_period<1:
                    rental_period=1


                #generate the final bill
                TotalPriceToPay += price * rental_period * 1.00  

                customertId = int(rentedCar.client_id)
                foundCustomer = list(x for x in Customers if int(x.mobile) == customertId)[0]

                #update the inventory stock, 
                rentedCar.status = 'available'
                rentedCar.client_id = ''
                rentedCar.rental_amout = 0      
                rentedCar.start_date = ''
                rentedCar.return_date = ''
                
                self.print_rental_receipt(rentedCar)                

                print(f"""
                    ---                    
                      FINAL BILL:

                            Customer Name:          {foundCustomer.fullname}
                            Customer ID:            {customertId}
                             
                            You Returned:           {numberCarsReturned} car(s).
                            Total to pay:           ${TotalPriceToPay} USD
                            
                            Thank you for your preference!
                    ---
                """)

        #Finish Rental
        return numberCarsReturned
