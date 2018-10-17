$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    var isMouseDown = false,
        solution = [],
        isHighlighted;
    $("#board td")
        .mousedown(function () {
            isMouseDown = true;
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
    $(document)
        .mouseup(function () {
            isMouseDown = false;
            if (solution.length > 0) {
                text = solution.join('');
                $.ajax({
                    method: "POST",
                    url: "/validate",
                    data: {data : text}
                }).done(function (response) {
                    solution = [];
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


$('.btn').on('click', function() {
   $("#fakeloader").fakeLoader({

        timeToHide: 1200000,

        zIndex: "999",

        spinner: "spinner1",

        bgColor: "#DAD4FF"
    });
});