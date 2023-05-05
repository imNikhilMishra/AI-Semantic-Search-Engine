const queryInput = document.getElementById("query");
const languageSelect = document.getElementById("language");
const resultsDiv = document.getElementById("results");

function performSearch() {
    // Get query and language from input fields
    const query = queryInput.value;
    const language = languageSelect.value;

    // Call the back-end function to perform the search
    fetch(`/search?query=${query}&language=${language}`)
        .then(response => response.json())
        .then(data => {
            // Clear the previous search results
            resultsDiv.innerHTML = "";

            // Display the search results
            if (data.length === 0) {
                resultsDiv.innerHTML = "<p>No results found.</p>";
            } else {
                data.forEach(result => {
                    const documentLink = `<a href="#">Document ${result.id + 1}</a>`;
                    const score = `Score: ${result.score.toFixed(2)}`;
                    const language = `Language: ${result.language}`;
                    const resultDiv = `<div>${documentLink} (${score}, ${language})</div>`;
                    resultsDiv.insertAdjacentHTML("beforeend", resultDiv);
                });
            }
        })
        .catch(error => {
            console.error(error);
            resultsDiv.innerHTML = "<p>An error occurred. Please try again later.</p>";
        });
}
