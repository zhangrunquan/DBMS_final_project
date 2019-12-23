set PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v --ignore=fe/data --ignore=fe/test/additional_test --ignore=fe/test/test_bench.py
coverage combine
coverage report
coverage html