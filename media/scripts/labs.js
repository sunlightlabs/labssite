var GB_ANIMATION = true;
$(document).ready(function(){

    $("div#leadBox").hide();
    $("div#favoritePosts").hide();
    $("div#advancedSearch").hide();

    //$("form#standard_signupForm").hide();
    //$("form#standard_signinForm").hide();
    
    $("button.startnewBtn").click(function(){
        $("div#leadBox").toggle("slow");
    });

    $("li#signup_standard a").click(function(){
        $("form#openid_signupForm").hide();
        $("form#standard_signupForm").show();
    });

    $("li#signup_openid a").click(function(){
        $("form#standard_signupForm").hide();
        $("form#openid_signupForm").show();
    });

    $("li#signin_standard a").click(function(){
        $("form#openid_signinForm").hide();
        $("form#standard_signinForm").show();
        return false;
    });

    $("li#signin_openid a").click(function(){
        $("form#standard_signinForm").hide();
        $("form#openid_signinForm").show();
    });

    $("a#advancedBtn").click(function(){
        $("div#advancedSearch").toggle("slow");
    });

    $("li#favorites a").click(function(){
        $("div#popularPosts").hide();
        $("li#popular a").attr('class', 'inactive');
        $("div#favoritePosts").show();
        $("li#favorites a").attr('class', 'active');
    });

    $("li#popular a").click(function(){
        $("div#favoritePosts").hide();
        $("li#favorites a").attr('class', 'inactive');
        $("div#popularPosts").show();
        $("li#popular a").attr('class', 'active');
    });

});
