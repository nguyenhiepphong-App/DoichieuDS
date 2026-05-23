import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Đối soát danh sách", layout="wide")
st.title("⚖️ Công cụ đối soát 2 danh sách học sinh")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Tải DS 1 (File gốc)", type=["xlsx"])
with col2:
    file2 = st.file_uploader("Tải DS 2 (File cần đối chiếu)", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # Chuẩn hóa cột làm khóa so sánh (Họ tên + Ngày sinh)
    # Lưu ý: Yêu cầu file Excel của ông phải có tên cột đúng là 'Họ tên' và 'Ngày sinh'
    df1['key'] = df1['Họ tên'].astype(str).str.strip().str.lower() + "_" + df1['Ngày sinh'].astype(str).str.strip()
    df2['key'] = df2['Họ tên'].astype(str).str.strip().str.lower() + "_" + df2['Ngày sinh'].astype(str).str.strip()
    
    # Tìm các em thiếu
    thieu_trong_ds2 = df1[~df1['key'].isin(df2['key'])].drop(columns=['key'])
    thieu_trong_ds1 = df2[~df2['key'].isin(df1['key'])].drop(columns=['key'])
    
    # Hiển thị kết quả trên web
    st.markdown("---")
    if not thieu_trong_ds2.empty:
        st.error(f"❌ Có {len(thieu_trong_ds2)} HS ở DS 1 nhưng thiếu trong DS 2")
    if not thieu_trong_ds1.empty:
        st.warning(f"⚠️ Có {len(thieu_trong_ds1)} HS ở DS 2 nhưng thiếu trong DS 1")
        
    # Nút xuất file Excel 2 sheets
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        thieu_trong_ds2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
        thieu_trong_ds1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
    
    st.download_button(
        label="📥 Tải file kết quả so sánh (.xlsx)",
        data=buffer,
        file_name="Ket_qua_doi_chieu.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")
st.markdown("Người thực hiện: **Nguyen Hiep Phong - THPT Bến Tre**")
