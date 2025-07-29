// This is the baseclass for all plugins that would like to provide a key handler
// 2022 Matthias Brunner

class KeyHandler {
  // XGEE Key handler base class

  constructor(
    key,
    preventPropagation = true,
    ctrlKey = false,
    altKey = false,
    shiftKey = false,
    caseSensitive = false,
  ) {
    this.key = key;
    this.modifiers = { ctrlKey: ctrlKey, altKey: altKey, shiftKey: shiftKey };
    this.caseSensitive = caseSensitive;
    this.preventPropagation = preventPropagation;
  }

  checkKey(key, ctrlKey, altKey, shiftKey) {
    // Checks the triggered key / key combination
    var result = false;
    if (this.caseSensitive) {
      result =
        key == this.key &&
        ctrlKey == this.modifiers.ctrlKey &&
        altKey == this.modifiers.altKey &&
        shiftKey == this.modifiers.shiftKey;
    } else {
      result =
        key.toUpperCase() == this.key.toUpperCase() &&
        ctrlKey == this.modifiers.ctrlKey &&
        altKey == this.modifiers.altKey &&
        shiftKey == this.modifiers.shiftKey;
    }
    return result;
  }

  isApplicableToEvent(key, ctrlKey, altKey, shiftKey, target) {
    // Checks whether this key handler is applicable to the key event
    var result = false;
    if (this.checkKey(key, ctrlKey, altKey, shiftKey)) {
      // Key handler specific implementation
      result = true;
    }
    return result;
  }

  action(target) {
    // The action performed by this key handler
    return true;
  }
}

export { KeyHandler };
