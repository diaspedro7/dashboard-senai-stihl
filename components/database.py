import mysql.connector

#Fazer a conexão com o banco de dados
def get_database():
    # mydb = mysql.connector.connect(
    # host="bwd3bxnuruinssz8cgmv-mysql.services.clever-cloud.com",
    # user="ulijg1pspqatdfta",
    # password="fDLM9NgbEYZTiMOXCZLP",
    # database="bwd3bxnuruinssz8cgmv",
    # )
    mydb = mysql.connector.connect(
    host="bqrdisnpyqnx6t4ifv0r-mysql.services.clever-cloud.com",
    user="uendncgdiftgorzs",
    password="73exox9HzKPm5A9NjYRK",
    database="bqrdisnpyqnx6t4ifv0r",
    )

    #Debuggar a conexão
    print("Database: " + str(mydb))
    
    return mydb

