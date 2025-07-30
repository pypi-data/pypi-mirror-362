# Robot KPI Metrics

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Robot Framework](https://img.shields.io/badge/Robot%20Framework-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Custom HTML KPI report (dashboard view) by parsing Robot Framework output.xml file.

## 🌟 About the Project

`Robot KPI Metrics` is a custom tool designed to generate comprehensive `HTML KPI reports` from Robot Framework's `output.xml` files. These reports provide a dashboard view with KPI-focused insights into your test executions, including suite statistics, test case results, and keyword performance.

### 🎯 Features

- **Custom KPI HTML Report**: Create visually appealing and informative KPI dashboard
- **Detailed KPI Metrics**: Access suite, test case, keyword statistics, status, and elapsed time
- **Support for RF7**: Fully compatible with Robot Framework 7
- **Command-Line Interface**: Easy-to-use CLI for KPI report generation
- **Interactive Dashboard**: Charts and graphs for better visualization

### 🛠️ Tech Stack

- **Python**: Core programming language
- **Robot Framework**: Test automation framework
- **Jinja2**: Template engine for HTML reports
- **Pandas**: Data manipulation and analysis
- **Bootstrap**: Frontend framework for responsive design
- **ApexCharts**: Interactive charts and graphs

## 🧰 Getting Started

### ⚙️ Installation

Install `robot-kpi-metrics` using pip:

```bash
pip install robot-kpi-metrics
```

Or install from source:

```bash
git clone <your-repo-url>
cd robot-kpi-metrics
pip install .
```

## 👀 Usage

After executing your Robot Framework tests, you can generate a KPI metrics report by running:

### Default Configuration
If `output.xml` is in the current directory:

```bash
robot-kpi-metrics
```

### Custom Path
If `output.xml` is located in a different directory:

```bash
robot-kpi-metrics --inputpath ./Result/ --output output1.xml
```

### Additional Options

```bash
robot-kpi-metrics --help
```

Available options:
- `--inputpath` or `-I`: Path of result files
- `--output` or `-O`: Name of output.xml file
- `--metrics-report-name` or `-M`: Output name of the generated KPI metrics report
- `--showkwtimes` or `-skt`: Display keyword times in KPI metrics report (default: True)
- `--showtags` or `-t`: Display test case tags in test metrics (default: False)
- `--showdocs` or `-d`: Display test case documentation in test metrics (default: False)
- `--log` or `-L`: Name of log.html file
- `--ignorelib`: Ignore keywords of specified library in report
- `--ignoretype`: Ignore keywords of specified type in report

### Example Usage

```bash
# Generate KPI report with custom name and show tags
robot-kpi-metrics --metrics-report-name my-kpi-report.html --showtags True

# Generate report from specific path with keyword times disabled
robot-kpi-metrics --inputpath ./test-results/ --showkwtimes False
```

## 📊 KPI Dashboard Features

The generated KPI report includes:

1. **Dashboard Overview**:
   - Test execution status (Pass/Fail/Skip) with pie charts
   - Suite status overview
   - Keyword execution statistics
   - Execution duration metrics

2. **Suite KPI Metrics**:
   - Suite-wise test results
   - Interactive table with filtering and sorting
   - Export options (CSV, Excel, Print)

3. **Test KPI Metrics**:
   - Individual test case results
   - Execution times and status
   - Test messages and tags (optional)

4. **Keyword Times KPI**:
   - Keyword execution statistics
   - Min/Max/Average execution times
   - Failure counts

5. **Detailed Analysis**:
   - Failed test case details
   - Keyword failure analysis
   - Suite-wise breakdown

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

This package is based on the original [robotframework-metrics](https://github.com/adiralashiva8/robotframework-metrics) project by Shiva Prasad Adirala. We've extended it with KPI-focused features and customizations.

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

⭐ **Star this repository if you find it useful!**
