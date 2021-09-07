all:
	python3 generator.py
compile:
	python3 generator.py
	arduino-cli compile /tmp/dactyl_right --fqbn arduino:avr:micro
	arduino-cli compile /tmp/dactyl_left --fqbn arduino:avr:micro
upload_right:
	python3 generator.py
	arduino-cli compile /tmp/dactyl_right --fqbn arduino:avr:micro && sudo -E arduino-cli upload -p `arduino-cli board list | grep ACM | cut -d ' ' -f 1` --fqbn arduino:avr:micro /tmp/dactyl_right --verbose
upload_left:
	python3 generator.py
	arduino-cli compile /tmp/dactyl_left --fqbn arduino:avr:micro && sudo -E arduino-cli upload -p `arduino-cli board list | grep ACM | cut -d ' ' -f 1` --fqbn arduino:avr:micro /tmp/dactyl_left --verbose