(function(){
  var $leftBox = $('#text-to-process'),
      $rightBox = $('#output'),
      $rotBox = $('#rot-input'),
      $encodeBtn = $('#encode-btn'),
      $decodeBtn = $('#decode-btn');

  // dimmer presentation

  function showAlert(msg){
    var $alertBox = $('#alert');
    $alertBox.html(msg).
    show().
    delay(2000).
    fadeOut('slow')
  }

  function buildChart(data, guess){ // build chart
    var chart = new FusionCharts( "column2d",
                     "MyChart", "700", "180", "0"),
        chartData = {
          "chart": {"caption": guess,
                    "xAxisName": "Letter",
                    "yAxisName": "percentage",
                    "numberPrefix": "%",
                    "theme": "fint"},
          "data": data
        };
    chart.setJSONData(chartData);
    chart.render("Frequency_chart");
  }

  function isValidEnglishAndPunctuation(text){
      var re = new RegExp('^[A-Za \t-z0-9!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+$');
      return re.test(text)
  }

  function isValidRot(digit){
    var re = new RegExp('^([0-9]|1[0-9]|2[0-6])$');
    return re.test(digit)
  }

  function caesarEncodeApi(encode){
    var url = encode ? 'encode' : 'decode',
        $rotVal = $rotBox.val(),
        leftBoxVal = $leftBox.val();

    if ( isValidEnglishAndPunctuation( leftBoxVal) ){
      if ( isValidRot($rotVal) ){
        $.get( 'api/' + url, { text: leftBoxVal, offset: $rotVal }, function( response ){
          $rightBox.val(response.result)
        });
      } else { showAlert('Invalid rot value'); }
    } else { showAlert('Only english and punctuation') }
  }

  $leftBox.on('blur', function() {
    if (isValidEnglishAndPunctuation($thisVal)) {
      var $thisVal = $(this).val(),
          frequency = $.get('api/frequency', {text: $thisVal}),
          guess     = $.get('api/guess', {text: $thisVal});

      $.when(frequency, guess).done(function (responce1, responce2) {
        var frequencyResponse = responce1[1] == "success" ? responce1[0] : undefined,
            guessResponse = responce2[1] == "success" ? responce2[0] : undefined;

        if (frequencyResponse && guessResponse){
          var data = frequencyResponse.frequency,
              chartHeader;
          if ( !guessResponse.is_encrypted ) {
              chartHeader = 'Looks like text is not encrypted. Choose ROT value and click encode';
            } else {
              chartHeader = 'Looks like text is encrypted. With key ' + guessResponse.best_key +
                            ' for ' + guessResponse.guess_rate + '% we can guess that a beginning of ' +
                            'decrypted text is ' + guessResponse.guess_text.substring(0, 20) + '...';
            }
          buildChart(data, chartHeader);
        }
      });
    } else {
      showAlert('Only english and punctuation')
    }
  });

  $rotBox.on('blur', function () {
    if ( !isValidRot($rotBox.val()) ){
      showAlert('Invalid rot value');
    }
  });

  $encodeBtn.on('click', function () {
    caesarEncodeApi(true)
  });

  $decodeBtn.on('click', function () {
    caesarEncodeApi(false)
  })

})();