import time
import os
import sqlite3
conn = sqlite3.connect("AtmUserDatabase.db")
cursor = conn.cursor()
cursor.execute('''
               
               create table if not exists AtmUsers(
                     AccountNumber int not null primary key,
                     UserId int unique,
                     PIN int check(PIN>=1000 and PIN<=9999),
                     Name varchar2(20),
                     MobileNumber number,
                     City varchar2(20), 
                     Balance number    
               )
      ''')

# cursor.execute(''' insert into AtmUsers values(12115,101,2468,'Nikita Yadav',7790998565,'Indore',5000)''')
# cursor.execute(''' insert into AtmUsers values(12116,102,3579,'Shivangi Agrawal',8998764521,'Lucknow',10000)''')
# cursor.execute(''' insert into AtmUsers values(12117,103,4681,'Harsimran kaur Bindra',9981885686,'New Delhi',10000)''')
# cursor.execute(''' insert into AtmUsers values(12118,104,5791,'Garima Garg',9711908266,'Jaiput',15000)''')
# cursor.execute(''' insert into AtmUsers values(12119,105,6813,'Megha Rai',8891008166,'Indore',15000)''')
# cursor.execute(''' insert into AtmUsers(AccountNumber,UserId,Name,MobileNumber,City,Balance) values(12120,106,'Sanskruti',7891118199,'Indore',15000)''')
# cursor.execute(''' insert into AtmUsers(AccountNumber,UserId,Name,MobileNumber,City,Balance) values(12121,107,'Sakshi Shrivas',9880998065,'Itarsi',25000)''')
# cursor.execute(''' insert into AtmUsers(AccountNumber,UserId,Name,MobileNumber,City,Balance) values(12122,108,'Savan Jain',8801238055,'Itarsi',20000)''')
# cursor.execute(''' insert into AtmUsers(AccountNumber,UserId,Name,MobileNumber,City,Balance) values(12123,109,'Raj singh',9811238155,'Itarsi',20000)''')
# cursor.execute(''' insert into AtmUsers(AccountNumber,UserId,Name,MobileNumber,City,Balance) values(12124,110,'Aaryan ',8991238955,'Bhopal',22000)''')
# conn.commit()
cursor.execute('''
               create table if not exists TransactionValue1(
                     Transaction_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                     Amount number,
                     Account_Number int,
                     TransactionType varchar2(10),
                     Timestamp datetime,
                     foreign key (Account_Number) references AtmUsers(Account_Number)        
                  )               
            ''')
# # cursor.execute(''' alter table TransactionValue1 add column Timestamp datetime ''')
# conn.commit()
# cursor.execute(''' select * from AtmUsers ''')
# a=cursor.fetchall()
# for i in a:
#     print(i)


accountNumber=0
def greenPIN():
    os.system('cls' if os.name=='nt' else 'clear')
    _accountNumber=int(input("Enter Your Account Number "))
    cursor.execute(" select PIN from AtmUsers where AccountNumber=?",(_accountNumber,))
    ch=cursor.fetchone()
    if ch is not None:
        if ch[0]!=None:
            print("You PIN is already Set, Go To Forgot PIN")
        else:
            newPin=int(input("Enter Your 4 digit PIN "))
            if newPin<1000 or newPin>9999:
                print("Error: Please Enter Exactly 4 digit PIN")
                exit()
            rePin=int(input("Re-Enter Your 4 digit PIN "))
            if newPin==rePin: 
                cursor.execute(''' update AtmUsers set PIN=? where AccountNumber=?''',(newPin,_accountNumber)  )
                if cursor.rowcount >0:
                    print("PIN Generated Successfully")
                    conn.commit()
                else:
                    print("erro")
            else:
                print("PIN does not matched please Re-Enter Your PIN")
    else:
        print("Account Number not exists")
    exit()


def pincheck():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
    x=int(input("\nEnter User Id\n"))
    y=int(input("Enter Your PIN\n"))
    cursor.execute("select AccountNumber from AtmUsers where PIN=? and UserId=?",(y,x))
    a=cursor.fetchone()
    if a is not None:
        accountNumber=a[0]
        return 1
    else:
        return 0

def menu():
    os.system('cls' if os.name=='nt' else 'clear')
    print("-----------------------Welcome to Canara Bank Atm---------------------------\n\n")
    print("1. Balance Enquire\n")
    print("2. Withraw\n")
    print("3. Deposit\n")
    print("4. Pin Change\n")
    print("5. Mini Statement\n")
    print("6. Exit\n")
    
def balanceEnquire():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
    # os.system("cls")
    cursor.execute('select Balance from AtmUsers where AccountNumber=?',(accountNumber,))
    amt=cursor.fetchone()
    if amt is not None:
        print("Currently Your Balance is ",amt[0])
    else:
        print("Server Error")
    time.sleep(3)
    
