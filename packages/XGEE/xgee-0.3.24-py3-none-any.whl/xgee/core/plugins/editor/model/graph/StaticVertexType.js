import Query from "../../queries/Query.js";
import ShapedObjectType from "./ShapedObjectType.js";

export default class StaticVertexType extends ShapedObjectType {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
    this.shape = null;
    this.isConditional = this.model.get("isConditional") ? true : false;
    this.condition = new Query(this.ecoreSync, null, this.model.get("condition"), "PARENT", null);
  }
}
