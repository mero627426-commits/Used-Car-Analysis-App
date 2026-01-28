import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile

# إعدادات الصفحة
st.set_page_config(page_title="Used Car Analyst", layout="wide")

# دالة لتحميل البيانات
@st.cache_data
def load_data():
    try:
        with zipfile.ZipFile('New_Data.zip', 'r') as zip_ref:
            zip_ref.extractall()
        df = pd.read_csv('New_Data.csv')
        # تنظيف بسيط للبيانات
        df['year'] = df['year'].astype(int)
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return None

df = load_data()

if df is not None:
    st.title("🚗 نظام تحليل بيانات السيارات المستخدمة")
    st.markdown("---")

    # --- القائمة الجانبية (Side Bar) ---
    st.sidebar.header("🔍 فلاتر البحث")
    
    manufacturer = st.sidebar.multiselect("اختر الشركة المصنعة:", options=df['manufacturer'].unique())
    condition = st.sidebar.multiselect("حالة السيارة:", options=df['condition'].unique())
    price_range = st.sidebar.slider("نطاق السعر ($):", 
                                    min_value=int(df['price'].min()), 
                                    max_value=int(df['price'].max()), 
                                    value=(5000, 50000))

    # تطبيق الفلاتر
    mask = df['price'].between(*price_range)
    if manufacturer:
        mask &= df['manufacturer'].isin(manufacturer)
    if condition:
        mask &= df['condition'].isin(condition)
    
    filtered_df = df[mask]

    # --- القسم الأول: الإحصائيات السريعة (KPIs) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("عدد السيارات المتاحة", len(filtered_df))
    with col2:
        st.metric("متوسط السعر", f"${filtered_df['price'].mean():,.0f}")
    with col3:
        st.metric("أعلى سعر موجود", f"${filtered_df['price'].max():,.0f}")

    st.markdown("---")

    # --- القسم الثاني: الرسوم البيانية ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 توزيع الأسعار")
        fig, ax = plt.subplots()
        sns.histplot(filtered_df['price'], kde=True, ax=ax, color='skyblue')
        st.pyplot(fig)

    with col_chart2:
        st.subheader("📈 الحالة مقابل السعر")
        fig2, ax2 = plt.subplots()
        sns.boxplot(x='condition', y='price', data=filtered_df, ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # --- القسم الثالث: عرض الجدول ---
    st.markdown("---")
    st.subheader("📋 بيانات السيارات التفصيلية")
    st.write(f"عرض {len(filtered_df)} نتيجة مطابقة لبحثك:")
    
    # عرض الجدول بشكل تفاعلي
    st.dataframe(filtered_df, use_container_width=True)

    # زر تحميل البيانات المفلترة
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 تحميل البيانات المفلترة (CSV)",
        data=csv,
        file_name='filtered_car_data.csv',
        mime='text/csv',
    )
