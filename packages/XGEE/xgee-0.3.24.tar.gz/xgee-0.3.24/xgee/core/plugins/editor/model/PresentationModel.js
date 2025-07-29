/**
 * XGEE editorModel (Presentation Model) class, e.g. OAAM Functions Editor
 */
export default class XGEEPresentationModel {
  /**
   * Create a new instance of the editorModel
   * @param {string} pathToModel - e.g. "plugins/editor.oaam.functions/"
   * @param {EObject} presentationModel -  the editorModel, e.g. OAAM Functions Editor
   */
  constructor(pathToModel, presentationModel) {
    this.pathToModel = pathToModel;
    this.presentationModel = presentationModel;
  }

  /**
   * Get the path to the model
   * @returns {string}
   */
  getPath() {
    return this.pathToModel;
  }

  /**
   * Get the presentation model / editorModel
   * @returns {EObject}
   */
  getModel() {
    return this.presentationModel;
  }
}
