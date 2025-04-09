import pandas as pd 
import tkinter as tk
from tkinter import ttk
import numpy as np 
import random
from matplotlib import pyplot as plt 

# δημιουργία DataFrames
def create_dfs():
    global users_df,user_df,admin_df,books_df,orders_df,favorites_df,categories_df,books_df2,bookstores_admins_df,ratings_df,bookstores_books_df,admins_df
    users_df = pd.read_csv('users.csv') # dataframe με τα στοιχεία των users χωρίς orders-favorites τα οποίa υπάρχουν σε αλλα αρχεία
    user_df = pd.read_csv('users.csv') # είναι το ολοκληρωμένο dataframe για τους users
    
    admin_df = pd.read_csv('admins.csv') # είναι το ολοκληρωμένο dataframe για τους admins
    admins_df = pd.read_csv('admins.csv')# είναι το ολοκληρωμένο dataframe για τους adminsdataframe με τα στοιχεία των admins χωρίς bookstores τα οποίa υπάρχουν σε αλλα αρχεία
    
    books_df = pd.read_csv('books.csv') # είναι το ολοκληρωμένο dataframe για τα books
    books_df2 = pd.read_csv('books.csv') # dataframe με τα στοιχεία των books χωρίς categories-bookstores τα οποίa υπάρχουν σε αλλα αρχεία
    
    orders_df = pd.read_csv('orders.csv') # dataframe που περιέχει τις σχέσεις user - orders με την χρήση των users/books id
    favorites_df = pd.read_csv('favorites.csv') # dataframe που περιέχει τις σχέσεις user - favorites με την χρήση των users/books id
    categories_df = pd.read_csv('categories.csv') # dataframe που περιέχει τις σχέσεις books - category με την χρήση των category(str)/book id
    
    bookstores_admins_df = pd.read_csv('bookstores_admins.csv') # dataframe που περιέχει τις σχέσεις admins_bookstores 
    bookstores_books_df = pd.read_csv('bookstores_books.csv') # dataframe που περιέχει τις σχέσεις books-bookstores και τα copies που υπάρχουν στο κάθε κατάστημα
    ratings_df = pd.read_csv('ratings.csv') #dataframe που εχει τις το id του user τo id του βιβλιου και την βαθμολογία/σχόλιο του χρήστη γ το αντίστοιχο βιβλίο 
    
    
    orders_list = []
    favorites_list = []
    
    # δημιουργεί τίς λίστες για orders και favorites
    for i in range(len(user_df)):
        uid = user_df.loc[i,'id'].item()
        if uid in orders_df['user_id']:
            users_orders_list = orders_df.loc[orders_df['user_id'] == uid,'book_id'].tolist()
            users_orders_list = [int(k) for k in users_orders_list]
            orders_list.append(users_orders_list)
        else:
            orders_list.append([])
            
        if uid in favorites_df['user_id']:
            users_favorites_list = favorites_df.loc[favorites_df['user_id'] == uid,'book_id'].tolist()
            users_favorites_list = [int(k) for k in users_favorites_list]
            favorites_list.append(users_favorites_list)
        else:
            favorites_list.append([])
    # αφου έχουν δημιουργηθεί οι λίστες προσθέτωνται οι στήλες στο orders favorites στο user_df   
    user_df['orders'] = orders_list
    user_df['favorites'] = favorites_list
    
    user_df['balance'].astype(np.float16)
    users_df['balance'].astype(np.float16)
    
    # δημιουργεί τίς λίστες για τις κατηγορίες
    categories_list = []
    ratings_list = []
    books_bokstrs = []
    for i in range(len(books_df)):
        
        b_id = books_df.loc[i,'id'].item()
        if b_id in categories_df['book_id']: # δημιουργείτε η στήλη(λίστα) για τς κατηγορίες κάθε βιβλίου 
            books_categories_list = categories_df.loc[categories_df['book_id'] == b_id,'cat'].tolist()
            books_categories_list = [str(k) for k in books_categories_list]
            categories_list.append(books_categories_list)
        else:
            categories_list.append([])
        
        l = ratings_df['book_id'].tolist()
        if b_id in l: # δημιουργείτε η στήλη για τς βαθμολογίες κάθε βιβλίου 
            users_ids_list = ratings_df.loc[ratings_df['book_id'] == b_id,'user_id'].tolist()
            user_ratings_list = ratings_df.loc[ratings_df['book_id'] == b_id,'rating'].tolist()
            comments_list = ratings_df.loc[ratings_df['book_id'] == b_id,'comment'].tolist()
            
            books_ratings_dict = {users_ids_list[k] : [user_ratings_list[k],comments_list[k]] for k in range(len(users_ids_list))}

            ratings_list.append(books_ratings_dict)
        else:
            ratings_list.append({})

        l2 = bookstores_books_df['book_id'].tolist()
        if b_id in l2: # δημιουργείτε η στήλη για τα βιβλιοπωλεία και τα αντίστοιχα copies κάθε βιβλίου
            bookstores_list = bookstores_books_df.loc[bookstores_books_df['book_id'] == b_id,'bookstore'].tolist()
            copies_list = bookstores_books_df.loc[bookstores_books_df['book_id'] == b_id,'copies'].tolist()
            
            bookstores_copies_dict = {bookstores_list[k] : copies_list[k] for k in range(len(bookstores_list))}

            books_bokstrs.append(bookstores_copies_dict)
        else:
            books_bokstrs.append({})
                     
    books_df['categories'] = categories_list
    books_df['ratings'] = ratings_list # η στήλη για τις βαθμολογίες είναι dictionary με key το id του χρήστη και value μια λιστα που περιέχει βαθμολογία/σχόλιο
    books_df['bookstores'] = books_bokstrs
    
    bstrs_list = []
    for i in range(len(admin_df)): # φτιάχνετε η λίστα που περιέχει τις λίστες οι οποίες έχουν για κάθε admin τα ονόματα των βιβλιοπωλείων στα οποία έχουν πρόσβαση
        a_id = admin_df.loc[i,'id']
        if a_id in bookstores_admins_df['admin_id']:
            bstrs_list.append(bookstores_admins_df.loc[bookstores_admins_df['admin_id'] == a_id,'bookstore'].tolist())
            
        
    admin_df['bookstores'] = bstrs_list # η λίστα μπένει ως στήλη στο dataframe
    
# ------------------------------------- τέλος δημιουργίας DataFrames -------------------------------------------

create_dfs()
r = tk.Tk()  
r.geometry('1000x600')
r.title('Project')

start_menu = tk.Frame(r)
login_frame = tk.Frame(r)
register_frame = tk.Frame(r)

container = ttk.Frame(r)
container2 = ttk.Frame(r)
container2.pack(fill='x',side='bottom')
canvas = tk.Canvas(container,height=600,width=970)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar2 = ttk.Scrollbar(container2, orient="horizontal", command=canvas.xview)

def export_all_dataframes_to_csv(): # εξαγωγή όλων των dataframes σε .csv αρχεία
    export_orders()
    export_favorites()
    export_users()
    export_user()
    export_books()
    export_books2()
    export_ratings()
    export_admins()
    export_admins2()
    export_bookstores_admins()       
    export_bookstores_books()
    
def export_orders():
    orders_df.to_csv(r'orders.csv', index = False, header=True)
    
def export_favorites():
    favorites_df.to_csv(r'favorites.csv', index = False, header=True)
    
def export_user(): # εξάγει το user_df στο user.csv το οποίο έχει τις favorites/orders 
    user_df.to_csv(r'user.csv', index = False, header=True)
    
def export_users(): # εξάγει το users_df στο users.csv χωρίς  favorites/orders 
    users_df.to_csv(r'users.csv', index = False, header=True)
    
def export_books(): # εξάγει το books_df στο books2.csv το οποίο έχει τις bookstores/ratings/categories
    books_df.to_csv(r'books2.csv', index = False, header=True)
    
def export_books2():  # εξάγει το books_df2 στο books.csv χωρίς bookstores/ratings/categories
    books_df2.to_csv(r'books.csv', index = False, header=True)
    
def export_ratings():
    ratings_df.to_csv(r'ratings.csv', index = False, header=True)
    
def export_admins(): # εξάγει το admin_df στο admins2.csv με bookstores , ειναι το ολοκληρωμενο df
    admin_df.to_csv(r'admins2.csv', index = False, header=True)
    
def export_admins2(): # εξάγει το admins_df στο admins.csv χωρίς bookstores . δεν ειναι το ολοκληρωμενο df
    admins_df.to_csv(r'admins.csv', index = False, header=True)
    
def export_bookstores_admins():
    bookstores_admins_df.to_csv(r'bookstores_admins.csv', index = False, header=True)
    
def export_bookstores_books():
    bookstores_books_df.to_csv(r'bookstores_books.csv', index = False, header=True)

