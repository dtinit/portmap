
function lucideElement(name) {
  element = document.createElement('i');
  element.setAttribute('data-lucide', value=name);
  return element
}

document.addEventListener('DOMContentLoaded', function() {
  let happyButton = document.getElementById("id_reaction_0");
  let sadButton = document.getElementById("id_reaction_1");

  happyButton.nextSibling.replaceWith(lucideElement('smile'));  // replaces "yes" string with smily face
  sadButton.nextSibling.replaceWith(lucideElement('frown'));  // replaces "no" with frown

  lucide.createIcons();

  let explanationText = document.getElementById("id_explanation");
  explanationText.hidden=true;
  let explanationLabel = explanationText.parentElement.getElementsByTagName('label')[0];
  explanationLabel.style.visibility = "hidden";

  sadButton.addEventListener("change", function() {
    explanationLabel.style.visibility = "visible";
    explanationText.hidden=false;
  });
})
