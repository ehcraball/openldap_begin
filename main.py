# from ldap3 import Server, Connection, SIMPLE, SYNC, ALL

# # Configuration de l'annuaire LDAP
# ldap_server = Server('ldap://10.10.1.21:2201')
# # ldap_user = 'cn=ldap,dc=ludo,dc=fr'
# ldap_user = 'cn=root'
# ldap_password = 'mdp'


# # Connexion à l'annuaire LDAP
# try:
#     ldap_connection = Connection (ldap_server, user=ldap_user, password=ldap_password, authentication=SIMPLE, auto_bind=True)

#     # Verifier la connexion
#     if ldap_connection.bind():
#         print("Authentification réussie")

#     else:
#         print("Erreur d'authentification")


#     # Déconnexion de l'annuaire LDAP
#     ldap_connection.unbind()

# except Exception as e:
#     print(f"Erreur de connexion : {e}")
    

from ldap3 import Server, Connection, ObjectDef, Reader, Writer, Entry, AttrDef, Attribute
from ldap3 import ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
from ldap3.core.exceptions import LDAPExceptionError
# --
from rich.pretty import pprint
# --
server = Server(
host='10.10.1.21',
port=38901,
use_ssl=False,
get_info='ALL'
)
cnx = Connection(
server,
user='cn=manager,dc=ensea,dc=fr',
password='mdp'
)
cnx.bind()
# --
object_class = [
'top',
'person',
'organizationalPerson',
'inetOrgPerson',
'posixAccount',
'sambaAccount',
'shadowAccount',
'trustAccount',
'nisMailAlias',
'ENSEAspecs'
]
object_def = ObjectDef(object_class, cnx)
base = 'ou=NIS,ou=people,dc=ensea,dc=fr'
reader = Reader(cnx, object_def, base)
dn = 'uid=alexpeti66,ou=NIS,ou=people,dc=ensea,dc=fr'
entry: Entry = reader.search_object(entry_dn=dn, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
data = dict()
for attribute_name in entry.entry_attributes:
    data[attribute_name] = entry[attribute_name]
pprint(data)
