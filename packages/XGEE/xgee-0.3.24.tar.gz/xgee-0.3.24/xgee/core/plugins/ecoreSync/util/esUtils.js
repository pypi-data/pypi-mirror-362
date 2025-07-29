/**
 * Module providing this.utils with utility functions for ecoreSync.
 * @module esUtils
 */

/** The main class for various utility functions in ecoreSync. */
class EsUtilities {
  /**
   * Creates an instance. Represents a utility class for ecoreSyncs.
   * @param {EsDomain} esDomain - Reverse link to the ecoreSync domain
   */
  constructor(esDomain) {
    this._esDomain = esDomain;
    this.builtInClasses = []; // stores built-in classes (Ecore M3 model classes like EPackage, EShort etc.) for isBuiltInClass()
  }

  /**
   * Initializes the EsUtilities instance.
   * Needs to be explicitly called after creation.
   * Retrieves once the built-in classes in the Ecore M3 model.
   */
  init() {
    this.builtInClasses = this.getBuiltInClasses();
  }

  /**
   * Retrieves the built-in classes in ecore.js Ecore M3 model.
   * @returns {Array<EObject>} An array of built-in classes.
   */
  getBuiltInClasses() {
    return Object.values(this._esDomain.getEcore()).filter((val) => {
      return val.eClass ? true : false;
    });
  }

  /**
   * Ensures that specified EClass is initialized.
   * @param {EObject} eClass - The EObject of the EClass to check.
   * @return TODO
   */
  async isEClassInitialized(eClass) {
    var oid = this._esDomain.rlookup(eClass);
    if (oid != null) {
      return this._esDomain.initEClass(oid, true);
    }
  }

  /**
   * Checks if an eObject is contained within a specific feature of its container eObject.
   * E.g. used to check if a feature needs to be added in initEClass().
   * @param {EObject} eContainer - The container object.
   * @param {string} featureName - The name of the feature to check.
   * @param {EObject} eObject - The object to check if it is contained within the feature.
   * @returns {boolean} - True if the object is contained within the feature, false otherwise.
   */
  isContained(eContainer, featureName, eObject) {
    var res = false;
    if (eContainer.get(featureName).array().includes(eObject)) {
      res = true;
    }
    return res;
  }

  /**
   * Checks if the given name corresponds to a Ecore M3 element.
   * very similar to isBuiltInClass()
   * used as a check before getLocalEcoreElement()
   * @param {string} name - The name of the Ecore element to check.
   * @returns {boolean} - Returns true if the name corresponds to a local Ecore element, otherwise returns false.
   */
  isLocalEcoreElement(name) {
    let res = false;
    if (name == "EInteger") name = "EInt";
    var keys = Object.keys(this._esDomain.getEcore());
    if (keys.includes(name)) {
      res = true;
    }
    return res;
  }

  /**
   * Retrieves the local Ecore M3 element by name.
   * Use 'isLocalEcoreElement()' to check if the element exists.
   * @param {string} name - The name of the Ecore element. E.g. "EString"
   * @returns {EObject|null} - The local Ecore element eObject if found, otherwise null.
   */
  getLocalEcoreElement(name) {
    let res = null;
    if (name == "EInteger") name = "EInt";
    var keys = Object.keys(this._esDomain.getEcore());
    if (keys.includes(name)) {
      res = this._esDomain.getEcore()[name];
    }
    return res;
  }

