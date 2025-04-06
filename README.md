# 项目甘特图应用

一个基于Streamlit的项目进度甘特图可视化工具。

## 功能特点

- 从CSV文件导入项目数据
- 显示任务和里程碑
- 交互式甘特图展示
- 项目概要统计
- 自动化的时间轴管理

## 在线使用

访问 Streamlit Cloud 版本：
[https://your-app-url.streamlit.app](https://your-app-url.streamlit.app)

## 本地开发

### 环境要求

- Python 3.8+
- pip (Python包管理器)

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/your-username/gantt-chart-app.git
cd gantt-chart-app
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
streamlit run app.py
```

## CSV数据格式

必需的列：
- `工作序号`: 任务编号
- `工作步骤`: 任务名称
- `开始时间`: DD/MM/YYYY格式
- `结束时间`: DD/MM/YYYY格式
- `负责人`: 任务负责人
- `备注`: Task或Milestones

参考 `sample_template.csv` 作为示例。

## Streamlit Cloud部署

1. Fork 此仓库到您的GitHub账户
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 使用GitHub账户登录
4. 点击 "New app" 并选择此仓库
5. 选择 app.py 作为入口文件
6. 点击 "Deploy!"

部署完成后，您将获得一个公开的URL，可以与团队成员共享。

## 贡献指南

1. Fork 此仓库
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License