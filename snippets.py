preamble = """
#include "Keyboard.h"
"""

functions = """
void setup_input(int pin) {
  pinMode(pin, INPUT_PULLUP);
}

void setup_output(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
}

void check_key(int pin, int & flag, char ch) {
  if (digitalRead(pin) == LOW) {
      if (flag == 0) {
        Keyboard.press(ch);        
        flag = 1;
      }
    }
    else {
      flag = 0;
      Keyboard.release(ch);
    }
}
"""