# Release Notes - Mosque Management System

All notable changes to this project will be documented in this file.

---

## [v1.0.0] - 2026-07-07

### 🚀 New Features
- **Audit Logging System**: Introduced a detailed system tracking all financial and administrative actions for transparency.
- **Soft-Delete Safeguard**: Added soft-delete mechanism with timestamps for donations and expenses to protect against accidental data loss.
- **Fund-Specific Controls**: Strict purpose-based tracking of funds (General, Zakat, Sadqa, Construction) with warning validations.
- **Personnel Payroll & HR**: Complete monthly salary disbursement system for mosque employees (Imams, Moazzins, Cleaners) with duplicate payment prevention.
- **Security Features**: Implemented startup locking screen, session auto-locking for inactivity, and in-app password management.
- **Automated Backups**: Created persistent backup utilities with user-configurable default paths.

### ⚡ Improvements
- **Urdu Localization**: Beautiful and professional Urdu translations (Jameel Noori Nastaleeq font) with a seamless, instant toggle option in the UI.
- **Modern Theme**: Clean, responsive dark mode GUI built using CustomTkinter with detailed cards, interactive charts, and styled tables.

### 📚 Documentation
- **Architecture & Codebase Tour**: Added [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) detailing architecture, schemas, and flow.
- **Design Philosophy**: Created [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) covering engineering decisions, UX, and offline-first priorities.
- **Contribution Guide**: Established [CONTRIBUTING.md](CONTRIBUTING.md) with guidelines for open source collaboration.
- **Refactored Readme**: Polished [README.md](README.md) with structured feature lists and installation guides.

### 🏗️ Infrastructure & Maintenance
- **Licensing**: Established GPL v3 license headers across codebase files and added full [LICENSE](LICENSE).
- **Executable Compiler**: Included PyInstaller spec file and Inno Setup configuration for building standalone Windows binaries and installers.
- **Username Normalization**: Normalized git authors and repository details to prepare for GitHub release.
