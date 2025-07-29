import GraphObjectType from "./GraphObjectType.js";
import ReferringObjectType from "./ReferringObjectType.js";
import { multipleClasses } from "../../lib/libaux.js";

export default class AnchorType extends multipleClasses(GraphObjectType, ReferringObjectType)  {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
  }

  getType() {
    return this.model.get("type");
  }
}