def admin_ui():
    global show_users_frame,admin_frame,books_frame_2,show_books_frame,add_book_frame,show_books_ratings,graphs_frame
    login_frame.pack_forget()
    admin_frame = tk.Frame(r)
    show_users_frame = tk.Frame(r)
    show_books_frame = tk.Frame(r)
    add_book_frame = tk.Frame(r)
    show_books_ratings = tk.Frame(r)
    graphs_frame = tk.Frame(r)
    admin_frame.pack() 
    tk.Button(admin_frame,text='Users',width=15,bg='grey',command=del_users).grid(row=2, column=0, pady=5)
    tk.Button(admin_frame,text='Books',width=15,bg='grey',command=books_admins).grid(row=3, column=0, pady=5)
    tk.Button(admin_frame,text='Add book',width=15,bg='grey',command=add_book).grid(row=4, column=0, pady=5)
    tk.Button(admin_frame,text='Graphs',width=15,bg='grey',command=graphs).grid(row=5, column=0, pady=5)
    
def graphs():
    admin_frame.pack_forget()
    
    tk.Button(graphs_frame,text='Back',width=5,bg='grey',command=lambda: go_back(graphs_frame,admin_frame)).grid(row=10, column=0)  
    
    def books_perPublisher():
        publishers_list = books_df['publisher'].tolist()
        publishers_list = set(publishers_list)
        books = []
        for p in publishers_list:
            books.append(len(books_df.loc[books_df['publisher'] == p,'id'].tolist()))
            
        plt.title("Αριθμός βιβλίων ανά εκδότη")
        plt.xlabel("Αριθμός βιβλίων")
        plt.ylabel("Publishers")
        y_pos = np.arange(len(publishers_list))
        plt.barh(y_pos,books)
        plt.yticks(y_pos,publishers_list)
        plt.show()
        
    def books_perPublisher_copies():
        publishers_list = books_df['publisher'].tolist()
        publishers_list = set(publishers_list)
        books_copies = []
        for p in publishers_list:
            books_copies.append(books_df.loc[books_df['publisher'] == p, 'copies'].aggregate(np.sum))
                
        plt.title("Αριθμός αντίτυπων ανά εκδότη")
        plt.xlabel("Αντίτυπα")
        plt.ylabel("Publishers")
        y_pos = np.arange(len(publishers_list))
        plt.barh(y_pos,books_copies)
        plt.yticks(y_pos,publishers_list)
    
        plt.show()
        
    def books_perAuthor():
        authors_list = books_df['author'].tolist()
        authors_list = set(authors_list)
        books = []
        for a in authors_list:
            books.append(int(len(books_df.loc[books_df['author'] == a,'id'].tolist())))
            
        plt.title("Αριθμός βιβλίων ανά συγγραφέα")
        plt.xlabel("Αριθμός βιβλίων")
        plt.ylabel("Publishers")
        y_pos = np.arange(len(authors_list))
        plt.barh(y_pos,books)
        plt.yticks(y_pos,authors_list)
        plt.show()
        
    def books_perAuthor_copies():
        authors_list = books_df['author'].tolist()
        authors_list = set(authors_list)
        books_copies = []
        for a in authors_list:
            books_copies.append(books_df.loc[books_df['author'] == a, 'copies'].aggregate(np.sum))
                
        plt.title("Αριθμός αντίτυπων συγγραφέα ")
        plt.xlabel("Αντίτυπα")
        plt.ylabel("Publishers")
        y_pos = np.arange(len(authors_list))
        plt.barh(y_pos,books_copies)
        plt.yticks(y_pos,authors_list)
        plt.show()
        
    def books_perCategories():
        categories_list = categories_df['cat'].tolist()
        categories_list = set(categories_list)
        books = []
        for c in categories_list:
            books.append(len(categories_df.loc[categories_df['cat'] == c, 'book_id'].tolist()))
                
        plt.title("Αριθμός βιβλίων ανά κατηγορία")
        plt.xlabel("Αριθμός βιβλίων")
        plt.ylabel("Categories")
        y_pos = np.arange(len(categories_list))
        plt.barh(y_pos,books)
        plt.yticks(y_pos,categories_list)
        plt.show()
        
    def books_perCategories_copies():
        categories_list = categories_df['cat'].tolist()
        categories_list = set(categories_list)
        books_copies = []
        for c in categories_list:
            l = categories_df.loc[categories_df['cat'] == c, 'book_id'].tolist()
            books_copies.append(books_df.loc[books_df['id'].isin(l), 'copies'].aggregate(np.sum))
                
        plt.title("Αριθμός αντίτυπων ανά κατηγορία")
        plt.xlabel("Αντίτυπα")
        plt.ylabel("Categories")
        y_pos = np.arange(len(categories_list))
        plt.barh(y_pos,books_copies)
        plt.yticks(y_pos,categories_list)
        plt.show()
        
    def users_perCity():
        city_list = user_df['city'].tolist()
        city_list = set(city_list)
        userspcity_list = []
        for c in city_list:
            userspcity_list.append(len(user_df.loc[user_df['city']==c,'id'].tolist()))
                
        plt.title("Αριθμός χρηστών ανά πόλη")
        plt.xlabel("Αριθμός χρηστών")
        plt.ylabel("City")
        y_pos = np.arange(len(city_list))
        plt.barh(y_pos,userspcity_list)
        plt.yticks(y_pos,city_list)
        plt.show()
        
    def books_perBookstorecopies():
        bookstores_list = bookstores_books_df['bookstore'].tolist()
        bookstores_list = set(bookstores_list)
        books_copies = []
        for b in bookstores_list:
            books_copies.append(bookstores_books_df.loc[bookstores_books_df['bookstore'] == b, 'copies'].aggregate(np.sum))
                
        plt.title("Αριθμός αντίτυπων ανά κατάστημα")
        plt.xlabel("Αντίτυπα")
        plt.ylabel("Bookstores")
        y_pos = np.arange(len(bookstores_list))
        plt.barh(y_pos,books_copies)
        plt.yticks(y_pos,bookstores_list)
        plt.show()

    
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά εκδότη (αντίτυπα)',width=35,bg='grey',command=books_perPublisher_copies).grid(row=1, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά εκδότη',width=35,bg='grey',command=books_perPublisher).grid(row=2, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά συγγραφέα (αντίτυπα)',width=35,bg='grey',command=books_perAuthor_copies).grid(row=3, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά συγγραφέα',width=35,bg='grey',command=books_perAuthor).grid(row=4, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά κατηγορία',width=35,bg='grey',command=books_perCategories).grid(row=5, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά κατηγορία (αντίτυπα)',width=35,bg='grey',command=books_perCategories_copies).grid(row=6, column=0,pady=5)  
    tk.Button(graphs_frame,text='Αριθμός βιβλίων ανά κατάστημα (αντίτυπα)',width=35,bg='grey',command=books_perBookstorecopies).grid(row=7, column=0,pady=5)    
    tk.Button(graphs_frame,text='Αριθμός χρηστών ανά πόλη',width=35,bg='grey',command=users_perCity).grid(row=8, column=0,pady=5)  
    
    
    graphs_frame.pack()
    
def add_book():
    admin_frame.pack_forget()
    
    tk.Button(add_book_frame,text='Back',width=5,bg='grey',command=lambda: go_back(add_book_frame,admin_frame)).grid(row=9, column=0)
    
    def addbook():
        ttl = title.get()
        au = author.get()
        pblser = publisher.get()
        co = float(cost.get())
        s_co = float(s_cost.get())
        
        av_books_titles = books_df['title'].tolist()
        if ttl in av_books_titles:
            print("Το βιβλίο υπάρχει ήδη.\nΜπορείτε να κανετε αλλαγές αν έχετε πρόσβαση στα βιβλιοπωλεία.")
        else:
            print("Δώστε τις κατηγορίες που ανήκει το βιβλίο.")
            cat_list = []
            while 1:
                cat = input("Κατηγορία: ")
                cat_list.append(str(cat))
                a = int(input("Θέλετε αν εισάγετε και άλλη κατηγορία για το βιβλίο? (1.ναι / 2.οχι)"))
                if a == 2:
                    break
    
            bookstores_dict = {}
            total_copies = 0
            print("Δώστε όνομα βιβλιοπωλείου και τα αντίτυπα.")
            while 1:
                bookstore_name = input("Bookstore name: ")
                book_copies = int(input("Copies: "))
                bookstores_dict[bookstore_name] = book_copies
                total_copies += int(book_copies)
                a = int(input("Θέλετε αν εισάγετε και άλλο βιβλιοπωλείο και τα αντίστοιχα copies? (1.ναι / 2.οχι)"))
                if a == 2:
                    break
            
            last_id = books_df.iloc[-1].tolist()
            b_id = int(last_id[0])+1
            books_df.loc[len(books_df.index)] = [b_id,ttl,au,pblser,co,s_co,True,total_copies,cat_list,{},bookstores_dict]
            books_df2.loc[len(books_df2.index)] = [b_id,ttl,au,pblser,co,s_co,True,total_copies]
            
            for i in cat_list:
                categories_df.loc[len(categories_df.index)] = [int(b_id),str(i)]
                
            admins_bookstores_list = bookstores_admins_df.loc[bookstores_admins_df['admin_id'] == cadmin_id,'bookstore'].tolist()
            for i in bookstores_dict.keys():
                bookstores_books_df.loc[len(bookstores_books_df.index)] = [str(i),int(b_id),int(bookstores_dict[i])]
                if i not in admins_bookstores_list:
                    bookstores_admins_df.loc[len(bookstores_admins_df.index)] = [i,cadmin_id]
                    admin_df.loc[admin_df['id'] == cadmin_id,'bookstores'].values[0].append(i)
                    
            export_all_dataframes_to_csv()
                    
                    
            
            
            
        
        
        
    tk.Label(add_book_frame,text="Title:").grid(row=2, column=0)
    title = tk.StringVar()
    titleEntry = tk.Entry(add_book_frame, textvariable=title)
    titleEntry.grid(row=2, column=1, pady=10) 

    tk.Label(add_book_frame,text="Author:").grid(row=3, column=0)
    author = tk.StringVar()
    authorEntry = tk.Entry(add_book_frame, textvariable=author)
    authorEntry.grid(row=3, column=1, pady=10) 

    tk.Label(add_book_frame,text="Publisher:").grid(row=4, column=0)
    publisher = tk.StringVar()
    publisherEntry = tk.Entry(add_book_frame, textvariable=publisher)
    publisherEntry.grid(row=4, column=1, pady=10) 

    
    tk.Label(add_book_frame,text="Cost:").grid(row=5, column=0)
    cost = tk.StringVar()
    costEntry = tk.Entry(add_book_frame, textvariable=cost)
    costEntry.grid(row=5, column=1, pady=10) 
    
    tk.Label(add_book_frame,text="Shipping Cost:").grid(row=6, column=0)
    s_cost = tk.StringVar()
    s_costEntry = tk.Entry(add_book_frame, textvariable=s_cost)
    s_costEntry.grid(row=6, column=1, pady=10) 

    
    button5 = tk.Button(add_book_frame,text="Add book",width=15,bg='grey',command=addbook)
    button5.grid(row=7, column=4, pady=15, padx=10)
    
    
    
    add_book_frame.pack()
    

