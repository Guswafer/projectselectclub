import tkinter as tk
import sqlite3
import tkinter.messagebox as messagebox
from tkinter import ttk, filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
#codeทั้งหมด
def plusdelscore():
    def comment():
        # สร้างหน้าต่าง Tkinter
        root = tk.Toplevel()
        root.title("โปรแกรมเพิ่มและลบคะแนนจิตพิสัย")
        root.geometry("700x450")
        # นำเข้าภาพพื้นหลัง
        background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\comment.png")
        background_photo = ImageTk.PhotoImage(background_image)

        # สร้าง Label สำหรับภาพพื้นหลัง
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        comment_entry = tk.Entry(root,font=("Arial", 20),width=25,bd=0)
        comment_entry.place(x=280, y=115)
        
        def save_comment():
            student_id = student_id_entry2.get()
            comment_text = comment_entry.get()

            if student_id and comment_text:
                conn = sqlite3.connect('student_data.db')
                cursor = conn.cursor()

                cursor.execute("SELECT students.full_name, club_members.Affective_score FROM students "
                            "INNER JOIN club_members ON students.student_id = club_members.student_id "
                            "WHERE students.student_id=?", (student_id,))
                student_data = cursor.fetchone()

                if student_data:
                    student_name, affective_score = student_data

                    # ดึง round_number ล่าสุดจากตาราง comments สำหรับนักเรียนนี้
                    cursor.execute("SELECT MAX(round_number) FROM comments WHERE student_id=?", (student_id,))
                    last_round = cursor.fetchone()[0]

                    # หากไม่มี round_number ที่มากกว่า 0 (คือไม่มีหมายเเต่ในรอบที่เพิ่มมาก่อน)
                    if last_round is None:
                        round_number = 1
                    else:
                        round_number = last_round + 1

                    # เพิ่มรายการหมายเเต่ใหม่ลงในตาราง comments
                    cursor.execute("INSERT INTO comments (student_id, round_number, full_name, Affective_score, comment) "
                                "VALUES (?, ?, ?, ?, ?)", (student_id, round_number, student_name, affective_score, comment_text))

                    conn.commit()
                    messagebox.showinfo("สำเร็จ", "บันทึกหมายเหตุเรียบร้อยแล้ว!\n"
                                        f"ชื่อ: {student_name}\n"
                                        f"คะแนนจิตพิสัย: {affective_score}\n"
                                        f"หมายเหตุ: {comment_text}")
                    root.destroy()
                else:
                    messagebox.showerror("ข้อผิดพลาด", "ไม่พบนักเรียนด้วยรหัสนักเรียนนี้!")
                conn.close()
            else:
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")
        savebutton=ImageTk.PhotoImage(Image.open("savecom.png"))
        save_button = tk.Button(root,image=savebutton,bg="#FFFFFF",bd=0, width=100, height=40, command=save_comment)#command=back)
        save_button.place(x=300, y=230)
        # เริ่มหน้าต่าง Tkinter
        root.mainloop()
    def add_affective_score():
        student_id = student_id_entry2.get()
        affective_score = affective_score_entry.get()
        if student_id and affective_score:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT full_name FROM students WHERE students.student_id=?", (student_id,))
            student_name = cursor.fetchone()

            cursor.execute("SELECT club_members.Affective_score FROM club_members WHERE club_members.student_id=?", (student_id,))
            current_score = cursor.fetchone()

            if student_name and current_score:
                current_score = current_score[0]

                # คำนวณคะแนนใหม่
                new_score = current_score + int(affective_score)

                if new_score >100:
                    messagebox.showerror("ข้อผิดพลาด", f"คะแนนจิตพิสัยเต็มแล้ว (100)!\n"f"ชื่อ: {student_name[0]}\n"f"คะแนนปัจจุบัน:100")
                else:
                    cursor.execute("UPDATE club_members SET Affective_score = ? WHERE student_id=?", (new_score, student_id))
                    conn.commit()
                    messagebox.showinfo("สำเร็จ", "เพิ่มคะแนนจิตพิสัยเรียบร้อยแล้ว!\n"f"ชื่อ: {student_name[0]}\n"f"คะแนนปัจจุบัน: {new_score}")
                    comment()
                conn.close()
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบนักเรียนด้วยรหัสนักเรียนนี้!")

        else:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")

    def remove_affective_score():
        student_id = student_id_entry2.get()
        affective_score = affective_score_entry.get()

        if student_id and affective_score:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT full_name FROM students WHERE students.student_id=?", (student_id,))
            student_name = cursor.fetchone()

            cursor.execute("SELECT club_members.Affective_score FROM club_members WHERE club_members.student_id=?", (student_id,))
            current_score = cursor.fetchone()

            if student_name and current_score:
                current_score = current_score[0]

                new_score = current_score - int(affective_score)

                cursor.execute("UPDATE club_members SET Affective_score = Affective_score - ? "
                            "WHERE student_id=?", (affective_score, student_id))
                conn.commit()
                messagebox.showinfo("สำเร็จ", "ลบคะแนนจิตพิสัยเรียบร้อยแล้ว!\n"f"ชื่อ: {student_name[0]}\n"f"คะแนนปัจจุบัน: {new_score}")
                conn.close()
                comment()
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบนักเรียนด้วยรหัสนักเรียนนี้!")

        else:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")

    # สร้างหน้าต่าง Tkinter
    root = tk.Tk()
    root.title("โปรแกรมเพิ่มและลบคะแนนจิตพิสัย")
    root.geometry("700x450")
    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\scoremain.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # เพิ่ม entry และปุ่มเพิ่ม/ลบคะแนนจิตพิสัย
    def two5():
        root.destroy()
        mainscore()
    student_id_entry2 = tk.Entry(root,font=("Arial", 22),bd=0)
    student_id_entry2.pack()
    student_id_entry2.place(x=410,y=85,width=200)

    affective_score_entry = tk.Entry(root,font=("Arial", 22),bd=0)
    affective_score_entry.pack()
    affective_score_entry.place(x=490,y=180,width=40)

    addbutton=ImageTk.PhotoImage(Image.open("add.png"))
    add_button = tk.Button(root,image=addbutton,bd=0,bg="#FFFFFF", width=120, height=40,command=add_affective_score)
    add_button.place(x=345, y=263)
    removebutton=ImageTk.PhotoImage(Image.open("del.png"))
    remove_button = tk.Button(root,image=removebutton,bg="#FFFFFF",bd=0, width=100, height=40,command=remove_affective_score)
    remove_button.place(x=540, y=263)

    backbutton=ImageTk.PhotoImage(Image.open("back.png"))
    back_button = tk.Button(root,image=backbutton,bg="#FFFFFF",bd=0, width=100, height=25,command=two5)
    back_button.place(x=35, y=390)

    # เริ่มหน้าต่าง Tkinter
    root.mainloop()
