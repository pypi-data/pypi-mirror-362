import * as contextMenus from "./extensions/EditorContextMenuProvider.js";
import { XGEEPublicAPI, XGEEPrivateAPI } from "./lib/libapi.js";
import * as mxGraphIntegration from "./graph/mxGraphIntegration.js"; //sets global mxGraph variables and overwrites mxGraph functions

import GraphViewMenu from "./view/GraphViewMenu.js";

import { serialPromise } from "./lib/libaux.js";
//Editor main plugin

/**
 * Return the implicit default literal for an EEnum.
 * Expects eEnum to be an actual EEnum - not checked here again
 * @param {EEnum} eEnum
 * @returns {string|undefined}
 * @private
 */
function _implicitEnumDefaultLiteral(eEnum) {
  const first = eEnum.get("eLiterals").array()[0];
  return first ? first.get("literal") || first.get("name") : undefined;
}

/**
 * Deserialize a literal value from an Ecore model to a JavaScript value.
 * @param {string} literal - the literal value as a string, e.g. "42", "3.14", "true"
 * @param {string } typeName - the Ecore type name, e.g. "EInt", "EFloat", "EBoolean"
 * @returns {*|undefined|number|boolean} - the deserialized JavaScript value
 * @private
 */
function _deserializeFromLiteral(literal, typeName) {
  if (literal == null || literal === "") return undefined;

  switch (typeName) {
    /* integer family */
    case "EInt":
    case "EIntegerObject":
    case "EShort":
    case "EByte":
    case "ELong":
    case "ELongObject":
      return parseInt(literal, 10);

    /* floating point */
    case "EFloat":
    case "EDouble":
    case "EFloatObject":
    case "EDoubleObject":
      return parseFloat(literal);

    /* boolean */
    case "EBoolean":
    case "EBooleanObject":
      return String(literal).trim().toLowerCase() === "true";

    default: // enums, strings, dates, whatever … - only tested for enums
      return literal; // hand the raw string to the client code
  }
}

/**
 * Fix default values for EAttributes in an EClass.
 * @param {EClass} eClass - the EClass to fix
 * @param logs - an array to log the changes made
 * @private
 */
function _fixDefaultsEClass(eClass, logs) {
  const structuralFeatures = eClass.get("eStructuralFeatures").array();
  structuralFeatures.forEach((feature) => {
    if (!feature.isKindOf("EAttribute")) return; // ignore references
    if (feature.get("defaultValue") !== undefined) return; // default already set

    // 1 – explicit default in the .ecore file
    let literal = feature.get("defaultValueLiteral");

    // 2 – for EEnums the implicit default is the first entry
    if (literal == null || literal === "") {
      const eType = feature.get("eType");
      if (eType?.isKindOf("EEnum")) {
        literal = _implicitEnumDefaultLiteral(eType);
      }
      if (literal == null) return; // still nothing to copy
    }

    const typeName = feature.get("eType")?.get("name");
    const jsValue = _deserializeFromLiteral(literal, typeName);
    logs.push({
      eClass: feature.eContainer.get("name"),
      attribute: feature.get("name"),
      type: typeName,
      value: jsValue,
    });
    feature.set("defaultValue", jsValue);
  });
}

/**
 * Recursively fix default values for EAttributes in an EPackage and its sub-packages.
 * @param {EPackage} ePackage - the EPackage to process - typically editorModel.ecore
 * @param logs - an array to log the changes made
 * @param seen - a Set to track already processed EPackages to avoid cycles
 * @private
 */
function _fixDefaultsEPackage(ePackage, logs, seen = new Set()) {
  if (seen.has(ePackage)) return; // guard against cycles
  seen.add(ePackage);

  // local classifiers
  const classifiers = ePackage.get("eClassifiers").array();
  const classes = classifiers.filter((c) => c.isKindOf("EClass"));
  classes.forEach((c) => _fixDefaultsEClass(c, logs));

  // nested sub-packages
  ePackage
    .get("eSubpackages")
    .array()
    .forEach((subpackage) => _fixDefaultsEPackage(subpackage, logs, seen));
}

