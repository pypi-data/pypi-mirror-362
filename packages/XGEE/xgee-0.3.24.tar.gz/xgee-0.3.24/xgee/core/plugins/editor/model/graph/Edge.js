import GraphObject from "./GraphObject.js";
import TypedObject from "./TypedObject.js";
import ContainerProvider from "./ContainerProvider.js";
import EObjectOwner from "./EObjectOwner.js";
import RoutableObject from "./RoutableObject.js";
import DeletableObject from "./DeletableObject.js";
import EventProvider from "./EventProvider.js";
import { multipleClasses } from "../../lib/libaux.js";

export default class Edge extends multipleClasses(
  GraphObject,
  TypedObject,
  RoutableObject,
  DeletableObject,
  ContainerProvider,
  EObjectOwner,
) {
  constructor(graphModel, type, parent = null) {
    super();
    this.graphModel = graphModel;
    this.anchors = [];
  }

  init() {
    //Update support points
    var self = this;
    this.on("ROUTED", function (supportPoints) {
      self.graphModel.layout.updateEdge(self, supportPoints);
    });
  }

  addAnchor(anchor) {
    anchor.parent = this;
    this.anchors.push(anchor);
    if (this.parent) {
      this.graphModel.events["EDGE_ANCHORS_CHANGED"].raise(this);
    }
  }

  removeAnchor(anchor) {
    let idx = this.anchors.indexOf(anchor);
    if (idx > -1) {
      this.anchors.splice(idx, 1);
    }
    if (this.parent) {
      this.graphModel.events["EDGE_ANCHORS_CHANGED"].raise(this);
    }
  }

  getAnchorByEObject(eObject) {
    return this.anchors.find(function (anchor) {
      return anchor.getEObject() == eObject;
    });
  }

  getAnchorByEObjectId(objectId) {
    return this.anchors.find(function (anchor) {
      return anchor.getEObjectId() == objectId;
    });
  }

  /**
   * Returns all anchors of this edge that are of type SOURCE or BOTH -> start of the edge
   */
  getSourceAnchors() {
    return this.anchors.filter(anchor => {
      const type = anchor.getType();
      return type === "SOURCE" || type === "BOTH";
    });
  }

  /**
   * See getSourceAnchors()
   */
  getTargetAnchors() {
    return this.anchors.filter(anchor => {
      const type = anchor.getType();
      return type === "TARGET" || type === "BOTH";
    });
  }

  /**
   * Returns all edge spans for this edge. Searches in all source/both and target/both anchors
   * for valid edge spans, depending on the edge type.
   */
  getEdgeSpans() {
    let edgeSpans = [];

    let sources = this.getSourceAnchors();
    let targets = this.getTargetAnchors();
    let edgeType = this.type.model.get("type") ? this.type.model.get("type") : "ONE2ONE";

    let edgeSpan;
    switch (edgeType) {
      case "ONE2MANY":
        let source = sources.length ? sources[0] : null;
        if (source) {
          for (let target of targets) {
            if (target) {
              edgeSpan = {};
              edgeSpan.source = source;
              edgeSpan.target = target;
              edgeSpans.push(edgeSpan);
            }
          }
        }
        break;
      case "MANY2ONE":
        edgeSpan = {};
        let target = targets.length ? targets[0] : null;
        if (target) {
          for (let source of sources) {
            if (source) {
              edgeSpan = {};
              edgeSpan.source = source;
              edgeSpan.target = target;
              edgeSpans.push(edgeSpan);
            }
          }
        }
        break;
      case "MANY2MANY":
        for (let source of sources) {
          if (source) {
            for (let target of targets) {
              if (target) {
                edgeSpan = {};
                edgeSpan.source = source;
                edgeSpan.target = target;
                edgeSpans.push(edgeSpan);
              }
            }
          }
        }
        break;
      case "UNILATERAL":
        console.debug("Processing UNILATERAL edge type, using default ONE2ONE behavior");
        // fall through to default
      case "BILATERAL":
        console.debug("Processing BILATERAL edge type, using default ONE2ONE behavior");
        // fall through to default
      case "ONE2ONE": // ONE2ONE is the default case, catches 'UNILATERAL' and 'BILATERAL'
      default:
        edgeSpan = {};
        // multiple sources/targets: try to avoid self-loops
        if (sources.length > 1 || targets.length > 1) {
          for (const source of sources) {
            for (const target of targets) {
              if (source.getEObject() !== target.getEObject()) {
                edgeSpan.source = source;
                edgeSpan.target = target;
                break;
              }
            }
            if (edgeSpan.source) break;
          }
        }

        if (!edgeSpan.source) {
          edgeSpan.source = sources.length ? sources[0] : null;
        }
        if (!edgeSpan.target) {
          edgeSpan.target = targets.length ? targets[0] : null;
        }

        if (edgeSpan.source && edgeSpan.target) {
          edgeSpans.push(edgeSpan);
        }
        break;
    }

    return edgeSpans;
  }

  getStyle(source, target) {
    var self = this;
    var style = "";

    var setEdgeStrokeWidth = function (style) {
      style += "strokeWidth=" + self.type.model.get("strokeWidth") + ";";
      return style;
    };

    var setEdgeColor = function (style) {
      if (self.type.model.get("autoColor")) {
        let color = "FF0000"; //removed # because these are no longer supported in strings by EOQ
        let colorProvider = getColorProvider(self.type.model.get("colorNamespace"));
        if (!colorProvider) {
          colorProvider = new ColorProvider(self.type.model.get("colorNamespace"), (a, b) => {
            return a == b;
          });
        }
        color = colorProvider.getColor(self.eObject);
        if (!color) {
          color = "FF000";
        } //fallback
        style += "strokeColor=#" + color + ";"; //added #
      } else {
        let color = self.type.model.get("color");
        if (!color) {
          color = "FF000";
        } //fallback color (red)
        style += "strokeColor=#" + color + ";"; //added #
      }
      return style;
    };

    var setEdgeAnchorAttachment = function (style, anchor) {
      var keyword;
      if (anchor.getType() == "SOURCE") {
        keyword = "exit";
      }

      if (anchor.getType() == "TARGET") {
        keyword = "entry";
      }

      if (keyword) {
        var attach = anchor.type.model.get("attach");
        var offsetType = anchor.type.model.get("offsetType")
          ? anchor.type.model.get("offsetType")
          : 0;
        var offsetX = Number.parseFloat(
          anchor.type.model.get("offsetX") ? anchor.type.model.get("offsetX") : 0,
        );
        var offsetY = Number.parseFloat(
          anchor.type.model.get("offsetY") ? anchor.type.model.get("offsetY") : 0,
        );

        //Attachment position defaults
        let attachX = 0;
        let attachY = 0;

        switch (attach) {
          case "NORTH":
            attachX = 0.5;
            attachY = 0;
            break;
          case "SOUTH":
            attachX = 0.5;
            attachY = 1;
            break;
          case "EAST":
            attachX = 1;
            attachY = 0.5;
            break;
          case "WEST":
            attachX = 0.0;
            attachY = 0.5;
            break;
          case "ANY":
            attachX = 0;
            attachY = 0;
            break;
          default:
            attachX = 0.5;
            attachY = 1;
            break;
        }

        style +=
          keyword +
          "X=" +
          attachX.toString() +
          ";" +
          keyword +
          "Y=" +
          attachY.toString() +
          ";" +
          keyword +
          "Dx=" +
          offsetX.toString() +
          ";" +
          keyword +
          "Dy=" +
          offsetY.toString() +
          ";";
        if (offsetX != 0 || offsetY != 0) style += keyword + "Perimeter=0;";

        if (attach == "NORTH" || attach == "SOUTH") {
          style += "edgeStyle=elbowEdgeStyle;elbow=vertical;";
        }

        if (attach == "EAST" || attach == "WEST") {
          style += "edgeStyle=elbowEdgeStyle;elbow=horizontal;";
        }
      }
      return style;
    };

    var setCurved = function (style) {
      if (self.type.model.get("curved")) {
        style += "curved=1;";
      } else {
        style += "curved=0;";
      }
      return style;
    };

    style = setEdgeStrokeWidth(style);
    style = setEdgeColor(style);
    style = setEdgeAnchorAttachment(style, source);
    style = setEdgeAnchorAttachment(style, target);
    style = setCurved(style);

    return style;
  }

  addContainer(container) {
    super.addContainer(container);
    this.graphModel.addToIndex(container);
  }

  removeContainer(container) {
    super.removeContainer(container);
    this.graphModel.removeFromIndex(container);
  }

  delete(source, target) {
    let valueSet = {};
    valueSet["SOURCE"] = source.eObject;
    valueSet["TARGET"] = target.eObject;
    super.delete(valueSet);
  }

  toString() {
    return "";
  }
}
