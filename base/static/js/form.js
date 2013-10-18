/*global $: false */
/*global console: false */
/*global document: false */
/*global alert: false */
/*global window: false */
/*global navigator: false */

var $datePicker = $('.date-picker');
if ($datePicker.datepicker) {
    $datePicker.datepicker({
        format: "dd/mm/yyyy",
        language: "es"
    });
}

$('.model-form input:text').addClass('form-control');

$('select').not('.filtered').chosen({
    no_results_text: "No hay resultados para",
    width: "95%"
});
