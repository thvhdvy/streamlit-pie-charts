import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import time
import textwrap
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Cấu hình trang
st.set_page_config(
    page_title="Biểu đồ phân tích kết quả khảo sát của Anh Thư",
    page_icon="📊",
    layout="wide"
)

# CSS tạo giao diện sinh động
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        0% { opacity: 0; transform: translateX(-50px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(50px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: calc(200px + 100%) 0; }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    /* Tổng thể - nền trắng */
    .main {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 107, 107, 0.03) 0%, transparent 50%);
    }
    
    /* Đảm bảo toàn bộ app có nền trắng */
    .stApp {
        background-color: #ffffff;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 107, 107, 0.03) 0%, transparent 50%);
    }
    
    /* Container chính */
    .block-container {
        background-color: transparent !important;
        padding-top: 2rem;
    }
    
    /* Header chính với animation */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: fadeInUp 1s ease-out, float 3s ease-in-out infinite;
        background-size: 200% 200%;
        animation: fadeInUp 1s ease-out, shimmer 3s linear infinite;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out 0.3s both;
        font-weight: 400;
    }
    
    /* Card container cho từng câu hỏi với animation */
    .question-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .question-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .question-card:hover::before {
        left: 100%;
    }
    
    /* Tiêu đề câu hỏi */
    .question-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid transparent;
        background: linear-gradient(white, white) padding-box,
                   linear-gradient(135deg, #667eea, #764ba2) border-box;
        border-bottom: 3px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        position: relative;
    }
    
    /* Container cho 2 biểu đồ */
    .chart-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
    }
    
    .chart-container:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Tiêu đề giới tính với animation */
    .gender-title {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
        padding: 0.8rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .gender-title::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .gender-title:hover::before {
        left: 100%;
    }
    
    .gender-male {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        animation: slideInLeft 0.8s ease-out;
    }
    
    .gender-male:hover {
        background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(116, 185, 255, 0.4);
    }
    
    .gender-female {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        animation: slideInRight 0.8s ease-out;
    }
    
    .gender-female:hover {
        background: linear-gradient(135deg, #e84393 0%, #fd79a8 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(253, 121, 168, 0.4);
    }
    
    /* Biểu đồ với animation */
    .chart-image {
        transition: all 0.4s ease;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .chart-image:hover {
        transform: scale(1.05) rotate(1deg);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    /* Cảnh báo không có dữ liệu */
    .no-data-warning {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #f39c12;
        border-radius: 15px;
        color: #856404;
        font-weight: 500;
        animation: pulse 2s infinite;
        transition: all 0.3s ease;
    }
    
    .no-data-warning:hover {
        transform: scale(1.02);
        background: linear-gradient(135deg, #ffeaa7 0%, #fff3cd 100%);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 500;
        margin-bottom: 2rem;
        animation: slideInLeft 0.8s ease-out, pulse 2s infinite;
        box-shadow: 0 5px 15px rgba(0, 184, 148, 0.3);
        transition: all 0.3s ease;
    }
    
    .success-message:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 184, 148, 0.4);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Ẩn các element không cần thiết */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Progress bar tùy chỉnh */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
        .question-title {
            font-size: 1.1rem;
        }
        .gender-title {
            font-size: 1rem;
        }
    }
    
    /* Smooth scroll */
    html {
        scroll-behavior: smooth;
    }
    
    /* Tạo hiệu ứng ripple khi click */
    .ripple {
        position: relative;
        overflow: hidden;
        transform: translate3d(0, 0, 0);
    }
    
    .ripple:after {
        content: "";
        display: block;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
        background-repeat: no-repeat;
        background-position: 50%;
        transform: scale(10, 10);
        opacity: 0;
        transition: transform .5s, opacity 1s;
    }
    
    .ripple:active:after {
        transform: scale(0, 0);
        opacity: .2;
        transition: 0s;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript cho hiệu ứng tương tác
st.markdown("""
<script>
// Tạo hiệu ứng particles
function createParticle() {
    const particle = document.createElement('div');
    particle.style.position = 'fixed';
    particle.style.width = '4px';
    particle.style.height = '4px';
    particle.style.background = 'linear-gradient(45deg, #667eea, #764ba2)';
    particle.style.borderRadius = '50%';
    particle.style.pointerEvents = 'none';
    particle.style.zIndex = '1000';
    particle.style.opacity = '0.7';
    
    const x = Math.random() * window.innerWidth;
    const y = Math.random() * window.innerHeight;
    
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    
    document.body.appendChild(particle);
    
    // Animation
    particle.animate([
        { transform: 'translate(0, 0) scale(1)', opacity: 0.7 },
        { transform: `translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) scale(0)`, opacity: 0 }
    ], {
        duration: 3000,
        easing: 'ease-out'
    }).onfinish = () => particle.remove();
}

// Tự động tạo particles
setInterval(createParticle, 3000);
</script>
""", unsafe_allow_html=True)

# Hàm rút ngắn nhãn để tránh lộn xộn
def shorten_label(label):
    if isinstance(label, str):
        # Sử dụng textwrap để chia dòng thông minh
        if len(label) > 25:
            # Chia thành các dòng tối đa 25 ký tự mỗi dòng
            wrapped = textwrap.fill(label, width=25)
            return wrapped
    return label

# Hàm tạo biểu đồ tròn với kích thước cố định
# Thay thế toàn bộ hàm plot_pie_chart:
# Hàm vẽ biểu đồ (thay thế plot_pie_chart_plotly)
def plot_chart_plotly(data, column_name, title, gender):
    # Lọc dữ liệu theo giới tính
    filtered_data = data[data['Giới tính của bạn là gì?'] == gender][column_name].dropna()
    
    if filtered_data.empty:
        return None
    
    # Kiểm tra xem dữ liệu có phải kiểu số không
    is_numeric = pd.api.types.is_numeric_dtype(filtered_data)
    
    # Bảng màu đẹp
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#F7DC6F', '#85C1E9', '#F8C471', '#AED6F1', '#F8BBD9']
    
    # Tính toán chiều cao động dựa trên số lượng items
    num_items = len(filtered_data.value_counts()) if not is_numeric else 1
    legend_rows = (num_items + 2) // 3
    base_height = 500
    legend_height = legend_rows * 30
    total_height = base_height + legend_height + 100
    
    if is_numeric:
        # Xử lý dữ liệu số: vẽ biểu đồ cột
        value_counts = filtered_data.value_counts().sort_index()  # Sắp xếp theo giá trị số
        labels = [str(label) for label in value_counts.index]  # Chuyển đổi thành chuỗi
        values = value_counts.values
        
        # Tạo biểu đồ cột
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(
                    color=colors[:len(values)],
                    line=dict(color='white', width=2),
                ),
                text=values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Số lượng: %{y}<extra></extra>'
            )
        ])
        
        # Cấu hình layout cho biểu đồ cột
        fig.update_layout(
            title=dict(text=f"<b>{gender}</b>", x=0.5, y=0.95, font=dict(size=18, color="#0f0f0f")),
            font=dict(size=12),
            showlegend=False,  # Không cần legend cho biểu đồ cột
            xaxis=dict(
                title=None,
                tickangle=45,
                tickfont=dict(size=14, color='#0f0f0f', weight='normal'),
                titlefont=dict(size=16),
                color='#0f0f0f',
            ),
            yaxis=dict(
                title='Số lượng',
                titlefont=dict(size=16),
                tickfont=dict(size=14, color='#0f0f0f'),
                color='#0f0f0f',           
            ),
            margin=dict(l=50, r=50, t=80, b=150),
            height=total_height,
            width=650,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Tổng: {sum(values)} phản hồi",
                    x=0.5, y=-0.15,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=12, color='#6c757d')
                )
            ]
        )
    else:
        # Xử lý dữ liệu không phải số (giữ nguyên logic biểu đồ tròn)
        valid_options = [
            "Các mối quan hệ trên mạng xã hội",
            "Trong mối quan hệ với gia đình",
            "Trong các mối quan hệ với bạn bè, đồng nghiệp",
            "Trong mối quan hệ với vợ/chồng/người yêu"
        ]
        
        all_values = []
        for response in filtered_data:
            if isinstance(response, str) and column_name == "Bạn thường bắt gặp tình huống xuất hiện hành vi Silent Treatment ở đâu?":
                values = [val.strip() for val in response.split('.') if val.strip() in valid_options]
                all_values.extend(values)
            elif isinstance(response, str):
                values = [val.strip() for val in response.split('.')]
                all_values.extend(values)
            else:
                all_values.append(response)
        
        value_counts = pd.Series(all_values).value_counts()
        if value_counts.empty:
            return None
        
        labels = []
        for label in value_counts.index:
            if isinstance(label, str) and len(label) > 25:
                words = label.split()
                if len(words) > 3:
                    mid = len(words) // 2
                    line1 = ' '.join(words[:mid])
                    line2 = ' '.join(words[mid:])
                    labels.append(f"{line1}<br>{line2}")
                else:
                    labels.append(label)
            else:
                labels.append(label)
        
        sizes = value_counts.values
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=sizes,
            hole=0.1,
            marker=dict(
                colors=colors[:len(sizes)],
                line=dict(color='white', width=2)
            ),
            textfont=dict(size=20, color='black'),
            textposition='inside',
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<br>Tỷ lệ: %{percent}<extra></extra>',
            pull=[0.05 if i == 0 else 0 for i in range(len(sizes))],
            domain=dict(x=[0.1, 0.9], y=[0.3, 0.9])
        )])
        
        fig.update_layout(
            template='plotly_white',
            title=dict(text=f"<b>{gender}</b>", x=0.5, y=0.95, font=dict(size=18, color='#2c3e50')),
            font=dict(size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=14, color='#000000'),
                itemsizing="constant",
                itemwidth=30,
                tracegroupgap=10,
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0
            ),
            margin=dict(l=50, r=50, t=80, b=150),
            height=total_height,
            width=650,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Tổng: {sum(sizes)} phản hồi",
                    x=0.5, y=0.25,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=12, color='#6c757d')
                )
            ]
        )
        
        fig.update_traces(
            textfont_size=16,
            marker=dict(colors=colors[:len(sizes)], line=dict(color='white', width=3)),
            hoverinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<br>Tỷ lệ: %{percent:.1%}<extra></extra>'
        )
    
    return fig
