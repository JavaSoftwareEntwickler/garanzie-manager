
document.addEventListener("DOMContentLoaded", function () {

    var modals = document.querySelectorAll('.modal');
    var cards = document.querySelectorAll('.card-garanzie');

    // Variabile per tenere traccia dello stato della modale
    var modalOpen = false;

    // Funzione per disabilitare l'hover sulla card
    function disableHover(card) {
      card.classList.add('no-hover');
    }

    // Funzione per abilitare l'hover sulla card
    function enableHover(card) {
      card.classList.remove('no-hover');
    }

    // Gestione del mouse sopra il bottone "Apri Scontrino"
    cards.forEach(function (card) {
      var button = card.querySelector('[data-bs-toggle="modal"]');

      if (button) {
        button.addEventListener('mouseenter', function () {
          // Disabilita l'hover quando il mouse è sopra il bottone
          disableHover(card);
        });

        button.addEventListener('mouseleave', function () {
          // Riabilita l'hover quando il mouse esce dal bottone
          if (!modalOpen) {
            enableHover(card);
          }
        });
      }
    });

    // Gestione dell'apertura della modale
    modals.forEach(function (modal) {
      modal.addEventListener('show.bs.modal', function () {
        modalOpen = true;
        // Disabilita l'hover sulla card quando la modale si apre
        var cardGaranzie = modal.closest('.card-garanzie');
        if (cardGaranzie) {
          disableHover(cardGaranzie);
        }
      });

      modal.addEventListener('hidden.bs.modal', function () {
        modalOpen = false;
        // Riabilita l'hover sulla card quando la modale si chiude
        var cardGaranzie = modal.closest('.card-garanzie');
        if (cardGaranzie) {
          if (!cardGaranzie.matches(':hover')) {
            enableHover(cardGaranzie);
          }
        }
      });
    });

    // Gestione del mouse sopra la card, quando non c'è una modale aperta
    cards.forEach(function (card) {
      card.addEventListener('mouseenter', function () {
        if (!modalOpen) {
          enableHover(card);
        }
      });

      card.addEventListener('mouseleave', function () {
        if (!modalOpen) {
          enableHover(card);
        }
      });
    });

    // Flash message timeout
    setTimeout(function () {
      var flashMessages = document.querySelectorAll('.alert');
      flashMessages.forEach(function (flashMessage) {
        flashMessage.classList.add('remove-message');
        setTimeout(function () {
          flashMessage.remove();
        }, 1000);
      });
    }, 2000);
});