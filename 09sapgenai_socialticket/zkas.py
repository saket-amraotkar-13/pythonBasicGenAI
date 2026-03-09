from hdbcli import dbapi

def connect_to_hana():
    ##local parameters for connection
    host = "f0ef67e6-c5e0-4e58-9a41-d6b5649ce956.hna1.prod-us10.hanacloud.ondemand.com"
    port = "443"
    user = "USR_5LRWIWBIQOD8QJDMH5WRSQU8P"
    password = "H:E3&c#Q%2~9J1WKPYJDPDBz];*W15wEP1u@+jKjPIT^I! ^v`%[]|n;|FU_!_=CMRA3L09GYh|A+a)s~jI7m)NfgHMC%+l~7W].2MLy#N|)ET+Y+a),%9w3z?@%Q^|%"

    try:
        ##established connection
        conn = dbapi.connect(
            address=host,
            port=port,
            user=user,
            password=password
        )
        print("connection successfull")

        ##create a cursor
        cursor = conn.cursor()
        cursor.execute('SELECT TO_NVARCHAR(SYSUUID) as UUID FROM DUMMY')

        ##Fetch and print result
        ##from now in cursor.fetchall()
        
        print(cursor.fetchone()["UUID"])
        #close curson and connection
        cursor.close()
        conn.close()

    except Exception as e:
            print(f"connetion failed: {e}")
    
if __name__ == "__main__":
    connect_to_hana()