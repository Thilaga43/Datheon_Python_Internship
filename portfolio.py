import csv
import random

# Mock database of current market prices for simulation
# (In a production environment, you could use 'yfinance' or requests to an API)
CURRENT_MARKET_PRICES = {
    "AAPL": 185.50,
    "MSFT": 420.25,
    "GOOGL": 175.00,
    "AMZN": 180.75,
    "TSLA": 175.20,
    "NVDA": 900.50,
}

def get_current_price(ticker):
    """
    Looks up the current price of a ticker symbol.
    Returns a mock price with slight random fluctuation if the ticker is known,
    otherwise asks the user to provide the current price manually.
    """
    ticker = ticker.upper().strip()
    if ticker in CURRENT_MARKET_PRICES:
        # Add a tiny bit of real-time realism via minor fluctuation (-1% to +1%)
        base_price = CURRENT_MARKET_PRICES[ticker]
        fluctuation = random.uniform(-0.01, 0.01)
        return round(base_price * (1 + fluctuation), 2)
    else:
        # Fallback if the ticker isn't in our mock database
        while True:
            try:
                price = float(input(f"Enter the current market price for {ticker}: $"))
                if price >= 0:
                    return round(price, 2)
                print("Price cannot be negative.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

def main():
    # Dictionary structure to store portfolio positions:
    # { 'TICKER': {'buy_price': float, 'shares': int} }
    portfolio = {}

    print("=" * 50)
    print("      STOCK PORTFOLIO PERFORMANCE TRACKER      ")
    print("=" * 50)

    # 1. User Input Phase
    while True:
        ticker = input("\nEnter stock ticker symbol (or type 'done' to calculate): ").upper().strip()
        if ticker == 'DONE':
            if not portfolio:
                print("Your portfolio is empty. Add at least one stock first.")
                continue
            break
        
        if not ticker:
            print("Ticker symbol cannot be empty.")
            continue

        # Get share quantity
        while True:
            try:
                shares = int(input(f"Enter number of shares held for {ticker}: "))
                if shares > 0:
                    break
                print("Quantity must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        # Get buy price
        while True:
            try:
                buy_price = float(input(f"Enter your average buy price per share for {ticker}: $"))
                if buy_price > 0:
                    break
                print("Buy price must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid price.")

        # Store position in dictionary structure
        portfolio[ticker] = {
            "buy_price": buy_price,
            "shares": shares
        }
        print(f"Added {shares} shares of {ticker} at ${buy_price:.2f} each.")

    # 2. Calculation and Output Phase
    print("\n" + "=" * 65)
    print(f"{'Ticker':<10}{'Shares':<10}{'Buy Price':<12}{'Current Price':<15}{'Gain/Loss %':<12}")
    print("-" * 65)

    total_invested_capital = 0.0
    total_market_value = 0.0
    summary_rows = []

    for ticker, data in portfolio.items():
        shares = data["shares"]
        buy_price = data["buy_price"]
        current_price = get_current_price(ticker)

        # Performance math
        invested_capital = shares * buy_price
        market_value = shares * current_price
        gain_loss_pct = ((current_price - buy_price) / buy_price) * 100

        # Accumulate totals
        total_invested_capital += invested_capital
        total_market_value += market_value

        # Display performance per holding
        print(f"{ticker:<10}{shares:<10}{f'${buy_price:.2f}':<12}{f'${current_price:.2f}':<15}{gain_loss_pct:+.2f}%")

        # Collect data for CSV exporting
        summary_rows.append([ticker, shares, buy_price, current_price, round(gain_loss_pct, 2)])

    # Total performance summary calculations
    total_gain_loss_val = total_market_value - total_invested_capital
    total_gain_loss_pct = ((total_market_value - total_invested_capital) / total_invested_capital) * 100 if total_invested_capital > 0 else 0

    print("-" * 65)
    print(f"Total Invested Capital: ${total_invested_capital:.2f}")
    print(f"Total Market Value:     ${total_market_value:.2f}")
    print(f"Total Portfolio Return: ${total_gain_loss_val:+.2f} ({total_gain_loss_pct:+.2f}%)")
    print("=" * 65)

    # 3. Export to CSV Phase
    csv_filename = "portfolio_summary.csv"
    try:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write Header
            writer.writerow(["Ticker", "Shares", "Avg Buy Price", "Current Price", "Gain_Loss_Percentage"])
            
            # Write Position Rows
            writer.writerows(summary_rows)
            
            # Write blank line and Total Summary rows
            writer.writerow([])
            writer.writerow(["Total Invested Capital", total_invested_capital])
            writer.writerow(["Total Market Value", total_market_value])
            writer.writerow(["Total Portfolio Return (%)", round(total_gain_loss_pct, 2)])
            
        print(f"\n[Success] Performance logs successfully saved to '{csv_filename}'.")
    except IOError as e:
        print(f"\n[Error] Could not write summary to CSV file: {e}")

if __name__ == "__main__":
    main()
