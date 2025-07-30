import React, { useEffect,useRef } from 'react'
import { Cosmograph,CosmographProvider } from '@cosmograph/react'
import "./App.css"

function Legend({ legend }) {
  return (
    <div className="legend-box">
      {legend.map(({ group, colour }) => (
        <div key={group} style={{ display: "flex", alignItems: "center", marginBottom: 4 }}>
          <span className="legend-dot" style={{ backgroundColor: colour }} ></span>
          <span>{group}</span>
        </div>
      ))}
    </div>
  );
}


export default function App({ data,params, legend }) {
  const cosmographRef = useRef(null)
  const graphRef = useRef(null);
  const colourMap = Object.fromEntries(legend.map(({ group, colour }) => [group, colour]));
  const {
    backgroundColor = "transparent",
    linkArrows = false,
    scaleNodesOnZoom = false,
    simulationGravity = 0.25,
    simulationRepulsion = 0.1,
    simulationRepulsionTheta = 1.7,
    simulationLinkDistance = 2,
    simulationFriction = 0.85,
    simulationCenter = 0.0,
    renderLinks = true,
    simulationDecay = 1000,
    simulationRepulsionFromMouse = 2.0,
    simulationLinkSpring = 1.0
  } = params || {};
  console.log("PARAMS:", params);
  const playPause = () => {
        if ((cosmographRef.current)?.isSimulationRunning) {
            (cosmographRef.current)?.pause();
        } else {
            (cosmographRef.current)?.start();
        }
    }
  const fitView = () => {
    console.log("PARAMS:", params);
    (cosmographRef.current)?.fitView();
        graphRef.current?.scrollIntoView({ behavior: 'smooth' });
    }

  return (
    <div ref={graphRef}>
      <Legend legend={legend} />
    <CosmographProvider>
    <Cosmograph
      ref={cosmographRef}
      backgroundColor={backgroundColor}
      nodes={data.nodes}
      links={data.links}
      linkArrows={linkArrows}
      renderLinks={renderLinks}
      nodeColor={(d) =>  colourMap[d.group] ?? "blue"}
      nodeSize={(d) => d.size ?? 5}
      scaleNodesOnZoom={scaleNodesOnZoom}
      nodeLabelColor={(d) =>  colourMap[d.group] ?? "blue"}
      nodeLabelAccessor={(d) => d.label}
      simulationGravity={simulationGravity}
      simulationRepulsion={simulationRepulsion}
      simulationRepulsionTheta={simulationRepulsionTheta}
      simulationLinkDistance={simulationLinkDistance}
      simulationLinkSpring={simulationLinkSpring}
      simulationFriction={simulationFriction}
      simulationDecay={simulationDecay}
      simulationCenter={simulationCenter}
      simulationRepulsionFromMouse={simulationRepulsionFromMouse}
    />
      <div className="controls">
        <button
          onClick={playPause}
          className="control-button"
        >
          Pause/Play
        </button>
        <button
          onClick={fitView}
          className="control-button"
        >
          Fit
        </button>
      </div>
    </CosmographProvider>
    </div>
  )
}
