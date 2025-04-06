import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="项目甘特图", layout="wide")
st.title("项目进度甘特图")

# Define colors for different categories
TASK_COLORS = {
    '望春': '#1f77b4',    # Blue
    '新厂房': '#2ca02c',  # Green
    'RFID跟踪': '#ff7f0e' # Orange
}

MILESTONE_COLOR = '#d62728'  # Red for all milestones

def create_gantt_chart(df):
    fig = go.Figure()
    
    # Sort dataframe by 工作序号
    df['工作序号'] = pd.to_numeric(df['工作序号'])
    df = df.sort_values('工作序号')
    
    # Process each resource's tasks and milestones
    for resource in df['负责人'].unique():
        resource_df = df[df['负责人'] == resource]
        
        # Add tasks
        tasks = resource_df[resource_df['备注'] == 'Task']
        if not tasks.empty:
            fig.add_trace(go.Bar(
                base=tasks['开始时间'],
                x=[(end - start).total_seconds() * 1000 for start, end in zip(tasks['开始时间'], tasks['结束时间'])],
                y=[f"{row['工作序号']}. {row['工作步骤']}" for _, row in tasks.iterrows()],
                orientation='h',
                name=resource,
                marker_color=TASK_COLORS.get(resource, '#7f7f7f'),
                showlegend=True,
                legendgroup=resource,
                hovertemplate=(
                    "任务: %{y}<br>" +
                    "开始: %{base|%Y-%m-%d}<br>" +
                    "结束: %{x}<br>" +
                    f"负责人: {resource}<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Add milestones for this resource
        milestones = resource_df[resource_df['备注'] == 'Milestones']
        if not milestones.empty:
            fig.add_trace(go.Scatter(
                x=milestones['结束时间'],
                y=[f"{row['工作序号']}. {row['工作步骤']}" for _, row in milestones.iterrows()],
                mode='markers',
                name=resource,
                marker=dict(
                    symbol='diamond',
                    size=16,
                    color=MILESTONE_COLOR,
                    line=dict(color=TASK_COLORS.get(resource, '#7f7f7f'), width=2)
                ),
                showlegend=False,
                hovertemplate=(
                    "里程碑: %{y}<br>" +
                    "日期: %{x|%Y-%m-%d}<br>" +
                    f"负责人: {resource}<br>" +
                    "<extra></extra>"
                )
            ))
    
    # Update layout
    min_date = df['开始时间'].min()
    max_date = df['结束时间'].max()
    
    fig.update_layout(
        title="项目进度甘特图",
        xaxis=dict(
            title="日期",
            type='date',
            tickformat='%Y-%m-%d',
            range=[min_date, max_date]
        ),
        yaxis=dict(
            title="工作内容",
            autorange="reversed"
        ),
        height=600,
        showlegend=True,
        barmode='overlay',
        font=dict(size=12),
        hoverlabel=dict(bgcolor="white"),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            orientation="h"
        )
    )
    
    return fig

def load_and_process_csv():
    # Move file upload to sidebar
    with st.sidebar:
        st.header("数据输入")
        uploaded_file = st.file_uploader("选择CSV文件", type=['csv'])
        
    if uploaded_file is not None:
        try:
            # Read CSV with Chinese characters
            df = pd.read_csv(uploaded_file)
            
            # Convert date columns from DD/MM/YYYY to datetime
            df['开始时间'] = pd.to_datetime(df['开始时间'], format='%d/%m/%Y')
            df['结束时间'] = pd.to_datetime(df['结束时间'], format='%d/%m/%Y')
            
            # Move data display to sidebar
            with st.sidebar:
                st.subheader("项目数据")
                st.dataframe(df, height=400)
            
            # Display project summary before Gantt chart
            st.subheader("项目概要")
            col1, col2, col3 = st.columns(3)
            
            tasks_df = df[df['备注'] == 'Task']
            milestones_df = df[df['备注'] == 'Milestones']
            
            with col1:
                st.metric("总任务数", len(tasks_df))
                st.metric("里程碑数", len(milestones_df))
            
            with col2:
                st.metric("项目开始日期", df['开始时间'].min().strftime('%Y-%m-%d'))
                st.metric("项目结束日期", df['结束时间'].max().strftime('%Y-%m-%d'))
            
            with col3:
                duration = (df['结束时间'].max() - df['开始时间'].min()).days
                st.metric("项目持续时间", f"{duration} 天")
            
            # Create and display Gantt chart
            fig = create_gantt_chart(df)
            st.plotly_chart(fig, use_container_width=True)
            
            return df
            
        except Exception as e:
            st.error(f"错误: {str(e)}")
            return None
    return None

# Main app logic
data = load_and_process_csv()