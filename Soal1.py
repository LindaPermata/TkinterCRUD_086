import sqlite3 #Modul untuk bekerja dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk #Modul untuk membuat GUI

def create_database(): #Fungsi untuk membuat database dan tabel
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuka koneksi ke database / menghubungkan ke database
    cursor = conn.cursor() #  Membuat objek cursor untuk eksekusi SQL
    #membuat tabel nilai mahasiswa
    cursor.execute('''   
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
        )
    ''')
    conn.commit() #menyimpan perubahan
    conn.close() # menutup koneksi ke database

def fetch_data(): # mengambil semua data dari tabel nilai_siswa
    conn = sqlite3.connect('nilai_siswa_.db') # Membuka koneksi ke database / menghubungkan ke database
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi SQL
    cursor.execute('SELECT * FROM nilai_siswa') # mengeksekusi SQL query untuk mengambil semua data dari tabel nilai_siswa
    rows = cursor.fetchall() # menyimpan hasil query ke variabel rows
    conn.close() # menutup koneksi ke database
    return rows # mengembalikan data yang diambil

def save_to_database(nama, biologi, fisika, inggris, prediksi):  # Menyimpan data baru ke tabel nilai_siswa.
    conn = sqlite3.connect('nilai_siswa_.db') # Membuka koneksi ke database / menghubungkan ke database
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi SQL
    # menyisipkan data baru ke tabel nilai_siswa
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit() # menyimpan perubahan ke database
    conn.close() # menutup koneksi ke database
    
def update_database(record_id, nama, biologi, fisika, inggris, prediksi): #Memperbarui data siswa di database 
    conn = sqlite3.connect('nilai_siswa_.db') # Membuka koneksi ke database / menghubungkan ke database
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi SQL
    # Mengupdate data 
    cursor.execute(''' 
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # menyisipkan data baru (update) ke tabel nilai_siswa
    conn.commit() # menyimpan perubahan ke database
    conn.close() # menutup koneksi ke database

def delete_database(record_id): #Menghapus data siswa dari database
    conn = sqlite3.connect('nilai_siswa_.db') # Membuka koneksi ke database / menghubungkan ke database
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi SQL
    # Menghapus data
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) 
    conn.commit() # menyimpan perubahan ke database
    conn.close() # menutup koneksi ke database

def calculate_prediction(biologi, fisika, inggris): #Menghitung prediksi fakultas berdasarkan nilai terbesar.
    if biologi > fisika and biologi > inggris: # Mengecek nilai biologi lebih besar dari nilai fisika dan inggris
        return "Kedokteran" #jika biologi tertinggi maka tampilkan kedokteran
    elif fisika > biologi and fisika > inggris: # Mengecek nilai fisika lebih besar dari nilai biologi dan inggris
        return "Teknik" #jika fisika tertinggi maka tampilkan teknik
    elif inggris > biologi and inggris > fisika: # Mengecek nilai inggris lebih besar dari nilai biologi dan fisika
        return "Bahasa" #jika inggris tertinggi maka tampilkan bahasa
    else:
        return "Tidak diketahui" #jika nilainya sama atau tidak jelas maka tampilkan tidak diketahui

def submit():   # Menyimpan data baru dari input form ke database.
    try: 
        # mengambil input dari pengguna
        nama = nama_var.get() # mengambil input dari pengguna
        biologi = int(biologi_var.get()) # mengambil input nilai biologi dari pengguna
        fisika = int(fisika_var.get()) # mengambil input nilai fisika dari pengguna
        inggris = int(inggris_var.get()) # mengambil input nilai inggris dari pengguna

        if not nama: # Mengecek apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.") #jika kosong maka tampilkan pesan "nama tidak boleh kosong"
        
        prediksi = calculate_prediction(biologi, fisika, inggris) # Menghitung prediksi fakultas berdasarkan nilai biologi, fisika, dan inggris
        save_to_database(nama, biologi, fisika, inggris, prediksi) # Menyimpan data baru ke database
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}") # menampilkan pesan "data berhasil disimpan" dan prediksi fakultas
        clear_inputs() # membersihkan input setelah disimpan
        populate_table() # memperbarui tabel dengan data yang baru

    except ValueError as e: # Memproses kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}") # menampilkan pesan error

def update(): #Memperbarui data siswa di database berdasarkan data input.
    try: 
        # Validasi jika tidak ada data yang dipilih 
        if not selected_record_id.get(): # Mengecek apakah ada data yang dipilih
            raise ValueError("Pilih data dari tabel untuk di-update.") #jika tidak ada data yang dipilih maka tampilkan pesan "Pilih data dari tabel untuk di-update."

        # Ambil input baru
        record_id = int(selected_record_id.get()) # Mengambil id dari data yang dipilih
        nama = nama_var.get() # Mengambil input nama
        biologi = int(biologi_var.get()) # Mengambil input biologi
        fisika = int(fisika_var.get()) # Mengambil input fisika
        inggris = int(inggris_var.get()) # Mengambil input inggris

        if not nama: # Mengecek apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.") #jika kosong maka tampilkan pesan "Nama siswa tidak boleh kosong."
        
        prediksi = calculate_prediction(biologi, fisika, inggris) # Menghitung prediksi nilai ujian berdasarkan input biologi, fisika, dan inggris
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) # Memperbarui data di database
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!") # Menampilkan pesan "Data Berhasil diperbarui!"
        clear_inputs() # Mengosongkan input
        populate_table() # Memperbarui tabel

    except ValueError as e: # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}") # Menampilkan pesan kesalahan

def delete(): #Menghapus data siswa dari database.
    try:
        # Validasi jika tidak ada data yang dipilih
        if not selected_record_id.get(): # Mengecek apakah tidak ada data yang dipilih
            raise ValueError("Pilih data dari tabel untuk dihapus!") # Jika tidak ada data yang dipilih, maka tampilkan pesan "Pilih data dari tabel untuk dihapus!"

        record_id = int(selected_record_id.get())
        delete_database(record_id) # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs(): # Menghapus semua data yang diisi di form.
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

def populate_table(): #Mengisi tabel tampilan dengan data dari database.
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

def fill_inputs_from_table(event): #Mengisi form input berdasarkan data yang dipilih di tabel tampilan.
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError: # Jika tidak ada data yang dipilih, maka tidak akan terjadi apa-apa.
        messagebox.showerror("Error", "Pilih data yang valid")

create_database() # Membuat database jika belum ada.

#membuat gui
root = Tk() # Membuat window utama.
root.title("Prediksi Fakultas Siswa") # Menambahkan judul window.

#variabel input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# label dan entry untuk menginput data
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) # Label untuk menginput nama siswa.
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Entry untuk menginput nama siswa.

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

# konfigurasi kolom tabel
for col in columns:
    tree.heading(col, text=col.capitalize()) #judul kolom
    tree.column(col, anchor='center') # Perataan teks

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # event saat memilih data di tabel

tree.bind('<ButtonRelease-1>', fill_inputs_from_table) # event saat memilih data di tabel

populate_table()  # tampilkan data di tabel

root.mainloop() # menjalankan aplikasi