// query_form.js handles populating the query form dropdowns on index.html.
// Dropdowns are filled based on selections so far, rather than show 100s of items
// not all of which are consistent.

function setupDropdown(dropdownElement, possibleValues) {
    dropdownElement.innerHTML = "";
    let defaultOption = document.createElement('option');
    defaultOption.text = 'Select an option';
    defaultOption.value = '';
    dropdownElement.add(defaultOption, dropdownElement.options[0]);
    dropdownElement.selectedIndex = 0;

    if (possibleValues.length > 0) {
        possibleValues.forEach((value) => {
            const option = document.createElement("option");
            option.text = value;
            option.value = value;
            dropdownElement.appendChild(option);
        });
        dropdownElement.disabled = false;
    } else {
        dropdownElement.disabled = true;
    }

}

const typeDropdown = document.getElementById("id_datatype");
const sourceDropdown = document.getElementById("id_datasource");
const destDropdown = document.getElementById("id_datadest");

function saveFormState() {
    sessionStorage.setItem('selectedType', typeDropdown.value);
    sessionStorage.setItem('selectedSource', sourceDropdown.value);
    sessionStorage.setItem('selectedDest', destDropdown.value);
}

// Add an event listener so that when the content type is chosen, a list of known sources is populated
// for the next step
typeDropdown.addEventListener("change", function () {
    saveFormState();
    const selectedType = typeDropdown.value;
    const knownSources = Object.keys(queryStructure[selectedType]);
    setupDropdown(sourceDropdown, knownSources);
    setupDropdown(destDropdown, []);
});

// Then when the source for data is chosen, a list of destinations
sourceDropdown.addEventListener("change", function () {
    saveFormState();
    const selectedType = typeDropdown.value;
    const selectedSource = sourceDropdown.value;
    const knownDestinations = queryStructure[selectedType][selectedSource];

    setupDropdown(destDropdown, knownDestinations);

});


destDropdown.addEventListener('change', saveFormState);

// Restore form state
function restoreFormState() {
    let selectedType = sessionStorage.getItem('selectedType');
    if (selectedType && selectedType != typeDropdown.value) {
        typeDropdown.value = selectedType;
        let knownSources = Object.keys(queryStructure[selectedType]);
        setupDropdown(sourceDropdown, knownSources);
    }
    let selectedSource = sessionStorage.getItem('selectedSource');
    if (selectedSource && selectedSource != sourceDropdown.value) {
        sourceDropdown.value = selectedSource;
        let knownDestinations = queryStructure[selectedType][selectedSource];
        setupDropdown(destDropdown, knownDestinations);
    }
    let selectedDest = sessionStorage.getItem('selectedDest');
    if (selectedDest && selectedDest != destDropdown.value) {
        destDropdown.value = selectedDest;
    }
}

// Call this function when the page loads

restoreFormState();
