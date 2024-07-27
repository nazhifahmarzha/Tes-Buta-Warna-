import streamlit as st # type: ignore
import pandas as pd # type: ignore
import joblib # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore
from streamlit_option_menu import option_menu # type: ignore
from io import BytesIO

# Load model dan LabelEncoder yang sudah dilatih
model = joblib.load('knn_model.pkl')
le = joblib.load('label_encoder.pkl')

# Load the CSV file
file_path = 'Updated_Dataset.csv'
data = pd.read_csv(file_path)

# Pra-pemrosesan data
X = data.drop(columns=['Nama', 'Jenis Kelamin', 'Diagnosa'])
feature_names = X.columns.tolist()

# Kunci jawaban
correct_answers = [12, 8, 29, 5, 3, 15, 74, 6, 45, 5, 7, 16, 73, "tidak ada", "tidak ada", 26, 42, "jalur merah dan ungu",
                   "tidak ada", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau",
                   "jalur violet dan orange", "jalur orange"]

multiple_choice_options = {
    13: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    14: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    17: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    18: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    19: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    20: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    21: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    22: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"],
    23: ["", "tidak ada", "jalur merah dan ungu", "jalur biru-hijau", "jalur orange", "jalur biru-hijau dan kuning-hijau", "jalur violet dan orange"]
}

def evaluate_responses(user_responses):
    """
    Evaluasi jawaban pengguna dan tentukan diagnosis.
    
    :param user_responses: Jawaban pengguna untuk setiap plate.
    :return: Diagnosis prediksi.
    """
    evaluated_responses = []
    for response, correct in zip(user_responses, correct_answers):
        if str(response).strip().lower() == str(correct).strip().lower():
            evaluated_responses.append(1)
        else:
            evaluated_responses.append(0)
    
    if evaluated_responses[0] == 0:
        return "total"
    
    incorrect_answers = evaluated_responses.count(0)
    
    if incorrect_answers >= 2:
        return "parcial"
    else:
        return "normal"

def reset_test():
    """Reset the test state."""
    st.session_state['submitted'] = False
    st.session_state['current_index'] = 0
    st.session_state['user_responses'] = [None] * 24
    st.session_state['start_test'] = False
    st.session_state['user_name'] = ""
    st.session_state['gender'] = ""
    st.session_state['age'] = ""

def save_results_to_excel(name, gender, age, diagnosis, user_responses):
    """
    Simpan hasil diagnosa dan biodata ke dalam file Excel.
    
    :param name: Nama pengguna.
    :param gender: Jenis kelamin pengguna.
    :param age: Umur pengguna.
    :param diagnosis: Hasil diagnosis.
    :param user_responses: Jawaban pengguna untuk setiap plate.
    :return: Excel dalam format BytesIO.
    """
    data = {
        "Nama": [name],
        "Jenis Kelamin": [gender],
        "Umur": [age],
        "Diagnosis": [diagnosis]
    }
    for i, response in enumerate(user_responses, 1):
        data[f"Plate {i}"] = [response]
    
    df = pd.DataFrame(data)
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Hasil Diagnosa')
    return excel_buffer.getvalue()

