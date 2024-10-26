document.addEventListener("DOMContentLoaded", () => {
    const showPopup = document.querySelector('.box_end_test');
    const popupContainer = document.querySelector('.popup_container');
    const popupClose = document.querySelector('.popup_box_right_tail_btn');

    console.log("showPopup:", showPopup);  // ตรวจสอบค่า showPopup
    console.log("popupContainer:", popupContainer);  // ตรวจสอบค่า popupContainer
    console.log("popupClose:", popupClose);  // ตรวจสอบค่า popupContainer

    if (showPopup && popupContainer) {
        showPopup.onclick = () => {
            popupContainer.classList.add('active');
        };
    } else {
        console.error("Not found!!!");
    }

    if (popupContainer && popupClose) {
        popupClose.onclick = () => {
            popupContainer.classList.remove('active');
        };
    }
});


