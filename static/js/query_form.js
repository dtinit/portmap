function createOptionElement(text, value = text) {
  const element = document.createElement("option");
  return Object.assign(element, { text, value });
}

// query_form.js handles populating the query form dropdowns on index.html,
// as well as saving form state to session storage to smooth the user experience.
// Dropdowns are filled based on selections so far, rather than show all options
// some of which are invalid for the content type chosen.
function createDropdownValuesSetter({
  dropdownElement,
  placeholder = "Select an option",
}) {
  return function setDropdownValues(possibleValues) {
    dropdownElement.innerHTML = "";
    const uniqueValues = Array.from(new Set(possibleValues));
    const optionElements = [createOptionElement(placeholder, "")].concat(
      uniqueValues.map((value) => createOptionElement(value))
    );
    dropdownElement.append(...optionElements);
    dropdownElement.disabled = uniqueValues.length === 0;
  };
}

function changeHelp(new_text) {
  let help_text = document.getElementById("help_text");
  help_text.innerText = new_text;
}

document.addEventListener("DOMContentLoaded", function () {
  var hidden_form_items = document.getElementsByClassName("formstarthidden");
  for (item of hidden_form_items) {
    item.style.display = "none";
  }

  const query_form = document.forms["query_form"];
  const sourceDropdown = document.getElementById("id_datasource");
  const destDropdown = document.getElementById("id_datadest");
  const submitButton = document.getElementById("query-form-submit-button");
  const setSourceValues = createDropdownValuesSetter({
    dropdownElement: sourceDropdown,
    placeholder: "Select a source",
  });
  const setDestinationValues = createDropdownValuesSetter({
    dropdownElement: destDropdown,
    placeholder: "Select a destination",
  });

  function get_selected_datatype() {
    let selected_radio_item = query_form.querySelector(
      'input[name="datatype"]:checked'
    );
    return selected_radio_item === null ? null : selected_radio_item.value;
  }

  if (!(sourceDropdown && destDropdown)) {
    console.error(
      "Missing expected form elements - id_datasource and id_datadest"
    );
    return;
  }

  function saveFormState() {
    if (get_selected_datatype()) {
      try {
        sessionStorage.setItem("selectedType", get_selected_datatype());
        sessionStorage.setItem("selectedSource", sourceDropdown.value);
        sessionStorage.setItem("selectedDest", destDropdown.value);
      } catch (e) {
        console.log("Session storage not available; form contents may reset");
      }
    }
  }

  // Add an event listener so that when the content type is chosen, a list of known sources is populated
  // for the next step
  let last_datatype = null;
  query_form.addEventListener("change", function () {
    var hidden_form_items = document.getElementsByClassName("formstarthidden");
    for (item of hidden_form_items) {
      item.style.display = "block";
    }
    new_datatype = get_selected_datatype();
    if (new_datatype != null && new_datatype != last_datatype) {
      last_datatype = new_datatype;
      datatype_lookup_key = new_datatype.replace(/_/g, " ");
      setSourceValues(Object.keys(queryStructure[datatype_lookup_key]));
      setDestinationValues([]);
      submitButton.removeAttribute("disabled");
    }
  });

  // Then when the source for data is chosen, a list of destinations
  sourceDropdown.addEventListener("change", function () {
    saveFormState();
    datatype_lookup_key = get_selected_datatype().replace(/_/g, " ");
    setDestinationValues(
      queryStructure[datatype_lookup_key][sourceDropdown.value]
    );
  });

  destDropdown.addEventListener("change", saveFormState);

  // Restore form state
  function restoreFormState() {
    try {
      let selectedType = sessionStorage.getItem("selectedType");
      if (selectedType) {
        let todo_radio_item = query_form.querySelector(
          "input[value=selectedType]"
        );
        todo_radio_item.select();
        setSourceValues(Object.keys(queryStructure[selectedType]));
      }
      let selectedSource = sessionStorage.getItem("selectedSource");
      if (selectedSource && selectedSource !== sourceDropdown.value) {
        sourceDropdown.value = selectedSource;
        setDestinationValues(queryStructure[selectedType][selectedSource]);
      }
      let selectedDest = sessionStorage.getItem("selectedDest");
      if (selectedDest && selectedDest !== destDropdown.value) {
        destDropdown.value = selectedDest;
      }
    } catch (e) {
      console.log(
        "Error restoring form state - sessionStorage may not be available",
        e
      );
    }
  }

  // Call this function when the page loads in case it loads from a "back" action
  restoreFormState();

  let askForArticle = document.getElementById("askforarticle");
  askForArticle.style.display = "none";
  let didNotFind = document.getElementById("didnotfind");
  didNotFind.addEventListener("click", function () {
    askForArticle.style.display = "inline";
  });
});
