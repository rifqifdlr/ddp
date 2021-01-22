import random, string, re

def menu():
    text = """
    MENU:
    [1] Buka rekening
    [2] Setoran tunai
    [3] Tarik tunai
    [4] Transfer
    [5] Lihat daftar Transfer
    [6] Keluar
    """
    print(text)

    while True:
        try:
            inMenu = int(input("Masukkan menu pilihan Anda: "))
            if inMenu >= 1 and inMenu <=6:
                if inMenu == 1:
                    return buatRekening()
                elif inMenu == 2:
                    return setorTunai()
                elif inMenu == 3:
                    return tarikTunai()
                elif inMenu == 4:
                    return transfer()
                elif inMenu == 5:
                    return daftarTransfer()
                elif inMenu == 6:
                    return print("Terima kasih atas kunjungan anda...")
            else:
                print("Pilihan Anda salah. Ulangi")
        except ValueError:
            print("Pilihan Anda salah. Ulangi")

#Fitur buat rekening
def buatRekening():
    print("*** BUAT REKENING ***")
    nama = input("Masukkan nama: ")
    saldo = input("Masukkan setoran awal: ")
    norek = "REK" + ''.join(random.choice(string.digits) for _ in range(3))

    file = open('nasabah.txt', 'a+')
    file.write(norek+','+nama+','+saldo+'\n')
    file.close()

    print("Pembukaan rekening dengan nomor",norek,"atas nama",nama,"berhasil.")
    return menu()

#Fitur setor tunai
def setorTunai():
    print()
    print("*** SETORAN TUNAI ***")
    norek   = input("Masukkan nomor rekening: ")
    nominal = input("Masukkan nominal yang akan disetor: ")

    check = checkRek(norek)
    if not check:
        print("Nomor rekening tidak terdaftar. Setoran tunai gagal")
    else:
        data    = check.split(',')
        saldo   = int(data[2])+int(nominal)
        new     = str(data[0]+','+data[1]+','+str(saldo)+'\n')

        file = open('nasabah.txt', 'r+')
        text = file.read()
        text = re.sub(check, new, text)
        file.seek(0)
        file.write(text)
        file.close()

        print("Setoran tunai sebesar",str(nominal),"ke rekening",norek," berhasil.")
    return menu()

#Fitur tarik tunai
def tarikTunai():
    print()
    print("*** TARIK TUNAI ***")
    norek   = input("Masukkan nomor rekening: ")
    nominal = input("Masukkan nominal yang akan ditarik: ")

    check = checkRek(norek)
    if not check:
        print("Nomor rekening tidak terdaftar. Setoran tunai gagal")
    else:
        data    = check.split(',')
        if int(nominal) <= int(data[2]):
            saldo   = int(data[2])-int(nominal)
            new     = str(data[0]+','+data[1]   +','+str(saldo)+'\n')

            file = open('nasabah.txt', 'r+')
            text = file.read()
            text = re.sub(check, new, text)
            file.seek(0)
            file.write(text)
            file.close()
            print("Tarik tunai sebesar",str(nominal),"dari rekening",norek," berhasil.")
        else:
            print("saldo tidak mencukupi, penarikan tidak berhasil")
    return menu()

#Fitur Transfer
def transfer():
    print()
    norek_sumber = input("Masukkan nomor rekening sumber: ")
    norek_tujuan = input("Masukkan nomor rekening tujuan: ")
    nominal = input("Masukkan nominal yang akan ditransfer: ")

    check_sumber = checkRek(norek_sumber)
    check_tujuan = checkRek(norek_tujuan)
    if not check_sumber:
        print("Nomor rekening sumber tidak terdaftar. Transfer gagal")
    elif not check_tujuan:
        print("Nomor rekening tujuan tidak terdaftar. Transfer gagal")
    else:
        data_sumber = check_sumber.split(',')
        data_tujuan = check_tujuan.split(',')
        if int(nominal) <= int(data_sumber[2]):
            saldo_sumber    = int(data_sumber[2])-int(nominal)
            new_sumber      = str(data_sumber[0]+','+data_sumber[1] +','+str(saldo_sumber)+"\n")
            saldo_tujuan    = int(data_tujuan[2])+int(nominal)
            new_tujuan      = str(data_tujuan[0]+','+data_tujuan[1]+','+str(saldo_tujuan)+"\n")

            file = open('nasabah.txt', 'r+')
            text = file.read()
            text = re.sub(check_sumber, new_sumber, text)
            text = re.sub(check_tujuan, new_tujuan, text)
            file.seek(0)
            file.write(text)
            file.close()
            notf = "TRF" + ''.join(random.choice(string.digits) for _ in range(3))

            file = open('transfer.txt', 'a+')
            file.write(notf+','+norek_sumber+','+norek_tujuan+','+nominal+'\n')
            file.close()
            print("Transfer sebesar", nominal, "dari rekening", norek_sumber, "ke rekening", norek_tujuan, "berhasil")
        else:
            print("Saldo tidak mencukupi. Transfer gagal")
        return menu()

#Fitur daftar Transfer
def daftarTransfer():
    print("*** LIHAT DATA TRANSFER ***")
    norek = input("Masukkan nomor rekening sumber transfer: ")
    check = checkRek(norek)
    if not check:
        print("Nomor rekening sumber tidak terdaftar.")
    else:
        listTransfer = []
        filetf = open('transfer.txt')
        for value in filetf:
            data = value.split(',')
            if data[1] == norek:
                listTransfer.append(value.replace(',',' '))
            filetf.close()
            if len(listTransfer):
                print("Daftar transfer dari rekening",norek,":")
                print(''.join(map(str, listTransfer)))
            else:
                print('Tidak ada data yang ditampilkan.')
        return menu()

#Untuk cek no rekening tersedia di file nasabah.txt
def checkRek(norek):
    account = ""
    file = open('nasabah.txt')
    for each_line in file:
        data = each_line.split(',')
        if data[0] == norek:
            account = each_line
    file.close()

    return account

print("***** SELAMAT DATANG DI NF BANK *****")
menu()