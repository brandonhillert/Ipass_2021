from csv import reader
from math import sqrt
import random

"""Laad het csv bestand in python zodat het bewerkt kan worden"""
def load_csv(filename):
	file = open(filename, "r")
	lines = reader(file)
	dataset = list(lines)
	return dataset

""""Zorgt ervoor dat de dataset in een list/dictionary komt zonder onnodige waardes ( bijv de Index) en creeert een coordinaat van 
de x ( ABV) en de y ( IBU)
Zo is het makkelijker om later ermee te werken"""
def prepare_data(dataset):
    dataframe = []

    for data in dataset[1:]:
        coordinate_x_abv = float(data[1])
        coordinate_y_ibu = float(data[2])
        type_of_beer = data[3]

        """Afronden naar 1 dec"""
        coordinate_x_abv = round(coordinate_x_abv, 1)

        dataframe.append([coordinate_x_abv, coordinate_y_ibu, type_of_beer])

    return dataframe

"""Functie die alle biertypes uniek in een lijst zet"""
def count_beer_types(data):

    list_of_beertypes = []

    for x in data:
        if x[2] not in list_of_beertypes:
            list_of_beertypes.append(x[2])

    return list_of_beertypes

"""Nog een functie die de waardes checken van de input ewn controleren net zo lang tot de input goed is"""
def ask_user_input():

    while True:
        try:
            abv = float(input('Vul het alcohol percentage ( ABV gehalte) van uw drankje in:'))
            abv = round(abv,1)

            break;
        except ValueError:
                print("Input is not correct")


    while True:
        try:
            ibu = float(input('Vul het IBU gehalte in:'))
            ibu = round(ibu,1)

            break;
        except ValueError:
                print("Input is not correct")



    user_input = [abv, ibu]

    return user_input

"""Functie die vraagt om een K value mee te geven"""
def ask_k_value():
    while True:
        try:
            k_value = int(input('Geef een K waarde voor het algoritme: '))
            break;
        except ValueError:
                print("Input is not correct")

    return k_value

"""Functie die de afstanden van punt tot punt berekent en op volgorde terug geeft met de waardes van type bier"""
def search_shortest_distance(user_input, datarow):

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

"""Functie die een die telt welke types ( neigbours) het meest in de buurt liggen"""
def count_frequency_neigbours(list_of_shortest_distances, list_of_beertypes, k_value):

    list_of_nearest_neigbours = []

    print("De waarde ligt het dichts in de buurt van:")
    for neighbours in list_of_shortest_distances[:k_value]:
        list_of_nearest_neigbours.append(neighbours[1])

        print(str(neighbours[1] +" "+ str(neighbours[0])))


    neighbours_with_frequency = []

    for neighbours in list_of_nearest_neigbours:

        frequency = list_of_nearest_neigbours.count(neighbours)
        neighbours_with_frequency.append([neighbours, frequency ])

    return neighbours_with_frequency


"""Vergelijkt de uitkomst van het algoritme met de daadwerkelijke biertype en geeft een slagingspercentage terug"""
def test_accuracy(k_value, data):
    """pakt de waardes 2 waardes uit de data lijst zonder het type erbij, het algoritme zal dan alleen nog kijken naar de nearest neighbour en
    niet naar zijn eigen type. Zo kunnen we kijken of biertypes een beetje gegroepeerd staan op basis van abv en ibu"""
    total_values = 0
    good_predictions = 0

    for x in data[:]:
        total_values = total_values + 1
        test_data = [x[0],x[1]]
        answer = x[2]

        prediction = algoritme(k_value, data, test_data)

        print("Correcte type:" + answer )

        if answer == prediction:
            good_predictions = good_predictions + 1

    accuracy_percentage_predictions = good_predictions/total_values * 100

    print("Het algoritme heeft een slagingspercentage van " + str(round(accuracy_percentage_predictions,1)) + "%")

    return round(accuracy_percentage_predictions,1)


"""Functie maakt een voorspelling op basis van een bepaalde K waarde. De waardes die het meest voorkomen binnen de K waardes, wordt de voorspelling
    Bij een gelijkspel wordt de lijst op alfabetische volgorde ingedeeld, en zal de eerst in alfabetische volgorde voorspellen """
def make_prediction_beertype(list_nearest_neighbours):
    highest_value = 0
    prediction = ""

    for data in list_nearest_neighbours:
        if data[1] > highest_value:
            highest_value = int(data[1])

            prediction = data[0]


    print("Voorspelling: " + prediction)

    return prediction

