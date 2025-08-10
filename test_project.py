import pytest
import pandas as pd
from project import get_amount, get_date, CSV

@pytest.fixture
def test_csv():
    """Fixture to set up and tear down test CSV file"""
    test_file = "test_finance_data.csv"
    CSV.CSV_FILE = test_file
    CSV.initialize_csv()
    yield test_file
    import os
    if os.path.exists(test_file):
        os.remove(test_file)

def test_amount_validation():
    """Test amount validation with valid and invalid inputs"""
    # Test valid amount
    assert get_amount(test_input="100.50") == 100.50
    assert get_amount(test_input="1000") == 1000.00
    
    # Test invalid amounts
    with pytest.raises(ValueError):
        get_amount(test_input="0")  # Zero not allowed
    
    with pytest.raises(ValueError):
        get_amount(test_input="abc")  # Non-numeric input

def test_date_validation():
    """Test date input validation"""
    # Test valid dates
    assert get_date(test_input="10-08-2025", allow_default=False) == "10-08-2025"
    assert get_date(test_input="01-01-2025", allow_default=False) == "01-01-2025"
    
    # Test invalid date format
    with pytest.raises(ValueError):
        get_date(test_input="2025-08-10", allow_default=False)  # Wrong format
    
    with pytest.raises(ValueError):
        get_date(test_input="32-13-2025", allow_default=False)  # Invalid day/month

def test_basic_transaction(test_csv):
    """Test adding and retrieving a simple transaction"""
    # Add a test transaction
    CSV.add_entry(
        date="10-08-2025",
        amount=1000.00,
        category_type="Income",
        subcategory="Salary",
        description="Test salary"
    )
    
    # Read and verify the transaction
    df = pd.read_csv(test_csv)
    assert len(df) == 1
    transaction = df.iloc[0]
    assert transaction["date"] == "10-08-2025"
    assert transaction["amount"] == 1000.00
    assert transaction["category"] == "Income"
    assert transaction["subcategory"] == "Salary"
    assert transaction["description"] == "Test salary"