def books_admins():
    admin_frame.pack_forget()
    
    books_frame_2 = ttk.Frame(canvas,width=970)
    books_frame_2.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=books_frame_2, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar2.set)

    tk.Button(books_frame_2,text='Back',width=5,bg='grey',command=lambda: go_back(canvas,admin_frame)).grid(row=0, column=0)
    tk.Label(books_frame_2,text="Books:").grid(row=1, column=0)
    
    authors_list = books_df['author'].tolist()
    authors_list = set(authors_list)
    publishers_list = books_df['publisher'].tolist()
    publishers_list = set(publishers_list)
    
    tk.Label(books_frame_2,text="Συνολικό κόστος όλων των διαθέσιμων βιβλίων για:").grid(row=1, column=3)
    tk.Label(books_frame_2,text="Author:").grid(row=2, column=2)
    tk.Label(books_frame_2,text="Publisher:").grid(row=2, column=3)
    tk.Label(books_frame_2,text="Συνολικά:").grid(row=2, column=4)
    
    c = 3
    for a in authors_list: # Συνολικό κόστος όλων των διαθέσιμων βιβλίων για authors
        total_books_cost = round(books_df.loc[(books_df['author'] == a) & (books_df['availability'] == True), 'cost'].aggregate(np.sum),2)
        tk.Label(books_frame_2,text=str(a)+": "+str(total_books_cost)+" €").grid(row=c, column=2,padx =5 ,pady=5)
        c+=1
    
    c = 3
    for a in publishers_list: # Συνολικό κόστος όλων των διαθέσιμων βιβλίων για publishers
        total_books_cost = round(books_df.loc[(books_df['publisher'] == a)  & (books_df['availability'] == True), 'cost'].aggregate(np.sum),2)
        tk.Label(books_frame_2,text=str(a)+": "+str(total_books_cost)+" €").grid(row=c, column=3,padx =5 ,pady=5)
        c+=1
    
    total_books_cost = round(books_df.loc[books_df['availability'] == True, 'cost'].aggregate(np.sum),2)
    tk.Label(books_frame_2,text="Συνολικό κόστος όλων των διαθέσιμων βιβλίων: "+str(total_books_cost)+" €").grid(row=3, column=4,padx =5 ,pady=5)
    
    
    books_ui_btns_dict = {}
    
    for i in range(len(books_df)):
        book_id = books_df.loc[i,'id']
        book_title = books_df.loc[i,'title']
        
        def show_book_admins(b_id=book_id):  
            canvas.pack_forget()
            show_books_frame.pack()
            tk.Button(show_books_frame,text='Back',width=5,bg='grey',command=lambda: go_back(show_books_frame,canvas)).grid(row=0, column=0)
            
            book_title = books_df.loc[books_df['id'] == b_id,'title'].values[0]
            cost = books_df.loc[books_df['id'] == b_id,'cost'].values[0]
            shipping_cost = books_df.loc[books_df['id'] == b_id,'shipping_cost'].values[0]
            author = books_df.loc[books_df['id'] == b_id,'author'].values[0]
            publisher = books_df.loc[books_df['id'] == b_id,'publisher'].values[0]
            av = books_df.loc[books_df['id'] == b_id,'availability'].values[0]
            copies = books_df.loc[books_df['id'] == b_id,'copies'].values[0]
            
            tk.Label(show_books_frame,text="Book title: "+str(book_title)).grid(row=1, column=0,padx =5 ,pady=5)
            tk.Label(show_books_frame,text="Cost: "+str(cost)+" €").grid(row=2, column=0,padx =5 ,pady=5)
            tk.Label(show_books_frame,text="Shipping_cost: "+str(shipping_cost)+" €").grid(row=3, column=0,padx =5 ,pady=5)
            tk.Label(show_books_frame,text="Author: "+str(author)).grid(row=4, column=0,padx =5 ,pady=5)
            tk.Label(show_books_frame,text="Publisher: "+str(publisher)).grid(row=5, column=0,padx =5 ,pady=5)
            tk.Label(show_books_frame,text="Total copies: "+str(copies)).grid(row=7, column=0,padx =5 ,pady=5)
            
            admin_bookstores_list = admin_df.loc[admin_df['id'] == cadmin_id,'bookstores'].values[0]
            books_bookstores_dict = books_df.loc[books_df['id'] == b_id,'bookstores'].values[0]
            
            def show_rating_comments():
                nonlocal b_id
                show_books_frame.pack_forget()
                show_books_ratings.pack()
                tk.Button(show_books_ratings,text='Back',width=5,bg='grey',command=lambda: go_back(show_books_ratings,show_books_frame)).grid(row=0, column=0)
                
                users_ids_rate_book = books_df.loc[books_df['id'] == b_id,'ratings'].values[0]
                
                if len(list(users_ids_rate_book.keys())) < 1:
                    tk.Label(show_books_ratings,text="Δεν υπάρχουν βαθμολογίες/σχόλια για αυτο το βιβλίο.").grid(row=1, column=1,padx =5 ,pady=5)
                else:
                    c = 1
                    change_rating_btns = {}
                    change_comment_btns = {}
                    new_rating_entry = {}
                    new_com_entry = {}
                    for k in users_ids_rate_book.keys():
                        rating = users_ids_rate_book[k][0]
                        comment = users_ids_rate_book[k][1]
                        user_un = user_df.loc[user_df['id'] == k,'username'].values[0]
                        tk.Label(show_books_ratings,text="Ο χρήστης "+str(user_un)+" έδωσε βαθμολογία/σχόλια:").grid(row=c, column=0,padx =5 ,pady=5)
                        
                        tk.Label(show_books_ratings,text="Rating:").grid(row=c+1, column=0,padx =1 ,pady=1)
                        new_rating_entry[k] = tk.StringVar()
                        new_nEntry = tk.Entry(show_books_ratings, textvariable=new_rating_entry[k])
                        new_nEntry.grid(row=c+1, column=1, pady=10) 
                        
                        def change_rating(u_id = k,re = new_rating_entry[k]):
                            nonlocal b_id                           
                            books_df.loc[books_df['id'] == b_id,'ratings'].values[0][u_id][0] = float(new_rating_entry[u_id].get())
                            ratings_df.loc[(ratings_df['book_id'] == b_id) & (ratings_df['user_id'] == u_id),'rating'] = float(new_rating_entry[u_id].get())
                            export_books()
                            export_ratings()
                        
                        
                        if comment != '':
                            tk.Label(show_books_ratings,text="Comment").grid(row=c+2,column=0,padx =1 ,pady=1)
                            new_com_entry[k] = tk.StringVar()
                            new_cEntry = tk.Entry(show_books_ratings, textvariable=new_com_entry[k])
                            new_cEntry.grid(row=c+2, column=1, pady=10)   
                            
                            def change_comment(u_id = k,ce = new_com_entry[k]):
                                nonlocal b_id,new_com_entry  
                                books_df.loc[books_df['id'] == b_id,'ratings'].values[0][u_id][1] = ce.get()
                                ratings_df.loc[(ratings_df['book_id'] == b_id) & (ratings_df['user_id'] == u_id),'comment'] = ce.get()
                                export_books()
                                export_ratings()
                            
                            change_comment_btns[k] = tk.Button(show_books_ratings,text='Change comment',width=15,bg='grey',command=change_comment)
                            change_comment_btns[k].grid(row=c+2, column=2, pady=15, padx=10)
                            
                            new_com_entry[k].set(comment)                            
                        else:
                            tk.Label(show_books_ratings,text="Ο χρήστης δεν έγραψε κάποιο σχόλιο.").grid(row=c+2,column=0,padx =1 ,pady=1)
                        new_rating_entry[k].set(rating)        
                        
                        change_rating_btns[k] = tk.Button(show_books_ratings,text='Change rating',width=15,bg='grey',command=change_rating)
                        change_rating_btns[k].grid(row=c+1, column=2, pady=15, padx=10)
                        
                        c = 4         
               
            
            tk.Button(show_books_frame,text='Show rating/comments',width=20,bg='grey',command=show_rating_comments).grid(row=0, column=5)
        
            f = 1         
            for b in books_bookstores_dict.keys():
                if b not in admin_bookstores_list:
                    f=0
                    break              
                
            if f: # αν έχει πρόσβαση σε κάθε βιβλιοπωλείο που έχει το βιβλίο.
                
                def change_cost():
                    new_c = new_cost.get()
                    nonlocal b_id
                    books_df.loc[books_df['id'] == b_id,'cost'] = float(new_c)
                    books_df2.loc[books_df2['id'] == b_id,'cost'] = float(new_c)
                    export_all_dataframes_to_csv()
                    
                    
                def change_sc():
                    nonlocal b_id
                    new_shipping_cost = new_sc.get()
                    books_df.loc[books_df['id'] == b_id,'cost'] = float(new_shipping_cost)
                    books_df2.loc[books_df2['id'] == b_id,'cost'] = float(new_shipping_cost)
                    export_all_dataframes_to_csv()

                    
                def change_author():
                    nonlocal b_id
                    new_author = new_a.get()
                    books_df.loc[books_df['id'] == b_id,'cost'] = new_author
                    books_df2.loc[books_df2['id'] == b_id,'cost'] = new_author
                    export_all_dataframes_to_csv()

                    
                def change_publisher():
                    nonlocal b_id
                    new_publisher = publisher_n.get()
                    books_df.loc[books_df['id'] == b_id,'cost'] = new_publisher
                    books_df2.loc[books_df2['id'] == b_id,'cost'] = new_publisher
                    export_all_dataframes_to_csv()
                    
                def del_book():
                    nonlocal b_id
                    books_df.drop(books_df.loc[books_df['id'] == b_id].index, inplace=True)
                    books_df2.drop(books_df2.loc[books_df2['id'] == b_id].index, inplace=True)
                    export_all_dataframes_to_csv()
            
                    
                
                
                new_cost = tk.StringVar()
                new_costEntry = tk.Entry(show_books_frame, textvariable=new_cost)
                new_costEntry.grid(row=2, column=1, pady=10) 
                button = tk.Button(show_books_frame,text='Change cost',width=15,bg='grey',command=change_cost)
                button.grid(row=2, column=2, pady=15, padx=10)
                
                new_sc = tk.StringVar()
                new_scEntry = tk.Entry(show_books_frame, textvariable=new_sc)
                new_scEntry.grid(row=3, column=1, pady=10) 
                button2 = tk.Button(show_books_frame,text='Change shipping cost',width=20,bg='grey',command=change_sc)
                button2.grid(row=3, column=2, pady=15, padx=10)
                
                new_a = tk.StringVar()
                new_aEntry = tk.Entry(show_books_frame, textvariable=new_a)
                new_aEntry.grid(row=4, column=1, pady=10) 
                button3 = tk.Button(show_books_frame,text='Change Author',width=12,bg='grey',command=change_author)
                button3.grid(row=4, column=2, pady=15, padx=10)
                
                publisher_n = tk.StringVar()
                new_plsrEntry = tk.Entry(show_books_frame, textvariable=publisher_n)
                new_plsrEntry.grid(row=5, column=1, pady=10) 
                button4 = tk.Button(show_books_frame,text='Change Publisher',width=15,bg='grey',command=change_publisher)
                button4.grid(row=5, column=2, pady=15, padx=10)
                
                button5 = tk.Button(show_books_frame,text="Delete book",width=15,bg='grey',command=del_book)
                button5.grid(row=1, column=4, pady=15, padx=10)
                          
            
            if av:
                tk.Label(show_books_frame,text="Availability: Διαθέσιμο").grid(row=6, column=0,padx =5 ,pady=5)
                j=0
                new_copies_btn = {}
                new_copies = tk.StringVar()
                new_copiesEntry = tk.Entry(show_books_frame, textvariable=new_copies)
                new_copiesEntry.grid(row=7, column=4, pady=10) 
                for k in books_bookstores_dict.keys():
                    av_copies = books_bookstores_dict[k]
                    tk.Label(show_books_frame,text=str(k)+", copies: "+str(av_copies)).grid(row=j+7, column=2,padx =5 ,pady=5)
                    j+=1
                    if k in admin_bookstores_list:
                        
                        def change_bookstore_copies(bookstore = k,book_id=b_id):
                            nonlocal new_copies
                            
                            new_copies_value = new_copies.get()
                        
                            indextd = bookstores_books_df[(bookstores_books_df['bookstore']==bookstore) & (bookstores_books_df['book_id']==book_id)].index[0]
                            bookstores_books_df.loc[indextd,'copies'] = bookstores_books_df.loc[indextd,'copies'] + int(new_copies_value)
                            books_df.loc[books_df['id'] == book_id,'bookstores'].values[0][bookstore] = bookstores_books_df.loc[indextd,'copies']
                            books_df.loc[books_df['id'] == book_id,'copies'] = books_df.loc[books_df['id'] == book_id,'copies'].values[0] + int(new_copies_value)
                            books_df2.loc[books_df2['id'] == book_id,'copies'] =  books_df2.loc[books_df2['id'] == book_id,'copies'].values[0] + int(new_copies_value)
                            
                            export_all_dataframes_to_csv()
                            
                        
                        new_copies_btn[k] = tk.Button(show_books_frame,text='Change',width=10,bg='grey',command=change_bookstore_copies)
                        new_copies_btn[k].grid(row=j+6, column=3, pady=10, padx=10)
                
            else:
                tk.Label(show_books_frame,text="Availability: Μη διαθέσιμο").grid(row=6, column=0,padx =5 ,pady=5)
            
        
        books_ui_btns_dict[book_id] = tk.Button(books_frame_2,text=book_title,width=40,bg='grey',command=show_book_admins)
        books_ui_btns_dict[book_id].grid(row=i+2, column=0, padx=7,pady=7)
        
    
    container.pack() 
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side='bottom', fill="x")
    
    
def del_users():
    admin_frame.pack_forget()
    show_users_frame.pack()
    tk.Button(show_users_frame,text='Back',width=5,bg='grey',command=lambda: go_back(show_users_frame,admin_frame)).grid(row=0, column=0)
    tk.Label(show_users_frame,text="Users:").grid(row=1, column=0)
    
    def delete_frame_widgets():
        for widget in show_users_frame.winfo_children():
            widget.destroy()
        del_users()
    
    users_del_btn_dict={}
    k = 1
    for u_id in user_df['id'].tolist():
        k+=1
        def del_user(user_id = u_id):
            user_df.drop(user_df.loc[user_df['id']==user_id].index, inplace=True)
            users_df.drop(users_df.loc[users_df['id']==user_id].index, inplace=True)
            export_users()
            export_user()
            delete_frame_widgets()
               
        user_un = user_df.loc[user_df['id'] == u_id,'username'].values[0]
        tk.Label(show_users_frame,text=user_un).grid(row=k, column=0,padx=5,pady=5)
        users_del_btn_dict[u_id] = tk.Button(show_users_frame,text='Delete user',width=15,bg='grey',command = del_user).grid(row=k, column=1,padx=5,pady=5)

