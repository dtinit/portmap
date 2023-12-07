// query_form.js handles populating the query form dropdowns on index.html,
// as well as saving form state to session storage to smooth the user experience.
// Dropdowns are filled based on selections so far, rather than show all options
// some of which are invalid for the content type chosen.

function setupDropdown(dropdownElement, possibleValues) {
    dropdownElement.innerHTML = "";
    let defaultOption = document.createElement('option');
    defaultOption.text = 'Select an option';
    defaultOption.value = '';
    dropdownElement.add(defaultOption, dropdownElement.options[0]);
    dropdownElement.selectedIndex = 0;
    let uniqueValues = [...new Set(possibleValues)];

    if (uniqueValues.length > 0) {
        uniqueValues.forEach((value) => {
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

document.addEventListener('DOMContentLoaded', function() {

  let typeDropdown = document.getElementById("id_datatype");
  let sourceDropdown = document.getElementById("id_datasource");
  let destDropdown = document.getElementById("id_datadest");

  if (!(typeDropdown && sourceDropdown && destDropdown)) {
    console.error("Missing expected form elements - id_datatype, id_datasource and id_datadest");
    return;
  }

  function saveFormState() {
    try {
      sessionStorage.setItem('selectedType', typeDropdown.value);
      sessionStorage.setItem('selectedSource', sourceDropdown.value);
      sessionStorage.setItem('selectedDest', destDropdown.value);
    } catch (e) {
      console.log("Session storage not available; form contents may reset")
    }
  }

  // Add an event listener so that when the content type is chosen, a list of known sources is populated
  // for the next step
  typeDropdown.addEventListener("change", function () {
    saveFormState();
    setupDropdown(sourceDropdown, Object.keys(queryStructure[typeDropdown.value]));
    setupDropdown(destDropdown, []);
  });

  // Then when the source for data is chosen, a list of destinations
  sourceDropdown.addEventListener("change", function () {
    saveFormState();
    setupDropdown(destDropdown, queryStructure[typeDropdown.value][sourceDropdown.value]);
  });

  destDropdown.addEventListener('change', saveFormState);

  // Restore form state
  function restoreFormState() {
    try {
      let selectedType = sessionStorage.getItem('selectedType');
      if (selectedType && selectedType !== typeDropdown.value) {
          typeDropdown.value = selectedType;
          setupDropdown(sourceDropdown, Object.keys(queryStructure[selectedType]));
      }
      let selectedSource = sessionStorage.getItem('selectedSource');
      if (selectedSource && selectedSource !== sourceDropdown.value) {
          sourceDropdown.value = selectedSource;
          setupDropdown(destDropdown, queryStructure[selectedType][selectedSource]);
      }
      let selectedDest = sessionStorage.getItem('selectedDest');
      if (selectedDest && selectedDest !== destDropdown.value) {
          destDropdown.value = selectedDest;
      }
    } catch (e) {
      console.log("Error restoring form state - sessionStorage may not be available", e)
    }
  }

  // Call this function when the page loads in case it loads from a "back" action
  restoreFormState();
});
