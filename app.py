import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Đối soát danh sách", layout="wide")
st.title("⚖️ Công cụ đối soát danh sách học sinh")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Tải DS 1", type=["xlsx"])
with col2:
    file2 = st.file_uploader("Tải DS 2", type=["xlsx"])

def find_col(df, options):
    """Tìm cột dựa trên danh sách các từ khóa có thể xảy ra"""
    for col in df.columns:
        col_clean = str(col).lower().replace(" ", "")
        for opt in options:
            if opt in col_clean:
                return col
    return None

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # Danh sách từ khóa mở rộng (bao gồm cả 'họ và tên')
        ten_keys = ['hoten', 'hovaten', 'ten']
        sinh_keys = ['ngaysinh', 'ns']
        
        t1, s1 = find_col(df1, ten_keys), find_col(df1, sinh_keys)
        t2, s2 = find_col(df2, ten_keys), find_col(df2, sinh_keys)
        
        if not all([t1, s1, t2, s2]):
            st.error("❌ Không tự nhận diện được cột. Vui lòng đổi tên cột trong file thành 'Họ tên' và 'Ngày sinh'")
            st.write("DS1 cột:", df1.columns.tolist())
            st.write("DS2 cột:", df2.columns.tolist())
        else:
            # Tạo khóa so sánh
            df1['key'] = df1[t1].astype(str).str.strip().str.lower() + "_" + df1[s1].astype(str).str.strip()
            df2['key'] = df2[t2].astype(str).str.strip().str.lower() + "_" + df2[s2].astype(str).str.strip()
            
            # So sánh
            thieu_trong_ds2 = df1[~df1['key'].isin(df2['key'])].drop(columns=['key'])
            thieu_trong_ds1 = df2[~df2['key'].isin(df1['key'])].drop(columns=['key'])
            
            st.success("✅ Đã đối soát xong!")
            
            # Xuất file
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                thieu_trong_ds2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
                thieu_trong_ds1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
            
            st.download_button("📥 Tải kết quả", data=buffer, file_name="Ket_qua.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
