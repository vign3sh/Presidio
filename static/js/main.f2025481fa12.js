document.getElementById("add").onclick = function() {
    //First things first, we need our text:
    var text = $("#ques").value; //.value gets input values
    $("#ques").value = ""; //Clears the input field

    //Now construct a quick list element
    var li = "<li>" + text + "</li>";
    var ul=document.getElementById("ques_list");
    $("#ques_list").append(`<li>${text}</li>`)

    
}