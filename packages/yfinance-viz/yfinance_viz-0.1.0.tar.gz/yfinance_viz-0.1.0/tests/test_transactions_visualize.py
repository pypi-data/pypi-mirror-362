"""
Tests for the transactions visualization module.
"""

import pytest
import pandas as pd
import tempfile
import os
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add yfinance_viz module to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from yfinance_viz.transactions_visualize import PortfolioFlowTracker, Position, FundSource


@pytest.fixture
def temp_resources_dir():
    """Create a temporary directory for test resources."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestPortfolioFlowTracker:
    """Test cases for PortfolioFlowTracker class."""
    
    def test_initialization(self):
        """Test that the tracker initializes correctly."""
        tracker = PortfolioFlowTracker("/test/resources")
        assert tracker.node_labels == ["Initial Cash"]
        assert len(tracker.node_colors) == 1
        assert len(tracker.positions) == 0
        assert len(tracker.available_funds) == 0
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_get_stock_currency(self, mock_read_csv, mock_exists):
        """Test currency detection for stocks."""
        tracker = PortfolioFlowTracker("/test/resources")
        mock_exists.return_value = True
        
        # Mock CSV data with USD currency
        mock_df = pd.DataFrame({'Currency': ['USD']})
        mock_read_csv.return_value = mock_df
        
        # Test with a known stock
        currency = tracker._get_stock_currency("MSFT")
        assert currency == "USD"
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_get_stock_currency_with_cache(self, mock_read_csv, mock_exists):
        """Test currency detection with caching."""
        tracker = PortfolioFlowTracker("/test/resources")
        mock_exists.return_value = True
        
        # Mock CSV data with USD currency
        mock_df = pd.DataFrame({'Currency': ['USD']})
        mock_read_csv.return_value = mock_df
        
        # First call should populate cache
        currency1 = tracker._get_stock_currency("MSFT")
        # Second call should use cache
        currency2 = tracker._get_stock_currency("MSFT")
        assert currency1 == currency2
        assert "MSFT" in tracker.currency_cache
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_get_stock_currency_with_file(self, mock_read_csv, mock_exists):
        """Test currency detection when stock file exists."""
        tracker = PortfolioFlowTracker("/test/resources")
        mock_exists.return_value = True
        
        # Mock CSV data with currency
        mock_df = pd.DataFrame({'Currency': ['EUR']})
        mock_read_csv.return_value = mock_df
        
        currency = tracker._get_stock_currency("ASML")
        assert currency == "EUR"
    
    @patch('os.path.exists')
    def test_get_stock_currency_file_not_found(self, mock_exists):
        """Test currency detection when stock file doesn't exist."""
        tracker = PortfolioFlowTracker("/test/resources")
        mock_exists.return_value = False
        
        currency = tracker._get_stock_currency("UNKNOWN")
        assert currency == "USD"  # Default fallback
    
    @patch('os.path.exists')
    @patch('pandas.read_csv')
    def test_get_stock_currency_exception_handling(self, mock_read_csv, mock_exists):
        """Test currency detection with exception handling."""
        tracker = PortfolioFlowTracker("/test/resources")
        mock_exists.return_value = True
        mock_read_csv.side_effect = Exception("File read error")
        
        currency = tracker._get_stock_currency("ERROR")
        assert currency == "USD"  # Default fallback
    
    def test_convert_to_usd(self):
        """Test currency conversion to USD."""
        tracker = PortfolioFlowTracker("/test/resources")
        date = datetime(2020, 1, 1)
        
        # Test USD to USD (no conversion)
        result = tracker._to_usd(100.0, "USD", date)
        assert result == 100.0
        
        # Test EUR to USD (with mocked exchange rates)
        # Add a test exchange rate
        date_str = date.strftime('%Y-%m-%d')
        tracker.exchange_rates[date_str] = 1.15
        tracker.sorted_rate_keys = [date_str]
        
        result = tracker._to_usd(100.0, "EUR", date)
        assert result == pytest.approx(115.0)  # 100 EUR * 1.15 = 115 USD
        assert isinstance(result, float)
    
    def test_eur_to_usd_with_exact_rate(self):
        """Test EUR to USD conversion with exact rate."""
        tracker = PortfolioFlowTracker("/test/resources")
        date = datetime(2020, 1, 1)
        date_str = date.strftime('%Y-%m-%d')
        
        # Add a test rate
        tracker.exchange_rates[date_str] = 1.15
        
        result = tracker._eur_to_usd(100.0, date)
        assert result == pytest.approx(115.0)
    
    def test_eur_to_usd_with_nearest_rate(self):
        """Test EUR to USD conversion with nearest rate."""
        tracker = PortfolioFlowTracker("/test/resources")
        date = datetime(2020, 1, 1)
        
        # Add some test rates
        tracker.exchange_rates = {
            '2019-12-31': 1.10,
            '2020-01-02': 1.20
        }
        tracker.sorted_rate_keys = ['2019-12-31', '2020-01-02']
        
        result = tracker._eur_to_usd(100.0, date)
        assert result > 0  # Should find nearest rate
    
    def test_eur_to_usd_no_rates_available(self):
        """Test EUR to USD conversion when no rates are available."""
        tracker = PortfolioFlowTracker("/test/resources")
        tracker.exchange_rates = {}
        tracker.sorted_rate_keys = []
        date = datetime(2020, 1, 1)
        
        with pytest.raises(ValueError, match="No exchange rates available"):
            tracker._eur_to_usd(100.0, date)
    
    def test_add_node(self):
        """Test node addition."""
        tracker = PortfolioFlowTracker("/test/resources")
        node_idx = tracker._add_node("AAPL")
        assert node_idx == 1  # After Initial Cash
        assert "AAPL" in tracker.node_labels
        assert len(tracker.node_colors) == 2
    
    def test_add_node_duplicate(self):
        """Test adding the same node twice."""
        tracker = PortfolioFlowTracker("/test/resources")
        node_idx1 = tracker._add_node("AAPL")
        node_idx2 = tracker._add_node("AAPL")
        assert node_idx1 == node_idx2
        assert tracker.node_labels.count("AAPL") == 1
    
    def test_get_node_color(self):
        """Test node color assignment."""
        tracker = PortfolioFlowTracker("/test/resources")
        idx1 = tracker._add_node("AAPL")
        idx2 = tracker._add_node("MSFT")
        color1 = tracker.node_colors[idx1]
        color2 = tracker.node_colors[idx2]
        assert isinstance(color1, str)
        assert isinstance(color2, str)
        assert color1 in tracker.node_colors
        assert color2 in tracker.node_colors
    
    def test_process_sell_transaction(self):
        """Test sell transaction processing."""
        tracker = PortfolioFlowTracker("/test/resources")
        transaction = pd.Series({
            'symbol': 'AAPL',
            'quantity': 10.0,
            'price': 150.0,
            'date': '2020-01-01',
            'source': 'Funds'
        })
        usd_value = tracker._process_sell_transaction(transaction)
        assert usd_value == 1500.0
        assert len(tracker.available_funds) == 1
        assert tracker.available_funds[0].source_type == 'sell'
    
    def test_process_sell_transaction_with_existing_position(self):
        """Test sell transaction when position already exists."""
        tracker = PortfolioFlowTracker("/test/resources")
        
        # Add existing position
        tracker.positions['AAPL'] = Position('AAPL', 20.0, 'USD', 3000.0)
        
        transaction = pd.Series({
            'symbol': 'AAPL',
            'quantity': 10.0,
            'price': 150.0,
            'date': '2020-01-01',
            'source': 'Funds'
        })
        usd_value = tracker._process_sell_transaction(transaction)
        
        assert usd_value == 1500.0
        assert tracker.positions['AAPL'].quantity == 10.0  # 20 - 10
    
    def test_process_sell_transaction_remove_position(self):
        """Test sell transaction that removes entire position."""
        tracker = PortfolioFlowTracker("/test/resources")
        
        # Add existing position
        tracker.positions['AAPL'] = Position('AAPL', 10.0, 'USD', 1500.0)
        
        transaction = pd.Series({
            'symbol': 'AAPL',
            'quantity': 10.0,
            'price': 150.0,
            'date': '2020-01-01',
            'source': 'Funds'
        })
        usd_value = tracker._process_sell_transaction(transaction)
        
        assert usd_value == 1500.0
        assert 'AAPL' not in tracker.positions  # Position should be removed
    
    def test_process_buy_transaction(self):
        """Test buy transaction processing."""
        tracker = PortfolioFlowTracker("/test/resources")
        transaction = pd.Series({
            'symbol': 'AAPL',
            'quantity': 10.0,
            'price': 150.0,
            'date': '2020-01-01',
            'source': 'Funds'
        })
        usd_value = tracker._process_buy_transaction(transaction)
        assert usd_value == 1500.0
        assert 'AAPL' in tracker.positions
        assert tracker.positions['AAPL'].quantity == 10.0
    
    def test_process_buy_transaction_existing_position(self):
        """Test buy transaction when position already exists."""
        tracker = PortfolioFlowTracker("/test/resources")
        
        # Add existing position
        tracker.positions['AAPL'] = Position('AAPL', 5.0, 'USD', 750.0)
        
        transaction = pd.Series({
            'symbol': 'AAPL',
            'quantity': 10.0,
            'price': 150.0,
            'date': '2020-01-01',
            'source': 'Funds'
        })
        usd_value = tracker._process_buy_transaction(transaction)
        
        assert usd_value == 1500.0
        assert tracker.positions['AAPL'].quantity == 15.0  # 5 + 10
        assert tracker.positions['AAPL'].total_value == 2250.0  # 750 + 1500
    
    def test_process_employment_transaction(self):
        """Test employment transaction processing."""
        tracker = PortfolioFlowTracker("/test/resources")
        transaction = pd.Series({
            'symbol': 'WDAY',
            'quantity': 100.0,
            'price': 200.0,
            'date': '2020-01-01',
            'source': 'RSU'
        })
        usd_value = tracker._process_employment_transaction(transaction)
        assert usd_value == 20000.0
        assert len(tracker.available_funds) == 1
        assert tracker.available_funds[0].source_type == 'rsu'
        assert 'WDAY' in tracker.positions
        assert tracker.positions['WDAY'].quantity == 100.0
    
    def test_allocate_funds(self):
        """Test fund allocation."""
        tracker = PortfolioFlowTracker("/test/resources")
        # Add some available funds
        fund1 = FundSource('sell', 'AAPL', 1000.0, datetime(2020, 1, 1), 0)
        fund2 = FundSource('sell', 'MSFT', 500.0, datetime(2020, 1, 2), 1)
        tracker.available_funds = [fund1, fund2]
        
        allocations = tracker._allocate_funds(1200.0, 'GOOGL', datetime(2020, 1, 3))
        assert len(allocations) == 2  # AAPL and MSFT (no Initial Cash needed)
        assert allocations[0][1] == 1000.0  # AAPL amount
        assert allocations[1][1] == 200.0   # Part of MSFT amount
    
    def test_allocate_funds_with_initial_cash(self):
        """Test fund allocation when initial cash is needed."""
        tracker = PortfolioFlowTracker("/test/resources")
        # Add some available funds
        fund1 = FundSource('sell', 'AAPL', 500.0, datetime(2020, 1, 1), 0)
        tracker.available_funds = [fund1]
        
        allocations = tracker._allocate_funds(1000.0, 'GOOGL', datetime(2020, 1, 2))
        assert len(allocations) == 2  # AAPL and Initial Cash
        assert allocations[0][1] == 500.0   # AAPL amount
        assert allocations[1][1] == 500.0   # Initial Cash amount
    
    def test_allocate_funds_no_available_funds(self):
        """Test fund allocation when no funds are available."""
        tracker = PortfolioFlowTracker("/test/resources")
        tracker.available_funds = []
        
        allocations = tracker._allocate_funds(1000.0, 'GOOGL', datetime(2020, 1, 1))
        assert len(allocations) == 1  # Only Initial Cash
        assert allocations[0][1] == 1000.0  # All from Initial Cash
    
    def test_create_sankey_diagram(self):
        """Test Sankey diagram creation."""
        tracker = PortfolioFlowTracker("/test/resources")
        # Add some test data
        tracker.node_labels = ["Initial Cash", "AAPL", "MSFT"]
        tracker.node_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
        tracker.flow_data = [
            {'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'},
            {'source': 1, 'target': 2, 'value': 500.0, 'date': '2020-01-02'}
        ]
        
        # Create diagram
        fig = tracker.create_sankey_diagram()
        
        # Check that it's a Plotly figure
        assert hasattr(fig, 'data')
        assert fig.data is not None
        # Check that it contains Sankey data
        assert any('sankey' in str(d).lower() for d in fig.data)
    
    def test_create_sankey_diagram_with_title(self):
        """Test Sankey diagram creation with custom title."""
        tracker = PortfolioFlowTracker("/test/resources")
        tracker.node_labels = ["Initial Cash", "AAPL"]
        tracker.node_colors = ["#1f77b4", "#ff7f0e"]
        tracker.flow_data = [{'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'}]
        
        fig = tracker.create_sankey_diagram("Custom Title")
        
        assert hasattr(fig, 'layout')
        assert fig.layout.title.text == "Custom Title"
    
    def test_save_diagram(self):
        """Test diagram saving."""
        tracker = PortfolioFlowTracker("/test/resources")
        # Add minimal test data
        tracker.node_labels = ["Initial Cash", "AAPL"]
        tracker.node_colors = ["#1f77b4", "#ff7f0e"]
        tracker.flow_data = [{'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'}]
        
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
            filename = tmp.name
        
        try:
            tracker.save_diagram(filename)
            assert os.path.exists(filename)
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'sankey' in content.lower()
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_show_diagram(self):
        """Test diagram display."""
        tracker = PortfolioFlowTracker("/test/resources")
        tracker.node_labels = ["Initial Cash", "AAPL"]
        tracker.node_colors = ["#1f77b4", "#ff7f0e"]
        tracker.flow_data = [{'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'}]
        
        # This should not raise an exception
        tracker.show_diagram()
    
    def test_calculate_current_holdings_value(self, temp_resources_dir):
        """Test current holdings value calculation."""
        tracker = PortfolioFlowTracker(resources_path=temp_resources_dir)
        
        # Create a mock stock file for AAPL
        stock_data = pd.DataFrame({
            'Close': [150.0, 155.0, 160.0],
            'Stock Splits': [0, 0, 0],
            'Currency': ['USD', 'USD', 'USD']
        })
        stock_file = os.path.join(temp_resources_dir, 'AAPL.csv')
        stock_data.to_csv(stock_file, index=False)
        
        # Add some positions
        tracker.positions['AAPL'] = Position('AAPL', 10.0, 'USD', 1500.0)
        tracker.positions['MSFT'] = Position('MSFT', 5.0, 'USD', 1000.0)
        # Add to node_labels so the method can find it
        tracker.node_labels = ["Initial Cash", "AAPL", "MSFT"]
        # Add to flow_data to simulate activity
        tracker.flow_data = [
            {'source': 0, 'target': 1, 'value': 1500.0, 'date': '2020-01-01'}
        ]
        value, count = tracker._calculate_current_holdings_value('AAPL')
        assert value == 1600.0  # 10 shares * 160.0 (latest price)
        assert count == 10.0
    
    def test_calculate_current_holdings_value_not_found(self):
        """Test current holdings value calculation for non-existent position."""
        tracker = PortfolioFlowTracker("/test/resources")
        
        value, count = tracker._calculate_current_holdings_value('UNKNOWN')
        assert value == 0.0
        assert count == 0
    
    def test_calculate_if_held_value(self, temp_resources_dir):
        """Test if-held value calculation."""
        tracker = PortfolioFlowTracker(resources_path=temp_resources_dir)
        # Create a mock transactions.csv file
        transactions_data = pd.DataFrame({
            'transaction': ['buy', 'sell'],
            'symbol': ['AAPL', 'AAPL'],
            'date': ['2020-01-01', '2020-02-01'],
            'quantity': [10, 5],
            'price': [100, 110],
            'source': ['Funds', 'Funds']
        })
        transactions_file = os.path.join(temp_resources_dir, 'transactions.csv')
        transactions_data.to_csv(transactions_file, index=False)
        # Create a mock stock file for AAPL
        stock_data = pd.DataFrame({
            'Close': [150.0, 155.0, 160.0],
            'Stock Splits': [0, 0, 0],
            'Currency': ['USD', 'USD', 'USD']
        })
        stock_file = os.path.join(temp_resources_dir, 'AAPL.csv')
        stock_data.to_csv(stock_file, index=False)
        tracker.flow_data = [
            {'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'},
            {'source': 1, 'target': 2, 'value': 500.0, 'date': '2020-01-02'}
        ]
        tracker.node_labels = ["Initial Cash", "AAPL", "MSFT"]
        tracker.positions['AAPL'] = Position('AAPL', 10.0, 'USD', 1500.0)
        value, count = tracker._calculate_if_held_value('AAPL')
        assert value == 1600.0  # 10 shares * 160.0 (latest price)
        assert count == 10
    
    def test_calculate_total_sales(self, temp_resources_dir):
        """Test total sales calculation."""
        tracker = PortfolioFlowTracker(resources_path=temp_resources_dir)
        # Create a mock transactions.csv file
        transactions_data = pd.DataFrame({
            'transaction': ['buy', 'sell'],
            'symbol': ['AAPL', 'AAPL'],
            'date': ['2020-01-01', '2020-02-01'],
            'quantity': [10, 5],
            'price': [100, 110],
            'source': ['Funds', 'Funds']
        })
        transactions_file = os.path.join(temp_resources_dir, 'transactions.csv')
        transactions_data.to_csv(transactions_file, index=False)
        # Create a mock stock file for AAPL
        stock_data = pd.DataFrame({
            'Close': [150.0, 155.0, 160.0],
            'Stock Splits': [0, 0, 0],
            'Currency': ['USD', 'USD', 'USD']
        })
        stock_file = os.path.join(temp_resources_dir, 'AAPL.csv')
        stock_data.to_csv(stock_file, index=False)
        tracker.flow_data = [
            {'source': 1, 'target': 0, 'value': 500.0, 'date': '2020-01-02'},  # Sale
            {'source': 0, 'target': 1, 'value': 1000.0, 'date': '2020-01-01'},  # Buy
        ]
        tracker.node_labels = ["Initial Cash", "AAPL"]
        tracker.positions['AAPL'] = Position('AAPL', 10.0, 'USD', 1500.0)
        total_sales = tracker._calculate_total_sales('AAPL')
        assert total_sales == 550.0
    
    def test_is_source_node(self):
        """Test source node identification."""
        tracker = PortfolioFlowTracker("/test/resources")
        
        assert tracker._is_source_node("Initial Cash") == True
        assert tracker._is_source_node("RSU Compensation") == True
        assert tracker._is_source_node("AAPL") == False


