all:
	python3 generator.py
upload_right:
	python3 generator.py
	arduino-cli compile /tmp/dactyl_right --fqbn arduino:avr:micro && sudo -E arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:micro /tmp/dactyl_right --verbose
upload_left:
	python3 generator.py
	arduino-cli compile /tmp/dactyl_left --fqbn arduino:avr:micro && sudo -E arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:micro /tmp/dactyl_left --verbose