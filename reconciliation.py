import pandas as pd
from difflib import SequenceMatcher

class ReconciliationEngine:
    def __init__(self, trial_balance_df, expected_accounts_df=None):
        """
        Initialize reconciliation engine
        trial_balance_df: Trial balance output from TrialBalanceProcessor
        expected_accounts_df: Chart of accounts (optional, for validation)
        """
        self.trial_balance = trial_balance_df
        self.expected_accounts = expected_accounts_df
        self.reconciliation_results = {}
        self.anomalies = []
        
    def check_balance(self):
        """Check if debits equal credits"""
        total_debit = self.trial_balance['Debit'].sum()
        total_credit = self.trial_balance['Credit'].sum()
        
        difference = abs(total_debit - total_credit)
        is_balanced = difference < 0.01
        
        return {
            'is_balanced': is_balanced,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'difference': difference,
            'status': 'PASS' if is_balanced else 'FAIL'
        }
    
    def find_missing_accounts(self):
        """Find accounts in expected chart but missing in GL"""
        if self.expected_accounts is None:
            return []
        
        gl_codes = set(self.trial_balance['Account_Code'].values)
        expected_codes = set(self.expected_accounts['Account_Code'].values)
        
        missing = expected_codes - gl_codes
        
        return list(missing)
    
    def detect_suspicious_entries(self):
        """Detect potentially problematic entries"""
        suspicious = []
        
        # Check for accounts with both debit and credit entries
        both_sides = self.trial_balance[
            (self.trial_balance['Debit'] > 0) & 
            (self.trial_balance['Credit'] > 0)
        ]
        
        for idx, row in both_sides.iterrows():
            suspicious.append({
                'Account_Code': row['Account_Code'],
                'Account_Name': row['Account_Name'],
                'Debit': row['Debit'],
                'Credit': row['Credit'],
                'Issue': 'Account has both debit and credit entries',
                'Severity': 'Medium'
            })
        
        # Check for zero-balance accounts
        zero_balance = self.trial_balance[
            (self.trial_balance['Debit'] == 0) & 
            (self.trial_balance['Credit'] == 0)
        ]
        
        for idx, row in zero_balance.iterrows():
            suspicious.append({
                'Account_Code': row['Account_Code'],
                'Account_Name': row['Account_Name'],
                'Debit': 0,
                'Credit': 0,
                'Issue': 'Zero balance account - may be inactive',
                'Severity': 'Low'
            })
        
        self.anomalies = suspicious
        return suspicious
    
    def find_round_amounts(self, threshold=1000):
        """Find suspiciously round amounts (potential manual entries)"""
        round_entries = []
        
        for idx, row in self.trial_balance.iterrows():
            if row['Debit'] > 0 and row['Debit'] % threshold == 0:
                round_entries.append({
                    'Account_Code': row['Account_Code'],
                    'Account_Name': row['Account_Name'],
                    'Amount': row['Debit'],
                    'Type': 'Debit',
                    'Note': f'Round amount ({threshold}x multiple)'
                })
            elif row['Credit'] > 0 and row['Credit'] % threshold == 0:
                round_entries.append({
                    'Account_Code': row['Account_Code'],
                    'Account_Name': row['Account_Name'],
                    'Amount': row['Credit'],
                    'Type': 'Credit',
                    'Note': f'Round amount ({threshold}x multiple)'
                })
        
        return round_entries
    
    def generate_reconciliation_report(self):
        """Generate comprehensive reconciliation report"""
        balance_check = self.check_balance()
        suspicious = self.detect_suspicious_entries()
        round_amounts = self.find_round_amounts()
        
        report = {
            'balance_status': balance_check,
            'suspicious_entries': suspicious,
            'round_amounts': round_amounts,
            'total_issues': len(suspicious) + len(round_amounts),
            'overall_status': 'READY FOR CLOSE' if balance_check['is_balanced'] and len(suspicious) < 3 else 'REVIEW NEEDED'
        }
        
        self.reconciliation_results = report
        return report
    
    def get_recommendations(self):
        """Get actionable recommendations for accountant"""
        recommendations = []
        report = self.reconciliation_results
        
        if not report['balance_status']['is_balanced']:
            recommendations.append(f"⚠️ Trial balance NOT balanced. Difference: ₹{report['balance_status']['difference']:,.2f}")
        else:
            recommendations.append("✓ Trial balance is balanced")
        
        if len(report['suspicious_entries']) > 0:
            recommendations.append(f"⚠️ {len(report['suspicious_entries'])} suspicious accounts detected - review before close")
        
        if len(report['round_amounts']) > 0:
            recommendations.append(f"ℹ️ {len(report['round_amounts'])} accounts with round amounts - may indicate manual entries")
        
        if not recommendations:
            recommendations.append("✓ All checks passed - ready for month-end close")
        
        return recommendations
