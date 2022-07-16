
window.onload = function(){

const activePage = window.location.pathname;
console.log(activePage);

 document.querySelectorAll('a').forEach(link => {
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
});

}

function changeColreblue(){
  // document.getElementById("container").classList.add('containerr')
  document.getElementById("container").style.backgroundColor = "rgb(139, 139, 226)"
  document.getElementById('hed').style.color = "rgb(139, 139, 226)";
}

function changeColrered(){
  // document.getElementById("container").classList.add('containerr')
  document.getElementById("container").style.backgroundColor = "rgb(201, 78, 78)"
  document.getElementById('hed').style.color ="rgb(201, 78, 78)";

}

function changeColreyellw(){
  // document.getElementById("container").classList.add('containerr')
  document.getElementById("container").style.backgroundColor = "rgb(148, 209, 7)"
  document.getElementById('hed').style.color = "rgb(148, 209, 7)";

}

function changeColreperppel(){
  // document.getElementById("container").classList.add('containerr')
  document.getElementById("container").style.backgroundColor = "rgb(221, 18, 211)"
  document.getElementById('hed').style.color = "rgb(221, 18, 211)";

}

