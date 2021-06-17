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

        """Afronden naar 1 dec"""
        coordinate_x_abv = round(coordinate_x_abv, 1)

        typeOfBeer = data[3]

        coordinate = [coordinate_x_abv, coordinate_y_ibu]
        set = [coordinate, typeOfBeer]
        dataframe.append(set)

    return dataframe


def askUserInput():

    """Nog een functie die de waardes checken van de input ewn controleren net zo lang tot de input goed is"""
    print('Vul het abv gehalte met 1 decimaal:')
    abv = input()

    print('Vul het IBU gehalte in:')
    ibu = float(input())

    userInput = [abv, ibu]

    return userInput



def searchShortesLentghToPoint(datarow):

    abv_main = 6.3
    ibu_main = 50

    distances = []

    for data in datarow:
        for point in data[0]:
            print(point)



    '''def distanceBetweenTwoPoints():'''
def mainloop():
    dataset = load_csv("NewDatasetBeers.csv")
    data =  preparedata(dataset)



    searchShortesLentghToPoint(data)






mainloop()