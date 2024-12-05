
 # TradeLens - Arbitrage Opportunity Finder

**Version**: 20.3  
**Author**: [Peter De Ceuster]  

## Overview
TradeLens is a comprehensive Python application that helps traders identify arbitrage opportunities across multiple financial markets, including cryptocurrencies and traditional stocks. It fetches historical price data, calculates potential profits based on real-time market trends, and provides a dynamic, user-friendly graphical interface for managing and visualizing arbitrage opportunities.

Key features include multi-asset scanning, real-time data fetching, and a profit visualization dashboard with pie chart displays. It is designed for experienced traders looking to automate and optimize arbitrage strategies.

---

## Key Features
- **Multi-Asset Arbitrage Scanning**: Supports a wide range of assets including cryptocurrencies (BTC, ETH, XRP) and stocks (AAPL, TSLA, AMZN, etc.).
- **Customizable Scan Types**: Choose from Small, Medium, or Full scan modes to focus on the assets most relevant to your strategy.
- **Real-Time Data Fetching**: Pulls historical price data via external APIs for up-to-date analysis.
- **Advanced Profit Calculation**: Automatically calculates profit based on the latest closing prices, providing real-world insights into potential arbitrage opportunities.
- **Profit Visualization**: Visualizes results in a table and dynamically updates pie charts to show profit distribution by asset.
- **Threaded Processing**: Efficiently runs multiple arbitrage scans in parallel using threading for faster results.
- **Logging and Alerts**: Keeps logs of identified arbitrage opportunities and allows for easy troubleshooting.
- **Modular and Expandable**: Add new assets or change scan parameters easily by modifying the code.
  
---

## Advanced Capabilities
### 1. **Profit Calculation Methodology**  
   The profit for each asset is determined by comparing the latest closing price with the price of the previous day. This allows users to track and exploit short-term price movements to make arbitrage profits.

### 2. **Real-Time Market Data Fetching**  
   TradeLens integrates with external APIs to pull market data for a variety of assets. It fetches the most recent 30 days of historical data, ensuring that the analysis is based on the latest market trends.

### 3. **Threaded Arbitrage Scanning**  
   The application runs in multiple threads, allowing for the concurrent scanning of different assets. This improves efficiency and allows users to check for arbitrage opportunities in a broader range of assets simultaneously.

### 4. **Customizable Asset List**  
   You can customize the assets you want to monitor by modifying the `self.assets` list in the code. This includes adding or removing cryptocurrency pairs and stock symbols.

### 5. **Dynamic Data Visualizations**  
   Profit data is displayed in a dynamic pie chart, with assets contributing a percentage of the total profit. The chart updates in real-time as new data is fetched and analyzed.

### 6. **Scan Modes (Small, Medium, Full)**  
   The program offers three scan modes:
   - **Small Scan**: Focuses on a select few assets (e.g., BTCUSD, ETHUSD, XRPUSD).
   - **Medium Scan**: Expands the asset pool to include additional stocks like AAPL, TSLA, and AMZN.
   - **Full Scan**: Analyzes all available assets, including major stocks, cryptocurrencies, and more.
   
 

TradeLens supports three predefined scan types, each scanning a different set of assets. Here are the assets covered by each scan type:

### 1. **Small Scan**
   Focuses on a small subset of assets, ideal for quick scans.
   - **Assets Included**:
     - BTCUSD
     - ETHUSD
     - XRPUSD

### 2. **Medium Scan**
   Expands the Small Scan set to include additional stocks and assets for a broader scan.
   - **Assets Included**:
     - BTCUSD
     - ETHUSD
     - XRPUSD
     - TQQQ
     - AAPL
     - AMZN

