import GraphObjectManager from "./GraphObjectManager.js";
import VertexManager from "./VertexManager.js";

export default class ContainerManager extends GraphObjectManager {
  constructor(...args) {
    super(...args);
  }

  /**
   * Very different to VertexManager.load(), a mix of VertexManager.load() and GraphModelManager.load()
   * A VertexManager manages multiple vertices, however a ContainerManager manages a single container of an Edge.
   * createVertex() is called in super.load() (GraphObjectManager), here the Container is directly created
   * Container has no direct EObject -> we link it to the parent EObject, the Edge
   * ValueSet of parent Edge is directly passed to subManagers without modification
   * Container has no Query, it behaves like an unconditional StaticVertex -- it is always there
   * No transaction start/end
   */
  async load(valueSet) {
    if (!valueSet?.PARENT) return []; // case no Edge/PARENT, unclear when this happens

    // get or create the single cell for the container, similar to VertexManager super.load()
    let managerCell =
      this.model.getContainerByEObject(valueSet["PARENT"]) ||
      this.graphModelFactory.createContainer(this.model, this.type, valueSet["PARENT"]);

    // similar to GraphModelManager.load(), it is also only one very big cell
    const subManagersCells = await Promise.all(
      this.subManagers.map((subManager) => subManager.load(valueSet)),
    );
    this.subManagers.forEach((subManager, subManagerIdx) => {
      const subManagerCells = subManagersCells[subManagerIdx];
      subManager.addCells(managerCell, subManagerCells);
    });

    // list keeps it compatible
    return [managerCell];
  }

  async observe(valueSet, callback) {
    var self = this;
    var container = null;
    if (valueSet["PARENT"]) {
      container = this.model.getContainerByEObject(valueSet["PARENT"]);
    }
    if (container) {
      self.subManagers
        .filter(function (manager) {
          return manager instanceof VertexManager;
        })
        .forEach(function (manager) {
          manager.observe(
            valueSet,
            function () {
              console.error("container resident changed!!!");
            },
            container,
          );
        });
    } else {
      $.notify("CONTAINER ERROR");
    }
  }

  addCell(parentObject, container) {
    parentObject.addContainer(container);
  }
}
