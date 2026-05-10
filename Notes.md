creative_workshop/
│
├── main.py                  ← Person 6: app entry point, navigation
├── db_connection.py         ← Person 1: shared DB connection (everyone imports this)
├── requirements.txt         ← list of pip packages
│
├── modules/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login_view.py        ← Person 2
│   │   ├── signup_view.py       ← Person 2
│   │   └── member_queries.py    ← Person 2: all SQL for members
│   │
│   ├── studio/
│   │   ├── __init__.py
│   │   ├── studio_view.py       ← Person 3
│   │   ├── booking_view.py      ← Person 3
│   │   └── studio_queries.py    ← Person 3: all SQL for studios
│   │
│   ├── workshop/
│   │   ├── __init__.py
│   │   ├── workshop_view.py     ← Person 4
│   │   ├── registration_view.py ← Person 4
│   │   └── workshop_queries.py  ← Person 4: all SQL for workshops
│   │
│   ├── inventory/
│   │   ├── __init__.py
│   │   ├── materials_view.py    ← Person 5
│   │   ├── rental_view.py       ← Person 5
│   │   └── inventory_queries.py ← Person 5: all SQL for materials & tools
│   │
│   └── reports/
│       ├── __init__.py
│       ├── reports_view.py      ← Person 6
│       └── reports_queries.py   ← Person 6: all 6 inquiry queries
│
├── database/
│   ├── schema.sql           ← Person 1: CREATE TABLE statements
│   └── seed_data.sql        ← Person 1: INSERT sample data
│
└── assets/
    └── logo.png             ← optional branding

    