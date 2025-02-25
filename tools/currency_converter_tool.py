from typing import Any, Optional
from smolagents.tools import Tool
import os
import requests

class ConvertCurrencyTool(Tool):
    name = "convert_currency"
    description = "Converts an amount between currencies for travel budgeting."
    inputs = {
        'amount': {'type': 'number', 'description': 'The amount to convert'},
        'from_currency': {'type': 'string', 'description': 'Source currency code (e.g., USD, EUR)'},
        'to_currency': {'type': 'string', 'description': 'Target currency code (e.g., JPY, GBP)'}
    }
    output_type = "string"

    def __init__(self, api_key=None):
        super().__init__()
        # You can set an API key for a real currency API
        self.api_key = api_key or os.environ.get("EXCHANGE_RATE_API_KEY")
        
        # Common exchange rates (as of early 2025, for demo/fallback purposes)
        self.exchange_rates = {
            "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 149.50, "CAD": 1.35, "AUD": 1.52, "CNY": 7.20, "INR": 83.20, "MXN": 17.05},
            "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 163.00, "CAD": 1.47, "AUD": 1.66, "CNY": 7.85, "INR": 90.70, "MXN": 18.60},
            "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 189.30, "CAD": 1.71, "AUD": 1.92, "CNY": 9.10, "INR": 105.30, "MXN": 21.60},
            "JPY": {"USD": 0.0067, "EUR": 0.0061, "GBP": 0.0053, "CAD": 0.0090, "AUD": 0.0102, "CNY": 0.0482, "INR": 0.5565, "MXN": 0.1141},
            "CAD": {"USD": 0.74, "EUR": 0.68, "GBP": 0.58, "JPY": 110.70, "AUD": 1.13, "CNY": 5.33, "INR": 61.60, "MXN": 12.60},
            "AUD": {"USD": 0.66, "EUR": 0.60, "GBP": 0.52, "JPY": 98.40, "CAD": 0.89, "CNY": 4.73, "INR": 54.70, "MXN": 11.20},
            "CNY": {"USD": 0.14, "EUR": 0.13, "GBP": 0.11, "JPY": 20.80, "CAD": 0.19, "AUD": 0.21, "INR": 11.60, "MXN": 2.37},
            "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095, "JPY": 1.80, "CAD": 0.016, "AUD": 0.018, "CNY": 0.086, "MXN": 0.205},
            "MXN": {"USD": 0.059, "EUR": 0.054, "GBP": 0.046, "JPY": 8.77, "CAD": 0.079, "AUD": 0.089, "CNY": 0.422, "INR": 4.88}
        }

    def forward(self, amount: float, from_currency: str, to_currency: str) -> str:
        try:
            # Normalize currency codes
            from_currency = from_currency.upper().strip()
            to_currency = to_currency.upper().strip()
            
            # Try to use a real currency API if the API key is available
            if self.api_key:
                try:
                    url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency}/{to_currency}/{amount}"
                    response = requests.get(url)
                    data = response.json()
                    
                    if data.get('result') == 'success':
                        converted_amount = data.get('conversion_result')
                        rate = data.get('conversion_rate')
                        
                        return f"💱 {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}\n\nExchange rate: 1 {from_currency} = {rate} {to_currency}\n\n(Data from ExchangeRate-API)"
                    else:
                        # Fall back to stored rates if API call fails
                        return self._convert_with_stored_rates(amount, from_currency, to_currency)
                
                except Exception:
                    # Fall back to stored rates if any error occurs
                    return self._convert_with_stored_rates(amount, from_currency, to_currency)
            
            # If no API key is available, use the stored rates
            return self._convert_with_stored_rates(amount, from_currency, to_currency)
        
        except Exception as e:
            return f"Error converting currency: {str(e)}"
    
    def _convert_with_stored_rates(self, amount: float, from_currency: str, to_currency: str) -> str:
        # Validate currencies
        if from_currency not in self.exchange_rates:
            return f"Sorry, I don't have exchange rate data for {from_currency}."
        
        # If same currency, return original amount
        if from_currency == to_currency:
            return f"{amount} {from_currency} = {amount} {to_currency}"
        
        # Direct conversion
        if to_currency in self.exchange_rates[from_currency]:
            rate = self.exchange_rates[from_currency][to_currency]
            converted_amount = amount * rate
            return f"💱 {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}\n\nExchange rate: 1 {from_currency} = {rate} {to_currency}\n\n(Note: Rates are approximations for planning purposes only)"
        
        # Try conversion through USD
        if to_currency in self.exchange_rates and "USD" in self.exchange_rates[from_currency]:
            usd_amount = amount * self.exchange_rates[from_currency]["USD"]
            rate_to_target = self.exchange_rates["USD"].get(to_currency)
            
            if rate_to_target:
                converted_amount = usd_amount * rate_to_target
                effective_rate = converted_amount / amount
                return f"💱 {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}\n\nExchange rate: 1 {from_currency} = {effective_rate:.4f} {to_currency}\n\n(Note: Rates are approximations for planning purposes only)"
        
        return f"Sorry, I don't have exchange rate data from {from_currency} to {to_currency}."
