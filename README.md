korebase-django/
├── manage.py
├── requirements.txt                  # Todas las dependencias
├── build.sh                          # Script de build para Render
├── .env.example                      # Template de variables de entorno
│
├── korebase/                         # Proyecto principal
│   ├── settings.py                   # ✅ PostgreSQL, WhiteNoise, Cloudinary
│   ├── urls.py                       # URLs principales
│   └── wsgi.py
│
├── core/                             # Módulo: Autenticación
│   ├── models.py                     # CustomUser, Permission, Role
│   ├── views.py                      # login, logout, dashboard
│   ├── urls.py
│   ├── admin.py
│   └── templates/core/
│       ├── login.html
│       └── dashboard.html
│
├── logistica/                        # Módulo: SCM
│   ├── models.py                     # Warehouse, Product, Stock, StockMovement, Supplier
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/logistica/
│       └── index.html
│
├── produccion/                       # Módulo: MRP
│   ├── models.py                     # BillOfMaterial, BOMLine, WorkOrder
│   ├── views.py
│   ├── urls.py
│   └── templates/produccion/
│       └── index.html
│
├── financiero/                       # Módulo: Contabilidad (SAGRADO)
│   ├── models.py                     # ChartOfAccounts, JournalEntry (INMUTABLE), Invoice
│   ├── views.py
│   ├── urls.py
│   └── templates/financiero/
│       └── index.html
│
├── templates/                        # Templates globales
│   └── base.html                     # Base con HTMX + Tailwind CSS
│
├── static/
│   ├── css/
│   └── js/
│       └── htmx.min.js              # HTMX library
│
└── venv/                             # Virtual environment
