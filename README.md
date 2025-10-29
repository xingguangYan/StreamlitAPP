
# 森林地上碳储量估算器

这是一个使用 Streamlit 开发的网页应用，用于估算森林地上碳储量。该应用提供了一个直观的界面，让用户能够通过输入基本林分参数来估算森林的碳储量。

## 功能特点

- 简单直观的用户界面
- 实时计算结果
- 支持以下参数输入：
  - 胸径(DBH)
  - 树高
  - 木材密度
  - 每公顷株数
- 计算并显示：
  - 单株生物量
  - 每公顷生物量
  - 每公顷碳储量

## 安装要求

```bash
pip install streamlit pandas numpy
```

## 使用方法

1. 克隆此仓库：
```bash
git clone https://github.com/your-username/forest-carbon-calculator.git
cd forest-carbon-calculator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
streamlit run app.py
```

## 计算方法

本应用使用改良的相对生长方程来计算生物量，并使用标准转换系数将生物量转换为碳储量。主要计算步骤包括：

- **单株生物量计算**：使用 DBH、树高和木材密度
- **每公顷生物量计算**：将单株生物量乘以每公顷株数
- **碳储量转换**：使用 0.5 的转换系数将生物量转换为碳储量

## 注意事项

- 计算结果仅供参考，实际应用中应根据具体树种和地区选择合适的方程
- 生物量转换为碳储量使用的是通用系数 0.5
- 所有计算结果单位采用国际标准单位制：
  - 生物量：Mg（兆克/吨）
  - 面积：ha（公顷）

## 未来改进计划

- 添加更多树种特定的生物量方程
- 支持批量数据处理
- 添加结果可视化功能
- 支持数据导出功能
- 添加更多参数选项

## 参考文献

- Chave et al. (2014) Improved allometric models to estimate the aboveground biomass of tropical trees
- IPCC Guidelines for National Greenhouse Gas Inventories

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

## 相关链接

- [Streamlit 文档](https://docs.streamlit.io/)
- [在线演示](https://solitary-monster-67rg47w6r7v245jp-8501.app.github.dev/)
- [项目问题反馈](https://github.com/your-username/forest-carbon-calculator/issues)

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：xingguangyan0703#gmail.com

> 注：请根据实际情况修改仓库地址、联系方式等信息。
```

主要修改内容：
1. 统一使用标准的Markdown标题格式
2. 代码块添加了语言标识，提高可读性
3. 列表项格式标准化
4. 重要内容使用粗体强调
5. 引用块用于标注说明信息
6. 链接使用标准Markdown格式
7. 整体结构层次更清晰，便于阅读
