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

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # Ép buộc lấy cột thứ 1 làm Tên và cột thứ 2 làm Ngày sinh (dựa trên ảnh ông chụp)
        # Tên cột ở vị trí 1 và 2 (theo danh sách 0, 1, 2, 3 của ông)
        t1, s1 = df1.columns[1], df1.columns[2]
        t2, s2 = df2.columns[1], df2.columns[2]
        
        # Tạo khóa so sánh
        df1['key'] = df1[t1].astype(str).str.strip().str.lower() + "_" + df1[s1].astype(str).str.strip()
        df2['key'] = df2[t2].astype(str).str.strip().str.lower() + "_" + df2[s2].astype(str).str.strip()
        
        # Đối soát
        thieu_trong_ds2 = df1[~df1['key'].isin(df2['key'])].drop(columns=['key'])
        thieu_trong_ds1 = df2[~df2['key'].isin(df1['key'])].drop(columns=['key'])
        
        st.success(f"✅ Đã đối soát xong! DS1 thiếu {len(thieu_trong_ds2)} em, DS2 thiếu {len(thieu_trong_ds1)} em.")
        
        # Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            thieu_trong_ds2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
            thieu_trong_ds1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
        
        st.download_button("📥 Tải kết quả", data=buffer, file_name="Ket_qua.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