# Antarmuka Streamlit
with st.sidebar:
    # Tambahkan gambar profil atau logo di atas menu
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Right_leaning_heart_pop.gif/640px-Right_leaning_heart_pop.gif', caption='Love', use_column_width=True)

    selected_option = option_menu("Menu", ["Home", "Tes Buta Warna", "Tentang"], 
        icons=['house', 'clipboard', 'info-circle'], menu_icon="cast", default_index=0)

    # Tambahkan ikon sosial media dalam posisi horizontal di atas teks "Developer by Nazifa"
    st.markdown("""
        <div style="text-align: center; margin-top: 15px;">
            <a href="https://wa.me/0895322662193" target="_blank" style="margin: 0 15px;"><img src="https://img.icons8.com/color/48/000000/whatsapp.png" alt="WhatsApp"/></a>
            <a href="https://instagram.com/nazhfh_" target="_blank" style="margin: 0 15px;"><img src="https://img.icons8.com/fluency/48/000000/instagram-new.png" alt="Instagram"/></a>
            <a href="https://mail.google.com/mail/?view=cm&fs=1&to=nazhifahmarzha@gmail.com" style="margin: 0 15px;"><img src="https://img.icons8.com/fluency/48/000000/email.png" alt="Email"/></a>
        </div>
    """, unsafe_allow_html=True)

    # Tambahkan teks "Developer by Nazifa" dengan animasi di bawah ikon sosial media
    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="font-size: 18px; display: inline-block; animation: slide 2s ease-out;">𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐛𝐲 𝐧𝐚𝐳𝐡𝐢𝐟𝐚𝐡‌</p>
        </div>
        <style>
            @keyframes slide {
                from {
                    transform: translateX(100%);
                }
                to {
                    transform: translateX(0);
                }
            }
        </style>
    """, unsafe_allow_html=True)

if selected_option == "Home":
    st.markdown("<h1 style='text-align: center;'>Selamat Datang di Aplikasi Tes Buta Warna</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>Gunakan menu di sebelah kiri untuk menavigasi aplikasi.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnhB7_axSjOtgsivmBhZGRJJinPWBhUulFkqlXsOGhqM7-yNNbUuLppXi1AOFDC6iCxxA&usqp=CAU' width='400'><p>N for Nazhifah</p></div>", unsafe_allow_html=True)
elif selected_option == "Tes Buta Warna":
    st.markdown("<h1 style='text-align: center;'>Aplikasi Tes Buta Warna</h1>", unsafe_allow_html=True)

    if 'user_responses' not in st.session_state:
        st.session_state['user_responses'] = [None] * 24

    if 'current_index' not in st.session_state:
        st.session_state['current_index'] = 0

    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    if 'start_test' not in st.session_state:
        st.session_state['start_test'] = False

    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = ""

    if 'gender' not in st.session_state:
        st.session_state['gender'] = ""

    if 'age' not in st.session_state:
        st.session_state['age'] = ""

    if not st.session_state['start_test']:
        st.session_state['user_name'] = st.text_input("Masukkan Nama Anda", value=st.session_state['user_name'])
        st.session_state['gender'] = st.selectbox("Pilih Jenis Kelamin Anda", ["", "Laki-laki", "Perempuan"], index=0 if st.session_state['gender'] == "" else ["", "Laki-laki", "Perempuan"].index(st.session_state['gender']))
        st.session_state['age'] = st.number_input("Masukkan Umur Anda", min_value=0, step=1, value=st.session_state['age'] or 0)
        
        with st.expander("Petunjuk Tes"):
            st.write("""
                Sebelum memulai tes Ishihara, Anda harus mengisi biodata terlebih dahulu.
                Tes ini berisikan plate-plate Ishihara yang dijawab sesuai dengan apa yang terlihat dengan waktu yang telah ditentukan dan Anda tidak dapat mengulang tes bila tidak berhasil menjawab.
            """)

        if st.session_state['user_name'] != "" and st.session_state['gender'] != "" and st.session_state['age'] > 0:
            if st.button('Start Test'):
                st.session_state['start_test'] = True
    else:
        st.write(f"Nama: {st.session_state['user_name']}")
        st.write(f"Jenis Kelamin: {st.session_state['gender']}")
        st.write(f"Umur: {st.session_state['age']}")

        feature_names = X.columns.tolist()

        # Form untuk input pengguna
        st.markdown("<h4 style='text-align: center;'>Masukkan Hasil Tes Anda</h4>", unsafe_allow_html=True)

        if st.session_state['current_index'] < 24:
            # Tentukan jalur gambar berdasarkan indeks saat ini
            plate_image_path = f'plate{st.session_state["current_index"] + 1}.jpeg'
            try:
                st.image(plate_image_path, caption=f'Plate {st.session_state["current_index"] + 1}', width=300)
                if st.session_state['current_index'] in multiple_choice_options:
                    st.session_state['user_responses'][st.session_state['current_index']] = st.selectbox(
                        f'Masukkan hasil untuk Plate {st.session_state["current_index"] + 1}', 
                        options=multiple_choice_options[st.session_state['current_index']],
                        index=0
                    )
                else:
                    st.session_state['user_responses'][st.session_state['current_index']] = st.text_input(
                        f'Masukkan hasil untuk Plate {st.session_state["current_index"] + 1}', 
                        value=st.session_state['user_responses'][st.session_state['current_index']] or ""
                    )
            except Exception as e:
                st.error(f"Error opening '{plate_image_path}': {e}")
            
            if st.button('Next'):
                if st.session_state['user_responses'][st.session_state['current_index']].strip() == "":
                    st.error("Mohon masukkan hasil untuk plate ini sebelum melanjutkan.")
                else:
                    if st.session_state['current_index'] == 0 and str(st.session_state['user_responses'][0]).strip().lower() != str(correct_answers[0]).strip().lower():
                        st.markdown("<h4 style='text-align: center;'>Prediksi Diagnosis: total</h4>", unsafe_allow_html=True)
                        if st.button('Mulai Ulang'):
                            reset_test()
                    else:
                        st.session_state['current_index'] += 1

        if st.session_state['current_index'] == 24:
            if st.button('Submit'):
                st.session_state['submitted'] = True

        # Prediksi dan tampilkan hasil
        if st.session_state['submitted']:
            if None in st.session_state['user_responses'] or "" in st.session_state['user_responses']:
                st.error("Mohon lengkapi semua hasil tes sebelum submit.")
            else:
                diagnosis = evaluate_responses(st.session_state['user_responses'])
                st.markdown(f"<h4 style='text-align: center;'>Prediksi Diagnosis: {diagnosis}</h4>", unsafe_allow_html=True)
                if st.button('Mulai Ulang'):
                    reset_test()

                # Simpan hasil ke dalam Excel
                excel_data = save_results_to_excel(st.session_state['user_name'], st.session_state['gender'], st.session_state['age'], diagnosis, st.session_state['user_responses'])
                st.download_button(label="Download Hasil Diagnosa", data=excel_data, file_name='hasil_diagnosa.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

elif selected_option == "Tentang":
    st.markdown("<h1 style='text-align: center;'>Tentang Aplikasi Ini</h1>", unsafe_allow_html=True)
    
    with st.expander("Sejarah Metode Ishihara"):
        st.markdown("<div style='text-align: center;'><img src='https://static.cdntap.com/tap-assets-prod/wp-content/uploads/sites/24/2022/06/a-ish.jpg?width=450&quality=90' width='400'><p>Dr. Shinobu Ishihara</p></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify;'>
        Metode Ishihara dikembangkan oleh Dr. Shinobu Ishihara pada tahun 1917. Dr. Ishihara, seorang profesor oftalmologi di Universitas Tokyo, menciptakan metode ini untuk mendeteksi gangguan persepsi warna, khususnya buta warna. 
        Metode ini terdiri dari gambar pseudo-isochromatic yang dirancang untuk menguji kemampuan seseorang dalam membedakan berbagai warna. 
        Setiap lembaran uji terdiri dari titik-titik dengan berbagai warna dan ukuran yang membentuk lingkaran. Di antara titik-titik ini, terdapat angka-angka atau pola tertentu yang harus ditebak oleh orang yang diuji.

        Dr. Ishihara awalnya mengembangkan metode ini selama dinasnya di Angkatan Darat Kekaisaran Jepang, di mana ia bertanggung jawab atas pemeriksaan medis para tentara. 
        Tes ini kemudian dipublikasikan pada tahun 1917 dan sejak itu menjadi standar emas dalam mendeteksi buta warna.

        Keunggulan dari metode Ishihara terletak pada kesederhanaannya dalam penggunaan dan keakuratan hasilnya. Tes ini tidak memerlukan peralatan khusus selain dari buku tes itu sendiri, yang membuatnya mudah digunakan di berbagai situasi klinis. 
        Hingga saat ini, metode Ishihara tetap menjadi salah satu tes yang paling umum digunakan di seluruh dunia untuk mendeteksi gangguan persepsi warna.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Tentang Pembuatan Aplikasi"):
        st.markdown("""
        <div style='text-align: justify;'>
        Aplikasi ini merupakan alat diagnostik yang dirancang untuk menilai kemampuan pengguna dalam membedakan warna menggunakan pola titik-titik warna khas Ishihara. 
        Tes ini sangat berguna dalam mengidentifikasi kondisi buta warna, dengan memberikan informasi yang akurat tentang kemampuan visual pengguna dalam mengenali berbagai spektrum warna.

        Fitur-fitur aplikasi ini meliputi:

        *Tes Ishihara*: Menggunakan serangkaian gambar yang terdiri dari titik-titik warna yang membentuk angka atau pola tertentu, pengguna akan diminta untuk mengidentifikasi angka atau pola tersebut. 
        Hasil dari tes ini akan membantu dalam menentukan apakah pengguna mengalami buta warna dan seberapa parah kondisinya.

        *Analisis Hasil*: Berdasarkan jawaban yang diberikan oleh pengguna, aplikasi ini akan memberikan diagnosis apakah pengguna normal, buta warna parsial, atau total. 
        Hasil ini didukung oleh algoritma pembelajaran mesin yang telah dilatih untuk memberikan prediksi yang akurat.

        *Antarmuka Pengguna yang Mudah*: Aplikasi ini dirancang dengan antarmuka yang ramah pengguna, memastikan bahwa tes dapat diikuti dengan mudah oleh semua kalangan usia.

        Dengan aplikasi ini, kami berharap dapat menyediakan alat yang efektif dan mudah digunakan untuk mendeteksi buta warna, sehingga pengguna dapat mengambil langkah-langkah yang tepat untuk mengatasi kondisi mereka.
        </div>
        """, unsafe_allow_html=True)