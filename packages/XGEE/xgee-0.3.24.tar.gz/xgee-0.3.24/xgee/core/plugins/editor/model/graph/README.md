model/graph: the Model part of MVC

# Model of MVC

## GraphModel.js
The root of the graph model. Holds all vertices and edges. 
Represents an eObject from EOQ, e.g. Functions #33
Created by GraphModelFactory.

## editorModel displayableObjects
Anchor, Container, Edge, FloatingLabel, NestedLabel, LabelSegment, StaticVertex, Vertex

These will be the 'values' of created mxGraph mxCell. Actual creation of mxCells is happening in GraphView.js.
Many classes that are used as mixins add functionality, similar to how it looks in the editorModel metamodel.

Abstract classes to inherit from: DeletableObject, EObjectOwner, EventProvider, GraphEvent, LocatableObject, RoutableObject, SizableObject, TransactionObject, TypedObject, EdgeContainer, VertexContainer.  
VertexContainer/EdgeContainer/LabelProvider/ContainerProvicer: displayableObject can have vertices/edges/labels/containers. 

## Manager
Loads and observes GraphModel and displayableObjects.

## Type
The type from the editorModel. 

## GraphLayoutManager.js
Responsible for the layout.

## Interaction with other packages

- **GraphController** (`plugins/editor/controllers/graph`) uses `GraphModel` and
  `GraphLayoutManager` to initialize and update the graph. It reacts to model events and
  delegates user actions.
- **GraphView** (`plugins/editor/view`) renders the model using mxGraph. It listens to
  controller events and refreshes the view when the model changes.
- **GraphResourceProvider** (`plugins/editor/graph`) loads external resources such as SVG
  shapes required by the object types. The factory and managers use it when creating
  objects.

