odoo.define('hr_recruitment_tai.website_welcome', function (require) {
    'use strict';

    require('website.editMenu');
    var websiteNavbarData = require('website.navbar');

    var menus = websiteNavbarData.websiteNavbarRegistry.get();

   /* _.map(menus, function (menu) {
        if (menu.selector === '#edit-page-menu') {
            menu.Widget.include({
                xmlDependencies: ['/website/static/src/xml/website.editor.xml',
                    '/hr_recruitment_tai/static/xml/templates.xml'],
                start: function () {
                    var def = this._super.apply(this, arguments);

                    // If we auto start the editor, do not show a welcome message
                    this.$welcomeMessage.html('<img src="/hr_recruitment_tai/static/src/img/hr.jpeg" style="height: 500px; width: 400px;"/>')
                    return def;
                },
            })
        }
    });*/
});


odoo.define('hr_recruitment_tai.ResumeEditor', function (require) {
"use strict";

require('web.dom_ready');

var core = require('web.core');
var session = require('web.session');

var rpc = require('web.rpc');
var weContext = require('web_editor.context');

if (!$('#referance_list').length) {
    return $.Deferred().reject("DOM doesn't contain '#referance_list'");
}

$('#referance_list button').on('click',function(e){

    var ref_id = $(e.currentTarget).data('ref-id')
    //return session.rpc('/my/resume/update_referance',{"ref_id":ref_id, "param1":"sadsad", "param2":"asda"});

    rpc.query({
            model: 'hr.recruitment.candidate.referance',
            method: 'read',
            args: [
                [ref_id],
                ['name']
            ],
            context: weContext.get(), // TODO use this._rpc
        })
        .then(function(data){
            alert(data);
        });

});

});


