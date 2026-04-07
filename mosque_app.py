"""
Mosque Management System
========================
A simple offline desktop application for tracking mosque donations and expenses.
Built with CustomTkinter (dark mode) and sqlite3.
Supports English and Urdu UI.
"""

import customtkinter as ctk
import sqlite3
import os
import shutil
from tkinter import filedialog
import tempfile
from datetime import datetime
import time

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────

APP_TITLE = "Mosque Management System"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
DB_NAME = "mosque.db"

COLOR_BG_DARK = "#0f1117"
COLOR_SIDEBAR = "#161b22"
COLOR_CARD = "#1c2230"
COLOR_CARD_HOVER = "#242d3d"
COLOR_ACCENT = "#38bdf8"
COLOR_ACCENT_HOVER = "#7dd3fc"

COLOR_GREEN = "#34d399"
COLOR_RED = "#f87171"
COLOR_AMBER = "#fbbf24"
COLOR_TEXT = "#e2e8f0"
COLOR_TEXT_DIM = "#94a3b8"
COLOR_BORDER = "#2d3748"

URDU_FONT = "Jameel Noori Nastaleeq"
DEFAULT_FONT = "Segoe UI"

DONATION_CAT_KEYS = ["cat_general", "cat_zakat", "cat_sadqa", "cat_construction"]
PAYMENT_TYPE_KEYS = ["pay_cash", "pay_bank", "pay_online"]
EXPENSE_CAT_KEYS = ["exp_electricity", "exp_gas", "exp_water", "exp_maintenance", "exp_salary", "exp_charity", "exp_other"]
DONATION_CAT_DB = ["General", "Zakat", "Sadqa", "Construction"]
PAYMENT_TYPE_DB = ["Cash", "Bank", "Online"]
EXPENSE_CAT_DB = ["Electricity", "Gas", "Water", "Maintenance", "Salary", "Charity", "Other"]


# ──────────────────────────────────────────────
# TRANSLATIONS
# ──────────────────────────────────────────────

TRANSLATIONS = {
    "en": {
        "app_name": "Mosque System", "app_subtitle": "Finance Tracker",
        "navigation": "NAVIGATION", "version_footer": "v1.0  •  Offline Mode",
        "nav_dashboard": "📊  Dashboard", "nav_add_donation": "💰  Add Donation",
        "nav_add_expense": "📝  Add Expense", "nav_reports": "📄  Reports",
        "dashboard": "Dashboard", "total_donations": "Total Donations",
        "total_expenses": "Total Expenses", "current_balance": "Current Balance",
        "recent_transactions": "Recent Transactions",
        "no_transactions": "No transactions recorded yet.",
        "col_type": "Type", "col_amount": "Amount", "col_date": "Date",
        "col_name": "Name / Title", "col_category": "Category", "col_actions": "Actions",
        "type_donation": "Donation", "type_expense": "Expense",
        "add_donation": "Add Donation",
        "add_donation_desc": "Record a new donation received by the mosque.",
        "donor_name": "Donor Name (optional)", "donor_placeholder": "Enter donor name",
        "amount_label": "Amount (Rs) *", "amount_placeholder": "Enter amount (e.g. 5000)",
        "category": "Category", "payment_type": "Payment Type",
        "date_label": "Date (DD-MM-YYYY)",
        "save_donation": "💾   Save Donation",
        "donation_saved": "✅  Donation of Rs {amount} saved successfully!",
        "back_to_dashboard": "◀  Back to Dashboard", "go_dashboard": "📊  Dashboard",
        "add_expense": "Add Expense",
        "add_expense_desc": "Record a new expense made by the mosque.",
        "expense_title": "Expense Title *", "expense_title_placeholder": "e.g. Electricity Bill",
        "paid_to": "Paid To (optional)", "paid_to_placeholder": "Enter name or vendor",
        "notes_label": "Notes (optional)", "save_expense": "💾   Save Expense",
        "expense_saved": "✅  Expense of Rs {amount} saved successfully!",
        "err_amount_required": "⚠  Please enter an amount.",
        "err_amount_numeric": "⚠  Amount must be a valid number.",
        "err_amount_positive": "⚠  Amount must be greater than zero.",
        "err_date_format": "⚠  Date must be in DD-MM-YYYY format.",
        "err_title_required": "⚠  Please enter a title.",
        "cat_general": "General", "cat_zakat": "Zakat", "cat_sadqa": "Sadqa",
        "cat_construction": "Construction",
        "pay_cash": "Cash", "pay_bank": "Bank", "pay_online": "Online",
        "exp_electricity": "Electricity", "exp_gas": "Gas", "exp_water": "Water",
        "exp_maintenance": "Maintenance", "exp_salary": "Salary", "exp_other": "Other",
        "reports": "Monthly Report", "select_month": "Select Month",
        "donation_by_cat": "Donations by Category", "expense_by_cat": "Expenses by Category",
        "all_transactions": "All Transactions", "print_report": "🖨  Print Report",
        "net_balance": "Net Balance", "no_data_month": "No transactions found for this month.",
        "report_title": "Mosque Financial Report",
        "settings": "⚙  Settings", "mosque_name": "Mosque Name",
        "address": "Address", "phone_number": "Phone Number",
        "imam_name": "Imam Name", "notes": "Notes",
        "theme": "Theme", "dark_mode": "Dark Mode", "light_mode": "Light Mode",
        "backup_data": "Backup Data", "restore_data": "Restore Data",
        "save_settings": "💾  Save Settings", "settings_saved": "✅  Settings saved successfully!",
        "mosque_profile": "Mosque Profile", "data_management": "Data Management",
        "backup_success": "✅  Backup saved to:\n{path}",
        "restore_warning": "⚠  WARNING: This will overwrite data!\nAre you sure?",
        "restore_success": "✅  Data restored! Reloading...",
        "nav_about": "ℹ️  About", "about_project": "About Project",
        "about_developer": "About Developer",
        "nav_employees": "👥  Employees", "employees": "Employees", 
        "add_employee": "➕ Add Employee", "edit_employee": "✏️ Edit Employee",
        "delete_employee": "🗑️ Delete", "pay_salary": "💸 Pay Salary",
        "role": "Role", "salary_amount": "Monthly Salary", 
        "role_imam": "Imam", "role_moazzin": "Moazzin", 
        "role_cleaner": "Cleaner", "role_other": "Other",
        "already_paid_warning": "⚠  Salary already paid for this month!",
        "salary_paid_success": "✅  Salary paid successfully!",
        "confirm_delete_emp": "Are you sure you want to delete {name}?",
        "err_name_required": "⚠  Please enter a name.",
        "err_insufficient_balance": "⚠  Insufficient balance! Current: Rs {bal:,.0f}",
        "edit": "Edit", "delete": "Delete", "confirm_delete": "Are you sure you want to delete this transaction?",
        "last_modified": "Last Modified", "lock_app": "🔒 Lock App", "unlock_app": "Unlock App",
        "change_password": "Change Password", "old_password": "Old Password",
        "new_password": "New Password", "confirm_password": "Confirm Password",
        "password_changed": "✅ Password changed successfully!", "invalid_password": "⚠ Invalid current password.",
        "password_mismatch": "⚠ New passwords do not match.",
        "app_locked": "APPLICATION LOCKED", "enter_password": "Enter Password",
        "confirm_exit": "Are you sure you want to exit?", "exit_title": "Confirm Exit",
        "yes": "Yes", "no": "No", "ok": "OK",
        "fund": "Fund", "fund_type": "Fund Type", "fund_balance": "Fund Balance",
        "insufficient_fund_balance": "⚠ Insufficient balance in {fund} fund!",
        "zakat_warning": "⚠ Zakat funds should only be used for eligible purposes",
        "exp_charity": "Charity",
        "audit_log": "📋 Audit Log", "action": "Action", "description": "Description",
        "filter": "Filter", "date_range": "Date Range", "all": "All",
        "from": "From", "to": "To", "search": "Search", "generate": "Generate",
        "backup_path": "Default Backup Path", "browse": "Browse",
        "confirm_identity": "Confirm Identity", "incorrect_password": "⚠ Incorrect Password",
        "print": "Print", "save_and_print": "💾 & 🖨️  Save & Print",
        "err_month_locked": "⚠ This month is locked for data integrity.",
        "close_month": "Close Month", "reopen_month": "Reopen Month",
        "month_closed": "Month Closed", "month_open": "Month Open",
        "imam_name": "Operator Name", "notes": "Notes",
        "operator_name": "Operator Name", "col_operator": "Operator",
    },









    "ur": {
        "app_name": "مسجد سسٹم", "app_subtitle": "مالیاتی ٹریکر",
        "navigation": "نیویگیشن", "version_footer": "v1.0  •  آف لائن",
        "nav_dashboard": "📊  ڈیش بورڈ", "nav_add_donation": "💰  چندہ شامل کریں",
        "nav_add_expense": "📝  اخراجات شامل کریں", "nav_reports": "📄  رپورٹس",
        "dashboard": "ڈیش بورڈ", "total_donations": "کل چندہ",
        "total_expenses": "کل اخراجات", "current_balance": "موجودہ بیلنس",
        "recent_transactions": "حالیہ لین دین",
        "no_transactions": "ابھی تک کوئی لین دین ریکارڈ نہیں ہوا۔",
        "col_type": "قسم", "col_amount": "رقم", "col_date": "تاریخ",
        "col_name": "نام / عنوان", "col_category": "زمرہ",
        "type_donation": "چندہ", "type_expense": "خرچ",
        "add_donation": "چندہ شامل کریں",
        "add_donation_desc": "مسجد کو موصول ہونے والا نیا چندہ ریکارڈ کریں۔",
        "donor_name": "عطیہ دہندہ کا نام (اختیاری)", "donor_placeholder": "نام درج کریں",
        "amount_label": "رقم (Rs) *", "amount_placeholder": "رقم درج کریں (مثلاً 5000)",
        "category": "زمرہ", "payment_type": "ادائیگی کی قسم",
        "date_label": "تاریخ (DD-MM-YYYY)",
        "save_donation": "💾   چندہ محفوظ کریں",
        "donation_saved": "✅  Rs {amount} کا چندہ کامیابی سے محفوظ ہو گیا!",
        "back_to_dashboard": "◀  ڈیش بورڈ پر واپس", "go_dashboard": "📊  ڈیش بورڈ",
        "add_expense": "اخراجات شامل کریں",
        "add_expense_desc": "مسجد کا نیا خرچ ریکارڈ کریں۔",
        "expense_title": "خرچ کا عنوان *", "expense_title_placeholder": "مثلاً بجلی کا بل",
        "paid_to": "کس کو ادا کیا (اختیاری)", "paid_to_placeholder": "نام یا دکاندار درج کریں",
        "notes_label": "نوٹس (اختیاری)", "save_expense": "💾   خرچ محفوظ کریں",
        "expense_saved": "✅  Rs {amount} کے اخراجات کامیابی سے محفوظ ہو گئے!",
        "err_amount_required": "⚠  براہ کرم رقم درج کریں۔",
        "err_amount_numeric": "⚠  رقم ایک درست عدد ہونی چاہیے۔",
        "err_amount_positive": "⚠  رقم صفر سے زیادہ ہونی چاہیے۔",
        "err_date_format": "⚠  تاریخ DD-MM-YYYY فارمیٹ میں ہونی چاہیے۔",
        "err_title_required": "⚠  براہ کرم عنوان درج کریں۔",
        "cat_general": "عمومی", "cat_zakat": "زکوٰۃ", "cat_sadqa": "صدقہ",
        "cat_construction": "تعمیر",
        "pay_cash": "نقد", "pay_bank": "بینک", "pay_online": "آن لائن",
        "exp_electricity": "بجلی", "exp_gas": "گیس", "exp_water": "پانی",
        "exp_maintenance": "مرمت", "exp_salary": "تنخواہ", "exp_other": "دیگر",
        "reports": "ماہانہ رپورٹ", "select_month": "مہینہ منتخب کریں",
        "donation_by_cat": "زمرہ کے مطابق چندہ", "expense_by_cat": "زمرہ کے مطابق اخراجات",
        "all_transactions": "تمام لین دین", "print_report": "🖨  رپورٹ پرنٹ کریں",
        "net_balance": "خالص بیلنس", "no_data_month": "اس مہینے کا کوئی لین دین نہیں ملا۔",
        "report_title": "مسجد مالیاتی رپورٹ",
        "settings": "⚙  ترتیبات", "mosque_name": "مسجد کا نام",
        "address": "پتہ", "phone_number": "فون نمبر",
        "imam_name": "آپریٹر کا نام", "notes": "نوٹس",

        "theme": "تھیم", "dark_mode": "ڈارک موڈ", "light_mode": "لائٹ موڈ",
        "backup_data": "بیک اپ لیں", "restore_data": "ڈیٹا بحال کریں",
        "save_settings": "💾  ترتیبات محفوظ کریں", "settings_saved": "✅  ترتیبات محفوظ ہو گئیں!",
        "mosque_profile": "مسجد کا پروفائل", "data_management": "ڈیٹا مینجمنٹ",
        "backup_success": "✅  بیک اپ محفوظ ہو گیا:\n{path}",
        "restore_warning": "⚠  انتباہ: یہ موجودہ ڈیٹا کو مٹا دے گا!\nکیا آپ کو یقین ہے؟",
        "restore_success": "✅  ڈیٹا بحال ہو گیا! ری لوڈ ہو رہا ہے...",
        "nav_about": "ℹ️  تفصیلات", "about_project": "پروجیکٹ کے بارے میں",
        "about_developer": "ڈویلپر کے بارے میں",
        "nav_employees": "👥  ملازمین", "employees": "ملازمین", 
        "add_employee": "➕ ملازم شامل کریں", "edit_employee": "✏️ ترمیم کریں",
        "delete_employee": "🗑️ حذف کریں", "pay_salary": "💸 تنخواہ ادا کریں",
        "role": "عہدہ", "salary_amount": "ماہانہ تنخواہ", 
        "role_imam": "امام", "role_moazzin": "مؤذن", 
        "role_cleaner": "خادم", "role_other": "دیگر",
        "col_actions": "کارروائی",
        "already_paid_warning": "⚠  اس مہینے کی تنخواہ پہلے ہی دی جا چکی ہے!",
        "salary_paid_success": "✅  تنخواہ کامیابی سے ادا کر دی گئی!",
        "confirm_delete_emp": "کیا آپ واقعی {name} کو حذف کرنا چاہتے ہیں؟",
        "err_name_required": "⚠  براہ کرم نام درج کریں۔",
        "err_insufficient_balance": "⚠  ناکافی بیلنس! موجودہ: Rs {bal:,.0f}",
        "edit": "ترمیم", "delete": "حذف کریں", "confirm_delete": "کیا آپ واقعی اس لین دین کو حذف کرنا چاہتے ہیں؟",
        "last_modified": "آخری ترمیم", "lock_app": "🔒 ایپ لاک کریں", "unlock_app": "انلاک کریں",
        "change_password": "پاس ورڈ تبدیل کریں", "old_password": "پرانا پاس ورڈ",
        "new_password": "نیا پاس ورڈ", "confirm_password": "پاس ورڈ کی تصدیق کریں",
        "password_changed": "✅ پاس ورڈ کامیابی سے تبدیل ہو گیا!", "invalid_password": "⚠ موجودہ پاس ورڈ غلط ہے۔",
        "password_mismatch": "⚠ نئے پاس ورڈز مطابقت نہیں رکھتے۔",
        "app_locked": "ایپلی کیشن لاک ہے", "enter_password": "پاس ورڈ درج کریں",
        "confirm_exit": "کیا آپ واقعی پروگرام سے باہر نکلنا چاہتے ہیں؟", "exit_title": "باہر نکلنے کی تصدیق",
        "yes": "جی ہاں", "no": "نہیں", "ok": "ٹھیک ہے",
        "fund": "فنڈ", "fund_type": "فنڈ کی قسم", "fund_balance": "فنڈ بیلنس",
        "insufficient_fund_balance": "⚠ {fund} فنڈ میں بیلنس ناکافی ہے!",
        "zakat_warning": "⚠ زکوٰۃ کے فنڈز صرف جائز مقاصد کے لیے استعمال ہونے چاہئیں",
        "exp_charity": "صدقہ جاریہ / مدد",
        "audit_log": "📋 آڈٹ لاگ", "action": "عمل", "description": "تفصیل",
        "filter": "فلٹر", "date_range": "تاریخ کا انتخاب", "all": "تمام",
        "from": "سے", "to": "تک", "search": "تلاش", "generate": "جنریٹ",
        "backup_path": "بیک اپ کا راستہ", "browse": "براؤز",
        "confirm_identity": "شناخت کی تصدیق کریں", "incorrect_password": "⚠ پاس ورڈ غلط ہے",
        "print": "پرنٹ کریں", "save_and_print": "محفوظ کریں اور پرنٹ کریں",
        "err_month_locked": "⚠ ڈیٹا کی حفاظت کے لیے یہ مہینہ لاک کر دیا گیا ہے۔",
        "close_month": "مہینہ لاک کریں", "reopen_month": "مہینہ دوبارہ کھولیں",
        "month_closed": "مہینہ لاک ہے", "month_open": "مہینہ کھلا ہے",
        "imam_name": "آپریٹر کا نام", "notes": "نوٹس",
        "operator_name": "آپریٹر کا نام", "col_operator": "آپریٹر",
    },









}

