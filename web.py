import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("resource_management.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resources (
    resource_id TEXT PRIMARY KEY,
    resource_name TEXT,
    personal_no TEXT,
    status TEXT,
    sourcing_block TEXT,
    service TEXT,
    career_level TEXT,
    gender TEXT,
    location TEXT,
    primary_skill TEXT
)
""")
conn.commit()

def search_resource():
    keyword =search_var.get()

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute(""" SELECT * FROM resources WHERE resource_id LIKE ? OR resource_name LIKE ? OR primary_skill LIKE ?""",(f"%{keyword}%",f"%{keyword}%",f"%{keyword}%"))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("",tk.END, values=row)

def select_resource(event):
    selected=tree.focus()

    if not selected:
        return

    values = tree.item(selected,"values")

    resource_id_var.set(values[0])
    resource_name_var.set(values[1])
    personal_no_var.set(values[2])
    status_var.set(values[3])
    sourcing_block_var.set(values[4])
    service_var.set(values[5])
    career_level_var.set(values[6])
    gender_var.set(values[7])
    location_var.set(values[8])
    primary_skill_var.set(values[9])

def update_resource():
    cursor.execute("""UPDATE resources SET resource_name=?,personal_no=?,status=?,sourcing_block=?,service=?,career_level=?,gender=?,location=?,primary_skill=? WHERE resource_id=?""", (resource_name_var.get(),personal_no_var.get(),status_var.get(),sourcing_block_var.get(),service_var.get(),career_level_var.get(),gender_var.get(),location_var.get(),primary_skill_var.get(),resource_id_var.get()))

    conn.commit()

    load_data()

    messagebox.showinfo("Success","Resource Updated")

#Metric Function
def update_metrics():

    cursor.execute("SELECT COUNT(*) FROM resources")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM resources WHERE status='Active'")
    active = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM resources WHERE status='Rolled off'")
    rolled = cursor.fetchone()[0]

    total_label.config(text=f"Total Resources:{total}")
    active_label.config(text=f"Active :{active}")
    rolled_label.config(text=f"Rolled off:{rolled}")

def show_dashboard():
    home_frame.pack_forget()
    dashboard_frame.pack(fill="both",expand=True)

# Function to Add Resource
# VAlidation for the Name, ID, personal No
def validate_resource_id():
    value = resource_id_var.get()
    return all(ch.isalpha() or ch =='.'for ch in value)

def validate_resource_name():
    value = resource_name_var.get()
    return value.replace(" ", "").isalpha()

def validate_personal_no():
    value = personal_no_var.get()
    return value.isdigit() and len(value)<=8

def add_resource():
    rid = resource_id_var.get()
    rname = resource_name_var.get()
    pno = personal_no_var.get()
    status = status_var.get()
    sblock = sourcing_block_var.get()
    service = service_var.get()
    clevel = career_level_var.get()
    gender = gender_var.get()
    location = location_var.get()
    skill = primary_skill_var.get()

    if rid == "" or rname == "":
        messagebox.showerror("Error", "Resource ID and Name are required")
        return
    
    if not validate_resource_id():
        messagebox.showerror("Error","Resource ID should contain letters only")
        return

    if not validate_resource_name():
        messagebox.showerror("Error","Resource name should contain letters only")
        return
    
    if not validate_personal_no():
        messagebox.showerror("Error","personal number must be numeric and 8 letters")
        return


    try:
        cursor.execute("""
        INSERT INTO resources VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (rid, rname, pno, status, sblock,
              service, clevel, gender, location, skill))
        conn.commit()

        messagebox.showinfo("Success", "Resource Added Successfully")
        clear_fields()
        load_data()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Resource ID already exists")

