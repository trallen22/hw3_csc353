const searchPlayerBtn = document.getElementById("search-btn");

const player_name = document.getElementById("player-input").value

function fetchData() {
  const responsePromise = fetch("/player?name=" + player_name.replace(/\s/g, ''), {
    method: "GET",
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });

  responsePromise.then(
    // Fulfilled
    async (response) => {
      populateList(await response.json())
    },
    // Error
    (error) => {
      alert("Cannot obtain player")
    })
}

function populateList(results) {
  let list = document.getElementById("myList")

  results.forEach(element => {
    let senator = document.createElement("li")

    senator.innerText = element.state

    list.appendChild(senator)
  })

}

searchPlayerBtn.addEventListener('click', fetchData);