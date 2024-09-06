from flask import Flask, render_template, request

app = Flask(__name__)

def shift_left(bits, n):
    return ((bits << n) & 0xF) | ((bits >> (4 - n)) & 0xF)

def bin_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:].upper()
    return hex_str

def xor_encrypt_ecb(plaintext, key):
    ciphertext = ""
    for i in range(0, len(plaintext), 4):
        block = plaintext[i:i+4]
        if len(block) < 4:
            block = block.ljust(4, '0')
        block_int = int(block, 2)
        encrypted_block = block_int ^ key
        encrypted_block = shift_left(encrypted_block, 1)
        ciphertext += format(encrypted_block, '04b')
    
    return bin_to_hex(ciphertext)

def xor_encrypt_cbc(plaintext, key, iv):
    ciphertext = ""
    prev_block = iv
    for i in range(0, len(plaintext), 4):
        block = plaintext[i:i+4]
        if len(block) < 4:
            block = block.ljust(4, '0')
        block_int = int(block, 2)
        xor_block = block_int ^ prev_block
        encrypted_block = xor_block ^ key
        encrypted_block = shift_left(encrypted_block, 1)
        ciphertext += format(encrypted_block, '04b')
        prev_block = encrypted_block
    
    return bin_to_hex(ciphertext)

@app.route("/", methods=["GET", "POST"])
def encrypt():
    ciphertext = None
    if request.method == "POST":
        plaintext = request.form.get("plaintext")
        key = int(request.form.get("key"), 2)
        iv = request.form.get("iv")
        mode = request.form.get("mode")

        if mode == "ECB":
            ciphertext = xor_encrypt_ecb(plaintext, key)
        elif mode == "CBC":
            iv = int(iv, 2)
            ciphertext = xor_encrypt_cbc(plaintext, key, iv)
    
    return render_template("enkrip.html", ciphertext=ciphertext)

if __name__ == "__main__":
    app.run(debug=True)
