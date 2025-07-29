import GraphObjectManager from "./GraphObjectManager.js";
import StaticVertexManager from "./StaticVertexManager.js";
import EdgeManager from "./EdgeManager.js";
import LabelManager from "./LabelManager.js";

export default class VertexManager extends GraphObjectManager {
  constructor(...args) {
    super(...args);
  }

  /**
   * Recursively loads the vertices e.g. all Tasks, then Inputs, ...
   * Called by and similar to GraphModelManager.load(), however we have only one Functions, but many Tasks -> more loops
   * Creates a new valueSet for the submanagers (mainly with new PARENT, the current vertex)
   * Then loads them and adds their cells to the current vertex
   * extends the load() of GraphObjectManager with the submanagers
   *
   * Recursion: Functions 1/tasks -> Task 1/inputs, Input 1/name
   *
   * dictionary old, new
   * results: managerCells: the cells that this manager creates
   * valueSets: the individual valueSet for the submanagers of every Vertex (Task) valueSetsForSubmanagers
   * pendingVSets: allSubManagersCells
   *
   * @param valueSet
   * @returns {Promise<*>}
   */
  async load(valueSet) {
    // managerCells: the cells that this manager creates as result of the load function e.g. [Task 1, Task 2]
    const managerCells = await super.load(valueSet); // no result checking here, because it is done in the super.load method, which calls the _postProcessResults method (at least for vertices)
    // the valueSets for my submanagers, every Vertex (Task) has its own valueSet, since PARENT is set to the Task
    const valueSetsForSubmanagers = await this.type.query.makeValueSets(
      valueSet,
      managerCells.map((cell) => cell.getEObject()),
    );

    // for every valueSetsForSubmanagers (Task), we run all submanagers' load functions
    // this gives us all the cells of every submanager for every Task
    const allSubManagersCells = await Promise.all(
      valueSetsForSubmanagers.map((valueSet) =>
        Promise.all(this.subManagers.map((subManager) => subManager.load(valueSet))),
      ),
    );

    // allSubManagersCells: e.g. [ [ [Input 1, Input 2], [Output 1], [Label 1]],  [[],[], [Label 2]] ]
    // all Task, nested all Inputs, Outputs and Labels
    for (const [managerCellIdx, managerCell] of managerCells.entries()) {
      // loop every Task, e.g. Task 1
      const subManagersCells = allSubManagersCells[managerCellIdx]; // aligns managerCell and its subManagersCells
      const transaction = await managerCell.startTransaction();

      this.subManagers.forEach((subManager, subManagerIdx) => {
        const subManagerCells = subManagersCells[subManagerIdx]; // every subManager, e.g. [Input 1, Input 2]
        subManager.addCells(managerCell, subManagerCells);
      });

      managerCell.endTransaction(transaction);
    }

    return managerCells;
  }