# ──────────────────────────────────────────────
# DATE HELPERS
# ──────────────────────────────────────────────

def get_today_date():
    """Return today's date in DD-MM-YYYY format."""
    return datetime.now().strftime("%d-%m-%Y")

def format_date(date_str):
    """Convert various date formats to DD-MM-YYYY. Returns original if unparseable."""
    if not date_str:
        return ""
    for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return date_str

def parse_date_to_ymd(date_str):
    """Convert DD-MM-YYYY to YYYY-MM-DD for SQL storage."""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def validate_date(date_str):
    """Return True if date_str is valid DD-MM-YYYY."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def get_month_options():
    """Return list of last 12 months in MM-YYYY format, most recent first."""
    now = datetime.now()
    months = []
    for i in range(12):
        m = now.month - i
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{m:02d}-{y}")
    return months

# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────

def get_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)

def init_database():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, donor_name TEXT,
        amount REAL NOT NULL, category TEXT, payment_type TEXT, date TEXT,
        is_deleted INTEGER DEFAULT 0, created_at TEXT, updated_at TEXT,
        operator TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, amount REAL,
        category TEXT, paid_to TEXT, date TEXT, notes TEXT,
        fund_type TEXT DEFAULT 'General',
        is_deleted INTEGER DEFAULT 0, created_at TEXT, updated_at TEXT,
        operator TEXT)""")

    
    # Check for missing columns in existing tables
    for table in ["donations", "expenses"]:
        c.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in c.fetchall()]
        if "is_deleted" not in columns:
            c.execute(f"ALTER TABLE {table} ADD COLUMN is_deleted INTEGER DEFAULT 0")
        if "created_at" not in columns:
            c.execute(f"ALTER TABLE {table} ADD COLUMN created_at TEXT")
        if "updated_at" not in columns:
            c.execute(f"ALTER TABLE {table} ADD COLUMN updated_at TEXT")
        if "operator" not in columns:
            c.execute(f"ALTER TABLE {table} ADD COLUMN operator TEXT")


    # DB Upgrades for version 2
    c.execute("PRAGMA table_info(expenses)")
    columns = [col[1] for col in c.fetchall()]
    if "expense_type" not in columns:
        c.execute("ALTER TABLE expenses ADD COLUMN expense_type TEXT DEFAULT 'General'")
    if "employee_id" not in columns:
        c.execute("ALTER TABLE expenses ADD COLUMN employee_id INTEGER")
    if "fund_type" not in columns:
        c.execute("ALTER TABLE expenses ADD COLUMN fund_type TEXT DEFAULT 'General'")
        
    c.execute("""CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY, mosque_name TEXT, address TEXT,
        phone TEXT, imam_name TEXT, notes TEXT, theme TEXT, password TEXT)""")
    
    # Check for backup_path in settings
    c.execute("PRAGMA table_info(settings)")
    columns = [col[1] for col in c.fetchall()]
    if "backup_path" not in columns:
        c.execute("ALTER TABLE settings ADD COLUMN backup_path TEXT")

    c.execute("""CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        action_type TEXT, table_name TEXT, record_id INTEGER,
        description TEXT, timestamp TEXT, operator TEXT)""")

    c.execute("PRAGMA table_info(audit_log)")
    columns = [col[1] for col in c.fetchall()]
    if "operator" not in columns:
        c.execute("ALTER TABLE audit_log ADD COLUMN operator TEXT")




    
    c.execute("PRAGMA table_info(settings)")
    columns = [col[1] for col in c.fetchall()]
    if "password" not in columns:
        c.execute("ALTER TABLE settings ADD COLUMN password TEXT DEFAULT 'admin'")
        
    c.execute("INSERT OR IGNORE INTO settings (id, mosque_name, address, phone, imam_name, notes, theme, password) "
              "VALUES (1, 'Mosque Name', '', '', '', '', 'dark', 'admin')")
              
    c.execute("""CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, 
        role TEXT NOT NULL, salary REAL NOT NULL)""")

    # Performance Indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_don_date ON donations(date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_don_cat ON donations(category)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_don_del ON donations(is_deleted)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_exp_date ON expenses(date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_exp_fund ON expenses(fund_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_exp_del ON expenses(is_deleted)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_audit_date ON audit_log(timestamp)")
    
    c.execute("""CREATE TABLE IF NOT EXISTS closed_months (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        month_year TEXT UNIQUE, closed_at TEXT)""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_closed_mo ON closed_months(month_year)")


    conn.commit()
    conn.close()


def get_current_balance():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("SELECT IFNULL(SUM(amount), 0) FROM donations WHERE is_deleted=0")
    td = c.fetchone()[0]
    c.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE is_deleted=0")
    te = c.fetchone()[0]
    conn.close()
    return td - te

def log_action(action_type, table_name, record_id, description, operator=None):
    """Log an action to the audit_log table."""
    conn = sqlite3.connect(get_db_path())
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    conn.execute("""INSERT INTO audit_log 
        (action_type, table_name, record_id, description, timestamp, operator)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (action_type, table_name, record_id, description, timestamp, operator))
    conn.commit(); conn.close()


