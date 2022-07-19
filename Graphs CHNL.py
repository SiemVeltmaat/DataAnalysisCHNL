import pandas as pd
import json
import csv
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np

plt.close("all")

#Loading the data, change paths.
dfCities = pd.read_csv("C:/Users/Siem Veltmaat/Documents/Scriptie/CitiesNLCH4.csv", sep=';')
dataNL = json.load(open("C:/Users/Siem Veltmaat/Downloads/antennasNR.json"))
dataCH = json.load(open("C:/Users/Siem Veltmaat/Downloads/ch.bakom.mobil-antennenstandorte-5g_de.json"))

dfNL = pd.DataFrame(dataNL)
dfCH = pd.DataFrame(dataCH)
dfNL = dfNL.transpose()
header_listNL = ['ID', 'type', 'x', 'y', 'antennas', 'city', 'powerlevel']
header_listCH = ['type', 'geometry', 'properties', 'city', 'powerlevel']
dfNL = dfNL.reindex(columns = header_listNL)
dfCH = dfCH.reindex(columns = header_listCH)
dfCities = dfCities.astype({"min_lat": float})
dfCities = dfCities.astype({"min_lon": float})
dfCities = dfCities.astype({"max_lat": float})
dfCities = dfCities.astype({"max_lon": float})


#Filling the entire city column with Countryside, which means outside of the 15 major cities.
dfNL.fillna("Countryside", inplace=True)
dfCH.fillna("Countryside", inplace=True)

#print(dfCH)
#print(dfNL)
#print(dfCities)
#print(dfCH.dtypes)

antennaamountNL = len(dfNL)
antennaamountCH = len(dfCH)

#Filling the city column for the antennas with the corresponding cities for the Netherlands.
i=0
while i < antennaamountNL:
    k=0
    latNL = dfNL["x"].iat[i]
    lonNL = dfNL["y"].iat[i]
    # print(latNL)
    # print(lonNL)
    # print(i)
    while k < 15:
        if latNL > dfCities["min_lat"].iat[k] and latNL < dfCities["max_lat"].iat[k] and lonNL > dfCities["min_lon"].iat[k] and lonNL < dfCities["max_lon"].iat[k]:
            dfNL.iat[i, 5] = dfCities['name'].iat[k]
        k += 1
    i += 1
citycountNL = dfNL["city"].value_counts()
citiesNL = citycountNL.drop("Countryside")
# print(citiesNL)

#Creating a graph for the number of antennas per city in the Netherlands
cityAntennaNLGraph = citiesNL.plot(kind = "barh")
cityAntennaNLGraph.set_ylabel("City")
cityAntennaNLGraph.set_xlabel("Number of antennas")

#Filling the city column for the antennas with the corresponding cities for Switzerland.
j=0
while j < antennaamountCH:
    l=15
    coords = dfCH["geometry"].iat[j]
    coordsCH = coords["coordinates"]
    lonCH = coordsCH[0]
    latCH = coordsCH[1]
    # print(latCH)
    # print(lonCH)
    while l < 30:
        if latCH > dfCities["min_lat"].iat[l] and latCH < dfCities["max_lat"].iat[l] and lonCH > dfCities["min_lon"].iat[l] and lonCH < dfCities["max_lon"].iat[l]:
            dfCH.iat[j, 3] = dfCities['name'].iat[l]
        l += 1
    j += 1
citycountCH = dfCH["city"].value_counts()
citiesCH = citycountCH.drop("Countryside")
# print(citycountCH)

#Creating a graph for the number of antennas per city in Switzerland
cityAntennaCHGraph = citiesCH.plot(kind = "barh")
cityAntennaCHGraph.set_ylabel("City")
cityAntennaCHGraph.set_xlabel("Number of antennas")

#Filling the power column with the corresponding values for the Netherlands.
p=0
while p < antennaamountNL:
    propertiesNL = dfNL["antennas"].iat[p]
    antennaPropertiesNL = propertiesNL["0"]
    powerNL = antennaPropertiesNL["power"]
    if powerNL <= 10:
        dfNL.iat[p,6] = "Very Small"
    elif powerNL > 10 and powerNL <= 20:
        dfNL.iat[p,6] = "Small"
    elif powerNL > 20 and powerNL <= 30:
        dfNL.iat[p,6] = "Medium"
    elif powerNL > 30:
        dfNL.iat[p,6] = "Large"
    p += 1
powercountNL = dfNL["powerlevel"].value_counts()
# print(powercountNL)
powercountNL.plot.bar()