user_balance = 0
def print_balance():
    global user_balance
    print("Balance:",user_balance,"€")

def user_ui(): # το menu του απλού χρήστη

    global user_frame , acc_details_frame,user_balance,recommendations_frame
    acc_details_frame = tk.Frame(r)
    user_frame = tk.Frame(r)
    recommendations_frame = tk.Frame(r)
    register_frame.pack_forget()
    login_frame.pack_forget()
    user_balance = user_df.loc[user_df['id'] == cuser_id, 'balance'].values[0]
    tk.Button(user_frame,text='Show Balance',width=15,bg='grey',command=print_balance).grid(row=0, column=0, pady=5)
    tk.Button(user_frame,text='Books',width=15,bg='grey',command=books).grid(row=1, column=0, pady=5)
    tk.Button(user_frame,text='Favorites',width=15,bg='grey',command=favorites).grid(row=2, column=0, pady=5)
    tk.Button(user_frame,text='Orders',width=15,bg='grey',command=orders).grid(row=3, column=0, pady=5)
    tk.Button(user_frame,text='Account details',width=15,bg='grey',command=acc_details).grid(row=4, column=0, pady=5)
    tk.Button(user_frame,text='Recommendations',width=15,bg='grey',command=recommendations).grid(row=5, column=0, pady=5)
    user_frame.pack()

