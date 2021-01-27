preamble = """
#include "Keyboard.h"
#include "Mouse.h"

"""

functions = """

enum KeyState {
    KEY_DOWN,
    KEY_UP,
    KEY_UP_FROM_DOWN,
    KEY_DOWN_FROM_UP,
    KEY_UNK
};

class KeyTracker {
  KeyState state;
  unsigned long downed_at;
  bool was_down;

  bool currently_down();
public:
  KeyTracker();
  void update(bool is_down);
};

KeyTracker::KeyTracker() : state(KeyState::KEY_UNK), downed_at(0), was_down(false) {}

void KeyTracker::update(bool is_down) {
  if (was_down && state == KeyState::KEY_DOWN_FROM_UP) {state = KeyState::KEY_DOWN;}
  if (!was_down && state == KeyState::KEY_UP_FROM_DOWN) {state = KeyState::KEY_UP;}

  if (was_down && !is_down) {state = KeyState::KEY_DOWN_FROM_UP; downed_at = millis();}
  if (!was_down && is_down) {state = KeyState::KEY_UP_FROM_DOWN;}

  was_down = is_down;
}

void setup_input(int pin) {
  pinMode(pin, INPUT_PULLUP);
}

void setup_output(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
}

void emit_chord(char mod, char leader) {
  Keyboard.press(mod);
  Keyboard.write(leader);
  Keyboard.release(mod);
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

char check_col_down(int column_pin) {
  if (digitalRead(column_pin) == LOW) {
    return '1';
  }
  return '0';
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