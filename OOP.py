from abc import ABC, abstractmethod
from datetime import date


class Employe(ABC) :
    
    def __init__(self,Nom, Matricule, Prenom ,anne_naiss) :
        self.nom=Nom
        self.Matricule=Matricule
        self.Prenom=Prenom
        self.anne_naiss=anne_naiss
    
       
    def __str__(self):
        return f"Nom: {self.nom}, Prenom: {self.Prenom}, Matricule: {self.Matricule}, anne_naiss: {self.anne_naiss}" 
    
    @abstractmethod 
    def  get_salaire(self) :
         pass
    
    
    
    
class Ouvrier(Employe) :
    def __init__(self,Nom, Matricule, Prenom ,anne_naiss,ann_entre) :
      super().__init__(Nom, Matricule, Prenom ,anne_naiss)   
      self.ann_entre=ann_entre
    
    
    def __str__(self):
       return f"{super().__str__()}, année d'entrée : {self.ann_entre}"    
   
    def  get_salaire(self) :
        Ancienne_ann=annee = date.today().year-self.ann_entre
        smig=2500
        salaire = smig + (Ancienne_ann) * 100
        if salaire < smig *  2 : return salaire
        
   
      
class Cadre (Employe):
    
    def __init__(self,Nom, Matricule, Prenom ,anne_naiss,indice) :
      super().__init__(Nom, Matricule, Prenom ,indice)   
      self.indice=indice
    
    
    def  get_salaire(self) :
        Indice_1 = 13000 
        Indice_2 =15000 
        Indice_3 =17000 
        
        if self.indice == 1:
           return Indice_1
        elif self.indice == 2:
           return Indice_2
        elif self.indice == 3:
           return Indice_3
      
      
        
    def __str__(self):
      return f"{super().__str__()},indice : {self.indice}"
    
    
    
    
class Patron(Employe)  :   
    def __init__(self,Nom, Matricule, Prenom ,anne_naiss,CA) :
      super().__init__(Nom, Matricule, Prenom ,CA)   
      self.CA=CA
    
    
    
    
    def __str__(self):
     return f"{super().__str__()},chiffre d'affaire : {self.CA}"
    
    def  get_salaire(self) :
         return   self.CA * 0.1




p1=Ouvrier("oubelkacem", "A127854", "Ahmed" ,2001,2012)
p2=Cadre("oubelkacem", "A127854", "Ahmed" ,2001,1)
p3=Ouvrier("oubelkacem", "A127854", "Ahmed" ,"2001",15000)
print(f"{p1} avec un saliare : {p1.get_salaire()}")


