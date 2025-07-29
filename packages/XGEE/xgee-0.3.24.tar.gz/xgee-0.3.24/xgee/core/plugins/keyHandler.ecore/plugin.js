export async function init(pluginAPI) {
  class RemoveEcoreKeyHandler extends pluginAPI.getInterface("editor.keys") {
    constructor(...args) {
      super(...args);
    }
    action(target) {
      if (target.isVertex) target.graphObject.delete();
      if (target.isEdge) target.graphObject.delete(target.edgeSource, target.edgeTarget);
    }
  }

  pluginAPI.implement(
    "editor.keys",
    new RemoveEcoreKeyHandler("Delete", true, false, false, false, true),
  );

  return true;
}

export var meta = {
  id: "keyHandler.ecore",
  description: "Generic keyhandler for ecore eObjects for standard operations",
  author: "Matthias Brunner",
  version: "0.1.0",
  requires: ["keyHandler", "editor"],
};
