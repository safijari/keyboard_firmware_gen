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

enum Device: byte {
  KEYBOARD,
  MOUSE,
  NONE,
};

struct KeyMeta {
  char code;
  Device device;
};

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
    KEY_UNK
};


class KeyTracker {
  unsigned long downed_at;
  bool was_down;
  bool down_sent;

  bool currently_down();
  IndKeyMap *_map;
public:
  KeyState state;
  KeyTracker();
  void update(bool is_down);
  void emit(IndKeyMap *map);
  unsigned long down_for();
  bool primary_down();
  bool up();
};

KeyTracker::KeyTracker() : state(KeyState::KEY_UP), downed_at(0), was_down(false), down_sent(false) {}

void KeyTracker::update(bool is_down) {
  if (was_down && state == KeyState::KEY_DOWN_FROM_UP) {state = KeyState::KEY_DOWN;}
  if (!was_down && state == KeyState::KEY_UP_FROM_DOWN) {state = KeyState::KEY_UP;}

  if (!was_down && is_down) {state = KeyState::KEY_DOWN_FROM_UP; downed_at = millis();}
  if (was_down && !is_down) {state = KeyState::KEY_UP_FROM_DOWN;}

  was_down = is_down;
  if (primary_down()) {
    Serial.println(down_for());
  }
}

bool KeyTracker::primary_down() {
  return (state == KeyState::KEY_DOWN || state == KeyState::KEY_DOWN_FROM_UP);
}

bool KeyTracker::up() {
  return (state == KeyState::KEY_UP || state == KeyState::KEY_UP_FROM_DOWN);
}

unsigned long KeyTracker::down_for() {
  return millis() - downed_at;
}

void KeyTracker::emit(IndKeyMap *map) {
  auto p = 95;
  if (state == KeyState::KEY_UP) {_map = map;}
  if (_map->primary.code == _map->secondary || down_for() > p) {
    if (state == KeyState::KEY_UP_FROM_DOWN) {
        release_gen(_map->primary.code, map->primary.device == Device::MOUSE, false);
        down_sent = false;
    }
    if (state == KeyState::KEY_DOWN_FROM_UP && !down_sent) {
        press_gen(_map->primary.code, map->primary.device == Device::MOUSE, false);
        down_sent = true;
    }
  }
  if (state == KeyState::KEY_DOWN && down_for() > p && !down_sent) {
    press_gen(_map->primary.code, map->primary.device == Device::MOUSE, false);
    down_sent = true;
  }
  if (down_for() <= p && _map->primary.code != _map->secondary && state == KeyState::KEY_UP_FROM_DOWN) {
    release_gen(_map->secondary, Device::KEYBOARD, true);
  }
}

"""