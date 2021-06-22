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

    """De 5 dichtsbijzijnde punten ( neighbours )"""
    print("De waarde ligt het dichts in de buurt van:")
    for neighbours in list_of_shortest_distances[:k_value]:
        list_of_nearest_neigbours.append(neighbours[1])
        print(neighbours)

    neighbours_with_frequency = []

    for neighbours in list_of_nearest_neigbours:

        frequency = list_of_nearest_neigbours.count(neighbours)

        neighbours_with_frequency.append([neighbours, frequency ])


    return neighbours_with_frequency

"""Functie maakt een voorspelling op basis van een bepaalde K waarde. De waardes die het meest voorkomen binnen de K waardes, wordt de voorspelling"""
def make_prediction_beertype(list_nearest_neighbours):
    highest_value = 0
    prediction = ""

    for data in list_nearest_neighbours:
        if data[1] > highest_value:
            highest_value = int(data[1])
            prediction = data[0]

    """Print de nearest neighbours, aantal afhankelijk van K waarde"""
    """
        for neighbour in list_nearest_neighbours:
        print(neighbour)
    """


    print("Voorspelling: " + prediction)

    return prediction

"""Vergelijkt de uitkomst van het algoritme met de daadwerkelijke biertype en geeft een slagingspercentage terug"""
def test_accuracy(data):
    """pakt de waardes 2 waardes uit de data lijst zonder het type erbij, het algoritme zal dan alleen nog kijken naar de nearest neighbour en
    niet naar zijn eigen type. Zo kunnen we kijken of biertypes een beetje gegroepeerd staan op basis van abv en ibu"""
    total_values = 0
    good_predictions = 0

    for x in data[:]:
        total_values = total_values + 1

        test_data = [x[0],x[1]]
        answer = x[2]


        prediction = algoritme(data, test_data)


        print("Correcte type:" + answer )

        if answer == prediction:
            good_predictions = good_predictions + 1

    accuracy_percentage_predictions = good_predictions/total_values * 100

    print("Het algoritme heeft een slagingspercentage van " + str(round(accuracy_percentage_predictions,1)) + "%")

""""Functie het algoritme zijn werk laat doen en een uitkomst geeft van de K nearest neighbours"""
def algoritme(data, type_of_program):
    """De K value geeft aan hoe groot de straal is waarin de buren zich mogen bevinden om een classificatie uit te voeren
        Zodra deze waarde dus veranderd, kan het ook zijn dat de voorspellling veranderd."""
    k_value = 5

    list_of_beertypes = count_beer_types(data)
    distances = search_shortest_distance(type_of_program, data)
    list_neighbours_with_frequency = count_frequency_neigbours(distances, list_of_beertypes, k_value)
    prediction = make_prediction_beertype(list_neighbours_with_frequency)
    return prediction

"""Dit is de mainloop die het alles laat runnen"""
def mainloop():
    dataset = load_csv("NewDatasetBeers.csv")
    data = prepare_data(dataset)

    while True:
        try:
            choice = int(input("Kies je voor 1 zelf input invoeren of voor 2 algoritme testen?"))
            if choice == 1:
                user_input = ask_user_input()
                algoritme(data, user_input)
                break
            if choice == 2:
                test_accuracy(data)
                break
        except ValueError:
                print("Input is not correct")

mainloop()


