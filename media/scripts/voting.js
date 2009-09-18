$(function() {
    // get all vote_links
    $('.votedBtn, .voteBtn').click(function(event) {
        // post to link
        var form = $(this).parent();
        var idea = form.children('[name=idea]');
        var score = form.children('[name=score]');
        var action = form.attr('action');
        event.preventDefault();

        // do the post
        $.ajax({
           type: 'POST',
           url: action,
           data: {'idea':idea.val(), 'score':score.val()},
           success: function(data, textStatus) {
                // toggle display on success
                form.parent().toggleClass('voted');

                if(score.val() == '0') {
                    score.val('1');
                } else {
                    score.val('0');
                }

                // update # of votes
                data = eval( '(' + data + ')' );
                form.siblings('.voteTotal').text(data.score + ' Votes');

                var span = form.find('.vote_link');
                if(span.text() == 'Vote') {
                    span.text('Unvote');
                } else {
                    span.text('Vote');
                }
            }
            });
    });
});