def infoscore():
    # สร้างหน้าต่าง Tkinter
    root = tk.Tk()
    root.title("คะแนนจิตพิสัยนักเรียน")
    root.geometry("1200x750")
    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\scoreinfo.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # สร้างวิดเจ็ต Entry สำหรับกรอกรหัสนักเรียน
    student_id_entry = tk.Entry(root, font=("Arial", 20), width=17, bd=0)
    student_id_entry.place(x=640, y=180)

    # สร้างวิดเจ็ต Treeview เพื่อแสดงหมายเหตุ
    columns = ("ชื่อนักเรียน", "คะแนนจิตพิสัย", "หมายเหตุ")
    treeview = ttk.Treeview(root, columns=columns, show="headings")
    treeview.heading("ชื่อนักเรียน", text="ชื่อนักเรียน")
    treeview.heading("คะแนนจิตพิสัย", text="คะแนนจิตพิสัย")
    treeview.heading("หมายเหตุ", text="หมายเหตุ")
    treeview.place(x=300, y=300)

    # ฟังก์ชันเพื่อค้นหานักเรียนและแสดงหมายเหตุของพวกเขา
    def search_student():
        student_id = student_id_entry.get()
        
        if student_id:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT students.full_name, club_members.Affective_score FROM students "
                        "INNER JOIN club_members ON students.student_id = club_members.student_id "
                        "WHERE students.student_id=?", (student_id,))
            student_data = cursor.fetchone()

            if student_data:
                student_name, affective_score = student_data
                cursor.execute("SELECT full_name, Affective_score, comment FROM comments "
                            "WHERE student_id=?", (student_id,))
                comments = cursor.fetchall()

                # Clear existing Treeview data
                for item in treeview.get_children():
                    treeview.delete(item)

                # Populate Treeview with comments
                for comment in comments:
                    treeview.insert("", "end", values=comment)
            else:
                treeview.delete(*treeview.get_children())  # Clear Treeview
                tk.messagebox.showerror("ข้อผิดพลาด", "ไม่พบนักเรียน!")
        conn.close()
    def two4():
        root.destroy()
        mainscore()
    # สร้างปุ่มเพื่อค้นหานักเรียน
    searchbutton=ImageTk.PhotoImage(Image.open("ok.png"))
    search_button = tk.Button(root,image=searchbutton,bg="#FFFFFF",bd=0, width=70, height=20, command=search_student)
    search_button.place(x=560, y=257)

    backbutton = ImageTk.PhotoImage(Image.open("backbig.png"))
    back_button = tk.Button(root, image=backbutton, bg="#FFFFFF", width=170, height=36, bd=0,command=two4)
    back_button.place(x=40, y=605)
    root.mainloop()
