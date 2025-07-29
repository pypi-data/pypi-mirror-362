/**
 * GraphObjectManager is an abstract class that manages the loading and observing of graph objects.
 * All managers, e.g. VertexManager extend this class to implement specific loading and observing logic.
 * Only the root GraphModelManager does not extend this class.
 */
export default class GraphObjectManager {
  constructor(graphModelFactory, ecoreSync, type, model, resourceProvider) {
    this.graphModelFactory = graphModelFactory;
    this.ecoreSync = ecoreSync;
    this.type = type;
    this.model = model;
    this.resourceProvider = resourceProvider;
    this.subManagers = [];
    this.observers = new Map();
  }

  async load(valueSet) {
    try {
      var vSet = Object.assign({}, valueSet);
      var query = this.type.query.build(vSet);
      var cmd = new eoq2.Get(query);
      var results = await this.ecoreSync.exec(cmd, false); // no result checking here, because it is done in the _postProcessResults method (at least for vertices)
      var res = await this._postProcessResults(results);
    } catch (error) {
      error.message = this.constructor.name + " failed to load: " + error.message;
      throw error;
    }
    return res;
  }

  async observe(valueSet, callback) {
    var vSet = Object.assign({}, valueSet);
    var self = this;
    var query = this.type.query.build(vSet);
    var observerToken = await this.ecoreSync.observe(
      query,
      async function (results, deltaPlus, deltaMinus) {
        self._interceptObserverCallback(
          valueSet,
          callback,
          await self._postProcessResults(results),
          await self._postProcessResults(deltaPlus),
          await self._postProcessResults(deltaMinus),
        );
      },
    );
  }

  mapObserver(graphObject, observerToken) {
    let observerArr = [];
    if (!this.observers.has(graphObject.uuid)) {
      this.observers.set(graphObject.uuid, observerArr);
    } else {
      observerArr = this.observers.get(graphObject.uuid);
    }

    observerArr.push(observerToken);
  }

  async unobserve(graphObject) {
    console.warn("Observer list");
    console.warn(this.observers);
  }

  async _postProcessResults(results) {
    return results;
  }

  async _interceptObserverCallback(valueSet, callback, results, deltaPlus, deltaMinus) {
    callback(results, deltaPlus, deltaMinus);
  }

  getTypeName() {
    return this.type.model.eClass.get("name");
  }

  /**
   * Managers themselves know how to add themselves to the model.
   * Will differentiate addEdge, addVertex
   * @param {GraphModel|GraphObject} parentObject - The parent object, e.g. GraphModel, Vertex to which the cell will be added. -> Functions, Task
   * @param {GraphObject} cell - The cell, e.g. Vertex, Edge to be added to the graph model.
   */
  addCell(parentObject, cell) {
    console.warn("Abstract, needs to be implemented in subclass.");
  }

  /**
   * Loop for addCell, submanagers add all cells at once.
   * @param {GraphModel|GraphObject} parentObject - The parent object, e.g. GraphModel, Vertex to which the cell will be added. -> Functions, Task
   * @param {Array<GraphObject>} cells - The cells, e.g. Vertices, Edges to be added to the graph model.
   */
  addCells(graphModel, cells) {
    cells.forEach(cell => this.addCell(graphModel, cell));
  }
}
