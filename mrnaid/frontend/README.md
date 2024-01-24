# mRNAid Frontend

## Overview

This is a frontend application for mRNAid.

### Packages

* TypeScript
* React (Create React App)
* Recompose
* React-router
* Ant Design
* Axios
* XLSX
* file-saver
* recharts
* react-pdf
* fornac

### Repository overview

Repository is created with [create-react-app](https://github.com/facebook/create-react-app)

### Running the Development Mode

```bash
npm install
npm start
```

### Frontend Project Structure
- `/frontend`. This folder contains everything related to frontend 
    - `/src/pages`. This folder represents the main module which contains main form page and result page
    - `/src/config`. This folder contains default motifs and codons 
    - `/src/routes`. This folder contains list of routes used for page redirect
    - `/src/services`. This folder contains logic for interacting application with backend API
    - `/src/types`. This folder contains types required by input data and result data


### Application state

The state is provided from `src/App.tsx` via HOC `src/utils/withJobStore.ts`. State also serves as a cache (non-persistent) in order to save some network traffic. The state is explicitly propagated (with and/or via handlers) via props.

There are more local states handled via `recompose` for example in `src/components/WorkflowScene/WorkflowScene.tsx` by utilizing `src/utils/withCurrentStepState.ts`. This approach is preferred to the React stateful components.

### API interaction

The application interacts with backend API via `src/utils/withJobStore.ts` which internally uses `src/services/api.ts`. Results are then later parsed and transformed to display friendly format in `src/services/ResultsData.ts`.


