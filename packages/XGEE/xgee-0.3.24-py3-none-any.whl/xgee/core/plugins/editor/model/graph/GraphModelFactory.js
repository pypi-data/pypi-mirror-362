/* Factory Class for Graph Model Objects */

import GraphResourceProvider from "../../graph/GraphResourceProvider.js";
import GraphModel from "./GraphModel.js";

//GraphObjects
import Vertex from "./Vertex.js";
import VertexType from "./VertexType.js";
import StaticVertex from "./StaticVertex.js";
import StaticVertexType from "./StaticVertexType.js";

import Container from "./Container.js";
import ContainerType from "./ContainerType.js";

import Edge from "./Edge.js";
import EdgeType from "./EdgeType.js";

import Anchor from "./Anchor.js";
import AnchorType from "./AnchorType.js";

import FloatingLabel from "./FloatingLabel.js";
import NestedLabel from "./NestedLabel.js";
import LabelType from "./LabelType.js";

import LabelSegment from "./LabelSegment.js";
import LabelSegmentType from "./LabelSegmentType.js";

//Managers
import GraphModelManager from "./GraphModelManager.js";

import GraphLayoutManager from "./GraphLayoutManager.js";

import VertexManager from "./VertexManager.js";
import StaticVertexManager from "./StaticVertexManager.js";
import ContainerManager from "./ContainerManager.js";

import EdgeManager from "./EdgeManager.js";

import AnchorManager from "./AnchorManager.js";

import LabelManager from "./LabelManager.js";
import LabelSegmentManager from "./LabelSegmentManager.js";

/**
 * Containments of the DisplayableObjects in the Editor model.
 * E.g. Edge has anchors and containers.
 * The depth-first search (DFS) uses this to know where to recurse.
 * This allows an arbitrary containment hierarchy of subVertices.
 */
const EDITOR_MODEL_CONTAINMENTS = {
  Vertex:          ["subVertices", "subEdges", "labels"],
  SubVertex:       ["subVertices", "subEdges", "labels"],
  StaticVertex:    ["subVertices", "subEdges", "labels"],
  StaticSubVertex: ["subVertices", "subEdges", "labels"],
  Edge:            ["anchors", "containers"],
  Container:       ["subVertices"],
  Anchor:          [],
  FloatingLabel:   ["segments"],
  NestedLabel:     ["segments"],
  LabelSegment:    [],
};

/**
 * Maps the editorModel DisplayableObjects to their corresponding managers.
 * E.g. SubVertex and Vertex are both manage by VertexManager.
 * Produces a per-call table that maps an EClass name to:
 *   • `ManagerConstructor` – the concrete *Manager* subclass we must create
 *   • `createType`         – builds the corresponding *Type* object
 */
function mappingDisplayableObjects2Managers(factory, ecoreSync) {
  return {
    Vertex: {
      ManagerConstructor: VertexManager,
      createType: elem => factory.createVertexType(ecoreSync, elem),
    },
    SubVertex: {
      ManagerConstructor: VertexManager,
      createType: elem => factory.createVertexType(ecoreSync, elem),
    },
    StaticVertex: {
      ManagerConstructor: StaticVertexManager,
      createType: elem => factory.createStaticVertexType(ecoreSync, elem),
    },
    StaticSubVertex: {
      ManagerConstructor: StaticVertexManager,
      createType: elem => factory.createStaticVertexType(ecoreSync, elem),
    },
    Edge: {
      ManagerConstructor: EdgeManager,
      createType: elem => factory.createEdgeType(ecoreSync, elem),
    },
    Container: {
      ManagerConstructor: ContainerManager,
      createType: elem => factory.createContainerType(ecoreSync, elem),
    },
    Anchor: {
      ManagerConstructor: AnchorManager,
      createType: elem => factory.createAnchorType(ecoreSync, elem),
    },
    FloatingLabel: {
      ManagerConstructor: LabelManager,
      createType: elem => factory.createLabelType(ecoreSync, elem),
    },
    NestedLabel: {
      ManagerConstructor: LabelManager,
      createType: elem => factory.createLabelType(ecoreSync, elem),
    },
    LabelSegment: {
      ManagerConstructor: LabelSegmentManager,
      createType: elem => factory.createLabelSegmentType(ecoreSync, elem),
    },
  };
}


/**
 * Factory for creating GraphModel
 * GraphModel is the M of MVC - the MxGraph model
 * it contains the hierarchy of  mxCells of the current editor
 * it also contains the hierarchy of mangers to keep the model in sync with the usermodel
 */
class GraphModelFactory {
  constructor(repositoryURL) {
    this.resourceProvider = new GraphResourceProvider(repositoryURL);
  }

  _getEditorModel(model) {
    var lvl = model;
    while (lvl.eClass.get("name") != "Editor") {
      lvl = lvl.eContainer;
      if (!lvl) break;
    }
    return lvl;
  }

  _getRepositoryURL(model) {
    var url = "";
    var editorModel = this._getEditorModel(model);
    if (editorModel) {
      url = editorModel.get("repositoryURL");
    }
    return url;
  }

  createModel(ecoreSync, model, eObject) {
    var graphModel = new GraphModel();
    graphModel.eObject = eObject;
    graphModel.layout = new GraphLayoutManager(eObject);
    graphModel.graphObjectDefinitions = model;
    graphModel.manager = this.createModelManager(ecoreSync, graphModel, model);
    return graphModel;
  }

