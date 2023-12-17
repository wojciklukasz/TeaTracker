# TeaTracker
## A Django project to help manage your tea (and maybe other drinks) collection

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=wojciklukasz_TeaTracker&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=wojciklukasz_TeaTracker)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=wojciklukasz_TeaTracker&metric=bugs)](https://sonarcloud.io/summary/new_code?id=wojciklukasz_TeaTracker)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=wojciklukasz_TeaTracker&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=wojciklukasz_TeaTracker)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=wojciklukasz_TeaTracker&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=wojciklukasz_TeaTracker)

### Planned features
- profile based collection tracking (could be upgrated to accounts)
- convinient storage for information about drinks
- ability to add brewing sessions to specific drinks

### Running from source
1. This project requires Python 3.8 or newer
2. Run python -m pip install requirements.txt
3. Required environmental variables can be found in TeaTracker/settings.py
4. Run python manage.py runserver to start the application