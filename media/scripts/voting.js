$(function() {
    // get all vote_links
    $('.vote_link').click(function(event) {
        // post to link
        var link = $(this);
        var href = link.attr('href');
        event.preventDefault();

        // do the post
        $.ajax({
           type: 'POST',
           url: href,
           data: {},
           success: function(data, textStatus) {
                // toggle display on success
                link.parent().toggleClass('voted');

                // update # of votes
                data = eval( '(' + data + ')' );
                link.siblings('.voteTotal').text(data.score + ' Votes');

                // switch link
                parts = href.match(/\/((?:un)?vote(?:_up)?)\/(\d+)\//);
                action = parts[1];
                num = parts[2];
                if (action == 'vote_up') {
                    link.attr('href', '/ideas/unvote/' + num + '/');
                } else { 
                    link.attr('href', '/ideas/vote_up/' + num + '/');
                }
            }
            });
        return false;
    });
});
