set PATHONPATH=`pwd`
coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v --ignore=fe/data --ignore=fe/test/additional_test
coverage combine
coverage report
coverage html