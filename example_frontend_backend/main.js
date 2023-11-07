function fetchData() {
  const responsePromise = fetch("/senator", {
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
      alert("Cannot obtain students")
    })
}

// For testing in the HTML world
// <!-- <button type="button" onclick="populateList([['a', 'b'], ['c', 'd']])"> -->
function populateList(results) {
  let list = document.getElementById("myList")

  results.forEach(element => {
    let senator = document.createElement("li")

    senator.innerText = element.state

    list.appendChild(senator)
  })
}