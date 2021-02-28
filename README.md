<h1>Cards Against Online</h1>

[![Build Status](https://www.travis-ci.org/z0glen/cards-against-online.svg?branch=master)](https://www.travis-ci.org/z0glen/cards-against-online)

An online player inspired by the Cards Against Humanity game. Currently supports only limited custom cards.

See the live demo [here](https://cahplayer.herokuapp.com/).

<h2>Running Locally</h2>

- The frontend and backend build separately and communicate using websockets
- From inside the client package, run `npm run serve`
- From inside the server package, run `python3 run.py`
    
<h2>Deployment</h2>
- Any pushed commit will trigger a travis build to ensure that everything compiles
- Any PR will trigger a travis build, and the build must be successful to merge
- Committing to master will automatically trigger a deployment, this should only be done through approved PRs
- For more details on the deployment process, see the .travis.yml file

<h2>Notes</h2>
- Currently only supports cards as defined in the calls and responses json files
- Cards must be defined with all of the same standard fields