#Delete Resource Function
def delete_resource():
    selected=tree.focus()

    if not selected:
        messagebox.showerror("Error","please Select a resource")
        return
    
    values=tree.item(selected,"values")
    rid=values[0]

    cursor.execute(
        "Delete From resources where resource_id=?",
        (rid,)
    )

    conn.commit()
    load_data()

    messagebox.showinfo("Success","Resource Deleted Successfully")
    
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM resources")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    update_metrics()

def check_login():
    username = username_var.get()
    password = password_var.get()

    if username == "shraddha.poojary" and password == "shraddha1234":
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )
        
def clear_fields():
    resource_id_var.set("")
    resource_name_var.set("")
    personal_no_var.set("")
    status_var.set("")
    sourcing_block_var.set("")
    service_var.set("")
    career_level_var.set("")
    gender_var.set("")
    location_var.set("")
    primary_skill_var.set("")


# Main Window
root = tk.Tk()
root.withdraw()
root.title("Resource Management Dashboard")
root.geometry("1200x650")

home_frame = tk.Frame(root)
home_frame.pack(fill="both",expand=True)

tracker_btn = tk.Button(home_frame,text="Resource Tracker",font=("Arial",14),width=20,height=2,command=lambda:show_dashboard())
tracker_btn.place(relx=0.5,rely=0.5,anchor="center")

dashboard_frame = tk.Frame(root)

# Variables
resource_id_var = tk.StringVar()
resource_name_var = tk.StringVar()
personal_no_var = tk.StringVar()
status_var = tk.StringVar()
sourcing_block_var = tk.StringVar()
service_var = tk.StringVar()
career_level_var = tk.StringVar()
gender_var = tk.StringVar()
location_var = tk.StringVar()
primary_skill_var = tk.StringVar()

# Form Frame
form_frame = tk.LabelFrame(dashboard_frame,text="Resource Details")
form_frame.pack(fill="x", padx=10, pady=10)

labels = [
    ("Resource ID", resource_id_var),
    ("Resource Name", resource_name_var),
    ("Personal No", personal_no_var),
    ("Status", status_var),
    ("Sourcing Block", sourcing_block_var),
    ("Service", service_var),
    ("Career Level", career_level_var),
    ("Gender", gender_var),
    ("Location", location_var),
    ("Primary Skill", primary_skill_var)
]                   

status_combo = ttk.Combobox(form_frame,textvariable=status_var,values=["Active","Rolled Off"],
                            state="readonly",width=27)

service_combo = ttk.Combobox(form_frame,textvariable=service_var,values=["Run","Build"],
                             state="readonly",width=27)

career_combo = ttk.Combobox(form_frame,textvariable=career_level_var,values=[str(i) for i in range(1,13)],
                            state="readonly",width=27)

gender_combo = ttk.Combobox(form_frame,textvariable=gender_var,values=["Female","Male"],state="readonly",width=27)

location = ttk.Combobox(form_frame, textvariable=location_var,values=["Bengaluru","Hyderabad","Mumbai","Chennai","Noida"],state="readonly",width=27)

#Resource ID
tk.Label(form_frame,text="Resource ID").grid(row=0,column=0,padx=10,pady=5)
tk.Entry(form_frame,textvariable=resource_id_var,width=30).grid(row=0,column=1,padx=10,pady=5)

#Resource Name
tk.Label(form_frame,text="Resource Name").grid(row=0,column=2,padx=10,pady=5)
tk.Entry(form_frame,textvariable=resource_name_var,width=30).grid(row=0,column=3,padx=10,pady=5)

#Personal No
tk.Label(form_frame,text="Personal No").grid(row=1,column=0,padx=10,pady=5)
tk.Entry(form_frame,textvariable=personal_no_var,width=30).grid(row=1,column=1,padx=10,pady=5)

#status
tk.Label(form_frame,text="Status").grid(row=1,column=2,padx=10,pady=5)
status_combo.grid(row=1,column=3,padx=10,pady=5)

#Sourcing Block
tk.Label(form_frame,text="Sourcing Block").grid(row=2,column=0,padx=10,pady=5)
tk.Entry(form_frame,textvariable=sourcing_block_var,width=30).grid(row=2,column=1,padx=10,pady=5)

