import os

# Base directory setup
SO_PATH = 'lib/arm64-v8a/libil2cpp.so'

def patch_file(file_path, offset_hex, patch_bytes):
    print(f"Patching {file_path} at {offset_hex}...")
    with open(file_path, 'r+b') as f:
        f.seek(int(offset_hex, 16))
        f.write(patch_bytes)

if __name__ == "__main__":
    if not os.path.exists(SO_PATH):
        print(f"Error: {SO_PATH} not found. Please run this script from the extracted APK root.")
    else:
        # GooglePurchase.IsPurchased -> Always true
        patch_file(SO_PATH, '0x5070B6C', bytes([0x20, 0x00, 0x80, 0x52, 0xC0, 0x03, 0x5F, 0xD6]))
        
        # Product.get_hasReceipt -> Always true
        patch_file(SO_PATH, '0x5023700', bytes([0x20, 0x00, 0x80, 0x52, 0xC0, 0x03, 0x5F, 0xD6]))
        
        # NonConsumableInAppPurchase.get_SaveIsPurchasedLocally -> Always true
        patch_file(SO_PATH, '0x42D8B4C', bytes([0x20, 0x00, 0x80, 0x52, 0xC0, 0x03, 0x5F, 0xD6]))
        
        print("Stable V2 patches applied successfully!")
