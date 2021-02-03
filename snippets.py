preamble = """
#include "Keyboard.h"
#include "Mouse.h"

#define HOLD_DELAY 200
#define DEBOUNCE_PERIOD 10
#define WHEEL_UP 1
#define WHEEL_DOWN -1
#define WHEEL_SENSITIVITY 10

"""

functions = """

enum Device: byte {
  KEYBOARD,
  CTRL,
  ALT,
  SUPER_SHIFT,
  CTRL_B,
  WHEEL,
  MOUSE,
  NONE,
};

struct KeyMeta {
  char code;
  Device device;
};

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

char check_col_down(int column_pin) {
  if (digitalRead(column_pin) == LOW) {
    return '1';
  }
  return '0';
}

bool is_keyboard(Device device) {
  if (device == Device::KEYBOARD || device == Device::CTRL || device == Device::ALT || device == Device::SUPER_SHIFT || device == Device::CTRL_B) { return true; }
  return false;
}


bool is_printable(char ch) {
    return ((int)ch > 31 && (int)ch < 128);
}


void press_gen(char ch, Device device, bool send_on_release) {
  if (ch == NO_OP) {return;}
  if (send_on_release) {return;}
  if (device == Device::WHEEL) {
    Mouse.move(0, 0, (int)ch*WHEEL_SENSITIVITY);
    return;
  }
  if (is_keyboard(device)) {
    if (device == Device::CTRL) {
        Keyboard.press(KEY_LEFT_CTRL);
    }
    if (device == Device::ALT) {
        Keyboard.press(KEY_LEFT_ALT);
    }
    if (device == Device::SUPER_SHIFT) {
        Keyboard.press(KEY_LEFT_GUI);
        Keyboard.press(KEY_LEFT_SHIFT);
    }
    if (device == Device::CTRL_B && is_printable(ch)) {
        Keyboard.press(KEY_LEFT_CTRL);
        Keyboard.write('b');
        Keyboard.release(KEY_LEFT_CTRL);
    }
    Keyboard.press(ch);
  }
  else {
    Mouse.press(ch);
  }
}

void release_gen(char ch, Device device, bool send_on_release) {
  if (ch == NO_OP) {return;}

  if (device == Device::WHEEL) {return;}
  if (is_keyboard(device)) {
    if (!send_on_release) {
        if (device == Device::CTRL) {
            Keyboard.release(KEY_LEFT_CTRL);
        }
        if (device == Device::ALT) {
            Keyboard.release(KEY_LEFT_ALT);
        }
        if (device == Device::SUPER_SHIFT) {
            Keyboard.release(KEY_LEFT_GUI);
            Keyboard.release(KEY_LEFT_SHIFT);
        }
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

class IndKeyMap {
  public:
  KeyMeta primary;
  char secondary;
  IndKeyMap() : primary((KeyMeta){255, Device::NONE}), secondary(255) {}
  IndKeyMap(char code) : primary((KeyMeta){code, Device::KEYBOARD}), secondary(code) {}
  IndKeyMap(char code, Device dev) : primary((KeyMeta){code, dev}), secondary(code) {}
  IndKeyMap(char code, Device dev, char code_sec) : primary((KeyMeta){code, dev}), secondary(code_sec) {}
};


enum KeyState: byte {
    KEY_DOWN,
    KEY_UP,
    KEY_UP_FROM_DOWN,
    KEY_DOWN_FROM_UP,
    KEY_DEBOUNCING,
    KEY_UNK
};


class KeyTracker {
  bool was_down;
  bool down_sent;

  bool currently_down();
  IndKeyMap _map;
  char _picked_code;
  char _picked_device;
public:
  unsigned long downed_at;
  KeyState state;
  KeyTracker();
  bool update(bool is_down);
  void emit(IndKeyMap map, bool at_least_one_downed_after, bool at_least_one_downed_before);
  unsigned long down_for();
  bool primary_down();
  bool long_down();
  bool up();
  bool down_longer_than_others(bool at_least_one_downed_after);
};

KeyTracker::KeyTracker() : state(KeyState::KEY_UP), downed_at(0), was_down(false), down_sent(false) {}

bool KeyTracker::update(bool is_down) {
  if (was_down && state == KeyState::KEY_DOWN_FROM_UP) {state = KeyState::KEY_DOWN;}
  if (!was_down && state == KeyState::KEY_UP_FROM_DOWN) {state = KeyState::KEY_UP;}

  if (!was_down && is_down) {state = KeyState::KEY_DEBOUNCING; downed_at = millis();}
  if (was_down && is_down && state == KeyState::KEY_DEBOUNCING && down_for() > DEBOUNCE_PERIOD) {state = KeyState::KEY_DOWN_FROM_UP;}
  if (was_down && !is_down) {state = KeyState::KEY_UP_FROM_DOWN;}

  was_down = is_down;
  
  return (KeyState::KEY_DOWN_FROM_UP == state);
}

bool KeyTracker::primary_down() {
  return (state == KeyState::KEY_DOWN || state == KeyState::KEY_DOWN_FROM_UP);
}

bool KeyTracker::long_down() {
  return (state == KeyState::KEY_DOWN && down_for() > HOLD_DELAY);
}

bool KeyTracker::up() {
  return (state == KeyState::KEY_UP || state == KeyState::KEY_UP_FROM_DOWN);
}

unsigned long KeyTracker::down_for() {
  return millis() - downed_at;
}

void KeyTracker::emit(IndKeyMap map, bool at_least_one_downed_after, bool at_least_one_downed_before=false) {
  if (!down_sent) {_map = map;}
  if (_map.primary.code == _map.secondary || down_for() > HOLD_DELAY || down_sent) {
    if (state == KeyState::KEY_UP_FROM_DOWN) {
        release_gen(_picked_code, _picked_device, false);
        down_sent = false;
        return;
    }
    if (state == KeyState::KEY_DOWN_FROM_UP && !down_sent) {
        _picked_code = _map.primary.code;
        _picked_device = _map.primary.device;
        press_gen(_map.primary.code, _map.primary.device, false);
        down_sent = true;
    }
  }
  if (state == KeyState::KEY_DOWN && (down_for() > HOLD_DELAY || at_least_one_downed_after) && !down_sent) {
    _picked_code = _map.primary.code;
    _picked_device = _map.primary.device;
    press_gen(_map.primary.code, _map.primary.device, false);
    down_sent = true;
  }
  if (down_for() <= HOLD_DELAY && _map.primary.code != _map.secondary && (state == KeyState::KEY_UP_FROM_DOWN || (state == KeyState::KEY_DOWN_FROM_UP && at_least_one_downed_before)) && !down_sent) {
    if (at_least_one_downed_before && is_printable(_map.secondary) && state == KeyState::KEY_DOWN_FROM_UP) {
      _picked_code = _map.secondary;
      _picked_device = Device::KEYBOARD;
      press_gen(_picked_code, _picked_device, false);
      down_sent = true;
    } else if (state == KeyState::KEY_UP_FROM_DOWN) {
      release_gen(_map.secondary, Device::KEYBOARD, true);
    }
}
}

bool KeyTracker::down_longer_than_others(bool at_least_one_downed_after) {
  if (state == KeyState::KEY_DOWN_FROM_UP || this->up()) {return false;}
  return at_least_one_downed_after;
}

"""