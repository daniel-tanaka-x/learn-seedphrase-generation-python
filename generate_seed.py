import hmac, hashlib, base58, struct
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import RIPEMD160

# === ユーティリティ関数 ===
def hmac_sha512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()

def derive_point_from_privkey(privkey):
    sk = SigningKey.from_string(privkey, curve=SECP256k1)
    vk = sk.verifying_key
    return vk.to_string("compressed")

def calc_fingerprint(pubkey):
    h = hashlib.sha256(pubkey).digest()
    ripemd = RIPEMD160.new(h).digest()
    return ripemd[:4]

def pubkey_to_p2pkh(pubkey):
    h = hashlib.sha256(pubkey).digest()
    ripemd = RIPEMD160.new(h).digest()
    payload = b'\x00' + ripemd
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()

def to_wif_compressed(privkey):
    payload = b'\x80' + privkey + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()

def derive_child_key(k_par, c_par, index):
    if index >= 0x80000000:
        data = b'\x00' + k_par + struct.pack('>L', index)
    else:
        pub_par = derive_point_from_privkey(k_par)
        data = pub_par + struct.pack('>L', index)
    I = hmac_sha512(c_par, data)
    IL, IR = I[:32], I[32:]
    k_int = (int.from_bytes(IL, 'big') + int.from_bytes(k_par, 'big')) % SECP256k1.order
    return k_int.to_bytes(32, 'big'), IR

# === Colab用プロンプトからエントロピー入力 ===
print("🌱 エントロピーを入力してください（例：0と1の文字列128文字。例: '010110...')")
while True:
    bin_str = input("🔑 エントロピー (128ビット=128文字): ").strip()
    if len(bin_str) == 128 and all(c in '01' for c in bin_str):
        break
    print("⚠️ 入力エラー：0と1の文字列128文字で入力してください。")

byte_data = bytes(int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8))
sha256_hash = hashlib.sha256(byte_data).digest()
checksum_bits = format(sha256_hash[0], '08b')[:4]
full_bits = bin_str + checksum_bits
indexes = [int(full_bits[i:i+11], 2) for i in range(0, len(full_bits), 11)]
with open('english.txt', 'r') as f:
    word_list = [line.strip() for line in f.readlines()]
mnemonic = ' '.join([word_list[i] for i in indexes])
print(f"🔑 ニーモニック: {mnemonic}")

# === パスフレーズ情報 ===
passphrase = "Buybitcoin"
salt = "mnemonic" + passphrase
print(f"\n🔐 パスフレーズ: {passphrase}")
print(f"🔐 ソルト: {salt}")

# === シード生成 ===
print("\n🔑 [PBKDF2-HMAC-SHA512]とニーモニックとソルトからシード生成")
seed = hashlib.pbkdf2_hmac('sha512', mnemonic.encode(), salt.encode(), 2048, dklen=64)
print(f"🔑 シード（64バイト）: {seed.hex()}")

# === マスター鍵生成（BIP32ルート） ===
print("\n🔑 [HMAC-SHA512]と固定文字列'Bitcoin seed'とシードからマスター秘密鍵とチェーンコード生成")
I = hmac_sha512(b"Bitcoin seed", seed)
k_master, c_master = I[:32], I[32:]
pubkey_master = derive_point_from_privkey(k_master)
root_fp = calc_fingerprint(pubkey_master).hex()
print(f"🌿 マスター秘密鍵（k_master）: {k_master.hex()}")
print(f"🌿 チェーンコード（c_master）: {c_master.hex()}")
print(f"🧩 フィンガープリント: {root_fp}")

# === BIP32ルート拡張鍵 ===
print("\n🔑 マスター秘密鍵とチェーンコードからBIP32ルート拡張鍵 (xprv/xpub)生成")
xprv_data = bytes.fromhex("0488ADE4") + b'\x00' + b'\x00'*4 + struct.pack('>L',0) + c_master + b'\x00' + k_master
xprv = base58.b58encode(xprv_data + hashlib.sha256(hashlib.sha256(xprv_data).digest()).digest()[:4]).decode()
xpub_data = bytes.fromhex("0488B21E") + b'\x00' + b'\x00'*4 + struct.pack('>L',0) + c_master + pubkey_master
xpub = base58.b58encode(xpub_data + hashlib.sha256(hashlib.sha256(xpub_data).digest()).digest()[:4]).decode()
print(f"🔑 xprv（ルート）: {xprv}")
print(f"🔑 xpub（ルート）: {xpub}")

# === BIP44アドレス＆秘密鍵（圧縮WIF） ===
print("\n📬 P2PKHアドレスと秘密鍵（圧縮WIF）: m/44'/0'/0'/0/i 生成")
bip44_path = [44+0x80000000, 0+0x80000000, 0+0x80000000, 0]
for i in range(5):
    k, c = k_master, c_master
    for idx in bip44_path + [i]:
        k, c = derive_child_key(k, c, idx)
    pubkey = derive_point_from_privkey(k)
    addr = pubkey_to_p2pkh(pubkey)
    wif = to_wif_compressed(k)
    print(f" - {i}: {addr}\n   🔐 秘密鍵（圧縮WIF）: {wif}")

# === BIP84ルート拡張鍵 ===
print("\n🔑 BIP84ルート拡張鍵 (zprv/zpub)生成")
zprv_data = bytes.fromhex("04b2430c") + b'\x00' + b'\x00'*4 + struct.pack('>L',0) + c_master + b'\x00' + k_master
zprv = base58.b58encode(zprv_data + hashlib.sha256(hashlib.sha256(zprv_data).digest()).digest()[:4]).decode()
zpub_data = bytes.fromhex("04b24746") + b'\x00' + b'\x00'*4 + struct.pack('>L',0) + c_master + pubkey_master
zpub = base58.b58encode(zpub_data + hashlib.sha256(hashlib.sha256(zpub_data).digest()).digest()[:4]).decode()
print(f"🔑 zprv: {zprv}")
print(f"🔑 zpub: {zpub}")