""""Functie het algoritme zijn werk laat doen en een uitkomst geeft van de K nearest neighbours"""
def algoritme(k_value, data, type_of_program):
    """De K value geeft aan hoe groot de straal is waarin de buren zich mogen bevinden om een classificatie uit te voeren
        Zodra deze waarde dus veranderd, kan het ook zijn dat de voorspellling veranderd."""
    list_of_beertypes = count_beer_types(data)
    distances = search_shortest_distance(type_of_program, data)
    list_neighbours_with_frequency = count_frequency_neigbours(distances, list_of_beertypes, k_value)
    prediction = make_prediction_beertype(list_neighbours_with_frequency)
    return prediction

"""Functie die de dataset splits in 5 gelijke stukken"""
def split_list(data):
    number_of_splits = int(len(data) / 5)

    for i in range(0, len(data), number_of_splits):
        yield data[i:i + number_of_splits]

"""Deze functie deelt de dataset op in 5 verschillende sets en test ze per 4 gemengd ( 80/20 ), """
def train_test_split(data):
    """"dataset wordt in 5 gesplits in gelijke lengtes"""
    split = list(split_list(data))

    k_value = ask_k_value()

    a = split[0]
    b = split[1]
    c = split[2]
    d = split[3]
    e = split[4]

    accuracy_values_sets = []

    subset_1 = a + b + c + d
    subset_2 = a + b + c + e
    subset_3 = a + b + d + e
    subset_4 = a + d + c + e
    subset_5 = b + c + d + e

    """
    Hieronder maak ik gebruik van de 80/20 verhouding BIJV:
    subset 1 is ABCD en de losse split is E, ABCD = 80 en E is 20
    Eerst wordt de subset getest hoe accuraat die is, en vervolgens wordt de losse split getest
    
    """
    accuracy_k_subset_1 = test_accuracy(k_value, subset_1)
    accuracy_k_subset_2 = test_accuracy(k_value, subset_2)
    accuracy_k_subset_3 = test_accuracy(k_value, subset_3)
    accuracy_k_subset_4 = test_accuracy(k_value, subset_4)
    accuracy_k_subset_5 = test_accuracy(k_value, subset_5)

    accuracy_k_split_a = test_accuracy(k_value, a)
    accuracy_k_split_b = test_accuracy(k_value, b)
    accuracy_k_split_c = test_accuracy(k_value, c)
    accuracy_k_split_d = test_accuracy(k_value, d)
    accuracy_k_split_e = test_accuracy(k_value, e)

    sum_subset = (accuracy_k_subset_1 + accuracy_k_subset_2 + accuracy_k_subset_3 + accuracy_k_subset_4 + accuracy_k_subset_5)
    sum_split = (accuracy_k_split_a + accuracy_k_split_b + accuracy_k_split_c + accuracy_k_split_d + accuracy_k_split_e)




    print("_________________RESULT_________________")
    print("K Value: " + str(k_value))
    print("Subset 1 accuracy: " + str(accuracy_k_subset_1)+ "  leftover split accuracy: " + str(accuracy_k_split_e ))
    print("Subset 2 accuracy: " + str(accuracy_k_subset_2)+ "  leftover split accuracy: " + str(accuracy_k_split_d ))
    print("Subset 3 accuracy: " + str(accuracy_k_subset_3)+ "  leftover split accuracy: " + str(accuracy_k_split_c ))
    print("Subset 4 accuracy: " + str(accuracy_k_subset_4)+ "  leftover split accuracy: " + str(accuracy_k_split_b ))
    print("Subset 5 accuracy: " + str(accuracy_k_subset_5)+ "  leftover split accuracy: " + str(accuracy_k_split_a ))
    print("")

    if sum_subset > sum_split:
        print("De value K= "+ str(k_value) + " acurater op de subset dan op de enkele split")
    else:
        print("De value K= " + str(k_value) + " acurater op de split dan op de subset")


"""Dit is de mainloop die het alles laat runnen"""
def mainloop():
    dataset = load_csv("NewDatasetBeers.csv")
    data = prepare_data(dataset)

    while True:
        try:
            print("1: Zelf input testen")
            print("2: Algoritme testen")
            print("3: Train split methode")


            choice = int(input("Ik kies voor optie: "))

            print("")
            if choice == 1:
                user_input = ask_user_input()
                k_value = ask_k_value()

                print("ABV: "+  str(user_input[0]) +" - IBU: "+ str(user_input[1]) +  " - K-VALUE: "+ str(k_value))
                print(" ")
                prediction = algoritme(k_value, data, user_input)
                break


            if choice == 2:
                k_value = ask_k_value()
                test_accuracy(k_value, data)
                break


            if choice == 3:
                dataset = load_csv("NewDatasetBeers.csv")
                data = prepare_data(dataset)
                train_test_split(data)
                break

        except ValueError:
                print("Input is not correct")

mainloop()










