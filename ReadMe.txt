# Bidwork

## Installation

### Requirements:
- Django~=3.1.2
- Selenium (Testing)
- behave_django (Testing)
- factory_boy (Testing)

### Step-by-step installation for Linux
```
conda create --name team01 python=3.6
conda activate team01
cd team01
pip install -r requirements.txt
cd Bidwork

```

## Testing

### Instructions for running testing
Set managed=True for Items and Biddings Model in sellers/migrations/000_initial.py
```
python manage.py behave
```