def get_fund_balances():

    """Calculate balance for each fund type."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    balances = {}
    for fund in DONATION_CAT_DB:
        c.execute("SELECT IFNULL(SUM(amount), 0) FROM donations WHERE category=? AND is_deleted=0", (fund,))
        don = c.fetchone()[0]
        c.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE fund_type=? AND is_deleted=0", (fund,))
        exp = c.fetchone()[0]
        balances[fund] = don - exp
    conn.close()
    return balances

def is_month_closed(month_year):
    """Check if a month (MM-YYYY) is closed."""
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("SELECT 1 FROM closed_months WHERE month_year=?", (month_year,))
    res = c.fetchone()
    conn.close()
    return res is not None

def check_date_lock(date_str):
    """Standard check for transaction lock by date (DD-MM-YYYY or YYYY-MM-DD)."""
    if not date_str or date_str == "—": return False
    # Standardize to MM-YYYY
    try:
        if "-" in date_str:
            parts = date_str.split("-")
            if len(parts[0]) == 4: # YYYY-MM-DD
                mo_yr = f"{parts[1]}-{parts[0]}"
            else: # DD-MM-YYYY
                mo_yr = f"{parts[1]}-{parts[2]}"
            return is_month_closed(mo_yr)
    except: pass
    return False

def close_period(month_year):
    """Lock a month for modification."""
    conn = sqlite3.connect(get_db_path())
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    conn.execute("INSERT OR IGNORE INTO closed_months (month_year, closed_at) VALUES (?,?)", (month_year, now))
    conn.commit(); conn.close()
    log_action("PERIOD_CLOSE", "closed_months", 0, f"Period {month_year} closed")

def reopen_period(month_year):
    """Unlock a month for modification."""
    conn = sqlite3.connect(get_db_path())
    conn.execute("DELETE FROM closed_months WHERE month_year=?", (month_year,))
    conn.commit(); conn.close()
    log_action("PERIOD_REOPEN", "closed_months", 0, f"Period {month_year} reopened")

def fetch_audit_logs(action_type=None, start_date=None, end_date=None):

    """Fetch audit logs with optional filters."""
    conn = sqlite3.connect(get_db_path())
    query = "SELECT timestamp, action_type, description, table_name, record_id, operator FROM audit_log WHERE 1=1"

    params = []
    
    if action_type and action_type != "All":
        query += " AND action_type = ?"
        params.append(action_type)
    
    if start_date:
        # Date in DB is DD-MM-YYYY HH:MM:SS, but we filter by date portion
        # Actually it's easier to filter by string if formatted correctly, 
        # but DD-MM-YYYY is not sortable. 
        # SQLITE can use substr(timestamp, 7, 4) || '-' || substr(timestamp, 4, 2) || '-' || substr(timestamp, 1, 2)
        # for YYYY-MM-DD comparison.
        sq_date = "substr(timestamp, 7, 4) || '-' || substr(timestamp, 4, 2) || '-' || substr(timestamp, 1, 2)"
        query += f" AND {sq_date} >= ?"
        params.append(parse_date_to_ymd(start_date))
        
    if end_date:
        sq_date = "substr(timestamp, 7, 4) || '-' || substr(timestamp, 4, 2) || '-' || substr(timestamp, 1, 2)"
        query += f" AND {sq_date} <= ?"
        params.append(parse_date_to_ymd(end_date))
        
    query += " ORDER BY timestamp DESC, id DESC LIMIT 200"
    
    c = conn.cursor()

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def get_employee_roles():


    return ["role_imam", "role_moazzin", "role_cleaner", "role_other"]

def fetch_employees():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("SELECT id, name, role, salary FROM employees ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

def check_salary_paid(emp_id, month_year):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    mm, yyyy = month_year.split("-")
    pattern = f"{yyyy}-{mm}-%"
    c.execute("SELECT 1 FROM expenses WHERE employee_id=? AND expense_type='Salary' AND date LIKE ? AND is_deleted=0", (emp_id, pattern))
    res = c.fetchone()
    conn.close()
    return res is not None

def add_employee(name, role, salary):
    conn = sqlite3.connect(get_db_path())
    c = conn.execute("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)", (name, role, salary))
    eid = c.lastrowid
    conn.commit()
    conn.close()
    log_action("CREATE", "employees", eid, f"Employee '{name}' added as {role} with salary {salary}")


def update_employee(emp_id, name, role, salary):
    conn = sqlite3.connect(get_db_path())
    conn.execute("UPDATE employees SET name=?, role=?, salary=? WHERE id=?", (name, role, salary, emp_id))
    conn.commit()
    conn.close()
    log_action("UPDATE", "employees", emp_id, f"Employee updated: {name}, {role}, Rs {salary}")


def delete_employee(emp_id):
    conn = sqlite3.connect(get_db_path())
    conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    log_action("DELETE", "employees", emp_id, "Employee record deleted")


def load_settings():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("SELECT mosque_name, address, phone, imam_name, notes, theme, password, backup_path FROM settings WHERE id=1")
    row = c.fetchone()
    conn.close()
    if row:
        return {"mosque_name": row[0], "address": row[1], "phone": row[2],
                "imam_name": row[3], "notes": row[4], "theme": row[5], "password": row[6],
                "backup_path": row[7] or ""}
    return {"mosque_name": "Mosque Name", "address": "", "phone": "",
            "imam_name": "", "notes": "", "theme": "dark", "password": "admin", "backup_path": ""}


def save_settings(data):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    # Check if we should update password
    if "password" in data:
        c.execute("""UPDATE settings SET 
            mosque_name=?, address=?, phone=?, imam_name=?, notes=?, theme=?, password=?, backup_path=? 
            WHERE id=1""", 
            (data["mosque_name"], data["address"], data["phone"], 
             data["imam_name"], data["notes"], data["theme"], data["password"], data.get("backup_path", "")))
    else:
        c.execute("""UPDATE settings SET 
            mosque_name=?, address=?, phone=?, imam_name=?, notes=?, theme=?, backup_path=? 
            WHERE id=1""", 
            (data["mosque_name"], data["address"], data["phone"], 
             data["imam_name"], data["notes"], data["theme"], data.get("backup_path", "")))
    conn.commit()
    conn.close()



def fetch_monthly_totals(filter_val=None, is_range=False):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    if is_range and filter_val:
        start, end = filter_val
        c.execute("SELECT COALESCE(SUM(amount),0) FROM donations WHERE date >= ? AND date <= ? AND is_deleted=0", (start, end))
        don = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date >= ? AND date <= ? AND is_deleted=0", (start, end))
        exp = c.fetchone()[0]
    else:
        if filter_val:
            mm, yyyy = filter_val.split("-")
            pattern = f"{yyyy}-{mm}-%"
        else:
            pattern = datetime.now().strftime("%Y-%m-") + "%"
        c.execute("SELECT COALESCE(SUM(amount),0) FROM donations WHERE date LIKE ? AND is_deleted=0", (pattern,))
        don = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date LIKE ? AND is_deleted=0", (pattern,))
        exp = c.fetchone()[0]
    conn.close()
    return don, exp

def fetch_fund_period_totals(filter_val=None, is_range=False):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    fund_totals = {} # {fund: (don, exp)}
    
    if is_range and filter_val:
        start, end = filter_val
        for fund in DONATION_CAT_DB:
            c.execute("SELECT COALESCE(SUM(amount),0) FROM donations WHERE category=? AND date >= ? AND date <= ? AND is_deleted=0", (fund, start, end))
            d = c.fetchone()[0]
            c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE fund_type=? AND date >= ? AND date <= ? AND is_deleted=0", (fund, start, end))
            e = c.fetchone()[0]
            fund_totals[fund] = (d, e)
    else:
        if filter_val:
            mm, yyyy = filter_val.split("-")
            pattern = f"{yyyy}-{mm}-%"
        else:
            pattern = datetime.now().strftime("%Y-%m-") + "%"
        for fund in DONATION_CAT_DB:
            c.execute("SELECT COALESCE(SUM(amount),0) FROM donations WHERE category=? AND date LIKE ? AND is_deleted=0", (fund, pattern))
            d = c.fetchone()[0]
            c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE fund_type=? AND date LIKE ? AND is_deleted=0", (fund, pattern))
            e = c.fetchone()[0]
            fund_totals[fund] = (d, e)
    conn.close()
    return fund_totals


def fetch_recent_transactions(limit=5):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    # Including id and updated_at for Edit UI, and fund_type/category
    c.execute(f"""
        SELECT 'Donation' AS type, donor_name, category, amount, date, id, updated_at, category as fund, operator FROM donations WHERE is_deleted=0
        UNION ALL 
        SELECT 'Expense', title, category, amount, date, id, updated_at, fund_type as fund, operator FROM expenses WHERE is_deleted=0
        ORDER BY date DESC, updated_at DESC LIMIT {limit}""")

    rows = c.fetchall()
    conn.close()
    return rows


def fetch_month_transactions(filter_val, is_range=False):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    if is_range:
        start, end = filter_val
        c.execute("""
            SELECT 'Donation', donor_name, category, amount, date, id, updated_at, category as fund, operator FROM donations 
            WHERE date >= ? AND date <= ? AND is_deleted=0
            UNION ALL 
            SELECT 'Expense', title, category, amount, date, id, updated_at, fund_type as fund, operator FROM expenses 
            WHERE date >= ? AND date <= ? AND is_deleted=0
            ORDER BY date DESC, updated_at DESC""", (start, end, start, end))

    else:
        mm, yyyy = filter_val.split("-")
        pattern = f"{yyyy}-{mm}-%"
        c.execute("""
            SELECT 'Donation', donor_name, category, amount, date, id, updated_at, category as fund, operator FROM donations 
            WHERE date LIKE ? AND is_deleted=0
            UNION ALL 
            SELECT 'Expense', title, category, amount, date, id, updated_at, fund_type as fund, operator FROM expenses 
            WHERE date LIKE ? AND is_deleted=0
            ORDER BY date DESC, updated_at DESC LIMIT 500""", (pattern, pattern))


    rows = c.fetchall()
    conn.close()
    return rows


def fetch_category_totals(filter_val=None, is_range=False):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    if is_range and filter_val:
        start, end = filter_val
        c.execute("SELECT category, SUM(amount) FROM donations WHERE date >= ? AND date <= ? AND is_deleted=0 GROUP BY category", (start, end))
        don_cats = c.fetchall()
        c.execute("SELECT category, SUM(amount) FROM expenses WHERE date >= ? AND date <= ? AND is_deleted=0 GROUP BY category", (start, end))
        exp_cats = c.fetchall()
    else:
        if filter_val:
            mm, yyyy = filter_val.split("-")
            pattern = f"{yyyy}-{mm}-%"
        else:
            pattern = datetime.now().strftime("%Y-%m-") + "%"
        c.execute("SELECT category, SUM(amount) FROM donations WHERE date LIKE ? AND is_deleted=0 GROUP BY category", (pattern,))
        don_cats = c.fetchall()
        c.execute("SELECT category, SUM(amount) FROM expenses WHERE date LIKE ? AND is_deleted=0 GROUP BY category", (pattern,))
        exp_cats = c.fetchall()
    conn.close()
    return don_cats, exp_cats

def soft_delete_transaction(t_type, t_id):
    table = "donations" if t_type == "Donation" else "expenses"
    conn = sqlite3.connect(get_db_path())
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    conn.execute(f"UPDATE {table} SET is_deleted=1, updated_at=? WHERE id=?", (now, t_id))
    conn.commit()
    conn.close()
    log_action("DELETE", table, t_id, f"{t_type} record marked as deleted")


def update_transaction(t_type, t_id, data):
    table = "donations" if t_type == "Donation" else "expenses"
    conn = sqlite3.connect(get_db_path())
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    
    if t_type == "Donation":
        conn.execute("""UPDATE donations SET 
            donor_name=?, amount=?, category=?, payment_type=?, date=?, updated_at=?, operator=?
            WHERE id=?""", 
            (data["donor_name"], data["amount"], data["category"], 
             data["payment_type"], data["date"], now, data.get("operator", ""), t_id))
    else:
        conn.execute("""UPDATE expenses SET 
            title=?, amount=?, category=?, paid_to=?, date=?, notes=?, updated_at=?, operator=?
            WHERE id=?""", 
            (data["title"], data["amount"], data["category"], 
             data["paid_to"], data["date"], data["notes"], now, data.get("operator", ""), t_id))

    conn.commit()
    conn.close()

def fetch_category_totals(filter_val, is_range=False):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    if is_range:
        start, end = filter_val
        c.execute("SELECT category, SUM(amount) FROM donations WHERE date >= ? AND date <= ? AND is_deleted=0 GROUP BY category", (start, end))
        don_cats = c.fetchall()
        c.execute("SELECT category, SUM(amount) FROM expenses WHERE date >= ? AND date <= ? AND is_deleted=0 GROUP BY category", (start, end))
        exp_cats = c.fetchall()
    else:
        mm, yyyy = filter_val.split("-")
        pattern = f"{yyyy}-{mm}-%"
        c.execute("SELECT category, SUM(amount) FROM donations WHERE date LIKE ? AND is_deleted=0 GROUP BY category", (pattern,))
        don_cats = c.fetchall()
        c.execute("SELECT category, SUM(amount) FROM expenses WHERE date LIKE ? AND is_deleted=0 GROUP BY category", (pattern,))
        exp_cats = c.fetchall()

    conn.close()
    return don_cats, exp_cats

# ──────────────────────────────────────────────
# UI HELPERS
# ──────────────────────────────────────────────

def make_card(parent, title, value, accent_color, row, col):
    card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=14,
                        border_width=1, border_color=COLOR_BORDER)
    card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    ctk.CTkFrame(card, fg_color=accent_color, height=4, corner_radius=2).pack(
        fill="x", padx=16, pady=(16, 0))
    ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=13),
                 text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=18, pady=(12, 0))
    vl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                      text_color=COLOR_TEXT, anchor="w")
    vl.pack(fill="x", padx=18, pady=(4, 18))
    return card, vl

# ──────────────────────────────────────────────
# THEMED DIALOGUE
# ──────────────────────────────────────────────

class ThemedMessagebox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, type="info", options=["OK"]):
        super().__init__(parent)
        self.title(title)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.configure(fg_color=COLOR_CARD)
        
        self.result = None
        self.options = options
        
        # Center on parent
        w, h = 420, 240
        try:
            parent.update_idletasks()
            px = parent.winfo_x() + (parent.winfo_width() // 2) - (w // 2)
            py = parent.winfo_y() + (parent.winfo_height() // 2) - (h // 2)
            self.geometry(f"{w}x{h}+{px}+{py}")
        except:
            self.geometry(f"{w}x{h}")
        
        icon = "ℹ️"
        if type == "question": icon = "❓"
        elif type == "warning": icon = "⚠️"
        elif type == "error": icon = "❌"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=0, sticky="nsew", padx=30, pady=25)
        
        ctk.CTkLabel(main, text=icon, font=ctk.CTkFont(size=44)).pack(pady=(0, 10))
        
        msg_lbl = ctk.CTkLabel(main, text=message, font=ctk.CTkFont(family=URDU_FONT if parent.lang == "ur" else DEFAULT_FONT, size=15), 
                               text_color=COLOR_TEXT, wraplength=350, justify="center")
        msg_lbl.pack(fill="x")
        
        btn_f = ctk.CTkFrame(self, fg_color=COLOR_BG_DARK, height=64, corner_radius=0)
        btn_f.grid(row=1, column=0, sticky="ew")
        
        def set_res(r):
            self.result = r
            self.destroy()

        for opt in reversed(options):
            is_accent = opt in ["OK", "Yes", "جی ہاں", "ٹھیک ہے"]
            b_color = COLOR_ACCENT if is_accent else COLOR_CARD
            t_color = "#0f172a" if is_accent else COLOR_TEXT
            
            if opt in ["Delete", "حذف کریں"]: 
                b_color = COLOR_RED
                t_color = "#ffffff"

            btn = ctk.CTkButton(btn_f, text=opt, width=100, height=36, font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color=b_color, text_color=t_color, border_width=1 if not is_accent else 0,
                                border_color=COLOR_BORDER if not is_accent else None,
                                command=lambda o=opt: set_res(o))
            btn.pack(side="right", padx=15, pady=14)

        self.grab_set()
        self.wait_window()

# ──────────────────────────────────────────────
# MAIN APPLICATION
# ──────────────────────────────────────────────

class MosqueApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.mosque_profile = load_settings()
        self.lang = "en"
        self.current_view = "dashboard"
        self.is_locked = True
        self.last_interaction_time = time.time()
        self.title(APP_TITLE)
        self.configure(fg_color=COLOR_BG_DARK)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._build_sidebar()
        self._build_content_area()
        self._show_lock_screen()
        self._update_clock() # Start dynamic clock
        self._check_inactivity() # Start inactivity check
        
        # Maximize after all elements are loaded
        self.update() # Force geometry calculations
        self.after(100, lambda: self.state("zoomed")) # Delayed maximize for Windows reliably
        
        # Bind activity events to reset inactivity timer
        self.bind_all("<Any-KeyPress>", self._reset_inactivity_timer)
        self.bind_all("<Any-Button>", self._reset_inactivity_timer)
        self.bind_all("<Motion>", self._reset_inactivity_timer)
        
        # Protocol for closing app
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        # Auto-backup before exit
        self._do_database_backup(auto=True)
        self.destroy()

    def _do_database_backup(self, path=None, auto=False):
        """Perform database backup with rotation (keep last 10)."""
        # Determine target directory
        d = path or self.mosque_profile.get("backup_path", "").strip()
        if not d and not auto:
            d = filedialog.askdirectory()
        
        if not d:
            if not auto: self.error("Error", "No backup directory selected.")
            return

        if not os.path.exists(d):
            try: os.makedirs(d)
            except: return

        # Perform copy
        tstr = datetime.now().strftime("%d%m%Y_%I%M%p")
        fname = f"backup_{tstr}.db" if not auto else f"auto_backup_{tstr}.db"
        fp = os.path.join(d, fname)
        
        try:
            import shutil
            shutil.copy2(get_db_path(), fp)
            if not auto:
                self.info("Backup", self.t("backup_success").format(path=fp))
            log_action("BACKUP", "maintenance", 0, f"Database backup created: {fname}")
            
            # Rotation: Keep last 10
            files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".db") and ("auto_backup" in f or "backup_" in f)]
            files.sort(key=os.path.getmtime, reverse=True)
            
            if len(files) > 10:
                for old_f in files[10:]:
                    try: os.remove(old_f)
                    except: pass
                    
        except Exception as ex:
            if not auto: self.error("Backup Error", str(ex))

    def confirm(self, title, message):

        opts = [self.t("yes"), self.t("no")]
        res = ThemedMessagebox(self, title, message, type="question", options=opts).result
        return res in ["Yes", "جی ہاں"]

    def info(self, title, message):
        ThemedMessagebox(self, title, message, type="info", options=[self.t("ok")]).result

    def error(self, title, message):
        ThemedMessagebox(self, title, message, type="error", options=[self.t("ok")]).result

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)

    def _get_font(self, size=14, weight="normal", fixed_size=False):
        family = URDU_FONT if self.lang == "ur" else DEFAULT_FONT
        actual_size = size + 4 if (self.lang == "ur" and not fixed_size) else size
        return ctk.CTkFont(family=family, size=actual_size, weight=weight)

    # ────────── Sidebar ──────────

    def _build_sidebar(self):
        if hasattr(self, "sidebar"):
            self.sidebar.destroy()
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=COLOR_SIDEBAR,
                                     corner_radius=0, border_width=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tf = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        tf.pack(fill="x", padx=16, pady=(24, 8))
        ctk.CTkLabel(tf, text="🕌", font=ctk.CTkFont(size=28), anchor="w").pack(anchor="w")
        m_name = self.mosque_profile.get("mosque_name", "").strip() or self.t("app_name")
        m_addr = self.mosque_profile.get("address", "").strip() or self.t("app_subtitle")
        
        ctk.CTkLabel(tf, text=m_name, font=self._get_font(18, "bold", fixed_size=True),
                     text_color=COLOR_TEXT, anchor="w", justify="left", wraplength=180).pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(tf, text=m_addr, font=self._get_font(11, fixed_size=True),
                     text_color=COLOR_TEXT_DIM, anchor="w", justify="left", wraplength=180).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, fg_color=COLOR_BORDER, height=1).pack(
            fill="x", padx=16, pady=(16, 12))
        ctk.CTkLabel(self.sidebar, text=f"  {self.t('navigation')}",
                     font=self._get_font(10, "bold", fixed_size=True), text_color=COLOR_TEXT_DIM,
                     anchor="w").pack(fill="x", padx=16, pady=(0, 6))

        self.btn_dashboard = self._make_nav_button(self.t("nav_dashboard"), self._show_dashboard, "dashboard")
        self.btn_donation = self._make_nav_button(self.t("nav_add_donation"), self._show_add_donation, "donation")
        self.btn_expense = self._make_nav_button(self.t("nav_add_expense"), self._show_add_expense, "expense")
        self.btn_employees = self._make_nav_button(self.t("nav_employees"), self._show_employees, "employees")
        self.btn_reports = self._make_nav_button(self.t("nav_reports"), self._show_reports, "reports")
        self.btn_audit = self._make_nav_button(self.t("audit_log"), self._show_audit_log, "audit")

        self.btn_settings = self._make_nav_button(self.t("settings"), self._show_settings, "settings")
        self.btn_about = self._make_nav_button(self.t("nav_about"), self._show_about, "about")
        self._highlight_active_nav()

        ctk.CTkFrame(self.sidebar, fg_color=COLOR_BORDER, height=1).pack(
            fill="x", padx=16, pady=(16, 12))
        
        # Lock Button
        ctk.CTkButton(self.sidebar, text=self.t("lock_app"), font=self._get_font(14, fixed_size=True),
                      fg_color="transparent", hover_color="#451a1a",
                      text_color="#ef4444", anchor="w", height=42, corner_radius=10,
                      command=self._lock_app).pack(fill="x", padx=12, pady=3)

        sw = "🌐  اردو" if self.lang == "en" else "🌐  English"
        ctk.CTkButton(self.sidebar, text=sw, font=self._get_font(14, fixed_size=True),
                      fg_color="transparent", hover_color=COLOR_CARD_HOVER,
                      text_color=COLOR_TEXT, anchor="w", height=42, corner_radius=10,
                      command=self._toggle_language).pack(fill="x", padx=12, pady=3)

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)
        ctk.CTkLabel(self.sidebar, text=self.t("version_footer"), font=self._get_font(10, fixed_size=True),
                     text_color=COLOR_TEXT_DIM).pack(side="bottom", pady=(0, 16))

    def _make_nav_button(self, text, command, view_name):
        btn = ctk.CTkButton(self.sidebar, text=text, font=self._get_font(14, fixed_size=True),
                            fg_color="transparent", hover_color=COLOR_CARD_HOVER,
                            text_color=COLOR_TEXT, anchor="w", height=42, corner_radius=10,
                            command=lambda v=view_name, c=command: self._nav_click(v, c))
        btn.pack(fill="x", padx=12, pady=3)
        return btn

    def _nav_click(self, view_name, command):
        if self.is_locked:
            return
        self.current_view = view_name
        self._highlight_active_nav()
        command()

    def _highlight_active_nav(self):
        if self.is_locked:
            return
        for name, btn in {"dashboard": self.btn_dashboard, "donation": self.btn_donation,
                          "expense": self.btn_expense, "employees": self.btn_employees,
                          "reports": self.btn_reports, "audit": self.btn_audit,
                          "settings": self.btn_settings, "about": self.btn_about}.items():

            if name == self.current_view:
                btn.configure(fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                              text_color="#0f172a")
            else:
                btn.configure(fg_color="transparent", hover_color=COLOR_CARD_HOVER,
                              text_color=COLOR_TEXT)

    def _toggle_language(self):
        if self.is_locked:
            return
        self.lang = "ur" if self.lang == "en" else "en"
        self._build_sidebar()
        self._refresh_current_view()

    def _refresh_current_view(self):
        if self.is_locked:
            self._show_lock_screen()
            return
        {"dashboard": self._show_dashboard, "donation": self._show_add_donation,
         "expense": self._show_add_expense, "reports": self._show_reports,
         "audit": self._show_audit_log, "employees": self._show_employees,
         "settings": self._show_settings, "about": self._show_about}.get(self.current_view, self._show_dashboard)()


    def _update_clock(self):
        """Update live clock on dashboard if it exists."""
        now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        if hasattr(self, "clock_label") and self.clock_label.winfo_exists():
            self.clock_label.configure(text=f"📅  {now}")
        self.after(1000, self._update_clock)

    def _reset_inactivity_timer(self, event=None):
        """Reset the last interaction time."""
        self.last_interaction_time = time.time()

    def _check_inactivity(self):
        """Check for inactivity and lock app after 10 minutes (600s)."""
        if not self.is_locked:
            elapsed = time.time() - self.last_interaction_time
            if elapsed > 600: # 10 minutes
                self._lock_app(reason="Auto")

        # Check every 5 seconds
        self.after(5000, self._check_inactivity)

    def _lock_app(self, reason="Manual"):
        self.is_locked = True
        msg = "Application auto-locked due to inactivity" if reason == "Auto" else "Application locked by user"
        log_action("LOGOUT", "security", 0, msg)
        self._highlight_active_nav()
        self._show_lock_screen()



    def _show_lock_screen(self):
        self._clear_content()
        
        main = ctk.CTkFrame(self.content, fg_color="transparent")
        main.pack(expand=True)
        
        lock_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=20, border_width=1, border_color=COLOR_BORDER)
        lock_card.pack(padx=40, pady=40)
        
        ctk.CTkLabel(lock_card, text="🔒", font=ctk.CTkFont(size=60)).pack(pady=(40, 10))
        ctk.CTkLabel(lock_card, text=self.t("app_locked"), font=self._get_font(24, "bold"), text_color=COLOR_TEXT).pack(pady=10, padx=60)
        ctk.CTkLabel(lock_card, text=self.t("enter_password"), font=self._get_font(14), text_color=COLOR_TEXT_DIM).pack(pady=(0, 20))
        
        pw_entry = ctk.CTkEntry(lock_card, show="*", width=260, height=45, font=self._get_font(16), placeholder_text="••••••••")
        pw_entry.pack(pady=10)
        # Use delay to ensure focus sticks after window is mapped/zoomed
        self.after(200, lambda: [pw_entry.focus_force(), pw_entry.focus()])
        
        err_lbl = ctk.CTkLabel(lock_card, text="", text_color="#ef4444", font=self._get_font(12))
        err_lbl.pack()
        
        def attempt_unlock(event=None):
            if pw_entry.get() == self.mosque_profile.get("password", "admin"):
                self.is_locked = False
                log_action("LOGIN", "security", 0, "Application unlocked successfully")
                self._highlight_active_nav()
                self._show_dashboard()

            else:
                err_lbl.configure(text=self.t("invalid_password"))
                pw_entry.delete(0, "end")

        pw_entry.bind("<Return>", attempt_unlock)
        ctk.CTkButton(lock_card, text=self.t("unlock_app"), font=self._get_font(14, "bold"),
                      fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#0f172a",
                      height=45, width=260, corner_radius=10, command=attempt_unlock).pack(pady=(20, 40))

    def _show_password_prompt(self, title, message, callback):
        """Show a modal password dialog for critical actions."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog manually
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 125
        dialog.geometry(f"+{x}+{y}")

        f = ctk.CTkFrame(dialog, fg_color=COLOR_CARD, corner_radius=12)
        f.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(f, text=message, font=self._get_font(14), text_color=COLOR_TEXT, wraplength=340).pack(pady=(20, 10))
        
        pw_e = ctk.CTkEntry(f, show="*", width=300, height=40, font=self._get_font(15), placeholder_text="••••••••")
        pw_e.pack(pady=10)
        pw_e.focus()
        
        err_l = ctk.CTkLabel(f, text="", font=self._get_font(12), text_color="#ef4444")
        err_l.pack()
        
        def check():
            if pw_e.get() == self.mosque_profile.get("password", "admin"):
                dialog.destroy()
                callback()
            else:
                err_l.configure(text=self.t("incorrect_password"))
                pw_e.delete(0, "end")

        pw_e.bind("<Return>", lambda e: check())
        
        btns = ctk.CTkFrame(f, fg_color="transparent")
        btns.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(btns, text=self.t("no"), width=140, height=36, fg_color=COLOR_BORDER, text_color=COLOR_TEXT, command=dialog.destroy).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns, text=self.t("yes"), width=140, height=36, fg_color=COLOR_ACCENT, text_color="#0f172a", command=check).pack(side="right")


    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _get_donation_categories(self):
        return [self.t(k) for k in DONATION_CAT_KEYS]

    def _get_payment_types(self):
        return [self.t(k) for k in PAYMENT_TYPE_KEYS]

    def _get_expense_categories(self):
        return [self.t(k) for k in EXPENSE_CAT_KEYS]

    def _resolve_combo_to_db(self, displayed, keys, db_vals):
        for key, db in zip(keys, db_vals):
            if self.t(key) == displayed:
                return db
        return displayed

    # ──────────────────────────────────────────
    # DASHBOARD
    # ──────────────────────────────────────────

    def _show_dashboard(self):
        self._clear_content()
        self.current_view = "dashboard"
        self._highlight_active_nav()

        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        header = ctk.CTkFrame(wrapper, fg_color="transparent")
        header.pack(fill="x")
        
        # Dashboard Live Clock (Top Left as per request)
        self.clock_label = ctk.CTkLabel(header, text="", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w")
        self.clock_label.pack(side="left")
        
        ctk.CTkLabel(header, text=self.t("dashboard"), font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="e").pack(side="right")

        don, exp = fetch_monthly_totals()
        bal = don - exp
        cf = ctk.CTkFrame(wrapper, fg_color="transparent")
        cf.pack(fill="x", pady=(16, 0))
        cf.columnconfigure((0, 1, 2), weight=1)
        make_card(cf, self.t("total_donations"), f"Rs {don:,.0f}", COLOR_GREEN, 0, 0)
        make_card(cf, self.t("total_expenses"), f"Rs {exp:,.0f}", COLOR_RED, 0, 1)
        make_card(cf, self.t("current_balance"), f"Rs {bal:,.0f}", COLOR_ACCENT, 0, 2)

        # Fund Balances Section
        ctk.CTkLabel(wrapper, text=self.t("fund_balance"), font=self._get_font(16, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(24, 0))
        
        fb_frame = ctk.CTkFrame(wrapper, fg_color="transparent")
        fb_frame.pack(fill="x", pady=(10, 0))
        fb_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        fund_bals = get_fund_balances()
        for i, fund in enumerate(DONATION_CAT_DB):
            f_bal = fund_bals.get(fund, 0)
            f_label = self.t("cat_" + fund.lower())
            
            f_card = ctk.CTkFrame(fb_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            f_card.grid(row=0, column=i, padx=5, sticky="nsew")
            
            ctk.CTkLabel(f_card, text=f_label, font=self._get_font(12), text_color=COLOR_TEXT_DIM).pack(pady=(12, 0))
            ctk.CTkLabel(f_card, text=f"Rs {f_bal:,.0f}", font=self._get_font(15, "bold"), text_color=COLOR_TEXT).pack(pady=(2, 12))


        ctk.CTkLabel(wrapper, text=self.t("recent_transactions"), font=self._get_font(16, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(24, 8))

        txns = fetch_recent_transactions(5)
        tf = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=12,
                          border_width=1, border_color=COLOR_BORDER)
        tf.pack(fill="x")

        if not txns:
            ctk.CTkLabel(tf, text=self.t("no_transactions"), font=self._get_font(13),
                         text_color=COLOR_TEXT_DIM, pady=30).pack()
        else:
            # Table Configuration
            tf.columnconfigure((0, 1, 2, 3, 4), weight=1)
            tf.columnconfigure(5, weight=0) # Actions column
            
            # Header row
            headers = ["col_type", "col_amount", "fund", "col_date", "col_operator", "col_actions"]
            for i, k in enumerate(headers):
                ctk.CTkLabel(tf, text=self.t(k), font=self._get_font(12, "bold"),
                             text_color=COLOR_TEXT_DIM, anchor="w", justify="left").grid(
                                 row=0, column=i, sticky="w", padx=(20 if i > 0 else 16), pady=(14, 6))
            
            # Header separator
            ctk.CTkFrame(tf, fg_color=COLOR_BORDER, height=1).grid(row=1, column=0, columnspan=6, sticky="ew", padx=16)



            for idx, txn_row in enumerate(txns):
                t_type, name, cat, amount, date, t_id, updated_at, fund, op_val = txn_row
                is_don = t_type == "Donation"

                bc = COLOR_GREEN if is_don else COLOR_RED
                bt = self.t("type_donation") if is_don else self.t("type_expense")
                
                # Column 0: Type
                ctk.CTkLabel(tf, text=f"  {bt}  ", font=self._get_font(11, "bold"),
                             text_color="#0f172a", fg_color=bc, corner_radius=6,
                             width=90, anchor="center").grid(row=idx+2, column=0, sticky="w", padx=16, pady=8)
                
                # Column 1: Amount
                sign = "+" if is_don else "-"
                ctk.CTkLabel(tf, text=f"{sign} Rs {amount:,.0f}", font=self._get_font(14, "bold"),
                             text_color=bc, anchor="w").grid(row=idx+2, column=1, sticky="w", padx=20)
                
                # Column 2: Fund
                fund_tr = self.t("cat_" + fund.lower()) if fund else "—"
                ctk.CTkLabel(tf, text=fund_tr, font=self._get_font(12),
                             text_color=COLOR_TEXT, anchor="w").grid(row=idx+2, column=2, sticky="w", padx=20)
                
                # Column 3: Date
                ctk.CTkLabel(tf, text=format_date(date) if date else "—", font=self._get_font(12),
                             text_color=COLOR_TEXT_DIM, anchor="w").grid(row=idx+2, column=3, sticky="w", padx=20)
                
                # Column 4: Operator
                ctk.CTkLabel(tf, text=op_val or "—", font=self._get_font(11),
                             text_color=COLOR_TEXT_DIM, anchor="w").grid(row=idx+2, column=4, sticky="w", padx=20)

                
                # Column 5: Actions
                act_f = ctk.CTkFrame(tf, fg_color="transparent")
                act_f.grid(row=idx+2, column=5, sticky="e", padx=16)

                
                ctk.CTkButton(act_f, text=self.t("print"), width=60, height=28, font=self._get_font(11),
                              fg_color="transparent", border_width=1, border_color=COLOR_ACCENT,
                              text_color=COLOR_ACCENT, hover_color=COLOR_CARD_HOVER,
                              command=lambda t=t_type, i=t_id: self._print_receipt(t, i)).pack(side="left", padx=4)



                ctk.CTkButton(act_f, text=self.t("edit"), width=50, height=28, font=self._get_font(11),
                              fg_color="transparent", border_width=1, border_color=COLOR_BORDER,
                              command=lambda t=t_type, i=t_id: self._handle_edit(t, i, None)).pack(side="left", padx=4)
                
                ctk.CTkButton(act_f, text=self.t("delete"), width=50, height=28, font=self._get_font(11),
                              fg_color="transparent", border_width=1, border_color="#ef4444",
                              text_color="#ef4444", hover_color="#451a1a",
                              command=lambda t=t_type, i=t_id: self._handle_delete(t, i)).pack(side="left")

            
            # Bottom spacing
            ctk.CTkFrame(tf, fg_color="transparent", height=8).grid(row=len(txns)+2, column=0)


    def _print_receipt(self, t_type, t_id):
        """Generate and open a text receipt for a transaction."""
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        table = "donations" if t_type == "Donation" else "expenses"
        c.execute(f"SELECT * FROM {table} WHERE id=?", (t_id,))
        row = c.fetchone()
        conn.close()
        
        if not row: return
        
        # Ensure receipts directory exists
        r_dir = os.path.join(os.getcwd(), "receipts")
        if not os.path.exists(r_dir): os.makedirs(r_dir)
        
        m_name = self.mosque_profile.get("mosque_name", "Mosque Management System")
        m_phone = self.mosque_profile.get("phone", "")
        
        # Extract data based on table schema
        if t_type == "Donation":
            # (id, donor, amount, cat, pay, date, is_del, created, updated)
            name, amt, cat, date = row[1], row[2], row[3], row[5]
            label_name = "Donor Name"
        else:
            # (id, title, amount, cat, paid_to, date, notes, fund, ...)
            name, amt, cat, date = row[1], row[2], row[3], row[5]
            label_name = "Description"

        receipt_content = f"""
==========================================
        {m_name.upper()}
==========================================
RECEIPT: {t_type.upper()}
ID: {t_id} | DATE: {format_date(date)}
------------------------------------------
{label_name}: {name}
AMOUNT: Rs {amt:,.0f}
CATEGORY: {cat}
------------------------------------------
Phone: {m_phone}
Generated on: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}
==========================================
        THANK YOU
==========================================
"""
        
        fpath = os.path.join(r_dir, f"receipt_{t_type.lower()}_{t_id}.txt")
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(receipt_content)
            os.startfile(fpath) # Open for printing
        except Exception as ex:
            self.error("Error", f"Could not generate receipt: {ex}")

    def _handle_edit(self, t_type, t_id, t_data):
        # We need to fetch the full data for edit
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        table = "donations" if t_type == "Donation" else "expenses"
        c.execute(f"SELECT * FROM {table} WHERE id=?", (t_id,))
        row = c.fetchone()
        conn.close()
        
        if not row: return

        # Check for Month Lock
        if check_date_lock(row[5]):
            self.error("Lock Error", self.t("err_month_locked"))
            return
        
        if t_type == "Donation":

            # (id, donor_name, amount, category, payment_type, date, is_deleted, created_at, updated_at)
            full_data = {"donor_name": row[1], "amount": row[2], "category": row[3], "payment_type": row[4], "date": row[5]}
            self._show_add_donation(t_id, full_data)
        else:
            # (id, title, amount, category, paid_to, date, notes, fund_type, expense_type, employee_id, is_deleted, created_at, updated_at)
            # Find fund_type index - after notes (row[6])
            # PRAGMA table_info says: id(0), title(1), amount(2), category(3), paid_to(4), date(5), notes(6), fund_type(7)
            full_data = {"title": row[1], "amount": row[2], "category": row[3], "paid_to": row[4], "date": row[5], "notes": row[6], "fund_type": row[7]}
            self._show_add_expense(t_id, full_data)


    def _handle_delete(self, t_type, t_id):
        # Check for Month Lock
        # Need date first
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        table = "donations" if t_type == "Donation" else "expenses"
        c.execute(f"SELECT date FROM {table} WHERE id=?", (t_id,))
        r = c.fetchone()
        conn.close()
        if r and check_date_lock(r[0]):
            self.error("Lock Error", self.t("err_month_locked"))
            return

        from tkinter import messagebox

        if messagebox.askyesno(self.t("delete"), self.t("confirm_delete")):
            soft_delete_transaction(t_type, t_id)
            self._refresh_current_view()

    # ──────────────────────────────────────────
    # ADD DONATION
    # ──────────────────────────────────────────

    def _show_add_donation(self, edit_id=None, edit_data=None):
        self._clear_content()
        self.current_view = "donation"
        self._highlight_active_nav()

        is_edit = edit_id is not None
        title_text = self.t("edit") if is_edit else self.t("add_donation")

        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=title_text, font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")
        ctk.CTkButton(hdr, text=self.t("back_to_dashboard"), font=self._get_font(13),
                      fg_color="transparent", hover_color=COLOR_CARD_HOVER,
                      text_color=COLOR_TEXT_DIM, height=34, corner_radius=8,
                      border_width=1, border_color=COLOR_BORDER,
                      command=lambda: self._nav_click("dashboard", self._show_dashboard)).pack(side="right")
        ctk.CTkLabel(wrapper, text=self.t("add_donation_desc"), font=self._get_font(13),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(4, 20))

        fc = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=14,
                          border_width=1, border_color=COLOR_BORDER)
        fc.pack(fill="x")
        fi = ctk.CTkFrame(fc, fg_color="transparent")
        fi.pack(fill="x", padx=28, pady=28)

        ctk.CTkLabel(fi, text=self.t("donor_name"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_donor = ctk.CTkEntry(fi, height=44, corner_radius=10,
                               placeholder_text=self.t("donor_placeholder"), font=self._get_font(15))
        if is_edit: e_donor.insert(0, edit_data.get("donor_name", ""))
        e_donor.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(fi, text=self.t("amount_label"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_amt = ctk.CTkEntry(fi, height=44, corner_radius=10,
                             placeholder_text=self.t("amount_placeholder"), font=self._get_font(15))
        if is_edit: e_amt.insert(0, str(edit_data.get("amount", "")))
        e_amt.pack(fill="x", pady=(0, 16))

        rf = ctk.CTkFrame(fi, fg_color="transparent")
        rf.pack(fill="x", pady=(0, 16))
        rf.columnconfigure((0, 1), weight=1)

        lf = ctk.CTkFrame(rf, fg_color="transparent")
        lf.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(lf, text=self.t("category"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        dc = self._get_donation_categories()
        cb_cat = ctk.CTkComboBox(lf, values=dc, height=44, corner_radius=10,
                                 font=self._get_font(15), dropdown_font=self._get_font(14), state="readonly")
        if is_edit: cb_cat.set(edit_data.get("category", dc[0]))
        else: cb_cat.set(dc[0])
        cb_cat.pack(fill="x")

        rt = ctk.CTkFrame(rf, fg_color="transparent")
        rt.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(rt, text=self.t("payment_type"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        pt = self._get_payment_types()
        cb_pay = ctk.CTkComboBox(rt, values=pt, height=44, corner_radius=10,
                                 font=self._get_font(15), dropdown_font=self._get_font(14), state="readonly")
        if is_edit: cb_pay.set(edit_data.get("payment_type", pt[0]))
        else: cb_pay.set(pt[0])
        cb_pay.pack(fill="x")

        ctk.CTkLabel(fi, text=self.t("date_label"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_date = ctk.CTkEntry(fi, height=44, corner_radius=10, font=self._get_font(15))
        if is_edit: e_date.insert(0, format_date(edit_data.get("date", "")))
        else: e_date.insert(0, get_today_date())
        e_date.pack(fill="x", pady=(0, 16))





        status = ctk.CTkLabel(fi, text="", font=self._get_font(14, "bold"), anchor="w")
        status.pack(fill="x", pady=(0, 6))

        def save(print_after=False):
            at = e_amt.get().strip()

            if not at:
                status.configure(text=self.t("err_amount_required"), text_color=COLOR_AMBER); return
            try:
                av = float(at)
            except ValueError:
                status.configure(text=self.t("err_amount_numeric"), text_color=COLOR_AMBER); return
            if av <= 0:
                status.configure(text=self.t("err_amount_positive"), text_color=COLOR_AMBER); return
            dt = e_date.get().strip()
            if dt and not validate_date(dt):
                status.configure(text=self.t("err_date_format"), text_color=COLOR_AMBER); return

            donor = e_donor.get().strip() or "Anonymous"
            cat = self._resolve_combo_to_db(cb_cat.get(), DONATION_CAT_KEYS, DONATION_CAT_DB)
            pay = self._resolve_combo_to_db(cb_pay.get(), PAYMENT_TYPE_KEYS, PAYMENT_TYPE_DB)
            ds = parse_date_to_ymd(dt) if dt else datetime.now().strftime("%Y-%m-%d")
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            op = self.mosque_profile.get("imam_name", "")


            if is_edit:
                update_transaction("Donation", edit_id, {
                    "donor_name": donor, "amount": av, "category": cat,
                    "payment_type": pay, "date": ds, "operator": op
                })
                log_action("UPDATE", "donations", edit_id, f"Donation updated. Amount: {edit_data.get('amount')} -> {av}, Cat: {edit_data.get('category')} -> {cat}", operator=op)
                
                if print_after:
                    self._print_receipt("Donation", edit_id)
                self._show_dashboard()
            else:
                conn = sqlite3.connect(get_db_path())
                c = conn.execute("INSERT INTO donations (donor_name,amount,category,payment_type,date,is_deleted,created_at,updated_at,operator) VALUES (?,?,?,?,?,?,?,?,?)",
                             (donor, av, cat, pay, ds, 0, now, now, op))
                did = c.lastrowid
                conn.commit(); conn.close()
                log_action("CREATE", "donations", did, f"Donation of {av} added from {donor} for {cat}", operator=op)
                e_donor.delete(0, "end"); e_amt.delete(0, "end")

                cb_cat.set(dc[0]); cb_pay.set(pt[0])
                e_date.delete(0, "end"); e_date.insert(0, get_today_date())
                status.configure(text=self.t("donation_saved").format(amount=f"{av:,.0f}"), text_color=COLOR_GREEN)

                
                if print_after:
                    self._print_receipt("Donation", did)


            status.configure(text=self.t("donation_saved").format(amount=f"{av:,.0f}"), text_color=COLOR_GREEN)

        br = ctk.CTkFrame(fi, fg_color="transparent")
        br.pack(fill="x", pady=(4, 0))
        br.columnconfigure((0, 1, 2), weight=1)
        
        # Save & Print
        ctk.CTkButton(br, text=self.t("save_and_print"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#0f172a",
                      height=50, corner_radius=12, 
                      command=lambda: save(print_after=True)).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Save Donation
        ctk.CTkButton(br, text=self.t("save_donation"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_GREEN, hover_color="#22c55e", text_color="#0f172a",
                      height=50, corner_radius=12, 
                      command=lambda: save(print_after=False)).grid(row=0, column=1, sticky="ew", padx=5)
        
        # Back
        ctk.CTkButton(br, text=self.t("go_dashboard"), font=self._get_font(13),
                      fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER, text_color=COLOR_TEXT,
                      height=50, corner_radius=12,
                      command=lambda: self._nav_click("dashboard", self._show_dashboard)).grid(row=0, column=2, sticky="ew", padx=(5, 0))


    # ──────────────────────────────────────────
    # ADD EXPENSE
    # ──────────────────────────────────────────

    def _show_add_expense(self, edit_id=None, edit_data=None):
        self._clear_content()
        self.current_view = "expense"
        self._highlight_active_nav()

        is_edit = edit_id is not None
        title_text = self.t("edit") if is_edit else self.t("add_expense")

        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=title_text, font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")
        ctk.CTkButton(hdr, text=self.t("back_to_dashboard"), font=self._get_font(13),
                      fg_color="transparent", hover_color=COLOR_CARD_HOVER,
                      text_color=COLOR_TEXT_DIM, height=34, corner_radius=8,
                      border_width=1, border_color=COLOR_BORDER,
                      command=lambda: self._nav_click("dashboard", self._show_dashboard)).pack(side="right")
        ctk.CTkLabel(wrapper, text=self.t("add_expense_desc"), font=self._get_font(13),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(4, 20))

        fc = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=14,
                          border_width=1, border_color=COLOR_BORDER)
        fc.pack(fill="x")
        fi = ctk.CTkFrame(fc, fg_color="transparent")
        fi.pack(fill="x", padx=28, pady=28)

        rf1 = ctk.CTkFrame(fi, fg_color="transparent")
        rf1.pack(fill="x", pady=(0, 16))
        rf1.columnconfigure((0, 1), weight=1)

        f_t = ctk.CTkFrame(rf1, fg_color="transparent")
        f_t.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(f_t, text=self.t("expense_title"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_title = ctk.CTkEntry(f_t, height=44, corner_radius=10,
                               placeholder_text=self.t("expense_title_placeholder"), font=self._get_font(15))
        if is_edit: e_title.insert(0, edit_data.get("title", ""))
        e_title.pack(fill="x")

        f_a = ctk.CTkFrame(rf1, fg_color="transparent")
        f_a.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(f_a, text=self.t("amount_label"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_amt = ctk.CTkEntry(f_a, height=44, corner_radius=10,
                             placeholder_text=self.t("amount_placeholder"), font=self._get_font(15))
        if is_edit: e_amt.insert(0, str(edit_data.get("amount", "")))
        e_amt.pack(fill="x")

        rf2 = ctk.CTkFrame(fi, fg_color="transparent")
        rf2.pack(fill="x", pady=(0, 16))
        rf2.columnconfigure((0, 1), weight=1)

        f_c = ctk.CTkFrame(rf2, fg_color="transparent")
        f_c.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(f_c, text=self.t("category"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        ec = self._get_expense_categories()
        cb_cat = ctk.CTkComboBox(f_c, values=ec, height=44, corner_radius=10,
                                 font=self._get_font(15), dropdown_font=self._get_font(14), state="readonly")
        if is_edit: cb_cat.set(edit_data.get("category", ec[0]))
        else: cb_cat.set(ec[0])
        cb_cat.pack(fill="x")

        f_f = ctk.CTkFrame(rf2, fg_color="transparent")
        f_f.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(f_f, text=self.t("fund_type") + " *", font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        funds = self._get_donation_categories()
        cb_fund = ctk.CTkComboBox(f_f, values=funds, height=44, corner_radius=10,
                                  font=self._get_font(15), dropdown_font=self._get_font(14), state="readonly")
        if is_edit: cb_fund.set(edit_data.get("fund_type", funds[0]))
        else: cb_fund.set(funds[0])
        cb_fund.pack(fill="x")

        rf3 = ctk.CTkFrame(fi, fg_color="transparent")
        rf3.pack(fill="x", pady=(0, 16))
        rf3.columnconfigure((0, 1), weight=1)

        f_p = ctk.CTkFrame(rf3, fg_color="transparent")
        f_p.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(f_p, text=self.t("paid_to"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_paid = ctk.CTkEntry(f_p, height=44, corner_radius=10,
                              placeholder_text=self.t("paid_to_placeholder"), font=self._get_font(15))
        if is_edit: e_paid.insert(0, edit_data.get("paid_to", ""))
        e_paid.pack(fill="x")

        f_d = ctk.CTkFrame(rf3, fg_color="transparent")
        f_d.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(f_d, text=self.t("date_label"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_date = ctk.CTkEntry(f_d, height=44, corner_radius=10, font=self._get_font(15))
        if is_edit: e_date.insert(0, format_date(edit_data.get("date", "")))
        else: e_date.insert(0, get_today_date())
        e_date.pack(fill="x")


        ctk.CTkLabel(fi, text=self.t("notes_label"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=(0, 5))
        e_notes = ctk.CTkTextbox(fi, height=70, corner_radius=10, font=self._get_font(15),
                                 fg_color=COLOR_BG_DARK)
        if is_edit: e_notes.insert("1.0", edit_data.get("notes", ""))
        e_notes.pack(fill="x", pady=(0, 16))





        status = ctk.CTkLabel(fi, text="", font=self._get_font(14, "bold"), anchor="w", wraplength=400)
        status.pack(fill="x", pady=(0, 6))

        def on_fund_change(*args):
            # Check Zakat compliance
            f = self._resolve_combo_to_db(cb_fund.get(), DONATION_CAT_KEYS, DONATION_CAT_DB)
            c = self._resolve_combo_to_db(cb_cat.get(), EXPENSE_CAT_KEYS, EXPENSE_CAT_DB)
            if f == "Zakat" and c not in ["Charity", "Other"]:
                status.configure(text=self.t("zakat_warning"), text_color=COLOR_AMBER)
            else:
                status.configure(text="")

        cb_fund.configure(command=on_fund_change)
        cb_cat.configure(command=on_fund_change)

        def save(print_after=False):
            tt = e_title.get().strip()

            if not tt:
                status.configure(text=self.t("err_title_required"), text_color=COLOR_AMBER); return
            at = e_amt.get().strip()
            if not at:
                status.configure(text=self.t("err_amount_required"), text_color=COLOR_AMBER); return
            try:
                av = float(at)
            except ValueError:
                status.configure(text=self.t("err_amount_numeric"), text_color=COLOR_AMBER); return
            if av <= 0:
                status.configure(text=self.t("err_amount_positive"), text_color=COLOR_AMBER); return

            fund_db = self._resolve_combo_to_db(cb_fund.get(), DONATION_CAT_KEYS, DONATION_CAT_DB)
            fund_balances = get_fund_balances()
            cur_bal = fund_balances.get(fund_db, 0)
            
            if is_edit:
                # If we are editing, add back the current expense amount to the balance check
                if edit_data.get("fund_type") == fund_db:
                    cur_bal += edit_data.get("amount", 0)
            
            if av > cur_bal:
                status.configure(text=self.t("insufficient_fund_balance").format(fund=fund_db), text_color=COLOR_AMBER); return

            dt = e_date.get().strip()
            if dt and not validate_date(dt):
                status.configure(text=self.t("err_date_format"), text_color=COLOR_AMBER); return

            cat = self._resolve_combo_to_db(cb_cat.get(), EXPENSE_CAT_KEYS, EXPENSE_CAT_DB)
            paid = e_paid.get().strip()
            ds = parse_date_to_ymd(dt) if dt else datetime.now().strftime("%Y-%m-%d")
            notes = e_notes.get("1.0", "end-1c").strip()
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            op = self.mosque_profile.get("imam_name", "")

            if is_edit:
                table = "expenses"
                update_transaction("Expense", edit_id, {
                    "title": tt, "amount": av, "category": cat,
                    "paid_to": paid, "date": ds, "notes": notes, "fund_type": fund_db, "operator": op
                })
                log_action("UPDATE", "expenses", edit_id, f"Expense updated. Amount: {edit_data.get('amount')} -> {av}, Fund: {edit_data.get('fund_type')} -> {fund_db}", operator=op)


                
                if print_after:
                    self._print_receipt("Expense", edit_id)
                self._show_dashboard()
            else:
                conn = sqlite3.connect(get_db_path())
                c = conn.execute("INSERT INTO expenses (title,amount,category,paid_to,date,notes,fund_type,is_deleted,created_at,updated_at,operator) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                             (tt, av, cat, paid, ds, notes, fund_db, 0, now, now, op))
                eid = c.lastrowid
                conn.commit(); conn.close()
                log_action("CREATE", "expenses", eid, f"Expense of {av} added. Title: {tt}, Fund: {fund_db}", operator=op)
                e_title.delete(0, "end"); e_amt.delete(0, "end")


                cb_cat.set(ec[0]); e_paid.delete(0, "end")
                e_date.delete(0, "end"); e_date.insert(0, get_today_date())
                e_notes.delete("1.0", "end")
                status.configure(text=self.t("expense_saved").format(amount=f"{av:,.0f}"), text_color=COLOR_GREEN)
                
                if print_after:
                    self._print_receipt("Expense", eid)




        br = ctk.CTkFrame(fi, fg_color="transparent")
        br.pack(fill="x", pady=(4, 0))
        br.columnconfigure((0, 1, 2), weight=1)
        
        # Save & Print
        ctk.CTkButton(br, text=self.t("save_and_print"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#0f172a",
                      height=50, corner_radius=12, 
                      command=lambda: save(print_after=True)).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Save Expense
        ctk.CTkButton(br, text=self.t("save_expense"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_GREEN, hover_color="#22c55e", text_color="#0f172a",
                      height=50, corner_radius=12, 
                      command=lambda: save(print_after=False)).grid(row=0, column=1, sticky="ew", padx=5)
        
        # Back
        ctk.CTkButton(br, text=self.t("go_dashboard"), font=self._get_font(13),
                      fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER, text_color=COLOR_TEXT,
                      height=50, corner_radius=12,
                      command=lambda: self._nav_click("dashboard", self._show_dashboard)).grid(row=0, column=2, sticky="ew", padx=(5, 0))


    # ──────────────────────────────────────────
    # EMPLOYEES SCREEN
    # ──────────────────────────────────────────

    def _show_employees(self):
        self._clear_content()
        self.current_view = "employees"
        self._highlight_active_nav()

        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        # Header
        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(hdr, text=self.t("employees"), font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")

        # Action Buttons
        bt_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        bt_frame.pack(side="right")
        
        ctk.CTkButton(bt_frame, text=self.t("pay_salary"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_AMBER, hover_color="#fcd34d", text_color="#0f172a",
                      command=self._show_pay_salary).pack(side="left", padx=(0, 10))
                      
        ctk.CTkButton(bt_frame, text=self.t("add_employee"), font=self._get_font(13),
                      fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER, text_color=COLOR_TEXT,
                      command=lambda: self._show_add_edit_employee()).pack(side="left")

        # Table Configuration
        list_frame = ctk.CTkScrollableFrame(wrapper, fg_color=COLOR_CARD, corner_radius=12,
                                            border_width=1, border_color=COLOR_BORDER)
        list_frame.pack(fill="both", expand=True)
        list_frame.columnconfigure((0, 1, 2), weight=1)
        list_frame.columnconfigure(3, weight=0) # Actions column
        
        # Table Header
        h_font = self._get_font(12, "bold")
        headers = ["col_name", "role", "salary_amount", "col_actions"]
        for i, k in enumerate(headers):
            ctk.CTkLabel(list_frame, text=self.t(k), font=h_font, text_color=COLOR_TEXT_DIM, anchor="w").grid(
                row=0, column=i, sticky="w", padx=(16 if i == 0 else 10), pady=(12, 6))
        
        ctk.CTkFrame(list_frame, fg_color=COLOR_BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew", padx=16)

        emps = fetch_employees()
        for idx, emp in enumerate(emps):
            e_id, e_name, e_role, e_salary = emp
            
            # Column 0: Name
            ctk.CTkLabel(list_frame, text=e_name, font=self._get_font(14, "bold"), 
                         text_color=COLOR_TEXT, anchor="w").grid(row=idx+2, column=0, sticky="w", padx=16, pady=8)
            
            # Column 1: Role
            r_tr = self.t(e_role)
            ctk.CTkLabel(list_frame, text=r_tr, font=self._get_font(13), 
                         text_color=COLOR_TEXT_DIM, anchor="w").grid(row=idx+2, column=1, sticky="w", padx=10)
            
            # Column 2: Salary
            ctk.CTkLabel(list_frame, text=f"Rs {e_salary:,.0f}", font=self._get_font(14), 
                         text_color=COLOR_GREEN, anchor="w").grid(row=idx+2, column=2, sticky="w", padx=10)

            # Column 3: Actions
            act_f = ctk.CTkFrame(list_frame, fg_color="transparent")
            act_f.grid(row=idx+2, column=3, sticky="e", padx=16)
            
            def make_del_cmd(pid=e_id, pname=e_name):
                def do_del():
                    if self.confirm("Delete", self.t("confirm_delete_emp").format(name=pname)):
                        delete_employee(pid)
                        self._show_employees()
                return do_del
                
            ctk.CTkButton(act_f, text=self.t("edit"), width=55, height=28, font=self._get_font(11), 
                          fg_color="transparent", border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT,
                          command=lambda e=emp: self._show_add_edit_employee(e)).pack(side="left", padx=4)
            ctk.CTkButton(act_f, text=self.t("delete"), width=55, height=28, font=self._get_font(11), 
                          fg_color="transparent", border_width=1, border_color="#ef4444",
                          text_color="#ef4444", hover_color="#451a1a",
                          command=make_del_cmd()).pack(side="left")
        
        # Bottom spacing
        ctk.CTkFrame(list_frame, fg_color="transparent", height=10).grid(row=len(emps)+2, column=0)

    def _show_add_edit_employee(self, employee=None):
        self._clear_content()
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.pack(expand=True, padx=24, pady=24, fill="both")
        
        is_edit = employee is not None
        title_txt = self.t("edit_employee") if is_edit else self.t("add_employee")
        
        main = ctk.CTkFrame(wrapper, fg_color="transparent")
        main.pack(expand=True)
        
        fi = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=16, width=400)
        fi.pack_propagate(False)
        fi.configure(width=450, height=520)
        fi.pack(pady=20)
        
        ctk.CTkLabel(fi, text=title_txt, font=self._get_font(20, "bold")).pack(pady=(30, 20))
        
        ctk.CTkLabel(fi, text="Name *", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=30)
        e_name = ctk.CTkEntry(fi, height=44, font=self._get_font(15))
        e_name.pack(fill="x", padx=30, pady=(4, 16))
        
        ctk.CTkLabel(fi, text=self.t("role"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=30)
        roles_keys = get_employee_roles()
        roles_tr = [self.t(k) for k in roles_keys]
        cb_role = ctk.CTkComboBox(fi, values=roles_tr, height=44, font=self._get_font(15), state="readonly")
        cb_role.pack(fill="x", padx=30, pady=(4, 16))
        
        ctk.CTkLabel(fi, text=self.t("salary_amount") + " *", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=30)
        e_sal = ctk.CTkEntry(fi, height=44, font=self._get_font(15))
        e_sal.pack(fill="x", padx=30, pady=(4, 20))
        
        err_lbl = ctk.CTkLabel(fi, text="", text_color=COLOR_RED, font=self._get_font(12))
        err_lbl.pack(pady=(0, 10))
        
        if is_edit:
            e_name.insert(0, employee[1])
            cb_role.set(self.t(employee[2]))
            e_sal.insert(0, str(int(employee[3])))
        else:
            cb_role.set(roles_tr[0])
            
        def do_save():
            nm = e_name.get().strip()
            if not nm:
                err_lbl.configure(text=self.t("err_name_required"))
                return
            sal_str = e_sal.get().strip()
            try:
                sal_val = float(sal_str)
                if sal_val <= 0: raise ValueError
            except:
                err_lbl.configure(text=self.t("err_amount_numeric"))
                return
                
            role_key = roles_keys[roles_tr.index(cb_role.get())]
            
            if is_edit:
                update_employee(employee[0], nm, role_key, sal_val)
            else:
                add_employee(nm, role_key, sal_val)
            self._show_employees()
            
        ctk.CTkButton(fi, text="Save", font=self._get_font(15, "bold"), height=46, command=do_save).pack(fill="x", padx=30, pady=(10, 8))
        ctk.CTkButton(fi, text="Cancel", font=self._get_font(14), fg_color="transparent", border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT, height=46, command=self._show_employees).pack(fill="x", padx=30)


    def _show_pay_salary(self):
        self._clear_content()
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.pack(expand=True, padx=24, pady=24, fill="both")
        
        main = ctk.CTkFrame(wrapper, fg_color="transparent")
        main.pack(expand=True)
        
        fi = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=16, width=450, height=450)
        fi.pack_propagate(False)
        fi.pack(pady=20)
        
        ctk.CTkLabel(fi, text=self.t("pay_salary"), font=self._get_font(20, "bold")).pack(pady=(30, 20))
        
        emps = fetch_employees()
        if not emps:
            ctk.CTkLabel(fi, text="No employees found.", font=self._get_font(14), text_color=COLOR_TEXT_DIM).pack(pady=40)
            ctk.CTkButton(fi, text="Back", height=46, command=self._show_employees).pack(padx=30, fill="x")
            return
            
        emp_names = [f"{e[1]} - Rs{e[3]:,.0f}" for e in emps]
        
        ctk.CTkLabel(fi, text=self.t("employees"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=30)
        cb_emp = ctk.CTkComboBox(fi, values=emp_names, height=44, font=self._get_font(15), state="readonly")
        cb_emp.set(emp_names[0])
        cb_emp.pack(fill="x", padx=30, pady=(4, 16))
        
        ctk.CTkLabel(fi, text="Month (MM-YYYY)", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=30)
        cur_mo = datetime.now().strftime("%m-%Y")
        e_mo = ctk.CTkEntry(fi, height=44, font=self._get_font(15))
        e_mo.insert(0, cur_mo)
        e_mo.pack(fill="x", padx=30, pady=(4, 20))
        
        err_lbl = ctk.CTkLabel(fi, text="", text_color=COLOR_RED, font=self._get_font(12))
        err_lbl.pack(pady=(0, 10))
        
        def do_pay():
            idx = emp_names.index(cb_emp.get())
            emp_id, emp_name, emp_role, emp_salary = emps[idx]
            mo_val = e_mo.get().strip()
            
            if not mo_val or len(mo_val) != 7 or "-" not in mo_val:
                err_lbl.configure(text="Invalid month format (MM-YYYY)")
                return
                
            if check_salary_paid(emp_id, mo_val):
                err_lbl.configure(text=self.t("already_paid_warning"))
                return
            
            cur_bal = get_current_balance()
            if emp_salary > cur_bal:
                err_lbl.configure(text=self.t("err_insufficient_balance").format(bal=cur_bal))
                return
                
            # Record expense
            title = f"Salary - {emp_name} ({mo_val})"
            pay_date = datetime.now().strftime("%Y-%m-%d") # Paid today
            now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            
            conn = sqlite3.connect(get_db_path())
            c = conn.execute("INSERT INTO expenses (title,amount,category,paid_to,date,notes,expense_type,employee_id,is_deleted,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                         (title, emp_salary, "Salary", emp_name, pay_date, "Monthly Salary Payment", "Salary", emp_id, 0, now, now))
            eid = c.lastrowid
            conn.commit(); conn.close()
            log_action("CREATE", "expenses", eid, f"Salary of {emp_salary} paid to {emp_name} for {mo_val}")

            
            self.info("Success", self.t("salary_paid_success"))
            self._show_employees()
            
        ctk.CTkButton(fi, text="Confirm Payment", font=self._get_font(15, "bold"), fg_color=COLOR_GREEN, text_color="#0f172a", hover_color="#22c55e", height=46, command=do_pay).pack(fill="x", padx=30, pady=(10, 8))
        ctk.CTkButton(fi, text="Cancel", font=self._get_font(14), fg_color="transparent", border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT, height=46, command=self._show_employees).pack(fill="x", padx=30)

    # ──────────────────────────────────────────
    # REPORTS SCREEN
    # ──────────────────────────────────────────

    def _show_reports(self):
        self._clear_content()
        self.current_view = "reports"
        self._highlight_active_nav()

        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)


        # Header
        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=self.t("reports"), font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")

        # Controls
        ctrl = ctk.CTkFrame(wrapper, fg_color="transparent")
        ctrl.pack(fill="x", pady=(16, 0))

        mode_var = ctk.StringVar(value="Monthly")
        mode_seg = ctk.CTkSegmentedButton(ctrl, values=["Monthly", "Date Range"],
                                          variable=mode_var, font=self._get_font(13))
        mode_seg.pack(side="left", padx=(0, 20))

        # Monthly container
        mon_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        ctk.CTkLabel(mon_frame, text=self.t("select_month"), font=self._get_font(14),
                     text_color=COLOR_TEXT_DIM, anchor="w").pack(side="left", padx=(0, 10))
        months = get_month_options()
        month_var = ctk.StringVar(value=months[0])
        month_cb = ctk.CTkComboBox(mon_frame, values=months, height=36, width=140,
                                   corner_radius=8, font=self._get_font(14),
                                   dropdown_font=self._get_font(13), state="readonly",
                                   variable=month_var)
        month_cb.pack(side="left")

        # Date Range container
        rng_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        ctk.CTkLabel(rng_frame, text="From:", font=self._get_font(14), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(0, 8))
        e_from = ctk.CTkEntry(rng_frame, height=36, width=120, font=self._get_font(14))
        e_from.insert(0, get_today_date())
        e_from.pack(side="left", padx=(0, 16))

        ctk.CTkLabel(rng_frame, text="To:", font=self._get_font(14), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(0, 8))
        e_to = ctk.CTkEntry(rng_frame, height=36, width=120, font=self._get_font(14))
        e_to.insert(0, get_today_date())
        e_to.pack(side="left")

        # Filter & Print Button
        bt_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        bt_frame.pack(side="right")
        
        def print_report():
            is_range = mode_var.get() == "Date Range"
            if is_range:
                f_val = (parse_date_to_ymd(e_from.get()), parse_date_to_ymd(e_to.get()))
                sel_label = f"{e_from.get()} to {e_to.get()}"
            else:
                f_val = month_var.get()
                sel_label = f_val

            don_total, exp_total = fetch_monthly_totals(f_val, is_range)
            balance = don_total - exp_total
            don_cats, exp_cats = fetch_category_totals(f_val, is_range)
            txns = fetch_month_transactions(f_val, is_range)
            fund_period = fetch_fund_period_totals(f_val, is_range)
            cum_bals = get_fund_balances()

            lines = []
            lines.append("=" * 60)
            lines.append(f"  {self.t('report_title').upper()}")
            
            p_name = self.mosque_profile.get("mosque_name", "").strip()
            if p_name: lines.append(f"  {p_name}")
            p_addr = self.mosque_profile.get("address", "").strip()
            if p_addr: lines.append(f"  {p_addr}")
            p_phone = self.mosque_profile.get("phone", "").strip()
            if p_phone: lines.append(f"  Phone: {p_phone}")

            lines.append(f"  Period: {sel_label}")
            lines.append(f"  Printed: {get_today_date()}  {datetime.now().strftime('%I:%M %p')}")
            lines.append("=" * 60)
            lines.append("")
            lines.append(f"  {self.t('total_donations'):.<30} Rs {don_total:>12,.0f}")
            lines.append(f"  {self.t('total_expenses'):.<30} Rs {exp_total:>12,.0f}")
            lines.append(f"  {self.t('net_balance'):.<30} Rs {balance:>12,.0f}")
            lines.append("")
            lines.append("-" * 60)
            lines.append(f"  {self.t('fund_balance').upper()} (SUMMARY)")
            lines.append("-" * 60)
            lines.append(f"  {'Fund':<18} {'Donations':>12} {'Expenses':>12} {'Balance':>12}")
            for fund in DONATION_CAT_DB:
                d, e = fund_period.get(fund, (0, 0))
                b = cum_bals.get(fund, 0)
                lines.append(f"  {fund:<18} {d:>12,.0f} {e:>12,.0f} {b:>12,.0f}")

            lines.append("")
            lines.append("-" * 60)
            lines.append(f"  {self.t('donation_by_cat')}")
            lines.append("-" * 60)
            for cat, total in (don_cats or [("—", 0)]):
                lines.append(f"    {(cat or '—'):.<26} Rs {total:>12,.0f}")
            lines.append("")
            lines.append("-" * 60)
            lines.append(f"  {self.t('expense_by_cat')}")
            lines.append("-" * 60)
            for cat, total in (exp_cats or [("—", 0)]):
                lines.append(f"    {(cat or '—'):.<26} Rs {total:>12,.0f}")
            lines.append("")
            lines.append("-" * 60)
            lines.append(f"  {self.t('all_transactions')}")
            lines.append("-" * 60)
            lines.append(f"  {'Type':<12}{'Name':<24}{'Fund':<12}{'Amount':>14}  {'Date':<12}")
            lines.append("  " + "-" * 80)

            for t_type, name, cat, amount, date, t_id, updated_at, fund in txns:
                s = "+" if t_type == "Donation" else "-"
                amt_str = f"{s}Rs {amount:,.0f}"
                lines.append(f"  {t_type:<12}{(name or '—'):<24}{(fund or '—'):<12}{amt_str:>14}  {format_date(date):<12}")

            lines.append("")
            lines.append("=" * 60)
            lines.append(f"  Generated: {get_today_date()}")
            lines.append("=" * 60)


            report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
            os.makedirs(report_dir, exist_ok=True)
            rf_name = sel_label.replace('-', '_').replace(' ', '_')
            fname = os.path.join(report_dir, f"report_{rf_name}.txt")
            with open(fname, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            os.startfile(fname)

        ctk.CTkButton(bt_frame, text=self.t("print_report"), font=self._get_font(13, "bold"),
                      fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                      text_color="#0f172a", height=36, corner_radius=8,
                      command=print_report).pack(side="right", padx=(10, 0))
                      
        ctk.CTkButton(bt_frame, text="Filter", font=self._get_font(13, "bold"),
                      fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER,
                      text_color=COLOR_TEXT, width=80, height=36, corner_radius=8,
                      command=lambda: render_report()).pack(side="right")

        # Month Integrity Control
        integrity_frame = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        integrity_frame.pack(fill="x", pady=(16, 0))
        
        status_lbl = ctk.CTkLabel(integrity_frame, text="", font=self._get_font(14, "bold"))
        status_lbl.pack(side="left", padx=20, pady=15)
        
        def refresh_integrity():
            m = month_var.get()
            closed = is_month_closed(m)
            for w in integrity_frame.winfo_children():
                if w != status_lbl: w.destroy()
            
            if closed:
                status_lbl.configure(text=f"🔒 {self.t('month_closed')} ({m})", text_color=COLOR_RED)
                ctk.CTkButton(integrity_frame, text=self.t("reopen_month"), width=150, height=34,
                              fg_color="#334155", hover_color="#475569", 
                              command=lambda: self._show_password_prompt(self.t("confirm_identity"), f"Are you sure you want to REOPEN {m}?", lambda: [reopen_period(m), refresh_integrity()])).pack(side="right", padx=20)
            else:
                status_lbl.configure(text=f"🔓 {self.t('month_open')} ({m})", text_color=COLOR_GREEN)
                ctk.CTkButton(integrity_frame, text=self.t("close_month"), width=150, height=34,
                              fg_color=COLOR_RED, hover_color="#b91c1c",
                              command=lambda: [close_period(m), refresh_integrity()]).pack(side="right", padx=20)

        # Container for report content

        report_frame = ctk.CTkFrame(wrapper, fg_color="transparent")
        report_frame.pack(fill="both", expand=True, pady=(16, 0))

        def render_report(*args):
            refresh_integrity()
            for w in report_frame.winfo_children():

                w.destroy()

            is_range = mode_var.get() == "Date Range"
            if is_range:
                f_val = (parse_date_to_ymd(e_from.get()), parse_date_to_ymd(e_to.get()))
            else:
                f_val = month_var.get()

            don_total, exp_total = fetch_monthly_totals(f_val, is_range)
            balance = don_total - exp_total
            don_cats, exp_cats = fetch_category_totals(f_val, is_range)
            txns = fetch_month_transactions(f_val, is_range)
            fund_sums = fetch_fund_period_totals(f_val, is_range)
            fund_bals = get_fund_balances()

            # Keep summary and categories in normal view
            top_part = ctk.CTkFrame(report_frame, fg_color="transparent")
            top_part.pack(fill="x")
            # Summary cards
            cf = ctk.CTkFrame(top_part, fg_color="transparent")
            cf.pack(fill="x")
            cf.columnconfigure((0, 1, 2), weight=1)
            make_card(cf, self.t("total_donations"), f"Rs {don_total:,.0f}", COLOR_GREEN, 0, 0)
            make_card(cf, self.t("total_expenses"), f"Rs {exp_total:,.0f}", COLOR_RED, 0, 1)
            make_card(cf, self.t("net_balance"), f"Rs {balance:,.0f}", COLOR_ACCENT, 0, 2)

            # Fund Summary Section
            ctk.CTkLabel(top_part, text=self.t("fund_balance") + " (Summary)", font=self._get_font(16, "bold"),
                         text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(20, 10))
            
            fs_tbl = ctk.CTkFrame(top_part, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
            fs_tbl.pack(fill="x")
            fs_tbl.columnconfigure((0, 1, 2, 3), weight=1)
            
            # FS Headers
            fs_hdrs = ["fund", "total_donations", "total_expenses", "current_balance"]
            for i, k in enumerate(fs_hdrs):
                ctk.CTkLabel(fs_tbl, text=self.t(k), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM, anchor="w").grid(row=0, column=i, sticky="w", padx=15, pady=10)

            
            for idx, fund in enumerate(DONATION_CAT_DB):
                d, e = fund_sums.get(fund, (0, 0))
                b = fund_bals.get(fund, 0)
                ctk.CTkLabel(fs_tbl, text=self.t("cat_"+fund.lower()), font=self._get_font(13), anchor="w").grid(row=idx+1, column=0, sticky="w", padx=15, pady=5)
                ctk.CTkLabel(fs_tbl, text=f"Rs {d:,.0f}", font=self._get_font(13), text_color=COLOR_GREEN, anchor="w").grid(row=idx+1, column=1, sticky="w", padx=15, pady=5)
                ctk.CTkLabel(fs_tbl, text=f"Rs {e:,.0f}", font=self._get_font(13), text_color=COLOR_RED, anchor="w").grid(row=idx+1, column=2, sticky="w", padx=15, pady=5)
                ctk.CTkLabel(fs_tbl, text=f"Rs {b:,.0f}", font=self._get_font(13, "bold"), text_color=COLOR_ACCENT, anchor="w").grid(row=idx+1, column=3, sticky="w", padx=15, pady=5)

            
            ctk.CTkFrame(fs_tbl, fg_color="transparent", height=8).grid(row=len(DONATION_CAT_DB)+1, column=0)


            # Category breakdown
            cat_row = ctk.CTkFrame(top_part, fg_color="transparent")
            cat_row.pack(fill="x", pady=(16, 0))
            cat_row.columnconfigure((0, 1), weight=1)

            # Donation categories
            dc_frame = ctk.CTkFrame(cat_row, fg_color=COLOR_CARD, corner_radius=12,
                                     border_width=1, border_color=COLOR_BORDER)
            dc_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            ctk.CTkLabel(dc_frame, text=self.t("donation_by_cat"), font=self._get_font(14, "bold"),
                         text_color=COLOR_GREEN, anchor="w").pack(fill="x", padx=16, pady=(14, 8))
            if don_cats:
                for cat, total in don_cats:
                    r = ctk.CTkFrame(dc_frame, fg_color="transparent")
                    r.pack(fill="x", padx=16, pady=3)
                    ctk.CTkLabel(r, text=cat or "—", font=self._get_font(13),
                                 text_color=COLOR_TEXT, anchor="w").pack(side="left")
                    ctk.CTkLabel(r, text=f"Rs {total:,.0f}", font=self._get_font(13, "bold"),
                                 text_color=COLOR_GREEN, anchor="w").pack(side="right")
            else:
                ctk.CTkLabel(dc_frame, text="—", font=self._get_font(13),
                             text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=16, pady=8)
            ctk.CTkFrame(dc_frame, fg_color="transparent", height=10).pack()

            # Expense categories
            ec_frame = ctk.CTkFrame(cat_row, fg_color=COLOR_CARD, corner_radius=12,
                                     border_width=1, border_color=COLOR_BORDER)
            ec_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
            ctk.CTkLabel(ec_frame, text=self.t("expense_by_cat"), font=self._get_font(14, "bold"),
                         text_color=COLOR_RED, anchor="w").pack(fill="x", padx=16, pady=(14, 8))
            if exp_cats:
                for cat, total in exp_cats:
                    r = ctk.CTkFrame(ec_frame, fg_color="transparent")
                    r.pack(fill="x", padx=16, pady=3)
                    ctk.CTkLabel(r, text=cat or "—", font=self._get_font(13),
                                 text_color=COLOR_TEXT, anchor="w").pack(side="left")
                    ctk.CTkLabel(r, text=f"Rs {total:,.0f}", font=self._get_font(13, "bold"),
                                 text_color=COLOR_RED, anchor="w").pack(side="right")
            else:
                ctk.CTkLabel(ec_frame, text="—", font=self._get_font(13),
                             text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", padx=16, pady=8)
            ctk.CTkFrame(ec_frame, fg_color="transparent", height=10).pack()

            # Trans list wrapped in scrollable frame
            ctk.CTkLabel(report_frame, text=self.t("all_transactions"),
                         font=self._get_font(16, "bold"), text_color=COLOR_TEXT,
                         anchor="w").pack(fill="x", pady=(20, 8))

            scroll_tbl = ctk.CTkScrollableFrame(report_frame, fg_color=COLOR_CARD, corner_radius=12,
                                                border_width=1, border_color=COLOR_BORDER)
            scroll_tbl.pack(fill="both", expand=True)

            if not txns:
                ctk.CTkLabel(scroll_tbl, text=self.t("no_data_month"), font=self._get_font(13),
                             text_color=COLOR_TEXT_DIM, pady=24, anchor="w").pack(fill="x", padx=16)
            else:
                # Table Configuration
                scroll_tbl.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
                scroll_tbl.columnconfigure(7, weight=0) # Actions column
                
                # Header row
                cw = [100, 200, 120, 120, 140, 120, 140, 120]
                cols = ["col_type", "col_name", "fund", "col_category", "col_amount", "col_date", "col_operator", "col_actions"]
                for i, k in enumerate(cols):
                    ctk.CTkLabel(scroll_tbl, text=self.t(k), font=self._get_font(12, "bold"),
                                 text_color=COLOR_TEXT_DIM, anchor="w", width=cw[i]).grid(
                                     row=0, column=i, sticky="w", padx=(16 if i == 0 else 10), pady=(12, 6))


                
                ctk.CTkFrame(scroll_tbl, fg_color=COLOR_BORDER, height=1).grid(row=1, column=0, columnspan=8, sticky="ew", padx=16)

                for idx, txn_row in enumerate(txns):
                    t_type, name, cat, amount, date, t_id, updated_at, fund, op_val = txn_row
                    is_don = t_type == "Donation"

                    bc = COLOR_GREEN if is_don else COLOR_RED
                    bt = self.t("type_donation") if is_don else self.t("type_expense")
                    
                    # Column 0: Type
                    ctk.CTkLabel(scroll_tbl, text=bt, font=self._get_font(10, "bold"),
                                 text_color="#0f172a", fg_color=bc, corner_radius=5,
                                 width=80, anchor="center").grid(row=idx+2, column=0, sticky="w", padx=16, pady=8)
                    
                    # Column 1: Name
                    ctk.CTkLabel(scroll_tbl, text=name or "—", font=self._get_font(13),
                                 text_color=COLOR_TEXT, anchor="w", width=200).grid(row=idx+2, column=1, sticky="w", padx=10)
                    
                    # Column 2: Fund
                    f_tr = self.t("cat_" + fund.lower()) if fund else "—"
                    ctk.CTkLabel(scroll_tbl, text=f_tr, font=self._get_font(13),
                                 text_color=COLOR_TEXT, anchor="w", width=120).grid(row=idx+2, column=2, sticky="w", padx=10)
                    
                    # Column 3: Category
                    ctk.CTkLabel(scroll_tbl, text=cat or "—", font=self._get_font(13),
                                 text_color=COLOR_TEXT_DIM, anchor="w", width=120).grid(row=idx+2, column=3, sticky="w", padx=10)
                    
                    # Column 4: Amount
                    sign = "+" if is_don else "-"
                    ctk.CTkLabel(scroll_tbl, text=f"{sign} Rs {amount:,.0f}", font=self._get_font(13, "bold"),
                                 text_color=bc, anchor="w", width=140).grid(row=idx+2, column=4, sticky="w", padx=10)
                    
                    # Column 5: Date
                    ctk.CTkLabel(scroll_tbl, text=format_date(date), font=self._get_font(13),
                                 text_color=COLOR_TEXT_DIM, anchor="w", width=120).grid(row=idx+2, column=5, sticky="w", padx=10)
                    
                    # Column 6: Operator
                    ctk.CTkLabel(scroll_tbl, text=op_val or "—", font=self._get_font(12),
                                 text_color=COLOR_TEXT_DIM, anchor="w", width=140).grid(row=idx+2, column=6, sticky="w", padx=10)


                    
                    # Column 7: Actions
                    act_f = ctk.CTkFrame(scroll_tbl, fg_color="transparent")
                    act_f.grid(row=idx+2, column=7, sticky="e", padx=16)
                    
                    ctk.CTkButton(act_f, text=self.t("print"), width=60, height=28, font=self._get_font(11),
                                  fg_color="transparent", border_width=1, border_color=COLOR_ACCENT,
                                  text_color=COLOR_ACCENT, hover_color=COLOR_CARD_HOVER,
                                  command=lambda t=t_type, i=t_id: self._print_receipt(t, i)).pack(side="left", padx=4)



                    ctk.CTkButton(act_f, text=self.t("edit"), width=50, height=28, font=self._get_font(11),
                                  fg_color="transparent", border_width=1, border_color=COLOR_BORDER,
                                  command=lambda t=t_type, i=t_id: self._handle_edit(t, i, None)).pack(side="left", padx=4)
                    
                    ctk.CTkButton(act_f, text=self.t("delete"), width=50, height=28, font=self._get_font(11),
                                  fg_color="transparent", border_width=1, border_color="#ef4444",
                                  text_color="#ef4444", hover_color="#451a1a",
                                  command=lambda t=t_type, i=t_id: self._handle_delete(t, i)).pack(side="left")


            
            # Bottom spacing
            ctk.CTkFrame(scroll_tbl, fg_color="transparent", height=10).grid(row=len(txns)+2, column=0)

        def toggle_mode(*args):
            if mode_var.get() == "Monthly":
                rng_frame.pack_forget()
                mon_frame.pack(side="left")
            else:
                mon_frame.pack_forget()
                rng_frame.pack(side="left")
            render_report()

        mode_var.trace_add("write", toggle_mode)
        toggle_mode()

    def _show_audit_log(self):
        self._clear_content()
        self.current_view = "audit"
        self._highlight_active_nav()
        
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)
        
        header = ctk.CTkFrame(wrapper, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text=self.t("audit_log"), font=self._get_font(24, "bold"), text_color=COLOR_TEXT).pack(side="left")
        
        # Filter Bar
        fb = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        fb.pack(fill="x", pady=(0, 20), ipady=10)
        
        # Action Type Filter
        ctk.CTkLabel(fb, text=self.t("action"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM).grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
        actions = ["All", "CREATE", "UPDATE", "DELETE", "RESTORE", "LOGIN", "LOGOUT", "PASSWORD_CHANGE", "BACKUP", "RESTORE_DB"]
        cb_type = ctk.CTkComboBox(fb, values=actions, width=150, state="readonly")
        cb_type.set("All")
        cb_type.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky="w")
        
        # Date Filters
        ctk.CTkLabel(fb, text=self.t("from"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        e_from = ctk.CTkEntry(fb, placeholder_text="DD-MM-YYYY", width=120)
        e_from.insert(0, get_today_date())
        e_from.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")
        
        ctk.CTkLabel(fb, text=self.t("to"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM).grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        e_to = ctk.CTkEntry(fb, placeholder_text="DD-MM-YYYY", width=120)
        e_to.insert(0, get_today_date())
        e_to.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="w")
        
        btn_search = ctk.CTkButton(fb, text="Generate", width=100, corner_radius=8, 
                                   fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#0f172a",
                                   command=lambda: render_table())
        btn_search.grid(row=1, column=3, padx=20, pady=(0, 10), sticky="s")


        
        # Table
        tbl_frame = ctk.CTkFrame(wrapper, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        tbl_frame.pack(fill="both", expand=True)
        
        # Headers
        hdr_f = ctk.CTkFrame(tbl_frame, fg_color="transparent", height=40)
        hdr_f.pack(fill="x", padx=16, pady=(10, 0))
        hdr_f.columnconfigure((0, 1), weight=0)
        hdr_f.columnconfigure(2, weight=1)
        
        ctk.CTkLabel(hdr_f, text=self.t("col_date"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM, width=160, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(hdr_f, text=self.t("action"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM, width=130, anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(hdr_f, text=self.t("description"), font=self._get_font(12, "bold"), text_color=COLOR_TEXT_DIM, anchor="w").grid(row=0, column=2, padx=20, sticky="w")

        
        ctk.CTkFrame(tbl_frame, fg_color=COLOR_BORDER, height=1).pack(fill="x", padx=16, pady=5)
        
        scroll_f = ctk.CTkScrollableFrame(tbl_frame, fg_color="transparent")
        scroll_f.pack(fill="both", expand=True, padx=4, pady=(0, 10))
        
        def render_table():
            for child in scroll_f.winfo_children(): child.destroy()
            
            logs = fetch_audit_logs(
                action_type=cb_type.get(),
                start_date=e_from.get().strip() or None,
                end_date=e_to.get().strip() or None
            )
            
            if not logs:
                ctk.CTkLabel(scroll_f, text=self.t("no_transactions"), font=self._get_font(13), text_color=COLOR_TEXT_DIM).pack(pady=40)
                return
                
            for idx, (ts, atype, desc, table, rid, op) in enumerate(logs):
                f = ctk.CTkFrame(scroll_f, fg_color="transparent")
                f.pack(fill="x", padx=12, pady=4)
                f.columnconfigure((0, 1), weight=0)
                f.columnconfigure(2, weight=1)
                f.columnconfigure(3, weight=0)
                
                # Timestamp
                ctk.CTkLabel(f, text=ts, font=self._get_font(12), text_color=COLOR_TEXT_DIM, width=160, anchor="w").grid(row=0, column=0)
                
                # Action Type Badge
                color = COLOR_ACCENT
                if atype == "DELETE": color = "#ef4444"
                if atype == "CREATE": color = COLOR_GREEN
                if atype == "UPDATE": color = COLOR_AMBER
                if atype in ["LOGIN", "LOGOUT"]: color = "#3b82f6"
                
                ctk.CTkLabel(f, text=f"  {atype}", font=self._get_font(11, "bold"), fg_color=color, text_color="#0f172a", corner_radius=6, width=100, anchor="w").grid(row=0, column=1, sticky="w")

                
                # Description
                ctk.CTkLabel(f, text=desc, font=self._get_font(12), text_color=COLOR_TEXT, anchor="w", justify="left", wraplength=400).grid(row=0, column=2, padx=20, sticky="w")
                
                # Operator
                ctk.CTkLabel(f, text=f"👤 {op or '—'}", font=self._get_font(11), text_color=COLOR_ACCENT, width=120, anchor="e").grid(row=0, column=3, padx=(10, 0))

                
                if idx < len(logs) - 1:
                    ctk.CTkFrame(scroll_f, fg_color=COLOR_BORDER, height=1).pack(fill="x", padx=12, pady=2)
                    
        render_table()

    # ──────────────────────────────────────────
    # SETTINGS SCREEN
    # ──────────────────────────────────────────


    def _show_settings(self):
        self._clear_content()
        self.current_view = "settings"
        self._highlight_active_nav()

        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        # Header
        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=self.t("settings"), font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")

        main = ctk.CTkFrame(wrapper, fg_color="transparent")
        main.pack(fill="x", pady=20)
        main.grid_columnconfigure((0, 1), weight=1)

        # 1. Mosque Profile Card (Left Column)
        p_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        p_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        pi = ctk.CTkFrame(p_card, fg_color="transparent")
        pi.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(pi, text=self.t("mosque_profile"), font=self._get_font(18, "bold"), text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(0, 16))

        row1 = ctk.CTkFrame(pi, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 12))
        row1.columnconfigure((0,1), weight=1)
        
        f1 = ctk.CTkFrame(row1, fg_color="transparent")
        f1.grid(row=0, column=0, sticky="ew", padx=(0,8))
        ctk.CTkLabel(f1, text=self.t("mosque_name"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_name = ctk.CTkEntry(f1, height=40, font=self._get_font(14))
        e_name.pack(fill="x")
        
        f2 = ctk.CTkFrame(row1, fg_color="transparent")
        f2.grid(row=0, column=1, sticky="ew", padx=(8,0))
        ctk.CTkLabel(f2, text=self.t("phone_number"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_phone = ctk.CTkEntry(f2, height=40, font=self._get_font(14))
        e_phone.pack(fill="x")

        row2 = ctk.CTkFrame(pi, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 12))
        row2.columnconfigure((0,1), weight=1)

        f3 = ctk.CTkFrame(row2, fg_color="transparent")
        f3.grid(row=0, column=0, sticky="ew", padx=(0,8))
        ctk.CTkLabel(f3, text=self.t("address"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_addr = ctk.CTkEntry(f3, height=40, font=self._get_font(14))
        e_addr.pack(fill="x")

        f4 = ctk.CTkFrame(row2, fg_color="transparent")
        f4.grid(row=0, column=1, sticky="ew", padx=(8,0))
        ctk.CTkLabel(f4, text=self.t("operator_name"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_imam = ctk.CTkEntry(f4, height=40, font=self._get_font(14))
        e_imam.pack(fill="x")


        ctk.CTkLabel(pi, text=self.t("notes"), font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_notes = ctk.CTkTextbox(pi, height=80, font=self._get_font(14), fg_color=COLOR_BG_DARK, corner_radius=10)
        e_notes.pack(fill="x", pady=(0, 20))

        status = ctk.CTkLabel(pi, text="", font=self._get_font(13, "bold"), anchor="w")
        status.pack(fill="x", pady=(0, 8))

        e_name.insert(0, self.mosque_profile.get("mosque_name", ""))
        e_phone.insert(0, self.mosque_profile.get("phone", ""))
        e_addr.insert(0, self.mosque_profile.get("address", ""))
        e_imam.insert(0, self.mosque_profile.get("imam_name", ""))
        e_notes.insert("1.0", self.mosque_profile.get("notes", ""))

        def do_save():
            p_data = dict(self.mosque_profile) # Clone
            p_data.update({
                "mosque_name": e_name.get().strip(),
                "address": e_addr.get().strip(),
                "phone": e_phone.get().strip(),
                "imam_name": e_imam.get().strip(),
                "notes": e_notes.get("1.0", "end-1c").strip()
            })
            save_settings(p_data)
            self.mosque_profile = load_settings()
            self._build_sidebar()
            status.configure(text=self.t("settings_saved"), text_color=COLOR_GREEN)
            log_action("UPDATE", "settings", 1, f"Mosque profile updated: {p_data['mosque_name']}")


        bt_save = ctk.CTkButton(pi, text=self.t("save_settings"), font=self._get_font(14, "bold"),
                                fg_color=COLOR_GREEN, hover_color="#22c55e", text_color="#0f172a",
                                height=46, corner_radius=10, command=do_save)
        bt_save.pack(fill="x")

        # 2. Security Card (Right Column)
        pw_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        pw_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        
        pfi = ctk.CTkFrame(pw_card, fg_color="transparent")
        pfi.pack(fill="both", expand=True, padx=28, pady=24)
        
        ctk.CTkLabel(pfi, text=self.t("change_password"), font=self._get_font(18, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(pfi, text=self.t("old_password"), font=self._get_font(14), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_old = ctk.CTkEntry(pfi, show="*", height=40, font=self._get_font(15))
        e_old.pack(fill="x", pady=(5, 12))
        
        ctk.CTkLabel(pfi, text=self.t("new_password"), font=self._get_font(14), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_new = ctk.CTkEntry(pfi, show="*", height=40, font=self._get_font(15))
        e_new.pack(fill="x", pady=(5, 12))
        
        ctk.CTkLabel(pfi, text=self.t("confirm_password"), font=self._get_font(14), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x")
        e_conf = ctk.CTkEntry(pfi, show="*", height=40, font=self._get_font(15))
        e_conf.pack(fill="x", pady=(5, 12))
        
        pw_status = ctk.CTkLabel(pfi, text="", font=self._get_font(12, "bold"))
        pw_status.pack(pady=(5, 0))

        def do_change_pw():
            old = e_old.get().strip()
            newp = e_new.get().strip()
            conf = e_conf.get().strip()
            
            if old != self.mosque_profile.get("password", "admin"):
                pw_status.configure(text=self.t("invalid_password"), text_color="#ef4444"); return
            if not newp:
                pw_status.configure(text=self.t("err_name_required"), text_color="#ef4444"); return
            if newp != conf:
                pw_status.configure(text=self.t("password_mismatch"), text_color="#ef4444"); return
            
            p_data = dict(self.mosque_profile) # Clone
            p_data["password"] = newp
            save_settings(p_data)
            self.mosque_profile = load_settings()
            pw_status.configure(text=self.t("password_changed"), text_color=COLOR_GREEN)
            log_action("UPDATE", "settings", 1, "Administrator password changed")

            e_old.delete(0, "end"); e_new.delete(0, "end"); e_conf.delete(0, "end")

        ctk.CTkButton(pfi, text=self.t("change_password"), font=self._get_font(14, "bold"),
                      fg_color=COLOR_GREEN, hover_color="#22c55e", text_color="#0f172a",
                      height=46, corner_radius=10, command=do_change_pw).pack(fill="x", pady=(10, 0))


        # 3. System Maintenance (spanning both columns at bottom)
        s_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        s_card.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(24, 0))

        si = ctk.CTkFrame(s_card, fg_color="transparent")
        si.pack(fill="x", padx=24, pady=24)

        ctk.CTkLabel(si, text=self.t("data_management"), font=self._get_font(16, "bold"), text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(0, 12))
        
        # Default Backup Path UI
        bp_frame = ctk.CTkFrame(si, fg_color="transparent")
        bp_frame.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(bp_frame, text=self.t("backup_path"), font=self._get_font(13), text_color=COLOR_TEXT_DIM).pack(side="left", padx=(0, 10))
        e_bp = ctk.CTkEntry(bp_frame, height=36, font=self._get_font(13), fg_color=COLOR_CARD_HOVER)
        e_bp.insert(0, self.mosque_profile.get("backup_path", ""))
        e_bp.configure(state="readonly")
        e_bp.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        def browse_backup_path():
            d = filedialog.askdirectory()
            if d:
                e_bp.configure(state="normal")
                e_bp.delete(0, "end")
                e_bp.insert(0, d)
                e_bp.configure(state="readonly")
                # Save immediately
                p_data = dict(self.mosque_profile)
                p_data["backup_path"] = d
                save_settings(p_data)
                self.mosque_profile = load_settings()
                log_action("UPDATE", "settings", 1, f"Default backup path updated to: {d}")


        ctk.CTkButton(bp_frame, text="📁 " + self.t("browse"), width=80, height=36, font=self._get_font(13),
                      fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER, text_color=COLOR_TEXT,
                      command=browse_backup_path).pack(side="right")

        b_frame = ctk.CTkFrame(si, fg_color="transparent")
        b_frame.pack(fill="x")

        
        def do_backup():
            self._do_database_backup()



        def do_restore():
            f = filedialog.askopenfilename(filetypes=[("Database", "*.db")])
            if f:
                def final_restore():
                    try:
                        import shutil
                        # 1. Capture current credentials
                        curr_pw = self.mosque_profile.get("password", "admin")
                        curr_bp = self.mosque_profile.get("backup_path", "")
                        
                        # 2. Restore file
                        shutil.copy2(f, get_db_path())
                        
                        # 3. Reinstate credentials to the new file
                        conn = sqlite3.connect(get_db_path())
                        c = conn.cursor()
                        c.execute("UPDATE settings SET password=?, backup_path=? WHERE id=1", (curr_pw, curr_bp))
                        conn.commit()
                        conn.close()
                        
                        # 4. Reload and notify
                        self.mosque_profile = load_settings()
                        self.info("Restore", self.t("restore_success"))
                        log_action("RESTORE_DB", "maintenance", 0, 
                                   f"Database restored (Credentials Preserved) from: {os.path.basename(f)}")
                        self._nav_click("dashboard", self._show_dashboard)
                    except Exception as ex:
                        self.error("Error", str(ex))

                
                self._show_password_prompt(
                    self.t("confirm_identity"),
                    self.t("restore_warning"),
                    final_restore
                )


        ctk.CTkButton(b_frame, text=self.t("backup_data"), font=self._get_font(14, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#0f172a", height=40, corner_radius=8, command=do_backup).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(b_frame, text=self.t("restore_data"), font=self._get_font(14, "bold"), fg_color=COLOR_RED, hover_color="#ef4444", text_color="#ffffff", height=40, corner_radius=8, command=do_restore).pack(side="left", fill="x", expand=True, padx=(6, 0))

    # ──────────────────────────────────────────
    # ABOUT SCREEN
    # ──────────────────────────────────────────

    def _show_about(self):
        self._clear_content()
        self.current_view = "about"
        self._highlight_active_nav()

        wrapper = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        # Header
        hdr = ctk.CTkFrame(wrapper, fg_color="transparent")
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text=self.t("nav_about"), font=self._get_font(24, "bold"),
                     text_color=COLOR_TEXT, anchor="w").pack(side="left")

        main = ctk.CTkFrame(wrapper, fg_color="transparent")
        main.pack(fill="x", pady=20)
        main.grid_columnconfigure(0, weight=1)

        # About Project Card
        p_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        p_card.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        pi = ctk.CTkFrame(p_card, fg_color="transparent")
        pi.pack(fill="x", padx=24, pady=20)
        
        ctk.CTkLabel(pi, text=self.t("about_project"), font=self._get_font(18, "bold"), text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(0, 12))
        
        desc = (
            "Mosque Management System is a professional, offline-first desktop application designed for transparency and accountability in mosque administration.\n\n"
            "Core Features:\n"
            "• Fund Separation: Strict management of Zakat, Sadqa, and Construction funds.\n"
            "• Comprehensive Audit Log: Every action is tracked for full transparency.\n"
            "• Employee Payroll: Manage staff records and monthly salary disbursements.\n"
            "• Advanced Security: Password protection, Auto-Lock, and Audit tracking.\n"
            "• Detailed Reports: Export and print professional financial summaries.\n"
            "• Data Safety: Automated backups and local SQLite3 storage for 100% privacy."
        )

        ctk.CTkLabel(pi, text=desc, font=self._get_font(14), text_color=COLOR_TEXT_DIM, anchor="w", justify="left", wraplength=600).pack(fill="x")

        # About Developer Card
        a_card = ctk.CTkFrame(main, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        a_card.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        ai = ctk.CTkFrame(a_card, fg_color="transparent")
        ai.pack(fill="x", padx=24, pady=20)
        
        ctk.CTkLabel(ai, text=self.t("about_developer"), font=self._get_font(18, "bold"), text_color=COLOR_TEXT, anchor="w").pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(ai, text="Salman Asmat", font=self._get_font(15, "bold"), text_color=COLOR_ACCENT, anchor="w").pack(fill="x", pady=2)
        ctk.CTkLabel(ai, text="Email: salmanasmat@outlook.com", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=2)
        ctk.CTkLabel(ai, text="Website: salmanasmat.com", font=self._get_font(13), text_color=COLOR_TEXT_DIM, anchor="w").pack(fill="x", pady=2)


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    init_database()
    app = MosqueApp()
    app.mainloop()
