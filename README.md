# Financial Close Assistant - MVP

**Automate month-end close processes for accounting firms and finance teams in India.**

---

## 🎯 What It Does

This Streamlit web app helps accounting firms and finance departments automate:

1. **Trial Balance Generation** - Auto-calculate trial balance from GL exports
2. **Reconciliation Checks** - Flag suspicious entries, missing accounts, data issues
3. **PDF/Excel Reports** - Professional reports for stakeholders and auditors
4. **Data Validation** - Ensure debits = credits and data integrity

**Time saved per month-end close:** ~2-3 hours per accountant per client

---

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)

---

## 🚀 Quick Start (Local Testing)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the App Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Step 3: Test with Sample Data

1. Go to **Trial Balance Generator** tab
2. Download the sample GL CSV (or use `sample_gl.csv` in the folder)
3. Upload it and see the trial balance generate automatically

---

## 📁 Project Structure

```
financial-close-mvp/
├── app.py                    # Main Streamlit application
├── trial_balance.py          # Trial balance calculation logic
├── reconciliation.py         # Reconciliation & anomaly detection
├── pdf_export.py             # PDF report generation
├── requirements.txt          # Python dependencies
├── sample_gl.csv             # Sample GL data for testing
└── README.md                 # This file
```

---

## 💰 Monetization Strategy

### Target Market
- **Accounting Firms** (5-50 employees)
- **Finance Teams** at mid-market companies (₹10cr+ annual revenue)
- **CA/CPA Practices** in India

### Pricing Models

#### Option 1: SaaS Subscription
- **Basic:** ₹5,000/month - 5 clients per month
- **Pro:** ₹12,000/month - 20 clients per month + support
- **Enterprise:** ₹25,000/month - unlimited + API access

**Why this works:** Every firm does this manually now. You save them 2-3 hours/client/month = ₹3,000-5,000 in labor savings per client.

#### Option 2: Pay-per-Use
- ₹500 per trial balance generated
- ₹200 per reconciliation report

**Best for:** Firms with irregular close schedules

#### Option 3: One-time Sale + Support
- ₹50,000 - perpetual license for one firm
- ₹500/month - ongoing support & updates

**Best for:** Large firms wanting on-premise/customized solution

---

## 🎬 Getting Customers (Day 1 Strategy)

### 1. Direct Outreach
- **Find accounting firms on:**
  - LinkedIn (search "CA", "Chartered Accountant", "Mumbai", "Delhi", "Bangalore")
  - JustDial (search "accounting firms near me")
  - ICAI directory (Institute of Chartered Accountants of India)

- **Pitch:** "Hi, I help CAs save 2-3 hours on month-end close. Demo available."
- **Demo:** Show them your app with a sample of their GL structure
- **Offer:** Free 1-month trial → ₹5,000/month after

### 2. Social Proof
- Create 2-3 case studies from beta users
- Get testimonials: "Saved us 10 hours/month" → share on LinkedIn
- Before/After: Manual process vs. your tool

### 3. Content
- LinkedIn posts: "3 mistakes accountants make during month-end close"
- YouTube demo: 5-min walkthrough of the tool
- Create a simple landing page (Webflow, Wix, or HTML) with pricing

---

## 📊 What to Include in Your First Pitch

**Subject:** "Trial Balance & Close Automation for CA Firms"

**Body:**
```
Hi [CA Name],

I built a tool that automates month-end trial balance & reconciliation.

What it does:
✓ Upload GL → Get trial balance in 30 seconds (not 2 hours)
✓ Flags errors & suspicious entries automatically
✓ Exports professional PDF/Excel reports
✓ Zero learning curve - works with your current setup

Works with: Tally, SAP, Custom ERP, CSV exports

Free 1-month trial | ₹5,000/month after

Can I show you a 10-minute demo?

Best,
[Your Name]
```

---

## 🔧 Customization for Clients

Once you land customers, you can add:

1. **Tally/SAP Integration** - Direct data pull instead of CSV upload
2. **Journal Entry Templates** - Pre-configured for common close entries
3. **Multi-company Close** - Consolidate across legal entities
4. **Audit Trail** - Track who changed what and when
5. **Email Reports** - Auto-send TB/reconciliation to stakeholders

---

## 🚢 Deployment (Making It Live)

Once you have paying customers, deploy to:

### Option A: Streamlit Cloud (Free, Easy)
1. Push code to GitHub (public or private)
2. Go to `streamlit.io` → "Deploy"
3. Connect GitHub → Select your repo → Deploy
4. Get a live URL in 2 minutes
5. Share with clients

**Cost:** Free tier (1 app), or ₹1,000/month for premium

### Option B: Heroku / Railway (Paid, More Control)
1. `pip install gunicorn`
2. Deploy Streamlit app
3. **Cost:** ₹500-2,000/month

### Option C: Replit (Free, No Code)
1. Upload files to Replit
2. Run `streamlit run app.py`
3. Get shareable link
4. **Cost:** Free (with ads) or paid

**Recommendation:** Start with Streamlit Cloud → move to Heroku when you have 5+ paying clients.

---

## 📈 Revenue Projection (Next 6 Months)

```
Month 1: 2 customers @ ₹5,000 = ₹10,000
Month 2: 4 customers @ ₹5,000 = ₹20,000
Month 3: 6 customers @ ₹5,000 = ₹30,000
Month 4: 8 customers @ ₹5,000 + 2 @ ₹12,000 = ₹64,000
Month 5: 10 customers @ ₹5,000 + 4 @ ₹12,000 = ₹98,000
Month 6: 12 customers @ ₹5,000 + 6 @ ₹12,000 = ₹132,000

**Total Year 1 Potential:** ₹3-5 lakhs
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### "CSV upload not working"
- Ensure CSV has columns: `Account_Code`, `Account_Name`, `Debit`, `Credit`
- No spaces in column names
- Debit/Credit must be numbers (not text)

### "PDF download button doesn't work"
- Make sure reportlab is installed: `pip install reportlab`

---

## 📚 Next Steps (After MVP Success)

1. **Month 1-2:** Get 3-5 paying customers, iterate based on feedback
2. **Month 3:** Add automated journal entries (largest pain point)
3. **Month 4:** Build Tally integration (most common ERP in India)
4. **Month 5:** Add GST compliance checks (second biggest market)
5. **Month 6:** Raise ₹10-20 lakhs from angel investors / build team

---

## 💡 Key Metrics to Track

- **Users who uploaded GL data:** Conversion from signup
- **Trial balance successful:** Feature adoption
- **Customers who exported PDF:** Monetization readiness
- **Time saved (estimate):** Collect from customers
- **Customer acquisition cost:** Track your marketing spend
- **Monthly recurring revenue (MRR):** Your actual income

---

## 📞 Support

For feature requests or bugs:
- Create an issue on GitHub
- Email: your-email@example.com

---

**Made with ❤️ for Indian accountants.**  
**Version 1.0 | Last Updated: 2024**