def Withraw():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
    # os.system("cls")
    amt=int(input("Enter the Amount\n"))
    if amt<0:
        print("Error:Negative Number")
        exit()
    cursor.execute('select Balance from AtmUsers where AccountNumber=?',(accountNumber,))
    WithrawAmount=cursor.fetchone()
    if WithrawAmount is not None and WithrawAmount[0]>=amt:
        val=WithrawAmount[0]-amt
        cursor.execute('update AtmUsers set Balance = ? where AccountNumber=?',(val,accountNumber))
        conn.commit()
        cursor.execute('select Balance from AtmUsers where AccountNumber=?',(accountNumber,))
        val2=cursor.fetchone()
        if val==val2[0]:
            print("Withrawing Successfully")
            cursor.execute(''' select datetime('now') ''')
            dt=cursor.fetchone()
            cursor.execute('insert into TransactionValue1 (Amount,Account_Number,TransactionType,Timestamp)  values(?,?,?,?)',(amt,accountNumber,'Withraw',dt[0]))
            conn.commit()
        else:
            print("Server Error")
    else:
        print("Not sufficient amount")
    time.sleep(3)    

def deposit():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
#     os.system("clear")
    DepositeAmt=int(input("Enter the amount\n"))
    if DepositeAmt is not None and DepositeAmt<0:
        print("Error: Negative Number")
        exit()
    a=DepositeAmt
    cursor.execute('select Balance from AtmUsers where AccountNumber = ?',(accountNumber,))
    amt=cursor.fetchone()
    DepositeAmt = DepositeAmt+amt[0]
    cursor.execute('update AtmUsers set Balance=? where AccountNumber=?',(DepositeAmt,accountNumber))
    conn.commit()
    cursor.execute('select Balance from AtmUsers where AccountNumber = ?',(accountNumber,))
    amt=cursor.fetchone()
    if amt is not None and DepositeAmt==amt[0]:
        print("Deposit Successfully")
        cursor.execute(''' select datetime('now') ''')
        dt=cursor.fetchone()
        cursor.execute('insert into TransactionValue1(Amount,Account_Number,TransactionType,Timestamp) values(?,?,?,?)',(a,accountNumber,'Deposit',dt[0]))
        conn.commit()
    else:
        print("Server Error")
    time.sleep(3)

def pinchange():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
    # os.system("clear")
    oldpin=int(input("Enter Old Pin\n"))
    cursor.execute("select PIN from AtmUsers where AccountNumber=?",(accountNumber,))
    pin=cursor.fetchone()
    if pin is not None and oldpin==pin[0]:
        newpin=int(input("enter new pin\n"))
        if newpin<1000 or newpin>9999:
            print("Error:Please Enter Exactly 4 digit PIN")
            time.sleep(2)
            exit()
        confirmpin=int(input("confrm pin\n"))
        if newpin==confirmpin:
            cursor.execute('update AtmUsers set PIN=? where AccountNumber=?',(newpin,accountNumber))
            conn.commit()
            cursor.execute('select PIN from AtmUsers where AccountNumber=?',(accountNumber,))
            pin=cursor.fetchone()
            if pin is not None and pin[0]==newpin:
                  print("Pin changes Successfully")
            else:
                print("PIN changing process failed,change again")
        else:
            print("confirm pin does not matched with new pin")
    else:
        print("wrong pin")
    time.sleep(3)

def ministatement():
    os.system('cls' if os.name=='nt' else 'clear')
    global accountNumber
    # os.system("clear")
    with open("statement.txt", "w") as f:
         f.write("-----------------------APNA BANK---------------------\n\n")
         f.write("Date         Time         UserId\n")
         cursor.execute('select * from TransactionValue1 where Account_Number=? order by Timestamp desc limit 5',(accountNumber,))
         out=cursor.fetchall();
         cursor.execute('select UserId,Balance from AtmUsers where AccountNumber=?',(accountNumber,))
         userIdBalance=cursor.fetchone()
         cursor.execute('''select datetime('now')''')
         dt=cursor.fetchone()
         f.write(f"{dt[0]}       {userIdBalance[0]}\n\n")
         f.write("FRM A/C: ")
         f.write(f"{accountNumber}\n\n")
         f.write("                    MINI STATEMENT          \n\n")
         for i in out:
             temp=i
             f.write(f"{temp[4]}         {temp[3]}        {temp[1]}\n")
         f.write("\nAVAIL BAL:                   ")
         f.write(f"             {userIdBalance[1]} \n\n")
         f.write("----------------Thank You, Please Visit Again---------")
         conn.commit()
    with open("statement.txt","r") as f:
             content = f.read()
             print(content)
    time.sleep(10)
conn.commit()
def welcomeScreen():
    os.system('cls' if os.name=='nt' else 'clear')
    print("\n\n------------------------WELCOME TO APNA BANK------------------------\n\n")
    out=int(input("  Press 1 for Green PIN or Press 2 for Continue: "))
    if out==1:
        greenPIN()
    if out==2:
        msg=pincheck()
        if msg==1:
           while True:
               menu()
               choice=int(input("Please Select Your Choice\n"))
               if choice==1:
                  balanceEnquire()
               elif choice==2:
                  Withraw()
               elif choice==3:
                  deposit()
               elif choice==4:
                  pinchange()
               elif choice==5:
                  ministatement()
               elif choice==6:
                  print("Thank You For Visiting!")
                  time.sleep(1)
                  quit()
               else:
                  print("wrong choice")
                  exit()
        else:
            print("Wrong pin")
            time.sleep(3)
            quit()
    else:
        print("wrong choice")
        exit()
            
welcomeScreen()