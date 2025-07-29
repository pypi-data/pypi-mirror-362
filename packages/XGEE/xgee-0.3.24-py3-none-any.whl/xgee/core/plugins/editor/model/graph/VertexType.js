import ShapedObjectType from "./ShapedObjectType.js";
import ReferringObjectType from "./ReferringObjectType.js";
import { multipleClasses } from "../../lib/libaux.js";

export default class VertexType extends multipleClasses(ShapedObjectType, ReferringObjectType)  {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
    this.shape = null;
  }
}
