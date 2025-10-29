import streamlit as st
import pandas as pd
import numpy as np

st.title('森林地上碳储量估算器')

st.write("""
这个应用可以帮助你估算森林的地上碳储量。请输入以下参数进行计算。
""")

# 创建输入区域
with st.container():
    st.subheader("基本参数输入")

    col1, col2 = st.columns(2)

    with col1:
        dbh = st.number_input('胸径(DBH,cm)', 
                             min_value=1.0, 
                             max_value=300.0, 
                             value=20.0)

        height = st.number_input('树高(H,m)', 
                               min_value=1.0,
                               max_value=100.0, 
                               value=15.0)

    with col2:
        wood_density = st.number_input('木材密度(g/cm³)', 
                                     min_value=0.1,
                                     max_value=1.5,
                                     value=0.5)

        trees_per_ha = st.number_input('每公顷株数',
                                     min_value=1,
                                     max_value=10000,
                                     value=100)

# 计算函数
def calculate_biomass(dbh, height, wood_density):
    """使用改良的相对生长方程计算单株生物量"""
    # 这里使用一个简化的方程,实际应用中可以根据树种和地区选择合适的方程
    biomass = 0.0673 * (wood_density * dbh**2 * height)**0.976
    return biomass

def calculate_carbon(biomass):
    """将生物量转换为碳储量(使用转换系数0.5)"""
    return biomass * 0.5

if st.button('计算碳储量'):
    # 计算单株生物量
    biomass_per_tree = calculate_biomass(dbh, height, wood_density)

    # 计算每公顷生物量
    biomass_per_ha = biomass_per_tree * trees_per_ha

    # 计算碳储量
    carbon_per_ha = calculate_carbon(biomass_per_ha)

    # 显示结果
    st.subheader('计算结果')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="单株生物量", 
                 value=f"{biomass_per_tree:.2f} Mg")

    with col2:
        st.metric(label="每公顷生物量", 
                 value=f"{biomass_per_ha:.2f} Mg/ha")

    with col3:
        st.metric(label="每公顷碳储量", 
                 value=f"{carbon_per_ha:.2f} MgC/ha")

    # 添加说明
    st.info("""
    注意事项:
    1. 本估算使用通用方程,可能需要根据具体树种和地区进行调整
    2. 生物量转换为碳储量使用系数0.5
    3. 结果单位: Mg = 兆克(吨), ha = 公顷
    """)

# 添加页脚
st.markdown("---")
st.markdown("""
*参考文献:*
- Chave et al. (2014) Improved allometric models to estimate the aboveground biomass of tropical trees
- IPCC Guidelines for National Greenhouse Gas Inventories
""")
