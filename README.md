# Identity Reconciliation Service

## Overview

A Django-based service that reconciles customer contact information by identifying and linking contacts that share either an email address or phone number.

## Features

- Receives customer contact information via API
- Identifies all connected contacts
- Returns a consolidated contact object
- Supports both primary and secondary contacts
- Automatically links related contacts

## API Endpoint

### POST `/identify/`

**Request:**
```json
{
  "email": "string",
  "phoneNumber": "string",
  "id": "integer"
}
```

**Response:**
```json
{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["string"],
    "phoneNumbers": ["string"],
    "secondaryContactIds": [2, 3]
  }
}
```


## Development Setup

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

## Requirements

- Python 3.10+
- Django 4.2+

## Architecture

- **Models**: Contact (with email, phoneNumber, linkPrecedence)
- **Services**: IdentityReconciliationService (core logic)
- **Views**: API endpoint for identity reconciliation
- **Serializers**: Request/response validation

## Testing

```bash
python manage.py runserver 0:8000
```
