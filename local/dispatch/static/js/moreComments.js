function moreComments() {
    var nC = document.createElement("div");
    nC.className = "prof";
    var img = document.createElement("div");
    img.style.width = "30px";
    img.style.height = "30px";
    img.style.border = "1px solid";
    img.style.borderRadius = "100%";
    var text = document.createElement("div");
    text.style.marginLeft = "5px";
    text.innerHTML =
        "<b>아기사자</b>리얼로컬<br />저 어제 다녀왔는데 괜찮아요~";
    nC.appendChild(img);
    nC.appendChild(text);

    var commentContainer = document.getElementById("diff").parentNode;
    commentContainer.insertBefore(nC, document.getElementById("diff"));
}

var loadMoreBtn = document.getElementById("diff");
loadMoreBtn.addEventListener("click", moreComments);