# Header chính với animation
#st.markdown('<h1 class="main-title">📊 Phân tích Silent Treatment theo Giới tính</h1>', unsafe_allow_html=True)
#st.markdown('<p class="subtitle">✨ Dữ liệu khảo sát được phân tích và theo giới tính</p>', unsafe_allow_html=True)

# Loading animation
with st.spinner('🔄 Đang tải dữ liệu...'):
    time.sleep(0.5)  # Giả lập loading
    
    # Đọc file Excel từ repository
    try:
        df = pd.read_excel('response.xlsx', engine='openpyxl')
        #st.markdown('<div class="success-message">✅ Đã tải dữ liệu thành công từ file response.xlsx! <span class="loading-spinner"></span></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file Excel: {str(e)}")
        st.stop()

# Progress bar cho loading effect
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
progress_bar.empty()

# Lấy các cột từ cột thứ 4 trở đi
columns_to_plot = df.columns[3:].tolist()



# Hiển thị biểu đồ cho từng câu hỏi với animation delay
for i, column in enumerate(columns_to_plot, 1):
    # Thêm delay animation cho từng card
    delay = (i - 1) * 0.1
    
    # Container cho từng câu hỏi
    st.markdown(f'''
    <div class="question-card" style="animation-delay: {delay}s;">
        <div class="question-title">
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); 
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                         font-weight: bold;">Câu hỏi {i}:</span> {column}
        </div>
    ''', unsafe_allow_html=True)
    
    # Tạo 2 cột cho Nam và Nữ
    col1, col2 = st.columns(2, gap="large")
    
    # Thay thế phần hiển thị biểu đồ trong vòng lặp:
    # Biểu đồ cho Nam
    with col1:
        #st.markdown('<div class="gender-title gender-male ripple">👨 Nam giới</div>', unsafe_allow_html=True)
        
        fig_male = plot_chart_plotly(df, column, column, "Nam")
        if fig_male:
            st.plotly_chart(fig_male, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="no-data-warning">⚠️ Không có dữ liệu cho Nam giới</div>', unsafe_allow_html=True)

    # Biểu đồ cho Nữ
    with col2:
        #st.markdown('<div class="gender-title gender-female ripple">👩 Nữ giới</div>', unsafe_allow_html=True)
        
        fig_female = plot_chart_plotly(df, column, column, "Nữ")
        if fig_female:
            st.plotly_chart(fig_female, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="no-data-warning">⚠️ Không có dữ liệu cho Nữ giới</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Thêm khoảng cách giữa các câu hỏi
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

# Footer với animation
st.markdown("---")
st.markdown('''
<div style="text-align: center; margin-top: 3rem; animation: fadeInUp 1s ease-out 1s both;">
    <p style="color: #6c757d; font-size: 1rem; margin-bottom: 0.5rem;">
        📈 Dữ liệu được cập nhật tự động từ file Excel
    </p>
</div>
''', unsafe_allow_html=True)
