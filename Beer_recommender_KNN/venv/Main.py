from csv import reader
from math import sqrt

"""Laad het csv bestand in python zodat het bewerkt kan worden"""
def load_csv(filename):
	file = open(filename, "r")
	lines = reader(file)
	dataset = list(lines)
	return dataset

""""Zorgt ervoor dat de dataset in een list/dictionary komt zonder onnodige waardes ( bijv de Index) en creeert een coordinaat van 
de x ( ABV) en de y ( IBU)
Zo is het makkelijker om later ermee te werken"""
def preparedata(dataset):
    dataframe = []

    for data in dataset[1:]:
        coordinate_x_abv = float(data[1])
        coordinate_y_ibu = float(data[2])
        type_of_beer = data[3]

        """Afronden naar 1 dec"""
        coordinate_x_abv = round(coordinate_x_abv, 1)

        dataframe.append([coordinate_x_abv, coordinate_y_ibu, type_of_beer])

    return dataframe


"""Nog een functie die de waardes checken van de input ewn controleren net zo lang tot de input goed is"""
def askUserInput():

    while True:
        try:
            abv = float(input('Vul het ABV gehalte van uw drankje in:'))
            abv = round(abv,1)
            print("Het ABV gehalte wordt afgerond naar:",abv )
            break;
        except ValueError:
                print("Input is not correct")

    print()
    while True:
        try:
            ibu = float(input('Vul het IBU gehalte in:'))
            ibu = round(ibu,1)
            print("Het IBU gehalte wordt afgerond naar: ", ibu)
            break;
        except ValueError:
                print("Input is not correct")

    user_input = [abv, ibu]

    return user_input


"""Functie die de afstanden van punt tot punt berekent en op volgorde terug geeft met de waardes van type bier"""
def searchShortesLentghToPoint(user_input, datarow):

    abv_user = user_input[0]
    ibu_user = user_input[1]

    distances = []

    for data in datarow:
        abv_data = data[0]
        ibu_data = data[1]
        type_of_beer = data[2]

        """Euclidean distance point to point berekent"""
        distance_input_to_point = sqrt((abv_user-abv_data)**2 + (ibu_user-ibu_data)**2)

        distances.append([distance_input_to_point, type_of_beer])

    distances.sort()

    return distances



def mainloop():
    dataset = load_csv("NewDatasetBeers.csv")
    data =  preparedata(dataset)

    user_input = askUserInput()

    distances = searchShortesLentghToPoint(user_input, data)
    for x in distances:
        print(x)




mainloop()