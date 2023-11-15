#Pagination mais qui affiche que une page sur le terminal

# from ldap3 import Server, Connection, ObjectDef, Reader, SUBTREE, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
# from ldap3.core.exceptions import LDAPExceptionError
# from ldap3.utils.dn import safe_dn
# from rich.pretty import pprint

# # Configuration du serveur LDAP
# server = Server(
#     host='10.10.1.21',
#     port=38901,
#     use_ssl=False,
#     get_info='ALL'
# )

# # Connexion à l'annuaire LDAP
# cnx = Connection(
#     server,
#     user='cn=manager,dc=ensea,dc=fr',
#     password='mdp'
# )
# cnx.bind()

# # Définition de l'objet
# object_class = [
#     'top',
#     'person',
#     'organizationalPerson',
#     'inetOrgPerson',
#     'posixAccount',
#     'sambaAccount',
#     'shadowAccount',
#     'trustAccount',
#     'nisMailAlias',
#     'ENSEAspecs'
# ]

# object_def = ObjectDef(object_class, cnx)
# base = 'ou=NIS,ou=people,dc=ensea,dc=fr'

# # Définition des attributs que vous souhaitez récupérer
# attributes = [ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]

# # Effectuer la recherche paginée
# try:
#     cnx.search(
#         search_base=base,
#         search_filter="(objectClass=*)",
#         search_scope=SUBTREE,
#         attributes=attributes,
#         paged_size=20
#     )

#     # Affichage des données de chaque compte
#     for entry in cnx.entries:
#         data = dict()
#         for attribute_name in entry.entry_attributes:
#             if attribute_name in ['cn', 'employeeNumber', 'mail']:
#                 data[attribute_name] = entry[attribute_name]
#         pprint(data)

# except LDAPExceptionError as e:
#     print(f"Erreur LDAP : {e}")

# finally:
#     # Déconnexion du serveur LDAP
#     cnx.unbind()











#Syeteme de block de 20 séparé dans le terminal

from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
from ldap3.core.exceptions import LDAPExceptionError
from rich.pretty import pprint

# Configuration du serveur LDAP
server = Server(
    host='10.10.1.21',
    port=38901,
    use_ssl=False,
    get_info='ALL'
)

# Connexion à l'annuaire LDAP
cnx = Connection(
    server,
    user='cn=manager,dc=ensea,dc=fr',
    password='mdp'
)
cnx.bind()

# Définition des paramètres de recherche
base = 'ou=NIS,ou=people,dc=ensea,dc=fr'
attributes = [ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]
page_size = 20

# Effectuer la recherche paginée
try:
    all_entries = []
    response = cnx.extend.standard.paged_search(
        search_base=base,
        search_filter="(objectClass=*)",
        search_scope=SUBTREE,
        attributes=attributes,
        paged_size=page_size,
        generator=False  # Utilisation de la pagination en mode "generator"
    )

    for entry in response:
        data = dict()
        for attribute_name in entry["attributes"]:
            if attribute_name in ['cn', 'employeeNumber', 'mail']:
                data[attribute_name] = entry["attributes"][attribute_name]
        all_entries.append(data)

    # Afficher ou traiter les données après avoir récupéré toutes les entrées
    for index, data in enumerate(all_entries, start=1):
        pprint(data)
        if index % page_size == 0:
            print(f"--- Fin du bloc de {page_size} entrées ---")

except LDAPExceptionError as e:
    print(f"Erreur LDAP : {e}")

finally:
    # Déconnexion du serveur LDAP
    cnx.unbind()
