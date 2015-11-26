import os
import math


#cette fonction permet de retrouver le numero de colonne
#dans un fichier CSV, a partir de l'adresse du CSV et du
#nom de l'entete de la colonne
def identifierEntete(adresseFichier, entete):
	numColonne=0
	fichier=open(adresseFichier,'r')
	premiereLigne=fichier.read().split("\n")[0].split("\t") #extraction de la premiere ligne et conversion en liste
	for element in premiereLigne:
		if element==entete:
			break
		else:
			numColonne+=1
	fichier.close()
	return numColonne
	
def nombreLignes(adresseFichier):
	fichier=open(adresseFichier,"r")
	nombreLignes=len(fichier.read().split("\n"))
	fichier.close()
	return nombreLignes
	
def nombreColonnes(adresseFichier):
	fichier=open(adresseFichier,"r")
	nombreColonnes=len(fichier.read().split("\n")[0].split("\t"))
	fichier.close()
	return nombreColonnes
	
#cette fonction permet d'identifer quels sont les noeuds qui sont
#relies au noeuds "noeud". Elle renvoie une liste de str	
def parcoursProches(adresseLiens,noeud):
	numA=identifierEntete(adresseLiens,"NODEA")
	numB=identifierEntete(adresseLiens,"NODEB")
	nLignes=nombreLignes(adresseLiens)
	nColonnes=nombreColonnes(adresseLiens)
	noeud=int(noeud)
	
	liste=[]
	#print(liste)
	
	fichier=open(adresseLiens,"r")
	contenu=fichier.read().split()
	fichier.close()
	
	#on parcours les colonne "Noeud A" et "Noeud B" si on retrouve
	#l'identifiant du noeud origine, on recopie l'autre extremite du
	#lien dans la liste
	i=1
	while i < nLignes:
		if contenu[i*nColonnes+numA]==str(noeud):
			liste=liste+[contenu[i*nColonnes+numB]]
			
		elif contenu[i*nColonnes+numB]==str(noeud):
			liste=liste+[contenu[i*nColonnes+numA]]
			
		i+=1

	#print("le noeud est : ", noeud,"  est les noeuds proches sont ", liste)
	return liste	

#cette fonction va servir a creer les etiquettes temporaires,
#on cree une etiquette par noeuds.
#structure de l'etiquette : (ID du noeud, cout, antecedant)	
def creationEtiquette(adresseNoeuds,noeudInitial):
	numID=identifierEntete(adresseNoeuds,"NODE")
	nLignes=nombreLignes(adresseNoeuds)
	nColonnes=nombreColonnes(adresseNoeuds)
	
	fichier=open(adresseNoeuds,"r")
	contenu=fichier.read().split()
	fichier.close()
	
	etiquette=[]
	noeudInitial=str(noeudInitial)
	i=1
	while i<nLignes:
		if contenu[i*nColonnes+numID]!=noeudInitial:
			etiquette=etiquette+[[contenu[i*nColonnes+numID],0,"-"]]
		i+=1

	#print("etiquette avant tri",etiquette)
	etiquette=sorted(etiquette)
	#print("apres tri" ,etiquette)
	return etiquette


#etape de l'algorithme de Djikstra qui consiste a transferer 
#l etiquette a plus faible cout de la liste temporaire a la liste
#definitive. Elle renvoie aussi l'identifiant du prochain noeud pour
#l'etape suivante		
def choixProchainNoeud(etiquettesTemporaires,etiquettes):
	n=len(etiquettesTemporaires)
	i=0
	choixEtiquette=0
	
	while i<n:
		if etiquettesTemporaires[i][2]!='-' and etiquettesTemporaires[choixEtiquette][2]=='-':
			choixEtiquette=i
		elif etiquettesTemporaires[i][2]!='-' and etiquettesTemporaires[i][1]<etiquettesTemporaires[choixEtiquette][1]:
			choixEtiquette=i
		i+=1
	#print("etiquette choisie pour porchaine noeus", etiquettesTemporaires[choixEtiquette])	
	etiquettes=etiquettes.append(etiquettesTemporaires[choixEtiquette])
	prochainNoeud=etiquettesTemporaires[choixEtiquette][0]
	etiquettesTemporaires.remove(etiquettesTemporaires[choixEtiquette])
	
	#print(etiquettes)
	#print(etiquettesTemporaires)
	#print("prochain noeud" ,prochainNoeud)
	return prochainNoeud


