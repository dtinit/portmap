/* global queryStructure */

function createOptionElement(text, value = text) {
  const element = document.createElement('option');
  return Object.assign(element, { text, value });
}

function getSourceDestinationMapForDatatype(datatype) {
  return queryStructure && queryStructure[datatype.replace(/_/g, ' ')];
}

function getAvailableSourcesForDatatype(datatype) {
  const map = getSourceDestinationMapForDatatype(datatype);
  return map && Object.keys(map);
}

function getAvailableDestinationsForSource({ datatype, source }) {
  const map = getSourceDestinationMapForDatatype(datatype);
  return map && map[source];
}

function safelySetSessionStorageItem(key, item) {
  try {
    sessionStorage.setItem(key, item);
  } catch (e) {
    console.error('Failed to set sessionStorage item', e);
  }
}

function safelyGetSessionStorageItem(key) {
  try {
    return sessionStorage.getItem(key);
  } catch (e) {
    console.error('Failed to get sessionStorage item', e);
    return null;
  }
}

// query_form.js handles populating the query form dropdowns on index.html,
// as well as saving form state to session storage to smooth the user experience.
// Dropdowns are filled based on selections so far, rather than show all options
// some of which are invalid for the content type chosen.
function createDropdownValuesSetter({
  dropdownElement,
  placeholder = 'Select an option',
}) {
  return function setDropdownValues(possibleValues) {
    dropdownElement.innerHTML = '';
    const uniqueValues = Array.from(new Set(possibleValues));
    const optionElements = [createOptionElement(placeholder, '')].concat(
      uniqueValues.map((value) => createOptionElement(value))
    );
    dropdownElement.append(...optionElements);
    dropdownElement.disabled = uniqueValues.length === 0;
  };
}

document.addEventListener('DOMContentLoaded', function () {
  var hidden_form_items = document.getElementsByClassName('formstarthidden');
  for (let item of hidden_form_items) {
    item.style.display = 'none';
  }

  const query_form = document.forms['query_form'];
  const sourceDropdown = document.getElementById('id_datasource');
  const destDropdown = document.getElementById('id_datadest');
  const submitButton = document.getElementById('query-form-submit-button');
  const setSourceValues = createDropdownValuesSetter({
    dropdownElement: sourceDropdown,
    placeholder: 'Select a source',
  });
  const setDestinationValues = createDropdownValuesSetter({
    dropdownElement: destDropdown,
    placeholder: 'Select a destination',
  });

  function getSelectedDatatype() {
    const selectedRadioItem = query_form.querySelector(
      'input[name="datatype"]:checked'
    );
    return selectedRadioItem && selectedRadioItem.value;
  }

  if (!(sourceDropdown && destDropdown)) {
    console.error(
      'Missing expected form elements - id_datasource and id_datadest'
    );
    return;
  }

  function populateSourceListForDatatype(datatype) {
    for (let item of hidden_form_items) {
      item.style.display = 'block';
    }
    setSourceValues(getAvailableSourcesForDatatype(datatype));
    setDestinationValues([]);
    submitButton.removeAttribute('disabled');
  }

  function populateDestinationListForSource(source) {
    setDestinationValues(
      getAvailableDestinationsForSource({
        datatype: getSelectedDatatype(),
        source,
      })
    );
  }

  function restoreFormState(datatype) {
    const typeRadioItem = query_form.querySelector(`input[value=${datatype}]`);
    if (!typeRadioItem) {
      return;
    }
    typeRadioItem.checked = true;
    populateSourceListForDatatype(datatype);
    const storedSource = safelyGetSessionStorageItem('selectedSource');
    if (!storedSource) {
      return;
    }
    const sources = getAvailableSourcesForDatatype(datatype);
    if (!sources.includes(storedSource)) {
      // The stored source doesn't match what's available for this datatype
      return;
    }
    sourceDropdown.value = storedSource;
    populateDestinationListForSource(storedSource);
    const storedDest = safelyGetSessionStorageItem('selectedDest');
    if (!storedDest) {
      return;
    }
    const destinations = getAvailableDestinationsForSource({
      datatype,
      source: storedSource,
    });
    if (destinations.includes(storedDest)) {
      destDropdown.value = storedDest;
    }
  }

  // If there's a data type already selected (like after a refresh),
  // populate the dropdowns
  let lastDatatype =
    getSelectedDatatype() || safelyGetSessionStorageItem('selectedType');
  if (lastDatatype) {
    restoreFormState(lastDatatype);
  }

  // Add an event listener so that when the content type is chosen, a list of known sources is populated
  // for the next step
  query_form.addEventListener('change', function () {
    const newDatatype = getSelectedDatatype();
    if (newDatatype !== null && newDatatype !== lastDatatype) {
      lastDatatype = newDatatype;
      populateSourceListForDatatype(newDatatype);
      safelySetSessionStorageItem('selectedType', newDatatype);
    }
  });

  // Then when the source for data is chosen, a list of destinations
  sourceDropdown.addEventListener('change', function () {
    populateDestinationListForSource(sourceDropdown.value);
    safelySetSessionStorageItem('selectedSource', sourceDropdown.value);
  });

  destDropdown.addEventListener('change', function () {
    safelySetSessionStorageItem('selectedDest', destDropdown.value);
  });

  let askForArticle = document.getElementById('askforarticle');
  askForArticle.style.display = 'none';
  let didNotFind = document.getElementById('didnotfind');
  didNotFind.addEventListener('click', function () {
    askForArticle.style.display = 'inline';
  });
});
