rm -rf .coverage
coverage run --parallel-mode --omit "/usr/*" src/tests/cruise_test.py
coverage run --parallel-mode --omit "/usr/*" src/tests/website_test.py
coverage combine
coverage report
coverage xml
