from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime, Text, func, desc, or_, and_, extract
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import sessionmaker

# ==========================================
# 1. CONFIGURATION DE LA BASE DE DONNÉES
# ==========================================
DATABASE_URI = 'postgresql://postgres:mathinfo@localhost:5432/restaurant_db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# # # ==========================================
# # # 2. DÉFINITION DES TABLES (MODÈLES)
# ==========================================
class Categorie(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    plats = relationship("Plat", back_populates="categorie")

class Fournisseur(Base):
    __tablename__ = 'fournisseurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    contact = Column(String)
    ingredients = relationship("Ingredient", back_populates="fournisseur")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    cout_unitaire = Column(Numeric(10, 2))
    stock = Column(Numeric(10, 2))
    fournisseur_id = Column(Integer, ForeignKey('fournisseurs.id'))
    fournisseur = relationship("Fournisseur", back_populates="ingredients")
    plats = relationship("PlatIngredient", back_populates="ingredient", cascade="all, delete-orphan")

class Plat(Base):
    __tablename__ = 'plats'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prix = Column(Numeric(10, 2), nullable=False)
    description = Column(String)
    categorie_id = Column(Integer, ForeignKey('categories.id'))
    
    categorie = relationship("Categorie", back_populates="plats")
    ingredients = relationship("PlatIngredient", back_populates="plat", cascade="all, delete-orphan")
    commandes = relationship("CommandePlat", back_populates="plat", cascade="all, delete-orphan")
    avis = relationship("Avis", back_populates="plat", cascade="all, delete-orphan")

class PlatIngredient(Base):
    __tablename__ = 'plat_ingredients'
    plat_id = Column(Integer, ForeignKey('plats.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantite_necessaire = Column(Numeric(10, 2))
    
    plat = relationship("Plat", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="plats")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
    
    commandes = relationship("Commande", back_populates="client", cascade="all, delete-orphan")
    avis = relationship("Avis", back_populates="client", cascade="all, delete-orphan")

class Commande(Base):
    __tablename__ = 'commandes'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date_commande = Column(DateTime)
    total = Column(Numeric(10, 2))
    
    client = relationship("Client", back_populates="commandes")
    plats = relationship("CommandePlat", back_populates="commande", cascade="all, delete-orphan")

class CommandePlat(Base):
    __tablename__ = 'commande_plats'
    commande_id = Column(Integer, ForeignKey('commandes.id'), primary_key=True)
    plat_id = Column(Integer, ForeignKey('plats.id'), primary_key=True)
    quantite = Column(Integer)
    
    commande = relationship("Commande", back_populates="plats")
    plat = relationship("Plat", back_populates="commandes")

class Avis(Base):
    __tablename__ = 'avis'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    plat_id = Column(Integer, ForeignKey('plats.id'))
    note = Column(Integer)
    commentaire = Column(Text, nullable=True)
    date_avis = Column(DateTime)
    
    client = relationship("Client", back_populates="avis")
    plat = relationship("Plat", back_populates="avis")

# Création des tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



# # def inserer_donnees():
# #     # Vérifier si les données existent déjà pour éviter les doublons
# #     if session.query(Categorie).first():
# #         print("Les données existent déjà. Saut de l'insertion.")
# #         return

# #     # Catégories
# #     categories = [
# #         Categorie(id=1, nom='Entrée'), Categorie(id=2, nom='Plat principal'),
# #         Categorie(id=3, nom='Dessert'), Categorie(id=4, nom='Boisson'), Categorie(id=5, nom='Végétarien')
# #     ]
    
# #     # Fournisseurs
# #     fournisseurs = [
# #         Fournisseur(id=1, nom='AgriFresh', contact='contact@agrifresh.com'),
# #         Fournisseur(id=2, nom='MeatSupplier', contact='info@meatsupplier.com'),
# #         Fournisseur(id=3, nom='BevCo', contact='sales@bevco.com'),
# #         Fournisseur(id=4, nom='DairyFarm', contact='dairy@farm.com')
# #     ]
    
# #     # Ingrédients
# #     ingredients = [
# #         Ingredient(id=1, nom='Poulet', cout_unitaire=15.00, stock=50, fournisseur_id=2),
# #         Ingredient(id=2, nom='Laitue', cout_unitaire=5.00, stock=20, fournisseur_id=1),
# #         Ingredient(id=3, nom='Tomate', cout_unitaire=3.00, stock=30, fournisseur_id=1),
# #         Ingredient(id=4, nom='Mozzarella', cout_unitaire=10.00, stock=15, fournisseur_id=4),
# #         Ingredient(id=5, nom='Pomme de terre', cout_unitaire=2.00, stock=100, fournisseur_id=1),
# #         Ingredient(id=6, nom='Café', cout_unitaire=20.00, stock=5, fournisseur_id=3),
# #         Ingredient(id=7, nom='Sucre', cout_unitaire=1.50, stock=25, fournisseur_id=3),
# #         Ingredient(id=8, nom='Pois chiches', cout_unitaire=4.00, stock=40, fournisseur_id=1)
# #     ]
    
# #     # Plats
# #     plats = [
# #         Plat(id=1, nom='Salade César', prix=45.00, description='Salade avec poulet grillé', categorie_id=1),
# #         Plat(id=2, nom='Soupe de légumes', prix=30.00, description='Soupe chaude de saison', categorie_id=1),
# #         Plat(id=3, nom='Steak frites', prix=90.00, description='Viande grillée et frites', categorie_id=2),
# #         Plat(id=4, nom='Pizza Margherita', prix=70.00, description='Pizza tomate & mozzarella', categorie_id=2),
# #         Plat(id=5, nom='Tiramisu', prix=35.00, description='Dessert italien', categorie_id=3),
# #         Plat(id=6, nom='Glace 2 boules', prix=25.00, description='Glace au choix', categorie_id=3),
# #         Plat(id=7, nom='Coca-Cola', prix=15.00, description='Boisson gazeuse', categorie_id=4),
# #         Plat(id=8, nom='Eau minérale', prix=10.00, description='Eau plate ou gazeuse', categorie_id=4),
# #         Plat(id=9, nom='Curry de légumes', prix=65.00, description='Plat végétarien épicé', categorie_id=5),
# #         Plat(id=10, nom='Falafel wrap', prix=50.00, description='Wrap avec falafels et légumes', categorie_id=5)
# #     ]
    
# #     # Plat Ingrédients
# #     plat_ingredients = [
# #         PlatIngredient(plat_id=1, ingredient_id=1, quantite_necessaire=0.2),
# #         PlatIngredient(plat_id=1, ingredient_id=2, quantite_necessaire=0.1),
# #         PlatIngredient(plat_id=2, ingredient_id=2, quantite_necessaire=0.05),
# #         PlatIngredient(plat_id=2, ingredient_id=5, quantite_necessaire=0.1),
# #         PlatIngredient(plat_id=3, ingredient_id=1, quantite_necessaire=0.3),
# #         PlatIngredient(plat_id=3, ingredient_id=5, quantite_necessaire=0.2),
# #         PlatIngredient(plat_id=4, ingredient_id=3, quantite_necessaire=0.1),
# #         PlatIngredient(plat_id=4, ingredient_id=4, quantite_necessaire=0.1),
# #         PlatIngredient(plat_id=5, ingredient_id=6, quantite_necessaire=0.05),
# #         PlatIngredient(plat_id=5, ingredient_id=7, quantite_necessaire=0.02),
# #         PlatIngredient(plat_id=9, ingredient_id=8, quantite_necessaire=0.1),
# #         PlatIngredient(plat_id=10, ingredient_id=8, quantite_necessaire=0.15)
# #     ]
    
# #     # Clients
# #     clients = [
# #         Client(id=1, nom='Amine Lahmidi', email='amine@example.com', telephone='+212600123456'),
# #         Client(id=2, nom='Sara Benali', email='sara.b@example.com', telephone='+212600654321'),
# #         Client(id=3, nom='Youssef El Khalfi', email='youssef.k@example.com', telephone=None),
# #         Client(id=4, nom='Fatima Zahra', email='fatima.z@example.com', telephone='+212600987654'),
# #         Client(id=5, nom='Omar Alaoui', email='omar.a@example.com', telephone='+212600112233')
# #     ]
    
# #     # Commandes
# #     commandes = [
# #         Commande(id=1, client_id=1, date_commande=datetime(2025, 7, 7, 12, 30), total=120.00),
# #         Commande(id=2, client_id=2, date_commande=datetime(2025, 7, 7, 13, 0), total=85.00),
# #         Commande(id=3, client_id=1, date_commande=datetime(2025, 7, 8, 19, 45), total=150.00),
# #         Commande(id=4, client_id=3, date_commande=datetime(2025, 8, 15, 18, 30), total=200.00),
# #         Commande(id=5, client_id=4, date_commande=datetime(2025, 9, 1, 20, 0), total=95.00),
# #         Commande(id=6, client_id=5, date_commande=datetime(2025, 9, 10, 12, 15), total=75.00)
# #     ]
    
# #     # Commande Plats
# #     commande_plats = [
# #         CommandePlat(commande_id=1, plat_id=1, quantite=1),
# #         CommandePlat(commande_id=1, plat_id=3, quantite=1),
# #         CommandePlat(commande_id=1, plat_id=7, quantite=2),
# #         CommandePlat(commande_id=2, plat_id=2, quantite=1),
# #         CommandePlat(commande_id=2, plat_id=4, quantite=1),
# #         CommandePlat(commande_id=2, plat_id=8, quantite=1),
# #         CommandePlat(commande_id=3, plat_id=3, quantite=1),
# #         CommandePlat(commande_id=3, plat_id=5, quantite=1),
# #         CommandePlat(commande_id=3, plat_id=7, quantite=1),
# #         CommandePlat(commande_id=4, plat_id=4, quantite=2),
# #         CommandePlat(commande_id=4, plat_id=9, quantite=1),
# #         CommandePlat(commande_id=5, plat_id=10, quantite=1),
# #         CommandePlat(commande_id=5, plat_id=8, quantite=2),
# #         CommandePlat(commande_id=6, plat_id=7, quantite=3),
# #         CommandePlat(commande_id=6, plat_id=6, quantite=1)
# #     ]
    
# #     # Avis
# #     avis = [
# #         Avis(id=1, client_id=1, plat_id=1, note=4, commentaire='Très frais, poulet bien cuit', date_avis=datetime(2025, 7, 7, 13, 0)),
# #         Avis(id=2, client_id=2, plat_id=4, note=5, commentaire='Meilleure pizza du coin !', date_avis=datetime(2025, 7, 7, 14, 0)),
# #         Avis(id=3, client_id=3, plat_id=9, note=3, commentaire='Un peu trop épicé', date_avis=datetime(2025, 8, 15, 19, 0)),
# #         Avis(id=4, client_id=4, plat_id=10, note=4, commentaire='Bon, mais manque de sauce', date_avis=datetime(2025, 9, 1, 21, 0)),
# #         Avis(id=5, client_id=5, plat_id=6, note=5, commentaire='Glace délicieuse', date_avis=datetime(2025, 9, 10, 13, 0))
# #     ]

# #     session.add_all(categories + fournisseurs + ingredients + plats + plat_ingredients + clients + commandes + commande_plats + avis)
# #    session.commit()
# #     print("Données insérées avec succès.\n")

# inserer_donnees()






Session = sessionmaker(bind=engine)

session = Session()

# print("--- 1. Plats triés par prix décroissant ---")
# q1 = session.query(Plat).order_by(desc(Plat.prix)).all()
# for p in q1: print(f"{p.nom} : {p.prix} MAD")

# print("\n--- 2. Plats entre 30 et 80 MAD ---")
# q2 = session.query(Plat).filter(Plat.prix.between(30, 80)).all()
# for p in q2:
#     print(f"{p.nom} : {p.prix} MAD")
# print("\n--- 3. Clients dont le nom commence par 'S' ou 'F' ---")
# q3=session.query(Client).filter(or_(Client.nom.startswith('S'),Client.nom.startswith('F'))).all()
# print(f"Names start with 'S or 'F' /n")
# for c in q3:
#     print(f"{c.nom},")
from sqlalchemy.orm import joinedload

# print("\n--- 4. Afficher les plats avec leur nom de catégorie et le nom du fournisseur principal ---")

#  plats = session.query(Plat).options(
#     joinedload(Plat.categorie),
#     joinedload(Plat.ingredients).joinedload(PlatIngredient.ingredient).joinedload(Ingredient.fournisseur)
# ).all()

# for p in plats:
#     categorie_nom = p.categorie.nom if p.categorie else "Aucune"
#         if p.ingredients:
#         pi_principal = max(p.ingredients, key=lambda pi: pi.quantite_necessaire)  
#         fournisseur = pi_principal.ingredient.fournisseur
#         fournisseur_nom = fournisseur.nom if fournisseur else "Aucun"
#     else:
#         fournisseur_nom = "Aucun"
        
#     print(f"Plat: {p.nom} | Catégorie: {categorie_nom} | Fournisseur: {fournisseur_nom}")

# # print("\n--- 5. Commandes avec nom client, date et total de plats ---")
# q5 = session.query(Commande, Client, func.sum(CommandePlat.quantite).label('total_plats')).join(Client).join(CommandePlat).group_by(Commande.id, Client.id).all()
# for cmd, cli, total in q5:
#     print(f"Client: {cli.nom} | Date: {cmd.date_commande} | Plats commandés: {total}")

# print("\n--- 6. Détail des commandes (Plats, quantité, coût des ingrédients) ---")
# from sqlalchemy.orm import joinedload
# q6 = session.query(CommandePlat, Plat).join(Plat).options(joinedload(Plat.ingredients).joinedload(PlatIngredient.ingredient)).all()

# for cp, p in q6:
#     cout_ingredients = sum([pi.quantite_necessaire * pi.ingredient.cout_unitaire for pi in p.ingredients])
#     print(f"Commande {cp.commande_id}: {p.nom} (x{cp.quantite}) - Coût ingrédients unitaire: {cout_ingredients} MAD")

# print("\n--- 7. Nombre de plats par catégorie (y compris sans plats) ---")
# q7 =session.query(Categorie.nom, func.count(Plat.id).label('count')).outerjoin(Categorie).group_by(Categorie.id).all()
# for cat, count in q7: print(f"{cat} : {count} plat(s)")

# print("\n--- 8. Prix moyen des plats par catégorie ---")
# q8=session.query(Categorie.nom,func.avg(Plat.prix)).join(Plat).group_by(Categorie.id).all()
# for cat, avg_prix in q8: print(f"{cat} : {round(avg_prix, 2)} MAD en moyenne")

# # print("\n--- 9. Nombre de commandes par client (décroissant) ---")
# q9=session.query(Client.nom,func.count(Commande.id).label('nb')).outerjoin(Commande).group_by(Client.id).order_by(desc('nb')).all()
# for nom, nb in q9: print(f"{nom} : {nb} commande(s)")

# print("\n--- 10. Clients ayant passé plus de 2 commandes ---")
# q10 = session.query(Client.nom,func.count(Commande.id).label('nb_c')).join(Commande).group_by(Client.id).having( func.count(Commande.id) >=2).all()
# if not q10: print("Aucun client n'a passé plus de 2 commandes.")
# for cli in q10: print(cli.nom)        

# print("\n--- 11. Commandes du 3e trimestre 2025 ---")
# q11 = session.query(Commande).filter(extract('month',Commande.date_commande).between(7,9),extract('year',Commande.date_commande)==2025).all()
# for cmd in q11: print(f"Commande {cmd.id} le {cmd.date_commande}")

# print("\n--- 12. Commande la plus récente ---")
# q12 = session.query(Commande, Client).join(Client).order_by(desc(Commande.date_commande)).first()
# print(f"Plus récente : {q12.Client.nom} le {q12.Commande.date_commande}")

# print("\n--- 13. Clients avec une commande > 150 MAD ---")
q13 = session.query(Client.nom, Client.telephone, Commande.total).join(Commande).filter(Commande.total > 150).all()
for nom, tel, total in q13: print(f"{nom} ({tel}) - Total: {total} MAD")

# print("\n--- 14. Ajouter un nouveau plat Végétarien ---")
# nouveau_plat = Plat(nom='Salade Quinoa', prix=55.00, description='Quinoa et légumes', categorie_id=5)
# session.add(nouveau_plat)
# session.commit()
# print(" Plat 'Salade Quinoa' ajouté.")

# print("\n--- 15. Supprimer le client 'Youssef El Khalfi' ---")
# client_a_supprimer = session.query(Client).filter_by(nom="Youssef El Khalfi").first()
# if client_a_supprimer:
#     session.delete(client_a_supprimer)
#     session.commit()
#     print(" Client 'Youssef El Khalfi' et ses dépendances supprimés.")

# print("\n--- 16. Top 3 des plats les plus commandés ---")
# q16 = session.query(Plat.nom, Categorie.nom, func.sum(CommandePlat.quantite).label('total_qte')).join(Categorie).join(CommandePlat).group_by(Plat.id, Categorie.id).order_by(desc('total_qte')).limit(3).all()
# for p, c, qte in q16: print(f"{p} ({c}) : Commandé {qte} fois")

# print("\n--- 17. Fournisseurs avec stock < 10 unités ---")
# q17 = session.query(Fournisseur.nom, func.sum(Ingredient.stock * Ingredient.cout_unitaire).label('valeur')).join(Ingredient).filter(Ingredient.stock < 10).group_by(Fournisseur.id).all()
# for f, valeur in q17: print(f"{f} : Valeur du stock critique = {valeur} MAD")

# Fermeture de la session
session.close()