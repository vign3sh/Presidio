document.getElementById("add").onclick = function() {
    //First things first, we need our text:
    var t = $("#ques").val(); 
    $("#ques").val(''); //Clears the input field
    $("#ques_list").append(`<li>${t}</li>`)
    var ques=$("#questions").val();
    if (ques){
        // convert json to js object
        var ques = JSON.parse(ques);
    }
    else{
        var ques = [];
    }
    // add new question to the list
    ques.push(t);
    // convert js object to json
    ques = JSON.stringify(ques);
    // update the hidden input field
    $("#questions").val(ques);
    // enable the submit button
    $("#getAnswer").prop("disabled", false);
    
}

