/*************************************************************************
_/                _/  _/_/_/    _/_/_/    _/_/_/    _/_/_/    _/      _/  
_/              _/   _/    _/  _/    _/  _/    _/  _/    _/    _/  _/     
_/    _/_/    _/    _/_/_/    _/_/_/    _/    _/  _/_/_/        _/        
_/  _/  _/  _/     _/        _/    _/  _/    _/  _/  _/        _/         
_/_/    _/_/      _/        _/_/_/    _/_/_/    _/    _/      _/  made it!
*************************************************************************/

document.getElementById("builder-form").addEventListener("submit", function(event){
    event.preventDefault();
    const budget = document.getElementById("builder-input").value;
    displayTeamResult(budget);
});

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

async function displayTeamResult(budget) {
    //Check valid input
    if(isNaN(budget) || budget - Math.floor(budget) != 0) {
        alert("Please enter a number without decimal point or other characters");
        return
    }
    //Set loading message
    var teamResultDiv = document.getElementById("team-result-div");
    teamResultDiv.innerHTML = "Calculating your team...";
    //Get results
    sendTeamRequest(budget)
    .catch(function(error) {
        console.log(error);
        if(error.message == "Failed to fetch") {
        alert("Connection error!");
        };
    })
    .then(payload => generateTeamResultsHtmlElements(payload))
    .catch(error => console.error(error))
    //Display results
    .then(function(htmlElements) {
        teamResultDiv.innerHTML = "";
        teamResultDiv.appendChild(htmlElements.header);
        teamResultDiv.appendChild(htmlElements.table);
    });
};

async function sendTeamRequest(budget) {
  const payload = {
    budget: budget
  }
  const response = await fetch(teamApiUrl, {
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json"
    },
    redirect: "follow",
    referrer: "no-referrer",
    body: JSON.stringify(payload)
  });
  return await response.json();
};

function generateTeamResultsHtmlElements(teamJson) {
  console.log(teamJson);
  //Create header
  var headerEl = document.createElement("h2");
  var table = document.createElement("table");
  if(teamJson.team_is_complete) {
    var headerText = document.createTextNode("You can have the following team for: €" + teamJson.price + ",00");
    //Create table
    //Add header row
    var tableHeader = {
      photo: profilePhotoUrl,
      name: "Name",
      position: "Position",
      age: "Age",
      nationality: "Nationality",
      position_score: "Score",
      value: "Value",
      preferred_foot: "Foot",
      height: "Height"
    };
    var headerRow = createResultRowTeam(tableHeader, "th");
    table.appendChild(headerRow);
    //Add result rows
    const teamPositions = ["goalkeeper", "fullback", "halfback", "forward playing"]
    for(var k=0; k<teamPositions.length; k++) {
      var position = teamPositions[k];
      var positionPlayers = teamJson[position];
      for (var l=0; l<positionPlayers.length; l++) {
        positionPlayers[l].position = capitalize(position);
        row = createResultRowTeam(positionPlayers[l], "td");
        table.appendChild(row);
      }
    }
  } else {
    var headerText = document.createTextNode("€" + teamJson.budget + ",00 is too little to buy an entire team :(");
  }
  headerEl.appendChild(headerText);
  return {
    header: headerEl,
    table: table
  };
};

function createResultRowTeam(resultItem, cellType) {
  var row = document.createElement("tr");
  const teamKeys = ["photo", "position", "name", "age", "nationality", "position_score", "value", "preferred_foot", "height"];
  for(var j=0; j<teamKeys.length; j++) {
    var cell = document.createElement(cellType);
    if(teamKeys[j] === "photo") {
      var cellContent = document.createElement("img");
      cellContent.setAttribute("src", resultItem.photo);
      cellContent.setAttribute("alt", resultItem.name);
    } else {
      var cellContent = document.createTextNode(resultItem[teamKeys[j]]);
    };
    cell.appendChild(cellContent);
    row.appendChild(cell);
  };
  return row;
};