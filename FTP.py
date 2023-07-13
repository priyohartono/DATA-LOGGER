import ftplib

# Define the FTP server address and credentials
FTP_HOST = "202.90.198.212"
FTP_USER = "arg"
FTP_PASS = "arg"

# Open a connection to the FTP server
ftp = ftplib.FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

# Switch to binary mode for transferring files
ftp.sendcmd("TYPE i")

# Upload the file to the server
with open("example.txt", "rb") as file:
    ftp.storbinary("STOR example.txt", file)

# Close the FTP connection
ftp.quit()