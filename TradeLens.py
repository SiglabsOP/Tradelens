import sys
import threading
from PyQt5 import QtWidgets, QtCore, QtGui
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
import requests
import logging

 

 

class ArbitrageOpportunityFinder:
    def __init__(self):
        self.api_key = "APIKEYHERE"  # Your real API key
        self.base_url = "https://financialmodelingprep.com/api/v3"  # Base API endpoint
        
        self.symbol_map = {
            "BTCUSD": "/historical-price-full/BTCUSD",
            "ETHUSD": "/historical-price-full/ETHUSD",
            "XRPUSD": "/historical-price-full/XRPUSD",
            "EURBTC": "/historical-price-full/EURBTC",
            "EURUSD": "/historical-price-full/EURUSD",
            "TSLA": "/historical-price-full/TSLA",
            "NVDA": "/historical-price-full/NVDA",
            "TQQQ": "/historical-price-full/TQQQ",
            "SPY": "/historical-price-full/SPY",
            "AAPL": "/historical-price-full/AAPL",
            "AMZN": "/historical-price-full/AMZN",
            "GOOGL": "/historical-price-full/GOOGL",
            "MSFT": "/historical-price-full/MSFT",
            "FB": "/historical-price-full/FB",
            "NFLX": "/historical-price-full/NFLX",
            "NVDA": "/historical-price-full/NVDA",
            "BABA": "/historical-price-full/BABA",
            "TSM": "/historical-price-full/TSM",
            "AMD": "/historical-price-full/AMD",
            "DIS": "/historical-price-full/DIS",
            "BA": "/historical-price-full/BA",
            "V": "/historical-price-full/V",
            "JNJ": "/historical-price-full/JNJ",
            "WMT": "/historical-price-full/WMT",
            "PG": "/historical-price-full/PG",
            "MA": "/historical-price-full/MA",
            "XOM": "/historical-price-full/XOM",
            "GE": "/historical-price-full/GE",
            "KO": "/historical-price-full/KO",
            "PEP": "/historical-price-full/PEP",
            "CVX": "/historical-price-full/CVX",
            "UNH": "/historical-price-full/UNH",
            "HD": "/historical-price-full/HD",
            "ORCL": "/historical-price-full/ORCL",
            "PYPL": "/historical-price-full/PYPL",
            "GS": "/historical-price-full/GS",
            "IBM": "/historical-price-full/IBM",
            "CSCO": "/historical-price-full/CSCO",
            "LMT": "/historical-price-full/LMT",
            "RTX": "/historical-price-full/RTX",
            "AMGN": "/historical-price-full/AMGN",
            "BA": "/historical-price-full/BA",
            "UPS": "/historical-price-full/UPS",
            "MO": "/historical-price-full/MO",
            "T": "/historical-price-full/T",
            "VZ": "/historical-price-full/VZ",
            "MCD": "/historical-price-full/MCD",
            "PEP": "/historical-price-full/PEP",
            "KO": "/historical-price-full/KO"
        }

        self.assets = ["BTCUSD", "ETHUSD", "XRPUSD", "EURBTC", "EURUSD", "TSLA", "NVDA", "TQQQ", "SPY", "AAPL", "AMZN", "GOOGL", "MSFT", "FB", "NFLX", "BABA", "TSM", "AMD", "DIS", "BA", "V", "JNJ", "WMT", "PG", "MA", "XOM", "GE", "KO", "PEP", "CVX", "UNH", "HD", "ORCL", "PYPL", "GS", "IBM", "CSCO", "LMT", "RTX", "AMGN", "UPS", "MO", "T", "VZ", "MCD"]

        self.arbitrage_data = []
        self.lock = threading.Lock()  # Ensure thread safety


    def fetch_historical_data(self, asset):
        endpoint = self.symbol_map.get(asset)
        if not endpoint:
            print(f"No endpoint found for asset {asset}")
            return None

        url = f"{self.base_url}{endpoint}?apikey={self.api_key}&timeseries=30"  # Fetch last 30 days of data
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful
            data = response.json()
            if isinstance(data, dict) and 'historical' in data:
                return data['historical']  # List of historical prices
        except Exception as e:
            print(f"Error fetching historical data for {asset}: {e}")
            return None

    def calculate_profit(self, historical_data):
        # Example: Calculate profit based on the difference between the latest closing price and the previous day's closing price
        if not historical_data or len(historical_data) < 2:
            return 0

        latest_price = historical_data[0]['close']
        previous_price = historical_data[1]['close']
        
        # Profit as the price change
        profit = latest_price - previous_price
        return profit
        
        
    def get_scan_assets(self, scan_type):
        # Define the subsets of assets for small, medium, and full scans
        small_scan_assets = ["BTCUSD", "ETHUSD", "XRPUSD"]
        medium_scan_assets = ["BTCUSD", "ETHUSD", "XRPUSD", "TQQQ", "AAPL", "AMZN"]
        full_scan_assets = self.assets  # All assets in the list
    
        if scan_type == "Small Scan":
            return small_scan_assets
        elif scan_type == "Medium Scan":
            return medium_scan_assets
        else:  # Full Scan
            return full_scan_assets

            

    def analyze_arbitrage(self, asset):
        historical_data = self.fetch_historical_data(asset)
        if historical_data is None:
            return  # Skip if no historical data was fetched

        # Calculate profit based on historical price change
        profit = self.calculate_profit(historical_data)

        # Lock the arbitrage data while accessing it to ensure thread safety
        with self.lock:  # Ensure thread-safe access to the shared resource
            if profit != 0:
                self.arbitrage_data.append({"asset": asset, "profit": profit})
                print(f"Arbitrage opportunity for {asset}: Profit = {profit:.2f}")
                self.logger.info(f"Arbitrage opportunity for {asset}: Profit = {profit:.2f}")


    def check_arbitrage(self, scan_type):
        assets_to_check = self.get_scan_assets(scan_type)
        for asset in assets_to_check:
            self.analyze_arbitrage(asset)

    def start_thread(self, scan_type):
        assets_to_check = self.get_scan_assets(scan_type)
        threading.Thread(target=self.check_arbitrage, args=(assets_to_check,), daemon=True).start()


        # Setting up the logging configuration
        logging.basicConfig(
            filename='arbitrage_opportunities.log',  # Log file path
            level=logging.INFO,  # Set logging level (INFO, DEBUG, etc.)
            format='%(asctime)s - %(message)s',  # Format: Timestamp - Log Message
            datefmt='%Y-%m-%d %H:%M:%S'  # Date format for timestamp
        )
        self.logger = logging.getLogger()    