  /**
   * Checks the type of a value based on the provided eType.
   * @param {EObject} eType - The eType eObject representing the type to check against.
   * @param {*} value - The value to be checked.
   * @returns {boolean} - Returns true if the value matches the specified type, otherwise false. E.g. used by valueToQuer().
   */
  checkType(eType, value) {
    //ecoreSync integrated type checking
    var res = false;
    var typeName = "";

    switch (eType.eClass.get("name")) {
      case "EDataType":
        typeName = eType.get("name");
        break;
      case "EEnum":
        typeName = "EEnum";
        break;
      default:
        typeName = "unsupported";
        break;
    }

    switch (typeName) {
      case "EChar":
        if (typeof value == "string" && value.length == 1) res = true;
        break;
      case "EString":
        if (typeof value == "string") res = true;
        break;
      case "EInt":
        if (Number.isInteger(value) && value != null) res = true;
        break;
      case "EByte":
        if (Number.isInteger(value) && value != null) res = true;
        break;
      case "EFloat":
        if (typeof value == "number" && value != null) res = true;
        break;
      case "EDouble":
        if (typeof value == "number" && value != null) res = true;
        break;
      case "EBoolean":
        if (typeof value == "boolean") res = true;
        break;
      case "EEnum":
        if (typeof value == "string") res = true; //because EOQ expects it like this
        break;
      case "EInteger": //ecorejs compatibility support
        if (Number.isInteger(value) && value != null) res = true;
        break;
      default:
        res = true; //seems to be custom type, we won't bother with that
        break;
    }
    return res;
  }

  /**
   * Converts a value to a query-compatible format based on the provided eType.
   * Converts floats that look like an integer to a float with a small offset.
   * @param {EObject} eType - The eType object representing the type of the value.
   * @param {*} value - The value to be converted.
   * @returns {*} The converted value.
   * @throws {Error} If the supplied value is of an incompatible type.
   * @throws {Error} If the datatype conversion is unknown.
   */
  valueToQuery(eType, value) {
    var res = null;

    if (this.checkType(eType, value)) {
      var typeName = "";
      switch (eType.eClass.get("name")) {
        case "EDataType":
          typeName = eType.get("name");
          break;
        case "EEnum":
          typeName = "EEnum";
          break;
        default:
          typeName = "unsupported";
          break;
      }

      switch (typeName) {
        case "EChar":
          res = value;
          break;
        case "EString":
          res = String(value);
          break;
        case "EInt":
          res = value;
          break;
        case "EByte":
          res = value;
          break;
        case "EFloat":
          res = value;
          if (Number.isInteger(value)) res += 1e-5;
          break;
        case "EDouble":
          res = value;
          if (Number.isInteger(value)) res += 1e-5;
          break;
        case "EBoolean":
          res = value;
          break;
        case "EEnum":
          res = value;
          break;
        case "EInteger": //ecorejs compatibility support
          res = value;
          break;
        default:
          if (value != null) {
            let oid = this._esDomain.rlookup(value);
            if (oid != null) {
              res = QRY.Obj(oid);
            } else {
              throw new Error("unknown datatype conversion");
            }
          } else {
            res = value; //no conversion of null value
          }
          break;
      }
    } else {
      throw new Error("supplied value was of incompatible type");
    }
    return res;
  }

  /**
   * Checks if the given class is a built-in class.
   * Built-in classes are classes that are part of the Ecore M3 model like EPackage, EShort.
   * Allows to treat built-in classes differently.
   * @param {EObject} eClass - The class to check.
   * @returns {boolean} - Returns true if the class is built-in, false otherwise.
   */
  isBuiltInClass(eClass) {
    let res = this.builtInClasses.find((clazz) => {
      return clazz == eClass;
    })
      ? true
      : false;
    return res;
  }

  isObjectURL(url) {
    var res = false;
    if (typeof url == "string") {
      if (url.includes("eoq://") && url.includes("/#")) {
        res = true;
      }
    }
    return res;
  }

  getObjectURL(eObject) {
    var oid = this._esDomain.rlookup(eObject);
    if (oid == null) throw new Error("The supplied eObject is unknown to ecoreSync");
    return (this._esDomain.eoq2domain.url + "/#" + oid)
      .replace("ws://", "eoq://")
      .replace("ws/eoq.do/", "");
  }

