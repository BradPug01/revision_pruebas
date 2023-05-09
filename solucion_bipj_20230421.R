library(readxl)
library(readr)
library(tidyverse)
library(psych)
library(ggplot2)
library(dplyr)
#Ejercicio 1
#a)
Base1<-read_csv2("INEC_Encuesta Estructural Empresarial_Tomo I_2021.csv") #se uso read_csv2 pues el archivo estaba delimitado por ;
#la base la guardé en la misma carpeta que donde tengo este proyecto, por tanto al correr se debería cambiar la base de datos.
view(Base1)
#b)
diezfilas=Base1[1:10,]
print(diezfilas)
#c)
id_estable<-Base1$id_empresa
act_econ<-Base1$des_letra
prov<-Base1$provincia
print(id_estable)
print(act_econ)
print(prov)
#########################################################
#Ejercicio 2
#Aquí tuve que ver la base de datos pues no sabía cual era exactamente la variable sobre la cual trabajar
#a)
summary(Base1$v5090)
sd(Base1$v5090)#summary no mostraba la desviación estandar 

describe.by(Base1$v5090)#esta me muestra todos 
#b)
n_total<-count(Base1, provincia)
print(n_total)
##########################################################
#Ejercicio 3
#a)
#Aqui surgió un problema pues no sabiía que número de provincia correspondia a Pichincha, pero luego de consultar resultó ser la 17
Pic=filter(Base1,provincia==17)
nPic=count(group_by(Pic,des_letra))
print(nPic)
#b)
nt=group_by(Pic,des_letra)%>%
  summarise(prom_tra=mean(v5090))
print(nt)
###########################################################
#Ejercicio 4
Base12=Base1%>%
  mutate(
    traba50=ifelse(v5090>=50,1,0)
  )
#a)
np=filter(Base12,traba50==1)
numero_empresasprov50=count(group_by(np,provincia))
print(numero_empresasprov50)
#b)
numero_empresasprov=count(group_by(Base1,provincia))
print(numero_empresasprov)
porcentajes=(numero_empresasprov50$n/numero_empresasprov$n)*100
numero_empresasprov50$Porcentajes=porcentajes
print(numero_empresasprov50)
#####################################################################
#Ejercicio 5
#Como la base tiene datos hasta 2019, suopondremos que esta es el año más alto
#a)
Base13=Base1%>%
  mutate(
    antiguedad=ifelse(anio_ruc_dis<2009,1,0)
  )
#b)
Base14=filter(Base13,antiguedad>0 & v5090>20) #base con la info de aquellos antiguos y con mas de 25 trabaja.

####################################################################
#EJERCICIOS SOBRE VISUALIZACIÓN DE DATOS
####################################################################
#Ejercicio 1
#El problema aquí es que no se sabe qué codigo corresponde a cada provincia, por tanto se tuvo que investigar
prv=transmute(numero_empresasprov,provincia=case_when(provincia=='01'~'Azuay',
                                         provincia=='02'~'Bolívar',
                                         provincia=='03'~ 'Cañar',
                                         provincia=='04'~ 'Carchi',
                                         provincia=='05'~ 'Cotopaxi',
                                         provincia=='06'~ 'Chimborazo',
                                         provincia=='07'~ 'El Oro',
                                         provincia=='08'~ 'Esmeraldas',
                                         provincia=='09'~ 'Guayas',
                                         provincia=='10'~ 'Imbabura',
                                         provincia=='11'~ 'Loja',
                                         provincia=='12'~ 'Los Rios',
                                         provincia=='13'~ 'Manabí',
                                         provincia=='14'~ 'Morona Santiago',
                                         provincia=='15'~ 'Napo',
                                         provincia=='16'~ 'Pastaza',
                                         provincia=='17'~ 'Pichincha',
                                         provincia=='18'~ 'Tungurahua',
                                         provincia=='19'~ 'Zamora',
                                         provincia=='20'~ 'Galápagos',
                                         provincia=='21'~ 'Sucumbíos',
                                         provincia=='22'~ 'Orellana',
                                         provincia=='23'~ 'Santo Domingo',
                                         provincia=='24'~ 'Santa Elena'))
numero_empresasprov$provincianame=prv
colnames(numero_empresasprov50)<-c('nprovincia','n','Porcentaje','Provincia')
ggplot(numero_empresasprov)+geom_bar(aes(x=provincianame$provincia,y=n),stat="identity")+labs(x="Provincia",y='Número de empresas')+theme(axis.text = element_text(angle = 90))


#############################################################################################################

#Ejercicio 2

#Revisando la base de datos encontre la variable "valag" que se referiía al valor agregado solamente
valor_agg=group_by(Base1,provincia)%>%
  summarise(valoragre=sum(valag))
print(valor_agg)
numero_empresasprov$valagg=valor_agg$valoragre
ggplot(numero_empresasprov)+geom_point(aes(x=n,y=log(valagg),col=provincianame$provincia))+labs(title="Relación entre número de embresas y valor agregado",x="Empresas",y='log(valor agregado)',col='Provincia')
#Decidí hacerle una transformacion logaritmica, de base e, al eje y pueto que los valores del mismo estabn por arriba del millon en algunos datos 
# y no permitían una buena visualización, para las conclusiones se debería tomar en cuanta esto.


