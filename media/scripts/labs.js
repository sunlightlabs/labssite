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

    make_toggle = function(pairs) {
        // attach event to each link in pairs
        for(var i=0; i < pairs.length; ++i) {
            click_response = function(event) {
                event.preventDefault();

                // deactivate all others
                for(var j=0; j < pairs.length; ++j) {
                    var link = $(pairs[j][0]);
                    if($(this).parent()[0].id != link.parent()[0].id) {
                        $(pairs[j][0]).attr('class', 'inactive');
                        $(pairs[j][1]).hide();
                    } else {
                        $(this).attr('class', 'active');
                        $(pairs[j][1]).show();
                    }
                }
            }
            $(pairs[i][0]).click(click_response);
        }
        $(pairs[0][0]).click();  // click first as default
    }

    make_toggle([["li#popular a", "div#popularPosts"],
                 ["li#favorites a", "div#favoritePosts"]]);
    make_toggle([["li#signup_standard a", "form#standard_signupForm"],
                 ["li#signup_openid a", "form#openid_signupForm"],
                 ["li#signup_google a", "form#google_signupForm"],
                 ["li#signup_yahoo a", "form#yahoo_signupForm"],
                 ["li#signup_aol a", "form#aol_signupForm"]]);
    make_toggle([["li#signin_standard a", "form#standard_signinForm"],
                 ["li#signin_openid a", "form#openid_signinForm"],
                 ["li#signin_google a", "form#google_signinForm"],
                 ["li#signin_yahoo a", "form#yahoo_signinForm"],
                 ["li#signin_aol a", "form#aol_signinForm"]]);

    // convert AOL box to screen-name only
    function aol_openid() {
        $('#aol_url').val('');
        $('#aol_signupForm, #aol_signinForm').submit(function() {
            $('#aol_url').val('http://openid.aol.com/' + $('#aol_url').val());
        });
    }
    aol_openid();
});
