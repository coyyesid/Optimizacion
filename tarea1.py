import pandas as pd
import gurobipy as gp
import csv
from gurobipy import GRB
from gurobipy import *

#Leer y ordenar la informacion del archivo
data = pd.read_csv('./Cicla/Cicla.csv', header=None, names= ['coorx','coory','rojo','verde','azul'])

#Rango de pixeles
coorx = range(0,data['coorx'].max()+1)
coory = range(0,data['coory'].max()+1)

#Parametros
#se crean diccionarios vacios donde se guarda la informacion de la intensidad del rojo, verde y azul de cada pixel

r, v, az = {}, {}, {}

for i,j in [(i, j) for i in coorx for j in coory]:
    r[i,j], v[i,j], az[i,j] = data.loc[(data['coorx'] == i) & (data['coory'] == j)].iloc[0, 2:5]

#Se crea un diccionario con el que se recorreran las coordenadas
P = list(r.keys())

#se crea el modelo con los parametros establecidos
m = Model()

#se asignan las varibales con las que se trabajaran y se les la naturaleza que corresponda en este caso tenemos 
#una varaible binaria que me identifica que valor tomar y tres variables enteras que corresponde a la intensidad en cada posicion 
x = m.addVars(P, vtype = GRB.BINARY, name = 'v')
a = m.addVar(vtype= GRB.INTEGER, name= "a")
b = m.addVar(vtype = GRB.INTEGER, name = 'b')
c = m.addVar(vtype = GRB.INTEGER, name = 'c')

for (i,j) in P:
    m.addConstr(255* x[i,j] - r[i,j] <= a)
    m.addConstr(-255* x[i,j] + r[i,j] <= a)
    m.addConstr(255* x[i,j] - v[i,j] <= b)
    m.addConstr(-255* x[i,j] + v[i,j] <= b)
    m.addConstr(255* x[i,j] - r[i,j] <= c)
    m.addConstr(-255* x[i,j] + r[i,j] <= c)

m.setObjective(a+b+c, GRB.MINIMIZE)
m.update()
m.optimize()

#se crea una nuevo archivo donde se guarda la informacion de la imagen que se paso a blanco y negro
f = open('Cicla/Cicla_blanco_negro',"a", newline="")
archivo_nuevo = csv.writer(f)

for i,j in P:
    if (x[i,j].x==0):
        tup = (i,j,0,0,0)
        archivo_nuevo.writerow(tup)
    else:
        tup = (i,j,255,255,255)
        archivo_nuevo.writerow(tup)

f.close()
