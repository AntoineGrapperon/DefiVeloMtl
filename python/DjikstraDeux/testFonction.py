import os
from deffonction import *

fichier=open("links.txt","r")
contenu=fichier.read()
print(contenu)
fichier.close()

#etiquette=[]

#etiq=creationEtiquette("nodes.txt",1)
#print(etiq)

#list1=[[1,4,5],[2,2,1]]
#list2=[]
#n=choixProchainNoeud(list1,list2)
#print ("list1 ",list1)
#print ("list2 ",list2)
#print("n", n)

couts=calculCouts("links.txt","nodes.txt")
#print(couts)
#identificationCoutUnitaire(couts,1)
#print("etiquette ", etiquette)
#print("etiquette temporaire ",etiq)
#n=etapeDjikstra(etiq,etiquette,1,"nodes.txt","links.txt",couts)
#print("etiquette ", etiquette)
#print("etiquette temporaire ",etiq)
#m=etapeDjikstra(etiq,etiquette,n,"nodes.txt","links.txt",couts)
#print("etiquette ", etiquette)
#print("etiquette temporaire ",etiq)
#print("prochain noeud ", n, "et",m)
#lien=identifierLien(1,2,"links.txt")
#print("idLIend est " , lien)

#etiquette=Djikstra(1,'nodes.txt',"links.txt",couts)
#print("etiquette ",etiquette)

totalDjikstra("nodes.txt","linksAlpha.txt")

os.system("pause")