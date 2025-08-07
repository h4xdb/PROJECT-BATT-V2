# Battery Repair ERP System

## Project Overview
A Flask-based ERP system for battery repair shops with features for:
- Customer and battery management
- Status tracking and history
- User authentication (admin, staff, technician roles)
- Receipt and bill generation
- Search functionality

## Project Architecture
- **Backend**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (migrated from SQLite for Replit compatibility)
- **Authentication**: Flask-Login with role-based access
- **Deployment**: Gunicorn WSGI server

## User Preferences
- Prefer web-based interfaces over API endpoints
- Focus on clean, functional UI
- Robust security practices required

## Recent Changes
- **2025-08-07**: Dashboard UI redesigned to match inventory interface design
- Main dashboard now uses modern card-based layout with hover effects and better visual hierarchy
- Statistics cards redesigned with larger display icons and consistent spacing
- Quick actions section reorganized with better button grouping and responsive design
- Recent activity table improved with better column structure and status badges
- Added comprehensive reports section for admin/staff users with analytics tools
- Dashboard now provides direct access to inventory management alongside all existing features
- **2025-08-02**: Complete offline functionality with dark/light theme toggle implemented
- Self-contained FontAwesome icons and Bootstrap CSS for true offline operation
- Added theme toggle button in navigation bar with persistent localStorage settings
- Enhanced Docker deployment support with offline-first CSS architecture
- System now works completely without internet connectivity while maintaining all features
- **2025-08-02**: Hybrid online/offline styling system implemented
- Primary: Uses Bootstrap CDN dark theme for best online experience  
- Fallback: Complete offline CSS when internet unavailable
- Maintains identical layout and functionality in both modes
- **2025-08-02**: Internal clock system with accurate Indian timezone
- Added live clock display in navigation bar with real-time updates using system time
- All database timestamps now use Indian Standard Time (IST) automatically
- Fixed recent batteries filter to show only pending and ready status batteries
- Clock syncs with system time using proper JavaScript timezone handling
- **2025-08-02**: Major workflow and feature enhancements (Migration + New Features)
- Extended battery status workflow: Added "Delivered", "Returned", and "Not Repairable" status options
- Implemented comprehensive staff notes system for battery follow-ups with note types (followup, reminder, issue, resolved)
- Added QR code sticker printing functionality for battery identification labels with offline fallback
- Created offline-compatible CSS styles for Docker container deployment without internet access
- Updated dashboard with 5-card statistics layout including "Not Repairable" count
- Enhanced battery details page with staff notes, delivery actions, and complete status history
- Added dedicated "Delivered Batteries" page to view all delivered, returned, and not repairable batteries
- Integrated note system into finished batteries page with edit icons and modals
- Added delivery/return buttons directly on bill page for immediate status updates
- Made all battery IDs clickable throughout the system (Ready → Bill page, Others → Details page)
- Updated Docker configuration for offline operation with OFFLINE_MODE environment flag
- Added delivery/return tracking with comments and staff assignment
- Enhanced technician panel with simplified Pending/Ready/Not Repairable workflow
- Updated all status badges throughout system with consistent color coding
- Added "Delivered" and "Not Repairable" navigation menu items for staff and admin users
- Enhanced finished batteries page with quick note adding functionality
- Updated search results to use new status badges and detail page linking
- Created dedicated "Not Repairable Batteries" page with specialized functionality
- Made all dashboard statistic cards clickable with hover effects for quick navigation
- Separated delivered/returned batteries from not repairable batteries in dedicated pages
- Added warranty return functionality to reopen completed batteries for warranty work
- Enhanced finished and delivered battery pages with warranty reopening capability
- **2025-08-02**: Hardcoded Docker configuration for zero-setup deployment
- All credentials and settings hardcoded in docker-compose.yml and Dockerfile
- Added automated startup scripts (run-docker.sh and run-docker.bat) for one-click deployment
- Docker setup requires no configuration - just run and use
- Added comprehensive "All Bills" page with revenue tracking, status filtering, and bulk actions
- Enhanced navigation with All Bills menu item and Quick Actions integration
- **2025-08-02**: Enhanced billing and revenue system improvements
- Updated revenue calculations to only include delivered/returned batteries (not ready status)
- Enhanced all battery listing pages to show total prices including pickup charges
- Restricted bill printing access to delivery area only for completed workflow control
- Bills only accessible from delivered batteries section after order completion
- **2025-08-01**: Successfully migrated from Replit Agent to Replit environment
- Database migrated from SQLite to PostgreSQL for production readiness
- Added ProxyFix middleware for proper HTTPS URL generation
- Updated configuration for environment variables
- Fixed backup and restore functionality - now fully operational
- Added pickup service charge functionality for batteries collected from customer sites
- Enhanced revenue calculations to include pickup service charges

## Environment Variables Required
- `SESSION_SECRET`: Flask session secret key
- `DATABASE_URL`: PostgreSQL connection string (auto-provided by Replit)

## Database Models
- User: Authentication and role management
- Customer: Customer information
- Battery: Battery tracking with auto-generated IDs
- BatteryStatusHistory: Status change tracking
- SystemSettings: Configurable system parameters