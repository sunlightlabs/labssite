/*
 * fancytags.js
 * By James Turk <jturk@sunlightfoundation.com>
 * Copyright 2009 Sunlight Foundation
 * MIT Licensed: http://www.opensource.org/licenses/mit-license.php
 *
 * 0.1 - July 29 2009
 */
fancytags = function(tag_input_selector, options) {
    var settings = jQuery.extend({
        fancy_tags_div: '#fancy_tags_widget',
        separator: ', ',
        illegal_char_regex: /,/g,
    }, options);

    // derived selectors
    var tag_list_selector = settings.fancy_tags_div + ' ul';
    var tag_button_selector = settings.fancy_tags_div + ' button';
    var add_tag_box_selector = settings.fancy_tags_div + ' input';

    var tag_list = jQuery(tag_list_selector);
    var tag_input = jQuery(tag_input_selector);

    // add li for a tag
    var add_tag_li = function(tag) {
        tag_list.append('<li><span class="delete">delete</span>' + tag +
                        '</span></li>');
    }

    // take contents of all tags and convert into a comma delimited list
    var rebuild_tag_input = function() {
        var tag_names = tag_list.children().contents().not('span');
        tag_names = jQuery.map(tag_names, function(n){ return n.textContent;});
        tag_input.val(tag_names.join(settings.separator));
    }

    // add click handler to all delete buttons
    var make_deletes_clickable = function () {
        jQuery('.delete').click(function() {
            jQuery(this).parent().remove();
            rebuild_tag_input();
        });
    }

    // made tag button work as expected
    jQuery(tag_button_selector).click(function(event) {
        event.preventDefault();
        var new_tag = jQuery(add_tag_box_selector).val();
        if(new_tag) {
            new_tag = new_tag.replace(settings.illegal_char_regex, '');
            jQuery(add_tag_box_selector).val('');
            add_tag_li(new_tag);
            make_deletes_clickable();
            rebuild_tag_input();
        }
    });

    // convert input to list
    var cur_tags = tag_input.val();
    if(cur_tags) {
        var tags = cur_tags.split(settings.separator);
        for(var i=0; i < tags.length; ++i) {
            add_tag_li(tags[i]);
        }
    }


    // hide list and show
    tag_input.hide();
    //$(settings.fancy_tag_div).show();

    make_deletes_clickable();
};