#renvoie l'identifiant du lien correspondant aux noeuds entres, 
#renvoie "False" si lien inexistant
def identifierLien(noeudA,noeudB, adresseLiens):
	numLINK=identifierEntete(adresseLiens,"LINK")
	numA=identifierEntete(adresseLiens,"NODEA")
	numB=identifierEntete(adresseLiens,"NODEB")
	nLignesLiens=nombreLignes(adresseLiens)
	nColonnesLiens=nombreColonnes(adresseLiens)

	fichier=open(adresseLiens,"r")
	contenuLiens=fichier.read().split()
	fichier.close()

	noeudA=str(noeudA)
	noeudB=str(noeudB)

	i=1
	while i < nLignesLiens:
		if contenuLiens[i*nColonnesLiens+numA]==noeudA and contenuLiens[i*nColonnesLiens+numB]==noeudB:
			idLien=contenuLiens[i*nColonnesLiens+numLINK]
		elif contenuLiens[i*nColonnesLiens+numA]==noeudB and contenuLiens[i*nColonnesLiens+numB]==noeudA:	
			idLien=contenuLiens[i*nColonnesLiens+numLINK]
		i+=1

	return idLien
#	if noeudA in contenuLiens:
#		indiceA=contenuLiens.index(noeudA)
#		print(indiceA)

#calcul a partir des coordonnees le cout.
#A FAIRE : prendre le cas ou il y a deja un renseignement usr le cout
def calculCouts(adresseLiens, adresseNoeuds):
	numLINK=identifierEntete(adresseLiens,"LINK")
	numA=identifierEntete(adresseLiens,"NODEA")
	numB=identifierEntete(adresseLiens,"NODEB")
	numNODE=identifierEntete(adresseNoeuds,"NODE")
	numX=identifierEntete(adresseNoeuds,"X")
	numY=identifierEntete(adresseNoeuds,"Y")
	#print("numLINK ", numLINK,"numA ", numA,"numB ", numB,"numX ", numX,"numY ", numY)
	nLignesLiens=nombreLignes(adresseLiens)
	nColonnesLiens=nombreColonnes(adresseLiens)
	nLignesNoeuds=nombreLignes(adresseNoeuds)
	nColonnesNoeuds=nombreColonnes(adresseNoeuds)

	fichier=open(adresseLiens,"r")
	contenuLiens=fichier.read().split()
	fichier.close()

	fichier=open(adresseNoeuds,"r")
	contenuNoeuds=fichier.read().split()
	fichier.close()

	i=1
	couts=[]
	while i<nLignesLiens:
		noeudA=str(contenuLiens[i*nColonnesLiens+numA])
		noeudB=str(contenuLiens[i*nColonnesLiens+numB])
		j=1

		while j<nLignesNoeuds:
			temp=str(contenuNoeuds[j*nColonnesNoeuds+numNODE])
			if noeudA==temp:
				indiceLigneA=j
			elif noeudB==temp:
				indiceLigneB=j
			j+=1
			
		xA=int(contenuNoeuds[indiceLigneA*nColonnesNoeuds+numX])
		yA=int(contenuNoeuds[indiceLigneA*nColonnesNoeuds+numY])
		xB=int(contenuNoeuds[indiceLigneB*nColonnesNoeuds+numX])
		yB=int(contenuNoeuds[indiceLigneB*nColonnesNoeuds+numY])
		#print("nouad A ",noeudA," noeud B ",noeudB, "indices respec ",indiceLigneA,indiceLigneB)
		#print("coordonnee A",xA,yA,"  coodronnee B ", xB,yB)

		coutUnitaire=math.sqrt(math.pow(xA-xB,2)+math.pow(yA-yB,2))
		coutUnitaire=float(coutUnitaire)
		idLien=contenuLiens[i*nColonnesLiens+numLINK]
		#print("idLien : ", idLien, "et coutassocie ",coutUnitaire,"\n")
		couts=couts+[idLien,coutUnitaire]
		i+=1
	return couts	

