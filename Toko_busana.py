import mysql.connector
from datetime import datetime
from tabulate import tabulate
from termcolor import colored
from colorama import init
from rich.console import Console
from rich.table import Table
from pyfiglet import figlet_format
import time  # Import time untuk animasi

# Inisialisasi
init(autoreset=True)  # Colorama untuk reset warna
console = Console()  # Rich untuk output yang menarik

# Konfigurasi Database
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'toko_busana'
}

# Koneksi Database
def get_connection():
    return mysql.connector.connect(**config)

# Header menggunakan PyFiglet
def print_header(text):
    header = figlet_format(text, font="slant")
    print(colored(header, "cyan"))

# Fungsi Login
def login():
    console.print("[bold cyan]Silakan masuk ke akun Anda[/bold cyan]")
    username = input(colored("Username: ", "cyan"))
    password = input(colored("Password: ", "cyan"))

    # Simulasi proses login
    console.print("[bold yellow]Memverifikasi informasi login...[/bold yellow]")
    for i in range(3):
        time.sleep(1)  # Delay 1 detik
        console.print(f"[bold yellow]Menghitung... {3 - i}[/bold yellow]")

    
    if username == "admin" and password == "admin":
        console.print("[bold green]Login berhasil! Selamat datang![/bold green]")
    else:
        console.print("[bold red]Login gagal! Silakan coba lagi.[/bold red]")
        return False
    return True

# Fungsi Produk
def manage_products():
    while True:
        print_header("Produk")
        console.print("[bold green]1. Tambah Produk[/bold green]")
        console.print("[bold yellow]2. Lihat Produk[/bold yellow]")
        console.print("[bold blue]3. Tambah Stok[/bold blue]")
        console.print("[bold cyan]4. Perbarui Data Produk[/bold cyan]")  # Opsi baru untuk memperbarui data produk
        console.print("[bold red]5. Hapus Produk[/bold red]")
        console.print("[bold magenta]6. Kembali ke Menu Utama[/bold magenta]")

        choice = input(colored("Pilih opsi: ", "cyan"))

        if choice == '1':
            nama = input(colored("Nama produk: ", "cyan"))
            harga = float(input(colored("Harga produk: ", "cyan")))
            stok = int(input(colored("Stok produk: ", "cyan")))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (nama, harga, stok) VALUES (%s, %s, %s)", (nama, harga, stok))
            conn.commit()
            conn.close()
            console.print("[bold green]Produk berhasil ditambahkan![/bold green]")
        
        elif choice == '2':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            conn.close()

            table = Table(title="Daftar Produk")
            table.add_column("ID", justify="center", style="cyan")
            table.add_column("Nama", style="magenta")
            table.add_column("Harga", style="green")
            table.add_column("Stok", justify="center", style="yellow")

            for product in products:
                product_id = str(product[0])  # Mengambil product_id
                product_name = product[1]      # Mengambil nama produk
                product_price = str(product[2]) # Mengambil harga produk
                product_stock = product[3]     # Mengambil stok produk

                # Tentukan warna berdasarkan stok
                if product_stock <= 10:
                    stock_color = "red"
                elif product_stock > 20:
                    stock_color = "green"
                else:
                    stock_color = "yellow"

                # Tambahkan baris ke tabel dengan warna stok yang sesuai
                table.add_row(product_id , product_name, product_price, f"[{stock_color}]{product_stock}[/{stock_color}]")

            console.print(table)

        elif choice == '3':
            product_id = input(colored("ID produk yang akan ditambahkan stok: ", "cyan"))
            additional_stock = int(input(colored("Jumlah stok yang akan ditambahkan: ", "cyan")))

            conn = get_connection()
            cursor = conn.cursor()

            # Ambil stok saat ini dari produk
            cursor.execute("SELECT stok FROM products WHERE product_id = %s", (product_id,))
            current_stock = cursor.fetchone()

            if current_stock is not None:
                new_stock = current_stock[0] + additional_stock  # Tambahkan stok baru ke stok yang ada
                cursor.execute(
                    "UPDATE products SET stok = %s WHERE product_id = %s",
                    (new_stock, product_id)
                )
                conn.commit()
                console.print("[bold green]Stok produk berhasil ditambahkan![/bold green]")
            else:
                console.print("[bold red]Produk tidak ditemukan![/bold red]")

            conn.close()

        elif choice == '4':  # Opsi untuk memperbarui data produk
            product_id = input(colored("ID produk yang akan diperbarui: ", "cyan"))
            conn = get_connection()
            cursor = conn.cursor()

            # Ambil data produk saat ini
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if product is not None:
                new_name = input(colored(f"Nama baru (sekarang: {product[1]}): ", "cyan")) or product[1]
                new_harga = input(colored(f"Harga baru (sekarang: {product[2]}): ", "cyan"))
                new_harga = float(new_harga) if new_harga else product[2]
                new_stok = input(colored(f"Stok baru (sekarang: {product[3]}): ", "cyan"))
                new_stok = int(new_stok) if new_stok else product[3]

                cursor.execute(
                    "UPDATE products SET nama = %s, harga = %s, stok = %s WHERE product_id = %s",
                    (new_name, new_harga, new_stok, product_id)
                )
                conn.commit()
                console.print("[bold green]Data produk berhasil diperbarui![/bold green]")
            else:
                console.print("[bold red]Produk tidak ditemukan![/bold red]")

            conn.close()

        elif choice == '5':
            product_id = input(colored("ID produk yang akan dihapus: ", "cyan"))
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            conn.commit()
            conn.close()
            console.print("[bold red]Produk berhasil dihapus![/bold red]")

        elif choice == '6':
            break
        else:
            console.print("[bold red]Opsi tidak valid, coba lagi![/bold red]")

