# Business Management System

A comprehensive Django web application for managing business operations including inventory, sales tracking, and profit analysis.

## 🚀 Features

### 📊 Dashboard
- **Real-time Statistics**: Total products, daily sales, profits, and low stock alerts
- **Interactive Charts**: Sales and profit trends using Chart.js
- **Quick Actions**: Fast access to common tasks
- **Low Stock Alerts**: Automatic warnings when inventory is running low (≤5 units)

### 📦 Inventory Management
- **Product Management**: Add, edit, delete, and view products
- **Category Organization**: Organize products by categories
- **Stock Tracking**: Real-time stock levels with low stock warnings
- **Supplier Information**: Track supplier details for each product
- **Profit Calculations**: Automatic profit per unit and margin calculations

### 💰 Sales & Profit Tracking
- **Sale Recording**: Easy-to-use interface for recording sales
- **Automatic Calculations**: Total cost and profit calculated automatically
- **Stock Deduction**: Inventory automatically updated after each sale
- **Customer Tracking**: Optional customer information for each sale
- **Sales History**: Comprehensive sales records with filtering options

### 📈 Reports & Analytics
- **Sales Reports**: Detailed analysis of sales performance
- **Profit Analysis**: Profit margins and performance metrics
- **Product Performance**: Top selling and most profitable products
- **Export Options**: CSV and PDF export functionality
- **Date Range Filtering**: Filter reports by custom date ranges

### 🔐 User Authentication
- **Secure Login**: Django's built-in authentication system
- **User Management**: Admin can manage staff accounts
- **Permission Control**: Role-based access control
- **Session Management**: Secure session handling

## 🛠️ Technology Stack

- **Backend**: Django 5.0.14
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (default, easily configurable for MySQL/PostgreSQL)
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome
- **PDF Generation**: ReportLab
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   cd /workspace/BusinessManagementSystem
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Or use the pre-created admin account:
   - **Username**: admin
   - **Password**: admin123

5. **Load sample data (optional)**
   ```bash
   python create_sample_data.py
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 📱 Usage Guide

### Getting Started
1. **Login** with your credentials (admin/admin123 for demo)
2. **Dashboard** provides an overview of your business metrics
3. **Add Products** through the Inventory section
4. **Record Sales** to track transactions and update inventory
5. **View Reports** for business insights and analytics

### Key Workflows

#### Adding a New Product
1. Navigate to Inventory → Add Product
2. Fill in product details (name, category, prices, quantity, supplier)
3. System automatically calculates profit margins
4. Save to add to inventory

#### Recording a Sale
1. Navigate to Sales → Record Sale
2. Select product from dropdown (shows available stock)
3. Enter quantity and optional customer details
4. System automatically:
   - Calculates total cost and profit
   - Updates inventory levels
   - Prevents overselling

#### Viewing Reports
1. Navigate to Reports section
2. Choose from Sales, Profit, or Product Performance reports
3. Use filters to customize date ranges
4. Export data as CSV or PDF

### Low Stock Management
- Products with ≤5 units automatically show low stock warnings
- Dashboard displays low stock count and affected products
- Low Stock page shows all products needing restocking

## 🏗️ Project Structure

```
BusinessManagementSystem/
├── BusinessManagementSystem/     # Main project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI configuration
├── dashboard/                   # Dashboard app
│   ├── views.py                 # Dashboard views and charts
│   └── urls.py                  # Dashboard URLs
├── inventory/                   # Inventory management
│   ├── models.py                # Product model
│   ├── views.py                 # Inventory views
│   ├── forms.py                 # Product forms
│   └── admin.py                 # Admin configuration
├── sales/                       # Sales tracking
│   ├── models.py                # Sale model
│   ├── views.py                 # Sales views
│   ├── forms.py                 # Sale forms
│   └── admin.py                 # Admin configuration
├── reports/                     # Reports and analytics
│   ├── views.py                 # Report views and exports
│   └── urls.py                  # Report URLs
├── templates/                   # HTML templates
│   ├── base.html                # Base template
│   ├── dashboard/               # Dashboard templates
│   ├── inventory/               # Inventory templates
│   ├── sales/                   # Sales templates
│   └── reports/                 # Report templates
├── static/                      # Static files (CSS, JS, images)
├── requirements.txt             # Python dependencies
└── create_sample_data.py        # Sample data generator
```

## 🎯 Key Features Explained

### Automatic Profit Calculation
- **Real-time Calculations**: Profit per unit and margins calculated automatically
- **Visual Indicators**: Color-coded profit margins in admin and views
- **Performance Tracking**: Track which products are most profitable

### Stock Management
- **Real-time Updates**: Stock levels updated immediately after sales
- **Prevention System**: Cannot sell more than available stock
- **Alert System**: Visual warnings for low stock items
- **Inventory Valuation**: Calculate total inventory value

### Business Intelligence
- **Trend Analysis**: 7-day sales and profit trends with charts
- **Performance Metrics**: Top selling and most profitable products
- **Time-based Reports**: Daily, weekly, monthly profit summaries
- **Export Capabilities**: Data export for external analysis

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Intuitive Interface**: Clean, modern design with clear navigation
- **Real-time Feedback**: Instant calculations and validations
- **Error Handling**: Comprehensive error messages and validations

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. To use MySQL or PostgreSQL:

1. Install the appropriate database adapter:
   ```bash
   pip install mysqlclient  # For MySQL
   pip install psycopg2     # For PostgreSQL
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',  # or postgresql
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',  # or 5432 for PostgreSQL
       }
   }
   ```

### Environment Variables
For production, use environment variables for sensitive settings:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `DATABASE_URL`: Database connection string

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for secrets
4. Set up proper database (MySQL/PostgreSQL)
5. Configure static file serving
6. Set up HTTPS
7. Configure email settings for notifications

### Sample Production Settings
```python
# settings.py
import os
from pathlib import Path

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support, please:
1. Check the documentation above
2. Review the code comments
3. Create an issue on the repository
4. Contact the development team

## 🎓 Learning Objectives

This project demonstrates:
- **Django Best Practices**: Proper project structure, models, views, templates
- **Database Design**: Efficient relationships and queries
- **User Interface**: Modern, responsive web design
- **Business Logic**: Real-world business process automation
- **Security**: Authentication, authorization, and data validation
- **Performance**: Optimized queries and efficient data handling

---

**Built with ❤️ using Django and modern web technologies**