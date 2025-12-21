import streamlit as st
import cv2
import numpy as np
from PIL import Image

def main():
    # 1. Judul dan Konfigurasi Halaman
    st.set_page_config(page_title="Image Enhancement App", layout="wide")
    st.title("Aplikasi Pengolahan Citra Digital - Image Enhancement")
    st.markdown("Oleh: **Muhammad Rossi & Rafael Hafid Taftazani**")

    # 2. Upload Gambar (Pengganti filedialog Tkinter)
    uploaded_file = st.sidebar.file_uploader("Pilih Gambar", type=["jpg", "jpeg", "png"])

    # 3. Panel Kontrol (Pengganti Slider Tkinter)
    st.sidebar.header("Pengaturan Filter")
    
    # Range slider disesuaikan dengan kode Tkinter Anda
    blur_amount = st.sidebar.slider("Blur (Kernel Size)", 1, 15, 1, step=2)
    contrast = st.sidebar.slider("Kontras", 0.5, 3.0, 1.0, 0.1)
    brightness = st.sidebar.slider("Brightness", -2.0, 2.0, 0.0, 0.1)
    saturation = st.sidebar.slider("Saturasi", 0.5, 3.0, 1.0, 0.1)
    sharpness = st.sidebar.slider("Sharpening", 0.0, 2.0, 0.0, 0.1)

    if uploaded_file is not None:
        # Konversi file upload ke format OpenCV
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_img = cv2.imdecode(file_bytes, 1)

        # ==========================================
        # PROSES FILTER (Logika dari file lama Anda)
        # ==========================================
        img = original_img.copy()

        # 1. Blur
        k = blur_amount
        if k % 2 == 0: k += 1
        if k > 1:
            img = cv2.GaussianBlur(img, (k, k), 0)

        # 2. Brightness & Contrast
        # Beta dikali 20 sesuai logika kode Tkinter Anda (brightness_slider.get() * 20)
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness * 20)

        # 3. Saturation (HSV)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] *= saturation
        hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
        img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # 4. Sharpening (Kernel Custom)
        if sharpness > 0:
            kernel = np.array([
                [0, -1, 0],
                [-1, 5 + sharpness, -1],
                [0, -1, 0]
            ])
            img = cv2.filter2D(img, -1, kernel)

        # ==========================================
        # TAMPILAN (Split View Before/After)
        # ==========================================
        col1, col2 = st.columns(2)

        with col1:
            st.header("Original (Before)")
            # Convert BGR to RGB for Streamlit/PIL
            st.image(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB), use_container_width=True)

        with col2:
            st.header("Hasil Filter (After)")
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_container_width=True)

        # Tombol Download
        # Convert kembali ke RGB Image untuk disimpan
        result_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Simpan ke buffer memory (virtual file)
        import io
        buf = io.BytesIO()
        result_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Simpan Hasil Gambar",
            data=byte_im,
            file_name="hasil_edit.jpg",
            mime="image/jpeg"
        )
    else:
        st.info("Silakan upload gambar melalui sidebar di sebelah kiri.")

if __name__ == "__main__":
    main()