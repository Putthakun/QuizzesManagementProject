const showPopup = document.querySelector('.box_end_test');
const popupContainer = document.querySelector('.popup_container');

showPopup.onclick = () => {
    popupContainer.classList.add('active');
}