  async getObjectByURL(url) {
    var res = null;
    if (this.isObjectURL(url)) {
      let domainHost = url.substr(
        url.indexOf("eoq://") + 6,
        url.indexOf("/#") - (url.indexOf("eoq://") + 6),
      );
      if (this._esDomain.eoq2domain.url.includes(domainHost)) {
        let objId = Number.parseInt(url.substr(url.indexOf("/#") + 2));
        res = this._esDomain.getObject(objId);
      }
      return res;
    }
  }

  /**
   * Retrieves the EOQ resource (file) containing the supplied eObject.
   * @param {EObject} eObject - The eObject to retrieve the resource for.
   * @returns {Promise<EObject>} - A Promise that resolves to the eObject of the EOQ resource.
   * @throws {Error} - If the supplied eObject is unknown to ecoreSync.
   */
  async getResource(eObject) {
    let oid = this._esDomain.rlookup(eObject);
    if (oid == null) throw new Error("The supplied eObject is unknown to ecoreSync");
    let cmd = CMD.Get(
      QRY.Obj(oid)
        .Met("ALLPARENTS")
        .Sel(new eoq2.Qry().Met("CLASSNAME").Equ("ModelResource"))
        .Trm(new eoq2.Met("SIZE").Equ(0), null)
        .Idx(0),
    );
    let mdlResource = await this._esDomain.remoteExec(cmd, true);
    return mdlResource;
  }

  /**
   * Retrieves the model root for the supplied eObject.
   * @param {EObject} eObject - The eObject for which to retrieve the model root.
   * @returns {Promise<EObject>} - A promise that resolves to the eObject of the model root. E.g. used to get valueSet["MODELROOT"] in XGEE.
   * @throws {Error} - If the supplied eObject is unknown to ecoreSync.
   */
  async getModelRoot(eObject) {
    //gets the  EOQ resource containing the supplied eObject
    let oid = this._esDomain.rlookup(eObject);
    if (oid == null) {
      console.log("Unknown eObject:");
      console.error(eObject);
      debugger;
      throw new Error("The supplied eObject is unknown to ecoreSync");
    }
    let cmd = CMD.Get(
      QRY.Obj(oid)
        .Met("ALLPARENTS")
        .Sel(new eoq2.Qry().Met("CLASSNAME").Equ("ModelResource"))
        .Trm(new eoq2.Met("SIZE").Equ(0), null)
        .Idx(0)
        .Pth("contents")
        .Trm(new eoq2.Met("SIZE").Equ(0), null)
        .Idx(0),
    );
    let mdlRoot = await this._esDomain.remoteExec(cmd, true);
    return mdlRoot;
  }

  /**
   * Retrieves the eContainer of the supplied eObject.
   * @param {EObject} eObject - The eObject for which to retrieve the eContainer.
   * @returns {Promise<EObject>} A Promise that resolves with the eContainer eObject of the supplied eObject.
   * @throws {Error} - If the supplied eObject is unknown to ecoreSync.
   */
  async getContainer(eObject) {
    var res = null;
    if (eObject.eContainer) {
      res = eObject.eContainer;
    } else {
      let oid = this._esDomain.rlookup(eObject);
      if (!oid) throw new Error("The supplied eObject is unknown to ecoreSync");
      let cmd = CMD.Get(QRY.Obj(oid).Met("PARENT"));
      res = await this._esDomain.remoteExec(cmd, true);
    }
    return res;
  }

