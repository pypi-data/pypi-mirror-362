import GraphObject from "./GraphObject.js";
import SizableObject from "./SizableObject.js";
import LocatableObject from "./LocatableObject.js";
import TypedObject from "./TypedObject.js";
import { multipleClasses } from "../../lib/libaux.js";

export default class Label extends multipleClasses(
  GraphObject,
  SizableObject,
  LocatableObject,
  TypedObject,
) {
  constructor() {
    super();
    this.content = "";
    this.color = "000000";
    this.rotation = 0.0;
    this.align = "CENTER";
    this.vAlign = "CENTER";
    this.anchor = "CENTER";
    this.segments = [];
  }

  /**
   * Initializes the label with the values read from the editorModel.
   * Because of mxGraphIntegration.js, we cannot handel rotation, offset as "normal", but store it
   * in the label and use it in the mxGraphIntegration.js.
   * Similar to Vertex.init()
   */
  init() {
    const offsetX = Number.parseInt(this.type.model.get("labelOffsetX"));
    const offsetY = Number.parseInt(this.type.model.get("labelOffsetY"));
    this.offset = {
      x: Number.isNaN(offsetX) ? 0 : offsetX,
      y: Number.isNaN(offsetY) ? 0 : offsetY,
    };

    this.anchor = this.type.model.get("anchor"); // default CENTER is in editorModel
    this.rotation = Number.parseFloat(this.type.model.get("labelRotation")); // default 0.0 is in editorModel

    this.content = "";
  }

  addSegment(labelSegment) {
    labelSegment.setParent(this);
    this.segments.push(labelSegment);
  }

  getContentPrototype() {
    if (this.type) {
      return this.type.model.get("content");
    }
    return "error: no label type set";
  }

  setContent(content, noParentRefresh = false) {
    this.content = content;
    if (this.parent && !noParentRefresh) {
      this.parent.graphModel.invalidate(this);
    }
  }

  refreshContent(noParentRefresh = false) {
    var content = "";
    this.segments.forEach(function (segment) {
      content += segment.getContent();
    });
    this.setContent(content, noParentRefresh);
  }

  isMovable() {
    return false;
  }

  isResizable() {
    return false;
  }

  toString() {
    return this.content;
  }
}
