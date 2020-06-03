import psycopg2

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

try:
    conn = psycopg2.connect(user= "postgres",password="admin123",host="localhost",port="5432",database="criminal")
    
except psycopg2.Error as e:
    print ("Unable to connect!")
    print (e.pgerror)
    print (e.diag.message_detail)
    sys.exit(1)
else:
    print ("Connected!")
    cur = conn.cursor()

    liti_name=input("Enter litigator's name: ")
    liti_contact=input("Enter litigator's contact: ")
    liti_address = input("Enter litigator's address: ")
    liti_gender=input("Enter litigator's gender(M/F): ")
    liti_age=input("Enter litigator's age: ")
    incident_place=input("Enter incident place: ")
    incident_date=input("Enter incident date: ")
    incident_time=input("Enter incident time: ")
    crime=input("Enter the details about the crime: ")
    log_place=input("Enter the place where the complaint is logged: ")
    
    command1 = "insert into litigator(liti_name,liti_contact,liti_address,liti_gender,liti_age) values (%s,%s,%s,%s,%s)"
    
    cur.execute(command1,(liti_name,liti_contact,liti_address,liti_gender,liti_age))
    
    vic_age=0
    acc_age=0
    
    cur.execute("insert into victim(vic_age) values (%s)",(0,))
    cur.execute("insert into accused(acc_age) values (%s)",(0,))
    
    cur.execute("select MAX(vic_id) from victim ")
    vic_id = cur.fetchone()
    
    cur.execute("select MAX(acc_id) from accused ")
    acc_id = cur.fetchone()
    

    command2 = "insert into fir_info(vic_id,log_place,incident_place,incident_date,incident_time,liti_name,liti_contact,acc_id,crime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(command2,(vic_id,log_place,incident_place,incident_date,incident_time,liti_name,liti_contact,acc_id,crime))
    
    cur.execute("select MAX(fir_id) from fir_info")
    fir_id = cur.fetchone()

    cur.execute("insert into case_fir(fir_id) values (%s)",(fir_id,))
    
    cur.execute("select MAX(case_id) from case_fir")
    case_id = cur.fetchone()
    
    command3 =  "insert into case_info(fir_id, officer_id, status, description) values (%s,%s,%s,%s)"
    

    
    cur.execute("select officer_id from officer order by random() limit 1") 
    officer_id = cur.fetchone()
    
    status = "OPEN"
    
    cur.execute(command3 ,(fir_id, officer_id, status,crime))
    
    print("")
    print("")
    
    
    print("A case is registered with ID", case_id , ",for the FIR:" , fir_id )
    print("The victim ID:", vic_id)
    print("The accused ID:", acc_id)
    print("The officer alloted :" , officer_id)
    
    
    
    

    
    
    
    conn.commit()
    #print (cur.fetchone())
    conn.close()
