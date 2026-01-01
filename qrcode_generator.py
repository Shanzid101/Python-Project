import qrcode
data = input("Enter a link/text:")
qr = qrcode.make(data)
qr.save("facebook.png")
print("QR code generate Successfully!")