import streamlit as st

st.set_page_config(page_title='个人简历生成器', page_icon='🎓',layout='wide')

st.title("个人简历生成器")
st.text("使用Streamlit创建您的个性化简历")

c1,c2= st.columns([1,2])

with c1:
    st.markdown("### 个人信息表单")
    st.text_input("姓名", value='name')
    st.text_input("职位", value='人工智能')
    st.text_input("电话", value='phone')
    st.text_input("邮箱", value='email')
    st.text_input("出生日期", value='2004/10/08')
    st.radio("性别", ["男", "女", "其他"], index=0)
    st.selectbox("学历", ["本科", "硕士", "博士等"], index=0)
    st.multiselect("语言能力", ["中文", "英语", "其他"], default=["中文", "英语"])
    st.multiselect("技能", ["Java", "c++", "机器学习", "Python", "其他"], default=["Java", "c++", "机器学习", "Python"])
    st.slider("工作经验（年）", min_value=0, max_value=10, value=4)
    st.write(f"**期望薪资**：{"13132 - 29898元"}")
    st.text_area("个人简介", value='无')

with c2:
    st.markdown("### 简历实时预览")
    st.markdown(f"# {'name'}")
    st.write(f"**职位**：{'人工智能'}")
    st.write(f"**性别**：{'男'}")
    st.write(f"**学历**：{'本科'}")
    st.write(f"**工作经验**：{'4年'}")
    st.write(f"**期望薪资**：{'13132 - 29898元'}")
    st.write(f"**最佳联系时间**：{'20.30'}")
    st.write(f"**语言能力**：{'中文,英文'}")
    st.write(f"**电话**：{'phone'}")
    st.write(f"**邮箱**：{'email'}")
    st.write(f"**出生日期**：{'2004/10/08'}")
    st.markdown("### 个人简介")
    st.write('无')
    st.markdown("### 专业技能")
    st.write("Java", "c++", "机器学习", "Python")