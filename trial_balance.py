import pandas as pd
import numpy as np
from datetime import datetime

class TrialBalanceProcessor:
    def __init__(self, gl_dataframe):
        """
        Initialize with GL export as pandas DataFrame
        Expected columns: Account_Code, Account_Name, Debit, Credit
        """
        self.gl_data = gl_dataframe.copy()
        self.trial_balance = None
        self.errors = []
        self.summary = {}
        
    def validate_data(self):
        """Validate GL data structure"""
        required_cols = ['Account_Code', 'Account_Name', 'Debit', 'Credit']
        
        for col in required_cols:
            if col not in self.gl_data.columns:
                self.errors.append(f"Missing required column: {col}")
                return False
        
        # Check for numeric columns
        try:
            self.gl_data['Debit'] = pd.to_numeric(self.gl_data['Debit'], errors='coerce')
            self.gl_data['Credit'] = pd.to_numeric(self.gl_data['Credit'], errors='coerce')
        except:
            self.errors.append("Debit and Credit columns must contain numeric values")
            return False
        
        # Replace NaN with 0
        self.gl_data['Debit'].fillna(0, inplace=True)
        self.gl_data['Credit'].fillna(0, inplace=True)
        
        return len(self.errors) == 0
    
    def generate_trial_balance(self):
        """Generate trial balance from GL data"""
        if not self.validate_data():
            return False
        
        # Group by account and sum debits/credits
        tb = self.gl_data.groupby('Account_Code', as_index=False).agg({
            'Account_Name': 'first',
            'Debit': 'sum',
            'Credit': 'sum'
        })
        
        # Calculate net balance
        tb['Net_Balance'] = tb['Debit'] - tb['Credit']
        tb['Balance_Type'] = tb['Net_Balance'].apply(
            lambda x: 'Debit' if x > 0 else ('Credit' if x < 0 else 'Nil')
        )
        tb['Absolute_Balance'] = tb['Net_Balance'].abs()
        
        # Sort by account code
        tb = tb.sort_values('Account_Code').reset_index(drop=True)
        
        self.trial_balance = tb
        
        # Calculate summary
        total_debit = tb['Debit'].sum()
        total_credit = tb['Credit'].sum()
        
        self.summary = {
            'total_debit': total_debit,
            'total_credit': total_credit,
            'difference': abs(total_debit - total_credit),
            'is_balanced': abs(total_debit - total_credit) < 0.01,
            'num_accounts': len(tb),
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return True
    
    def get_trial_balance(self):
        """Return formatted trial balance dataframe"""
        if self.trial_balance is None:
            return None
        
        display_tb = self.trial_balance[[
            'Account_Code', 'Account_Name', 'Debit', 'Credit', 'Absolute_Balance', 'Balance_Type'
        ]].copy()
        
        # Format currency columns
        for col in ['Debit', 'Credit', 'Absolute_Balance']:
            display_tb[col] = display_tb[col].apply(lambda x: f"₹{x:,.2f}")
        
        return display_tb
    
    def get_unbalanced_accounts(self, threshold=100):
        """Get accounts with unusual balances (potential errors)"""
        if self.trial_balance is None:
            return []
        
        suspicious = self.trial_balance[
            (self.trial_balance['Debit'] > 0) & 
            (self.trial_balance['Credit'] > 0)
        ].copy()
        
        return suspicious[['Account_Code', 'Account_Name', 'Debit', 'Credit']].to_dict('records')
    
    def get_summary(self):
        """Return summary statistics"""
        return self.summary
