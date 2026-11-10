#!/usr/bin/env python3
"""
AI MSME Working Capital Estimator
Practical demo tool for Indian MSMEs to estimate working capital needs
and identify cash-flow gaps using invoices, UPI patterns, and GST context.

Created: 2026-11-10
Author: ShihaiSuru
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def generate_sample_data():
    """Generate realistic sample data for an Indian MSME (e.g., trading or manufacturing)."""
    # Sample invoices (receivables)
    invoices = [
        {"id": "INV-001", "amount": 150000, "date": "2026-10-01", "due_days": 45, "status": "pending", "customer": "Retail Chain A"},
        {"id": "INV-002", "amount": 85000, "date": "2026-10-15", "due_days": 30, "status": "pending", "customer": "Distributor B"},
        {"id": "INV-003", "amount": 220000, "date": "2026-09-20", "due_days": 60, "status": "overdue", "customer": "Govt Supplier C"},
        {"id": "INV-004", "amount": 45000, "date": "2026-11-01", "due_days": 15, "status": "pending", "customer": "Local Buyer D"},
    ]
    
    # Sample UPI / bank inflows (last 60 days)
    inflows = [
        {"date": "2026-10-05", "amount": 120000, "source": "UPI - Customer A"},
        {"date": "2026-10-20", "amount": 60000, "source": "UPI - Customer B"},
        {"date": "2026-11-02", "amount": 35000, "source": "UPI - Misc"},
    ]
    
    # Sample outflows / expenses
    outflows = [
        {"date": "2026-10-10", "amount": 90000, "category": "Raw materials"},
        {"date": "2026-10-25", "amount": 45000, "category": "Salaries"},
        {"date": "2026-11-05", "amount": 30000, "category": "GST payment"},
    ]
    
    return invoices, inflows, outflows

def calculate_receivables_aging(invoices):
    """Simple aging analysis for receivables."""
    today = datetime(2026, 11, 10)
    aging = {"current": 0, "1-30": 0, "31-60": 0, "60+": 0}
    
    for inv in invoices:
        inv_date = datetime.strptime(inv["date"], "%Y-%m-%d")
        days_outstanding = (today - inv_date).days
        if inv["status"] == "pending" or inv["status"] == "overdue":
            if days_outstanding <= 30:
                aging["current"] += inv["amount"]
            elif days_outstanding <= 60:
                aging["1-30"] += inv["amount"]
            else:
                aging["60+"] += inv["amount"]
    
    return aging

def estimate_working_capital(invoices, inflows, outflows):
    """
    Core estimation logic:
    - Calculate average monthly inflows/outflows
    - Factor in pending receivables
    - Apply simple risk buffer for Indian MSME payment delays
    """
    total_pending_receivables = sum(inv["amount"] for inv in invoices if inv["status"] in ["pending", "overdue"])
    
    # Simple averages (demo)
    avg_monthly_inflow = sum(i["amount"] for i in inflows) / 2  # ~2 months data
    avg_monthly_outflow = sum(o["amount"] for o in outflows) / 2
    
    # Working capital need = operating cycle buffer + pending gap
    # Typical MSME operating cycle: 45-60 days
    operating_buffer = avg_monthly_outflow * 1.5  # 45-day buffer
    cash_gap = max(0, total_pending_receivables * 0.4 - avg_monthly_inflow)  # Conservative collection assumption
    
    estimated_wc = operating_buffer + cash_gap
    
    # Risk score (0-100)
    overdue_ratio = sum(inv["amount"] for inv in invoices if inv["status"] == "overdue") / max(1, total_pending_receivables)
    risk_score = min(100, int(overdue_ratio * 70 + 20))
    
    return {
        "total_pending_receivables": total_pending_receivables,
        "avg_monthly_inflow": round(avg_monthly_inflow),
        "avg_monthly_outflow": round(avg_monthly_outflow),
        "estimated_working_capital_need": round(estimated_wc),
        "risk_score": risk_score,
        "recommendation": "Consider invoice discounting or short-term working capital loan" if estimated_wc > avg_monthly_outflow else "Current liquidity looks manageable"
    }

def print_report(result, aging):
    """Pretty-print the estimation report."""
    print("=" * 60)
    print("AI MSME WORKING CAPITAL ESTIMATOR")
    print("Indian MSME Cash-Flow Analysis | Demo Date: 2026-11-10")
    print("=" * 60)
    print(f"Total Pending Receivables : ₹{result['total_pending_receivables']:,}")
    print(f"Avg Monthly Inflow        : ₹{result['avg_monthly_inflow']:,}")
    print(f"Avg Monthly Outflow       : ₹{result['avg_monthly_outflow']:,}")
    print("-" * 60)
    print(f"Estimated WC Requirement  : ₹{result['estimated_working_capital_need']:,}")
    print(f"Risk Score (0-100)        : {result['risk_score']}")
    print(f"Recommendation            : {result['recommendation']}")
    print("-" * 60)
    print("Receivables Aging:")
    for bucket, amount in aging.items():
        print(f"  {bucket:10} : ₹{amount:,}")
    print("=" * 60)
    print("\nNote: This is a practical starter demo. Replace sample data with real")
    print("UPI statements, invoices, and GST summaries for production use.")
    print("Built for Indian MSME founders focused on AI cash-flow systems.")

if __name__ == "__main__":
    print("Loading sample MSME data...\n")
    invoices, inflows, outflows = generate_sample_data()
    aging = calculate_receivables_aging(invoices)
    result = estimate_working_capital(invoices, inflows, outflows)
    print_report(result, aging)
