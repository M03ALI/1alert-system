# Stock Inventory Dashboard & Alert System

An offline inventory tracker for **Health Data Matrics (HDM)**. It installs as a normal
Windows program (Start-Menu and Desktop shortcuts), opens in its own window, and needs
**no Python** on the user's computer. All data stays on the machine in
`C:\Users\<you>\StockInventory\`.

---

## What it does

- **Dashboard** with colour-coded status (Available / Moderate / Restock / Out of stock).
- **Usage by day**, **Restocking**, and full **Usage history** with search, date filters and CSV export.
- **Expiry tracking** — flags items that are expired or expiring soon (Dashboard + Restocking page).
- **Days of stock left** — estimated from each item's recent usage.
- **Reports** — save / email / share HTML and PDF reports.
- **Bulk import** items from a `.csv` or `.xlsx` (non-destructive: blank cells never erase saved data).
- **Edit / correct** past usage and restock entries.
- **"Recorded by"** field + an **audit trail** of every change.
- **Accounts** — sign in with a Google or work email + password; the app is locked until an account is created.
- **Automatic backups** (kept in `StockInventory\Backups`) with one-click restore.
- **Settings** — alert thresholds, bulk import, backups, audit trail.
- **Refresh** button to fully reload the app if the screen becomes unresponsive.
- **Check for updates** (optional, needs internet).

---

## Build the Windows installer (in the cloud — nothing to install on your PC)

1. **Upload these files** to your GitHub repo (keep the folder layout):

       inventoryapp.py
       app_entry.py
       requirements.txt
       StockInventory.spec
       installer.iss
       logo.ico
       README.md
       .github/workflows/build-windows.yml

   (Easiest: extract `StockInventory-repo.zip` and upload its contents.)

2. On GitHub, open the **Actions** tab -> **Build Windows Installer** -> **Run workflow**.
   Wait a few minutes for the green tick.

3. Open the **Releases** section of the repo -> download **`StockInventory-Setup.exe`**.

4. On your Windows machine, **run `StockInventory-Setup.exe`** and follow the installer.
   Launch it from the **Start Menu** or the **Desktop shortcut**.

> Windows SmartScreen may warn that the publisher is unknown (the app isn't code-signed).
> Click **More info -> Run anyway**. This is expected for in-house software.

---

## Updating later

- Make your changes, upload the new `inventoryapp.py` (and any other changed files), and
  run the workflow again to produce a new installer.
- To make the in-app **Check for updates** light up, create a GitHub **Release** with a tag
  like `v1.1.1` (a higher number than the version in the app).

---

## Notes

- The app runs **fully offline**. Only two optional things use the internet:
  **Check for updates**, and the one-time cloud build above.
- "Continue with Google / work account" links the account to that email and stores a secure
  **local** password; it is not a live Google sign-in.
- **Tech:** Python, Streamlit, SQLite, Plotly, ReportLab, openpyxl, packaged with PyInstaller
  and Inno Setup via GitHub Actions.
