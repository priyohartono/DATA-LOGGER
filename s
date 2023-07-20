string = "Koneksi Berhasil.<h3>Informasi Koneksi</h3>DATABASE: db_awscenter<br>HOST: 172.19.2.215<br>PORT: 5432<br><h3>Cek Status Query</h3>Koneksi berhasi"

# Cut from index 7 to the end of the string
substring = string[0:16]
print(substring) 

if substring == "Koneksi berhasil":
    print("1")
else :
    print("0")
