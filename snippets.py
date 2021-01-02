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

void check_key(int pin, int & flag, char ch, int row, int column) {
  if (digitalRead(pin) == LOW) {
      if (flag == 0) {
        Keyboard.press(ch);        
        if (DEBUG == 1) {
          Serial.print(row);
          Serial.print(",");
          Serial.println(column);
        }
        flag = 1;
      }
    }
    else {
      flag = 0;
      Keyboard.release(ch);
    }
}
"""