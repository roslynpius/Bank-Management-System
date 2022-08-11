from tkinter import *
import sqlite3
import random
import datetime

conn=sqlite3.connect('bank_db.db')
c=conn.cursor()

'''
c.execute("""CREATE TABLE bank_db(
		name text,
		account_number text,
		password text,
		creation_date date,
		amount float
		)""")
'''
class Table:    #for  creating tables  with gui
      
    def __init__(self,root,lst,total_rows,total_columns): 
          
        # code for creating table 
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = Entry(root, width=20, fg='blue', 
                               font=('Arial',11,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, lst[i][j]) 
 

def check():
	#function to check the details of the account
	chck=Tk()
	chck.title('Account Details')
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	c.execute("SELECT * FROM bank_db WHERE account_number="+login_accno.get())
	k=[['NAME:','ACCOUNT NUMBER:','PASSWORD:','CREATION DATE:','AMOUNT:']]
	r=k+c.fetchall()
	total_rows = len(r)
	total_columns = len(r[0])

	t = Table(chck,r,total_rows,total_columns)
	#print(type(r))-->list

	conn.commit()
	conn.close()
	chck.mainloop()
	
def save():
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	
	c.execute("""UPDATE bank_db SET
		name= :n,
		account_number= :an,
		password= :p,
		creation_date= :cd1,
		amount= :a
		WHERE account_number="""+login_accno.get(),
		{
		'n': name_e.get(),
		'an': login_accno.get(),
		'p': pwd_e.get(),
		'cd1': r1[3],
		'a': r1[4],
		})

	
	conn.commit()
	conn.close()
	alter.destroy()


def edit():
	global name_e,accno_e,cd_e,amt_e,pwd_e,alter,r1,edit
	alter=Tk()
	alter.title('Edit Account Details')
	alter.geometry('585x400+250+10')
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	f3=Frame(alter,bd=3,relief=RIDGE)
	f3.grid(row=1,column=1)
	#print(id)
	c.execute("SELECT *,oid FROM bank_db")
	records1=c.fetchall()
	#print("1)",records1)
	for r in records1:
		if ((login_accno.get() in r)==True):
			r1=r
			break
	#print("2)",r1)
	##creating entry for adding an account
	name_e=Entry(f3,width=30)
	name_e.grid(row=1,column=1,padx=20,pady=30)
	pwd_e=Entry(f3,width=30)
	pwd_e.grid(row=2,column=1,pady=30,padx=20)
	##labels
	name_label=Label(f3,text='Name',font=('arial',15,'bold'))
	name_label.grid(row=1,column=0,padx=20,pady=30)
	p_label=Label(f3,text='Password',font=('arial',15,'bold'))
	p_label.grid(row=2,column=0,padx=20,pady=30)
	
	name_e.insert(0,r1[0])
	pwd_e.insert(0,r1[2])
	
	save_bt=Button(f3,text='SAVE',cursor='hand2',command=save,font=('arial',15,'bold'),bg='white')
	save_bt.grid(row=4,column=1,pady=5,padx=5,ipadx=50)
	
	conn.commit()
	conn.close()
	alter.mainloop()
	
def dep_amt():
	from tkinter import messagebox as msb
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	c.execute("SELECT amount FROM bank_db WHERE account_number="+login_accno.get())
	a=c.fetchone()
	#print(a)
	
	c.execute("""UPDATE bank_db SET
		amount= :at
		WHERE account_number="""+login_accno.get(),
		{
		'at': a[0]+float(dep_money.get()),
		})
	msb.showinfo("DEPOSIT", "AMOUNT DEPOSITED")

	conn.commit()
	conn.close()
	
def dep():
	global d,dep_money
	d=Tk()
	d.title('DEPOSIT AMOUNT')
	d.geometry('585x400+250+10')
	
	dep_money=Entry(d,width=30)
	dep_money.grid(row=0,column=1,padx=20)
	dep_label=Label(d,text='ENTER AMOUNT TO BE DEPOSITED',font=('arial',15,'bold'),bg='white')
	dep_label.grid(row=0,column=0)
	dep_bt=Button(d,text='DEPOSIT AMOUNT',cursor='hand2',command=dep_amt,font=('arial',10,'bold'),bg='white')
	dep_bt.grid(row=1,column=1,padx=10)
	
	d.mainloop()
	
def wd_amt():
	from tkinter import messagebox as msb
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	c.execute("SELECT amount FROM bank_db WHERE account_number="+login_accno.get())
	a=c.fetchone()
	#print(a)
	if float(wd_money.get())<=a[0]:
		c.execute("""UPDATE bank_db SET
			amount= :at
			WHERE account_number="""+login_accno.get(),
			{
			'at': a[0]-float(wd_money.get()),
			})
		msb.showinfo("AMOUNT WITHDRAWAL STATUS","AMOUNT WITHDRAWN")
	else:
		msb.showerror("AMOUNT WITHDRAWAL STATUS","INSUFFICIENT FUNDS")

	conn.commit()
	conn.close()

def withdraw():
	global wd,wd_money
	wd=Tk()
	wd.title('WITHDRAW AMOUNT')
	wd.geometry('585x400+250+10')
	
	wd_money=Entry(wd,width=30)
	wd_money.grid(row=0,column=1,padx=20)
	wd_label=Label(wd,text='ENTER AMOUNT TO WITHDRAW',font=('arial',15,'bold'),bg='white')
	wd_label.grid(row=0,column=0)
	wd_bt=Button(wd,text='WITHDRAW AMOUNT',cursor='hand2',command=wd_amt,font=('arial',10,'bold'),bg='white')
	wd_bt.grid(row=1,column=1,padx=10)
	
	wd.mainloop()
	
def t_check():
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	from tkinter import messagebox as msb
	c.execute("SELECT account_number FROM bank_db")
	records1=c.fetchall()  
	flag=1
	#print("1)",records1)
	#print(login_accno.get())
	for r in records1:
		if (to_acc.get()==str(r[0])):
			flag=0
			break
	
			
	if flag==0:
		
		c.execute("SELECT amount FROM bank_db WHERE account_number="+login_accno.get())
		a=c.fetchone()
		c.execute("SELECT amount FROM bank_db WHERE account_number="+to_acc.get())
		b=c.fetchone()
		if float(fund.get())<=a[0]:
			c.execute("""UPDATE bank_db SET
				amount= :at
				WHERE account_number="""+to_acc.get(),
				{
				'at': b[0]+float(fund.get()),
				})
			c.execute("""UPDATE bank_db SET
				amount= :at
				WHERE account_number="""+login_accno.get(),
				{
				'at': a[0]-float(fund.get()),
				})
			msb.showinfo("STATUS","FUND TRANSFERRED")
		else:
			msb.showerror("STATUS","INSUFFICIENT FUNDS")
	else:
		msb.showerror("STATUS","INVALID ACCOUNT NUMBER")
		to_acc.delete(0,END)
		fund.delete(0,END)
		
			
	conn.commit()
	conn.close()

def t_fund():
	global transfer,to_acc,fund
	transfer=Tk()
	transfer.title('TRANSFER FUNDS')
	transfer.geometry('585x400+250+10')
	
	to_acc=Entry(transfer,width=30)
	to_acc.grid(row=0,column=1,pady=30,padx=20)
	to_label=Label(transfer,text='ACCOUNT NUMBER OF RECIPIENT',font=('arial',15,'bold'))
	to_label.grid(row=0,column=0)
	
	fund=Entry(transfer,width=30)
	fund.grid(row=2,column=1,padx=20,pady=50)
	fund_label=Label(transfer,text='FUND TO BE TRANSFERRED',font=('arial',15,'bold'))
	fund_label.grid(row=2,column=0)
	#print(to_acc.get())
	#print(type(to_acc.get()))
	
	ch_bt=Button(transfer,text='SUBMIT',cursor='hand2',command=t_check,font=('arial',15,'bold'),bg='white')
	ch_bt.grid(row=4,column=1,padx=10)
	
	transfer.mainloop()
	
def del_ac():
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	
	from tkinter import messagebox as mb
	if mb.askyesno('Verify','Really Delete?'):
		c.execute("DELETE from bank_db WHERE account_number="+login_accno.get())
	else:
		mb.showinfo('No', 'Good Choice')
	conn.commit()
	conn.close()
	
	
	
	
def user():
	user_win=Tk()
	user_win.title('USER')
	user_win.geometry('585x400+250+10')
	
	check_bt=Button(user_win,text='CHECK YOUR ACCOUNT DETAILS',cursor='hand2',command=check,font=('arial',15,'bold'),bg='white')
	check_bt.grid(row=0,column=0,pady=10,padx=10,ipadx=100)
	
	edit_bt=Button(user_win,text='EDIT ACCOUNT DETAILS',cursor='hand2',command=edit,font=('arial',15,'bold'),bg='white')
	edit_bt.grid(row=1,column=0,pady=8,padx=10,ipadx=145)
	
	addamt_bt=Button(user_win,text='DEPOSIT MONEY',cursor='hand2',command=dep,font=('arial',15,'bold'),bg='white')
	addamt_bt.grid(row=2,column=0,pady=10,padx=10,ipadx=180)
	
	wd_bt=Button(user_win,text='WITHDRAW MONEY',cursor='hand2',command=withdraw,font=('arial',15,'bold'),bg='white')
	wd_bt.grid(row=3,column=0,pady=10,padx=10,ipadx=170)
	
	tf_bt=Button(user_win,text='TRANSFER FUND',cursor='hand2',command=t_fund,font=('arial',15,'bold'),bg='white')
	tf_bt.grid(row=4,column=0,pady=10,padx=10,ipadx=180)
	
	del_bt=Button(user_win,text='DELETE ACCOUNT',cursor='hand2',command=del_ac,font=('arial',15,'bold'),bg='white')
	del_bt.grid(row=5,column=0,pady=10,padx=10,ipadx=175)
	
	
	user_win.mainloop()

def submit():
	from tkinter import messagebox as msb
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	
	c.execute("SELECT account_number FROM bank_db")
	records1=c.fetchall()  
	flag=1
	#print("1)",records1)
	#print(login_accno.get())
	for r in records1:
		
		if (login_accno.get()==str(r[0])):
			r1=str(r[0])
			flag=0
			break
	if flag==0:
		c.execute("SELECT password FROM bank_db WHERE account_number="+r1)
		rec=c.fetchone()
		#print(rec)
		
		if login_pwd.get()==str(rec[0]):
			#print("password verified")
			
			user()
				
				
		else:
			'''
			print("wrong password") 
			wrong_pwd=Label(lgn,text='THE PASSWORD YOU ENTERED IS WRONG TRY AGAIN',font=('arial',15,'bold'),bg='white')
			wrong_pwd.grid(row=6,column=1)
			'''
			
			msb.showerror("Error", "INCORRECT PASSWORD")
			login_pwd.delete(0,END)
			
		
		
	if flag==1:#CHECK
		msb.showerror("ERROR","INVALID ACCOUNT NUMBER")
		login_accno.delete(0,END)
		login_pwd.delete(0,END)
		home_page_bt=Button(lgn,text="GO TO HOME PAGE",cursor='hand2',command=lgn.destroy,font=('arial',15,'bold'),bg='white')
		home_page_bt.grid(row=6,column=0)
	conn.commit()
	conn.close()

def add_db():
	from tkinter import messagebox as msb
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	if (name.get()!='' and str(pwd.get())!='' and str(amt.get())!=''):
		c.execute("INSERT INTO bank_db VALUES(:name, :accno, :pass, :cd, :amt)",
				{
					'name':name.get(),
					'accno':accno,
					'pass':pwd.get(),
					'cd':date,
					'amt':amt.get()
				})
		msb.showinfo("ACCOUNT CREATED", "ACCOUNT NUMBER: "+accno)
		
	else:
		msb.showerror('Error','All Fields Are Required',parent=add_acc)
		
	#add_acc.destroy()
	
	conn.commit()
	conn.close()


def add_acc():
	global name,pwd,accno,date,amt,add_acc
	#WINDOW FOR FUNCTION--adding account
	add_acc=Tk()
	add_acc.title('New Account')
	add_acc.geometry('585x400+250+10')
	add_acc.resizable(False,False)
	add_acc.configure(bg='white')
	h2_label=Label(add_acc,text='CREATE NEW ACCOUNT',font=('Impact',25,'bold'),bg='white')
	h2_label.grid(row=0,column=0,columnspan=2)
	
	f1=Frame(add_acc,bd=3,relief=RIDGE)
	f1.grid(row=1,column=1)
	
	##creating entry for adding an account
	name=Entry(f1,width=30)
	name.grid(row=2,column=1,padx=20)
	pwd=Entry(f1,width=30)
	pwd.grid(row=3,column=1)
	amt=Entry(f1,width=30)
	amt.grid(row=4,column=1)

	##labels
	name_label=Label(f1,text='Name',font=('arial',15,'bold'),bg='white')
	name_label.grid(row=2,column=0)
	pwd_label=Label(f1,text='Password',font=('arial',15,'bold'),bg='white')
	pwd_label.grid(row=3,column=0)
	amt_label=Label(f1,text='Amount',font=('arial',15,'bold'),bg='white')
	amt_label.grid(row=4,column=0)
	
	accno=str(random.randint(1000000000,9999999999))
	current=datetime.datetime.now()
	date=current.strftime("%d/%m/%Y")
	
	#SUBMIT BUTTON
	submit_btn=Button(f1,text='Add Account',cursor='hand2',command=add_db,font=('arial',15,'bold'),bg='white')
	submit_btn.grid(row=6,column=0,columnspan=2,pady=10,padx=10,ipadx=70)
	
	
	
	add_acc.mainloop()
		
def login():
	global lgn,login_accno,login_pwd
	lgn=Tk()
	lgn.title('Login Page')
	lgn.geometry('585x400+250+10')
	lgn.resizable(False,False)
	lgn.configure(bg='white')
	h3_label=Label(lgn,text='USER LOGIN',font=('Impact',25,'bold'),bg='white')
	h3_label.grid(row=0,column=0,columnspan=2)
	
	f2=Frame(lgn,bd=3,relief=RIDGE)
	f2.grid(row=1,column=0)
	#login entry
	login_accno=Entry(f2,width=30)
	login_accno.grid(row=2,column=1,padx=20,pady=20)
	login_pwd=Entry(f2,show="*",width=30)
	login_pwd.grid(row=3,column=1,padx=20,pady=20)
	#labels
	label1=Label(f2,text='Enter Account Number',font=('arial',15,'bold'),bg='white')
	label1.grid(row=2,column=0,pady=20,padx=20)
	label1=Label(f2,text='Enter Password',font=('arial',15,'bold'),bg='white')
	label1.grid(row=3,column=0,pady=20,padx=20)
	#enter button
	enter_bt=Button(f2,text='SUBMIT',cursor='hand2',command=submit,font=('arial',10,'bold'),bg='white')
	enter_bt.grid(row=5,column=1,pady=10,padx=10,ipadx=70)
	
	lgn.mainloop()

def all_rec():    
	recds=Tk()
	recds.title('ALL RECORDS')
	#recds.geometry('400x400')
	
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	#query the database
	c.execute("SELECT *,oid FROM bank_db")
	k=[['NAME:','ACCOUNT NUMBER:','PASSWORD:','CREATION DATE:','AMOUNT:']]
	records=k+c.fetchall()
	total_rows = len(records)
	total_columns = len(records[0])

	t = Table(recds,records,total_rows,total_columns)
	recds.mainloop()
	conn.commit()
	conn.close()

def bal_en():
	bal=Tk()
	bal.title('BALANCE ENQUIRY')
	bal.geometry('585x400+250+10')
	bal.resizable(False,False)
	bal.configure(bg='white')
	conn=sqlite3.connect('bank_db.db')
	c=conn.cursor()
	lf3=Frame(bal,bd=3,relief=RIDGE)
	#lf3.grid(row=1,column=1) .............
	lf3.pack()
	
	c.execute("SELECT amount FROM bank_db")
	amt=c.fetchall()
	#print(amt)
	sum=0.0
	for i in amt:
		sum=sum+i[0]
	balance=Label(lf3,font=('Arial',15,'bold'),bg='white',text='TOTAL BALANCE=  '+str(sum))
	#balance.grid(row=1,column=0)
	balance.pack()
	
	conn.commit()
	conn.close()
	bal.mainloop()

def sub():
	un='admin'
	p='5678'
	from tkinter import messagebox as msgb
	if (un==user_name.get() and p==ad_pwd.get()):
		admn.destroy()
		qu=Tk()
		qu.title('ADMIN')
		qu.geometry('585x400+250+10')
		qu.resizable(False,False)
		qu.configure(bg='white')
		
		h3_label=Label(qu,text='WELCOME ADMIN',font=('Impact',30,'bold'),bg='white')
		h3_label.pack()
		
		lf2=Frame(qu,bd=3,relief=RIDGE)
		#lf2.grid(row=3,column=1)
		lf2.pack()
		
		view_bt=Button(lf2,text='VIEW ALL ACCOUNTS',cursor='hand2',font=('Arial',15,'bold'),bg='white',command=all_rec)
		#view_bt.grid(row=3,column=0,pady=10,padx=10,ipadx=100)
		view_bt.pack()
		#BALANCE ENQUIRY BUTTON
		bal_bt=Button(lf2,cursor='hand2',font=('Arial',15,'bold'),bg='white',text='TOTAL BALANCE ENQUIRY',command=bal_en)
		#bal_bt.grid(row=4,column=0,pady=10,padx=10,ipadx=80)
		bal_bt.pack()
	else:
		msgb.showerror('Error','Invalid User ID/Password',parent=admn)
		user_name.delete(0,END)
		ad_pwd.delete(0,END)

def admin():
	global admn,user_name,ad_pwd
	admn=Tk()
	admn.title('ADMIN LOGIN')
	admn.geometry('585x400+250+10')
	admn.resizable(False,False)
	admn.configure(bg='white')
	
	h2_label=Label(admn,text='ADMIN LOGIN',font=('Impact',30,'bold'),bg='white')
	h2_label.grid(row=0,column=0,columnspan=2)
	
	lf1=Frame(admn,bd=3,relief=RIDGE)
	lf1.grid(row=2,column=1)
	
	user_name=Entry(lf1,width=30)
	user_name.grid(row=2,column=1,padx=20)
	user_lbl=Label(lf1,font=('Arial',15,'bold'),bg='white',text='USER ID')
	user_lbl.grid(row=2,column=0,padx=20)
	
	ad_pwd=Entry(lf1,show="*",width=30)
	ad_pwd.grid(row=3,column=1,padx=20)
	pwd_lbl=Label(lf1,text='PASSWORD',font=('Arial',15,'bold'),bg='white')
	pwd_lbl.grid(row=3,column=0,padx=20)
	
	sub_bt=Button(lf1,text='SUBMIT',cursor='hand2',font=('Arial',15,'bold'),bg='white',command=sub)
	sub_bt.grid(row=4,column=1,pady=10,padx=10,ipadx=100)
	
	admn.mainloop()



#MAIN WINDOW
root=Tk()
root.title('Bank Management System')
root.geometry('585x400+250+10')
root.resizable(False,False)
root.configure(bg='white')

h1='Bank Management System'
h1_label=Label(root,text=h1,font=('Impact',35,'bold'),bg='white')
h1_label.grid(row=0,column=0,columnspan=2)
lf=Frame(root,bd=4,relief=RIDGE)
lf.grid(row=1,column=1)
login_bt=Button(lf,text='LOGIN',cursor='hand2',font=('Arial',15,'bold'),bg='white',command=login)
login_bt.grid(row=2,column=0,pady=30,padx=30,ipadx=212)

creat_bt=Button(lf,text='CREATE ACCOUNT',cursor='hand2',font=('Arial',15,'bold'),bg='white',command=add_acc)
creat_bt.grid(row=3,column=0,pady=30,padx=30,ipadx=155)

adm=Button(lf,text='ADMIN LOGIN',cursor='hand2',font=('Arial',15,'bold'),bg='white',command=admin)
adm.grid(row=4,column=0,pady=30,padx=30,ipadx=180)

conn.commit()
conn.close()
root.mainloop()