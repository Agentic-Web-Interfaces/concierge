"""
Simple stock exchange server example.
Run this to start the HTTP server.
"""
from pydantic import BaseModel, Field
from concierge import State, tool, stage, workflow, construct, run_http_server


@construct()
class Stock(BaseModel):
    """Stock selection"""
    symbol: str = Field(description="Stock symbol like AAPL, GOOGL")
    quantity: int = Field(ge=1, description="Number of shares")


@stage(name="browse", prerequisites=[])
class BrowseStage:
    """Browse and search stocks"""
    
    @tool()
    def search(
        self, 
        state: State, 
        symbol: str = Field(description="Stock ticker symbol", examples=["AAPL", "GOOGL", "MSFT"])
    ) -> dict:
        """Search for a stock by ticker symbol"""
        return {
            "result": f"Found {symbol}: $150.00",
            "symbol": symbol,
            "price": 150.00
        }
    
    @tool()
    def add_to_cart(
        self, 
        state: State, 
        symbol: str = Field(description="Stock ticker symbol", examples=["AAPL", "GOOGL"]), 
        quantity: int = Field(description="Number of shares to purchase", examples=[10, 50, 100])
    ) -> dict:
        """Add stock to your cart for purchase"""
        state.set("cart", {"symbol": symbol, "quantity": quantity})
        return {"result": f"Added {quantity} shares of {symbol} to cart"}


@stage(name="transact", prerequisites=[Stock])
class TransactStage:
    """Execute stock transactions"""
    
    @tool()
    def buy(self, state: State) -> dict:
        """Buy the stock in your cart"""
        cart = state.get("cart")
        if not cart:
            return {"error": "Cart is empty"}
        
        return {
            "order_id": "ORD12345",
            "status": "completed",
            "message": f"Bought {cart['quantity']} shares of {cart['symbol']}"
        }
    
    @tool()
    def sell(
        self, 
        state: State,
        symbol: str = Field(description="Stock symbol to sell", examples=["AAPL"]),
        quantity: int = Field(description="Number of shares to sell", examples=[5, 10])
    ) -> dict:
        """Sell shares of a stock"""
        return {
            "order_id": "ORD67890",
            "status": "completed",
            "message": f"Sold {quantity} shares of {symbol}"
        }


@stage(name="portfolio", prerequisites=[])
class PortfolioStage:
    """View portfolio and holdings"""
    
    @tool()
    def view_holdings(self, state: State) -> dict:
        """View your current stock holdings"""
        return {
            "holdings": [
                {"symbol": "AAPL", "quantity": 10, "value": "$1,500.00"},
                {"symbol": "GOOGL", "quantity": 5, "value": "$700.00"}
            ],
            "total_value": "$2,200.00"
        }
    
    @tool()
    def view_profit(self, state: State) -> dict:
        """View your profit/loss summary"""
        return {
            "total_invested": "$2,000.00",
            "current_value": "$2,200.00",
            "profit": "$200.00",
            "profit_percentage": "10%"
        }


@workflow(name="stock_exchange", description="Simple stock trading workflow")
class StockWorkflow:
    """Stock exchange workflow with multiple stages"""
    
    browse = BrowseStage
    transact = TransactStage
    portfolio = PortfolioStage
    
    transitions = {
        browse: [transact, portfolio],
        transact: [portfolio, browse],
        portfolio: [browse]
    }


if __name__ == "__main__":
    # Get workflow and run HTTP server
    workflow = StockWorkflow._workflow
    run_http_server(workflow, host="localhost", port=8080)
