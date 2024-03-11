/* global lucide */

(function () {
  function lucideElement(name) {
    const element = document.createElement('i');
    element.setAttribute('data-lucide', name);
    return element;
  }

  document.addEventListener('DOMContentLoaded', function () {
    const happyButton =
      document.getElementById('id_reaction_0').nextElementSibling;
    const sadButton =
      document.getElementById('id_reaction_1').nextElementSibling;

    // replaces "yes" string with smily face
    happyButton.innerHTML = '';
    happyButton.appendChild(lucideElement('smile'));

    // replaces "no" with frown
    sadButton.innerHTML = '';
    sadButton.appendChild(lucideElement('frown'));

    lucide.createIcons();

    const explanationText = document.getElementById('id_explanation');
    explanationText.hidden = true;
    const explanationLabel =
      explanationText.parentElement.getElementsByTagName('label')[0];
    explanationLabel.style.visibility = 'hidden';

    [happyButton, sadButton].forEach((button) => {
      button.previousElementSibling.addEventListener('change', function () {
        explanationLabel.style.visibility = 'visible';
        explanationText.hidden = false;
      });
    });
  });
})();
