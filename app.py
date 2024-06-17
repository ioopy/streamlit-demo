import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(file_path):
    """Load CSV data into a pandas DataFrame."""
    return pd.read_csv(file_path)

df = load_data('data/data.csv')

def intro():
    st.write("# สวัสดี 👋")

    st.markdown(
        """
        จากแบบสำรวจทั้งหมด สามารถวิเคราะห์ข้อมูลได้ดังนี้
    """
    )

def analyze_1():
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        ประเภทการซื้อ จากแบบสำรวจ
"""
    )
    purchase_type_counts = df['ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด'].value_counts().reset_index()
    purchase_type_counts.columns = ['ประเภทการซื้อ', 'จำนวน']
    total_count = purchase_type_counts['จำนวน'].sum()
    purchase_type_counts['เปอร์เซ็นต์ (%)'] = (purchase_type_counts['จำนวน'] / total_count) * 100

    # Create a bar chart with Altair
    base_chart = alt.Chart(purchase_type_counts).mark_bar().encode(
        x=alt.X('ประเภทการซื้อ', axis=alt.Axis(title='ประเภทการซื้อ', labelAngle=0)),
        y=alt.Y('จำนวน', axis=alt.Axis(title='จำนวน')),
        tooltip=['ประเภทการซื้อ', 'จำนวน', 'เปอร์เซ็นต์ (%)']
    ).properties(
        width=600,
        height=400
    )

    # Add text labels on the bars
    text = base_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-10  # Nudges text to be above the bars
    ).encode(
        text='จำนวน:Q'
    )

    # Combine the bar chart and text layers
    layered_chart = alt.layer(base_chart, text).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(layered_chart)

def analyze_2():
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        ประเภทการซื้อ จากแบบสำรวจ
"""
    )
    df = load_data('data/processed_data.csv')
    df['ประเภทของร้านค้า'] = df['ประเภทของร้านค้า'].map({0: 'ไม่มีแบรนด์', 1: 'มีแบรนด์'})
    df['ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด'] = df['ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด'].map({0: 'ซื้อยกลัง', 1: 'ซื้อเป็นขวด'})

    # Pivot the DataFrame to have 'Purchase Type' as columns
    pivot_df = df.pivot_table(index='ประเภทของร้านค้า', columns='ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด', values='ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน / กรอกตัวเลข  *', aggfunc='sum').reset_index()

    # Melt the pivot table to long format for Altair
    melted_df = pivot_df.melt(id_vars='ประเภทของร้านค้า', var_name='ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด', value_name='ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน')

    # Create the Altair chart
    bar_chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X('ประเภทของร้านค้า:N', axis=alt.Axis(title='ประเภทของร้านค้า', labelAngle=0)),
        y=alt.Y('sum(ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน):Q', title='ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน'),
        color='ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด:N',
        tooltip=['ประเภทของร้านค้า', 'ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด', alt.Tooltip('sum(ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน):Q', format='.2f')]
    ).properties(
        width=600,
        height=400,
        title='ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน'
    )

    # Add text labels to the bars
    text = bar_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Adjust the position of the text
    ).encode(
        text=alt.Text('sum(ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน):Q', format='.2f')
    )

    # Combine the bar chart and text layers
    layered_chart = (bar_chart + text).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    # Calculate average quantity sold per day for each purchase type and group
    average_sales = df.groupby(['ประเภทของร้านค้า', 'ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด'])['ปริมาณที่ขายได้ต่อแก้วในแต่ละวัน / กรอกตัวเลข  *'].mean().reset_index()
    average_sales.columns = ['ประเภทของร้านค้า', 'ลักษณะการซื้อไซรัปของท่าน เป็นแบบใด', 'Average']

    # Display the chart in Streamlit
    st.altair_chart(layered_chart, use_container_width=True)

    # Display average sales as a table
    st.write("Average quantity sold per day for each purchase type and group:")
    st.table(average_sales)

page_names_to_funcs = {
    "บทนำ": intro,
    "การวิเคราะห์ที่ 1": analyze_1,
    "การวิเคราะห์ที่ 2": analyze_2
}

demo_name = st.sidebar.radio("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

