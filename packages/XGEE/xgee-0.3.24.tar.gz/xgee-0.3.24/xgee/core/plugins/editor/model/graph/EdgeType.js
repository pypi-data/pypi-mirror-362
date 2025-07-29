import GraphObjectType from "./GraphObjectType.js";
import ReferringObjectType from "./ReferringObjectType.js";
import { multipleClasses } from "../../lib/libaux.js";

export default class EdgeType extends multipleClasses(GraphObjectType, ReferringObjectType) {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
  }
}
