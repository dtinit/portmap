(function () {
  document.addEventListener('DOMContentLoaded', function () {
    const happyButton =
      document.getElementById('id_reaction_0').nextElementSibling;
    const sadButton =
      document.getElementById('id_reaction_1').nextElementSibling;

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
