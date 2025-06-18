import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def get_dataframe_from_excel():
    """从Excel读取数据并处理时间列"""
    try:
        df = pd.read_excel('supermarket_sales.xlsx', 
                           sheet_name='销售数据', 
                           skiprows=1, 
                           index_col='订单号')
        
        # 处理时间列并填充缺失值
        df['小时数'] = pd.to_datetime(df['时间'], format="%H:%M:%S").dt.hour
        
        # 填充数值列的缺失值
        numeric_cols = ['总价', '评分']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
                
        return df
    except Exception as e:
        st.error(f"读取Excel文件时出错: {e}")
        st.stop()

def add_sidebar_func(df):
    """创建侧边栏筛选功能"""
    with st.sidebar:
        st.header("请筛选数据：")
        
        # 获取唯一值并处理空值
        city_unique = df["城市"].unique() if "城市" in df.columns else []
        customer_type_unique = df["顾客类型"].unique() if "顾客类型" in df.columns else []
        gender_unique = df["性别"].unique() if "性别" in df.columns else []
        
        # 设置默认选中所有选项
        city = st.multiselect(
            "请选择城市：",
            options=city_unique,
            default=city_unique if city_unique.size > 0 else []
        )
        
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_unique,
            default=customer_type_unique if customer_type_unique.size > 0 else []
        )
        
        gender = st.multiselect(
            "请选择性别",
            options=gender_unique,
            default=gender_unique if gender_unique.size > 0 else []
        )
        
        # 处理空筛选条件
        if not city:
            city = city_unique.tolist() if city_unique.size > 0 else []
        if not customer_type:
            customer_type = customer_type_unique.tolist() if customer_type_unique.size > 0 else []
        if not gender:
            gender = gender_unique.tolist() if gender_unique.size > 0 else []
        
        # 执行筛选
        try:
            df_selection = df.query(
                "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
            )
        except Exception as e:
            st.sidebar.error(f"筛选数据时出错: {e}")
            df_selection = pd.DataFrame()
            
        return df_selection

def product_line_chart(df):
    """生成按产品类型划分的销售额图表"""
    if df.empty or "产品类型" not in df.columns or "总价" not in df.columns:
        return px.bar(title="无有效数据生成图表")
    
    sales_by_product_line = df.groupby(by=["产品类型"])["总价"].sum().sort_values(ascending=True)
    fig_product_sales = px.bar(
        sales_by_product_line, 
        x="总价",
        y=sales_by_product_line.index, 
        orientation="h", 
        title="<b>按产品类型划分的销售额</b>",
    )
    return fig_product_sales

def hour_chart(df):
    """生成按小时划分的销售额图表"""
    if df.empty or "小时数" not in df.columns or "总价" not in df.columns:
        return px.bar(title="无有效数据生成图表")
    
    sales_by_hour = df.groupby(by=["小时数"])["总价"].sum()
    fig_hour_sales = px.bar(
        sales_by_hour, 
        x=sales_by_hour.index, 
        y="总价",
        title="<b>按小时数划分的销售额</b>",
    )
    return fig_hour_sales

def main_page_demo(df):
    """主界面函数，显示关键指标和图表"""
    if df.empty:
        st.warning("没有找到匹配的数据，请调整筛选条件")
        return
    
    # 设置标题
    st.title(' :bar_chart: 销售仪表板')
    
    # 创建关键指标信息区
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    
    # 计算关键指标并处理可能的NaN值
    total_sales = int(np.nan_to_num(df["总价"].sum(), nan=0))
    average_rating = round(np.nan_to_num(df["评分"].mean(), nan=0), 1)
    
    # 处理星级评分
    try:
        star_rating_string = ":star:" * int(round(average_rating, 0))
    except:
        star_rating_string = ":star:" * 0
        
    average_sale_by_transaction = round(np.nan_to_num(df["总价"].mean(), nan=0), 2)
    
    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")
    
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating_string}")
    
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")
    
    st.divider()  # 生成水平分割线
    
    # 创建图表信息区
    left_chart_col, right_chart_col = st.columns(2)
    
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    """启动应用程序"""
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    
    # 读取数据
    sale_df = get_dataframe_from_excel()
    
    # 筛选数据
    df_selection = add_sidebar_func(sale_df)
    
    # 显示主界面
    main_page_demo(df_selection)

if __name__ == "__main__":
    run_app()