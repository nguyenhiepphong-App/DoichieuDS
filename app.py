import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Đối soát danh sách", layout="wide")
st.title("⚖️ Công cụ đối soát danh sách học sinh tự động")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Tải DS 1 (File gốc)", type=["xlsx"])
with col2:
    file2 = st.file_uploader("Tải DS 2 (File cần đối chiếu)", type=["xlsx"])

def find_col(df, keywords):
    """Tự động tìm tên cột dựa trên từ khóa"""
    for col in df.columns:
        col_clean = str(col).lower().replace(" ", "").replace("à", "a").replace("á", "a") # Chuẩn hóa cơ bản
        for kw in keywords:
            if kw in col_clean:
                return col
    return None

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # Danh sách từ khóa để máy tự "đoán" cột
        ten_kw = ['hoten', 'hovaten', 'tenhs', 'ten']
        sinh_kw = ['ngaysinh', 'ngaysinh', 'ns', 'ngaysinhhocsinh']
        
        # Tìm cột
        t1, s1 = find_col(df1, ten_kw), find_col(df1, sinh_kw)
        t2, s2 = find_col(df2, ten_kw), find_col(df2, sinh_kw)
        
        if not all([t1, s1, t2, s2]):
            st.error("❌ Không tự động nhận diện được cột! Kiểm tra tên các cột trong file:")
            st.write("DS1 có các cột:", df1.columns.tolist())
            st.write("DS2 có các cột:", df2.columns.tolist())
        else:
            # Tạo khóa so sánh (làm sạch dữ liệu)
            def create_key(df, col_ten, col_sinh):
                return df[col_ten].astype(str).str.strip().str.lower() + "_" + df[col_sinh].astype(str).str.strip()

            df1['key'] = create_key(df1, t1, s1)
            df2['key'] = create_key(df2, t2, s2)
            
            # Đối soát
            thieu_trong_ds2 = df1[~df1['key'].isin(df2['key'])].drop(columns=['key'])
            thieu_trong_ds1 = df2[~df2['key'].isin(df1['key'])].drop(columns=['key'])
            
            st.success("✅ Đã đối soát thành công!")
            
            # Hiển thị tóm tắt
            c1, c2 = st.columns(2)
            c1.metric("Thiếu trong DS2", len(thieu_trong_ds2))
            c2.metric("Thiếu trong DS1", len(thieu_trong_ds1))
            
            # Xuất file Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                thieu_trong_ds2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
                thieu_trong_ds1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
            
            st.download_button("📥 Tải kết quả đối soát (.xlsx)", data=buffer, file_name="Ket_qua_so_sanh.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")

st.markdown("---")
st.markdown("Người thực hiện: **Nguyen Hiep Phong - THPT Bến Tre**")
