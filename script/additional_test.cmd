set PATHONPATH=`pwd`
coverage run -m pytest fe\\test\\additional_test
coverage combine
coverage report
coverage html