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

bool check_key_down(int row_pin, int column_pin) {
  digitalWrite(row_pin, LOW);

  bool out = (digitalRead(column_pin) == LOW);
  digitalWrite(row_pin, HIGH);

  return out;
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

void check_key_state(int pin, char & flag) {
  if (digitalRead(pin) == LOW) {
      if (flag == '0') {
        flag = '1';
      }
  }
  else {
    flag = '0';
  }
}
"""