#!/usr/bin/env python
# coding: utf-8

"""
Created on Fri Nov 18 08:45:16 2022

@author: Grunsky

@module: DLMDWPM01

@description: main programm. 

@purpose: evaluate ideal functions for a set of training data (1) and assign 
    values of a test-dataset to those ideal functions (2)

@details: Used criteria for evaluation:
    (1) to match training data and ideal functions: 
        minimum MeanSquaredError (MSE)
    (2) to match ideal functions and test data: 
        precalculated MSE (1) * SquareRoot(2)

@Python_Version: python: 3.9.13 (main, Aug 25 2022, 23:51:50) 
"""

### Mögliche Klassen
# Plot Klasse
# 


# # Klassen, Konstruktor, Dekorator, Setter, Vererbung

# In[17]:


# PKW-Klasse erneut definieren
class Vehicle():
    # Konstruktor definieren
    def __init__(self, color = "blue", use_type = "pkw", current_speed = 0):
        self.color = color
        self.use_type = use_type
        self.current_speed = current_speed
    
    # Methode zur Beschleunigung hinzufügen
    def increase_speed(self, increment=5.0):
        self.current_speed += increment
    
    # in einer Funktion die Beschreibung aus initiierten
    # Attributen zusammensetzen und diese als
    # Attribut behandeln
    @property
    def description(self):
        return self.color + ' ' + self.use_type
    
    # eine Setter-Methode zur Änderung von Attributen
    # auf Basis der Beschreibung definieren
    @description.setter
    def description(self, desc):
        color, use_type = desc.split(" ")
        self.color = color
        self.use_type = use_type


# In[13]:


my_car = Vehicle("pink", "caravan")


# In[45]:



# Attribute anzeigen
print("Color:", my_car.color)
print("Use Type:", my_car.use_type)
print("Description:", my_car.description)
print("Current Speed:", my_car.current_speed)


# In[15]:


# die Beschreibung ändern
my_car.description = "ocher van"
# Attribute anzeigen
print("Color:", my_car.color)
print("Use Type:", my_car.use_type)
print("Description:", my_car.description)
type(my_car)


# In[43]:


# Vererbung

# Eine Sub-Klasse anlegen
# Die Subklasse Car verfügt zunächst über keine eigenen Attribute und Methoden, was wir mit dem pass-Statement angeben.
class Lfz(Vehicle):
    pass

# Kind-Klasse definieren
class Car(Vehicle):
    # Methoden-Überschreibung
    def increase_speed(self, increment=10.0):
        self.current_speed += increment

# eine weitere Kind-Klasse definieren
# Kind-Klasse definieren
class Bike(Vehicle):
    # Methoden-Überschreibung
    def increase_speed(self, increment=2.0):
        self.current_speed += increment

# zwei Objekte auf Basis der beiden Subklassen generieren
my_car = Car()
my_bike = Bike(use_type = "Bike")
print(my_bike.description)


# In[46]:


## Neues Attribut für Kind-Klasse
'''
Dieses Attribut definieren wir über die Konstruktor-Methode __init__. Inner-
halb dieses Konstruktors muss aber nicht nur das neue Attribut n_doors, sondern auch
die Attibute der Eltern-Klasse für jede Instanz dieser Klasse angelegt werden. Wir könn-
ten den Code des Konstruktors aus der Eltern-Klasse kopieren und in den Konstruktor
der Kind-Klasse einfügen. Das würde allerdings zu redundantem Code führen, was wir
unbedingt vermeiden wollen. Glücklicherweise ist sich unsere Kind-Klasse Car über
den Konstruktor der Eltern-Klasse Vehicle bewusst und kann auf diesen zugreifen.
Anstatt alle Attribute der Eltern-Klasse im Konstruktor der Kind-Klasse erneut zu pro-
grammieren, können wir für diese Attribute einfach den Konstruktor der Eltern-Klasse
via Punkt-Notation, Vehicle.__init__(), aufrufen. Der gesamte Code für die Kind-
Klasse könnte dann wie folgt aussehen.
'''
# Eine Sub-Klasse mit angepassten Attributen anlegen
class Juhu(Vehicle):
    # Konstruktor-Methode definieren
    def __init__(self, n_wheels=10,         n_doors=3):
        
        # Konstruktor-Methode der Elternklasse ausführen
        Vehicle.__init__(self, n_wheels, current_speed)
        
        # angepasste Konstruktor-Methode der
        # Kind-Klasse ausführen
        self.n_doors = n_doors


# In[47]:


my_juhu = Juhu()
print(my_juhu.current_speed)


# In[21]:


# beide Objekte 7-fach beschleunigen
for i in range(7):
    my_car.increase_speed()
    my_bike.increase_speed()

# aktuelle Geschwindigkeiten ausgeben
print("PKW-Geschwindigkeit:", my_car.current_speed)
print("Fahrrad-Geschwindigkeit:", my_bike.current_speed)


# #    # öffentliche, private und geschützte Attribute

# In[30]:


# eine Fahrzeug-Klasse definieren
class Kfz():
    # Attribute per Konstruktor anlegen
    def __init__(self, n_wheels=4, increment=10, type="car"):

        # ein "öffentliches" Attribut anlegen
        self.n_wheels = n_wheels

        # ein "privates" Attribut anlegen, Schreibweise deutet nur auf die beabsichtigte Verwendung hin
        # das Attribut kann jedoch ausgegeben und verändert werden.
        self._increment = increment

        # ein "geschütztes" Attribut anlegen
        self.__type = type

# eine Instanz der Klasse erzeugen
my_pkw = Kfz()
dir(my_pkw)


# "geschütztes" Attribut ausgeben
# !!! ACHTUNG: NIEMALS AUF DIESE WEISE
# AUF EIN GESCHÜTZTES ATTRIBUT ZUGREIFEN !!!
print(my_pkw._Kfz__type) # NIEMALS SO PROGRAMMIEREN !!!

Beispielsweise wird das Attribut __type
nicht nur vor unserem print()-Befehl hinter dem Namen _Vehicle__type versteckt,
sondern auch von erbenden Kind-Klassen. Auf diese Weise können wir Kind-Klassen
mit gleichnamigen Attributen vergeben, wenn diese nur für eine Subklasse zielführend
sind. Wir könnten beispielsweise auf Basis der Eltern-Klasse Vehicle eine Kindklasse
Car definieren, die das geschütze Attribut _Car__type mit dem Wert Family Car trägt.
Auf diese Weise sind wir auch unabhängig von den Klassennamen.



# eine Fahrzeug-Klasse definieren
class SubKfz(Kfz):
    # Attribute per Konstruktor anlegen
    #def __init__(self, n_wheels=4, increment=10, type="newcar"):
    def __init__(self, type="newcar"):
        # ein "öffentliches" Attribut anlegen
        #self.n_wheels = n_wheels
        # ein "privates" Attribut anlegen
        #self._increment = increment
        # ein "geschütztes" Attribut anlegen
        self.__type = type

    # Setter für "geschützes" Attribut definieren
    def setType(self, type):
        self.__type = type
    
    # Getter für "geschützes" Attribut definieren
    def getType(self):
        print(self.__type)


# In[40]:


# eine Instanz der Klasse erzeugen
my_kfz = SubKfz()
# auf "geschütztes" Attribut zugreifen
my_kfz.getType()
# console output: car
dir(my_kfz)
print(my_kfz.n_wheels)

