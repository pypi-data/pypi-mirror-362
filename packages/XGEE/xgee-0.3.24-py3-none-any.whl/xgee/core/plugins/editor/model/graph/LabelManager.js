import Query from "../../queries/Query.js";
import GraphObjectManager from "./GraphObjectManager.js";
import { replaceTemplates } from "../../lib/libaux.js";
import LabelSegmentManager from "./LabelSegmentManager.js";

export default class LabelManager extends GraphObjectManager {
  constructor(...args) {
    super(...args);
  }

  /**
   * Based on ContainerManager.load()
   * Copies valueSet to make sure that sub-managers do not modify the original valueSet - not sure if this is necessary
   * Does a .refreshContent()
   * Each LabelSegment exists exactly once, so we turn it into a list to stay compatible
   * @param valueSet
   * @returns {Promise<(*|FloatingLabel)[]>}
   */
  async load(valueSet) {
    const managerCell = this.graphModelFactory.createLabel(this.type); // the labelCell

    const subManagersCells = await Promise.all(
      this.subManagers.map((subManager) => subManager.load({ ...valueSet })), // clone vSet defensively, not sure if necessary but safer
    );
    this.subManagers.forEach((subManager, subManagerIdx) => {
      let subManagerCells = subManagersCells[subManagerIdx];
      // every LabelSegment exists exactly 1 time, we turn it into a list to stay compatible
      subManagerCells = [subManagerCells];
      subManager.addCells(managerCell, subManagerCells);
    });

    managerCell.refreshContent();
    return [managerCell];
  }

  async observe(valueSet, callback, labelProvider) {
    var self = this;
    labelProvider.labels.forEach(function (label) {
      self.subManagers.forEach(function (manager) {
        if (manager instanceof LabelSegmentManager) {
          label.segments
            .filter(function (segment) {
              return segment.type == manager.type;
            })
            .forEach(function (segment) {
              manager.observe(valueSet, segment);
            });
        }
      });
    });
  }

  async unobserve(label) {
    var self = this;
    self.subManagers.forEach(function (manager) {
      if (manager instanceof LabelSegmentManager) {
        label.segments
          .filter(function (segment) {
            return segment.type == manager.type;
          })
          .forEach(function (segment) {
            manager.unobserve(segment);
          });
      }
    });
  }

  addCell(parentObject, label) {
    parentObject.addLabel(label);
  }
}
