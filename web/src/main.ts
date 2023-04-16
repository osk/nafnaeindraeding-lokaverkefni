/**
 * Based on example:
 * https://codesandbox.io/s/sigma-example-csv-to-network-map-2mqjf
 */

import Sigma from 'sigma';
import circular from 'graphology-layout/circular';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import { cropToLargestConnectedComponent } from 'graphology-components';

import Graph from 'graphology';

import relations from './relations.json';
// import relations from './weak.json';

const graph: Graph = new Graph();

relations.forEach((relation) => {
  if (!graph.hasNode(relation.source)) {
    graph.addNode(relation.source, {
      label: relation.source,
    });
  }
  if (!graph.hasNode(relation.target)) {
    graph.addNode(relation.target, {
      label: relation.target,
    });
  }

  if (!graph.hasEdge(relation.source, relation.target)) {
    graph.addEdge(relation.source, relation.target, { label: relation.type });
  }
});

cropToLargestConnectedComponent(graph);

const degrees = graph.nodes().map((node) => graph.degree(node));
const minDegree = Math.min(...degrees);
const maxDegree = Math.max(...degrees);
const minSize = 3,
  maxSize = 15;
graph.forEachNode((node) => {
  const degree = graph.degree(node);
  graph.setNodeAttribute(
    node,
    'size',
    minSize +
      ((degree - minDegree) / (maxDegree - minDegree)) * (maxSize - minSize),
  );
});

circular.assign(graph);
const settings = forceAtlas2.inferSettings(graph);
forceAtlas2.assign(graph, { settings, iterations: 600 });

const container = document.getElementById('sigma-container') as HTMLElement;
new Sigma(graph, container, { renderEdgeLabels: true });