def test_integration(temp_resources_dir):
    """Integration test with sample data."""
    tracker = PortfolioFlowTracker(resources_path=temp_resources_dir)
    
    # Create sample transactions
    transactions_data = [
        {'transaction': 'buy', 'symbol': 'AAPL', 'date': '2020-01-01', 'quantity': 10, 'price': 150, 'source': 'Funds'},
        {'transaction': 'sell', 'symbol': 'AAPL', 'date': '2020-02-01', 'quantity': 5, 'price': 160, 'source': 'Funds'},
        {'transaction': 'buy', 'symbol': 'MSFT', 'date': '2020-03-01', 'quantity': 8, 'price': 200, 'source': 'Funds'},
        {'transaction': 'buy', 'symbol': 'WDAY', 'date': '2020-04-01', 'quantity': 50, 'price': 180, 'source': 'RSU'},
    ]
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        df = pd.DataFrame(transactions_data)
        df.to_csv(tmp.name, index=False)
        filename = tmp.name
    
    try:
        # Process transactions
        tracker.process_transactions(filename)
        
        # Check results
        assert len(tracker.node_labels) > 1
        assert len(tracker.flow_data) > 0
        assert 'AAPL' in tracker.positions
        assert 'MSFT' in tracker.positions
        assert 'WDAY' in tracker.positions
        
        # Check that RSU transaction was processed correctly
        rsu_flows = [f for f in tracker.flow_data if 'RSU Compensation' in [tracker.node_labels[f['source']], tracker.node_labels[f['target']]]]
        assert len(rsu_flows) > 0
        
    finally:
        if os.path.exists(filename):
            os.unlink(filename)


@patch('yfinance_viz.transactions_visualize.PortfolioFlowTracker')
def test_main_function(mock_tracker_class):
    """Test the main function."""
    mock_tracker = MagicMock()
    mock_tracker_class.return_value = mock_tracker
    # Ensure process_transactions returns a non-empty list and node_labels and flow_data are not empty
    mock_tracker.process_transactions.return_value = [1]
    mock_tracker.node_labels = ["Initial Cash", "AAPL"]
    mock_tracker.flow_data = [1]
    from yfinance_viz.transactions_visualize import main
    main("/test/resources")
    mock_tracker_class.assert_called_once_with("/test/resources")
    mock_tracker.process_transactions.assert_called_once()
    mock_tracker.save_diagram.assert_called_once()
    # Do not assert create_sankey_diagram, as it is called inside save_diagram


if __name__ == "__main__":
    pytest.main([__file__]) 