function randomNumber(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
var rand = randomNumber(0, 1330)
fetch("https://api-thirukkural.web.app/kural?num=" + rand)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    document.getElementById("line1").innerHTML = data.line1;
    document.getElementById("line2").innerHTML = data.line2;
    document.getElementById("exp").innerHTML = data.tam_exp;
    document.getElementById("chap").innerHTML = data.chap_tam;

  });
window.onload = function () {
  setTimeout(function () {
    document.getElementById("msg").remove();
  }, 2000);

};


var check = function () {
  if (document.getElementById('formGroupExampleInput3').value ==
    document.getElementById('formGroupExampleInput4').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'Password Matched';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = "Password doesn't Match";
  }
};

function copyin(){
  n=document.getElementById("input9").value;
  document.getElementById("input10").value=n;
}
function caps(){
  n=document.getElementById("input5");
  n.style.textTransform="lowercase";


}
function copy() {
  var copyText = document.querySelector("#p1");
  copyText.select();
  document.execCommand("copy");
}

document.querySelector("#copy").addEventListener("click", copy);

// function disable(){
// a=document.getElementById("input12");
// b=document.getElementById("input13");
// if (a.disabled==true && b.disabled==true){
//   a.disabled=false;
//   b.disabled=false;
// }
// else{
//   a.disabled=true;
//   b.disabled=true;
//   var bn=document.createElement("input")
//   bn.name="input12"
//   bn.value=null
//   bn.hidden=true
//   document.body.appendChild(bn);
//   var exp=document.createElement("input")
//   exp.name="input13"
//   exp.value=null
//   bn.hidden=true
//   document.body.appendChild(exp);
// }

// }


// window.onload = function () {
//   a=document.getElementById("input12");
//   b=document.g