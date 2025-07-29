import GraphObjectManager from "./GraphObjectManager.js";
import VertexManager from "./VertexManager.js";
import LabelManager from "./LabelManager.js";

export default class StaticVertexManager extends GraphObjectManager {
  constructor(...args) {
    super(...args);
  }

  /**
   * Similar to ContainerManager.load()
   * Also static. However, it can be conditional and have a query.
   * @param valueSet
   * @returns {Promise<*[]>}
   */
  async load(valueSet) {
    if (!valueSet?.PARENT) return [];

    // Try to reuse existing cell
    let [managerCell] = this.model.getByEObject(valueSet["PARENT"], this.type); // first element of array or undefined

    // Conditional StaticVertex: return empty if condition is not met
    if (this.type.isConditional) {
      const conditionOk = await this.ecoreSync.exec(
        new eoq2.Get(this.type.condition.build(valueSet)),
      );
      if (!conditionOk) return [];
    }

    // At this point: PARENT exists, unconditional or condition is met
    if (!managerCell) {
      managerCell = this.graphModelFactory.createStaticVertex(
        this.model,
        this.type,
        valueSet["PARENT"],
      );
    }

    const subManagersCells = await Promise.all(
      this.subManagers.map((subManager) => subManager.load({ ...valueSet })),
    );
    this.subManagers.forEach((subManager, subManagerIdx) => {
      const subManagerCells = subManagersCells[subManagerIdx];
      subManager.addCells(managerCell, subManagerCells);
    });

    return [managerCell];
  }

  async observe(valueSet, callback, container) {
    var self = this;
    var staticVertex = null;
    if (valueSet["PARENT"]) {
      let staticVertices = this.model.getByEObject(valueSet["PARENT"], this.type);
      staticVertex = staticVertices.length ? staticVertices[0] : null;
    }

    if (staticVertex) {
      //Initialize observance for the already present static vertex

      //Initialize label observance
      this.subManagers
        .filter(function (manager) {
          return manager instanceof LabelManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, staticVertex);
        });

      //Initialize vertex manager observance
      this.subManagers
        .filter(function (manager) {
          return manager instanceof VertexManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, staticVertex);
        });

      //Initialize static vertex manager observance
      this.subManagers
        .filter(function (manager) {
          return manager instanceof StaticVertexManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, staticVertex);
        });
    }

    if (this.type.isConditional) {
      var vSet = Object.assign({}, valueSet);
      var conditionQry = this.type.condition.build(vSet);
      var observerToken = await this.ecoreSync.observe(conditionQry, async (condition) => {
        let results = [];

        if (condition) {
          if (!staticVertex) {
            staticVertex = self.graphModelFactory.createStaticVertex(
              this.model,
              this.type,
              valueSet["PARENT"],
            );

            let loadingSubManagers = [];
            self.subManagers.forEach(function (manager) {
              loadingSubManagers.push(manager.load(valueSet));
            });

            var vSetEvaluation = await Promise.all(loadingSubManagers);
            var transaction = await staticVertex.startTransaction();
            vSetEvaluation.forEach(function (managerResult, managerIdx) {
              for (let i in managerResult) {
                if (self.subManagers[managerIdx] instanceof VertexManager) {
                  staticVertex.addVertex(managerResult[i]);
                }

                if (self.subManagers[managerIdx] instanceof StaticVertexManager) {
                  staticVertex.addVertex(managerResult[i]);
                }

                if (self.subManagers[managerIdx] instanceof LabelManager) {
                  staticVertex.addLabel(managerResult[i]);
                }
              }
            });
            staticVertex.endTransaction(transaction);

            //Initialize observance for the static vertex created during this observer event

            //Initialize label observance
            self.subManagers
              .filter(function (manager) {
                return manager instanceof LabelManager;
              })
              .forEach(function (manager) {
                manager.observe(valueSet, function () {}, staticVertex);
              });

            //Initialize vertex manager observance
            self.subManagers
              .filter(function (manager) {
                return manager instanceof VertexManager;
              })
              .forEach(function (manager) {
                manager.observe(valueSet, function () {}, staticVertex);
              });

            //Initialize static vertex manager observance
            self.subManagers
              .filter(function (manager) {
                return manager instanceof StaticVertexManager;
              })
              .forEach(function (manager) {
                manager.observe(valueSet, function () {}, staticVertex);
              });
          }

          container.addVertex(staticVertex);
        } else {
          if (staticVertex) {
            container.removeVertex(staticVertex);
          }
        }
      });
    }
  }

  addCell(graphModel, vertex) {
    graphModel.addVertex(vertex);
  }
}