#Checking how many of the powerlevels correspond to the countryside in the Netherlands.
b = 0
vsNL = 0
sNL = 0
mNL = 0
gNL = 0
while b < antennaamountNL:
    if dfNL["city"].iat[b] == "Countryside":
        if dfNL["powerlevel"].iat[b] == "Very Small":
            vsNL += 1
        elif dfNL["powerlevel"].iat[b] == "Small":
            sNL += 1
        elif dfNL["powerlevel"].iat[b] == "Medium":
            mNL += 1
        elif dfNL["powerlevel"].iat[b] == "Large":
            gNL += 1
    b += 1
# print(vsNL)
# print(sNL)
# print(mNL)
# print(gNL)


#Filling the power column with the corresponding values for Switzerland.
o=0
while o < antennaamountCH:
    propertiesCH = dfCH["properties"].iat[o]
    powerCH = propertiesCH["powercode_de"]
    if powerCH == "Sehr Klein":
        dfCH.iat[o,4] = "Very Small"
    elif powerCH == "Klein":
        dfCH.iat[o,4] = "Small"
    elif powerCH == "Mittel":
        dfCH.iat[o,4] = "Medium"
    elif powerCH == "Gross":
        dfCH.iat[o,4] = "Large"
    o += 1
powercountCH = dfCH["powerlevel"].value_counts()
powercountCH.plot.bar()

# print(powercountCH)
powerCHGraph = powercountCH.plot.bar()
powerCHGraph.set_ylabel("Amount of antennas")
powerCHGraph.set_xlabel("Powerlevel")

#Checking how many of the powerlevels correspond to the countryside in Switzerland.
u = 0
vsCH = 0
sCH = 0
mCH = 0
gCH = 0
while u < antennaamountCH:
    if dfCH["city"].iat[u] == "Countryside":
        if dfCH["powerlevel"].iat[u] == "Very small":
            vsCH += 1
        elif dfCH["powerlevel"].iat[u] == "Small":
            sCH += 1
        elif dfCH["powerlevel"].iat[u] == "Medium":
            mCH += 1
        elif dfCH["powerlevel"].iat[u] == "Large":
            gCH += 1
    u += 1
# print(vsCH)
# print(sCH)
# print(mCH)
# print(gCH)



# print("The amount of antennas in the Netherlands:", antennaamountNL)
# print("The amount of antennas in Switzerland:", antennaamountCH)

#The graph for the amount of antennas per powerlevel per city in the Netherlands.
powerCityGraph = dfCities.drop(columns = ["min_lat","min_lon","max_lat","max_lon","population_amount"])
powerCityGraphNL = powerCityGraph.drop([15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
powerCityGraphCH = powerCityGraph.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

labelsNL = powerCityGraphNL["name"].unique()
vsNL = np.array([57,21,36,1,5,26,0,1,3,5,0,0,3,0,1])
sNL = np.array([10,0,2,1,1,5,0,0,2,0,0,0,1,0,0])
mNL = np.array([2,2,3,0,0,0,0,0,0,0,1,3,1,0,0])
gNL = np.array([546,267,309,72,84,183,34,44,98,59,60,25,97,23,88])


x = np.arange(len(labelsNL))
width = 0.3

fig, ax = plt.subplots()
rects1 = ax.bar(x , vsNL, width, label='Very small',bottom = gNL + mNL + sNL)
rects2 = ax.bar(x , sNL, width, label='Small', bottom = gNL + mNL)
rects3 = ax.bar(x , mNL, width, label='Medium', bottom = gNL)
rects4 = ax.bar(x , gNL, width, label='Large')

ax.set_ylabel('Number of antennas')
ax.set_title('Power of antennas per city')
ax.set_xticks(x, labelsNL, rotation = 90)
ax.legend()

#The graph for the amount of antennas per powerlevel per city in Switzerland.
labelsCH = powerCityGraphCH["name"].unique()
vsCH = np.array([144,25,11,25,12,5,9,3,2,6,1,0,1,0,0])
sCH = np.array([56,28,23,29,17,7,21,8,5,2,1,3,2,3,6])
mCH = np.array([359,139,143,127,135,67,50,50,77,47,21,12,22,24,31])
gCH = np.array([47,9,12,7,27,13,1,9,6,4,13,1,5,0,5])


x = np.arange(len(labelsCH))
width = 0.3

fig, ax = plt.subplots()
rects1 = ax.bar(x, vsCH, width, label='Very small', bottom = gCH + mCH + sCH)
rects2 = ax.bar(x, sCH, width, label='Small', bottom = gCH + mCH)
rects3 = ax.bar(x, mCH, width, label='Medium', bottom = gCH)
rects4 = ax.bar(x, gCH, width, label='Large')

ax.set_ylabel('Number of antennas')
ax.set_title('Power of antennas per city')
ax.set_xticks(x, labelsCH, rotation = 90)
ax.legend()

plt.tight_layout()
plt.show()