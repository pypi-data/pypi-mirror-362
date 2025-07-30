import React, { useEffect,useRef } from 'react'
import { Cosmograph,CosmographProvider } from '@cosmograph/react'
import "./App.css"



export default function App({ data,params }) {
  const cosmographRef = useRef(null)
  const graphRef = useRef(null);

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
    <CosmographProvider>
    <Cosmograph
      ref={cosmographRef}
      backgroundColor={backgroundColor}
      nodes={data.nodes}
      links={data.links}
      linkArrows={linkArrows}
      renderLinks={renderLinks}
      nodeColor={(d) => d.colour ?? "blue"}
      nodeSize={(d) => d.size ?? 5}
      scaleNodesOnZoom={scaleNodesOnZoom}
      nodeLabelColor={(d) => d.colour ?? "blue"}
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