def apa(cframe,row_num,book_cost,book_shipping_cost,book_copies): # υπολογίζει τα copies του βιβλίου που μπορεί να αγοράσει ο χρήστης ανάλογα το balance που εχει 
    apa_t =  (user_balance//book_cost)
    total_price = (apa_t*book_cost)+book_shipping_cost
    if total_price > user_balance:
        apa_t-=1
    if book_copies < apa_t:
        apa_t = book_copies
    apa_t = int(apa_t) 
    
    tk.Label(cframe, text='|| Μπορείτε να αγοράσετε '+str(apa_t)+' αντίτυπα από αυτό το βιβλίο.').grid(row=row_num, column=7,padx=5,pady=5)

def books():
    global user_balance
    user_frame.pack_forget()
    
    def delete_frame_widgets():
        for widget in books_frame.winfo_children():
            widget.destroy()
        books()
    
    books_frame = ttk.Frame(canvas,width=970)
    books_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=books_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar2.set)
    
    button = tk.Button(books_frame,text='Back',width=5,bg='grey',command=lambda: go_back(canvas,user_frame)) # κουμπί back
    button.grid(row=0, column=0, pady=10, padx=10) 
    button1 = tk.Button(books_frame,text='Show Balance',width=15,bg='grey',command=print_balance)
    button1.grid(row=0, column=1, pady=10 , padx=10)
    
    cuser_orders = user_df.loc[user_df['id'] == cuser_id,'orders'].values[0] # λίστα με τα orders του χρήστη
    cuser_favorites = user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0] # λίστα με τα favorites του χρήστη
    
    button_dict={} # για τα κουμπιά που προσθέτουν στην λίστα orders
    button_dict2={} # για τα κουμπιά που αφαιρούν στην λίστα orders
    
    btns_add_fav_dict={}
    btns_remove_fav_dict={}
    
    books_id_list = books_df['id'].tolist() # λίστα με τα id όλων των βιβλίων
    for k in range(len(books_id_list)):
        i = books_id_list[k] # i = id του βιβλίου όπως είναι στο αρχείο books.csv
        
        book_title = books_df.loc[k,'title']
        book_cost = books_df.loc[k,'cost']
        book_shipping_cost = books_df.loc[k,'shipping_cost'] 
        book_copies = books_df.loc[k,'copies']
        
        tk.Label(books_frame, text=book_title).grid(row=k+1, column=0,padx=5,pady=5)
        tk.Label(books_frame, text="Price: "+str(book_cost)+" €").grid(row=k+1, column=4,padx=5,pady=5)
        tk.Label(books_frame, text="Shipping cost: "+str(book_shipping_cost)+" €").grid(row=k+1, column=5,padx=5,pady=5)
        tk.Label(books_frame, text="Copies: "+str(book_copies)).grid(row=k+1, column=6,padx=5,pady=5)
        
        if books_df.loc[k,'availability']: # αν το βιβλίο είναι διαθέσιμο

            def add_order(book_id=i):
                global user_balance
                user_df.loc[user_df['id'] == cuser_id,'orders'].values[0].append(book_id) # εισάγει στην λίστα orders το id του βιβλίου
                
                # υπολογισμός νέου balance οταν προσθέτουμε το βιβλίο στα orders
                book_cost = books_df.loc[books_df['id'] == book_id,'cost'].values[0]
                shipping_cost = books_df.loc[books_df['id'] == book_id,'shipping_cost'].values[0]                            
                user_df.loc[user_df['id'] == cuser_id,'balance'] = round(user_balance - (book_cost + shipping_cost),2)
                users_df.loc[users_df['id'] == cuser_id,'balance'] = round(user_balance - (book_cost + shipping_cost),2)
                cuser_new_balance = user_df.loc[user_df['id'] == cuser_id,'balance'].values[0]
                user_balance = cuser_new_balance
                books_df.loc[books_df['id'] == book_id,'copies'] =  books_df.loc[books_df['id'] == book_id,'copies'].values[0] - 1
                books_df2.loc[books_df2['id'] == book_id,'copies'] =  books_df2.loc[books_df2['id'] == book_id,'copies'].values[0] - 1
                
                orders_df.loc[len(orders_df.index)] = [0,cuser_id,book_id] # ει΄σαγει την νέα εγγραφή συσχέτισης user-book στο orders dataframe export_user()
                export_all_dataframes_to_csv()
                delete_frame_widgets()
                    
                
            def remove_order(book_id=i):
                global user_balance
                user_df.loc[user_df['id'] == cuser_id,'orders'].values[0].remove(book_id) # αφαιρεί από την λίστα στο user_df['orders'] του χρήστη, το id του βιβλίου
                
                # υπολογισμός νέου balance οταν αφαιρείτε το βιβλίο από τα orders
                book_cost = books_df.loc[books_df['id'] == book_id,'cost'].values[0]
                shipping_cost = books_df.loc[books_df['id'] == book_id,'shipping_cost'].values[0]

                user_df.loc[user_df['id'] == cuser_id,'balance'] = round(user_balance + (book_cost + shipping_cost),2)
                users_df.loc[users_df['id'] == cuser_id,'balance'] = round(user_balance + (book_cost + shipping_cost),2)
                cuser_new_balance = user_df.loc[user_df['id'] == cuser_id,'balance'].values[0]
                books_df.loc[books_df['id'] == book_id,'copies'] =  books_df.loc[books_df['id'] == book_id,'copies'].values[0] + 1
                books_df2.loc[books_df2['id'] == book_id,'copies'] =  books_df2.loc[books_df2['id'] == book_id,'copies'].values[0] + 1
                user_balance = cuser_new_balance
                
                indextd = orders_df[(orders_df['user_id']==cuser_id) & (orders_df['book_id']==book_id)].index[0] # βρίσκει το index label του βιβλίου
                orders_df.drop(indextd,inplace=True) # διαγράφει από το dataframe orders την εγγραφη
                export_all_dataframes_to_csv()
                delete_frame_widgets()
    
                
            def add_favorite(book_id=i):         
                
                user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0].append(book_id) # εισάγει στην λίστα favorites το id του βιβλίου
            
                favorites_df.loc[len(favorites_df.index)] = [0,cuser_id,book_id] # ει΄σαγει την νέα εγγραφή συσχέτισης user-book στο favorites dataframe
                export_favorites()
                export_user()
                export_users()
                delete_frame_widgets()
 
                
            def remove_favorite(book_id=i):
                
                user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0].remove(book_id) # αφαιρεί από την λίστα στο user_df['favorites'] του χρήστη, το id του βιβλίου
                
                indextd = favorites_df[(favorites_df['user_id']==cuser_id) & (favorites_df['book_id']==book_id)].index[0] # βρίσκει το index label του βιβλίου
                favorites_df.drop(indextd,inplace=True) # διαγράφει από το dataframe orders την εγγραφη
                export_favorites()
                export_user()
                export_users()
                delete_frame_widgets()

            button_dict2[i] = tk.Button(books_frame,text='Remove from orders',width=15,bg='grey',command=remove_order) # τα buttons για την αφαίρεση από orders
            button_dict[i] = tk.Button(books_frame,text='Add to orders',width=15,bg='grey',command=add_order)  # τα buttons για την προσθήκη στα orders
            
            btns_remove_fav_dict[i] = tk.Button(books_frame,text='Remove from favorites',width=20,bg='grey',command=remove_favorite) # τα buttons για την αφαίρεση από favorites
            btns_add_fav_dict[i] = tk.Button(books_frame,text='Add to favorites',width=15,bg='grey',command=add_favorite)  # τα buttons για την προσθήκη στα favorites
            
            if i in cuser_orders:
                button_dict2[i].grid(row=k+1, column=2, pady=5,padx=5) 
            else:
                button_dict[i].grid(row=k+1, column=2, pady=5,padx=5)  
            
            if i in cuser_favorites: # αν το βιβλίο με βαση το id ειναι στα αγαπημένα του χρήστη εμφανίζει το κουμπί για την αφαίρεση
                btns_remove_fav_dict[i].grid(row=k+1, column=1, pady=5,padx=5)
            else: # αν το βιβλίο με βαση το id ΔΕΝ ειναι στα αγαπημένα του χρήστη εμφανίζει το κουμπί για την προσθήκη
                btns_add_fav_dict[i].grid(row=k+1, column=1, pady=5,padx=5) 
          
                
            tk.Label(books_frame, text='Άμεσα διαθέσιμο').grid(row=k+1, column=3,padx=5,pady=5)
            
            apa(books_frame,k+1,book_cost,book_shipping_cost,book_copies)

        else: # αν το βιβλίο δεν είναι διαθέσιμο
            tk.Label(books_frame, text='Μη διαθέσιμο').grid(row=k+1, column=1,padx=5,pady=5)
            
    container.pack() 
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side='bottom', fill="x")

