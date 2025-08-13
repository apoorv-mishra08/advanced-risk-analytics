# 📊 Value-at-Risk (VaR) Calculator

## 🎯 Project Overview
A sophisticated **quantitative risk management application** that calculates **Value-at-Risk (VaR)** for investment portfolios using multiple statistical methodologies.  
This professional-grade tool helps investors, portfolio managers, and financial analysts **quantify potential losses** their portfolios might face under normal market conditions — with institutional accuracy.

---

## 🔍 What is Value-at-Risk (VaR)?
Imagine you have ₹100,000 invested in stocks. VaR answers the question:  

> *"What's the maximum amount I might lose in the next 20 days if the market behaves normally?"*

If your VaR is ₹5,000, it means there’s only a 5% chance you’ll lose **more than ₹5,000** in those 20 days.

**Definition:**  
VaR is a statistical risk measure that quantifies the potential loss in value of a portfolio over a defined period for a given confidence interval.  
It represents the threshold value such that the probability of portfolio loss exceeding this value is small (typically **1% or 5%**).

---

## 🚀 Key Features

### **Core VaR Methods**
- 📊 **Historical Simulation VaR** – Uses actual past returns to predict future risk.  
- 📐 **Parametric VaR** – Uses mathematical models assuming normal distribution.  
- 🎲 **Monte Carlo VaR** – Runs thousands of simulations to estimate risk.  

### **Advanced Analytics**
- **Component VaR** – Shows which assets contribute most to portfolio risk.  
- **Risk Decomposition** – Visual breakdown of risk sources.  
- **Correlation Analysis** – How assets move together.  
- **Performance Metrics** – Sharpe ratio, volatility, maximum drawdown.  

### **Professional Features**
- **Real-time Data** – Live feeds via Yahoo Finance API.  
- **Interactive Visualizations** – Dynamic charts & graphs.  
- **Multiple Weighting Schemes** – Equal weight, market cap, risk parity.  
- **Bootstrap Enhancement** – Improved accuracy through resampling.  

---

## 🏗️ Technical Architecture

main.py # Main Streamlit application
portfolio_manager.py # Portfolio construction & data management

risk_calculator.py # Core VaR calculation engine

visualization.py # Advanced plotting capabilities

data_handler.py # Data processing & validation

conf.toml # Application configuration

requirements.txt # Python dependencies


---

## 📚 Financial Concepts Explained

| Term             | Simple Explanation | Expert Definition |
|------------------|-------------------|-------------------|
| **Portfolio**    | Your collection of stocks | A collection of investments held by an individual/institution |
| **Returns**      | Profit or loss made | Gain/loss over a period as a percentage |
| **Volatility**   | How much prices jump | Statistical measure of return dispersion |
| **Correlation**  | How two stocks move together | Statistical relationship between securities |
| **Confidence Level** | How sure we are about a prediction | Degree of certainty in a statistical conclusion |
| **Rolling Window** | Last X days of data | Moving subset of data for analysis |

---

## 🛠 Installation & Quick Start

### **Prerequisites**
- Python **3.8+**
- `pip` package manager
- Internet connection (for live data)

---

### **One-Command Setup**
```bash
git clone https://github.com/yourusername/var-calculator.git
cd var-calculator
pip install -r requirements.txt
streamlit run main.py


# Step 1: Clone the repository
git clone https://github.com/yourusername/var-calculator.git

# Step 2: Navigate to project directory
cd var-calculator

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the application
streamlit run main.py

Optional Docker Setup

docker build -t var-calculator .
docker run -p 8501:8501 var-calculator


📖 Usage Guide
Basic Usage (Beginner)
Enter Stock Symbols – Example: AAPL MSFT GOOG TSLA

Set Date Range – Select start and end dates.

Configure Parameters:

Rolling Window: e.g., 20 (monthly), 60 (quarterly)

Confidence Level: e.g., 95% or 99%

Portfolio Value: Total investment amount

Click “Calculate VaR” – Instant risk assessment.

Advanced Usage (Professional)

from portfolio_manager import PortfolioManager
from risk_calculator import RiskCalculator

# Create portfolio
portfolio = PortfolioManager(
    ['AAPL', 'MSFT', 'GOOG'],
    start_date='2020-01-01',
    end_date='2024-01-01',
    portfolio_value=1_000_000
)

# Calculate risk metrics
risk_calc = RiskCalculator(portfolio, confidence_level=0.95, time_horizon=20)
results = risk_calc.calculate_all_var_methods()


📊 Understanding the Results
Historical VaR – Based on actual past performance.

Parametric VaR – Based on mathematical assumptions.

Monte Carlo VaR – Based on thousands of random simulations.

Key Metrics

Sharpe Ratio – Higher is better.

Maximum Drawdown – Largest peak-to-trough loss.

Volatility – Annualized standard deviation.

🔧 Technical Implementation
Data Pipeline

Data Acquisition (Yahoo Finance API)

Data Validation (missing value checks)

Return Calculation (log returns)

Risk Modeling (multiple VaR methods)

Visualization (Plotly charts)

Key Algorithms

EWMA (Exponentially Weighted Moving Average)

Bootstrap Sampling

Component VaR

Monte Carlo Simulation


[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

# for .env file

YAHOO_FINANCE_API_KEY=your_key_here
DEFAULT_CONFIDENCE_LEVEL=0.95
MAX_PORTFOLIO_SIZE=50
CACHE_EXPIRY_HOURS=6


### **Development Setup**

git clone https://github.com/yourusername/var-calculator.git
cd var-calculator

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements-dev.txt
pre-commit install

