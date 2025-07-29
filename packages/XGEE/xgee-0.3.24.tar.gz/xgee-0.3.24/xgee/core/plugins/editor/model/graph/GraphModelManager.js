import EdgeManager from "./EdgeManager.js";
import VertexManager from "./VertexManager.js";
import StaticVertexManager from "./StaticVertexManager.js";

/**
 * Manages the GraphModel: keeps it in sync with the user model
 * Manages all the submanagers.
 */
export default class GraphModelManager {
  constructor(graphModelFactory, ecoreSync, model, resourceProvider) {
    this.graphModelFactory = graphModelFactory;
    this.ecoreSync = ecoreSync;
    this.model = model;
    this.subManagers = [];
    this.resourceProvider = resourceProvider;
  }

  /**
   * Loads editor: recursively loads submanagers, adds their cells to the graphModel and applies layout.
   * E.g. for Functions: /tasks, /signals, /externalTaskLinks
   * @param valueSet
   * @returns {Promise<boolean>}
   */
  async load(valueSet) {
    var self = this; // used by layout stuff, we might want to switch to nice arrow functions later
    let tabName = `${this.model.eObject.eClass.get("name")} Editor ([#${this.ecoreSync.rlookup(this.model.eObject)}])`
    console.info(`Loading model ${tabName}...`);
    this.model.vertices = [];
    this.model.edges = [];

    // simpler than vertexManager, since there is only one Functions, not many Tasks to loop
    const subManagersCells = await Promise.all(
      this.subManagers.map((subManager) => subManager.load(valueSet)),
    );
    console.info(`${tabName} submanagers completed loading`)

    // add Vertices of VertexManager, StaticVertexManager, Edges of EdgeManager
    this.subManagers.forEach((subManager, subManagerIdx) => {
      const subManagerCells = subManagersCells[subManagerIdx]; // e.g. all Tasks, all Signals, all top-level DisplayableObjects
      subManager.addCells(this.model, subManagerCells);
    });

    //Layout data
    var toplevelGraphObjects = [];

    var initEdgeSupportPoints = async function (e) {
      let results = [];
      let rawSupportPoints = await self.model.layout.getEdgeSupportPoints(e);

      rawSupportPoints.sort((a, b) => {
        if (a.get("pointIndex") < b.get("pointIndex")) {
          return -1;
        }
        if (a.get("pointIndex") > b.get("pointIndex")) {
          return 1;
        }
        return 0;
      });
      for (let rawSupportPoint of rawSupportPoints) {
        results.push({
          x: rawSupportPoint.get("x"),
          y: rawSupportPoint.get("y"),
        });
      }
      return results;
    };
    var initEdge = async function (e) {
      let supportPoints = await initEdgeSupportPoints(e);
      e.supportPoints = supportPoints;
    };
    var initVertexPosition = async function (v) {
      var position = self.model.layout.getVertexPosition(v);
      if (position) return position;
      return { x: 0, y: 0 };
    };
    var initVertexSize = async function (v) {
      var size = self.model.layout.getVertexSize(v);
      if (size) return size;
      return { x: 0, y: 0 };
    };
    var initVertex = async function (v) {
      v.position = await initVertexPosition(v);
      let size = await initVertexSize(v);
      if (size.x > 0 && size.y > 0) {
        v.size = size;
      }
      var vertices = [];
      v.vertices.forEach(function (sv) {
        vertices.push(initVertex(sv));
      });
      return await Promise.all(vertices);
    };

    for (let vertex of this.model.vertices) {
      toplevelGraphObjects.push(initVertex(vertex));
    }
    for (let edge of this.model.edges) {
      toplevelGraphObjects.push(initEdge(edge));
    }
    await Promise.all(toplevelGraphObjects);

    console.info("Cells added to graphModel, layout loaded where available");
    return true;
  }

  async initObservers(valueSet) {
    var self = this;
    this.subManagers
      .filter(function (v) {
        return v.getTypeName() == "Vertex" || v.getTypeName() == "Edge";
      })
      .forEach(function (manager) {
        manager.observe(
          valueSet,
          function () {
            console.warn("unhandled observer interception");
          },
          self.model,
        );
      });
  }
}