def orders():
    global user_balance
    user_frame.pack_forget()
    
    def delete_frame_widgets():
        for widget in orders_frame.winfo_children():
            widget.destroy()
        orders()
    
    orders_frame = ttk.Frame(canvas,width=970)
    orders_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=orders_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    button = tk.Button(orders_frame,text='Back',width=5,bg='grey',command=lambda: go_back(canvas,user_frame)) # κουμπί back
    button.grid(row=0, column=0, pady=5 , padx=10) 
    button1 = tk.Button(orders_frame,text='Show Balance',width=15,bg='grey',command=print_balance)
    button1.grid(row=0, column=1, pady=5 , padx=10)
    
    cuser_orders = user_df.loc[user_df['id'] == cuser_id,'orders'].values[0] # λίστα με τα orders του χρήστη

    btns_remove_order_dict={}
    btns_rate_book={}
    btns_show_rating={}
    
    if len(cuser_orders) > 0:
        for k in range(len(cuser_orders)):
            i = cuser_orders[k]
            
            book_title = books_df.loc[books_df['id'] == i,'title'].values[0]
            book_cost = books_df.loc[books_df['id'] == i,'cost'].values[0]
            book_shipping_cost = books_df.loc[books_df['id'] == i,'shipping_cost'].values[0]
            book_copies = books_df.loc[books_df['id'] == i,'copies'].values[0]
            
            tk.Label(orders_frame, text=book_title).grid(row=k+1, column=0,padx=5,pady=5)
            tk.Label(orders_frame, text="Price: "+str(book_cost)+" €").grid(row=k+1, column=4,padx=5,pady=5)
            tk.Label(orders_frame, text="Shipping cost: "+str(book_shipping_cost)+" €").grid(row=k+1, column=5,padx=5,pady=5)
            tk.Label(orders_frame, text="Copies: "+str(book_copies)).grid(row=k+1, column=6,padx=5,pady=5)
            
            def rate_book(book_id=i):
                
                user_rate = float(input("Δώστε την βαθμολογία: "))
                user_rate = round(user_rate,1)
                c_an = int(input("Θέλετε να γράψετε ένα σχόλιο? 1.ναι /2.οχι"))
              
                if c_an == 1:
                    user_comment = input("Σχόλια: ")
                    books_df.loc[books_df['id'] == book_id ,'ratings'].values[0][cuser_id] = [user_rate,user_comment]
                    ratings_df.loc[len(ratings_df.index)] = [cuser_id,book_id,user_rate,user_comment]
                else:
                    books_df.loc[books_df['id'] == book_id ,'ratings'].values[0][cuser_id] = [user_rate,'']
                    ratings_df.loc[len(ratings_df.index)] = [cuser_id,book_id,user_rate,'']
     
                export_books()
                export_ratings()
                delete_frame_widgets()
               
                export_all_dataframes_to_csv()
                delete_frame_widgets()
                
            def show_rating(book_id=i):
                l = books_df.loc[books_df['id'] == book_id ,'ratings'].values[0][cuser_id]
                print("Η βαθμολογία που δώσατε είναι:",l[0])
                if l[1] == "":
                    print("Δεν έχετε κάνει σχόλιο.")
                else:
                    print("Το σχόλιό σας:\n",l[1])


            def remove_order(book_id=i):
                global user_balance
                user_df.loc[user_df['id'] == cuser_id,'orders'].values[0].remove(book_id) # αφαιρεί από την λίστα στο user_df['orders'] του χρήστη, το id του βιβλίου
                
                # υπολογισμός νέου balance οταν αφαιρείτε το βιβλίο από τα orders
                book_cost = books_df.loc[books_df['id'] == book_id,'cost'].values[0]
                shipping_cost = books_df.loc[books_df['id'] == book_id,'shipping_cost'].values[0]

                user_df.loc[user_df['id'] == cuser_id,'balance'] = round(user_balance + (book_cost + shipping_cost),2)
                users_df.loc[users_df['id'] == cuser_id,'balance'] = round(user_balance + (book_cost + shipping_cost),2)
                cuser_new_balance = user_df.loc[user_df['id'] == cuser_id,'balance'].values[0]
                books_df.loc[books_df['id'] == book_id,'copies'] =  books_df.loc[books_df['id'] == book_id,'copies'].values[0] + 1
                books_df2.loc[books_df2['id'] == book_id,'copies'] =  books_df2.loc[books_df2['id'] == book_id,'copies'].values[0] + 1
                user_balance = cuser_new_balance
                    
                indextd = orders_df[(orders_df['user_id']==cuser_id) & (orders_df['book_id']==book_id)].index[0] # βρίσκει το index label του βιβλίου
                orders_df.drop(indextd,inplace=True) # διαγράφει από το dataframe orders την εγγραφη
                export_all_dataframes_to_csv()
                delete_frame_widgets()
             
            btns_remove_order_dict[i] = tk.Button(orders_frame,text='Remove from orders',width=20,bg='grey',command=remove_order) # τα buttons για την αφαίρεση από favorites
            btns_remove_order_dict[i].grid(row=k+1, column=1, pady=5,padx=5)             
                    
            tk.Label(orders_frame, text='Άμεσα διαθέσιμο').grid(row=k+1, column=3,padx=5,pady=5)
            
            btns_rate_book[i] = tk.Button(orders_frame,text='rate the book',width=20,bg='grey',command=rate_book)
            btns_rate_book[i].grid(row=k+1, column=7,padx=5,pady=5)
            
            if cuser_id in books_df.loc[books_df['id'] == i ,'ratings'].values[0]:
                btns_show_rating[i] = tk.Button(orders_frame,text='Show my rating',width=20,bg='grey',command=show_rating)
                btns_show_rating[i].grid(row=k+1, column=8,padx=5,pady=5)
            else:
                tk.Label(orders_frame, text="Δεν έχετε κάνει αξιολόγηση για αυτό το βιβλίο").grid(row=k+1, column=8,padx=5,pady=5)
            
            

    else:
        tk.Label(orders_frame, text="Η λίστα με τις παραγγελίες είναι άδεια!").grid(row=3, column=2,padx=5,pady=5)
            
    container.pack() 
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side='bottom', fill="x")

def favorites():
    global user_balance
    user_frame.pack_forget()
    
    def delete_frame_widgets():
        for widget in favorites_frame.winfo_children():
            widget.destroy()
        favorites()
    
    favorites_frame = ttk.Frame(canvas,width=970)
    favorites_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=favorites_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def remove_all_favorites():
        user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0].clear()
        favorites_df.drop(favorites_df.index[favorites_df['user_id'] == cuser_id],inplace = True)
        export_favorites()
        export_user()
        delete_frame_widgets()
    
    button = tk.Button(favorites_frame,text='Back',width=5,bg='grey',command=lambda: go_back(canvas,user_frame)) # κουμπί back
    button.grid(row=0, column=0, pady=5 , padx=10) 
    button1 = tk.Button(favorites_frame,text='Show Balance',width=15,bg='grey',command=print_balance)
    button1.grid(row=0, column=1, pady=5 , padx=10)
    
    cuser_favorites = user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0] # λίστα με τα favorites του χρήστη

    btns_remove_fav_dict={}
    
    if len(cuser_favorites) > 0:
        button2 = tk.Button(favorites_frame,text='Remove all favorites',width=15,bg='grey',command=remove_all_favorites)
        button2.grid(row=0, column=2, pady=5 , padx=10)
        for k in range(len(cuser_favorites)):
            i = cuser_favorites[k]
            
            book_title = books_df.loc[books_df['id'] == i,'title'].values[0]
            book_cost = books_df.loc[books_df['id'] == i,'cost'].values[0]
            book_shipping_cost = books_df.loc[books_df['id'] == i,'shipping_cost'].values[0]
            book_copies = books_df.loc[books_df['id'] == i,'copies'].values[0]
            
            tk.Label(favorites_frame, text=book_title).grid(row=k+1, column=0,padx=5,pady=5)
            tk.Label(favorites_frame, text="Price: "+str(book_cost)+" €").grid(row=k+1, column=4,padx=5,pady=5)
            tk.Label(favorites_frame, text="Shipping cost: "+str(book_shipping_cost)+" €").grid(row=k+1, column=5,padx=5,pady=5)
            tk.Label(favorites_frame, text="Copies: "+str(book_copies)).grid(row=k+1, column=6,padx=5,pady=5)
            
            av = books_df.loc[books_df['id'] == i,'availability'].values[0]
            if av: # αν το βιβλίο είναι διαθέσιμο    
    
                def remove_favorite(book_id=i):
                    
                    user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0].remove(book_id) # αφαιρεί από την λίστα στο user_df['favorites'] του χρήστη, το id του βιβλίου
                    
                    indextd = favorites_df[(favorites_df['user_id']==cuser_id) & (favorites_df['book_id']==book_id)].index[0] # βρίσκει το index label του βιβλίου
                    favorites_df.drop(indextd,inplace=True) # διαγράφει από το dataframe favorites την εγγραφη
                    export_favorites()
                    
                    delete_frame_widgets()
             
                btns_remove_fav_dict[i] = tk.Button(favorites_frame,text='Remove from favorites',width=20,bg='grey',command=remove_favorite) # τα buttons για την αφαίρεση από favorites
                       
                if i in cuser_favorites: # αν το βιβλίο με βαση το id ειναι στα αγαπημένα του χρήστη εμφανίζει το κουμπί για την αφαίρεση
                    btns_remove_fav_dict[i].grid(row=k+1, column=1, pady=5,padx=5)             
                    
                tk.Label(favorites_frame, text='Άμεσα διαθέσιμο').grid(row=k+1, column=3,padx=5,pady=5)
                
                apa(favorites_frame,k+1,book_cost,book_shipping_cost,book_copies)
                
                tk.Label(favorites_frame, text='|| Μπορείτε να αγοράσετε '+str(apa)+' αντίτυπα από αυτό το βιβλίο.').grid(row=k+1, column=7,padx=5,pady=5)

            else: # αν το βιβλίο δεν είναι διαθέσιμο
                tk.Label(favorites_frame, text='Μη διαθέσιμο').grid(row=k+1, column=1,padx=5,pady=5)
    else:
        tk.Label(favorites_frame, text="Η λίστα με τα αγαπημένα είναι άδεια!").grid(row=3, column=2,padx=5,pady=5)
            
    container.pack() 
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scrollbar2.pack(side='bottom', fill="x")
    