  /**
   * Assemble the full Manager tree for graphModel by a
   * table-driven depth-first search (DFS) over the editorModel displayableObjects.
   *
   *  • `managerByEClass` says how to build a manager for each EClass.
   *  • `EDITOR_MODEL_CONTAINMENTS` says what child elements are available.
   *
   * The traversal fails fast for unknown EClasses.
   *
   * @param {EsInstance} ecoreSync – our EcoreSync instance
   * @param {GraphModel} graphModel – the GraphModel (mxGraph) to populate
   * @param {EObject} modelDefinition – the editorModel, e.g. OAAM Functions Editor
   * @returns {GraphModelManager} – the populated root manager
   */
  createModelManager(ecoreSync, graphModel, modelDefinition) {
    const managerByEClass = mappingDisplayableObjects2Managers(this, ecoreSync);

    // The root GraphModel manager owns every other manager
    const rootGraphModelManager = new GraphModelManager(
      this,
      ecoreSync,
      graphModel,
      this.resourceProvider,
    );

    // Instantiate and attach a manager for `element'
    const instantiateManager = (parentManager, element) => {
      const className = element.eClass.get("name");
      const manager = managerByEClass[className];

      if (!manager) {
        throw new Error(
          `Unsupported EClass “${className}”. ` +
            `Add a mapping in mappingDisplayableObjects2Managers() inside GraphModelFactory.`,
        );
      }

      const typeObject = manager.createType(element);
      const { ManagerConstructor } = manager;

      const managerInstance = new ManagerConstructor(
        this, // graphModelFactory
        ecoreSync,
        typeObject,
        graphModel,
        this.resourceProvider,
      );

      parentManager.subManagers.push(managerInstance);
      return managerInstance;
    };

    // Depth-first search that mirrors the editorModel displayableObjects containment tree
    const traverseDepthFirst = (element, parentManager) => {
      const currentManager = instantiateManager(parentManager, element);

      const childContainmentNames = EDITOR_MODEL_CONTAINMENTS[element.eClass.get("name")] || [];

      for (const containmentName of childContainmentNames) {
        for (const child of element.get(containmentName).array()) {
          traverseDepthFirst(child, currentManager);
        }
      }
    };

    // Start here: with the model’s top-level displayableObjects (Vertex, StaticVertex, Edge), e.g. Task, Signal
    for (const displayable of modelDefinition.get("displayableObjects").array()) {
      traverseDepthFirst(displayable, rootGraphModelManager);
    }

    return rootGraphModelManager;
  }

  createVertexType(ecoreSync, model) {
    const vertexType = new VertexType(ecoreSync, model);
    const filepath = model?.get("shape")?.get("filepath");
    vertexType.shape = filepath ? this.resourceProvider.LoadResource(filepath) : null;
    return vertexType;
  }

  createVertex(graphModel, type, eObject) {
    var vertex = new Vertex(graphModel);
    vertex.eObject = eObject;
    vertex.type = type;
    vertex.init();
    return vertex;
  }

  createStaticVertexType(ecoreSync, model) {
    const staticVertexType = new StaticVertexType(ecoreSync, model);
    const filepath = model?.get("shape")?.get("filepath");
    staticVertexType.shape = filepath ? this.resourceProvider.LoadResource(filepath) : null;
    return staticVertexType;
  }

  createStaticVertex(graphModel, type, eObject) {
    var staticVertex = new StaticVertex(graphModel);
    staticVertex.eObject = eObject;
    staticVertex.type = type;
    staticVertex.init();
    return staticVertex;
  }

  createEdgeType(ecoreSync, model) {
    return new EdgeType(ecoreSync, model);
  }

  createEdge(graphModel, type, eObject) {
    var edge = new Edge(graphModel);
    edge.eObject = eObject;
    edge.type = type;
    edge.init();
    return edge;
  }

  createLabelType(ecoreSync, model) {
    return new LabelType(ecoreSync, model);
  }

  createLabel(type) {
    let label;

    switch (type.model.eClass.get("name")) {
      case "FloatingLabel":
        label = new FloatingLabel();
        break;
      case "NestedLabel":
        label = new NestedLabel();
        break;
      default:
        label = null;
    }

    label.type = type;
    label.init();
    return label;
  }

  createLabelSegmentType(ecoreSync, model) {
    return new LabelSegmentType(ecoreSync, model);
  }

  createLabelSegment(type) {
    var labelSegment = new LabelSegment();
    labelSegment.type = type;
    labelSegment.content = "";
    return labelSegment;
  }

  createContainerType(ecoreSync, model) {
    const containerType = new ContainerType(ecoreSync, model);
    const filepath = model?.get("shape")?.get("filepath");
    containerType.shape = filepath ? this.resourceProvider.LoadResource(filepath) : null;
    return containerType;
  }

  createContainer(graphModel, type, eObject) {
    var container = new Container(graphModel);
    container.eObject = eObject;
    container.type = type;
    container.init();
    return container;
  }

  createAnchorType(ecoreSync, model) {
    return new AnchorType(ecoreSync, model);
  }

  createAnchor(graphModel, type, eObject) {
    var anchor = new Anchor(graphModel);
    anchor.eObject = eObject;
    anchor.type = type;
    return anchor;
  }
}

export default GraphModelFactory;