  /**
   * Retrieves the short path of the supplied eObject.
   * @param {EObject} eObject - The eObject for which to retrieve the short path.
   * @returns {Promise<string>} - A promise that resolves to the short path of the eObject. E.g.  "./Example.oaam/#2274". Used in the tab in XGEE.
   * @throws {Error} If the supplied eObject is unknown to ecoreSync.
   */
  async getObjectShortPath(eObject) {
    //TODO: Update with new EOQ commands?
    var res = "";
    let oid = this._esDomain.rlookup(eObject);
    if (!oid) throw new Error("The supplied eObject is unknown to ecoreSync");

    let cmd = new eoq2.Cmp()
      .Get(new eoq2.Qry().Obj(oid).Met("ALLPARENTS"))
      .Get(new eoq2.Qry().His(-1).Try(new eoq2.Qry().Pth('name')));  // Try makes it tolerant to no name feature

    let val = await this._esDomain.eoq2domain.Do(cmd);
    let pathSegments = [];
    for (let j = 0; j < val[0].length; j++) {
      let segmentName = val[1][j];
      let segmentId = val[0][j].v;
      pathSegments.push(segmentName ? segmentName : "#" + segmentId);
    }
    res = pathSegments.join("/");

    return res;
  }

  /**
   * Retrieves the string path of the given eObject.
   * @param {EObject} eObject - The eObject for which to retrieve the string path.
   * @returns {Promise<string>} The string path of the eObject. E.g. "resources.2/contents.0/tasks.5". This is used as the "EOQ Path" in XGEE Properties View. Very similar to EOQ2 QRF command.
   * @throws {Error} If the supplied eObject is unknown to ecoreSync.
   */
  async getObjectStringPath(eObject) {
    //TODO: Update with new EOQ commands?
    var res = "";
    let oid = this._esDomain.rlookup(eObject);
    if (!oid) throw new Error("the supplied eObject is unknown to ecoreSync");

    if (oid != 0) {
      //return the path to the object
      let cmd = CMD.Cmp()
        .Get(QRY.Obj(oid).Met("INDEX"))
        .Get(QRY.Obj(oid).Met("CONTAININGFEATURE"))
        .Get(QRY.His(-1).Pth("name"))
        .Get(QRY.His(-2).Pth("upperBound"))
        .Get(QRY.Obj(oid).Met("ALLPARENTS").Idx([1, -1, 1]))
        .Get(QRY.His(-1).Met("INDEX"))
        .Get(QRY.His(-2).Met("CONTAININGFEATURE"))
        .Get(QRY.His(-1).Pth("name"))
        .Get(QRY.His(-2).Pth("upperBound"));

      let val = await this._esDomain.eoq2domain.Do(cmd);
      var pathSegments = [];
      //do the container segments first
      var n = val[4].length;
      for (var i = 0; i < n; i++) {
        var index = val[5][i];
        var featureName = val[7][i];
        var upperBound = val[8][i];
        var segmentStr = featureName;
        if (upperBound != 1) {
          segmentStr += "." + index;
        }
        pathSegments.push(segmentStr);
      }
      //the last segment need special care
      {
        var index = val[0];
        var featureName = val[2];
        var upperBound = val[3];
        var segmentStr = featureName;
        if (upperBound != 1) {
          segmentStr += "." + index;
        }
        pathSegments.push(segmentStr);
      }
      res = pathSegments.join("/");
    }

    return res;
  }

  async getAllContents(eObject, filter = null) {
    var self = this;
    var results = [];
    let oid = this._esDomain.rlookup(eObject);
    if (!oid)
      throw new Error(
        "Cannot get contents: the supplied eObject is unknown to this ecoreSync instance",
      );
    if (filter != null) {
      if (filter(eObject)) {
        results.push(eObject);
      }
    }
    await this.isEClassInitialized(eObject.eClass);
    var containments = eObject.eClass.get("eAllContainments");
    let cmd = new eoq2.Cmp();

    containments.forEach(function (cnt) {
      cmd.Get(new eoq2.Obj(oid).Pth(cnt.get("name")));
    });

    var res = await this._esDomain.exec(cmd);
    res.forEach(function (cnts) {
      if (Array.isArray(cnts)) {
        results = results.concat(cnts);
      } else {
        if (cnts) {
          results.push(cnts);
        }
      }
    });

    var subContents = [];
    results.forEach(function (obj) {
      if (obj) {
        subContents.push(self.getAllContents(obj));
      }
    });
    subContents = await Promise.all(subContents);
    subContents.forEach(function (sc) {
      results = results.concat(sc);
    });

    if (filter == null) {
      return results;
    } else {
      return results.filter(filter);
    }
  }

