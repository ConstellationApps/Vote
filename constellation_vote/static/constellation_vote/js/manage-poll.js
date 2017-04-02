/* global componentHandler Handlebars Sortable */
/* exported addChoice deleteChoice submitPoll */


/*
 * Enable dragging choices around
 */
Sortable.create(document.getElementById('choices-list'), {
  animation: 150,
  handle: '.drag-handle',
});

let source = $('#choice-template').html();
let template = Handlebars.compile(source);

$(function() {
  addChoice();
  $('.datetimefield').datetimepicker({
    onSelect: function() {
      $(this)[0].parentElement.MaterialTextfield.checkValidity();
      $(this)[0].parentElement.MaterialTextfield.checkDirty();
    },
  });
});


/**
 * Add a new choice to the choices-list ul
 */
function addChoice() {
  addChoice.count = ++addChoice.count || 1;       // Like a static var
  let element = template({id: addChoice.count});
  let choice = $(element).appendTo($('#choices-list'));
  componentHandler.upgradeDom();

  /* Turn on remove buttons */
  if ($(choice).siblings().length > 1) {
    $('#choices-list').find('.delete-choice').removeAttr('disabled');
  }
}


/**
 * Delete a choice from the choices-list ul
 * @param {Object} elem - The element to delete
 */
function deleteChoice(elem) {
  let choice = elem.parentNode.parentNode;
  /* Don't allow removing the last choice item */
  let siblings = $(choice).siblings();
  if (siblings.length > 0) {
    choice.remove();
  }
  if (siblings.length <= 2) {
    siblings.find('.delete-choice').attr('disabled', '');
  }
}


/**
 * Put the array in name:value order
 * @param {Array} array - The array to index
 * @return {Array} array - The indexed array
 */
function indexArray(array) {
  let indexedArray = {};
  $.map(array, function(n, i) {
    indexedArray[n['name']] = n['value'];
  });
  return indexedArray;
}

/**
 * Collect the choices and submit them to the backend
 */
function submitPoll() {
  let voteForm = {'choices': []};
  let csrfToken = $.cookie('csrftoken');
  let i = 0;
  $('#poll-holder').find('li').each(function() {
    voteForm.choices[i++] = {
      'text': $(this).find('.choice-title').val(),
      'desc': $(this).find('.choice-desc').val(),
    };
  });
  voteForm['meta'] = indexArray($('#poll-title').serializeArray());
  voteForm['options'] = indexArray($('#poll-options').serializeArray());
  let data = {
    'csrfmiddlewaretoken': csrfToken,
    'data': JSON.stringify(voteForm),
  };
  $.post($(location).attr('href'), data, function(response) {
  });
}
