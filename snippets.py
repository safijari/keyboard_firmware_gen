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

bool check_key_down(int column_pin, int row_pin = -1) {
  if (row_pin != -1) {
    digitalWrite(row_pin, LOW);
  }

  bool out = (digitalRead(column_pin) == LOW);
  if (row_pin != -1) {
    digitalWrite(row_pin, HIGH);
  }

  return out;
}

void press_gen(char ch, bool is_mouse, bool send_on_release) {
  if (send_on_release) {return;}
  if (!is_mouse) {
    Keyboard.press(ch);
  }
  else {
    Mouse.press(ch);
  }
}

void release_gen(char ch, bool is_mouse, bool send_on_release) {
  if (!is_mouse) {
    if (!send_on_release) {
        Keyboard.release(ch);
    } else {
        Keyboard.write(ch);
    }
  }
  else {
    if (!send_on_release) {
        Mouse.release(ch);
    } else {
        Mouse.click(ch);
    }
  }
}

void hold_key(char & state, char & flag, char ch, bool is_mouse = false, bool send_on_release = false) {
  if (state == '1') {
      if (flag == '0') {
        press_gen(ch, is_mouse, send_on_release);
        flag = '1';
      }
    }
    else {
      if (flag == '1') {
        flag = '0';
        release_gen(ch, is_mouse, send_on_release);
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