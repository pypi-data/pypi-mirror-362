/**
 * ReferringObjectType.js
 * @module editor/model/graph/ReferringObjectType
 * Idea: centralize the query init of VertexType, EdgeType, and AnchorType
 * AnchorType is not (yet) inheriting ReferringObject in the editorModel metamodel yet, but it has
 * the exact same init with the same properties (however, in the editorModel, "alias" is missing)
 */

import Query from "../../queries/Query.js";

/**
 * reads query properties from editorModel during initialization (multipleClasses calls the initializer)
 */
export default class ReferringObjectType {
  initializer() {
    this.query = new Query(
      this.ecoreSync,
      this.model.get("alias"),
      this.model.get("queryStr"),
      this.model.get("queryTarget"),
      this.model.get("queryTargetAlias"),
    );
  }
}