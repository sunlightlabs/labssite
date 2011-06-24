var GB_ANIMATION = true;
$(document).ready(function(){

    $("div#leadBox").hide();
    $("div#advancedSearch").hide();

    $("button.startnewBtn").click(function(){
        $("div#leadBox").toggle("slow");
    });

    $("a#advancedBtn").click(function(event){
        $("div#advancedSearch").toggle("slow");
        event.preventDefault();
    });
});
