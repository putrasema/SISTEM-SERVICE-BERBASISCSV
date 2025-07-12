# Sistem Pencatatan Service Hardware dan Software dengan Database Flat File (CSV)

import csv
from datetime import datetime
import os

CSV_FILE = 'service_data.csv'

class ServiceEntry:
    def __init__(self, id, customer_name, device_type, service_type, description, status, timestamp):
        self.id = id
        self.customer_name = customer_name
        self.device_type = device_type
        self.service_type = service_type
        self.description = description
        self.status = status
        self.timestamp = timestamp

    def to_list(self):
        return [self.id, self.customer_name, self.device_type, self.service_type, self.description, self.status, self.timestamp]

    def display(self):
        print(f"ID         : {self.id}")
        print(f"Customer   : {self.customer_name}")
        print(f"Device     : {self.device_type}")
        print(f"Service    : {self.service_type}")
        print(f"Desc       : {self.description}")
        print(f"Status     : {self.status}")
        print(f"Timestamp  : {self.timestamp}\n")


class ServiceSystem:
    def __init__(self):
        self.services = []
        self.load_data()

    def load_data(self):
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        entry = ServiceEntry(*row)
                        self.services.append(entry)

    def save_data(self):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            for service in self.services:
                writer.writerow(service.to_list())

    def add_service(self, customer_name, device_type, service_type, description, status):
        service_id = str(int(datetime.now().timestamp()))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = ServiceEntry(service_id, customer_name, device_type, service_type, description, status, timestamp)
        self.services.append(entry)
        self.save_data()
        print("Service berhasil ditambahkan!\n")

    def list_services(self):
        if not self.services:
            print("Tidak ada data service.\n")
        for entry in self.services:
            entry.display()

    def update_status(self, service_id, new_status):
        for entry in self.services:
            if entry.id == service_id:
                entry.status = new_status
                self.save_data()
                print("Status berhasil diperbarui.\n")
                return
        print("Service ID tidak ditemukan.\n")

    def search_by_customer(self, customer_name):
        found = False
        for entry in self.services:
            if customer_name.lower() in entry.customer_name.lower():
                entry.display()
                found = True
        if not found:
            print("Tidak ada data untuk pelanggan tersebut.\n")


# Contoh Penggunaan
if __name__ == "__main__":
    system = ServiceSystem()

    while True:
        print("\n--- SISTEM SERVICE HARDWARE DAN SOFTWARE ---")
        print("1. Tambah Service")
        print("2. Lihat Semua Service")
        print("3. Update Status Service")
        print("4. Cari Berdasarkan Nama Pelanggan")
        print("5. Keluar")
        
        choice = input("Pilih menu (1-5): ")

        if choice == '1':
            name = input("Nama Pelanggan: ")
            device = input("Tipe Perangkat: ")
            service_type = input("Jenis Servis (Hardware/Software): ")
            desc = input("Deskripsi Kerusakan: ")
            status = input("Status Awal: ")
            system.add_service(name, device, service_type, desc, status)

        elif choice == '2':
            system.list_services()

        elif choice == '3':
            sid = input("Masukkan ID Service: ")
            new_status = input("Masukkan Status Baru: ")
            system.update_status(sid, new_status)

        elif choice == '4':
            cname = input("Masukkan Nama Pelanggan: ")
            system.search_by_customer(cname)

        elif choice == '5':
            print("Keluar dari sistem.")
            break

        else:
            print("Pilihan tidak valid.\n")
