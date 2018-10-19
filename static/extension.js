var solution_positions = {};

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    var isMouseDown = false,
        solution = [],
        isHighlighted;
    $("#board td")
        .mousedown(function () {
            isMouseDown = true;
            solution = [];
            var highlighted = $( ".highlighted" );
            highlighted.removeClass("highlighted");
            $(this).toggleClass("highlighted");
            isHighlighted = $(this).hasClass("highlighted");
            if(isHighlighted){
                solution.push($(this).text())
            }
            return false; // prevent text selection
        })
        .mouseover(function () {
            if (isMouseDown) {
                $(this).toggleClass("highlighted", isHighlighted);
            }
            if(isHighlighted){
                solution.push($(this).text())
            }
        })
        .bind("selectstart", function () {
            return false;
        });
    $("#board td")
        .mouseup(function () {
            isMouseDown = false;
            if (solution.length > 0) {
                text = solution.join('');
                $.ajax({
                    method: "POST",
                    url: "/validate",
                    data: {data : text}
                }).done(function (response) {
                    var highlighted = $( ".highlighted" );
                    if(response == "true"){
                        // highlight cells in green
                        highlighted.addClass("correct");
                        highlighted.removeClass("highlighted");
                    }else{
                        highlighted.addClass("wrong");
                        highlighted.removeClass("highlighted");
                        setTimeout(function(){
                            highlighted.removeClass("wrong");
                        },2000);

                    }
                });
            }
        });
});

function getSolution(){
    $.ajax({
        method: "POST",
        url: "/solution",
    }).done(function (response) {
        response = JSON.parse(response);
        $("#main").append('<h3 id="solution" class="display-5" style="margin-top: 1rem">Die Lösungen unseres Systems sind </h3>');
        $("#main").append('<ul class="list-group row">')
        for(var i in response){
            var sol = response[i];
            if(!(sol[0] in solution_positions)){
                solution_positions[sol[0]] = {
                    'positions': [{
                        'direction': sol[1],
                        'col': sol[2],
                        'row': sol[3]
                    }]
                };
                $("#main").append('<li class="list-group-item col-sx-6" onclick="getPosition(this.textContent)">' + sol[0] + '</li>');
            }else{
                solution_positions[sol[0]]['positions'].push({
                        'direction': sol[1],
                        'col': sol[2],
                        'row': sol[3]
                });
            }
        }
        $("#main").append('</ul>')
        $("#fakeloader").hide();
    });
}

function getPosition(key){
    if(key in solution_positions){
        var cells_correct = [];
        var positions = solution_positions[key]['positions'];
        var rows = $('tr');
        var cells = [];
        for(var l = 0; l < rows.length; l++){
            cells.push(rows[l].children)
        }

        for(var i=0; i < positions.length; i++){
            var pos = positions[i];
            var direction = pos['direction'];

            for(var j=0; j < key.length; j++){
                if(direction == 'up'){
                    cells_correct.push(cells[pos['row']-j][pos['col']]);
                }else if(direction == 'down'){
                    cells_correct.push(cells[pos['row']+j][pos['col']]);
                }else if(direction == 'right'){
                    cells_correct.push(cells[pos['col']][pos['row']+j]);
                }else if(direction == 'left'){
                    cells_correct.push(cells[pos['col']][pos['row']-j]);
                }
            }
        }
        for(var k=0; k < cells_correct.length; k++){
            var cell = $(cells_correct[k]);
            cell.addClass("sol");
        }
        $('html, body').animate({ scrollTop: 0 }, 'fast');
        setTimeout(function(){
            $('.sol').removeClass("sol");

        },3000);
    }
    console.log(key);
}

$('.btn').on('click', function() {
   $("#fakeloader").fakeLoader({

        timeToHide: 1200000,

        zIndex: "999",

        spinner: "spinner1",

        bgColor: "#DAD4FF"
    });
});