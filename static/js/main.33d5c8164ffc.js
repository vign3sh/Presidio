document.getElementById("add").onclick = function() {
    //First things first, we need our text:
    var text = document.getElementById("ques").value; //.value gets input values

    //Now construct a quick list element
    var li = "<li>" + text + "</li>";

    console.log(li);
    //Now use appendChild and add it to the list!
    //document.getElementById("ques_list").appendChild(li);
    
}