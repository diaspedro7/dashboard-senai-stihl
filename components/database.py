import mysql.connector

#Fazer a conexão com o banco de dados
def get_database():
    mydb = mysql.connector.connect(
    host="bwd3bxnuruinssz8cgmv-mysql.services.clever-cloud.com",
    user="ulijg1pspqatdfta",
    password="fDLM9NgbEYZTiMOXCZLP",
    database="bwd3bxnuruinssz8cgmv",
    )

    #Debuggar a conexão
    print("Database: " + str(mydb))
    
    return mydb
