import streamlit as st

def show():
    st.markdown("""
<div style='
    background-color: #DFF0FF;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 20px;
'>
    Selamat datang di halaman utama Human Capital Evaluation Tools.
</div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
    <style>
        .hover-box {{
            background-color: #8fc0ed; 
            padding: 3px;
            margin-bottom: 10px;
            border-radius: 2px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .hover-box:hover {{
            transform: scale(1.05); /* Zoom saat hover */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Efek bayangan */
        }}
        .content {{
            margin-left: 20px;
        }}
    </style>

    <div class="hover-box">
        <ul class="content">
            <li><b>Menu Tab</b> berisi Features dan HC Tools.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li> Menu <b>Feature</b>, menjelaskan informasi dataset dan fitur yang digunakan dalam model.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li>Pada Menu <b>HC Tools</b>, tersedia adalah alat bantu untuk mengevaluasi performa karyawan berdasarkan data yang tersedia.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li><b>Tools ini dikembangkan oleh:</b> Alvina Tsabitah - 2025.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