def acc_details():
    user_frame.pack_forget()
    
    un = user_df.loc[user_df['id'] == cuser_id,'username'].values[0]
    c_psw = user_df.loc[user_df['id'] == cuser_id,'password'].values[0]
    c_address = user_df.loc[user_df['id'] == cuser_id,'address'].values[0]
    c_city = user_df.loc[user_df['id'] == cuser_id,'city'].values[0]
    
    def delete_frame_widgets():
        for widget in acc_details_frame.winfo_children():
            widget.destroy()
        acc_details()
    
    def change_password():
        new_psw = psw.get()
        user_df.loc[user_df['id'] == cuser_id,'password'] = new_psw
        users_df.loc[users_df['id'] == cuser_id,'password'] = new_psw
        
        export_users()
        export_user()
        delete_frame_widgets()
        
        
    def change_city():
        new_city = city.get()
        user_df.loc[user_df['id'] == cuser_id,'city'] = new_city
        users_df.loc[users_df['id'] == cuser_id,'city'] = new_city
        
        export_users()
        export_user()
        delete_frame_widgets()
        
        
    def change_address():
        new_adr = adr.get()
        user_df.loc[user_df['id'] == cuser_id,'address'] = new_adr
        users_df.loc[users_df['id'] == cuser_id,'address'] = new_adr
        
        export_users()
        export_user()
        delete_frame_widgets()
        
        
    def change_balance():
        global user_balance
        new_balance = float(balance.get()) + user_balance
        user_balance = new_balance
        user_df.loc[user_df['id'] == cuser_id,'balance'] = user_balance
        users_df.loc[users_df['id'] == cuser_id,'balance'] = user_balance
        
        export_users()
        export_user()
        delete_frame_widgets()
        
        
    usernameLabel = tk.Label(acc_details_frame, text="Username: "+str(un))
    usernameLabel.grid(row=0, column=0)
    
    pswLabel = tk.Label(acc_details_frame, text="Password: "+str(c_psw))
    pswLabel.grid(row=1, column=0 , pady=10)
    psw = tk.StringVar()
    passwordEntry = tk.Entry(acc_details_frame, textvariable=psw)
    passwordEntry.grid(row=1, column=1,pady=10) 
    button = tk.Button(acc_details_frame,text='Change Password',width=15,bg='grey',command=change_password)
    button.grid(row=1, column=2, pady=15, padx=10)
    
    addressLabel = tk.Label(acc_details_frame, text="Address: "+str(c_address))
    addressLabel.grid(row=2, column=0, pady=10)
    adr = tk.StringVar()
    addressEntry = tk.Entry(acc_details_frame, textvariable=adr)
    addressEntry.grid(row=2, column=1, pady=10) 
    button2 = tk.Button(acc_details_frame,text='New address',width=15,bg='grey',command=change_address)
    button2.grid(row=2, column=2, pady=15, padx=10)
    
    cityLabel = tk.Label(acc_details_frame, text="City: "+str(c_city))
    cityLabel.grid(row=3, column=0, pady=10)
    city = tk.StringVar()
    cityEntry = tk.Entry(acc_details_frame, textvariable=city)
    cityEntry.grid(row=3, column=1, pady=10) 
    button3 = tk.Button(acc_details_frame,text='New city',width=15,bg='grey',command=change_city)
    button3.grid(row=3, column=2, pady=15, padx=10)
    
    balanceLabel = tk.Label(acc_details_frame, text="Balance: "+str(user_balance)+" €")
    balanceLabel.grid(row=4, column=0, pady=10)
    balance = tk.StringVar()
    balanceEntry = tk.Entry(acc_details_frame, textvariable=balance)
    balanceEntry.grid(row=4, column=1, pady=10) 
    button4 = tk.Button(acc_details_frame,text='Προσθήκη χρημάτων',width=20,bg='grey',command=change_balance)
    button4.grid(row=4, column=2, pady=15, padx=10)
    
    back_button = tk.Button(acc_details_frame,text='Back',width=5,bg='grey',command=lambda: go_back(acc_details_frame,user_frame))
    back_button.grid(row=6, column=0, pady=15 , padx=10)
    
    acc_details_frame.pack()

def recommendations():
    user_frame.pack_forget()
    
# ---------------- εύρεση τυχαίων βιβλίων με βάση την κατηγορία βιβλι
    def delete_frame_widgets():
        for widget in recommendations_frame.winfo_children():
            widget.destroy()
        recommendations()
    
    fav_books_categories_list = []
    favorites_list = user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0]
    orders_list = user_df.loc[user_df['id'] == cuser_id,'orders'].values[0]
    
    if len(favorites_list) > 0: # αν η λίστα με τα αγαπημένα έχει έστω ένα στοιχείο τότε εμφανίζονται τυχαίες προτάσεις βιβλίων.
        for i in favorites_list:
            books_cats_list = books_df.loc[books_df['id'] == i,'categories'].values[0]
            for k in books_cats_list:
                fav_books_categories_list.append(k)
    
        categories_dict = {}
      
        for i in fav_books_categories_list:
            if i in categories_dict:
                categories_dict[i] += 1
            else:
                categories_dict[i] = 1
        
        categories_sorted_list = sorted(categories_dict.items(), key=lambda x: x[1], reverse=True)
        key_cat = categories_sorted_list[0][0] # η κατηγορία με την μεγαλύτερη συχνότητα εμφάνισης.
        
        book_id_list = categories_df.loc[categories_df['cat'] == key_cat,'book_id'].tolist()
        
        for i in favorites_list:
            if i in book_id_list:
                book_id_list.remove(i)
        for i in orders_list:
            if i in book_id_list:
                book_id_list.remove(i)

        if len(book_id_list) < 1:
            tk.Label(recommendations_frame, text="Δεν υπάρχουν ροτάσεις με βάση την κατηγορία: "+str(key_cat)).grid(row=1, column=0)
        else:
            k1 = random.randrange(len(book_id_list))
            random_recommendations = random.choices(book_id_list,k=k1)
            random_recommendations = set(random_recommendations)
            random_recommendations = list(random_recommendations)
            tk.Label(recommendations_frame, text="Προτάσεις με βάση την κατηγορία: "+str(key_cat)).grid(row=1, column=0)
        
        button_dict={} # για τα κουμπιά που προσθέτουν στην λίστα orders
        btns_add_fav_dict={}
        
        cntr = 1
        for i in random_recommendations:
            cntr+=1
            book_title = books_df.loc[books_df['id'] == i,'title'].values[0]
            book_cost = books_df.loc[books_df['id'] == i,'cost'].values[0]
            book_shipping_cost = books_df.loc[books_df['id'] == i,'shipping_cost'].values[0]
            book_copies = books_df.loc[books_df['id'] == i,'copies'].values[0]
            
            tk.Label(recommendations_frame, text=book_title).grid(row=cntr, column=0,padx=5,pady=5)
            tk.Label(recommendations_frame, text="Price: "+str(book_cost)+" €").grid(row=cntr, column=4,padx=5,pady=5)
            tk.Label(recommendations_frame, text="Shipping cost: "+str(book_shipping_cost)+" €").grid(row=cntr, column=5,padx=5,pady=5)
            tk.Label(recommendations_frame, text="Copies: "+str(book_copies)).grid(row=cntr, column=6,padx=5,pady=5)
            
            if books_df.loc[books_df['id'] == i,'availability'].item(): # αν το βιβλίο είναι διαθέσιμο

                def add_order(book_id=i):
                    global user_balance
                    user_df.loc[user_df['id'] == cuser_id,'orders'].values[0].append(book_id) # εισάγει στην λίστα orders το id του βιβλίου
                    
                    # υπολογισμός νέου balance οταν προσθέτουμε το βιβλίο στα orders
                    book_cost = books_df.loc[books_df['id'] == book_id,'cost'].values[0]
                    shipping_cost = books_df.loc[books_df['id'] == book_id,'shipping_cost'].values[0]                            
                    user_df.loc[user_df['id'] == cuser_id,'balance'] = round(user_balance - (book_cost + shipping_cost),2)
                    users_df.loc[users_df['id'] == cuser_id,'balance'] = round(user_balance - (book_cost + shipping_cost),2)
                    cuser_new_balance = user_df.loc[user_df['id'] == cuser_id,'balance'].values[0]
                    user_balance = cuser_new_balance
                    books_df.loc[books_df['id'] == book_id,'copies'] =  books_df.loc[books_df['id'] == book_id,'copies'].values[0] - 1
                    books_df2.loc[books_df2['id'] == book_id,'copies'] =  books_df2.loc[books_df2['id'] == book_id,'copies'].values[0] - 1
                    
                    orders_df.loc[len(orders_df.index)] = [0,cuser_id,book_id] # ει΄σαγει την νέα εγγραφή συσχέτισης user-book στο orders dataframe export_user()
                    export_user()
                    export_users()
                    export_orders()
                    export_books()
                    export_books2()
                    delete_frame_widgets()

                    
                def add_favorite(book_id=i):         
                    
                    user_df.loc[user_df['id'] == cuser_id,'favorites'].values[0].append(book_id) # εισάγει στην λίστα favorites το id του βιβλίου
                
                    favorites_df.loc[len(favorites_df.index)] = [0,cuser_id,book_id] # ει΄σαγει την νέα εγγραφή συσχέτισης user-book στο favorites dataframe
                    export_favorites()
                    export_user()
                    delete_frame_widgets()

                button_dict[i] = tk.Button(recommendations_frame,text='Add to orders',width=15,bg='grey',command=add_order)  # τα buttons για την προσθήκη στα orders
                
                btns_add_fav_dict[i] = tk.Button(recommendations_frame,text='Add to favorites',width=15,bg='grey',command=add_favorite)  # τα buttons για την προσθήκη στα favorites
                

                button_dict[i].grid(row=cntr, column=2, pady=5,padx=5)  

                btns_add_fav_dict[i].grid(row=cntr, column=1, pady=5,padx=5) 
              
                    
                tk.Label(recommendations_frame, text='Άμεσα διαθέσιμο').grid(row=cntr, column=3,padx=5,pady=5)
                
                apa(recommendations_frame,cntr,book_cost,book_shipping_cost,book_copies)

            else: # αν το βιβλίο δεν είναι διαθέσιμο
                tk.Label(recommendations_frame, text='Μη διαθέσιμο').grid(row=cntr, column=1,padx=5,pady=5)
    else:
        tk.Label(recommendations_frame, text="Δεν υπάρχουν προτάσεις").grid(row=1, column=0)
    
    back_button = tk.Button(recommendations_frame,text='Back',width=5,bg='grey',command=lambda: go_back(recommendations_frame,user_frame))
    back_button.grid(row=0, column=0, pady=15)

    recommendations_frame.pack()
    
