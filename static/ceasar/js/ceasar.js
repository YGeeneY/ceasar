function send_data(encode) { // AJAX request function
  var formData = $('#ajax-form').serialize(); // data to be send
  $.ajax({
    type: 'GET',
    dataType: 'json',
    url: '',
    data: formData + '&encode=' + encode,
    success: function (data) {

      $('#text_output').text(data.text); //output the translation if exist
      build_chart(data.frequency); // build chart frequency of de/encoded text

      $("#guess").text(data.guess);// try to guess if text encoded
      $("#prewrap").fadeIn(2000);
    },
    error: function (response, error) {
      $('#text_output').text("An error occurred");
      console.log(response);
      console.log(error);
    } // type an error if ajax fail

  }) //end of ajax
}; //end of function

function build_chart(data){ // build chart
  var myChart = new FusionCharts( "column2d",
                   "MyChart", "700", "180", "0" );
  myChart.setJSONData(data)
  myChart.render("Frequency_chart");
};

function offset_valid() { // offset field Validation
  re_offset = /^[0-9]+$/;
  offset = $('#id_offset').val();
  if (re_offset.test(offset) && offset >= 0 && offset != '') {
    $('#id_offset').removeClass("error");
    return true;
  }//end if
  else {
    $('#errorfield').addClass("error"); // message if invalid
    return false;
  }//end of else

}
//end of offset validation

function text_valid() { // text field Validation
  re_text = /^[\w\s,.\-!?;><:$@)(\[\]\"\']+$/; //"\w\s,.\-!?;><':
  text = $('#id_text').val();
  if (re_text.test(text)) {
    $('#id_text').removeClass("error");
    return true;
  }//end if
   else {
    $('#id_text').addClass("error"); // message if invalid
    $('#guess').text("");
    return false;
  }//end of else

}//end of text validation

$('.ajax-btn').click(function (event) { // submitting ajax if form is valid
  event.preventDefault();
  if (text_valid() && offset_valid()) { // check for both fields validation
    var enDe = $(this).val(); //choosing what to do based on buttons value
    send_data(enDe);
  }//end if
   else {
  }//end else


})
$('#id_offset').blur(offset_valid); // dynamic validation

$('#id_text').blur(function(){ // get frquency
if (text_valid()) {
send_data("just_frequency&offset=1")
}
text_valid; //dynamic validation
});
