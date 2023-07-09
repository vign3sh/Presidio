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

// When the page loads make a fetch request to get the answer
$(document).ready(function(){
    var texts=$('#texts').val()

    //make a fetch request with JSON data of texts
    fetch('/encode', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        body: JSON.stringify({texts: texts})
    }).then(function(response){
        //convert response to json
        response.json().then(function(data){
            //update the answer
            $("#answer").text(data.answer);
        })
    });
});