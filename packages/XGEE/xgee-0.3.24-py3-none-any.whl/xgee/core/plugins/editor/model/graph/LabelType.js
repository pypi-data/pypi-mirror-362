import GraphObjectType from "./GraphObjectType.js";

export default class LabelType extends GraphObjectType {
  constructor(ecoreSync, model) {
    super(ecoreSync, model);
  }

  getStyle() {
    let align = "center";
    switch (this.model.get("labelAlignment")) {
      case "CENTER":
        align = "center";
        break;
      case "LEFT":
        align = "left";
        break;
      case "RIGHT":
        align = "right";
        break;
    }

    let vAlign = "middle";
    switch (this.model.get("labelVerticalAlignment")) {
      case "CENTER":
        vAlign = "middle";
        break;
      case "TOP":
        vAlign = "top";
        break;
      case "BOTTOM":
        vAlign = "bottom";
        break;
    }

    return (
      "shape=rectangle" +
      ";align=" +
      align +
      ";verticalAlign=" +
      vAlign +
      ";autosize=1;resizable=0;pointerEvents:0;editable=0"
    );
  }
}