# Fungsi Pelanggan
def manage_customers():
    while True:
        print_header("Pelanggan")
        console.print("[bold green]1. Tambah Pelanggan[/bold green]")
        console.print("[bold yellow]2. Lihat Pelanggan[/bold yellow]")
        console.print("[bold blue]3. Hapus Pelanggan[/bold blue]")  # Opsi baru untuk menghapus pelanggan
        console.print("[bold magenta]4. Kembali ke Menu Utama[/bold magenta]")

        choice = input(colored("Pilih opsi: ", "cyan"))

        if choice == '1':
            nama = input(colored("Nama pelanggan: ", "cyan"))
            nohp = input(colored("Nomor telepon: ", "cyan"))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (nama, NoHp) VALUES (%s, %s)", (nama, nohp))
            conn.commit()
            conn.close()
            console.print("[bold green]Pelanggan berhasil ditambahkan![/bold green]")

        elif choice == '2':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
            conn.close()

            table = Table(title="Daftar Pelanggan")
            table.add_column("ID", style="cyan")
            table.add_column("Nama", style="magenta")
            table.add_column("No. Telepon", style="yellow")

            for customer in customers:
                table.add_row(str(customer[0]), customer[1], customer[2])

            console.print(table)

        elif choice == '3':  # Opsi untuk menghapus pelanggan
            customer_id = input(colored("ID pelanggan yang akan dihapus: ", "cyan"))
            conn = get_connection()
            cursor = conn.cursor()

            # Cek apakah pelanggan ada
            cursor.execute("SELECT * FROM customers WHERE customers_id = %s", (customer_id,))
            customer = cursor.fetchone()

            if customer:
                cursor.execute("DELETE FROM customers WHERE customers_id = %s", (customer_id,))
                conn.commit()
                console.print("[bold red]Pelanggan berhasil dihapus![/bold red]")
            else:
                console.print("[bold red]Pelanggan tidak ditemukan![/bold red]")

            conn.close()

        elif choice == '4':
            break
        else:
            console.print("[bold red]Opsi tidak valid, coba lagi![/bold red]")