  getObserverState(observerToken) {
    var res = [];
    if (this._esDomain.qryObservers.has(observerToken)) {
      var observer = this._esDomain.qryObservers.get(observerToken);
      var state = observer.observerState;
      return {
        results: state.getResults(),
        deltaPlus: state.getDeltaPlus(),
        deltaMinus: state.getDeltaMinus(),
      };
    }
    return res;
  }

  /**
   * Decodes the given object or array of objects.
   * If the input is an array, it decodes each element recursively.
   * If the input is an object with `qry` property equal to "OBJ", it retrieves the object using the `_esDomain` property.
   * Otherwise, it returns the input object as is.
   * @param {Object|Array} obj - The object or array of objects to decode. Typical is the result of a EOQ query like this: '{"qry":"OBJ","v":12}'
   * @returns {Promise<EObject|Array>} - The decoded eObject or array of eObjects.
   * @throws {Error} - If decoding fails or if the input format is invalid.
   */
  async decode(obj) {
    var self = this;
    var res = null;
    if (Array.isArray(obj)) {
      try {
        res = await awaitAll(
          obj.map(function (e) {
            return self.decode(e);
          }),
        );
      } catch (e) {
        throw new Error("ecoreSync: Failed while decoding array " + e);
      }
    } else {
      if (obj != null) {
        if (obj.qry == "OBJ") {
          try {
            if (!Number.isInteger(obj.v))
              throw new Error(
                "ecoreSync: Invalid input format during decode: object id is invalid",
              );
            res = await this._esDomain.getObject(obj.v);
          } catch (e) {
            throw new Error("ecoreSync: Failed to get object during decoding " + e);
          }
        } else {
          res = obj;
        }
      }
    }
    return res;
  }

  /**
   * Encodes the given object into a format suitable for transmission or storage.
   * If the object is an array, it recursively encodes each element.
   * If the object is an EObject, it looks up its ID in the ecoreSync instance and encodes it as an object query.
   * Otherwise, it returns the object as is.
   * @param {any} obj - The object to encode, typically EObject or array of EObjects.
   * @returns {any} - The encoded object. E. g. '{"qry":"OBJ","v":12}'.
   * @throws {Error} - If encoding fails or if the input format is invalid.
   */
  encode(obj) {
    var self = this;
    if (Array.isArray(obj)) {
      return obj.map(function (e) {
        return self.encode(e);
      });
    }
    var res = null;
    if (obj != null) {
      switch (obj.constructor.name) {
        case "EObject":
          let oid = this._esDomain.rlookup(obj);
          if (oid == null)
            throw new Error(
              "cannot encode: the supplied eObject of type " +
                obj.eClass.get("name") +
                " is unknown to this ecoreSync instance",
            );
          res = { qry: "OBJ", v: oid };
          break;
        default:
          res = obj;
          break;
      }
    }
    return res;
  }

  async awaitAll(obj) {
    // aux function to await all promises in an array structure
    var res = obj;
    if (Array.isArray(obj)) {
      res = [];
      for (let i in obj) {
        res.push(awaitAll(obj[i]));
      }
      res = await Promise.all(res);
    } else {
      res = await obj;
    }
    return res;
  }
}

/**
 * EsDomain inherits from EsUtils which provides various ecoreSync utility functions.
 * EsUtils class has the one attribute 'utils' which is an instance of EsUtilities.
 * This allows providing all the utility functions by myDomain.utils.functionName().
 */
export default class EsUtils {
  /**
   * Initializes the EsUtils class. Happens centrally only once since esDomain inherits from this class. Non-standard.
   */
  initializer() {
    this.utils = new EsUtilities(this);
  }
}
