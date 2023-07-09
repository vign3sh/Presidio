document.getElementById("add").onclick = function() {
    //First things first, we need our text:
    var t = $("#ques").val(); 
    $("#ques").val(''); //Clears the input field
    console.log(t);
    $("#ques_list").append(`<li>${t}</li>`)

    
}