#fonction permettait d'aller chercher dans la liste des couts, le cout 
#associe au lien demande
def identificationCoutUnitaire(couts,lien):
	lien=str(lien)
	indice=couts.index(lien)
	#print("lindice est " ,indice)
	coutUnitaire=couts[indice+1]
	#print("le cout unitaire est ", coutUnitaire)

	return coutUnitaire

#fonction permettant d aller chercher dans la liste d etiquette definitive le cout necessqire
#pour aller jusqu a l antecedant
def identificationCoutAntecedant(etiquette, noeudAntecedant):
	nEtiquette=len(etiquette)
	i=0
	while i<nEtiquette:
		if str(etiquette[i][0])==str(noeudAntecedant):
			coutAntecedant=etiquette[i][1]
			i=nEtiquette
		else:
			i+=1
	if i==0:
		coutAntecedant=0		
	coutAntecedant=float(coutAntecedant)
	return coutAntecedant				

#element clef du progrqmme : cette fonction met a jour les etiquettes temporaires 
#et renvoie le noeud a partir duquel il faudra faire l'etape suivante
def etapeDjikstra(etiquetteTemp,etiquette,noeud,adresseNoeuds,adresseLiens,couts):
	listeVoisins=parcoursProches(adresseLiens,noeud)
	nEtiquette=len(etiquetteTemp)
	#print('etiquetttes ', etiquetteTemp)
	#print("les voisins : ",listeVoisins)
	#print("netiquette", nEtiquette)
	#print("noeud initial",noeud)
	for node in listeVoisins:
		i=0
		node=int(node)
		while i<nEtiquette:
			if node==int(etiquetteTemp[i][0]):
				lien=identifierLien(noeud,node,adresseLiens)
				coutAntecedant=identificationCoutAntecedant(etiquette,noeud)
				coutUnitaire=identificationCoutUnitaire(couts,lien)
				#print("etiqette avant modification ", etiquetteTemp[i], "et cout unitaire ", coutUnitaire)
				coutTemp=float(coutAntecedant)+float(coutUnitaire)
				if coutTemp<etiquetteTemp[i][1] and etiquetteTemp[i][2]!='-':
					etiquetteTemp[i][2]=str(noeud)
					etiquetteTemp[i][1]=coutTemp
				elif etiquetteTemp[i][2]=='-':
					etiquetteTemp[i][2]=str(noeud)
					etiquetteTemp[i][1]=coutTemp	
				#print("etiquette apres modif ", etiquetteTemp[i])
			i+=1
	prochainNoeud=choixProchainNoeud(etiquetteTemp,etiquette)
	return prochainNoeud

def Djikstra(noeudInitial,adresseNoeuds,adresseLiens,couts):
	
	etiquette=[]
	etiquetteTemp=creationEtiquette(adresseNoeuds,noeudInitial)
	#initialisation
	prochainNoeud=etapeDjikstra(etiquetteTemp,etiquette,noeudInitial,adresseNoeuds,adresseLiens,couts)
	#print(prochainNoeud)				

	while etiquetteTemp!=[]:
		prochainNoeud=etapeDjikstra(etiquetteTemp,etiquette,prochainNoeud,adresseNoeuds,adresseLiens,couts)
		#print(prochainNoeud)

	return etiquette

def totalDjikstra(adresseNoeuds,adresseLiens):
	couts=calculCouts(adresseLiens,adresseNoeuds)
	#print("cout",couts)
	fichier=open(adresseNoeuds,"r")
	contenu=fichier.read().split()
	fichier.close()

	numNODE=identifierEntete(adresseNoeuds,"NODE")
	nColonnes=nombreColonnes(adresseNoeuds)
	nNoeuds=nombreLignes(adresseNoeuds)-1

	
	reponse=open("reponse.txt","w")
	reponse.write('ORIGIN\tDEST\tCOST\tPREVIOUS_NODE\n')
	for i in range(nNoeuds):
		noeudInitialTemporaire=contenu[(1+i)*(nColonnes)+numNODE]
		reponseDjikstra=Djikstra(noeudInitialTemporaire,adresseNoeuds,adresseLiens,couts)
		#print(reponseDjikstra)
		for j in reponseDjikstra:
			reponse.write(str(contenu[(i+1)*nColonnes+numNODE])+"\t")
			for k in j:
				reponse.write(str(k)+"\t")
			reponse.write("\n")	
	reponse.close()

			