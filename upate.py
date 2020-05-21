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
    
    print("Enter the Case ID whose related information has to be edited")
    case_id = input("CaseID")
    
    print("What information Do you want to edit?")
    menuname = input("\n\
    a) Accused Info\n\
    v) Victim Info\n\
    p) Litigator Information\n\
    ")
    

    
    conn.commit()
    conn.close()
