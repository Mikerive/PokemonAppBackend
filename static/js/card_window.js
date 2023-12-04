function displayCardGrid(cardDetailsList) {
  const cardLayout = document.getElementById('card-results');

  cardDetailsList.forEach((cardDetails) => {
    const cardElement = document.createElement('li');
    cardElement.className = 'card';
    cardElement.dataset.id = cardDetails.id;

    const cardImage = document.createElement('img');
    cardImage.src = cardDetails.small_image_url;
    cardElement.appendChild(cardImage);

    // Create and append the card name and number
    const cardName = document.createElement('h3'); // Larger text for the name
    cardName.textContent = `${cardDetails.name}`; // Append the card number to the name
    cardElement.appendChild(cardName);

    const cardNumber = document.createElement('h3');
    cardNumber.textContent = `#${cardDetails.national_pokedex_numbers}`;
    cardElement.appendChild(cardNumber);

    // Create and append the card price
    const cardPrice = document.createElement('p');
    cardPrice.textContent = `Price: ${cardDetails.price}`;
    cardElement.appendChild(cardPrice);

    cardElement.addEventListener('click', () => {
      openModal(cardDetails);
      console.log('Clicked!')
    });

    cardLayout.appendChild(cardElement);
  });
}


function fetchCardsByUserInput(inputStr) {
  return fetch(`/get-cards-by-user-input?input=${inputStr}`)
    .then((response) => response.json())
    .catch((error) => console.error('Error fetching card details:', error));
}

let modalContent;
document.addEventListener('DOMContentLoaded', (event) => {
  const modal = document.getElementById('my-modal');
  modalContent = {
    name: modal.querySelector('.card-modal-name'),
    image: modal.querySelector('.card-modal-image'),
    rarity: modal.querySelector('.card-modal-rarity'),
    artist: modal.querySelector('.card-modal-artist'),
    flavorText: modal.querySelector('.card-modal-flavortext'),
    pokedex: modal.querySelector('.card-modal-pokedex'),
    price: modal.querySelector('.card-modal-price'),
    hp: modal.querySelector('.card-modal-hp'),
    level: modal.querySelector('.card-modal-level'),
    supertype: modal.querySelector('.card-modal-supertype'),
    set: modal.querySelector('.card-modal-set')
  };

  // This function is called when anywhere outside of the modal content is clicked
  window.onclick = function(event) {
    if (event.target === modal) {
      closeModal();
    }
  };
});

function openModal(card) {
  // Safely update content, assuming 'card' always has an 'id' property.
  modalContent.name.textContent = card.name ? `${card.name} (#${card.national_pokedex_numbers})` : 'Name not available';
  modalContent.image.src = card.small_image_url || 'default-image.png'; // Fallback if URL is not provided
  modalContent.rarity.textContent = card.rarity || 'Not specified';
  modalContent.artist.textContent = card.artist || 'Unknown artist';
  modalContent.flavorText.textContent = card.flavor_text || 'No description';
  modalContent.price.textContent = card.price ? `${card.price}` : 'Price unavailable';
  modalContent.hp.textContent = card.hp || 'HP not set';
  modalContent.level.textContent = card.level || 'Level not set';
  modalContent.supertype.textContent = card.supertype || 'Supertype not set';
  modalContent.set.textContent = card.set || 'Set not defined';

  // Open the modal
  const modal = document.getElementById('my-modal');
  modal.style.display = 'block';
}

function closeModal() {
  const modal = document.getElementById('my-modal');
  modal.style.display = 'none';
}