def switch_to_login_menu():
    login_frame.pack() 
    start_menu.pack_forget()
    
def switch_to_register_menu():
    register_frame.pack() 
    start_menu.pack_forget()
    
def go_back(cur_frame,prev): # επιστροφή στο προηγούμενο frame
    for widget in cur_frame.winfo_children():
        widget.destroy()
    prev.pack() 
    cur_frame.pack_forget()
    

# LOGIN AND REGISTER FUNCTIONS
def login():
    cntr = 3
    un = str(username.get())
    psw = str(password.get())
    global cuser_id 
    def un_psw_attempts():
        nonlocal cntr
        cntr -= 1
        if cntr == 0:
            r.destroy()
            return '',''
        print("Τα στοιχεία που δώσατε είναι λάθος! Απομένουν",cntr,"προσπάθειες!")
        un = input("Username: ")
        psw = input("Password: ")
        return un,psw
    while 1:
        if un in user_df["username"].tolist(): # αν το username υπάρχει στο dataframe με τους απλούς χρήστες.
            psw2 = user_df.loc[user_df['username'] == un ,"password"].values[0]
            if psw == psw2:
                cuser_id = user_df.loc[user_df['username'] == un ,"id"].values[0]
                user_ui()
                break
            else:
                un,psw = un_psw_attempts()
        elif un in admin_df["username"].tolist():  # αν το username υπάρχει στο dataframe με τους admins.
            psw2 = admin_df.loc[admin_df['username'] == un ,"password"].values[0]
            if psw == psw2:
                global cadmin_id
                cadmin_id = admin_df.loc[admin_df['username'] == un ,"id"].values[0]
                admin_ui()
                break
            else:
                un,psw = un_psw_attempts()
        else:
            un,psw = un_psw_attempts()
        if cntr == 0:
            break
    
def register():
    un = str(username_r.get())
    psw = str(password_r.get())
    adr = str(Address.get())
    bal = str(balance.get())
    cit = str(city.get())
    global cuser_id
    while un in user_df["username"].tolist() or un in admin_df["username"].tolist():
        print('Το όνομα χρήστη υπάρχει ήδη! Δοκιμάστε κάποιο άλλο.')
        un = input("Εισάγετε username: ")
    sc = ['!','@','#','$','%','^','&','*','(',')','`','~','{','}','[',']',';',':',',','.','<','>',"|",'/','?',"'",'"\"']
    f=0
    while 1:
        if len(psw) >= 8:
            for i in psw:
                if i in sc:
                    f=1
                    break
            if f:
                break
            else:
                print("\nΤο password πρέπει να έχει 8+ χαρακτήρες και ένα τουλάχιστον ειδικό χαρακτήρα!")
        else:
            print("\nΤο password πρέπει να έχει 8+ χαρακτήρες και ένα τουλάχιστον ειδικό χαρακτήρα!")
        psw = input("Password: ")
    if user_df.empty :
        cuser_id = 0
        user_df.append([cuser_id,un,psw,adr,cit,bal,'',''])
        users_df.append([cuser_id,un,psw,adr,cit,bal])
    else:
        last_id = user_df.iloc[-1].tolist()
        cuser_id = int(last_id[0])+1
        user_df.loc[len(user_df.index)] = [cuser_id,un,psw,adr,cit,bal,'','']
        users_df.loc[len(user_df.index)] = [cuser_id,un,psw,adr,cit,bal]
    export_users()
    create_dfs()
    user_ui()

# start menu
start_menu.pack()
login_button = tk.Button(start_menu,text='Login',width=25,command=switch_to_login_menu)
login_button.pack(pady=25)

register_button = tk.Button(start_menu,text='Register',width=25,command=switch_to_register_menu)
register_button.pack()

# login frame:
usernameLabel = tk.Label(login_frame, text="Username").grid(row=0, column=0)
username = tk.StringVar()
usernameEntry = tk.Entry(login_frame, textvariable=username).grid(row=0, column=1)  

passwordLabel = tk.Label(login_frame,text="Password").grid(row=1, column=0)  
password = tk.StringVar()
passwordEntry = tk.Entry(login_frame, textvariable=password, show='*').grid(row=1, column=1) 

login_button = tk.Button(login_frame,text='Login',width=10,bg='grey',command=login).grid(row=2, column=0, pady=15)
back_button = tk.Button(login_frame,text='Back',width=5,bg='grey',command=lambda: go_back(login_frame,start_menu)).grid(row=3, column=0, pady=15)

# Register frame:
usernameLabel = tk.Label(register_frame, text="Username").grid(row=0, column=0)
username_r = tk.StringVar()
usernameEntry = tk.Entry(register_frame, textvariable=username_r).grid(row=0, column=1)  

passwordLabel = tk.Label(register_frame,text="Password").grid(row=1, column=0)  
password_r = tk.StringVar()
passwordEntry = tk.Entry(register_frame, textvariable=password_r, show='*').grid(row=1, column=1) 

AddressLabel = tk.Label(register_frame, text="Address").grid(row=2, column=0)
Address = tk.StringVar()
AddressEntry = tk.Entry(register_frame, textvariable=Address).grid(row=2, column=1)  

cityLabel = tk.Label(register_frame, text="City").grid(row=3, column=0)
city = tk.StringVar()
cityEntry = tk.Entry(register_frame, textvariable=city).grid(row=3, column=1)  

balanceLabel = tk.Label(register_frame, text="Balance").grid(row=4, column=0)
balance = tk.StringVar()
balanceEntry = tk.Entry(register_frame, textvariable=balance).grid(row=4, column=1)  

register_button = tk.Button(register_frame,text='Register',width=10,bg='grey',command=register).grid(row=5, column=0, pady=15)
back_button = tk.Button(register_frame,text='Back',width=5,bg='grey',command=lambda: go_back(register_frame,start_menu)).grid(row=6, column=0, pady=15)

r.mainloop()








