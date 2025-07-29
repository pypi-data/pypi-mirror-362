import ShapedObjectType from "./ShapedObjectType.js";

export default class ContainerType extends ShapedObjectType {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
    this.shape = null;
  }
}
