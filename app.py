import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile

# حل مشكلة imghdr في النسخ الحديثة يدوياً لو لزم الأمر
try:
    import imghdr
except ImportError:
    import sys
    from types import ModuleType
    sys.modules['imghdr'] = ModuleType('imghdr')

st.title("نظام تحليل بيانات السيارات المستخدمة")

# تحميل البيانات
try:
    with zipfile.ZipFile('New_Data.zip', 'r') as zip_ref:
        zip_ref.extractall()
    df = pd.read_csv('New_Data.csv')
    st.success("تم تحميل البيانات بنجاح!")
    
    # عرض أول 5 صفوف للتأكد
    st.write(df.head())
    
    # رسم بياني بسيط للتجربة
    fig, ax = plt.subplots()
    sns.histplot(df['price'], ax=ax)
    st.pyplot(fig)

except Exception as e:
    st.error(f"حدث خطأ في تحميل الملفات: {e}")
