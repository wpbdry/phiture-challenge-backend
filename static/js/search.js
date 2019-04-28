/*************************************************************************
_/                _/  _/_/_/    _/_/_/    _/_/_/    _/_/_/    _/      _/  
_/              _/   _/    _/  _/    _/  _/    _/  _/    _/    _/  _/     
_/    _/_/    _/    _/_/_/    _/_/_/    _/    _/  _/_/_/        _/        
_/  _/  _/  _/     _/        _/    _/  _/    _/  _/  _/        _/         
_/_/    _/_/      _/        _/_/_/    _/_/_/    _/    _/      _/  made it!
*************************************************************************/

document.getElementById("search-form").addEventListener("submit", function(event){
    event.preventDefault();
    const searchTerm = document.getElementById("search-input").value;
    displaySearchResults(searchTerm);
});

async function displaySearchResults(searchTerm) {
  //Set loading message
  var resultsDiv = document.getElementById("results-div");
  resultsDiv.innerHTML = "Searching...";
  //Get results
  sendSearchRequest(searchTerm)
    .catch(function(error) {
      console.log(error);
      if(error.message == "Failed to fetch") {
        alert("Connection error!");
      };
    })
    .then(payload => generateSearchResultsHtmlElements(payload))
    .catch(error => console.error(error))
    //Display results
    .then(function(htmlElements) {
      resultsDiv.innerHTML = "";
      resultsDiv.appendChild(htmlElements.header1);
      resultsDiv.appendChild(htmlElements.results1);
      resultsDiv.appendChild(htmlElements.header2);
      resultsDiv.appendChild(htmlElements.results2);
      document.getElementById("search-input").select();
    });
};

async function sendSearchRequest(searchTerm) {
  const payload = {
    searchterm: searchTerm
  }
  const response = await fetch(searchApiUrl, {
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

function generateSearchResultsHtmlElements(apiReturn) {
  console.log(apiReturn);
  //1 is exact search matches and 2 is close search matches, as returned from the server
  var headerText1 = document.createTextNode("");
  var headerText2 = document.createTextNode("");
  var resultsTable1 = document.createElement("div");
  var resultsTable2 = document.createElement("div");
  switch (apiReturn.exitcode) {
    case 1: //Server received empty search result
      if(apiReturn.search === "") {
        headerText1 = document.createTextNode("Please no empty searches :)");
      } else {
        headerText1 = document.createTextNode("Unknown server error...");
      };
      break;
    case 2: //Serverside database connection error
      alert("Sorry! Our backend could not connect to remote database hosted on elephantsql.");
    case 3: //Other unknown server side error
      headerText1 = document.createTextNode("Unknown server error...");
      break;
    default: //Array of results is returned as expected
      results = apiReturn.results;
      moreResults = apiReturn.moreresults;
      if (results.length === 0) {
        headerText1 = document.createTextNode("No exact matches for: " + apiReturn.search);
      } else {
        headerText1 = document.createTextNode("Exact matches for: " + apiReturn.search);
        resultsTable1 = createResultsTable(results);
      };
      if (moreResults.length !== 0) {
        headerText2 = document.createTextNode("Close matches for: " + apiReturn.search);
        resultsTable2 = createResultsTable(moreResults);
      }
  };
  // Return elements
  var headerEl1 = document.createElement("h2");
  var headerEl2 = document.createElement("h2");
  headerEl1.appendChild(headerText1);
  headerEl2.appendChild(headerText2);
  return {
    header1: headerEl1,
    results1: resultsTable1,
    header2: headerEl2,
    results2: resultsTable2
  };
};

function createResultsTable(searchResults) {
  //Create table
  table = document.createElement("table");
  //Add header row
  var tableHeader = {
    photo: profilePhotoUrl,
    name: "Name",
    age: "Age",
    nationality: "Nationality",
    club: "Club",
    overall: "Overall Score",
    value: "Value"
  };
  var headerRow = createResultRow(tableHeader, "th");
  table.appendChild(headerRow);
  //Add result rows
  for(var i=0; i<searchResults.length; i++) {
    row = createResultRow(searchResults[i], "td");
    table.appendChild(row);
  };
  //Return results
  return table
};

function createResultRow(resultItem, cellType) {
  var row = document.createElement("tr");
  const keys = ["photo", "name", "age", "nationality", "club", "overall", "value"];
  for(var j=0; j<keys.length; j++) {
    var cell = document.createElement(cellType);
    if(keys[j] === "photo") {
      var cellContent = document.createElement("img");
      cellContent.setAttribute("src", resultItem.photo);
      cellContent.setAttribute("alt", resultItem.name);
    } else {
      var cellContent = document.createTextNode(resultItem[keys[j]]);
    };
    cell.appendChild(cellContent);
    row.appendChild(cell);
  };
  return row;
};