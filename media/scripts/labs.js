var GB_ANIMATION = true;
$(document).ready(function(){

    $("div#leadBox").hide();
    $("div#advancedSearch").hide();

    $("button.startnewBtn").click(function(){
        $("div#leadBox").toggle("slow");
    });

    $("a#advancedBtn").click(function(){
        $("div#advancedSearch").toggle("slow");
    });

    make_toggle = function(link_a, div_a, link_b, div_b) {
        $(link_a).click(function(){
            $(div_b).hide();
            $(link_b).attr('class', 'inactive');
            $(div_a).show();
            $(link_a).attr('class', 'active');
        }).click();

        $(link_b).click(function(){
            $(div_a).hide();
            $(link_a).attr('class', 'inactive');
            $(div_b).show();
            $(link_b).attr('class', 'active');
        });
    }
    make_toggle("li#popular a", "div#popularPosts",
                "li#favorites a", "div#favoritePosts");
    make_toggle("li#signup_standard a", "form#standard_signupForm",
                "li#signup_openid a", "form#openid_signupForm");
    make_toggle("li#signin_standard a", "form#standard_signinForm",
                "li#signin_openid a", "form#openid_signinForm");

});
