/**
 * ShapedObjectType
 * @module editor/model/graph/ShapedObjectType
 * IDEA: currently, getStyle() is called for every individual vertex. It would be interesting to
 * collect all styles in the mxStyleSheet.
 */

import GraphObjectType from "./GraphObjectType.js";

/**
 * Serializes a style dictionary into the string format for mxGraph "style" attribute.
 * @param styleDict - dictionary with style properties
 * @returns {string}
 * @private
 */
function _serializeStyle(styleDict) {
  return Object.entries(styleDict).reduce((str, [key, val]) => str + `${key}=${val};`, "");
}

const STATIC_CONFIG_BY_SHAPE = {
  Rectangle: { shape: "rectangle" },
  IsoscelesTriangle: { shape: "triangle" },
  RoundedRectangle: { shape: "rectangle", rounded: 1, absoluteArcSize: 1 }
};

/**
 * Vertex, StaticVertex, and Container are "ShapedObject"
 * Their style is defined by a contained Shape
 */
export default class ShapedObjectType extends GraphObjectType {
  /**
   * Translate editorModel ShapedObject into mxGraph style string
   * addVertexToGraph() calls getStyle for every vertex
   * differentiates SVG (ShapeFromResource) and GeometricShape (Rectangle, RoundedRectangle, Triangle)
   * @returns {string} - The mxGraph style string, e.g. "shape=rectangle;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1;"
   */
  getStyle() {
    const shape = this.model?.get("shape");
    if (!shape) {
      let name = this.model?.get("name") || "<unnamed>";
      console.info(`No shape defined in editorModel for ${this.model.eClass.get("name")} ` +
       `with name "${name}", falling back to default rectangle style.`)
      return _serializeStyle({ shape: "rectangle" }); // Default style if no shape is defined, convenient during development of editorModels
    }
    const className = shape.eClass.get("name");

    // Case GeometricShape
    // shape geometry properties specified in editorModel
    if (shape?.isKindOf("GeometricShape")) {
      // isKind = INO instanceOf
      // 3 steps: static config, general dynamic properties, special cases
      if (!STATIC_CONFIG_BY_SHAPE[className]) {
        console.warn(`Unrecognized shape class: ${className}, defaulting to rectangle.`);
      }
      const staticConfig = STATIC_CONFIG_BY_SHAPE[className] || STATIC_CONFIG_BY_SHAPE.Rectangle; // Default to Rectangle if className not recognized

      const styleDict = {
        ...staticConfig,
        fillColor: shape.get("fillColor"),
        strokeColor: shape.get("strokeWidth") > 0 ? shape.get("strokeColor") : "none", // mxGraph uses 'none' for no stroke
        strokeWidth: shape.get("strokeWidth"), // mxGraph will reset 0 strokeWidth to 1 -> strokeColor = 'none'
        rotation: shape.get("rotation"), // automatically ignored if default 0
      };

      // currently only one special case, when the list grows, we might handle it better
      const radius = shape.get("radius"); // currently only used for RoundedRectangle
      if (radius) styleDict.arcSize = radius * 2; // mxGraph uses arcSize=diameter, not radius

      return _serializeStyle(styleDict);

      // Case SVG Vector Graphic = ShapeFromResource
    } else if (shape.isTypeOf("ShapeFromResource")) {
      const styleDict = {
        shape: "image",
        image: `data:image/svg+xml,${btoa(this.shape)}`,
        imageAspect: 0, // 0 = stretch, 1 = keep aspect ratio - we want 2d resize
        editable: 0, // has always been 0
        rotation: shape.get("rotation")
      };
      return _serializeStyle(styleDict);

      // Case Default
      // cannot be reached, but just in case
    } else {
      return _serializeStyle({ shape: "rectangle" });
    }
  }
}