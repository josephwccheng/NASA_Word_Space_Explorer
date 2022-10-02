// global variables
const base_url = "https://word-space-exploration.azurewebsites.net/"
const search_engine_extension = "searchEngine"
const document_metadata_extension = "documentMetadata/"
const tag_recommender_extension = "tagRecommender"
var saved_query = ""
var document_list = ""

function searchClicked() {
    var query = document.getElementById("search").value;
    document.getElementById("tagResult").innerHTML = "";
    document.getElementById("documentResults").innerHTML = "";
    searchEngineQuery(query)
    tagRecommenderQuery(query)
}

// TODO
// function tagClicked(evt) {
//   console.log(evt.currentTarget.myParam)
//   // tag_value = document.getElementById(button_id).textContent
//   console.log('clicked!')
// }


/*
  Below are all the APIs
*/

// API Async function - documentMetadata
const getDocument = async (document_id) => {
    var response = await fetch(base_url + document_metadata_extension + document_id);
    var myJson = await response.json();
    console.log(myJson)
  }

const getDocumentandUpdateDocDiv = async (doc_index, document_id) => {
  var response = await fetch(base_url + document_metadata_extension + document_id);
  var myJson = await response.json();
  console.log(myJson)
}

// API Async function - searchEngine
const searchEngineQuery = async (query) => {
  payload = `{"query": "` + query + `"}`
  const response = await fetch(base_url + search_engine_extension, {
    method: 'POST',
    body: payload,
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const myJson = await response.json();
  console.log("Search Engine Query Result")
  console.log(myJson)
  saved_query = query;

  for(let i = 0; i < myJson.documentList.length; i++){
    var docDiv = document.createElement("div");
    docDiv.className= "docDiv"
    var doc_index = "docIndex"+i;
    docDiv.setAttribute("id", doc_index);
    var t = document.createTextNode(myJson.documentList[i]);       
    docDiv.appendChild(t);
    document.getElementById('documentResults').appendChild(docDiv);
    // getDocumentandUpdateDocDiv(doc_index, myJson.documentList[i])
  }
}

// API Async function - tag
const tagRecommenderQuery = async (query) => {
  payload = `{"query": "` + query + `"}`
  const response = await fetch(base_url + tag_recommender_extension, {
    method: 'POST',
    body: payload,
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const myJson = await response.json();
  console.log("Tag Recommender Query Result")
  console.log(myJson.tagsRecommended)

  for(let i = 0; i < myJson.tagsRecommended.length - 10; i++){
    var btn = document.createElement("button");
    btn.className = "btn";
    var button_id = "tag"+i;
    btn.setAttribute("id", button_id);
    var t = document.createTextNode(myJson.tagsRecommended[i]);       
    btn.appendChild(t);
    document.getElementById('tagResult').appendChild(btn);
    // TO DO
    // document.getElementById(button_id).addEventListener("click", tagClicked, false);
  }
}