### 3. **Full Scan**
   Covers all available assets, providing the most comprehensive scan of both cryptocurrencies and stocks.
   - **Assets Included**:
     - BTCUSD
     - ETHUSD
     - XRPUSD
     - EURBTC
     - EURUSD
     - TSLA
     - NVDA
     - TQQQ
     - SPY
     - AAPL
     - AMZN
     - GOOGL
     - MSFT
     - FB
     - NFLX
     - BABA
     - TSM
     - AMD
     - DIS
     - BA
     - V
     - JNJ
     - WMT
     - PG
     - MA
     - XOM
     - GE
     - KO
     - PEP
     - CVX
     - UNH
     - HD
     - ORCL
     - PYPL
     - GS
     - IBM
     - CSCO
     - LMT
     - RTX
     - AMGN
     - UPS
     - MO
     - T
     - VZ
     - MCD



---

## How to Use TradeLens

### 1. **Starting the Scan**
   - Navigate to the **Assets** tab and choose the scan type (Small, Medium, or Full).
   - Click **Start Arbitrage Scan** to begin the analysis.
   - The system will fetch market data, calculate potential profits, and display the results.

### 2. **Viewing Results**
   - The **Assets** tab shows a table with the asset names and their corresponding profit potential.
   - The **Profits** tab displays cumulative profit and includes a pie chart showing the distribution of profits by asset.

### 3. **Help and Guidance**
   - The **Help/About** tab provides detailed instructions and tips for using the application, including:
     - **Understanding Arbitrage**: Explanation of arbitrage strategies and how the app helps identify such opportunities.
     - **Live Data Usage**: Information on how the app fetches and processes real-time data.
     - **Profit Calculation**: Details on how the app calculates profits based on price movements.
     - **Frequently Asked Questions (FAQs)**: Answers to common questions like how to add more assets, modify scan types, and more.

---

## How the Application Works

1. **Fetching Historical Data**:  
   The app fetches the last 30 days of historical price data for each asset using the `Financial Modeling Prep` API.

2. **Calculating Profits**:  
   Profit for each asset is calculated based on the price change between the latest closing price and the previous day's closing price.

3. **Displaying Opportunities**:  
   Arbitrage opportunities are displayed in a table format, with the asset name and its calculated profit. The table is automatically updated every 2 seconds.

4. **Visualizing Profit**:  
   A dynamic pie chart displays the distribution of profits by asset. The chart updates automatically as new data is analyzed.

---

## Help Section 
### What is Arbitrage?
Arbitrage is the practice of exploiting price differences of the same asset across different markets. TradeLens helps you monitor and identify opportunities in real-time by comparing historical data across multiple exchanges.

### How TradeLens Uses Live Data
TradeLens fetches data from external APIs like `Financial Modeling Prep` to track the price movements of assets such as BTC, ETH, and stocks over the last 30 days. It calculates potential profits based on the difference between the latest closing price and the price from the previous day.

### How the Profit Calculation Works
The app calculates potential profit for each asset by comparing its closing price today and yesterday. If there is a price difference, the app calculates the potential profit you could make if you took advantage of the price difference.



---

## Disclaimer
This application is for experienced traders and developers. Trading involves substantial risk, and you should exercise caution and consult with a financial advisor before making any investment decisions.

---

## Contact & Support
For additional help or support, visit [our website](https://peterdeceuster.uk) or contact us through [Buy Me A Coffee](https://buymeacoffee.com/siglabo) if you find the application useful.

Thank you for using TradeLens!

![Screenshot 2024-12-05 231911](https://github.com/user-attachments/assets/fed528d5-7432-441d-9673-705a0090a3a0)
![Screenshot 2024-12-05 231925](https://github.com/user-attachments/assets/9b401cb0-205f-493c-a3c8-1d5199b7dea4)
![Screenshot 2024-12-05 232301](https://github.com/user-attachments/assets/573c81ba-c40a-4b95-a39f-bc16f155737e)


(c) Peter De Ceuster 2024
Software Distribution Notice: https://peterdeceuster.uk/doc/code-terms 
This software is released under the FPA General Code License.
 
 
