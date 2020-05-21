import psycopg2
import sys 


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
    print("\n")
    
    print("Enter the Case ID whose related information has to be edited")
    print("\n")
    case_id = int(input("CaseID:"))

    cur.execute("select * from case_fir")
    case_fir_ids=cur.fetchall()
    n1=len(case_fir_ids)
    fir_id = -1
    i = 0
    
    while(i<n1):               
        if (case_fir_ids[i][0] == case_id):
            fir_id=case_fir_ids[i][1]
        i=i+1
    if (fir_id == -1):
        print("\n\n\n\tENTER A VALIED CASE ID\n\n\n")
        conn.commit()
        conn.close()
        sys.exit()
    #fir_id

    def accusededit():
        cur.execute("select * from fir_info")
        fir_acc_ids=cur.fetchall()
        n2=len(fir_acc_ids)
        acc_id = -1
        i=0
        while(i<n2):               
            if (fir_acc_ids[i][0] == fir_id):
                acc_id=fir_acc_ids[i][10]
            i=i+1
        #print (acc_id)
        if (acc_id == -1):
            print("\n\n\n\tERROR\n\n\n")
            conn.commit()
            conn.close()
            sys.exit()
        acc_aadhar=input("Enter Accused's aadhar:")
        acc_name = input("Enter Accused's name:")
        acc_gender = input("Enter Accused's gender(M/F):")
        acc_identification= input("Enter Accused's identification")
        acc_age=input("Enter Accused's age")
        acc_contact=input("Enter Accused's contact")
        acc_address=input("Enter Accused's address")
        
        
        query1='''
        
        CREATE TABLE acc_temp AS (SELECT acc_id from accused where aadhar=%s);
        CREATE TABLE acc_old AS (SELECT acc_id from fir_info WHERE fir_id = %s);
        
        '''
        
        cur.execute(query1,(acc_aadhar,fir_id))
        
        
        query2='''
        
        DO $$
        BEGIN
        
        IF (SELECT COUNT(*) FROM acc_temp)=1
        THEN
        UPDATE fir_info SET acc_id = (SELECT acc_id FROM acc_temp) WHERE fir_id = %s;
        DELETE FROM accused where acc_id = (SELECT acc_id FROM acc_old);
        END IF;
        IF (SELECT COUNT(*) FROM acc_temp)=0
        THEN 
        UPDATE accused SET 
        aadhar=%s , 
        acc_name=%s,
        acc_gender=%s,
        acc_identification=%s,
        acc_age=%s,
        acc_contact=%s,
        acc_address=%s 
        WHERE acc_id = %s;
        END IF;
        END $$;
        
        '''
        
        cur.execute(query2,(fir_id,acc_aadhar,acc_name,acc_gender,acc_identification,acc_age,acc_contact,acc_address,acc_id))
        
    def victimedit():
        cur.execute("select * from fir_info")
        fir_vic_ids=cur.fetchall()
        n3=len(fir_vic_ids)
        vic_id = -1
        i=0
        while(i<n3):               
            if (fir_vic_ids[i][0] == fir_id):
                vic_id=fir_vic_ids[i][1]
            i=i+1
        #print (vic_id)
        if (vic_id == -1):
            print("\n\n\n\tERROR\n\n\n")
            conn.commit()
            conn.close()
            sys.exit()
        vic_name = input("Enter Victim's name:")
        vic_age = input("Enter Victim's age:")
        vic_contact = input("Enter victim's contact:")
        vic_gender = input("Enter victim's gender:")
        vic_address = input("Enter victim's address:")
        
        query3='''
        
        CREATE TABLE vic_temp AS (SELECT vic_id from victim where vic_name=%s and vic_contact=%s);
        CREATE TABLE vic_old AS (SELECT vic_id from fir_info WHERE fir_id = %s);
        
        '''
        cur.execute(query3,(vic_name,vic_contact,fir_id))
        
        query4='''
        
        DO $$
        BEGIN
        
        IF (SELECT COUNT(*) FROM vic_temp)=1
        THEN
        UPDATE fir_info SET vic_id = (SELECT vic_id FROM vic_temp) WHERE fir_id = %s;
        DELETE FROM accused where vic_id = (SELECT vic_id FROM vic_old);
        END IF;
        IF (SELECT COUNT(*) FROM vic_temp)=0
        THEN 
        UPDATE victim SET 
        vic_name = %s ,
        vic_age = %s ,
        vic_contact = %s ,
        vic_gender = %s ,
        vic_address  = %s
        WHERE vic_id = %s;
        END IF;
        END $$;
        
        '''
    
        cur.execute(query4,(fir_id,vic_name,vic_age,vic_contact,vic_gender,vic_address,vic_id))
  
    
    
    
    print("What information Do you want to edit?")
    menuname = input("\n\
    a) Accused Information\n\
    v) Victim Information\n\n")
    
    if menuname == "a":
        accusededit()
    elif menuname == "v":
        victimedit()
    else:
        print("\n\n\n\tWRONG INPUT\n\n\n")
        conn.commit()
        conn.close()
        sys.exit()
    
    conn.commit()
    conn.close()