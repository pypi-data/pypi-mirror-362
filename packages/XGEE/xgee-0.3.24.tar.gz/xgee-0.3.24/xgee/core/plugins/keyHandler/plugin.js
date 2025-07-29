export async function init(pluginAPI) {
  var keyhandlerModules = await pluginAPI.loadModules(["js/KeyHandler.js"]);
  pluginAPI.expose({ GenericKeyHandler: keyhandlerModules[0].KeyHandler });
  return true;
}

export var meta = {
  id: "keyHandler",
  description: "Generic key handler definition for XGEE",
  author: "Matthias Brunner",
  version: "0.0.1",
  requires: [],
};