  async observe(valueSet, callback, container) {
    var self = this;
    if (!container) throw new Error(" no container supplied ");

    var ObserverCallback = async function (results, addedVertices, removedVertices) {
      for (let i = 0; i < removedVertices.length; i++) {
        let vertex = removedVertices[i];

        if (vertex) {
          let vSet = await self.type.query.makeValueSets(valueSet, vertex.getEObject());
          self.unobserve(vertex);
          container.removeVertex(vertex);
        } else {
          console.error("removed vertex was not found in model");
        }
      }

      for (let i = 0; i < addedVertices.length; i++) {
        let vertex = addedVertices[i];
        var tempPos = self.model.layout.getTemporaryVertexPosition(
          vertex.getEObjectId(),
          ecoreSync.rlookup(valueSet["PARENT"]),
        );
        if (tempPos)
          vertex.position = {
            x: tempPos.x - vertex.size.x * 0.5,
            y: tempPos.y - vertex.size.y * 0.5,
          };
        if (tempPos) self.model.layout.setVertexPosition(vertex, tempPos.x, tempPos.y);

        container.addVertex(vertex);

        let vSet = await self.type.query.makeValueSets(valueSet, vertex.getEObject());

        //Initialize observance of sub managers
        self.subManagers.forEach(function (manager) {
          if (manager instanceof VertexManager) {
            manager.observe(vSet, function (results) {}, vertex);
          }

          if (manager instanceof StaticVertexManager) {
            manager.observe(vSet, function (results) {}, vertex);
          }

          if (manager instanceof EdgeManager) {
            manager.observe(vSet, function (results) {}, vertex);
          }

          if (manager instanceof LabelManager) {
            manager.observe(vSet, function (results) {}, vertex);
          }
        });
      }
    };

    //start observing all vertices & get the current query results
    var vSet = Object.assign({}, valueSet);
    var query = this.type.query.build(vSet);
    var observerToken = await this.ecoreSync.observe(
      query,
      async function (results, deltaPlus, deltaMinus) {
        // hot fix for issue: https://gitlab.com/xgee/xgee-core/-/issues/11
        results = Array.isArray(results) ? results : [results]; // hot fix
        deltaPlus = Array.isArray(deltaPlus) ? deltaPlus : [deltaPlus]; // hot fix
        deltaMinus = Array.isArray(deltaMinus) ? deltaMinus : [deltaMinus]; // hot fix
        // end hot fix

        //Force unique results
        results = [...new Set(results)];
        deltaPlus = [...new Set(deltaPlus)];
        deltaMinus = [...new Set(deltaMinus)];

        self._interceptObserverCallback(
          valueSet,
          function (results, deltaPlus, deltaMinus) {
            ObserverCallback(results, deltaPlus, deltaMinus);
          },
          await self._postProcessResults(results, container),
          await self._postProcessResults(deltaPlus, container),
          await self._postProcessResults(deltaMinus, container),
        );
      },
    );

    this.observers.set(container, observerToken);

    var transaction = await container.startTransaction();
    var results = await self._postProcessResults(
      this.ecoreSync.utils.getObserverState(observerToken).results,
      container,
    );
    container.endTransaction(transaction);

    //All subitems
    var valueSets = await this.type.query.makeValueSets(
      valueSet,
      results.map(function (e) {
        return e.getEObject();
      }),
    );
    valueSets.forEach(function (valueSet, i) {
      //Initialize label observance
      self.subManagers
        .filter(function (manager) {
          return manager instanceof LabelManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, results[i]);
        });

      //Initialize vertex manager observance
      self.subManagers
        .filter(function (manager) {
          return manager instanceof VertexManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, results[i]);
        });

      //Initialize static vertex manager observance
      self.subManagers
        .filter(function (manager) {
          return manager instanceof StaticVertexManager;
        })
        .forEach(function (manager) {
          manager.observe(valueSet, function () {}, results[i]);
        });

      //Initialize edge manager observance
      self.subManagers
        .filter(function (manager) {
          return manager instanceof EdgeManager;
        })
        .forEach(function (manager) {
          manager.observe(
            valueSet,
            function () {
              console.error("Edge ");
            },
            results[i],
          );
        });
    });
  }

  unobserve(vertex) {
    //unobserves this vertex and all nested graph objects
    var self = this;
    if (this.observers.has(vertex)) {
      ecoreSync.unobserve(this.observers.get(vertex));
      this.observers.delete(vertex);
    }

    this.subManagers.forEach(function (manager) {
      if (manager instanceof LabelManager) {
        vertex.labels.forEach(function (label) {
          manager.unobserve(label);
        });
      }

      if (manager instanceof VertexManager) {
        vertex.vertices.forEach(function (vertex) {
          manager.unobserve(vertex);
        });
      }

      if (manager instanceof EdgeManager) {
        vertex.edges.forEach(function (edge) {
          manager.unobserve(edge);
        });
      }
    });
  }

  async _interceptObserverCallback(valueSet, callback, results, deltaPlus, deltaMinus) {
    //execute submanagers load functions for the newly added vertices (deltaPlus)

    var self = this;
    var valueSets = await this.type.query.makeValueSets(
      valueSet,
      deltaPlus.map(function (e) {
        return e.getEObject();
      }),
    );

    var pendingVSets = valueSets.map(function (vSet) {
      //for each loaded vertex, apply the submanagers load routine
      let loadingSubManagers = [];
      self.subManagers.forEach(function (manager) {
        loadingSubManagers.push(manager.load(vSet));
      });
      return Promise.all(loadingSubManagers);
    });
    var evaluatedVSets = await Promise.all(pendingVSets);

    evaluatedVSets.forEach(function (vSetEvaluation, resultIdx) {
      vSetEvaluation.forEach(function (managerResult, managerIdx) {
        for (let i in managerResult) {
          if (self.subManagers[managerIdx] instanceof VertexManager) {
            if (!deltaPlus[resultIdx].containsVertex(managerResult[i])) {
              deltaPlus[resultIdx].addVertex(managerResult[i]);
            }
          }

          if (self.subManagers[managerIdx] instanceof StaticVertexManager) {
            deltaPlus[resultIdx].addVertex(managerResult[i]);
          }

          if (self.subManagers[managerIdx] instanceof EdgeManager) {
            if (!deltaPlus[resultIdx].containsEdge(managerResult[i])) {
              deltaPlus[resultIdx].addEdge(managerResult[i]);
            }
          }

          if (self.subManagers[managerIdx] instanceof LabelManager) {
            if (!deltaPlus[resultIdx].hasLabel(managerResult[i])) {
              deltaPlus[resultIdx].addLabel(managerResult[i]);
            }
          }
        }
      });
    });

    callback(results, deltaPlus, deltaMinus);
  }

  /**
   * Processes the results and creates vertices for the given results.
   * @param {Array<EObject>|EObject} results - The results from a query of the GraphManager to be processed. It can be an array of eObjects or a single eObject.
   * @param {Object} [container=null] - The container object. Used by observers. The container is e.g. the vertex that contains the observed vertices.
   * @returns {Array} - An array of vertices created from the results. If a vertex could not be created, an empty array is returned for that result.
   */
  async _postProcessResults(results, container = null) {
    var self = this;

    // Handling of getting 'null' as a result
    if (!results) {
      let container_id = container ? container.type.model.values.id : null;
      let container_name = container ? container.type.model.values.name : null;
      console.warn(
        `Problem in editorModel with id: ${self.type.model.values.id} and name: ${self.type.model.values.name}. Input: results: ${results}, container id: ${container_id}, container name: ${container_name}. The queryStr: ${self.type.model.values.queryStr} resulted with 'null' as a result. Cannot create a vertex for 'null'.\nThe queryStr: ${self.type.model.values.queryStr} likely wants to query a single value feature (SET). XGEE is optimized for features with a multiplicity of '*' (ADD). If you still want to display it as a vertex, turn it into a list by adding a '&TRM((=%),[])' to the queryStr.\nFor your better experience, I will skip this vertex for now and continue rendering. However you are now entering untested territory. It is highly recommended to use TRM and follow the docu at: https://docs.xgee.de/tutorial/xgee_example_app.html.`,
      );
      return []; // return an empty array to signal that the vertex could not be created and allow further processing. Empty list means so execution of .map, so no valueSets will be created.
    }

    if (!Array.isArray(results)) {
      results = [results];
    }

    // default behavior
    if (!container) {
      return results.map(function (eObject) {
        return self.graphModelFactory.createVertex(self.model, self.type, eObject);
      });
    }

    // container behavior (used by observers)
    return results.map(function (eObject) {
      let vertex = container.getVertexByEObject(eObject);
      if (!vertex) {
        vertex = self.graphModelFactory.createVertex(self.model, self.type, eObject);
      } else {
        if (vertex.type != self.type) {
          vertex = self.graphModelFactory.createVertex(self.model, self.type, eObject);
        }
      }
      return vertex;
    });
  }

  addCell(parentObject, vertex) {
    parentObject.addVertex(vertex);
  }
}