class ArbitrageGUI(QtWidgets.QMainWindow):
    def __init__(self, arbitrage_finder):
        super().__init__()
        self.arbitrage_finder = arbitrage_finder
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TradeLens v20.3")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
 
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Create tabs
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #457b9d; }
            QTabBar::tab { background: #1d3557; color: white; padding: 10px; }
            QTabBar::tab:selected { background: #457b9d; }
            QTabBar::tab:hover { background: #a8dadc; }
        """)

        self.assets_tab = self.create_assets_tab()
        self.profits_tab = self.create_profits_tab()
        self.help_tab = self.create_help_tab()

        self.tabs.addTab(self.assets_tab, "Assets")
        self.tabs.addTab(self.profits_tab, "Profits")
        self.tabs.addTab(self.help_tab, "Help/About")

        self.layout.addWidget(self.tabs)
        
 

            

    def create_assets_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
    
        title = QtWidgets.QLabel("Monitor Arbitrage Opportunities")
        title.setFont(QtGui.QFont("Arial", 18))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
    
        # Add scan selection options
        self.scan_type_combo = QtWidgets.QComboBox()
        self.scan_type_combo.addItem("Small Scan")
        self.scan_type_combo.addItem("Medium Scan")
        self.scan_type_combo.addItem("Full Scan")
        layout.addWidget(self.scan_type_combo)
    
        start_button = QtWidgets.QPushButton("Start Arbitrage Scan")
        start_button.setStyleSheet("background-color: #457b9d; color: white; font-size: 18px;")
        start_button.clicked.connect(self.start_arbitrage)
        layout.addWidget(start_button, alignment=QtCore.Qt.AlignCenter)
    
        self.assets_table = QtWidgets.QTableWidget()
        self.assets_table.setColumnCount(2)
        self.assets_table.setHorizontalHeaderLabels(["Asset", "Profit"])
        self.assets_table.setStyleSheet("""
            background-color: #f1faee; 
            color: #1d3557; 
            border: 1px solid #457b9d;
            font-size: 16px;
        """)
        self.assets_table.horizontalHeader().setStyleSheet("""
            background-color: #457b9d; 
            color: black; 
            font-size: 18px;
        """)
        layout.addWidget(self.assets_table)
    
        return tab
    def create_profits_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
    
        title = QtWidgets.QLabel("Current Profits Overview")
        title.setFont(QtGui.QFont("Arial", 18))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
    
        self.profit_label = QtWidgets.QLabel("Total Profit: $0.00")
        self.profit_label.setFont(QtGui.QFont("Arial", 16))
        self.profit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.profit_label.setStyleSheet("color: #1d3557; font-weight: bold;")
        layout.addWidget(self.profit_label)
    
        self.graph_canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.graph_canvas)
    
        # Message label that shows when no data is available for the pie chart
        self.pie_message_label = QtWidgets.QLabel("Pie chart will be displayed here when data is available.")
        self.pie_message_label.setFont(QtGui.QFont("Arial", 14))
        self.pie_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pie_message_label.setStyleSheet("color: #1d3557; font-style: italic;")
        layout.addWidget(self.pie_message_label)
    
        return tab

    def create_help_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
    
        help_text = """
        <h1 style="color: #457b9d;">TradeLens Help Guide</h1>
        <p>Welcome to TradeLens, a comprehensive platform for monitoring arbitrage opportunities in classical and cryptocurrency trading. This guide provides detailed instructions, tips, and resources to help you use the application effectively.</p>
    
        <h2 style="color: #457b9d;">What is Arbitrage?</h2>
        <p>Arbitrage is the practice of exploiting price differences for the same asset across different markets or exchanges. For example, buying Bitcoin at a lower price on one exchange and selling it at a higher price on another can yield a profit. TradeLens helps you identify these opportunities in real-time.</p>
    
        <h2 style="color: #457b9d;">How TradeLens Uses Live Data</h2>
        <p>TradeLens uses real-time data to monitor standard market and cryptocurrency prices and identify arbitrage opportunities. The platform fetches historical price data from external APIs, such as Financial Modeling Prep, to track the price movements of assets like BTC, ETH, and XRP over the past 30 days.</p>
        <p>The system then calculates potential profits based on the price changes from the most recent historical data. Results are logged. The calculations consider the difference between the latest closing price and the previous day's closing price. This process ensures that the analysis reflects actual market trends and not simulated data. We do not use indicators here, since we use the python trading bot for such strategies. You can find the bot at our GITHUB depository.</p>
    
        <h2 style="color: #457b9d;">How the Profit Calculation Works</h2>
        <p>The profit for each asset is calculated by comparing its most recent closing price with the price from the previous day. The difference between these two prices is considered the potential profit. For example, if the closing price of BTC on day 1 is $20,000 and the closing price on day 2 is $21,000, the profit is $1,000.</p>
    
        <h2 style="color: #457b9d;">How to Use TradeLens</h2>
        <ol style="font-size: 16px;">
            <li><b>Starting the Scan:</b> Go to the <b>Assets</b> tab and click "Start Arbitrage Scan." The system will begin monitoring and displaying opportunities.</li>
            <li><b>Understanding the Results:</b> The "Assets" tab shows real-time results in a table with two columns:
                <ul>
                    <li><b>Asset:</b> The currency pair being monitored (e.g., BTCUSD).</li>
                    <li><b>Profit:</b> The estimated profit in USD for a potential arbitrage opportunity.</li>
                </ul>
            </li>
            <li><b>Viewing Cumulative Profits:</b> Navigate to the <b>Profits</b> tab to see the total profits from all opportunities analyzed so far.</li>
            <li><b>Getting Help:</b> Refer to this tab anytime for detailed guidance.</li>
        </ol>
    
        <h2 style="color: #457b9d;">Features</h2>
        <ul style="font-size: 16px;">
            
            <li><b>Visual Data Representation:</b> Displays opportunities in a clear and concise table, with additional graphing capabilities.</li>
            <li><b>Customizable Assets:</b> Add or modify the list of currency pairs in the code to suit your needs.</li>
        </ul>
    
        <h2 style="color: #457b9d;">Understanding Transaction Costs</h2>
        <p>When engaging in arbitrage, remember to account for transaction fees, withdrawal fees, and deposit times. TradeLens includes a basic cost deduction in its profit calculation, but additional fees may apply based on your exchanges.</p>
    
        <h2 style="color: #457b9d;">Frequently Asked Questions (FAQs)</h2>
    <dl style="font-size: 16px;">
        <dt><b>Q: Can I add more currency pairs?</b></dt>
        <dd>A: Yes, you can edit the <code>self.assets</code> list in the code to include more pairs. You can also modify the predefined scan types to suit your needs.</dd>
        
        <dt><b>Q: What are the predefined scan types?</b></dt>
        <dd>
            The application provides three predefined scan types:
            <ul>
                <li><b>Small Scan:</b> Monitors a focused set of assets, including <code>BTCUSD</code>, <code>ETHUSD</code>, and <code>XRPUSD</code>.</li>
                <li><b>Medium Scan:</b> Includes the assets from Small Scan and adds <code>TQQQ</code>, <code>AAPL</code>, and <code>AMZN</code>.</li>
                <li><b>Full Scan:</b> Covers all available assets, including cryptocurrencies and stocks:
                    <code>BTCUSD, ETHUSD, XRPUSD, EURBTC, EURUSD, TSLA, NVDA, TQQQ, SPY, AAPL, AMZN, GOOGL, MSFT, FB, NFLX, BABA, TSM, AMD, DIS, BA, V, JNJ, WMT, PG, MA, XOM, GE, KO, PEP, CVX, UNH, HD, ORCL, PYPL, GS, IBM, CSCO, LMT, RTX, AMGN, UPS, MO, T, VZ, MCD</code>.
                </li>
            </ul>
        </dd>
    </dl>
    
        <h2 style="color: #457b9d;">Tips for Successful Arbitrage</h2>
        <ul style="font-size: 16px;">
            <li>Choose exchanges with low fees and fast processing times.</li>
            <li>Monitor market trends and stay updated on currency news.</li>
            <li>Start with small amounts to test the feasibility of your strategy.</li>
        </ul>
    
        <h2 style="color: #457b9d;">Disclaimer</h2>
        <p>This application is intended for expert purposes only. Currency trading involves significant risk, and you should exercise caution and consult a financial expert before making any investment decisions.</p>
    
        <h2 style="color: #457b9d;">Contact and Support</h2>
        <p>For further assistance, visit <a href="https://peterdeceuster.uk/" style="color: #457b9d;">our website</a><b>..Thank you!</b></p>
        <p>If you enjoy using this application, consider <a href="https://buymeacoffee.com/siglabo" style="color: #457b9d;">buying me a coffee</a>.</p>
        """
        help_label = QtWidgets.QLabel(help_text)
        help_label.setTextFormat(QtCore.Qt.RichText)
        help_label.setOpenExternalLinks(True)
        help_label.setStyleSheet("font-size: 18px; color: #1d3557;")
        help_label.setAlignment(QtCore.Qt.AlignTop)
    
        layout.addWidget(help_label)
        return tab

    def start_arbitrage(self):
        scan_type = self.scan_type_combo.currentText()  # Get the selected scan type
        self.arbitrage_finder.start_thread(scan_type)  # Start the thread with the scan type
        QtWidgets.QMessageBox.information(self, "Scan Started", f"{scan_type} initiated. Results will appear shortly.")
        
        

    def update_table(self):
        # Fetch the current scan type
        scan_type = self.scan_type_combo.currentText()
        assets_to_check = self.arbitrage_finder.get_scan_assets(scan_type)
        
        # Filter the arbitrage data for the current scan type
        with self.arbitrage_finder.lock:
            data = pd.DataFrame(self.arbitrage_finder.arbitrage_data)
        
        if not data.empty:
            # Filter data for the selected scan type
            data = data[data['asset'].isin(assets_to_check)]
            
            if not data.empty:
                self.assets_table.setRowCount(len(data))
                total_profit = 0
                asset_profits = {}
                
                for i, row in data.iterrows():
                    asset = row["asset"]
                    profit = row["profit"]
                    
                    self.assets_table.setItem(i, 0, QtWidgets.QTableWidgetItem(asset))
                    self.assets_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"${profit:.2f}"))
                    
                    total_profit += profit
                    asset_profits[asset] = asset_profits.get(asset, 0) + profit
                
                self.profit_label.setText(f"Total Profit: ${total_profit:.2f}")
                self.update_pie_chart(asset_profits)
            else:
                # Clear the table if no data matches the selected scan type
                self.assets_table.setRowCount(0)
                self.profit_label.setText("Total Profit: $0.00")
                self.update_pie_chart({})
        else:
            # Handle the case when arbitrage_data is empty
            self.assets_table.setRowCount(0)
            self.profit_label.setText("Total Profit: $0.00")
            self.update_pie_chart({})

    def update_pie_chart(self, asset_profits):
        figure = self.graph_canvas.figure
        figure.clear()
    
        ax = figure.add_subplot(111)  # Regular 2D Axes for the pie chart
    
        # Remove zero values from the asset_profits
        asset_profits = {k: v for k, v in asset_profits.items() if v > 0}
    
        if not asset_profits:  # Check if the asset_profits dictionary is empty after removing zeros
            # Show message
            ax.text(
                0.5, 0.5, 
                "Pie chart will be displayed here when data is available.", 
                horizontalalignment="center", 
                verticalalignment="center", 
                fontsize=16, 
                color="#1d3557", 
                transform=ax.transAxes  # Ensure the text uses the axes coordinate system
            )
            ax.set_xticks([])  # Remove X-axis ticks
            ax.set_yticks([])  # Remove Y-axis ticks
            ax.set_frame_on(False)  # Hide the axes frame
            self.pie_message_label.setVisible(True)  # Show message label
        else:
            # Hide message label
            self.pie_message_label.setVisible(False)
    
            # Set a threshold for small profits (e.g., 2% of the total)
            threshold = 0.02
    
            # Calculate the total sum of profits
            total = sum(asset_profits.values())
    
            # Create a new dictionary where small profits are combined into "Others"
            asset_profits_combined = {}
            others_profit = 0
            for label, profit in asset_profits.items():
                if profit / total < threshold:
                    others_profit += profit
                else:
                    asset_profits_combined[label] = profit
    
            # If there were small profits, add them as a single "Others" slice
            if others_profit > 0:
                asset_profits_combined['Others'] = others_profit
    
            # Recalculate sizes, labels
            sizes = [max(profit, 0) for profit in asset_profits_combined.values()]
            labels = list(asset_profits_combined.keys())
    
            # Adjust the explode parameter dynamically for better visuals
            explode = [0.1 if size > threshold * total else 0 for size in sizes]
    
            # Pie chart logic
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",  # Display percentage on the chart
                startangle=140,
                explode=explode,
                colors=plt.cm.Paired.colors,  # Color palette
                pctdistance=0.85  # Adjust distance of text from center
            )
    
            # Styling the pie chart labels
            for text in texts:
                text.set_color("#1d3557")
                text.set_fontsize(14)
    
            # Styling the percentage text inside the chart
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(12)
                autotext.set_fontweight("bold")
    
            # Set the title of the pie chart
            ax.set_title("Profit Distribution by Asset", fontsize=18, color="#457b9d")
    
        # Ensure the chart remains circular
        ax.axis('equal')
    
        # Redraw the canvas to update the chart
        self.graph_canvas.draw()

if __name__ == "__main__":
    arbitrage_finder = ArbitrageOpportunityFinder()
    app = QtWidgets.QApplication(sys.argv)
    gui = ArbitrageGUI(arbitrage_finder)

    timer = QtCore.QTimer()
    timer.timeout.connect(gui.update_table)
    timer.start(2000)
 
    gui.showMaximized()  # Start the window maximized
    sys.exit(app.exec_())