export async function init(pluginAPI) {
  var contextMenu = pluginAPI.require("contextMenu");
  var keyHandler = pluginAPI.require("keyHandler");
  var eventBroker = pluginAPI.require("eventBroker");
  var editorResourceSet = Ecore.ResourceSet.create();

  //Read meta model
  try {
    let xmlResources = await pluginAPI.loadXMLResources(["model/editorModel.ecore"]);
    var metaModel = xmlResources[0];
    var metaModelResource = editorResourceSet.create({ uri: "EditorModels" });
    metaModelResource.parse(metaModel.txt, Ecore.XMI);
    const editorPackage = metaModelResource.get("contents").array()[0];

    // set defaultValue for EAttributes
    const fixDefaultsLogs = [];
    _fixDefaultsEPackage(editorPackage, fixDefaultsLogs);
    if ($DEBUG) {
      console.log(
        "The following EAttributes were patched with defaultValue after parsing editorModel.ecore :",
      );
      console.table(fixDefaultsLogs);
    }

    Ecore.EPackage.Registry.register(editorPackage);
  } catch (e) {
    throw "XGEE meta-model initialization failed: " + e;
  }

  // Initialize API
  var privateAPI = new XGEEPrivateAPI(pluginAPI);
  privateAPI.setResourceSet(editorResourceSet);
  privateAPI.setMetaModel(metaModel);
  privateAPI.setApplication(pluginAPI.getGlobal("app"));

  var publicAPI = new XGEEPublicAPI();

  //Compatibility hack (TODO: remove these global functions)
  window["serialPromise"] = serialPromise;

  let stylesSheets = await pluginAPI.loadStylesheets([
    "css/loading.css",
    "css/xgeeJsaIntegration.css",
  ]);

  var editorRegistry = [];
  var editorContextMenuRegistry = [];

  var editorModels = pluginAPI.provide("xgee.models", null, function (event) {
    ///register editor
    privateAPI.registerEditorFromModelPath(event.extension.modelPath);
  });

  //automatically provide edit entries for editable objects
  class EditorGenericMenuProvider extends pluginAPI.getInterface("ecoreTreeView.menus") {
    constructor() {
      super();
    }

    isApplicableToNode(node) {
      return publicAPI.canOpen(node.data.eObject);
    }

    getContextMenu(node) {
      var cMenu = false;
      if (publicAPI.canOpen(node.data.eObject)) {
        cMenu = contextMenu.createContextMenu("xgee-context-menu", "XGEE Context Menu", 100);
        var editors = publicAPI.getEditors(node.data.eObject);

        if (editors.length == 1) {
          cMenu.addNewEntry(
            "xgee-edit",
            "Edit",
            function () {
              publicAPI.open(node.data.eObject, true);
            },
            "edit",
          );
        } else if (editors.length > 1) {
          var editMenu = contextMenu.createContextMenu(
            "xgee-edit-with-submenu",
            "Edit with...",
            100,
            "edit",
          );
          editors.forEach(function (editor, i) {
            editMenu.addNewEntry(
              "xgee-edit-" + i,
              editor.get("name"),
              function () {
                publicAPI.open(node.data.eObject, true, i);
              },
              "edit",
            );
          });
          cMenu.addSubMenu("xgee-edit-with", editMenu);
        }
      }
      return cMenu;
    }
  }
  pluginAPI.implement("ecoreTreeView.menus", new EditorGenericMenuProvider());

  // XGEE context menu extension point
  var menuProviders = [];
  menuProviders.push(new GraphViewMenu(contextMenu)); //Built-In XGEE Menu Entries
  pluginAPI.provide("editor.menus", contextMenus.EditorContextMenuProvider, function (event) {
    menuProviders.push(event.extension);
  });

  //the eventBroker may need some sort of permissions for events in order to allow this kind of architecture?
  eventBroker.subscribe("XGEE/CONTEXTMENU", function (evt) {
    var applicableMenuProviders = menuProviders.filter(function (p) {
      return p.isApplicableToTarget(evt.data.target);
    });
    if (applicableMenuProviders.length > 0) {
      contextMenu.showContextMenu(
        { x: evt.data.event.pageX, y: evt.data.event.pageY },
        contextMenu.util.collectAndMerge(applicableMenuProviders, evt.data.target),
      );
    }
  });

  // XGEE key handler extension point
  var keyHandlers = [];
  pluginAPI.provide("editor.keys", keyHandler.GenericKeyHandler, function (event) {
    keyHandlers.push(event.extension);
  });

  eventBroker.subscribe("XGEE/KEYPRESS", function (evt) {
    for (const keyHandler of keyHandlers) {
      if (
        keyHandler.isApplicableToEvent(
          evt.data.key,
          evt.data.ctrlKey,
          evt.data.altKey,
          evt.data.shiftKey,
          evt.data.target,
        )
      ) {
        keyHandler.action(evt.data.target);
        if (keyHandler.preventPropagation) {
          break;
        }
      }
    }
  });

  pluginAPI.expose(publicAPI);

  return true;
}

export var meta = {
  id: "editor",
  description: "A model-based Graphical Editor for Ecore Models",
  author: "Matthias Brunner, Andreas Waldvogel",
  version: "0.1.1",
  requires: [
    "ecore",
    "ecoreSync",
    "eventBroker",
    "plugin.ecoreTreeView",
    "contextMenu",
    "keyHandler",
  ],
};
