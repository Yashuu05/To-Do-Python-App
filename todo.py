"""
creating a simple to do app
"""
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
# ----------------------------------------------

class myapp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('To Do app')
        self.geometry('600x350')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # set up databse with creation of table
        self.steup_databse()
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------
        # main dashboard widgets
        self.upper_frame = ctk.CTkFrame(self, width=600, height=100, fg_color='#F5EFFF')
        self.upper_frame.grid(row=0, column=0, padx=10, pady=10)

        self.main_frame = ctk.CTkScrollableFrame(self, width=550, height=250, fg_color='#F5EFFF')
        self.main_frame.grid(row=1, column=0, padx=10, pady=10)
        # add button
        self.add_btn = ctk.CTkButton(master=self.upper_frame, text='ADD', font=('Arial',12,'bold'), fg_color='#CDC1FF', corner_radius=6, text_color='black', border_width=2,border_color='#B13BFF', command=self.add)
        self.add_btn.grid(row=0, column=1, padx=10, pady=10)
        # exit button
        ctk.CTkButton(master=self.upper_frame, text='Exit', font=('Arial',12,'bold'), fg_color='#E14434', corner_radius=6, border_width=2, border_color='black', command=self.exit).grid(row=0, column=0, padx=10,pady=10)

        # call the function which fetch the stored data from database
        self.load_tasks_from_db()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    # logic to close the app
    def exit(self):
        self.destroy()
    # -------------------------------------------------------------
    # logic to add the tasks
    def add(self):
        self.withdraw()
        # create new window
        root = ctk.CTkToplevel()
        root.title('Add tasks')
        root.geometry('400x200')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # ----------------------------------------------------------
        def cancel():
            root.destroy()
            self.deiconify()
        # -----------------------------------------------------------
        def save():
            task_text = task_entry.get().strip()
            if not task_text:
                messagebox.showerror('Error','task cannot be empty')
            else:
                #self.display_task(task_text)
                # insert the task into database
                self.cursor.execute("INSERT INTO tasks (task_text) VALUES (?)", (task_text,))
                self.conn.commit()
                messagebox.showinfo('info','task added')
                # call display_task() to display stored tasks
                self.display_task(task_text=task_text)
        #--------------------------------------------------------------
        def clear():
            task_entry.delete(0, ctk.END)
        # -------------------------------------------------------------
        # frame
        frame = ctk.CTkFrame(master=root, width=390, height=200, fg_color='#F5EFFF')
        frame.grid(row=0, column=0, padx=10, pady=10)
        # user input
        task_entry = ctk.CTkEntry(frame, width=330, placeholder_text='enter task')
        task_entry.grid(row=0,column=0,pady=10,padx=10, columnspan=3)
        # cancel button
        cancel_btn = ctk.CTkButton(frame, text='cancel', command=cancel, fg_color='#DC2525', font=('arial',12,'bold'), hover_color='#FFDCDC',width=100, border_width=2, border_color='black')
        cancel_btn.grid(row=2, column=0, padx=10, pady=10)
        # save button
        save_btn = ctk.CTkButton(frame, text='save', command=save, fg_color='#B6F500', font=('arial',12,'bold'), text_color='black', hover_color='#DDF6D2', width=100, border_width=2, border_color='black')
        save_btn.grid(row=2, column=2, padx=10, pady=10)
        # clear button
        ctk.CTkButton(frame, text='clear', command=clear, fg_color='#FFE700', font=('arial',12,'bold'), text_color='black', hover_color='#FEFFA7', width=100, border_width=2, border_color='black').grid(row=2, column=1, padx=10,pady=10)
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # function to display the task on main window
    def display_task(self,task_text, task_id=None, status=0):
        # saving checkbox mark to database
        # ---------------------------------------------------------------------------------------
        def checkbox_callback():
            new_status = 1 if checkbox.get() == 1 else 0
            self.cursor.execute("UPDATE tasks SET status=? WHERE id=?", (new_status,task_id))
            self.conn.commit()
        # ----------------------------------------------------------------------------------------
        # function to edit the task
        def edit():
            self.withdraw()
            # create a new window to edit the task
            window = ctk.CTkToplevel()
            window.title('Edit Task')
            window.geometry('400x200')
            # ----------------------------------------------------------------
            # function to go back (no edit)
            def cancel():
                window.destroy()
                self.deiconify()
            # -----------------------------------------------------------------
            # function to clear the field
            def clear():
                task_entry.delete(0, ctk.END)
            # -----------------------------------------------------------------
            # function to allow user to edit the task
            def update_task():
                new_task = task_entry.get().strip()
                if new_task:
                    self.cursor.execute("UPDATE tasks SET task_text=? WHERE id=?", (new_task, task_id))
                    self.conn.commit()
                    checkbox.configure(text=new_task)
                    messagebox.showinfo('Info','task updated successfully')
                else:
                    messagebox.showerror('Error','Task text cannot be empty.')
            # --------------------------------------------------------------------------------------------------
            # widgets for update task function [edit()]
            # frame to hold entry field, clear and back button
            frame = ctk.CTkFrame(window,corner_radius=6, fg_color='#F5EFFF')
            frame.pack(padx=10, pady=10, fill='both',expand=True)
            # configure 3 columns with equal weights
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)
            # input from user 
            task_entry = ctk.CTkEntry(frame, width=300)
            task_entry.grid(row=0,column=0,columnspan=3, padx=10, pady=(20,10), sticky='ew')
            task_entry.insert(0, task_text)  # pre-fill old text
            # back  button
            back_btn = ctk.CTkButton(frame, text='Cancel', command=cancel, font=('Arial',10,'bold'), fg_color='#E14434', text_color='white', border_width=2, border_color='black', width=50)
            back_btn.grid(row=1, column=0, padx=5, pady=10, sticky='ew')
            # clear button
            clear_btn = ctk.CTkButton(frame, text='Clear', command=clear, font=('Arial',10,'bold'), fg_color='#FFCC00', text_color='black', border_width=2, border_color='black',width=50)
            clear_btn.grid(row=1, column=1, padx=5, pady=10, sticky='ew')
            # update button
            update_btn = ctk.CTkButton(frame, text='update', command=update_task, font=('Arial',10,'bold'), fg_color='#06923E', text_color='white', border_width=2, border_color='black',width=50)
            update_btn.grid(row=1, column=2, padx=5, pady=10, sticky='ew')
        # ------------------------------------------------------------------------------------------------------------------------
        # task_display() widgets
        # create a new frame to store task
        task_frame = ctk.CTkFrame(self.main_frame, fg_color='#CDC1FF', corner_radius=4)
        task_frame.pack(fill='x', padx=10, pady=5)
        # checkbox to mark completed task
        checkbox = ctk.CTkCheckBox(task_frame, text=task_text, text_color='black', command=checkbox_callback)
        if status == 1:
            checkbox.select()
        checkbox.pack(side='left', padx=5)
        # -----------------------------------------------------------------------------------------------------------------------
        # delete entrire frame and checkbox 
        def delete():
            # delte from DB only if saved
            if  task_text and task_id:
                self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
                self.conn.commit()
                # delete checkbox
                checkbox.destroy()
                # delete frame
                task_frame.destroy()
            else:
                messagebox.showerror('Error','No tasks exist to delete.')
        # ------------------------------------------------------------------------------------------------------------------------
        # create a subframe for Edit and delete button
        button_frame = ctk.CTkFrame(task_frame, fg_color='transparent')
        button_frame.pack(side='right')
        # button to delete the task
        ctk.CTkButton(button_frame, command=delete, width=35, text='D', font=('Arial',12,'bold'), fg_color='#FF6363', border_color='black', border_width=1, corner_radius=4).pack(side='right',padx=0)
        # button to edit the task        
        ctk.CTkButton(button_frame, command=edit, width=35, text='E', font=('Arial',12,'bold'), fg_color='#06923E', border_color='black', border_width=1, corner_radius=4).pack(side='right', padx=0)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def steup_databse(self):
        # creates dabase if not exist
        self.conn = sqlite3.connect('task.db')
        self.cursor = self.conn.cursor()
        # creates a table if not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_text TEXT NOT NULL,
                status INTEGER DEFAULT 0  -- 0 = not done, 1 = completed
            )
        ''')
        self.conn.commit()
    # ---------------------------------------------------------------------------------------------------------
    # this function fetches all stored data from the database and displays it by calling display_task() function
    def load_tasks_from_db(self):
        self.cursor.execute('SELECT id, task_text, status FROM tasks')
        rows = self.cursor.fetchall()
        for task_id, task_text, status in rows:
            self.display_task(task_text, task_id=task_id, status=status)
# ------------------------------------------------------------------------------------------------------------

# run the app
app = myapp()
app.mainloop()
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------