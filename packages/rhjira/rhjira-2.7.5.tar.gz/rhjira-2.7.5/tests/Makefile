run:
	bats -x -T --print-output-on-failure *.bats
	pytest test_util.py -v

no-dump-run:
	bats -x -T --print-output-on-failure 000[23456789]*.bats
	pytest test_util.py -v