odoo.define('hr_recruitment_tai.ResumeEditorAddress', function (require) {
"use strict";

require('web.dom_ready');

var core = require('web.core');
var session = require('web.session');

var rpc = require('web.rpc');
var weContext = require('web_editor.context');

if (!$('#province_id').length) {
    return $.Deferred().reject("DOM doesn't contain '#province_id'");
}


//sayfa yenilendiğinde seçili değerleri tekrar kullanmak için localStorage yaptık.
localStorage.setItem("province", $('#province_id').val());
// ülke seçtiğimizde şehirler id ile eşleşip geliyor. Selection'a döngü ile ekleniyor. Ama selected değeri kaybediyoruz.
// O yuzden bu değeri aldım sonra kullanacağız
localStorage.setItem("selectedCity",$('#city_id').find(":selected").val());



$('#province_id').on('change',function(e){

    var country_id = parseInt($(e.currentTarget).val());
    //return session.rpc('/my/resume/update_referance',{"ref_id":ref_id, "param1":"sadsad", "param2":"asda"});

    rpc.query({
            model: 'res.country.state',
            method: 'search_read',
            args: [
                [['country_id','=',country_id]],
                ['name']
            ],
            context: weContext.get(), // TODO use this._rpc
        })
        .then(function(data){

            //Önce şehir combosunu boşaltıyoruz.
            $("#city_id").empty();
            var city_id = document.getElementById('city_id');

            //rpc.query ile başlayan kod bloğundan gelen data object olduğu için Stringe çeviriyoruz. JSON.stringify ile
            // localStorage için Object ve List stringe dönüştürülmeli
            localStorage.setItem("dataa",JSON.stringify(data));
            //datadan gelen her bir şehir bilgisini döngü ile option olarak comboya ekliyoruz
            data.forEach(function(element) {
                city_id.options[city_id.options.length] = new Option(element.name, element.id);
              });
            //seçili şehir, ülke değiştirildekten sonra tekrar gelsin diye aşağıdaki kodu ekledim. Çok önemli bir case değil
            $("#city_id").val(localStorage.getItem("selectedCity"));

        });

});

// sayfa yenilendiği zaman bu fonksiyon çalışıyor.
// şehirleri tekrar listelemek için. (burası daha efektif olabilir. aynı işlemi tekrar yapmamak için)
// en son satırda daha önce seçilmiş değeri set ediyor comboya
$('#province_id').ready(function(){

    $("#city_id").empty();
    var city_id = document.getElementById('city_id');
    JSON.parse(window.localStorage.getItem("dataa")).forEach(function (element) {
         city_id.options[city_id.options.length] = new Option(element.name, element.id);
    })
    $("#city_id").val(localStorage.getItem("selectedCity"));

});

});

 //uygun olmayan alanlar için mesaj verme fonksiyonu
 (function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    if(forms){
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });}
  }, false);
})();


 window.onload= function (){

     // is tecrübesi varsa staj bilgisi girilmemesi
     var company_name = document.getElementById("company_name_i").value;
     if (company_name.length > 0)
     {
         document.getElementById("step10").disabled = true;
     }


     //  seklemere tıklayınca sayfa yenilenmeden linklerin değişmesini sağlıyor. .collapse ile tıklanan sekmenin içeriğini açıyor.
     $('#step1').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step1');
       $('.collapse').collapse('#collapseOne')
       return false;
     });
     $('#step2').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step2');
       $('.collapse').collapse('#collapseTwo')
       return false;
     });
     $('#step3').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step3');
       $('.collapse').collapse('#collapseThree')
       return false;
     });
     $('#step4').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step4');
       $('.collapse').collapse('#collapseFour')
       return false;
     });
     $('#step5').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step5');
       $('.collapse').collapse('#collapseFive')
       return false;
     });
     $('#step6').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step6');
       $('.collapse').collapse('#collapseSix')
       return false;
     });
     $('#step7').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step7');
       $('.collapse').collapse('#collapseSeven')
       return false;
     });
     $('#step8').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step8');
       $('.collapse').collapse('#collapseEight')
       return false;
     });
     $('#step9').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step9');
       $('.collapse').collapse('#collapseNine')
       return false;
     });
     $('#step10').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step10');
       $('.collapse').collapse('#collapseTen')
       return false;
     });
     $('#step11').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step11');
       $('.collapse').collapse('#collapseEleven')
       return false;
     });
     $('#step12').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step12');
       $('.collapse').collapse('#collapseTwelve')
       return false;
     });
     $('#step13').click(function() {
       window.history.pushState('obj', 'PageTitle', '/my/resume/step13');
       $('.collapse').collapse('#collapse13')
       return false;
     });


     // sekmelere tıklayınca link değişmesi için yapılmıştı. Üsteki satırlar çalışınca iptal ettik
     // $('#step1').click(function(){ window.location.replace( '/my/resume/step1')});
     // $('#step2').click(function(){ window.location.replace('/my/resume/step2')});
     // $('#step3').click(function(){ window.location.replace('/my/resume/step3')});
     // $('#step4').click(function(){ window.location.replace('/my/resume/step4')});
     // $('#step5').click(function(){ window.location.replace('/my/resume/step5')});
     // $('#step6').click(function(){ window.location.replace('/my/resume/step6')});
     // $('#step7').click(function(){ window.location.replace('/my/resume/step7')});
     // $('#step8').click(function(){ window.location.replace('/my/resume/step8')});
     // $('#step9').click(function(){ window.location.replace('/my/resume/step9')});
     // $('#step10').click(function(){ window.location.replace('/my/resume/step10')});
     // $('#step11').click(function(){ window.location.replace('/my/resume/step11')});
     // $('#step12').click(function(){ window.location.replace('/my/resume/step12')});
     // $('#step13').click(function(){ window.location.replace('/my/resume/step13')});

     //Your entire JS code here
     //for Input Filter
     var exam_id = document.getElementById('eng_exam').value
     if (exam_id == ""){
         document.getElementById("eng_score_id").required = false;
         document.getElementById("eng_score_id").value = null;
         document.getElementById("eng_score_id").style.visibility = "hidden";
         document.getElementById("eng_exam_date").required = false;
         document.getElementById("eng_exam_date").value = null;
         document.getElementById("eng_exam_date").style.visibility = "hidden";
         document.getElementById("eng_score_lb_id").style.visibility = "hidden";
         document.getElementById("eng_exam_date_id").style.visibility = "hidden";
     }
     else{
         document.getElementById("eng_score_id").required = true;
         document.getElementById("eng_score_id").disabled = false;
         document.getElementById("eng_score_id").style.visibility = "visible";
         document.getElementById("eng_exam_date").required = true;
         document.getElementById("eng_exam_date").disabled = false;
         document.getElementById("eng_exam_date").style.visibility = "visible";
         document.getElementById("eng_score_lb_id").style.visibility = "visible";
         document.getElementById("eng_exam_date_id").style.visibility = "visible";
     }


