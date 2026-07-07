# Design Philosophy - Mosque Management System

This document outlines the core design goals, architectural choices, user experience principles, and trade-offs made in developing the Mosque Management System.

---

## 1. Problem Definition

Mosques (Masjids) are community-driven institutions that rely heavily on public donations (General, Zakat, Sadqa, and Construction funds) to cover operational expenses (utilities, maintenance, payroll).

In many parts of the world, mosque finances are managed manually on paper ledgers or generic Excel sheets. This introduces several challenges:
- **Lack of Transparency**: High risk of errors, loss of records, or lack of strict accounting trails.
- **Complexity in Fund Allocation**: Zakat funds have specific Islamic guidelines for distribution and must not be mixed with construction or general expenses.
- **Language Barriers**: Most available software is strictly English, whereas mosque administrators in regions like Pakistan, India, or the Middle East prefer operating in local languages (such as Urdu/Nastaleeq).
- **Security & Privacy Risks**: Cloud-based systems raise privacy concerns, require recurring subscriptions, and depend on unstable internet connections.

---

## 2. Why This Solution?

The Mosque Management System is designed as a **modern, local-first desktop application** that addresses all these issues:
1. **Offline-First & Local Storage**: Utilizes SQLite3 to store all records locally, ensuring 100% data privacy and zero dependence on internet availability.
2. **Dual-Language support (Urdu & English)**: Featuring a high-quality Urdu Nastaleeq typography layout designed specifically for local users.
3. **Purpose-Bound Fund Tracking**: Built-in logic segregates donations and expenses into distinct funds (Zakat, Sadqa, General, Construction) to maintain religious compliance.
4. **Zero-Configuration Setup**: Packaged as a standalone Windows installer containing a self-contained database, making installation and backup simple for non-technical users.

---

## 3. Core Design Principles

### A. Simplicity First
The users of this system are often mosque trustees or imams who may not be highly tech-literate. The UI emphasizes:
- Large, legible fonts and buttons.
- A clean, distraction-free layout (Modern Dark Theme).
- Clear, descriptive error messages and warnings in both English and Urdu.

### B. High Reliability and Integrity (Audit Trail)
Financial software must prevent accidental or malicious manipulation of records.
- **Soft Delete**: Deleting a transaction does not erase it from the database; it flags it as deleted, keeping historical reports intact.
- **Audit Logging**: Every single create, edit, or delete action is logged in an immutable system table with timestamps and descriptions.

### C. Offline Security
Physical security of the computer is reinforced by application-level controls:
- **Startup Protection**: The application is locked with a password by default.
- **Session Auto-Lock**: Automatically locks the screen after 10 minutes of inactivity to prevent unauthorized access if the computer is left unattended.

---

## 4. Target Audience & Use Cases

- **Mosque Trustees & Administrators**: Tracking daily/weekly collections and monthly expense logs.
- **Imams & Moazzins**: Accessing system reports and managing payroll disbursements.
- **Auditors & Donors**: Reviewing printable monthly ledger summaries for transparency.

---

## 5. Real-World Workflow Fit

The application fits seamlessly into a mosque’s administrative schedule:
- **Friday Prayers**: Record large collection summaries quickly under the *Add Donation* panel.
- **Monthly Utilities**: Log electricity/gas bills, selecting the appropriate payment method (Cash/Bank) and funding source.
- **Payroll (End of Month)**: Access the *Employees* page to disburse salaries to Imam, Moazzin, or cleaners with one-click balance validations.
- **Reporting**: Print and display the *Monthly Report* on the mosque bulletin board for public accountability.

---

## 6. Trade-offs & Constraints

- **Local Monolith vs. Cloud Sync**: By choosing a local SQLite database, we trade off real-time multi-device sync and remote mobile access for 100% privacy, speed, and offline reliability.
- **CustomTkinter GUI**: We chose Python's CustomTkinter library to maintain a native feel with modern dark mode styling, avoiding heavy web-view frameworks like Electron which consume high memory.
- **Manual Backups**: Automated backups are performed locally (to a user-selected path or USB drive) rather than on cloud storage, placing backup responsibility on the local administrator.
