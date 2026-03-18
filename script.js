function vote(option){
fetch('/vote',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({option})
})
.then(res=>res.json())
.then(data=>{
for(let key in data){
document.getElementById(key).innerText = data[key];
}
});
}

function sendMessage(){
let msg = document.getElementById("msg").value;
let box = document.getElementById("chatBox");

box.innerHTML += "<p><b>You:</b> "+msg+"</p>";

fetch('/ai',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({message:msg})
})
.then(res=>res.json())
.then(data=>{
box.innerHTML += "<p><b>AI:</b> "+data.response+"</p>";
});

document.getElementById("msg").value="";
}