#Service
tk.Label(form_frame,text="Service").grid(row=2,column=2,padx=10,pady=5)
service_combo.grid(row=2,column=3,padx=10,pady=5)

#Career level
tk.Label(form_frame,text="Career Level").grid(row=3,column=0,padx=10,pady=5)
career_combo.grid(row=3,column=1,padx=10,pady=5)

#Gender
tk.Label(form_frame,text="Gender").grid(row=3,column=2,padx=10,pady=5)
gender_combo.grid(row=3,column=3,padx=10,pady=5)

#Location
tk.Label(form_frame,text="Location").grid(row=4,column=0,padx=10,pady=5)
location.grid(row=4,column=1,padx=10,pady=5)

#Primary skill
tk.Label(form_frame,text="Primary skill").grid(row=4,column=2,padx=10,pady=5)
tk.Entry(form_frame,textvariable=primary_skill_var,width=30).grid(row=4,column=3,padx=10,pady=5)                                          

btn_frame=tk.Frame(dashboard_frame)
btn_frame.pack(anchor='w',padx=10,pady=10)

add_btn=tk.Button(btn_frame,text="Add Resource",bg="green",fg="white",width=15,command=add_resource)
add_btn.pack(side=tk.LEFT,padx=5)

#Delete Button
delete_btn=tk.Button(btn_frame,text="Delete Resource",bg="red",fg="white",width=15,command=delete_resource)
delete_btn.pack(side=tk.LEFT,padx=5)

#Update Button
update_btn = tk.Button(btn_frame,text="Update Resource",bg="blue",fg="white",width=15,command=update_resource)

update_btn.pack(side=tk.LEFT,padx=10)

# Table
columns = (
    "Resource ID",
    "Resource Name",
    "Personal No",
    "Status",
    "Sourcing Block",
    "Service",
    "Career Level",
    "Gender",
    "Location",
    "Primary Skill"
)

metric_frame = tk.Frame(dashboard_frame)
metric_frame.pack(fill="x",pady=5)

total_label = tk.Label(metric_frame,text="Total Resources : 0",font=("Arial",10,"bold"))

active_label = tk.Label(metric_frame,text="Active Resources : 0",font=("Arial",10,"bold"))

rolled_label = tk.Label(metric_frame,text="Rolled off :0",font=("Arial",10,"bold"))

total_label.pack(side=tk.LEFT,padx=20)
active_label.pack(side=tk.LEFT,padx=20)
rolled_label.pack(side=tk.LEFT,padx=20)

#login screen
login_window = tk.Toplevel()

login_window.title("login")
login_window.geometry("1000x450")

username_var = tk.StringVar()
password_var = tk.StringVar()

tk.Label(login_window,text="Username").pack(pady=5)

tk.Entry(login_window,textvariable=username_var).pack()

tk.Label(login_window,text="Password").pack(pady=5)

tk.Entry(login_window,textvariable=password_var,show="*").pack()

tk.Button(login_window,text="Login",command=check_login).pack(pady=10)

#Search 
search_frame = tk.Frame(dashboard_frame)
search_frame.pack(fill="x",padx=10,pady=5)

search_var = tk.StringVar()

tk.Label(search_frame,text="Search").pack(side=tk.LEFT)

tk.Entry(search_frame,textvariable=search_var,width=30).pack(side=tk.LEFT,padx=5)

tk.Button(search_frame,text="Search",command=search_resource).pack(side=tk.LEFT)

tk.Button(search_frame,text="Show All",command=load_data).pack(side=tk.LEFT,padx=5)

tree = ttk.Treeview(dashboard_frame, columns=columns, show="headings", height=15)

tree.bind("<ButtonRelease-1>",select_resource)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, padx=10, pady=10)

load_data()

root.mainloop()

conn.close()