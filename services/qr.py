"""
QR generation using the `qrcode` library (already in requirements.txt).

The rest of the app expects one function here:

    generate_qr_png(url: str) -> bytes

which takes the full delivery URL (e.g. f"{BASE_URL}/d/{token}") and returns
PNG image bytes. routes/admin.py calls this and serves the bytes directly.
"""

import io

import qrcode


def generate_qr_png(url: str) -> bytes:
    qr = qrcode.QRCode(
        version=None,  # let the library pick the smallest size that fits the data
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,   # pixels per QR "module" — bump this up for a bigger printed code
        border=4,      # quiet zone, in modules — keep at least 4 for reliable scanning
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()