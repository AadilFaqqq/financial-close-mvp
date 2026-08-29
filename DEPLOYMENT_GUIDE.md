# 🚀 Deployment Guide - Financial Close Assistant

**Get your app live in 5 minutes and start selling it.**

---

## **Option A: Streamlit Cloud (RECOMMENDED - FREE)**

### Prerequisites
- GitHub account (free at github.com)
- Streamlit account (sign in with GitHub - free)

### Step-by-Step

#### **1. Create GitHub Repository**

1. Go to **github.com** → Sign in
2. Click **"+"** (top right) → **"New repository"**
3. Fill in:
   - **Repository name:** `financial-close-mvp`
   - **Description:** "Trial Balance & Reconciliation Automation for CA Firms"
   - **Public** (so Streamlit Cloud can access it)
   - ✅ Add README
4. Click **"Create repository"**

#### **2. Upload Your Files to GitHub**

**Option A: Via GitHub Web UI (Easy)**
1. Open your new repo
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop these files:
   - `app.py`
   - `trial_balance.py`
   - `reconciliation.py`
   - `pdf_export.py`
   - `requirements.txt`
   - `sample_gl.csv`
   - `README.md`
4. Click **"Commit changes"**

**Option B: Via Command Line (Faster)**
```bash
cd /home/claude

git init
git add .
git commit -m "Initial commit - Financial Close MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/financial-close-mvp.git
git push -u origin main
```

#### **3. Deploy to Streamlit Cloud**

1. Go to **streamlit.io/cloud** → Sign in with GitHub
2. Click **"New app"**
3. Fill in:
   - **GitHub account:** Your username
   - **Repository:** `financial-close-mvp`
   - **Branch:** `main`
   - **File path:** `app.py`
4. Click **"Deploy"**

**That's it! Your app is live.**

You'll get a URL like: `https://financial-close-mvp-aadil.streamlit.app`

---

#### **4. Share Your Live App**

Send this to customers:
```
Try our Financial Close Assistant:
https://financial-close-mvp-aadil.streamlit.app

Upload your GL → Get trial balance in 30 seconds
Free demo available
```

---

## **Option B: Heroku (Paid, More Control)**

**Cost:** ₹500-1,500/month  
**Better for:** Custom domain, more control, running 24/7

### Steps

1. **Create Heroku account:** heroku.com
2. **Install Heroku CLI**
3. **Push your code:**

```bash
heroku create financial-close-mvp
git push heroku main
```

**Your URL:** `https://financial-close-mvp.herokuapp.com`

---

## **Option C: Railway (Simple, Cheap)**

**Cost:** ₹300-1,000/month  
**Better for:** Quick deployment, good uptime

```bash
npm install -g @railway/cli
railway up
```

---

## **After Deployment**

### ✅ Test Your Live App

1. Open your Streamlit Cloud URL
2. Upload `sample_gl.csv`
3. Verify trial balance generates correctly
4. Download PDF/Excel
5. Test on mobile (responsive?)

### ✅ Set Up Custom Domain (Optional)

If you want `yourfirm.com` instead of `streamlit.app`:

1. Buy domain on Namecheap/GoDaddy (₹100-500/year)
2. Point DNS to Streamlit Cloud
3. Configure in Streamlit settings

### ✅ Add Analytics

Track how many people use your app:

```python
# Add to app.py (top of file)
import streamlit_analytics
streamlit_analytics.start_tracking()

# ... rest of your code ...

streamlit_analytics.stop_tracking()
```

### ✅ Enable Sharing Features

Add this to `app.py` to let users share via WhatsApp/email:

```python
st.markdown("""
    Share this app: 
    [WhatsApp](https://wa.me/?text=Check%20out%20Financial%20Close%20Assistant%20https://financial-close-mvp.streamlit.app)
    | [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://financial-close-mvp.streamlit.app)
    | [Email](mailto:?subject=Financial%20Close%20Assistant&body=Check%20this%20out:%20https://financial-close-mvp.streamlit.app)
""")
```

---

## **Troubleshooting**

### "Deployment failed"
- Check that `requirements.txt` has all packages
- Ensure no local file paths in code

### "App runs locally but crashes on Streamlit Cloud"
- Add missing packages to `requirements.txt`
- Check for file path issues

### "Takes too long to load"
- Add `@st.cache_data` decorator to slow functions
- Reduce sample data size

---

## **Going Live Checklist**

- [ ] Code pushed to GitHub
- [ ] App deployed to Streamlit Cloud
- [ ] Tested with sample CSV
- [ ] PDF/Excel export works
- [ ] Mobile-responsive (tested on phone)
- [ ] Share button added
- [ ] Analytics tracking enabled (optional)
- [ ] Created landing page
- [ ] Email templates ready for outreach

---

## **Next: Create a Landing Page**

See `LANDING_PAGE.html` to create a simple website for your product.

Then: Start emailing CA firms and accounting companies.
