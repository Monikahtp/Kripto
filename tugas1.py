import tkinter as tk
from tkinter import ttk

# Fungsi untuk menggeser bit ke kiri
def shift_left(bits, n):
    # Geser bit ke kiri, dengan wrapping untuk bit yang keluar
    return ((bits << n) & 0xF) | ((bits >> (4 - n)) & 0xF)

# Fungsi enkripsi ECB
def xor_encrypt_ecb(plaintext, key):
    ciphertext = ""
    # Bagi plaintext menjadi blok-blok 4-bit
    for i in range(0, len(plaintext), 4):
        block = plaintext[i:i+4]
        if len(block) < 4:
            block = block.ljust(4, '0')  # Isi dengan 0 jika panjangnya kurang dari 4

        # Konversi blok ke bilangan bulat
        block_int = int(block, 2)
        # XOR dengan kunci
        encrypted_block = block_int ^ key
        # Geser 1 bit ke kiri
        encrypted_block = shift_left(encrypted_block, 1)
        # Konversi kembali ke string biner dan tambahkan ke ciphertext
        ciphertext += format(encrypted_block, '04b')
    return ciphertext

# Fungsi enkripsi CBC
def xor_encrypt_cbc(plaintext, key, iv):
    ciphertext = ""
    prev_block = iv
    # Bagi plaintext menjadi blok-blok 4-bit
    for i in range(0, len(plaintext), 4):
        block = plaintext[i:i+4]
        if len(block) < 4:
            block = block.ljust(4, '0')  # Isi dengan 0 jika panjangnya kurang dari 4

        # Konversi blok ke bilangan bulat
        block_int = int(block, 2)
        # XOR dengan blok sebelumnya
        xor_block = block_int ^ prev_block
        # XOR dengan kunci
        encrypted_block = xor_block ^ key
        # Geser 1 bit ke kiri
        encrypted_block = shift_left(encrypted_block, 1)
        # Konversi kembali ke string biner dan tambahkan ke ciphertext
        ciphertext += format(encrypted_block, '04b')
        # Update blok sebelumnya
        prev_block = encrypted_block
    return ciphertext

# Fungsi yang dipanggil saat tombol enkripsi ditekan
def encrypt():
    plaintext = entry_plaintext.get()
    key = int(entry_key.get(), 2)  # Mengubah kunci dari biner ke integer
    iv = int(entry_iv.get(), 2)  # Mengubah IV dari biner ke integer

    mode = combo_mode.get()
    if mode == "ECB":
        ciphertext = xor_encrypt_ecb(plaintext, key)
    elif mode == "CBC":
        ciphertext = xor_encrypt_cbc(plaintext, key, iv)
    else:
        ciphertext = "Invalid Mode Selected!"

    output_ciphertext.set(ciphertext)

# Membuat jendela UI dengan Tkinter
window = tk.Tk()
window.title("XOR Encryption with Tkinter")

# Label dan Entry untuk plaintext
tk.Label(window, text="Plaintext (biner):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_plaintext = tk.Entry(window)
entry_plaintext.grid(row=0, column=1, padx=5, pady=5)

# Label dan Entry untuk kunci
tk.Label(window, text="Key (4-bit biner):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_key = tk.Entry(window)
entry_key.grid(row=1, column=1, padx=5, pady=5)

# Label dan Entry untuk IV
tk.Label(window, text="IV (CBC only, 4-bit biner):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_iv = tk.Entry(window)
entry_iv.grid(row=2, column=1, padx=5, pady=5)

# Combo box untuk memilih mode enkripsi
tk.Label(window, text="Mode:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
combo_mode = ttk.Combobox(window, values=["ECB", "CBC"])
combo_mode.grid(row=3, column=1, padx=5, pady=5)
combo_mode.current(0)  # Default ke ECB

# Tombol untuk Enkripsi
button_encrypt = tk.Button(window, text="Encrypt", command=encrypt)
button_encrypt.grid(row=4, columnspan=2, pady=10)

# Output ciphertext
output_ciphertext = tk.StringVar()
tk.Label(window, text="Ciphertext:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
tk.Entry(window, textvariable=output_ciphertext, state='readonly').grid(row=5, column=1, padx=5, pady=5)

# Jalankan UI
window.mainloop()
