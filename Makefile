.PHONY: all
all: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-run)

.PHONY: time
time: $(foreach dir,$(sort $(wildcard [012]*)),day-$(dir)-time)

.PHONY: day-%
day-%: run.py %/go.py %/test*.txt %/input.txt
	/usr/bin/time python3 run.py -t $*
	/usr/bin/time python3 run.py $*

.PHONY: day-%-run
day-%-run: run.py %/go.py %/input.txt
	python3 run.py $*

.PHONY: day-%-time
day-%-time: run.py %/go.py %/input.txt
	/usr/bin/time python3 run.py $*

.PHONY: clean
clean:
	rm -rf *~ */*~ */__pycache__