def mainscore():
    def show_selected_students():
        selected_club = selected_club_var.get()
        if selected_club:
            
            # สร้างตารางแสดงรายชื่อนักเรียน
            student_tree = ttk.Treeview(columns=("Student ID", "Full Name", "Student Number", "Student Class", "Affectivescore"), show="headings")

            # สร้างคอลัมน์แสดงคะแนนจิตพิสัย
            student_tree.heading("Affectivescore", text="คะแนนจิตพิสัย")

            # สร้างตารางแสดงรายชื่อนักเรียน
            student_tree.heading("Student ID", text="รหัสประจำตัวนักเรียน")
            student_tree.heading("Full Name", text="ชื่อ - นามสกุล")
            student_tree.heading("Student Number", text="เลขที่")
            student_tree.heading("Student Class", text="ชั้น")

            student_tree.column("Affectivescore", width=100)
            student_tree.column("Student ID", width=120)
            student_tree.column("Full Name", width=180)
            student_tree.column("Student Number", width=50)
            student_tree.column("Student Class", width=50)
            student_tree.pack()
            student_tree.place(x=420, y=175)
            #ตารางโชว์
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()
            student_tree.configure(style="Custom.Treeview")
            custom_style = ttk.Style()
            custom_style.configure("Custom.Treeview.heading", font=("DB HELVETHAICA X BD EXT", 18))
            custom_style.configure("Custom.Treeview", font=("DB HELVETHAICA X BD EXT", 12), rowheight=45)
            

            # ดึงข้อมูลนักเรียนในชุมนุม
            cursor.execute("SELECT students.student_id, full_name, student_number, student_class, Affective_score FROM students LEFT JOIN club_members ON students.student_id = club_members.student_id WHERE club_id=?", (selected_club,))
            selected_students = cursor.fetchall()
            conn.close()
            
    # ฟังก์ชันสำหรับรีเฟรชหน้าตารางแสดงรายชื่อนักเรียน
            def refresh_student_table():
                selected_club = selected_club_var.get()
                if selected_club:
                    student_tree.delete(*student_tree.get_children())  # ลบรายชื่อนักเรียนทั้งหมดในตาราง
                    conn = sqlite3.connect('student_data.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT students.student_id, full_name, student_number, student_class, Affective_score FROM students LEFT JOIN club_members ON students.student_id = club_members.student_id WHERE club_id=?", (selected_club,))
                    # ดึงข้อมูลทั้งหมดที่ตรงกับเงื่อนไขหรือคำสั่ง
                    selected_students = cursor.fetchall()
                    conn.close()

                    # เติมข้อมูลลงในตารางใหม่
                    for student in selected_students:
                        student_tree.insert("", "end", values=student)

            # เพิ่มปุ่ม Refresh
            refresh_button = tk.Button(root,text="รีเฟรชข้อมูล",font=("Helvetica", 19),bd=0,bg="#FFFFFF",command=refresh_student_table)
            refresh_button.place(x=615, y=113)

    # สร้างหน้าต่างหลัก
    root = tk.Tk()
    root.title("โปรแกรมเลือกชุมนุมสำหรับนักเรียนมัธยม")
    root.geometry("1200x750")

    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\active.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # สร้างฐานข้อมูล SQLite
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    # สร้างตาราง club_members ถ้ายังไม่มี
    cursor.execute('''CREATE TABLE IF NOT EXISTS club_members (student_id TEXT,club_id INTEGER,PRIMARY KEY (student_id, club_id))''')

    # สร้างตาราง clubs ถ้ายังไม่มี
    cursor.execute('''CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER PRIMARY KEY,club_name TEXT)''')

    conn.close()

    # สร้างรายชื่อชุมนุมใน Dropdown
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clubs")
    clubs = cursor.fetchall()
    conn.close()

    club_names = [club[1] for club in clubs]
    selected_club_var = tk.StringVar()

    if club_names:
        selected_club_var.set(club_names[0])
    else:
        selected_club_var.set("ไม่มีชุมนุม")

    club_dropdown = None

    if club_names:
        club_dropdown = tk.OptionMenu(root, selected_club_var, *club_names)
        club_dropdown.pack()
        club_dropdown.place(x=40,y=180)
        club_dropdown.config(font=("Arial", 17),bg="#FFFFFF",bd=0)
    else:
        label_no_clubs = tk.Label(root, text="ไม่มีชุมนุมในฐานข้อมูล")
        label_no_clubs.pack()
    def plusdelscore1():
        root.destroy()
        plusdelscore()
    # นำเข้าข้อมูลเริ่มต้นเมื่อโปรแกรมเริ่ม
    show_selected_students()
    def infoscore1():
        root.destroy()
        infoscore()
    def back():
        root.destroy()
        two()
    scorebutton = ImageTk.PhotoImage(Image.open("scorebut.png"))
    score_student_button = tk.Button(root, image=scorebutton, bg="#FFFFFF", width=160, height=45, bd=0,command=plusdelscore1)
    score_student_button.place(x=590, y=665)

    infobutton = ImageTk.PhotoImage(Image.open("info.png"))
    info_student_button = tk.Button(root, image=infobutton, bg="#FFFFFF", width=220, height=50, bd=0,command=infoscore1)
    info_student_button.place(x=990, y=5)

    backbutton = ImageTk.PhotoImage(Image.open("backbig.png"))
    back_button = tk.Button(root, image=backbutton, bg="#FFFFFF", width=170, height=36, bd=0,command=back)
    back_button.place(x=30, y=670)

    root.mainloop()
def selec1():
    # def thre():
    #     three()
    # ฟังก์ชันแสดงรายชื่อนักเรียนในชุมนุม
    def show_selected_students():
        selected_club = selected_club_var.get()
        if selected_club:
            
            # สร้างตารางแสดงรายชื่อนักเรียน
            student_tree = ttk.Treeview(columns=("Student ID", "Full Name", "Student Number", "Student Class", "Affectivescore"), show="headings")

            # สร้างคอลัมน์แสดงคะแนนจิตพิสัย
            student_tree.heading("Affectivescore", text="คะแนนจิตพิสัย")

            # สร้างตารางแสดงรายชื่อนักเรียน
            student_tree.heading("Student ID", text="รหัสประจำตัวนักเรียน")
            student_tree.heading("Full Name", text="ชื่อ - นามสกุล")
            student_tree.heading("Student Number", text="เลขที่")
            student_tree.heading("Student Class", text="ชั้น")

            student_tree.column("Affectivescore", width=100)
            student_tree.column("Student ID", width=120)
            student_tree.column("Full Name", width=180)
            student_tree.column("Student Number", width=50)
            student_tree.column("Student Class", width=50)
            student_tree.pack()
            student_tree.place(x=340, y=175)
            #ตารางโชว์
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()
            student_tree.configure(style="Custom.Treeview")
            custom_style = ttk.Style()
            custom_style.configure("Custom.Treeview.heading", font=("DB HELVETHAICA X BD EXT", 18))
            custom_style.configure("Custom.Treeview", font=("DB HELVETHAICA X BD EXT", 12), rowheight=40)

            # ดึงข้อมูลนักเรียนในชุมนุม
            cursor.execute("SELECT students.student_id, full_name, student_number, student_class, Affective_score FROM students LEFT JOIN club_members ON students.student_id = club_members.student_id WHERE club_id=?", (selected_club,))
            selected_students = cursor.fetchall()
            conn.close()
            
    # ฟังก์ชันสำหรับรีเฟรชหน้าตารางแสดงรายชื่อนักเรียน
            def refresh_student_table():
                selected_club = selected_club_var.get()
                if selected_club:
                    student_tree.delete(*student_tree.get_children())  # ลบรายชื่อนักเรียนทั้งหมดในตาราง
                    conn = sqlite3.connect('student_data.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT students.student_id, full_name, student_number, student_class, Affective_score FROM students LEFT JOIN club_members ON students.student_id = club_members.student_id WHERE club_id=?", (selected_club,))
                    # ดึงข้อมูลทั้งหมดที่ตรงกับเงื่อนไขหรือคำสั่ง
                    selected_students = cursor.fetchall()
                    conn.close()

                    # เติมข้อมูลลงในตารางใหม่
                    for student in selected_students:
                        student_tree.insert("", "end", values=student)

            # เพิ่มปุ่ม Refresh
            refresh_button = tk.Button(root,text="รีเฟรชข้อมูล",font=("Helvetica", 19),bd=0,bg="#FFFFFF",command=refresh_student_table)
            refresh_button.place(x=530, y=610)
    # ฟังก์ชันเพิ่มนักเรียนลงในชุมนุม
    def add_student_to_club():
        student_id = student_id_entry1.get()
        club_id = selected_club_var.get()
        Affective_score = 100  # ปรับคะแนนจิตพิสัยตามที่คุณต้องการ

        if student_id and club_id:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT student_id FROM students WHERE student_id=?", (student_id,))
            student_data = cursor.fetchone()

            if student_data:
                cursor.execute("SELECT club_id FROM club_members WHERE student_id=?", (student_id,))
                existing_clubs = cursor.fetchall()

                if existing_clubs:
                    for existing_club in existing_clubs:
                        if existing_club[0] == club_id:
                            messagebox.showerror("ข้อผิดพลาด", "ท่านได้ลงทะเบียนชุมนุมนี้แล้ว!")
                            conn.close()
                            return
                        else:
                            messagebox.showerror("ข้อผิดพลาด", "ท่านได้ลงทะเบียนชุมนุมอื่นแล้ว กรุณาตรวจสอบอีกครั้ง!")
                            conn.close()
                            return

                cursor.execute("INSERT INTO club_members (student_id, club_id, Affective_score) VALUES (?, ?, ?)",
                            (student_id, club_id, Affective_score))
                conn.commit()
                student_id_entry1.delete(0, tk.END)
                messagebox.showinfo("สำเร็จ", "เพิ่มนักเรียนลงในชุมนุมเรียบร้อยแล้ว!")
            else:
                messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลนักเรียน")
            conn.close()
        else:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")
    # ฟังก์ชันแก้ไขการเลือกชุมนุมของนักเรียน
    def edit_student_club():
        student_id = student_id_entry1.get()
        selected_club = selected_club_var.get()

        if student_id and selected_club:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE club_members SET club_id=? WHERE student_id=?", (selected_club, student_id))
            conn.commit()

            conn.close()
            messagebox.showinfo("สำเร็จ", "แก้ไขการเลือกชุมนุมของนักเรียนเรียบร้อยแล้ว!")
        else:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")

    # ฟังก์ชันยกเลิกการเลือกชุมนุมของนักเรียน
    def cancel_student_club():
        student_id = student_id_entry1.get()
        if student_id:
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM club_members WHERE student_id=?", (student_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("สำเร็จ", "ยกเลิกการเลือกชุมนุมของนักเรียนเรียบร้อยแล้ว!")
            student_id_entry1.delete(0, tk.END)
        else:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกข้อมูลให้ครบถ้วน!")
    # ฟังก์ชันตรวจสอบว่ารหัสประจำตัวนักเรียนซ้ำในฐานข้อมูลหรือไม่
        
    def is_student_id_exists(student_id):
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            cursor.execute("SELECT student_id FROM students WHERE student_id=?", (student_id,))
            #ใช้ในการดึงข้อมูลที่ตรงกับเงื่อนไขจากคำสั่ง
            existing_id = cursor.fetchone()
            conn.close()
            return existing_id is not None
    # สร้างหน้าต่างหลัก
    root = tk.Tk()
    root.title("โปรแกรมเลือกชุมนุม")
    root.geometry("1200x750")

    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\select2.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # สร้างฐานข้อมูล SQLite
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()

    # สร้างตาราง club_members ถ้ายังไม่มี
    cursor.execute('''CREATE TABLE IF NOT EXISTS club_members (student_id TEXT,club_id INTEGER,PRIMARY KEY (student_id, club_id))''')

    # สร้างตาราง clubs ถ้ายังไม่มี
    cursor.execute('''CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER PRIMARY KEY,club_name TEXT)''')

    conn.close()

    # สร้างรายชื่อชุมนุมใน Dropdown
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clubs")
    clubs = cursor.fetchall()
    conn.close()

    club_names = [club[1] for club in clubs]
    selected_club_var = tk.StringVar()

    if club_names:
        selected_club_var.set(club_names[0])
    else:
        selected_club_var.set("ไม่มีชุมนุม")

    club_dropdown = None

    if club_names:
        club_dropdown = tk.OptionMenu(root, selected_club_var, *club_names)
        club_dropdown.pack()
        club_dropdown.place(x=950,y=170)
        club_dropdown.config(font=("Arial", 17),bg="#FFFFFF",bd=0)
    else:
        label_no_clubs = tk.Label(root, text="ไม่มีชุมนุมในฐานข้อมูล")
        label_no_clubs.pack()
    def two3():
        root.destroy()
        two()
    # สร้าง Entry และปุ่มสำหรับการเพิ่มนักเรียน
    student_id_entry1 = tk.Entry(root, font=("Arial", 16), width=12,bd=0)
    student_id_entry1.place(x=975, y=340)

    addbutton = ImageTk.PhotoImage(Image.open("addbutton.png"))
    add_student_button = tk.Button(root, image=addbutton, bg="#FFFFFF", width=182, height=45, bd=0, command=add_student_to_club)
    add_student_button.place(x=955, y=405)

    editbutton = ImageTk.PhotoImage(Image.open("editbutton.png"))
    edit_button = tk.Button(root, image=editbutton, bg="#FFFFFF", width=190, height=35, bd=0, command=edit_student_club)
    edit_button.place(x=950, y=490)

    cancelbutton = ImageTk.PhotoImage(Image.open("cancelbutton.png"))
    cancel_button = tk.Button(root, image=cancelbutton, bg="#FFFFFF", width=191, height=39, bd=0, command=cancel_student_club)
    cancel_button.place(x=948, y=570)

    backbutton = ImageTk.PhotoImage(Image.open("backbig.png"))
    back_button = tk.Button(root, image=backbutton, bg="#FFFFFF", width=170, height=36, bd=0,command=two3)
    back_button.place(x=50, y=610)

    # นำเข้าข้อมูลเริ่มต้นเมื่อโปรแกรมเริ่ม
    show_selected_students()

    root.mainloop()
def edit1():
        def two1():
            root.destroy()
            two()
        def search_student():
            student_id = numentry.get()

            # เชื่อมต่อกับฐานข้อมูล
            conn = sqlite3.connect('student_data.db')
            cursor = conn.cursor()

            # ค้นหานักเรียนโดยใช้รหัสนักเรียน
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            student = cursor.fetchone()

            if student:
                root.destroy()
                show_student_info(student)
            else:
                messagebox.showerror('ข้อผิดพลาด', 'ไม่พบนักเรียนรหัสนี้ในระบบ')

            # ปิดการเชื่อมต่อกับฐานข้อมูล
            conn.close()

        # ฟังก์ชันแสดงข้อมูลนักเรียนในหน้าใหม่
        def show_student_info(student):
            def two2():
                student_root.destroy()
                two()
            # สร้างหน้าต่างใหม่
            student_root = tk.Tk()
            student_root.title('ข้อมูลนักเรียน')
            student_root.geometry("1200x750")
            # นำเข้าภาพพื้นหลัง
            background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\edit.png")
            background_photo = ImageTk.PhotoImage(background_image)
            # สร้าง Label สำหรับภาพพื้นหลัง
            background_label = tk.Label(image=background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # สร้างและแสดงข้อมูลนักเรียนในหน้าใหม่
            student_id_entry = tk.Entry(student_root,font=("Arial", 25),width=18,bd=0)
            student_id_entry.place(x=600,y=190)
            student_id_entry.insert(0, student[0])  # แสดงข้อมูลรหัสนักเรียนใน Entry
            
            name_entry = tk.Entry(student_root,font=("Arial", 25),width=18,bd=0)
            name_entry.place(x=600,y=300)
            name_entry.insert(0, student[1])  # แสดงข้อมูลชื่อนักเรียนใน Entry
            
            number_entry = tk.Entry(student_root,font=("Arial", 25),width=18,bd=0)
            number_entry.place(x=600,y=410)
            number_entry.insert(0, student[2])  # แสดงข้อมูลเลขที่ใน Entry

            class_entry = tk.Entry(student_root,font=("Arial", 25),width=18,bd=0)
            class_entry.place(x=600,y=520)
            class_entry.insert(0, student[3])  # แสดงข้อมูลชั้นใน Entry
            
            # เมื่อคลิกปุ่ม "บันทึกการแก้ไข"
            def save_edit():
                new_student_id = student_id_entry.get()
                new_name = name_entry.get()
                new_class = class_entry.get()
                new_number = number_entry.get()
                
                if new_student_id and new_name and new_class and new_number:
                    # เชื่อมต่อกับฐานข้อมูล
                    conn = sqlite3.connect('student_data.db')
                    cursor = conn.cursor()
                    # ตรวจสอบว่ารหัสประจำตัวใหม่ไม่ซ้ำกับรหัสประจำตัวของนักเรียนอื่นๆ
                    cursor.execute('SELECT * FROM students WHERE student_id = ? AND student_id != ?', (new_student_id, student[0]))
                    duplicate_student = cursor.fetchone()
                    if duplicate_student:
                        messagebox.showerror('ข้อผิดพลาด', 'รหัสประจำตัวนักเรียนซ้ำกับคนอื่นในระบบ')
                    else:
                        # อัปเดตข้อมูลนักเรียนในฐานข้อมูล
                        cursor.execute('UPDATE students SET student_id = ?, full_name = ?, student_class = ?, student_number = ? WHERE student_id = ?', (new_student_id, new_name, new_class, new_number, student[0]))
                        conn.commit()
                        conn.close()
                        # แสดงข้อความยืนยันการแก้ไข
                        messagebox.showinfo('สำเร็จ', 'แก้ไขข้อมูลเรียบร้อย')
                        # ปิดหน้าต่างนี้
                        
            # สร้างปุ่ม "บันทึกการแก้ไข"
            save_button = tk.Button(student_root,font=("Arial", 20),bg="#FFFFFF",text='แก้ไขข้อมูล', width=8, height=1,bd=0, command=save_edit)
            save_button.place(x=695,y=615)

            back_button = tk.Button(student_root,font=("Arial", 20),bg="#FFFFFF",text='BACK', width=8, height=1,bd=0,command=two2)
            back_button.place(x=70,y=595)
            root.mainloop()
            
        # สร้างหน้าต่าง GUI
        root = tk.Tk()
        root.title('โปรแกรมแก้ไขข้อมูลนักเรียน')
        root.geometry("700x450")

        # นำเข้าภาพพื้นหลัง
        background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\editnum.png")
        background_photo = ImageTk.PhotoImage(background_image)

        # สร้าง Label สำหรับภาพพื้นหลัง
        background_label = tk.Label(root, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # สร้างช่องป้อนข้อมูลรหัสนักเรียน
        numentry = tk.Entry(root, font=("Arial", 25),width=15,bd=0)
        numentry.place(x=360, y=115)

        # สร้างปุ่ม "ค้นหา"
        search_studentbutton = ImageTk.PhotoImage(Image.open("search.png"))
        search_button = tk.Button(root, image=search_studentbutton, bd=0, bg="#FFFFFF", width=150, height=35, command=search_student)
        search_button.place(x=275, y=233)

        backbutton=ImageTk.PhotoImage(Image.open("back.png"))
        back_button = tk.Button(root,image=backbutton,bg="#FFFFFF",bd=0, width=100, height=25,command=two1)
        back_button.place(x=35, y=390)

        # เริ่มการทำงานของโปรแกรม
        root.mainloop()
def add1():
    def two1():
        root.destroy()
        two()
    def is_student_id_exists(student_id):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT student_id FROM students WHERE student_id=?", (student_id,))
        existing_id = cursor.fetchone()
        conn.close()
        return existing_id is not None

    def upload_image():
        student_id = student_id_entry.get()
        full_name = full_name_entry.get()  # ดึงข้อมูลจากช่องกรอก full_name
        if not student_id.isdigit() or not full_name:
            messagebox.showerror("ข้อมูลไม่ครบหรือไม่ถูกต้อง", "กรุณากรอกข้อมูลเป็นตัวเลขในช่อง รหัสประจำตัวนักเรียนและชื่อเต็มให้ถูกต้อง")
            return

        if is_student_id_exists(student_id):
            messagebox.showerror("ข้อมูลซ้ำ", "รหัสประจำตัวนักเรียนมีอยู่ในฐานข้อมูลแล้ว คุณไม่สามารถอัปโหลดรูปได้")
            display_profile_image(student_id)
            return
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as image_file:
                image_blob = image_file.read()
            student_id = student_id_entry.get()
            full_name = full_name_entry.get()
            if not is_student_id_exists(student_id):
                conn = sqlite3.connect('student_data.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (student_id, full_name, student_number, student_class, profile_image) VALUES (?, ?, ?, ?, ?)",
                            (student_id, full_name, student_number_entry.get(), student_class_entry.get(), image_blob))
                conn.commit()
                conn.close()
                messagebox.showinfo("ยืนยันการบันทึก", "บันทึกข้อมูลเรียบร้อยแล้ว!")
                display_profile_image(student_id)
            else:
                messagebox.showerror("ข้อมูลซ้ำ", "รหัสประจำตัวนักเรียนซ้ำกันในฐานข้อมูล!")

            # เพิ่มโค้ดสำหรับแสดงรูปภาพที่อัพโหลด
            display_profile_image(student_id)

    def display_profile_image(student_id):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT profile_image FROM students WHERE student_id=?", (student_id,))
        profile_image_blob = cursor.fetchone()
        conn.close()
        if profile_image_blob:
            profile_image_data = profile_image_blob[0]
            profile_image = Image.open(io.BytesIO(profile_image_data))
            profile_image = profile_image.resize((300, 300), Image.LANCZOS)  # Resize the image
            profile_image = ImageTk.PhotoImage(profile_image)
            profile_image_label.config(image=profile_image)
            profile_image_label.image = profile_image
        else:
            profile_image_label.config(image=None)

    root = tk.Tk() 
    root.title("โปรแกรมเลือกชุมนุมสำหรับนักเรียนมัธยม")
    root.geometry("1200x750")

    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\select1.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    student_id_entry = tk.Entry(root, font=("Arial", 25),width=15,bd=0)
    student_id_entry.place(x=780, y=190)

    full_name_entry = tk.Entry(root, font=("Arial", 25),width=15,bd=0)
    full_name_entry.place(x=780, y=300)

    student_number_entry = tk.Entry(root, font=("Arial", 25),width=15,bd=0)
    student_number_entry.place(x=780, y=410)

    student_class_entry = tk.Entry(root, font=("Arial", 25),width=15,bd=0)
    student_class_entry.place(x=780, y=520)

    savebutton = ImageTk.PhotoImage(Image.open("savebutton.png"))
    save_button = tk.Button(root, image=savebutton, bd=0, bg="#FFFFFF", width=170, height=37, command=upload_image)
    save_button.place(x=830, y=606)

    backbutton = ImageTk.PhotoImage(Image.open("backbig.png"))
    back_button = tk.Button(root, image=backbutton, bg="#FFFFFF", width=170, height=36, bd=0,command=two1)
    back_button.place(x=40, y=605)

    profile_image_label = tk.Label(root)
    profile_image_label.place(x=28, y=225)

    root.mainloop()
def pdf():
    def back():
        root.destroy()

    def get_club_name(club_id):
        conn = sqlite3.connect(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\student_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT club_name FROM clubs WHERE club_id=?", (club_id,))
        club_name = cursor.fetchone()
        conn.close()
        return club_name[0] if club_name else ""

    def pdf(selected_club):
        # เพิ่มเส้นทางของฟอนต์ 'THSarabun' ที่คุณดาวน์โหลดมา
        fonts_path = r"C:\Users\โฟกัส\Documents\PROJECT\Project4\THSarabun.ttf"
        font_name = 'THSarabun'
        # ลงทะเบียนฟอนต์ 'THSarabun' ให้ใช้ในระบบของ ReportLab
        pdfmetrics.registerFont(TTFont(font_name, fonts_path))
        pdfmetrics.registerFont(TTFont('THSarabun', fonts_path))  # ลงทะเบียนฟอนต์ตัวหนา (ถ้ามี)

        # ตั้งค่าไฟล์ PDF
        pdf_file = f"{selected_club}.pdf"  # ใช้ชื่อชุมนุมในชื่อไฟล์ PDF
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        # สร้างเทเบิลสไตล์
        styles = getSampleStyleSheet()
        style_table = styles["Normal"]
        style_table.fontName = font_name
        style_table.fontSize = 12
        style_table.leading = 14

        # สร้างสไตล์ของข้อความ "รายชื่อนักเรียนทั้งหมด"
        title_style = ParagraphStyle(name='TitleStyle', fontName=font_name, fontSize=16, alignment=1)

        # เชื่อมต่อกับฐานข้อมูล SQLite3
        conn = sqlite3.connect(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\student_data.db")
        cursor = conn.cursor()

        # อ่านข้อมูลจากตาราง students
        cursor.execute("SELECT student_id, full_name, student_number, student_class FROM students")
        student_data = cursor.fetchall()

        # อ่านข้อมูลจากตาราง club_members โดยคัดเลือกตามชุมนุมที่เลือก
        cursor.execute("SELECT students.student_id, students.full_name, students.student_number, students.student_class, club_members.club_id, club_members.Affective_score FROM students INNER JOIN club_members ON students.student_id = club_members.student_id WHERE club_members.club_id=?", (selected_club,))
        club_data = cursor.fetchall()

        # สร้างโครงสร้างข้อมูลสำหรับ PDF
        table_data = [["รหัสนักเรียน", "ชื่อนักเรียน", "เลขที่", "ชั้น", "ชื่อชุมนุม", "คะแนนจิตพิสัย"]]  # เพิ่มหัวข้อคอลัมน์

        # สร้างตารางข้อมูลใน PDF
        for student_row in student_data:
            student_id, full_name, student_number, student_class = student_row
            club_info = [(club_row[4], club_row[0], club_row[5]) for club_row in club_data if club_row[0] == student_id]

            # จัดการกรณีที่นักเรียนอาจมีการเป็นสมาชิกของชุมนุมหลายอัน
            for club_row in club_info:
                club_id, student_id, Affective_score = club_row
                # สร้างข้อมูลที่ครบถ้วนสำหรับคอลัมน์ในตาราง PDF
                table_row = [student_id, full_name, student_number, student_class, club_id, Affective_score]
                table_data.append(table_row)

        # ปรับขนาดคอลัมน์ตามจำนวนคอลัมน์ในข้อมูล (7 คอลัมน์)
        col_widths = [100] * 6
        table = Table(table_data, colWidths=col_widths)

        # สร้างตาราง
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'THSarabun'),  # ใช้ตัวหนาสำหรับหัวข้อ
            ('FONTNAME', (0, 1), (-1, -1), font_name),  # ใช้ฟอนต์ปกติสำหรับเนื้อหา
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # สร้างไฟล์ PDF และเพิ่มตารางและข้อความ
        doc.build([table])

        # ปิดการเชื่อมต่อกับฐานข้อมูล
        conn.close()

    def create_pdf():
        selected_club_value = selected_club.get()  # ใช้ selected_club ที่สร้างขึ้น
        if selected_club_value:
            pdf(selected_club_value)
            messagebox.showinfo("สร้าง PDF", "สร้าง PDF เสร็จสิ้น!")
        else:
            messagebox.showwarning("เลือกชุมนุม", "โปรดเลือกชุมนุมก่อนสร้าง PDF")
    # สร้างหน้าต่าง tkinter
    root = tk.Toplevel()
    root.title("สร้าง PDF รายชื่อนักเรียน")
    root.geometry("700x450")
    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\pdff.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # เพิ่ม Dropdown
    conn = sqlite3.connect(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\student_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT club_id FROM club_members")
    clubs = cursor.fetchall()
    conn.close()

    club_list = [club[0] for club in clubs]
    selected_club = tk.StringVar(root)
    selected_club.set(club_list[0])  # ตั้งค่าเริ่มต้น

    dropdown = tk.OptionMenu(root, selected_club, *club_list)
    dropdown.grid(row=0, column=0, padx=10, pady=10)
    dropdown.config(font=("Arial", 18),bg="#FFFFFF",bd=0)
    dropdown.place(x=120,y=150)

    # เพิ่มปุ่ม "สร้าง PDF"
    pdfbutton=ImageTk.PhotoImage(Image.open("pdf.png"))
    pdf_button = tk.Button(root,image=pdfbutton,bg="#FFFFFF",bd=0, width=140, height=35,command=create_pdf)
    pdf_button.place(x=390, y=155)

    backbutton=ImageTk.PhotoImage(Image.open("backsmall.png"))
    back_button = tk.Button(root,image=backbutton,bg="#FFFFFF",bd=0, width=100, height=30,command=back)
    back_button.place(x=37, y=385)
    root.mainloop()

def pujud():
    about_dialog = tk.Toplevel()
    about_dialog.title("คณะผู้จัดทำ")
    about_dialog.geometry("1200x750")
    image_path = r'C:\Users\โฟกัส\Documents\PROJECT\Project4\puujudtum.png'
    pillow_image = Image.open(image_path)
    global background_image
    background_image = ImageTk.PhotoImage(pillow_image)
    background_label = tk.Label(about_dialog, image=background_image)
    background_label.pack()
    about_dialog.mainloop()
def two():
    root = tk.Tk() 
    root.title("หน้าต่างเมนู")
    root.geometry("1200x750")

    # นำเข้าภาพพื้นหลัง
    background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\main.png")
    background_photo = ImageTk.PhotoImage(background_image)
    # สร้าง Label สำหรับภาพพื้นหลัง
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    def add():
        root.destroy()
        add1()
    def edit():
        root.destroy()
        edit1()
    def selec():
        root.destroy()
        selec1()
    def mainscore1():
        root.destroy()
        mainscore()
    pdfbutton = ImageTk.PhotoImage(Image.open("pdfbutton.png"))
    pdf_button = tk.Button(root, image=pdfbutton,width=300,height=50,bd=0,command=pdf)
    pdf_button.place(x=5, y=5)

    aboutbutton= ImageTk.PhotoImage(Image.open("aboutbutton.png"))
    about_button = tk.Button(root, image=aboutbutton, width=300, height=50,bg="#FFFFFF", bd=0,command=pujud)
    about_button.place(x=950, y=5)

    addbutton = ImageTk.PhotoImage(Image.open("add1button.png"))
    add_button= tk.Button(root, image=addbutton, width=190, height=41,bg="#FFFFFF",bd=0,command=add)
    add_button.place(x=505, y=170)

    editbutton = ImageTk.PhotoImage(Image.open("edit1button.png"))
    edit_button= tk.Button(root, image=editbutton,width=190, height=39,bg="#FFFFFF", bd=0,command=edit)
    edit_button.place(x=505, y=272)

    selectbutton =  ImageTk.PhotoImage(Image.open("selectbutton.png"))
    select_button= tk.Button(root, image=selectbutton, width=185, height=35,bg="#FFFFFF", bd=0,command=selec)
    select_button.place(x=505, y=375)

    scorebutton = ImageTk.PhotoImage(Image.open("scorebutton.png"))
    score_button= tk.Button(root, image=scorebutton, width=180,bg="#FFFFFF", height=40, bd=0,command=mainscore1)
    score_button.place(x=505, y=470)

    root.mainloop()
#หน้า login
def create_table():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)''')
    conn.commit()
    conn.close()

def login():
    username = username_entry.get()
    password = password_entry.get()
    conn = sqlite3.connect('user.db')
    #ช่วยให้สามารถสร้างคำสั่ง SQL เพื่อดึงข้อมูล
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    #คือการดึงข้อมูลทั้งหมดที่ตรงกับเงื่อนไขหรือคำสั่ง
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("เข้าสู่ระบบสำเร็จ", "เข้าสู่ระบบสำเร็จ")
        root.destroy()
        two()
    else:
        messagebox.showerror("เข้าสู่ระบบล้มเหลว", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
create_table()
# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ระบบล็อกอินและลงทะเบียน")
root.geometry("1200x750")  # กำหนดขนาดหน้าต่าง
# นำเข้าภาพพื้นหลัง
background_image = Image.open(r"C:\Users\โฟกัส\Documents\PROJECT\Project4\aa1.png")
background_photo = ImageTk.PhotoImage(background_image)

# สร้าง Label สำหรับภาพพื้นหลัง
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)
# สร้างแท็บล็อกอิน
username_entry = tk.Entry( font=("Helvetica", 19),fg="#FF6600",bd=0)
username_entry.place(x=480,y=315)
password_entry = tk.Entry( show="*", font=("Helvetica", 19),fg="#FF6600",bd=0)  #ซ่อนรหัสผ่าน
password_entry.place(x=480,y=420)

imgbutton= ImageTk.PhotoImage(Image.open("button.png"))
login_button = tk.Button(text="",image=imgbutton,command=login,fg="#FF6600",bd=0)
login_button.place(x=528,y=492)
root.mainloop()
