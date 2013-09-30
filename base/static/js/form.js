$(document).ready(function () {
    var $datePicker = $('.date-picker')
    if ($datePicker.datepicker) {
        $datePicker.datepicker({
            format: "dd/mm/yyyy"
        });
    }
});