function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      }
    });
  });
}


// Install input filters.
setInputFilter(document.getElementById("tckn"), function(value) {
  return /^\d*$/.test(value); });
setInputFilter(document.getElementById("disability_percentage"), function(value) {
  return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 100); });
setInputFilter(document.getElementById("zip_code"), function(value) {
  return /^\d*$/.test(value); });

// setInputFilter(document.getElementById("intLimitTextBox"), function(value) {
//   return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 500); });
// setInputFilter(document.getElementById("intTextBox"), function(value) {
//   return /^-?\d*$/.test(value); });
// setInputFilter(document.getElementById("floatTextBox"), function(value) {
//   return /^-?\d*[.,]?\d*$/.test(value); });
// setInputFilter(document.getElementById("currencyTextBox"), function(value) {
//   return /^-?\d*[.,]?\d{0,2}$/.test(value); });
// setInputFilter(document.getElementById("basicLatinTextBox"), function(value) {
//   return /^[a-z]*$/i.test(value); });
// setInputFilter(document.getElementById("extendedLatinTextBox"), function(value) {
//   return /^[a-z\u00c0-\u024f]*$/i.test(value); });
// setInputFilter(document.getElementById("hexTextBox"), function(value) {
//   return /^[0-9a-f]*$/i.test(value); });
}



//sınav varsa ilgili alanların gözükmesi
function engSetting(exam_id) {
     var eng_score = document.getElementById("eng_score_id")
     var eng_date  = document.getElementById("eng_exam_date")
     if (exam_id == ""){
         eng_score.required = false;
         eng_score.value = null;
         eng_score.style.visibility = "hidden";
         eng_date.required = false;
         eng_date.value = null;
         eng_date.style.visibility = "hidden";
         document.getElementById("eng_score_lb_id").style.visibility = "hidden";
         document.getElementById("eng_exam_date_id").style.visibility = "hidden";
     }
     else{
         eng_score.required = true;
         eng_score.disabled = false;
         eng_score.style.visibility = "visible";
         eng_date.required = true;
         eng_date.disabled = false;
         eng_date.style.visibility = "visible";
         document.getElementById("eng_score_lb_id").style.visibility = "visible";
         document.getElementById("eng_exam_date_id").style.visibility = "visible";
     }
}

function otherLangSetting(o_lan_id) {
     var o_lan_lbl = document.getElementById("o_lan_label")
     var o_lan_lvl  = document.getElementById("o_lan_level")
     if (o_lan_id == ""){
         o_lan_lvl.required = false;
         o_lan_lvl.selectedIndex = 0;
         o_lan_lvl.style.visibility = "hidden";
         o_lan_lbl.style.visibility = "hidden";
     }
     else{
         o_lan_lvl.required = true;
         o_lan_lvl.disabled = false;
         o_lan_lvl.style.visibility = "visible";
         o_lan_lbl.style.visibility = "visible";
     }
}


//disability
function disSetting(dis_statu) {

     if (dis_statu == "non"){

         document.getElementById("dis_col").required = false;
         document.getElementById("dis_col").value = null;
         document.getElementById("dis_col").style.visibility = "hidden"
         document.getElementById("dis_button").style.position = "absolute";
         document.getElementById("dis_button").style.marginTop = 30;
         document.getElementById("dis_button").style.right=0;
         $( "#dis_button" ).insertAfter( $( "#dis_statu" ) );
         // document.getElementById("dis_col").disabled = true;
     }
     else{
         document.getElementById("dis_col").required = true;
         document.getElementById("dis_col").disabled = false;
         document.getElementById("dis_col").style.visibility = "visible";
         $( "#dis_button" ).insertAfter( $( "#blocking_illness_id" ) );
     }
}



function checkEmail() {

    var email = document.getElementById('txtEmail');
    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    if (!filter.test(email.value)) {
    // getElementById('invalid-email').style.visibility = "visible";
    // getElementById('invalid-email').style.color = "red";
    alert('Please provide a valid email address');
    email.focus;
    return false;
 }}