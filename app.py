import streamlit as st
import pandas as pd
import io
from trial_balance import TrialBalanceProcessor
from reconciliation import ReconciliationEngine
from pdf_export import PDFReportGenerator
from datetime import datetime

st.set_page_config(
    page_title="Financial Close Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ SIMPLE PASSWORD LOGIN ============
password_input = st.text_input("🔐 Enter password:", type="password")

if password_input != "aadil-admin-forever":
    st.error("❌ Invalid password")
    st.stop()

st.success("✅ Access granted")

# ============ REST OF APP ============

st.markdown("""
    <style>
        .main { padding: 2rem; }
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
**Purpose:** Automate month-end close for CA firms
""")

if 'trial_balance_df' not in st.session_state:
    st.session_state.trial_balance_df = None
if 'summary' not in st.session_state:
    st.session_state.summary = {}
if 'reconciliation_report' not in st.session_state:
    st.session_state.reconciliation_report = None
if 'original_gl' not in st.session_state:
    st.session_state.original_gl = None

# HOME PAGE
if page == "Home":
    st.title("Welcome to Financial Close Assistant")
    st.subheader("Automate Your Month-End Close Process")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What We Do
        - **Trial Balance Generation**: Auto-create trial balance from GL
        - **Reconciliation**: Flag suspicious entries and issues
        - **PDF Reports**: Professional reports for stakeholders
        - **Excel Export**: Download clean data
        """)
    
    with col2:
        st.markdown("""
        ### Required Format
        CSV with columns:
        - **Account_Code** (e.g., 1001)
        - **Account_Name** (e.g., Cash)
        - **Debit** (numeric)
        - **Credit** (numeric)
        """)
        
        sample_data = {
            'Account_Code': ['1001', '1010', '1100', '2100', '2200', '3100', '4000', '4100', '5000', '5100'],
            'Account_Name': ['Cash', 'Bank', 'AR', 'AP', 'Loans', 'Capital', 'Revenue', 'Service', 'Salary', 'Rent'],
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

elif page == "Trial Balance Generator":
    st.title("Trial Balance Generator")
    st.markdown("Upload your GL export")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload GL Export (CSV)", type=['csv'])
    
    with col2:
        company_name = st.text_input("Company Name", value="Your Company")
    
    if uploaded_file is not None:
        try:
            gl_df = pd.read_csv(uploaded_file)
            st.session_state.original_gl = gl_df
            
            processor = TrialBalanceProcessor(gl_df)
            
            if processor.generate_trial_balance():
                st.session_state.trial_balance_df = processor.trial_balance
                st.session_state.summary = processor.summary
                
                st.divider()
                st.subheader("📈 Trial Balance Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Debits", f"₹{processor.summary['total_debit']:,.0f}")
                with col2:
                    st.metric("Total Credits", f"₹{processor.summary['total_credit']:,.0f}")
                with col3:
                    st.metric("Difference", f"₹{processor.summary['difference']:,.0f}", delta="Balanced" if processor.summary['is_balanced'] else "Not Balanced")
                with col4:
                    st.metric("Accounts", processor.summary['num_accounts'])
                
                if processor.summary['is_balanced']:
                    st.markdown("<div class='success-box'>✅ <b>Trial Balance is BALANCED</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='error-box'>❌ <b>Trial Balance is NOT BALANCED</b></div>", unsafe_allow_html=True)
                
                st.divider()
                st.subheader("📋 Detailed Trial Balance")
                
                display_tb = processor.get_trial_balance()
                st.dataframe(display_tb, use_container_width=True, height=400, hide_index=True)
                
                st.divider()
                st.subheader("💾 Export")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        display_tb.to_excel(writer, sheet_name='TB', index=False)
                    excel_buffer.seek(0)
                    
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"tb_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    pdf_generator = PDFReportGenerator(company_name=company_name)
                    pdf_buffer = pdf_generator.generate_trial_balance_pdf(processor.trial_balance, processor.summary)
                    
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"tb_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif page == "Reconciliation Review":
    st.title("Reconciliation Review")
    
    if st.session_state.trial_balance_df is None:
        st.warning("Please upload a trial balance first")
    else:
        engine = ReconciliationEngine(st.session_state.trial_balance_df)
        recon_report = engine.generate_reconciliation_report()
        st.session_state.reconciliation_report = recon_report
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", recon_report['overall_status'])
        with col2:
            st.metric("Issues", recon_report['total_issues'])
        with col3:
            balance = recon_report['balance_status']
            st.metric("Difference", f"₹{balance['difference']:,.0f}")
        
        st.divider()
        st.subheader("Balance Check")
        balance = recon_report['balance_status']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Debits", f"₹{balance['total_debit']:,.0f}")
        with col2:
            st.metric("Credits", f"₹{balance['total_credit']:,.0f}")
        with col3:
            if balance['is_balanced']:
                st.markdown("<div class='success-box'>✅ BALANCED</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='error-box'>❌ NOT BALANCED</div>", unsafe_allow_html=True)

elif page == "Export Reports":
    st.title("Export Reports")
    
    if st.session_state.trial_balance_df is None:
        st.warning("Please upload a trial balance first")
    else:
        st.success("All exports ready")

st.divider()
st.markdown("<div style='text-align: center; color: #666; font-size: 0.8em;'><p><b>Financial Close Assistant v1.0</b></p></div>", unsafe_allow_html=True)
