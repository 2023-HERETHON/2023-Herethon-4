const positionForm = document.querySelector("#position-form");
const positionInput = document.querySelector("#position-form input");
const tag = document.querySelector("#tag");

function deleteSpot(event) {
    const li = event.target.parentElement;
    // 이벤트가 발생했을 때 해당 객체를 지정하여 그것의 부모 태그 지정 -> 어떤 요소 클릭되었는지 알 수 있음
    li.remove();
}

function paintSpot(travelSpot) {
    const li = document.createElement("li");
    const span = document.createElement("span");
    li.appendChild(span);
    li.style.listStyleType = 'none';
    span.innerHTML = travelSpot;

    const button = document.createElement("button");
    button.innerText = "X";
    button.style.backgroundColor = '#fff';
    button.style.border = '0';
    button.style.color = '#FF552B';

    button.addEventListener("click", deleteSpot);
    li.appendChild(span);
    li.appendChild(button);
    tag.appendChild(li);
    
}

function positionSubmit(event){
    event.preventDefault();
    const travelSpot = positionInput.value;
    positionInput.value = "";
    paintSpot(travelSpot);
}

positionForm.addEventListener("submit",positionSubmit);