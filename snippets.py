preamble = """
#include "Keyboard.h"
#include "Mouse.h"

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

void press_gen(char ch, bool is_mouse) {
  if (!is_mouse) {
    Keyboard.press(ch);
  }
  else {
    Mouse.press(ch);
  }
}

void release_gen(char ch, bool is_mouse) {
  if (!is_mouse) {
    Keyboard.release(ch);
  }
  else {
    Mouse.release(ch);
  }
}

void check_key(int pin, char & flag, char ch, int row, int column, bool is_mouse = false) {
  if (digitalRead(pin) == LOW) {
      if (flag == '0') {
        press_gen(ch, is_mouse);
        flag = '1';
      }
    }
    else {
      if (flag == '1') {
        flag = '0';
        release_gen(ch, is_mouse);
      }
    }
}

void hold_key(char & state, char & flag, char ch, bool is_mouse = false) {
  if (state == '1') {
      if (flag == '0') {
        press_gen(ch, is_mouse);
        flag = '1';
      }
    }
    else {
      if (flag == '1') {
        flag = '0';
        release_gen(ch, is_mouse);
      }
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