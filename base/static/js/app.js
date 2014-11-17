var App = {};
var app;

(function() {
  app = {
    data: {},
    messages: {},
    forms: {
      datepicker: {
        format: 'dd/mm/yyyy',
        language: 'es',
        autoclose: true
      },
      dateTimePicker: {
        language: 'es'
      }
    }
  };

  app.utils = {
    hideLoading: function() {
      $('body').removeClass('wait');
    },

    thousandSeparator: function(x) {
      x = Math.round(x);
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },

    showLoading: function() {
      $('body').addClass('wait');
    },

    highlight: function($el) {
      $el.addClass('highlight');
      setTimeout(function() {
        $el.toggleClass('dim highlight');
      }, 15);
      setTimeout(function() {$el.removeClass('dim');}, 1010);
    }
  };

  $('.hidden').hide().removeClass('hidden');

  $('.alert').each(function() {
    app.utils.highlight($(this));
  });
}());