# Fungsi Pesanan
def manage_orders():
    while True:
        print_header("Pesanan")
        console.print("[bold green]1. Buat Pesanan[/bold green]")
        console.print("[bold yellow]2. Lihat Pesanan[/bold yellow]")
        console.print("[bold blue]3. Cetak Struk[/bold blue]")
        console.print("[bold magenta]4. Kembali ke Menu Utama[/bold magenta]")

        choice = input(colored("Pilih opsi: ", "cyan"))

        if choice == '1':
            customer_id = input(colored("ID Pelanggan: ", "cyan"))
            product_id = input(colored("ID Produk: ", "cyan"))
            jumlah = int(input(colored("Jumlah Produk: ", "cyan")))

            conn = get_connection()
            cursor = conn.cursor()

            # Ambil harga dan stok produk
            cursor.execute("SELECT harga, stok FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if product:
                harga, stok = product
                if stok >= jumlah:
                    total_harga = harga * jumlah
                    cursor.execute(
                        "INSERT INTO pesanan (customer_id, product_id, jumlah_produk, total_harga, tanggal_order) VALUES (%s, %s, %s, %s, %s)",
                        (customer_id, product_id, jumlah, total_harga, datetime.now())
                    )
                    cursor.execute("UPDATE products SET stok = stok - %s WHERE product_id = %s", (jumlah, product_id))
                    conn.commit()
                    console.print("[bold green]Pesanan berhasil dibuat![/bold green]")
                else:
                    console.print("[bold red]Stok tidak mencukupi![/bold red]")
            else:
                console.print("[bold red]Produk tidak ditemukan![/bold red]")

            conn.close()

        elif choice == '2':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, c.nama AS customer_name, pr.nama AS product_name, p.jumlah_produk, p.total_harga, p.tanggal_order
                FROM pesanan p
                JOIN customers c ON p.customer_id = c.customers_id
                JOIN products pr ON p.product_id = pr.product_id
            """)
            pesanan = cursor.fetchall()
            conn.close()
            
            if pesanan:
                headers = ["ID", "Nama Pelanggan", "Nama Produk", "Jumlah Produk", "Total Harga", "Tanggal Order"]
                console.print(tabulate(pesanan, headers=headers, tablefmt="fancy_grid"))
            else:
                console.print("Tidak ada pesanan ditemukan.")

        elif choice == '3':
            order_id = input(colored("Masukkan ID Pesanan untuk dicetak: ", "cyan"))
            conn = get_connection()
            cursor = conn.cursor()

            # Ambil detail pesanan
            cursor.execute("""
                SELECT p.id, c.nama, pr.nama, p.jumlah_produk, p.total_harga, p.tanggal_order
                FROM pesanan p
                JOIN customers c ON p.customer_id = c.customers_id
                JOIN products pr ON p.product_id = pr.product_id
                WHERE p.id = %s
            """, (order_id,))
            order_detail = cursor.fetchone()

            if order_detail:
                # Mencetak struk
                console.print("\n" + "="*38)
                console.print("          STRUK PESANAN          ")
                console.print("="*38)
                console.print(f"ID Pesanan     : {order_detail[0]}")
                console.print(f"Nama Pelanggan  : {order_detail[1]}")
                console.print(f"Produk         : {order_detail[2]}")
                console.print(f"Jumlah         : {order_detail[3]}")
                console.print(f"Total Harga    : Rp {order_detail[4]:,.2f}")
                console.print(f"Tanggal Pesanan : {order_detail[5].strftime('%Y-%m-%d %H:%M:%S')}")
                console.print("="*38)
                console.print(" Terima kasih telah berbelanja! ")
                console.print("="*38)
            else:
                console.print("[bold red]Pesanan tidak ditemukan![/bold red]")

            conn.close()
        elif choice == "4":
            break
        else:
            console.print("[bold red]Opsi tidak valid, coba lagi![/bold red]")

# Fungsi Laporan Penjualan
def sales_report():
    print_header("Laporan Penjualan")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pr.nama, SUM(p.jumlah_produk) AS total_terjual, SUM(p.total_harga) AS pendapatan
        FROM pesanan p
        JOIN products pr ON p.product_id = pr.product_id
        GROUP BY p.product_id
    """)
    sales = cursor.fetchall()
    conn.close()

    if sales:
        table = Table(title="Laporan Penjualan")
        table.add_column("Produk", style="cyan")
        table.add_column("Total Terjual", justify="center", style="magenta")
        table.add_column("Pendapatan", justify="right", style="green")

        for sale in sales:
            table.add_row(sale[0], str(sale[1]), f"Rp {sale[2]:,}")

        console.print(table)
    else:
        console.print("[bold yellow]Tidak ada data penjualan saat ini.[/bold yellow]")

# Menu Utama
def main():
    if login():  # Panggil fungsi login sebelum masuk ke menu utama
        while True:
            print_header("Toko Busana Muslim")
            console.print("[bold green]1. Kelola Produk[/bold green]")
            console.print("[bold yellow]2. Kelola Pelanggan[/bold yellow]")
            console.print("[bold blue]3. Kelola Pesanan[/bold blue]")
            console.print("[bold magenta]4. Laporan Penjualan[/bold magenta]")
            console.print("[bold red]5. Keluar[/bold red]")

            choice = input(colored("Pilih opsi: ", "cyan"))

            if choice == '1':
                manage_products()
            elif choice == '2':
                manage_customers()
            elif choice == '3':
                manage_orders()
            elif choice == '4':
                sales_report()
            elif choice == '5':
                console.print("[bold red]Keluar dari aplikasi...[/bold red]")
                break
            else:
                console.print("[bold red]Opsi tidak valid, coba lagi![/bold red]")

# Jalankan Program
if __name__ == "__main__":
    main()