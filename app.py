import streamlit as st
import pandas as pd
import io
from trial_balance import TrialBalanceProcessor
from reconciliation import ReconciliationEngine
from pdf_export import PDFReportGenerator
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Financial Close Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #dc3545;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Navigation
st.sidebar.title("📊 Financial Close Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "Select a tool:",
    ["Home", "Trial Balance Generator", "Reconciliation Review", "Export Reports"]
)

st.sidebar.divider()
st.sidebar.markdown("### About")
st.sidebar.info("""
**Version:** 1.0  
**Purpose:** Automate month-end close processes for accounting firms and finance teams.  
**Built by:** Trial Balance Assistant
""")

# Initialize session state
if 'trial_balance_df' not in st.session_state:
    st.session_state.trial_balance_df = None
if 'summary' not in st.session_state:
    st.session_state.summary = {}
if 'reconciliation_report' not in st.session_state:
    st.session_state.reconciliation_report = None
if 'original_gl' not in st.session_state:
    st.session_state.original_gl = None

# ==================== HOME PAGE ====================
if page == "Home":
    st.title("Welcome to Financial Close Assistant")
    st.subheader("Automate Your Month-End Close Process")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What We Do
        - **Trial Balance Generation**: Automatically create trial balance from GL exports
        - **Reconciliation**: Flag suspicious entries, missing accounts, and data issues
        - **PDF Reports**: Professional reports for stakeholders and auditors
        - **Excel Export**: Download clean data for further analysis
        
        ### How to Use
        1. Upload your GL export (CSV format)
        2. Review the trial balance
        3. Check reconciliation findings
        4. Export reports and data
        """)
    
    with col2:
        st.markdown("""
        ### Required Format
        Your CSV should have these columns:
        - **Account_Code** (e.g., 1001, 2100)
        - **Account_Name** (e.g., Cash, Accounts Payable)
        - **Debit** (numeric)
        - **Credit** (numeric)
        
        ### Sample Data
        You can download our sample GL file to test the tool.
        """)
        
        # Create sample data
        sample_data = {
            'Account_Code': ['1001', '1010', '1100', '2100', '2200', '3100', '4000', '4100', '5000', '5100'],
            'Account_Name': ['Cash', 'Bank Account', 'Accounts Receivable', 'Accounts Payable', 'Short-term Loans', 'Capital Stock', 'Revenue from Sales', 'Service Revenue', 'Salary Expense', 'Rent Expense'],
            'Debit': [50000, 100000, 75000, 0, 0, 0, 0, 0, 25000, 10000],
            'Credit': [0, 0, 0, 35000, 40000, 150000, 180000, 50000, 0, 0]
        }
        sample_df = pd.DataFrame(sample_data)
        
        csv_buffer = io.BytesIO()
        sample_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Sample GL CSV",
            data=csv_buffer.getvalue(),
            file_name="sample_gl.csv",
            mime="text/csv"
        )

# ==================== TRIAL BALANCE GENERATOR ====================
elif page == "Trial Balance Generator":
    st.title("Trial Balance Generator")
    st.markdown("Upload your General Ledger export and we'll generate a trial balance automatically.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload GL Export (CSV)", type=['csv'])
    
    with col2:
        company_name = st.text_input("Company Name", value="Your Company Name")
    
    if uploaded_file is not None:
        try:
            # Read CSV
            gl_df = pd.read_csv(uploaded_file)
            st.session_state.original_gl = gl_df
            
            # Process trial balance
            processor = TrialBalanceProcessor(gl_df)
            
            if processor.generate_trial_balance():
                st.session_state.trial_balance_df = processor.trial_balance
                st.session_state.summary = processor.summary
                
                # Display summary metrics
                st.divider()
                st.subheader("📈 Trial Balance Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Debits",
                        f"₹{processor.summary['total_debit']:,.0f}"
                    )
                
                with col2:
                    st.metric(
                        "Total Credits",
                        f"₹{processor.summary['total_credit']:,.0f}"
                    )
                
                with col3:
                    st.metric(
                        "Difference",
                        f"₹{processor.summary['difference']:,.0f}",
                        delta="Balanced" if processor.summary['is_balanced'] else "Not Balanced"
                    )
                
                with col4:
                    st.metric(
                        "Number of Accounts",
                        processor.summary['num_accounts']
                    )
                
                # Balance status
                if processor.summary['is_balanced']:
                    st.markdown("""
                        <div class="success-box">
                        ✅ <b>Trial Balance is BALANCED</b>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="error-box">
                        ❌ <b>Trial Balance is NOT BALANCED</b> - Please review your GL entries
                        </div>
                    """, unsafe_allow_html=True)
                
                # Display trial balance table
                st.divider()
                st.subheader("📋 Detailed Trial Balance")
                
                display_tb = processor.get_trial_balance()
                
                # Format for display
                numeric_cols = ['Debit', 'Credit', 'Absolute_Balance']
                
                st.dataframe(
                    display_tb,
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )
                
                # Unbalanced accounts warning
                unbalanced = processor.get_unbalanced_accounts()
                if len(unbalanced) > 0:
                    st.divider()
                    st.markdown("""
                        <div class="warning-box">
                        ⚠️ <b>Accounts with Both Debit and Credit Entries</b> - These may need review
                        </div>
                    """, unsafe_allow_html=True)
                    
                    unbalanced_df = pd.DataFrame(unbalanced)
                    st.dataframe(unbalanced_df, use_container_width=True, hide_index=True)
                
                # Export options
                st.divider()
                st.subheader("💾 Export Trial Balance")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Excel export
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        display_tb.to_excel(writer, sheet_name='Trial Balance', index=False)
                        
                        # Summary sheet
                        summary_df = pd.DataFrame([
                            ['Total Debits', f"₹{processor.summary['total_debit']:,.2f}"],
                            ['Total Credits', f"₹{processor.summary['total_credit']:,.2f}"],
                            ['Difference', f"₹{processor.summary['difference']:,.2f}"],
                            ['Status', 'BALANCED' if processor.summary['is_balanced'] else 'NOT BALANCED']
                        ], columns=['Metric', 'Value'])
                        
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="📊 Download Excel (.xlsx)",
                        data=excel_buffer.getvalue(),
                        file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # PDF export
                    pdf_generator = PDFReportGenerator(company_name=company_name)
                    pdf_buffer = pdf_generator.generate_trial_balance_pdf(
                        processor.trial_balance,
                        processor.summary
                    )
                    
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_buffer.getvalue(),
                        file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                
                st.success("✅ Ready for reconciliation review!")
            
            else:
                st.error("❌ Error processing GL data:")
                for error in processor.errors:
                    st.error(f"- {error}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# ==================== RECONCILIATION REVIEW ====================
elif page == "Reconciliation Review":
    st.title("Reconciliation & Review")
    st.markdown("Review your trial balance for suspicious entries and potential issues.")
    
    if st.session_state.trial_balance_df is None:
        st.warning("⚠️ Please upload and generate a trial balance first!")
    else:
        # Run reconciliation
        engine = ReconciliationEngine(st.session_state.trial_balance_df)
        recon_report = engine.generate_reconciliation_report()
        st.session_state.reconciliation_report = recon_report
        
        # Overall status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = recon_report['overall_status']
            st.metric("Status", status)
        
        with col2:
            st.metric("Total Issues", recon_report['total_issues'])
        
        with col3:
            balance = recon_report['balance_status']
            st.metric("Difference", f"₹{balance['difference']:,.0f}")
        
        # Balance check
        st.divider()
        st.subheader("1️⃣ Balance Check Results")
        
        balance = recon_report['balance_status']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Debits", f"₹{balance['total_debit']:,.0f}")
        with col2:
            st.metric("Total Credits", f"₹{balance['total_credit']:,.0f}")
        with col3:
            if balance['is_balanced']:
                st.markdown("""
                    <div class="success-box">
                    ✅ BALANCED
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="error-box">
                    ❌ NOT BALANCED - Difference: ₹{:,.2f}
                    </div>
                """.format(balance['difference']), unsafe_allow_html=True)
        
        # Suspicious entries
        st.divider()
        st.subheader("2️⃣ Flagged Issues")
        
        suspicious = recon_report['suspicious_entries']
        
        if len(suspicious) == 0:
            st.markdown("""
                <div class="success-box">
                ✅ No issues detected
                </div>
            """, unsafe_allow_html=True)
        else:
            sus_df = pd.DataFrame(suspicious)
            st.dataframe(sus_df, use_container_width=True, hide_index=True)
        
        # Round amounts
        st.divider()
        st.subheader("3️⃣ Round Amount Entries")
        
        round_amounts = recon_report['round_amounts']
        
        if len(round_amounts) == 0:
            st.info("ℹ️ No suspiciously round amounts detected")
        else:
            st.warning(f"Found {len(round_amounts)} accounts with round amounts (likely manual entries)")
            round_df = pd.DataFrame(round_amounts)
            st.dataframe(round_df, use_container_width=True, hide_index=True)
        
        # Recommendations
        st.divider()
        st.subheader("💡 Recommendations")
        
        recommendations = engine.get_recommendations()
        for rec in recommendations:
            st.write(rec)
        
        # Export reconciliation report
        st.divider()
        st.subheader("💾 Export Reconciliation Report")
        
        company_name = st.text_input("Company Name for Report", value="Your Company Name")
        
        pdf_generator = PDFReportGenerator(company_name=company_name)
        pdf_buffer = pdf_generator.generate_reconciliation_pdf(
            st.session_state.trial_balance_df,
            recon_report
        )
        
        st.download_button(
            label="📄 Download Reconciliation Report (PDF)",
            data=pdf_buffer.getvalue(),
            file_name=f"reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

# ==================== EXPORT REPORTS ====================
elif page == "Export Reports":
    st.title("Export Reports & Data")
    st.markdown("Download comprehensive reports and data for your records.")
    
    if st.session_state.trial_balance_df is None:
        st.warning("⚠️ Please upload and generate a trial balance first!")
    else:
        st.subheader("Available Exports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Trial Balance Exports")
            
            # Excel trial balance
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                display_tb = pd.DataFrame(st.session_state.trial_balance_df)
                display_tb.to_excel(writer, sheet_name='Trial Balance', index=False)
                
                summary_df = pd.DataFrame([
                    ['Total Debits', st.session_state.summary['total_debit']],
                    ['Total Credits', st.session_state.summary['total_credit']],
                    ['Difference', st.session_state.summary['difference']],
                    ['Is Balanced', st.session_state.summary['is_balanced']]
                ], columns=['Metric', 'Value'])
                
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📊 Trial Balance (Excel)",
                data=excel_buffer.getvalue(),
                file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="export_tb_excel"
            )
            
            # PDF trial balance
            company_name = st.text_input("Company Name", value="Your Company Name", key="company_1")
            pdf_generator = PDFReportGenerator(company_name=company_name)
            pdf_buffer = pdf_generator.generate_trial_balance_pdf(
                st.session_state.trial_balance_df,
                st.session_state.summary
            )
            
            st.download_button(
                label="📄 Trial Balance (PDF)",
                data=pdf_buffer.getvalue(),
                file_name=f"trial_balance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="export_tb_pdf"
            )
        
        with col2:
            st.markdown("### Reconciliation Exports")
            
            if st.session_state.reconciliation_report is not None:
                company_name = st.text_input("Company Name", value="Your Company Name", key="company_2")
                pdf_generator = PDFReportGenerator(company_name=company_name)
                pdf_buffer = pdf_generator.generate_reconciliation_pdf(
                    st.session_state.trial_balance_df,
                    st.session_state.reconciliation_report
                )
                
                st.download_button(
                    label="📄 Reconciliation Report (PDF)",
                    data=pdf_buffer.getvalue(),
                    file_name=f"reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="export_recon_pdf"
                )
            else:
                st.info("ℹ️ Go to Reconciliation Review tab to generate report")
        
        st.divider()
        
        # Original GL export
        st.subheader("Original Data")
        
        csv_buffer = io.BytesIO()
        st.session_state.original_gl.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="📥 Original GL Data (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"original_gl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;'>
    <p><b>Financial Close Assistant v1.0</b> | Automate your month-end close process</p>
    <p>For support or feature requests, contact support@example.com</p>
    </div>
""", unsafe_allow_html=True)
