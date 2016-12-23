(function app(){
"use strict";


// Popover / Tooltip for magic search help.
$('[data-toggle="popover"]').popover();


function hide_speeches(ids){
  // Deals with the things.
  $.each(ids, function(index, id){
    $('tr[data-id!='+ id +']').hide();

  })
};

function update_speech_count(amount){
  $('span[id="speech-count"]').html(String(amount));
};

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

// Ajax Call for backend search of the transcripts on keyup
$('#search').on('keyup', function(event){

    if ( $(this).val().length > 2 ) {

      $.ajax({
        url: "/speeches/search/",
        type: 'GET',
        data: {'query': $(this).val()},
        success: function(rsp){
            // hide_speeches(rsp);
            update_speech_count(rsp.length);
        },
        error: function(err){
          alert(err);
        }
        // End Data
        });
        // End Condition len > 2
      }

  });

//End app
})();
